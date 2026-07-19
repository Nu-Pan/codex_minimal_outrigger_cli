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
from commons.indexing import enable_indexing_preflight
from commons.prompt_editor_input import (
    collect_prompt_editor_input,
    ensure_prompt_editor_roots_ignored,
)

# {{work-root}}/oracle/doc/app_spec/sub_command/oracle_investigation.md
ORACLE_INVESTIGATION_TEMPLATE = """<!--
以下の指示は `cmoc oracle investigation` で自動注入されるため、このファイルに書いてはいけない。

- oracle file は読み取り専用
- realization file の読み書き禁止
- oracle file の規約・規範
- TODO
-->"""


def cmoc_oracle_investigation_impl() -> None:
    """CLI runtime を通して oracle investigation を実行する。"""
    enable_indexing_preflight()
    run_cli_subcommand(
        _cmoc_oracle_investigation_body,
        pre_log_check=ensure_prompt_editor_roots_ignored,
        command_name="oracle investigation",
        command_argv=["cmoc", "oracle", "investigation"],
        total_steps=4,
    )


def _cmoc_oracle_investigation_body() -> None:
    root = repo_root()
    current_root = work_root()
    start_subcommand_step(2, "oracle 調査指示を入力", "edit investigation")
    original_path, instruction = collect_prompt_editor_input(
        root,
        ORACLE_INVESTIGATION_TEMPLATE,
    )
    start_subcommand_step(3, "TUI 起動パラメータを構築", "build TUI parameter")
    parameter = build_oracle_investigation_launch_tui_parameter(
        original_path.name.removesuffix("_orig.md"),
        instruction,
    )
    start_subcommand_step(4, "Codex TUI を起動", "launch Codex TUI")
    run_codex_tui(
        parameter,
        root=root,
        cwd=current_root,
        config=load_config(current_root),
        purpose="oracle investigation",
    )
