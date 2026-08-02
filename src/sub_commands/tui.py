from collections.abc import Callable
from pathlib import Path

from acp.builder.tui.launch_tui import build_tui_launch_tui_parameter
from cmoc_runtime import (
    load_config,
    repo_root,
    run_cli_subcommand,
    run_codex_tui,
    start_subcommand_step,
    work_root,
)
from commons.indexing import enable_indexing_preflight
from commons.prompt_editor_input import (
    collect_prompt_editor_input,
    ensure_prompt_editor_roots_ignored,
)
from commons.runtime_results import CommandResult
from config.cmoc_config import CmocConfig

CodexTui = Callable[..., CommandResult]


def cmoc_tui_impl() -> None:
    """CLI runtime を通して tui を実行する。"""
    enable_indexing_preflight()
    run_cli_subcommand(
        _cmoc_tui_from_current_context,
        pre_log_check=ensure_prompt_editor_roots_ignored,
        command_name="tui",
        command_argv=["cmoc", "tui"],
        total_steps=3,
    )


def _cmoc_tui_body(
    run_codex_tui: CodexTui,
    *,
    root: Path,
    config: CmocConfig,
) -> None:
    """依頼文を編集し、固定パラメータで Codex TUI を起動する。"""
    # {{work-root}}/oracle/doc/app_spec/prompt_editor_input.md
    start_subcommand_step(2, "オリジナルプロンプトを入力", "edit original prompt")
    original_path, original_prompt = collect_prompt_editor_input(root, "")

    # {{work-root}}/oracle/doc/app_spec/sub_command/tui.md
    parameter = build_tui_launch_tui_parameter(
        original_path.name.removesuffix("_orig.md"),
        original_prompt,
    )

    start_subcommand_step(3, "AI Agent TUI を起動", "launch agent TUI")
    run_codex_tui(
        parameter,
        root=root,
        config=config,
        purpose="tui codex",
    )


def _cmoc_tui_from_current_context() -> None:
    """現在の repository 状態から `cmoc tui` の本体処理を起動する。"""
    root = repo_root()
    current_root = work_root()
    _cmoc_tui_body(
        run_codex_tui,
        root=root,
        config=load_config(current_root),
    )
