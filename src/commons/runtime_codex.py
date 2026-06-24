import json
import subprocess
import threading
import time
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
    validate_codex_home,
)
from commons.runtime_errors import CmocError
from commons.runtime_logging import SubcommandLogger, current_subcommand_logger
from commons.runtime_paths import (
    codex_log_dir,
    console_timestamp,
    format_duration,
    repo_root,
    timestamp,
    work_root,
)
from commons.runtime_results import CodexExecResult, CommandResult


_QUOTA_CONDITION = threading.Condition()
_QUOTA_POLLING = False


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
) -> CodexExecResult:
    root = root or repo_root()
    cwd = cwd or root
    config = config or load_config(root)
    log_dir = codex_log_dir(root)
    log_dir.mkdir(parents=True, exist_ok=True)
    ts = timestamp()
    stdout_path = log_dir / f"{ts}_stdout.jsonl"
    stderr_path = log_dir / f"{ts}_stderr.log"
    output_path = log_dir / f"{ts}_output.json"
    call_path = log_dir / f"{ts}_call.json"
    codex_home = resolve_codex_home(cwd)
    validate_codex_home(codex_home)
    codex_env = codex_subprocess_env(codex_home)
    profile_path = prepare_codex_profile(parameter, config, codex_home)
    profile_name = codex_profile_name(profile_path)
    schema_path = (
        prepare_schema(work_root(cwd), parameter.structured_output_schema_path)
        if parameter.structured_output_schema_path
        else None
    )
    argv = [
        "codex",
        "exec",
        "--profile",
        profile_name,
        "--json",
        "--output-last-message",
        str(output_path),
    ]
    if schema_path is not None:
        argv.extend(["--output-schema", str(schema_path)])
    argv.append("-")
    base_call_data = {
        "codex_home": str(codex_home),
        "profile_name": profile_name,
        "profile_path": str(profile_path),
        "model_class": parameter.model_class.value,
        "reasoning_effort": parameter.reasoning_effort.value,
        "file_access_mode": parameter.file_access_mode.value,
    }

    def write_call_log(
        path: Path,
        *,
        run_purpose: str,
        run_ts: str,
        run_argv: list[str],
        run_stdout_path: Path,
        run_stderr_path: Path,
        run_output_path: Path,
        run_schema_path: Path | None,
    ) -> None:
        path.write_text(
            json.dumps(
                {
                    "purpose": run_purpose,
                    "timestamp": run_ts,
                    "argv": run_argv,
                    **base_call_data,
                    "schema_path": str(run_schema_path) if run_schema_path else None,
                    "stdout_log_path": str(run_stdout_path),
                    "stderr_log_path": str(run_stderr_path),
                    "output_path": str(run_output_path),
                },
                ensure_ascii=False,
                indent=2,
            )
            + "\n"
        )

    write_call_log(
        call_path,
        run_purpose=purpose,
        run_ts=ts,
        run_argv=argv,
        run_stdout_path=stdout_path,
        run_stderr_path=stderr_path,
        run_output_path=output_path,
        run_schema_path=schema_path,
    )
    call_started_at = time.perf_counter()
    quota_wait_sec = 0.0
    logger = subcommand_logger or current_subcommand_logger()

    def emit_codex_event(
        returncode: int, status: str, error: str | None = None
    ) -> None:
        elapsed_sec = time.perf_counter() - call_started_at
        print(
            "\n".join(
                [
                    f"# {console_timestamp()} Codex CLI call",
                    f"- purpose: `{purpose}`",
                    f"- call_log: `{call_path}`",
                    f"- elapsed: `{format_duration(elapsed_sec)}`",
                    f"- returncode: `{returncode}`",
                ]
            ),
            flush=True,
        )
        if logger is None:
            return
        payload: dict[str, Any] = {
            "purpose": purpose,
            "status": status,
            "returncode": returncode,
            "elapsed_sec": elapsed_sec,
            "quota_wait_sec": quota_wait_sec,
            "quota_polls": quota_polls,
            "call_log_path": str(call_path),
            "stdout_log_path": str(stdout_path),
            "stderr_log_path": str(stderr_path),
            "output_path": str(output_path),
            "codex_home": str(codex_home),
            "profile_name": profile_name,
            "profile_path": str(profile_path),
            "schema_path": str(schema_path) if schema_path else None,
        }
        if error is not None:
            payload["error"] = error
        logger.event("codex_call", **payload)

    semantic_attempts = 0
    capacity_attempts = 0
    quota_polls = 0
    sleep_sec = capacity_initial_sleep_sec
    last_result: subprocess.CompletedProcess[str] | None = None
    current_argv = argv
    while True:
        result = subprocess.run(
            current_argv,
            cwd=cwd,
            input=parameter.prompt,
            text=True,
            capture_output=True,
            env=codex_env,
        )
        last_result = result
        stdout_path.write_text(result.stdout)
        stderr_path.write_text(result.stderr)
        error_text = codex_error_text(result.stdout, result.stderr)
        if result.returncode != 0:
            if (
                is_capacity_error(error_text)
                and capacity_attempts < max_capacity_retries
            ):
                capacity_attempts += 1
                time.sleep(sleep_sec)
                sleep_sec *= 2
                continue
            if is_quota_error(error_text):
                global _QUOTA_POLLING
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
                        if resume_token:
                            current_argv = [*argv[:-1], "resume", resume_token, "-"]
                        else:
                            current_argv = argv
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
                            emit_codex_event(
                                result.returncode, "quota_exhausted", error_text
                            )
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
                        probe_ts = timestamp()
                        probe_stdout_path = log_dir / f"{probe_ts}_stdout.jsonl"
                        probe_stderr_path = log_dir / f"{probe_ts}_stderr.log"
                        probe_output_path = log_dir / f"{probe_ts}_output.json"
                        probe_call_path = log_dir / f"{probe_ts}_call.json"
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
                        write_call_log(
                            probe_call_path,
                            run_purpose="quota availability probe",
                            run_ts=probe_ts,
                            run_argv=probe_argv,
                            run_stdout_path=probe_stdout_path,
                            run_stderr_path=probe_stderr_path,
                            run_output_path=probe_output_path,
                            run_schema_path=None,
                        )
                        poll = subprocess.run(
                            probe_argv,
                            cwd=cwd,
                            input="quota availability probe",
                            text=True,
                            capture_output=True,
                            env=codex_env,
                        )
                        probe_stdout_path.write_text(poll.stdout)
                        probe_stderr_path.write_text(poll.stderr)
                        print(
                            f"# {console_timestamp()} Codex CLI quota probe returned {poll.returncode}",
                            flush=True,
                        )
                        if poll.returncode == 0 and not is_quota_error(
                            codex_error_text(poll.stdout, poll.stderr)
                        ):
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
                if resume_token:
                    current_argv = [*argv[:-1], "resume", resume_token, "-"]
                else:
                    current_argv = argv
                continue
            emit_codex_event(result.returncode, "failed", error_text)
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
                    continue
                emit_codex_event(
                    result.returncode, "schema_validation_failed", str(exc)
                )
                raise CmocError(
                    "Codex CLI の Structured Output 検証に失敗しました。",
                    ["schema と output を確認してください。"],
                    f"schema: {schema_path}\noutput: {output_path}\nerror: {exc}",
                ) from exc
        output_text = output_path.read_text() if output_path.exists() else ""
        elapsed_sec = time.perf_counter() - call_started_at
        emit_codex_event(result.returncode, "succeeded")
        return CodexExecResult(
            returncode=result.returncode,
            output_text=output_text,
            output_json=output_json,
            call_log_path=call_path,
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


def run_codex_tui(
    parameter: AgentCallParameter,
    *,
    root: Path | None = None,
    cwd: Path | None = None,
    config: CmocConfig | None = None,
    purpose: str = "codex tui",
) -> CommandResult:
    root = root or repo_root()
    cwd = cwd or root
    config = config or load_config(root)
    log_dir = codex_log_dir(root)
    log_dir.mkdir(parents=True, exist_ok=True)
    ts = timestamp()
    call_path = log_dir / f"{ts}_tui_call.json"
    codex_home = resolve_codex_home(cwd)
    validate_codex_home(codex_home)
    profile_path = prepare_codex_profile(parameter, config, codex_home)
    profile_name = codex_profile_name(profile_path)
    argv = [
        "codex",
        "--profile",
        profile_name,
        parameter.prompt,
    ]
    call_path.write_text(
        json.dumps(
            {
                "purpose": purpose,
                "timestamp": ts,
                "argv": argv,
                "codex_home": str(codex_home),
                "profile_name": profile_name,
                "profile_path": str(profile_path),
                "model_class": parameter.model_class.value,
                "reasoning_effort": parameter.reasoning_effort.value,
                "file_access_mode": parameter.file_access_mode.value,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n"
    )
    result = subprocess.run(
        argv,
        cwd=cwd,
        env=codex_subprocess_env(codex_home),
    )
    logger = current_subcommand_logger()
    if logger is not None:
        logger.event(
            "codex_tui_call",
            purpose=purpose,
            returncode=result.returncode,
            call_log_path=str(call_path),
            codex_home=str(codex_home),
            profile_name=profile_name,
            profile_path=str(profile_path),
        )
    if result.returncode != 0:
        raise CmocError(
            "Codex CLI/TUI 呼び出しが失敗しました。",
            ["Codex CLI/TUI の出力と call log を確認してください。"],
            f"returncode: {result.returncode}\ncall_log: {call_path}",
        )
    return CommandResult(result.returncode, "", "")
