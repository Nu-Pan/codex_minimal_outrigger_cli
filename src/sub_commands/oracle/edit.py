"""`cmoc oracle edit` の CLI 本体。"""

from acp.builder.oracle.edit.launch_tui import (
    build_oracle_edit_launch_tui_parameter,
)
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

# {{work-root}}/oracle/doc/app_spec/sub_command/oracle_edit.md
ORACLE_EDIT_TEMPLATE = """<!--
以下の指示は `cmoc oracle edit` で自動注入されるため、このファイルに書いてはいけない。

- realization file の読み書き禁止
- oracle file の規約・規範
- TODO
-->"""


def cmoc_oracle_edit_impl() -> None:
    """CLI runtime を通して oracle edit を実行する。"""
    enable_indexing_preflight()
    run_cli_subcommand(
        _cmoc_oracle_edit_body,
        pre_log_check=ensure_prompt_editor_roots_ignored,
        command_name="oracle edit",
        command_argv=["cmoc", "oracle", "edit"],
        total_steps=4,
    )


def _cmoc_oracle_edit_body() -> None:
    """ユーザー指示を受け取り、固定 parameter で Codex TUI を起動する。"""
    root = repo_root()
    current_root = work_root()

    # {{work-root}}/oracle/doc/app_spec/prompt_editor_input.md
    start_subcommand_step(2, "oracle 最終状態の指示を入力", "edit oracle instruction")
    original_path, user_instruction = collect_prompt_editor_input(
        root,
        ORACLE_EDIT_TEMPLATE,
    )

    # 正本 builder の返却値を変更せず、そのまま TUI 起動へ渡す。
    start_subcommand_step(3, "TUI 起動パラメータを構築", "build TUI parameter")
    parameter = build_oracle_edit_launch_tui_parameter(
        original_path.name.removesuffix("_orig.md"),
        user_instruction,
    )
    start_subcommand_step(4, "Codex TUI を起動", "launch Codex TUI")
    run_codex_tui(
        parameter,
        root=root,
        cwd=current_root,
        config=load_config(current_root),
        purpose="oracle edit codex",
    )
