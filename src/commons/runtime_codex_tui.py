import json
import subprocess
import time
from pathlib import Path

from basic.acp import AgentCallParameter
from basic.path_model import AgentCallPathContext
from config.cmoc_config import CmocConfig

from .runtime_codex_logging import (
    emit_codex_call_console,
    format_codex_call_error,
)
from .runtime_codex_profile import (
    codex_subprocess_env,
    prepare_codex_override_args,
    resolve_codex_home,
    run_codex_subprocess,
    validate_codex_home,
)
from .runtime_config import load_config
from .runtime_errors import CmocError
from .runtime_logging import current_subcommand_logger
from .runtime_paths import (
    _reserve_timestamped_path,
    codex_log_dir,
    timestamp,
)
from .runtime_results import CommandResult


def run_codex_tui(
    parameter: AgentCallParameter,
    *,
    root: Path | None = None,
    config: CmocConfig | None = None,
    purpose: str = "codex tui",
) -> CommandResult:
    """Codex TUI を設定上書き argv と call log を準備して起動する。"""
    path_context = AgentCallPathContext(parameter.agent_call_cwd)
    root = root or path_context.repo_root
    config = config or load_config(path_context.work_root)
    log_dir = codex_log_dir(root)
    log_dir.mkdir(parents=True, exist_ok=True)
    agent_call_cwd = path_context.agent_call_cwd
    # {{work-root}}/oracle/doc/app_spec/codex_exec_rule.md
    # 利用者指定の env value は変更せず、Codex が相対 CODEX_HOME を解決する場所に
    # validation を合わせる。
    codex_home = resolve_codex_home(agent_call_cwd)
    validate_codex_home(codex_home)
    override_args = prepare_codex_override_args(
        parameter,
        config,
    )
    argv = [
        "codex",
        *override_args,
        "--cd",
        str(agent_call_cwd),
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
                "cwd": str(agent_call_cwd),
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
            cwd=agent_call_cwd,
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

    def _emit_event(error: str | None = None) -> None:
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
        _emit_event(error)
        raise startup_failure
    _emit_event()
    if failure is not None:
        raise CmocError(
            "Codex CLI/TUI 呼び出しが失敗しました。",
            ["Codex CLI/TUI の出力と call log を確認してください。"],
            f"returncode: {returncode}\ncall_log: {call_path}",
        ) from failure
    assert returncode is not None
    return CommandResult(returncode, "", "")
