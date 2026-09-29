"""`cmoc oracle investigation` の read-only TUI workload。"""

from acp.builder.oracle.investigation.launch_tui import (
    build_oracle_investigation_launch_tui_parameter,
)
from cmoc_runtime import (
    load_config,
    repo_root,
    run_cli_subcommand,
    run_codex_tui,
    start_subcommand_step,
    work_root,
)
from commons.prompt_editor_input import (
    ORIGINAL_PROMPT_PLACEHOLDER,
    collect_prompt_editor_input,
    edit_prompt_editor_input,
    ensure_prompt_editor_roots_ignored,
    reserve_prompt_editor_input,
)
from commons.runtime_document_search_scope import oracle_doc_scope


def cmoc_oracle_investigation_impl() -> None:
    """CLI runtime を通して oracle investigation を実行する。"""
    run_cli_subcommand(
        _cmoc_oracle_investigation_body,
        pre_log_check=ensure_prompt_editor_roots_ignored,
        command_name="oracle investigation",
        command_argv=["cmoc", "oracle", "investigation"],
        tui_process=True,
        total_steps=5,
    )


def _cmoc_oracle_investigation_body() -> None:
    """入力された oracle 調査指示から Codex TUI を起動する。"""
    root = repo_root()
    current_root = work_root()
    search_scope = oracle_doc_scope()

    # oracle 調査契約を含む完全 prompt の skeleton を handoff ガイドに使う。
    # {{work-root}}/oracle/doc/app_spec/sub_command/oracle_investigation.md
    start_subcommand_step(
        2, "完全プロンプトの skeleton を構築", "build prompt skeleton"
    )
    input_path = reserve_prompt_editor_input(root)
    complete_prompt_skeleton = build_oracle_investigation_launch_tui_parameter(
        ORIGINAL_PROMPT_PLACEHOLDER,
        document_search_scope=search_scope,
    ).prompt

    start_subcommand_step(3, "oracle 調査指示を入力", "edit investigation")
    edit_prompt_editor_input(
        root,
        input_path,
        complete_prompt_skeleton,
    )
    instruction = collect_prompt_editor_input(
        root,
        input_path,
    )

    start_subcommand_step(4, "TUI 起動パラメータを構築", "build TUI parameter")
    parameter = build_oracle_investigation_launch_tui_parameter(
        instruction, document_search_scope=search_scope
    )
    start_subcommand_step(5, "Codex TUI を起動", "launch Codex TUI")
    run_codex_tui(
        parameter,
        root=root,
        config=load_config(current_root),
        purpose="oracle investigation",
        notification_command_name="oracle investigation",
    )
