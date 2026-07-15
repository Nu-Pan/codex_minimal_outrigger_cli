import json
import subprocess
import time
from pathlib import Path

from basic.acp import AgentCallParameter
from config.cmoc_config import CmocConfig

from commons.runtime_config import load_config
from commons.runtime_codex_logging import (
    emit_codex_call_console,
    format_codex_call_error,
)
from commons.runtime_codex_profile import (
    codex_subprocess_env,
    parameter_codex_cwd,
    prepare_codex_override_args,
    resolve_codex_home,
    run_codex_subprocess,
    validate_codex_home,
)
from commons.runtime_errors import CmocError
from commons.runtime_logging import current_subcommand_logger
from commons.runtime_paths import (
    _reserve_timestamped_path,
    codex_log_dir,
    repo_root,
    timestamp,
    work_root,
)
from commons.runtime_results import CommandResult


def run_codex_tui(
    parameter: AgentCallParameter,
    *,
    root: Path | None = None,
    cwd: Path | None = None,
    config: CmocConfig | None = None,
    purpose: str = "codex tui",
    extra_read_paths: list[Path] | None = None,
) -> CommandResult:
    """Codex TUI を設定上書き argv と call log を準備して起動する。"""
    root = root or repo_root()
    cwd = cwd or root
    codex_work_root = work_root(cwd)
    config = config or load_config(codex_work_root)
    log_dir = codex_log_dir(root)
    log_dir.mkdir(parents=True, exist_ok=True)
    codex_cwd = parameter_codex_cwd(parameter, codex_work_root)
    # {{work-root}}/oracle/doc/app_spec/codex_exec_rule.md
    # Match validation to where Codex resolves a relative
    # CODEX_HOME while keeping the user-provided env value unchanged.
    codex_home = resolve_codex_home(codex_cwd)
    validate_codex_home(codex_home)
    # {{work-root}}/oracle/doc/app_spec/sub_command/tui.md
    # TUI complete prompt is stored under {{repo-root}} even when Codex runs in a
    # linked worktree; writable roots and schema state still follow codex_work_root.
    override_args = prepare_codex_override_args(
        parameter,
        config,
        codex_work_root,
        extra_read_paths,
        extra_read_root=root,
    )
    argv = [
        "codex",
        *override_args,
        "--cd",
        str(codex_cwd),
        parameter.prompt,
    ]
    # {{work-root}}/oracle/doc/app_spec/codex_exec_rule.md
    ts, call_path = _reserve_timestamped_path(log_dir, "_tui_call.json", timestamp)
    call_path.write_text(
        json.dumps(
            {
                "purpose": purpose,
                "timestamp": ts,
                "argv": argv,
                "codex_home": str(codex_home),
                "model_class": parameter.model_class.value,
                "reasoning_effort": parameter.reasoning_effort.value,
                "file_access_mode": parameter.file_access_mode.value,
                "cwd": str(codex_cwd),
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n"
    )
    started_at = time.perf_counter()
    failure: subprocess.CalledProcessError | None = None
    startup_failure: BaseException | None = None
    returncode: int | None = None
    try:
        result = run_codex_subprocess(
            argv,
            cwd=codex_cwd,
            env=codex_subprocess_env(codex_home),
            check=True,
        )
        returncode = result.returncode
    except subprocess.CalledProcessError as exc:
        failure = exc
        returncode = exc.returncode
    except BaseException as exc:
        startup_failure = exc
    elapsed_sec = time.perf_counter() - started_at
    error: str | None = None
    if startup_failure is not None:
        error = format_codex_call_error(startup_failure)
    emit_codex_call_console(purpose, call_path, elapsed_sec, returncode, error)
    logger = current_subcommand_logger()
    status = "succeeded" if returncode == 0 else "failed"

    def emit_event(error: str | None = None) -> None:
        """Codex CLI の成功・失敗 event を logger に記録する。

        根拠: {{work-root}}/oracle/doc/app_spec/console_and_file_log.md
        """
        if logger is None:
            return
        payload = {
            "purpose": purpose,
            "status": status if error is None else "failed",
            "returncode": returncode,
            "elapsed_sec": elapsed_sec,
            "call_log_path": str(call_path),
            "codex_home": str(codex_home),
        }
        if error is not None:
            payload["error"] = error
        logger.event(
            "codex_call",
            **payload,
        )

    if startup_failure is not None:
        emit_event(error)
        raise startup_failure
    emit_event()
    if failure is not None:
        raise CmocError(
            "Codex CLI/TUI 呼び出しが失敗しました。",
            ["Codex CLI/TUI の出力と call log を確認してください。"],
            f"returncode: {returncode}\ncall_log: {call_path}",
        ) from failure
    assert returncode is not None
    return CommandResult(returncode, "", "")
