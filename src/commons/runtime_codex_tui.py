import json
import subprocess
import time
from pathlib import Path

from basic.acp import AgentCallParameter
from config.cmoc_config import CmocConfig

from commons.runtime_config import load_config
from commons.runtime_codex_logging import emit_codex_call_console
from commons.runtime_codex_profile import (
    codex_profile_name,
    codex_subprocess_env,
    file_access_to_codex_cwd,
    prepare_codex_profile,
    resolve_codex_home,
    run_codex_subprocess,
    validate_codex_home,
)
from commons.runtime_errors import CmocError
from commons.runtime_logging import current_subcommand_logger
from commons.runtime_paths import codex_log_dir, repo_root, timestamp, work_root
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
    """Codex TUI を profile と call log を準備して起動する。"""
    root = root or repo_root()
    cwd = cwd or root
    config = config or load_config(root)
    log_dir = codex_log_dir(root)
    log_dir.mkdir(parents=True, exist_ok=True)
    ts = timestamp()
    call_path = log_dir / f"{ts}_tui_call.json"
    codex_work_root = work_root(cwd)
    codex_cwd = file_access_to_codex_cwd(parameter.file_access_mode, codex_work_root)
    # <work-root>/oracle/doc/app_spec/codex_exec_rule.md
    # Match validation/profile placement to where Codex resolves a relative
    # CODEX_HOME while keeping the user-provided env value unchanged.
    codex_home = resolve_codex_home(codex_cwd)
    validate_codex_home(codex_home)
    # <work-root>/oracle/doc/app_spec/sub_command/tui.md
    # TUI complete prompt is stored under <repo-root> even when Codex runs in a
    # linked worktree; writable roots and schema state still follow codex_work_root.
    profile_path = prepare_codex_profile(
        parameter,
        config,
        codex_home,
        codex_work_root,
        extra_read_paths,
        extra_read_root=root,
    )
    profile_name = codex_profile_name(profile_path)
    argv = [
        "codex",
        "--profile",
        profile_name,
        "--cd",
        str(codex_cwd),
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
    started_at = time.perf_counter()
    failure: subprocess.CalledProcessError | None = None
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
    elapsed_sec = time.perf_counter() - started_at
    emit_codex_call_console(purpose, call_path, elapsed_sec, returncode)
    logger = current_subcommand_logger()
    status = "succeeded" if returncode == 0 else "failed"

    def emit_event(error: str | None = None) -> None:
        if logger is None:
            return
        payload = {
            "purpose": purpose,
            "status": status if error is None else "failed",
            "returncode": returncode,
            "elapsed_sec": elapsed_sec,
            "call_log_path": str(call_path),
            "codex_home": str(codex_home),
            "profile_name": profile_name,
            "profile_path": str(profile_path),
        }
        if error is not None:
            payload["error"] = error
        logger.event(
            "codex_call",
            **payload,
        )

    emit_event()
    if failure is not None:
        raise CmocError(
            "Codex CLI/TUI 呼び出しが失敗しました。",
            ["Codex CLI/TUI の出力と call log を確認してください。"],
            f"returncode: {returncode}\ncall_log: {call_path}",
        ) from failure
    return CommandResult(returncode, "", "")
