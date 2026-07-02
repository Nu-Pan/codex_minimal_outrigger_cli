"""Codex exec の単一試行ループを扱う。

このファイルは 16,000 文字を超えるが、Structured Output 検証、capacity
retry、quota 代表 probe、resume 継続は同じ subprocess 結果、call log、
subcommand event、retry counter を共有する 1 つの状態機械である。TUI 起動は
別 module へ分け、exec の分岐だけをここに残すことで責務境界を exec 実行制御
へ限定している。quota 処理だけをさらに分離すると、resume token と log/event
の読み取り文脈が呼び出し元と分断されるため、現状は一体で読む方が凝集性が高い。
根拠: <work-root>/oracle/src/oracle/prompt_builder/parts/realization_standard.py
"""

import hashlib
import json
import os
import subprocess
import threading
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

from jsonschema import validate

from basic.acp import AgentCallParameter, FileAccessMode
from config.cmoc_config import CmocConfig

from commons.runtime_config import load_config
from commons.runtime_codex_profile import (
    codex_error_text,
    codex_profile_name,
    codex_subprocess_env,
    extract_resume_token,
    file_access_to_codex_cwd,
    is_capacity_error,
    is_quota_error,
    prepare_codex_profile,
    prepare_schema,
    read_output_json,
    resolve_codex_home,
    run_codex_subprocess,
    validate_codex_home,
)
from commons.runtime_errors import CmocError
from commons.runtime_codex_logging import emit_codex_call_console
from commons.runtime_git import is_untracked_git_ignored, run_git
from commons.runtime_logging import SubcommandLogger, current_subcommand_logger
from commons.runtime_paths import (
    codex_log_dir,
    console_timestamp,
    repo_root,
    timestamp,
    work_root,
)
from commons.runtime_results import CodexExecResult


_QUOTA_CONDITION = threading.Condition()
_QUOTA_POLLING = False
_QUOTA_PROBE_AVAILABLE = False
_QUOTA_PROBE_ERROR: BaseException | None = None
_CODEX_LOG_TIMESTAMP_LOCK = threading.Lock()
_LAST_CODEX_LOG_TIMESTAMP: str | None = None
_FORBIDDEN_FILESYSTEM_DIFF_ROOTS = (".agents", ".codex", ".git", "memo")
_IGNORED_GIT_DIFF_EXCLUDED_ROOTS = (".cmoc", ".venv")
_ForbiddenSnapshot = dict[Path, tuple[int, int, int, int, str | None]]
_PathFingerprint = tuple[str, int, int, str | None] | None
_WorktreeDiffSnapshot = dict[Path, tuple[str, _PathFingerprint]]


def _write_prompt_log(path: Path, prompt: str) -> None:
    # <work-root>/oracle/doc/app_spec/codex_exec_rule.md
    # The prompt log is the replayable stdin source itself, not metadata.
    path.write_text(prompt)


def _read_required_output_json(path: Path) -> Any:
    # <work-root>/oracle/doc/app_spec/codex_exec_rule.md
    # Structured Output parse failure is semantic failure; schema permissiveness
    # must not turn missing, empty, or malformed output into success.
    try:
        text = path.read_text()
    except FileNotFoundError as exc:
        raise ValueError(f"output file does not exist: {path}") from exc
    if not text.strip():
        raise ValueError(f"output file is empty: {path}")
    try:
        return json.loads(text)
    except json.JSONDecodeError as exc:
        raise ValueError(f"output file is not valid JSON: {exc}") from exc


def _base_exec_argv(profile_name: str, codex_cwd: Path) -> list[str]:
    # <work-root>/oracle/doc/app_spec/codex_exec_rule.md
    # cmoc may run Codex from linked worktrees or generated roots; repo
    # validation belongs to cmoc's own preflight, not to Codex CLI startup.
    return [
        "codex",
        "exec",
        "--skip-git-repo-check",
        "--profile",
        profile_name,
        "--cd",
        str(codex_cwd),
    ]


def _quota_availability_probe_parameter(
    base_parameter: AgentCallParameter,
) -> AgentCallParameter:
    # <work-root>/oracle/doc/app_spec/codex_exec_rule.md
    # The oracle specifies the polling behavior but has no dedicated oracle-src
    # builder file. Keep this realization builder tiny and let runtime reuse the
    # same CODEX_HOME/profile/cwd as the failed call.
    from acp.builder.quota_probe import build_quota_availability_probe_parameter

    return build_quota_availability_probe_parameter(base_parameter)


def _next_codex_log_timestamp() -> str:
    """壁時計後退時も同一プロセス内の Codex exec log 名を単調増加させる。"""
    global _LAST_CODEX_LOG_TIMESTAMP
    with _CODEX_LOG_TIMESTAMP_LOCK:
        current = timestamp()
        if _LAST_CODEX_LOG_TIMESTAMP is not None and current <= _LAST_CODEX_LOG_TIMESTAMP:
            current_dt = datetime.strptime(
                _LAST_CODEX_LOG_TIMESTAMP[:-3], "%Y-%m-%d_%H-%M_%S_%f"
            )
            current = (current_dt + timedelta(microseconds=1)).strftime(
                "%Y-%m-%d_%H-%M_%S_%f000"
            )
        _LAST_CODEX_LOG_TIMESTAMP = current
        return current


def run_codex_exec(
    parameter: AgentCallParameter,
    *,
    root: Path | None = None,
    cwd: Path | None = None,
    config: CmocConfig | None = None,
    purpose: str = "codex exec",
    max_semantic_retries: int = 2,
    max_capacity_retries: int = 8,
    capacity_initial_sleep_sec: float = 5.0,
    quota_poll_interval_sec: float = 1800.0,
    max_quota_polls: int | None = None,
    subcommand_logger: SubcommandLogger | None = None,
    extra_read_paths: list[Path] | None = None,
    extra_writable_paths: list[Path] | None = None,
    allow_oracle_conflict_writes: bool = False,
    verify_file_access: bool = True,
) -> CodexExecResult:
    """Codex exec の再試行、Structured Output 検証、実行記録を一括制御する。"""
    root = root or repo_root()
    cwd = cwd or root
    config = config or load_config(root)
    log_dir = codex_log_dir(root)
    log_dir.mkdir(parents=True, exist_ok=True)
    codex_work_root = work_root(cwd)
    codex_cwd = file_access_to_codex_cwd(parameter.file_access_mode, codex_work_root)
    # <work-root>/oracle/doc/app_spec/codex_exec_rule.md
    # Relative CODEX_HOME is still passed through unchanged, so preflight and
    # profile generation must target the path Codex resolves from its real cwd.
    codex_home = resolve_codex_home(codex_cwd)
    validate_codex_home(codex_home)
    codex_env = codex_subprocess_env(codex_home)
    profile_path = prepare_codex_profile(
        parameter,
        config,
        codex_home,
        codex_work_root,
        extra_read_paths,
        extra_writable_paths,
        allow_oracle_conflict_writes=allow_oracle_conflict_writes,
    )
    profile_name = codex_profile_name(profile_path)
    # <work-root>/oracle/doc/app_spec/codex_exec_rule.md
    # `--output-schema` must point at state under the same work root Codex uses.
    schema_path = (
        prepare_schema(codex_work_root, parameter.structured_output_schema_path)
        if parameter.structured_output_schema_path
        else None
    )
    base_call_data = {
        "codex_home": str(codex_home),
        "profile_name": profile_name,
        "profile_path": str(profile_path),
        "model_class": parameter.model_class.value,
        "reasoning_effort": parameter.reasoning_effort.value,
        "file_access_mode": parameter.file_access_mode.value,
    }

    def new_log_paths() -> tuple[str, Path, Path, Path, Path, Path]:
        """Codex call 用 log path 群を時刻順に追える名前で確保する。"""
        while True:
            run_ts = _next_codex_log_timestamp()
            run_call_path = log_dir / f"{run_ts}_call.json"
            if not run_call_path.exists():
                return (
                    run_ts,
                    log_dir / f"{run_ts}_prompt.jsonl",
                    log_dir / f"{run_ts}_stdout.jsonl",
                    log_dir / f"{run_ts}_stderr.log",
                    log_dir / f"{run_ts}_output.json",
                    run_call_path,
                )

    def build_argv(output_path: Path, resume_token: str | None) -> list[str]:
        """schema と resume 状態を反映した `codex exec` の argv を組み立てる。"""
        run_argv = _base_exec_argv(profile_name, codex_cwd)
        run_argv.extend(["--json", "--output-last-message", str(output_path)])
        if schema_path is not None:
            run_argv.extend(["--output-schema", str(schema_path)])
        if resume_token:
            run_argv.extend(["resume", resume_token])
        run_argv.append("-")
        return run_argv

    def run_with_prompt_file(
        run_argv: list[str], run_prompt_path: Path
    ) -> subprocess.CompletedProcess[str]:
        # <work-root>/oracle/doc/app_spec/codex_exec_rule.md
        # The prompt log file is the stdin source for `codex exec ... -`.
        with run_prompt_path.open() as prompt_file:
            return run_codex_subprocess(
                run_argv,
                cwd=codex_cwd,
                stdin=prompt_file,
                text=True,
                capture_output=True,
                env=codex_env,
            )

    def write_call_log(
        path: Path,
        *,
        run_purpose: str,
        run_ts: str,
        run_argv: list[str],
        run_prompt_path: Path,
        run_stdout_path: Path,
        run_stderr_path: Path,
        run_output_path: Path,
        run_schema_path: Path | None,
    ) -> None:
        """後から実行条件を追跡できる call log JSON を保存する。"""
        path.write_text(
            json.dumps(
                {
                    "purpose": run_purpose,
                    "timestamp": run_ts,
                    "argv": run_argv,
                    **base_call_data,
                    "schema_path": str(run_schema_path) if run_schema_path else None,
                    "prompt_log_path": str(run_prompt_path),
                    "stdout_log_path": str(run_stdout_path),
                    "stderr_log_path": str(run_stderr_path),
                    "output_path": str(run_output_path),
                },
                ensure_ascii=False,
                indent=2,
            )
            + "\n"
        )

    call_started_at = time.perf_counter()
    quota_wait_sec = 0.0
    logger = subcommand_logger or current_subcommand_logger()

    def emit_codex_call_event(
        *,
        run_purpose: str,
        run_call_path: Path,
        run_prompt_path: Path,
        run_stdout_path: Path,
        run_stderr_path: Path,
        run_output_path: Path,
        run_schema_path: Path | None,
        started_at: float,
        returncode: int,
        status: str,
        error: str | None = None,
    ) -> None:
        """console と subcommand log の両方へ Codex call 結果を記録する。"""
        elapsed_sec = time.perf_counter() - started_at
        emit_codex_call_console(run_purpose, run_call_path, elapsed_sec, returncode)
        if logger is None:
            return
        payload: dict[str, Any] = {
            "purpose": run_purpose,
            "status": status,
            "returncode": returncode,
            "elapsed_sec": elapsed_sec,
            "quota_wait_sec": quota_wait_sec,
            "quota_polls": quota_polls,
            "call_log_path": str(run_call_path),
            "prompt_log_path": str(run_prompt_path),
            "stdout_log_path": str(run_stdout_path),
            "stderr_log_path": str(run_stderr_path),
            "output_path": str(run_output_path),
            "codex_home": str(codex_home),
            "profile_name": profile_name,
            "profile_path": str(profile_path),
            "schema_path": str(run_schema_path) if run_schema_path else None,
        }
        if error is not None:
            payload["error"] = error
        logger.event("codex_call", **payload)

    semantic_attempts = 0
    capacity_attempts = 0
    quota_polls = 0
    sleep_sec = capacity_initial_sleep_sec
    last_result: subprocess.CompletedProcess[str] | None = None
    resume_token: str | None = None
    generated_paths: set[Path] = set()
    if schema_path is not None:
        generated_paths.add(schema_path.resolve())
    forbidden_baseline = (
        _forbidden_filesystem_snapshot(codex_work_root) if verify_file_access else None
    )
    worktree_diff_baseline = (
        _worktree_diff_snapshot(codex_work_root) if verify_file_access else None
    )

    while True:
        ts, prompt_path, stdout_path, stderr_path, output_path, call_path = new_log_paths()
        current_argv = build_argv(output_path, resume_token)
        _write_prompt_log(prompt_path, parameter.prompt)
        generated_paths.update(
            path.resolve()
            for path in (prompt_path, stdout_path, stderr_path, output_path, call_path)
        )
        write_call_log(
            call_path,
            run_purpose=purpose,
            run_ts=ts,
            run_argv=current_argv,
            run_prompt_path=prompt_path,
            run_stdout_path=stdout_path,
            run_stderr_path=stderr_path,
            run_output_path=output_path,
            run_schema_path=schema_path,
        )
        attempt_started_at = time.perf_counter()
        result = run_with_prompt_file(current_argv, prompt_path)
        last_result = result
        stdout_path.write_text(result.stdout)
        stderr_path.write_text(result.stderr)
        error_text = codex_error_text(result.stdout, result.stderr)
        if result.returncode != 0:
            if (
                is_capacity_error(result.stdout)
                and capacity_attempts < max_capacity_retries
            ):
                capacity_attempts += 1
                emit_codex_call_event(
                    run_purpose=purpose,
                    run_call_path=call_path,
                    run_prompt_path=prompt_path,
                    run_stdout_path=stdout_path,
                    run_stderr_path=stderr_path,
                    run_output_path=output_path,
                    run_schema_path=schema_path,
                    started_at=attempt_started_at,
                    returncode=result.returncode,
                    status="capacity_retrying",
                    error=error_text,
                )
                time.sleep(sleep_sec)
                sleep_sec *= 2
                continue
            if is_quota_error(result.stdout):
                global _QUOTA_POLLING, _QUOTA_PROBE_AVAILABLE, _QUOTA_PROBE_ERROR
                emit_codex_call_event(
                    run_purpose=purpose,
                    run_call_path=call_path,
                    run_prompt_path=prompt_path,
                    run_stdout_path=stdout_path,
                    run_stderr_path=stderr_path,
                    run_output_path=output_path,
                    run_schema_path=schema_path,
                    started_at=attempt_started_at,
                    returncode=result.returncode,
                    status="quota_waiting",
                    error=error_text,
                )
                quota_probe_parameter = _quota_availability_probe_parameter(parameter)
                with _QUOTA_CONDITION:
                    if _QUOTA_POLLING:
                        wait_started_at = time.perf_counter()
                        print(
                            "# "
                            f"{console_timestamp()} "
                            "Codex CLI quota wait: waiting for representative probe",
                            flush=True,
                        )
                        _QUOTA_CONDITION.wait_for(lambda: not _QUOTA_POLLING)
                        waited_sec = time.perf_counter() - wait_started_at
                        quota_wait_sec += waited_sec
                        if logger is not None:
                            logger.add_quota_wait(waited_sec)
                        if _QUOTA_PROBE_ERROR is not None:
                            raise _QUOTA_PROBE_ERROR
                        if not _QUOTA_PROBE_AVAILABLE:
                            raise CmocError(
                                "Codex CLI quota 待機の代表 probe が中断しました。",
                                [
                                    "quota 回復後に同じ cmoc コマンドを再実行してください。"
                                ],
                                error_text,
                            )
                        resume_token = extract_resume_token(result.stdout)
                        continue
                    _QUOTA_PROBE_AVAILABLE = False
                    _QUOTA_PROBE_ERROR = None
                    _QUOTA_POLLING = True
                print(
                    f"# {console_timestamp()} Codex CLI quota wait: entering polling mode",
                    flush=True,
                )
                probe_available = False
                probe_error: BaseException | None = None
                try:
                    while True:
                        if (
                            max_quota_polls is not None
                            and quota_polls >= max_quota_polls
                        ):
                            raise CmocError(
                                "Codex CLI quota が枯渇しました。",
                                [
                                    "quota 回復後に同じ cmoc コマンドを再実行してください。"
                                ],
                                error_text,
                            )
                        quota_polls += 1
                        if logger is not None:
                            logger.add_quota_wait(quota_poll_interval_sec)
                        quota_wait_sec += quota_poll_interval_sec
                        time.sleep(quota_poll_interval_sec)
                        (
                            probe_ts,
                            probe_prompt_path,
                            probe_stdout_path,
                            probe_stderr_path,
                            probe_output_path,
                            probe_call_path,
                        ) = new_log_paths()
                        probe_argv = _base_exec_argv(profile_name, codex_cwd)
                        probe_argv.extend(
                            [
                                "--json",
                                "--output-last-message",
                                str(probe_output_path),
                                "-",
                            ]
                        )
                        _write_prompt_log(
                            probe_prompt_path, quota_probe_parameter.prompt
                        )
                        write_call_log(
                            probe_call_path,
                            run_purpose="quota availability probe",
                            run_ts=probe_ts,
                            run_argv=probe_argv,
                            run_prompt_path=probe_prompt_path,
                            run_stdout_path=probe_stdout_path,
                            run_stderr_path=probe_stderr_path,
                            run_output_path=probe_output_path,
                            run_schema_path=None,
                        )
                        probe_started_at = time.perf_counter()
                        poll = run_with_prompt_file(probe_argv, probe_prompt_path)
                        probe_stdout_path.write_text(poll.stdout)
                        probe_stderr_path.write_text(poll.stderr)
                        probe_error_text = codex_error_text(poll.stdout, poll.stderr)
                        probe_quota_error = is_quota_error(poll.stdout)
                        probe_capacity_error = is_capacity_error(poll.stdout)
                        probe_available = (
                            poll.returncode == 0
                            and not probe_quota_error
                            and not probe_capacity_error
                        )
                        if (
                            probe_capacity_error
                            and capacity_attempts < max_capacity_retries
                        ):
                            capacity_attempts += 1
                            quota_polls -= 1
                            emit_codex_call_event(
                                run_purpose="quota availability probe",
                                run_call_path=probe_call_path,
                                run_prompt_path=probe_prompt_path,
                                run_stdout_path=probe_stdout_path,
                                run_stderr_path=probe_stderr_path,
                                run_output_path=probe_output_path,
                                run_schema_path=None,
                                started_at=probe_started_at,
                                returncode=poll.returncode,
                                status="capacity_retrying",
                                error=probe_error_text,
                            )
                            time.sleep(sleep_sec)
                            sleep_sec *= 2
                            continue
                        if not probe_available and not probe_quota_error:
                            emit_codex_call_event(
                                run_purpose="quota availability probe",
                                run_call_path=probe_call_path,
                                run_prompt_path=probe_prompt_path,
                                run_stdout_path=probe_stdout_path,
                                run_stderr_path=probe_stderr_path,
                                run_output_path=probe_output_path,
                                run_schema_path=None,
                                started_at=probe_started_at,
                                returncode=poll.returncode,
                                status="failed",
                                error=probe_error_text,
                            )
                            # <work-root>/oracle/doc/app_spec/codex_exec_rule.md
                            # A probe is still `codex exec`; non-quota failure is
                            # not recoverable by waiting for quota reset.
                            raise CmocError(
                                "Codex CLI quota availability probe が失敗しました。",
                                ["stderr/stdout log を確認して原因を解消してください。"],
                                (
                                    f"call_log: {probe_call_path}\n"
                                    f"stdout_log: {probe_stdout_path}\n"
                                    f"stderr_log: {probe_stderr_path}\n"
                                    f"{probe_error_text}"
                                ),
                            )
                        emit_codex_call_event(
                            run_purpose="quota availability probe",
                            run_call_path=probe_call_path,
                            run_prompt_path=probe_prompt_path,
                            run_stdout_path=probe_stdout_path,
                            run_stderr_path=probe_stderr_path,
                            run_output_path=probe_output_path,
                            run_schema_path=None,
                            started_at=probe_started_at,
                            returncode=poll.returncode,
                            status="succeeded" if probe_available else "quota_waiting",
                            error=None if probe_available else probe_error_text,
                        )
                        if probe_available:
                            break
                except BaseException as exc:
                    probe_error = exc
                    raise
                finally:
                    with _QUOTA_CONDITION:
                        # <work-root>/oracle/doc/app_spec/codex_exec_rule.md
                        # Waiters may resume only after the representative probe
                        # proved quota availability; probe failure is shared.
                        _QUOTA_PROBE_AVAILABLE = probe_available
                        _QUOTA_PROBE_ERROR = probe_error
                        _QUOTA_POLLING = False
                        _QUOTA_CONDITION.notify_all()
                print(
                    f"# {console_timestamp()} Codex CLI quota wait: resuming work",
                    flush=True,
                )
                resume_token = extract_resume_token(result.stdout)
                continue
            emit_codex_call_event(
                run_purpose=purpose,
                run_call_path=call_path,
                run_prompt_path=prompt_path,
                run_stdout_path=stdout_path,
                run_stderr_path=stderr_path,
                run_output_path=output_path,
                run_schema_path=schema_path,
                started_at=attempt_started_at,
                returncode=result.returncode,
                status="failed",
                error=error_text,
            )
            raise CmocError(
                "Codex CLI 呼び出しが失敗しました。",
                ["stderr/stdout log を確認して原因を解消してください。"],
                (
                    f"call_log: {call_path}\n"
                    f"stdout_log: {stdout_path}\n"
                    f"stderr_log: {stderr_path}\n"
                    f"{error_text}"
                ),
            )
        if schema_path is not None:
            try:
                output_json = _read_required_output_json(output_path)
                validate(
                    instance=output_json, schema=json.loads(schema_path.read_text())
                )
            except Exception as exc:
                if semantic_attempts < max_semantic_retries:
                    semantic_attempts += 1
                    emit_codex_call_event(
                        run_purpose=purpose,
                        run_call_path=call_path,
                        run_prompt_path=prompt_path,
                        run_stdout_path=stdout_path,
                        run_stderr_path=stderr_path,
                        run_output_path=output_path,
                        run_schema_path=schema_path,
                        started_at=attempt_started_at,
                        returncode=result.returncode,
                        status="schema_validation_retrying",
                        error=str(exc),
                    )
                    continue
                emit_codex_call_event(
                    run_purpose=purpose,
                    run_call_path=call_path,
                    run_prompt_path=prompt_path,
                    run_stdout_path=stdout_path,
                    run_stderr_path=stderr_path,
                    run_output_path=output_path,
                    run_schema_path=schema_path,
                    started_at=attempt_started_at,
                    returncode=result.returncode,
                    status="schema_validation_failed",
                    error=str(exc),
                )
                raise CmocError(
                    "Codex CLI の Structured Output 検証に失敗しました。",
                    ["schema と output を確認してください。"],
                    f"schema: {schema_path}\noutput: {output_path}\nerror: {exc}",
                ) from exc
        else:
            output_json = read_output_json(output_path)
        output_text = output_path.read_text() if output_path.exists() else ""
        elapsed_sec = time.perf_counter() - call_started_at
        emit_codex_call_event(
            run_purpose=purpose,
            run_call_path=call_path,
            run_prompt_path=prompt_path,
            run_stdout_path=stdout_path,
            run_stderr_path=stderr_path,
            run_output_path=output_path,
            run_schema_path=schema_path,
            started_at=attempt_started_at,
            returncode=result.returncode,
            status="succeeded",
        )
        exec_result = CodexExecResult(
            returncode=result.returncode,
            output_text=output_text,
            output_json=output_json,
            call_log_path=call_path,
            prompt_log_path=prompt_path,
            stdout_log_path=stdout_path,
            stderr_log_path=stderr_path,
            output_path=output_path,
            codex_home=codex_home,
            profile_name=profile_name,
            profile_path=profile_path,
            schema_path=schema_path,
            elapsed_sec=elapsed_sec,
            quota_wait_sec=quota_wait_sec,
            quota_polls=quota_polls,
        )
        if verify_file_access:
            allowed_paths: list[Path] = []
            if allow_oracle_conflict_writes:
                # <work-root>/oracle/src/oracle/acp_builder/session/join/conflict_resolution.py
                # Codex profile can only open parent directories, so the
                # stricter file-level conflict target boundary is enforced here.
                allowed_paths.extend(extra_writable_paths or [])
            recover_file_access_violations(
                codex_work_root,
                exec_result,
                parameter.file_access_mode,
                config,
                generated_paths,
                root=root,
                subcommand_logger=logger,
                allowed_paths=allowed_paths,
                forbidden_baseline=forbidden_baseline,
                worktree_diff_baseline=worktree_diff_baseline,
            )
        return exec_result

    assert last_result is not None


def recover_file_access_violations(
    worktree: Path,
    violated_result: CodexExecResult,
    violated_mode: FileAccessMode,
    config: CmocConfig,
    ignored_paths: set[Path] | None = None,
    *,
    root: Path | None = None,
    subcommand_logger: SubcommandLogger | None = None,
    allowed_paths: list[Path] | None = None,
    forbidden_baseline: _ForbiddenSnapshot | None = None,
    worktree_diff_baseline: _WorktreeDiffSnapshot | None = None,
) -> None:
    """agent call 後に残った file access rule 違反を設定回数だけ修復する。"""
    # <work-root>/oracle/doc/app_spec/codex_exec_rule.md
    # Runtime-generated logs are ignored here; the post-check targets agent
    # edits that remain in the worktree after the call.
    ignored = {path.resolve() for path in ignored_paths or set()}
    violations = file_access_violations(
        worktree,
        _post_call_changed_worktree_paths(
            worktree, forbidden_baseline, worktree_diff_baseline
        ),
        violated_mode,
        ignored,
        allowed_paths,
    )
    if not violations:
        return
    for _attempt in range(config.codex.num_try_falv_recovery):
        from acp.builder.common.file_access_rule_vaolation_recovery import (
            build_file_access_rule_vaolation_recovery_parameter,
        )

        parameter = build_file_access_rule_vaolation_recovery_parameter(
            violated_result.call_log_path,
            violations,
            violated_mode,
        )
        recovery_result = run_codex_exec(
            parameter,
            root=root or worktree,
            cwd=worktree,
            config=config,
            purpose="file access rule violation recovery",
            subcommand_logger=subcommand_logger,
            verify_file_access=False,
        )
        ignored.update(
            path.resolve()
            for path in (
                recovery_result.call_log_path,
                recovery_result.prompt_log_path,
                recovery_result.stdout_log_path,
                recovery_result.stderr_log_path,
                recovery_result.output_path,
            )
        )
        if recovery_result.schema_path is not None:
            ignored.add(recovery_result.schema_path.resolve())
        violations = file_access_violations(
            worktree,
            _post_call_changed_worktree_paths(
                worktree, forbidden_baseline, worktree_diff_baseline
            ),
            violated_mode,
            ignored,
            allowed_paths,
        )
        if not violations:
            return
    raise CmocError(
        "agent call がファイルアクセス規則に違反しました。",
        ["Codex call log と作業差分を確認してから cmoc コマンドを再実行してください。"],
        "\n".join(str(path) for path in violations),
    )


def changed_worktree_paths(root: Path) -> list[Path]:
    """worktree 上の変更 path を absolute path として返す。"""
    return [path for _status, path in _changed_worktree_path_statuses(root)]


def _changed_worktree_path_statuses(
    root: Path, *, include_ignored: bool = False
) -> list[tuple[str, Path]]:
    """worktree 上の変更 path と git status code を absolute path として返す。"""
    paths: list[tuple[str, Path]] = []
    # <work-root>/oracle/doc/app_spec/sub_command/apply_fork.md
    # <work-root>/oracle/doc/app_spec/codex_exec_rule.md
    # apply requeue and file access validation both need file-level paths;
    # default status can collapse untracked directories into one directory path.
    for line in run_git(["status", "--short", "-uall"], root).stdout.splitlines():
        status = line[:2]
        path_text = line[3:]
        if " -> " in path_text:
            path_text = path_text.split(" -> ", 1)[1]
        paths.append((status, root / path_text))
    if not include_ignored:
        return paths
    for line in run_git(
        ["ls-files", "--others", "--ignored", "--exclude-standard"], root
    ).stdout.splitlines():
        parts = Path(line).parts
        if parts and parts[0] in _IGNORED_GIT_DIFF_EXCLUDED_ROOTS:
            continue
        paths.append(("!!", root / line))
    return paths


def _post_call_changed_worktree_paths(
    root: Path,
    forbidden_baseline: _ForbiddenSnapshot | None,
    worktree_diff_baseline: _WorktreeDiffSnapshot | None,
) -> list[Path]:
    """agent call 後の検査対象 path を返す。"""
    paths = _post_call_changed_git_paths(root, worktree_diff_baseline)
    if forbidden_baseline is not None:
        paths.extend(_forbidden_filesystem_changed_paths(root, forbidden_baseline))
    seen: set[Path] = set()
    result: list[Path] = []
    for path in paths:
        resolved = path.resolve()
        if resolved not in seen:
            seen.add(resolved)
            result.append(path)
    return result


def _post_call_changed_git_paths(
    root: Path, baseline: _WorktreeDiffSnapshot | None
) -> list[Path]:
    paths: list[Path] = []
    for status, path in _changed_worktree_path_statuses(root, include_ignored=True):
        if baseline is None:
            paths.append(path)
            continue
        resolved = path.resolve()
        current = (status, _path_fingerprint(path))
        if baseline.get(resolved) != current:
            paths.append(path)
    return paths


def _worktree_diff_snapshot(root: Path) -> _WorktreeDiffSnapshot:
    return {
        path.resolve(): (status, _path_fingerprint(path))
        for status, path in _changed_worktree_path_statuses(root, include_ignored=True)
    }


def _path_fingerprint(path: Path) -> _PathFingerprint:
    try:
        stat = path.lstat()
    except FileNotFoundError:
        return None
    digest: str | None = None
    if path.is_symlink():
        digest = hashlib.sha256(os.readlink(path).encode()).hexdigest()
    elif path.is_file():
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
    return (
        "dir" if path.is_dir() else "file",
        stat.st_mode,
        stat.st_size,
        digest,
    )


def _forbidden_filesystem_snapshot(root: Path) -> _ForbiddenSnapshot:
    snapshot: _ForbiddenSnapshot = {}
    for name in _FORBIDDEN_FILESYSTEM_DIFF_ROOTS:
        base = root / name
        if not base.exists():
            continue
        if base.is_file() or base.is_symlink():
            snapshot[base.relative_to(root)] = _forbidden_file_fingerprint(
                base, include_digest=name == ".git"
            )
            continue
        if name == ".git":
            # cmoc の git status 自体が .git directory を更新し得るため、
            # linked worktree の .git file だけを filesystem 差分対象にする。
            continue
        for current_root, _dirnames, filenames in os.walk(base):
            for filename in filenames:
                path = Path(current_root) / filename
                try:
                    fingerprint = _forbidden_file_fingerprint(path)
                except FileNotFoundError:
                    continue
                snapshot[path.relative_to(root)] = fingerprint
    return snapshot


def _forbidden_file_fingerprint(
    path: Path, *, include_digest: bool = False
) -> tuple[int, int, int, int, str | None]:
    stat = path.lstat()
    digest = hashlib.sha256(path.read_bytes()).hexdigest() if include_digest else None
    return stat.st_mode, stat.st_size, stat.st_mtime_ns, stat.st_ctime_ns, digest


def _forbidden_filesystem_changed_paths(
    root: Path, baseline: _ForbiddenSnapshot
) -> list[Path]:
    # <work-root>/oracle/doc/app_spec/codex_exec_rule.md
    # Ignored files below denied roots do not appear in git status, so post-check
    # also compares file metadata captured immediately before the agent call.
    current = _forbidden_filesystem_snapshot(root)
    changed: list[Path] = []
    for relative in sorted(set(baseline) | set(current), key=str):
        if baseline.get(relative) != current.get(relative):
            changed.append(root / relative)
    return changed


def file_access_violations(
    root: Path,
    paths: list[Path],
    mode: FileAccessMode,
    ignored_paths: set[Path] | None = None,
    allowed_paths: list[Path] | None = None,
) -> list[Path]:
    """FileAccessMode 上、差分が残ってはいけない path だけを返す。"""
    ignored = {path.resolve() for path in ignored_paths or set()}
    allowed = {path.resolve() for path in allowed_paths or []}
    return [
        path
        for path in paths
        if path.resolve() not in ignored
        and path.resolve() not in allowed
        and not _is_cmoc_generated_diff_path(root, path)
        and not _is_write_allowed_by_file_access_mode(root, path, mode)
    ]


def _is_cmoc_generated_diff_path(root: Path, path: Path) -> bool:
    try:
        relative = path.resolve().relative_to(root.resolve())
    except ValueError:
        return False
    return len(relative.parts) >= 2 and relative.parts[:2] == (".cmoc", "log")


def _is_write_allowed_by_file_access_mode(
    root: Path,
    path: Path,
    mode: FileAccessMode,
) -> bool:
    try:
        relative = path.resolve().relative_to(root.resolve())
    except ValueError:
        return False
    if not relative.parts:
        return False
    blocked_runtime_roots = {
        ".agents",
        ".cmoc",
        ".codex",
        ".git",
        ".pytest_cache",
        "memo",
    }
    if relative.parts[0] in blocked_runtime_roots:
        return False
    if (len(relative.parts) == 1 and path.name == "README.md") or path.name in {
        "AGENTS.md",
        "INDEX.md",
    }:
        return False
    match mode:
        case FileAccessMode.READONLY | FileAccessMode.PURE_ORACLE_READ:
            return False
        case FileAccessMode.REALIZATION_WRITE:
            if is_untracked_git_ignored(root, path):
                return False
            return relative.parts[0] != "oracle"
        case FileAccessMode.PURE_ORACLE_WRITE:
            return relative.parts[0] == "oracle"
        case FileAccessMode.REPO_WRITE | FileAccessMode.NO_RULE:
            return True
        case _:
            return False
