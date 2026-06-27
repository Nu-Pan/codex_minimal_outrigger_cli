"""Codex exec の単一試行ループを扱う。

このファイルは 16,000 文字を超えるが、Structured Output 検証、capacity
retry、quota 代表 probe、resume 継続は同じ subprocess 結果、call log、
subcommand event、retry counter を共有する 1 つの状態機械である。TUI 起動は
別 module へ分け、exec の分岐だけをここに残すことで責務境界を exec 実行制御
へ限定している。quota 処理だけをさらに分離すると、resume token と log/event
の読み取り文脈が呼び出し元と分断されるため、現状は一体で読む方が凝集性が高い。
"""

import json
import subprocess
import threading
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

from jsonschema import validate

from basic.acp import AgentCallParameter
from config.cmoc_config import CmocConfig

from commons.runtime_config import load_config
from commons.runtime_codex_profile import (
    codex_error_text,
    codex_profile_name,
    codex_subprocess_env,
    extract_resume_token,
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
_CODEX_LOG_TIMESTAMP_LOCK = threading.Lock()
_LAST_CODEX_LOG_TIMESTAMP: str | None = None


def _agents_status(root: Path) -> str:
    return subprocess.run(
        ["git", "status", "--short", "--", ".agents"],
        cwd=root,
        text=True,
        capture_output=True,
        check=False,
    ).stdout


def _reject_agents_edit(root: Path, before: str, call_path: Path) -> None:
    after = _agents_status(root)
    if after != before:
        raise CmocError(
            "Codex CLI 呼び出しが .agents 配下を変更しました。",
            [
                ".agents 配下を変更しない形で作業をやり直してください。",
                "必要な変更がある場合は、人間が別途 .agents 配下を編集してください。",
            ],
            f"call_log: {call_path}\nbefore:\n{before or '(clean)'}\nafter:\n{after or '(clean)'}",
        )


def _write_prompt_log(path: Path, prompt: str) -> None:
    # <work-root>/oracle/doc/app_spec/codex_exec_rule.md requires a
    # `_prompt.jsonl` log; stdin must still receive the original prompt text.
    path.write_text(json.dumps({"prompt": prompt}, ensure_ascii=False) + "\n")


def _read_prompt_log(path: Path) -> str:
    return json.loads(path.read_text())["prompt"]


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
) -> CodexExecResult:
    """Codex exec の再試行、Structured Output 検証、実行記録を一括制御する。"""
    root = root or repo_root()
    cwd = cwd or root
    config = config or load_config(root)
    log_dir = codex_log_dir(root)
    log_dir.mkdir(parents=True, exist_ok=True)
    codex_home = resolve_codex_home(cwd)
    validate_codex_home(codex_home)
    codex_env = codex_subprocess_env(codex_home)
    codex_work_root = work_root(cwd)
    profile_path = prepare_codex_profile(
        parameter,
        config,
        codex_home,
        codex_work_root,
        extra_read_paths,
        extra_writable_paths,
    )
    profile_name = codex_profile_name(profile_path)
    agents_status_before = _agents_status(codex_work_root)
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
        run_argv = [
            "codex",
            "exec",
            "--profile",
            profile_name,
            "--json",
            "--output-last-message",
            str(output_path),
        ]
        if schema_path is not None:
            run_argv.extend(["--output-schema", str(schema_path)])
        if resume_token:
            run_argv.extend(["resume", resume_token])
        run_argv.append("-")
        return run_argv

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

    def reject_agents_edit_after_event(
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
    ) -> None:
        try:
            _reject_agents_edit(codex_work_root, agents_status_before, run_call_path)
        except CmocError as exc:
            # <work-root>/oracle/doc/app_spec/console_and_file_log.md requires
            # every completed Codex CLI call to be logged, even when
            # <work-root>/oracle/doc/app_spec/codex_exec_rule.md then rejects
            # the call because `.agents` changed.
            emit_codex_call_event(
                run_purpose=run_purpose,
                run_call_path=run_call_path,
                run_prompt_path=run_prompt_path,
                run_stdout_path=run_stdout_path,
                run_stderr_path=run_stderr_path,
                run_output_path=run_output_path,
                run_schema_path=run_schema_path,
                started_at=started_at,
                returncode=returncode,
                status="failed",
                error=exc.detail,
            )
            raise

    while True:
        ts, prompt_path, stdout_path, stderr_path, output_path, call_path = new_log_paths()
        current_argv = build_argv(output_path, resume_token)
        _write_prompt_log(prompt_path, parameter.prompt)
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
        result = run_codex_subprocess(
            current_argv,
            cwd=cwd,
            input=_read_prompt_log(prompt_path),
            text=True,
            capture_output=True,
            env=codex_env,
        )
        last_result = result
        stdout_path.write_text(result.stdout)
        stderr_path.write_text(result.stderr)
        reject_agents_edit_after_event(
            run_purpose=purpose,
            run_call_path=call_path,
            run_prompt_path=prompt_path,
            run_stdout_path=stdout_path,
            run_stderr_path=stderr_path,
            run_output_path=output_path,
            run_schema_path=schema_path,
            started_at=attempt_started_at,
            returncode=result.returncode,
        )
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
                global _QUOTA_POLLING
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
                with _QUOTA_CONDITION:
                    if _QUOTA_POLLING:
                        wait_started_at = time.perf_counter()
                        print(
                            f"# {console_timestamp()} Codex CLI quota wait: waiting for representative probe",
                            flush=True,
                        )
                        _QUOTA_CONDITION.wait_for(lambda: not _QUOTA_POLLING)
                        waited_sec = time.perf_counter() - wait_started_at
                        quota_wait_sec += waited_sec
                        if logger is not None:
                            logger.add_quota_wait(waited_sec)
                        resume_token = extract_resume_token(result.stdout)
                        continue
                    _QUOTA_POLLING = True
                print(
                    f"# {console_timestamp()} Codex CLI quota wait: entering polling mode",
                    flush=True,
                )
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
                        probe_argv = [
                            "codex",
                            "exec",
                            "--profile",
                            profile_name,
                            "--json",
                            "--output-last-message",
                            str(probe_output_path),
                            "-",
                        ]
                        _write_prompt_log(
                            probe_prompt_path, "quota availability probe"
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
                        poll = run_codex_subprocess(
                            probe_argv,
                            cwd=cwd,
                            input=_read_prompt_log(probe_prompt_path),
                            text=True,
                            capture_output=True,
                            env=codex_env,
                        )
                        probe_stdout_path.write_text(poll.stdout)
                        probe_stderr_path.write_text(poll.stderr)
                        reject_agents_edit_after_event(
                            run_purpose="quota availability probe",
                            run_call_path=probe_call_path,
                            run_prompt_path=probe_prompt_path,
                            run_stdout_path=probe_stdout_path,
                            run_stderr_path=probe_stderr_path,
                            run_output_path=probe_output_path,
                            run_schema_path=None,
                            started_at=probe_started_at,
                            returncode=poll.returncode,
                        )
                        probe_error_text = codex_error_text(poll.stdout, poll.stderr)
                        probe_available = poll.returncode == 0 and not is_quota_error(
                            poll.stdout
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
                finally:
                    with _QUOTA_CONDITION:
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
                f"call_log: {call_path}\nstdout_log: {stdout_path}\nstderr_log: {stderr_path}\n{error_text}",
            )
        output_json = read_output_json(output_path)
        if schema_path is not None:
            try:
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
        return CodexExecResult(
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

    assert last_result is not None
