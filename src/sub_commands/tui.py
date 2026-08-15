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
    ORIGINAL_PROMPT_PLACEHOLDER,
    collect_prompt_editor_input,
    edit_prompt_editor_input,
    ensure_prompt_editor_roots_ignored,
    finalize_prompt_editor_input,
    reserve_prompt_editor_input,
)
from commons.runtime_results import CommandResult
from config.cmoc_config import CmocConfig

_CodexTui = Callable[..., CommandResult]


def cmoc_tui_impl() -> None:
    """CLI runtime を通して tui を実行する。"""
    enable_indexing_preflight()
    run_cli_subcommand(
        _cmoc_tui_from_current_context,
        pre_log_check=ensure_prompt_editor_roots_ignored,
        command_name="tui",
        command_argv=["cmoc", "tui"],
        tui_process=True,
        total_steps=5,
    )


def _cmoc_tui_body(
    run_codex_tui: _CodexTui,
    *,
    root: Path,
    config: CmocConfig,
) -> None:
    """依頼文を編集し、構築したパラメータで Codex TUI を起動する。"""
    # オリジナル prompt だけ未確定の完全 prompt を初期表示に使う。
    # {{work-root}}/oracle/doc/app_spec/sub_command/tui.md
    start_subcommand_step(
        2, "完全プロンプトの skeleton を構築", "build prompt skeleton"
    )
    editor_work_path, input_copy_path = reserve_prompt_editor_input(root)
    complete_prompt_skeleton = build_tui_launch_tui_parameter(
        ORIGINAL_PROMPT_PLACEHOLDER
    ).prompt

    # {{work-root}}/oracle/doc/app_spec/prompt_editor_input.md
    start_subcommand_step(3, "オリジナルプロンプトを入力", "edit original prompt")
    edit_prompt_editor_input(
        root,
        editor_work_path,
        complete_prompt_skeleton,
    )
    original_prompt = collect_prompt_editor_input(
        root,
        editor_work_path,
        input_copy_path,
    )

    # 抽出した入力から担当固有の完全 prompt と起動パラメータを構築する。
    # {{work-root}}/oracle/doc/app_spec/sub_command/tui.md
    start_subcommand_step(4, "TUI 起動パラメータを構築", "build TUI parameter")
    parameter = build_tui_launch_tui_parameter(original_prompt)
    finalize_prompt_editor_input(editor_work_path)

    start_subcommand_step(5, "AI Agent TUI を起動", "launch agent TUI")
    run_codex_tui(
        parameter,
        root=root,
        config=config,
        purpose="tui codex",
        notification_command_name="tui",
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
