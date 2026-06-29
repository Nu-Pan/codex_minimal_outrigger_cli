"""`<work-root>/oracle/src/oracle/acp_builder/tui/launch_tui.py` を接続する。

TUI 起動パラメータの正本を oracle 側に保ったまま既存の
`acp.builder.tui.launch_tui` 参照を成立させるために残す。削除条件は
realization 側と利用者向け公開面からこの import path 参照がなくなること。
"""

from dataclasses import replace

from basic.acp import AgentCallParameter, FileAccessMode
from oracle.acp_builder.tui.launch_tui import (
    build_tui_launch_tui_parameter as _build_tui_launch_tui_parameter,
)


def build_tui_launch_tui_parameter(
    time_stamp: str,
    role: str,
    summary: str,
    goal: str,
    file_access_mode: FileAccessMode,
    original_prompt: str,
    oracle_and_realization_basic: bool,
    oracle_standard: bool,
    realization_standard: bool,
    review_oracle_standard: bool,
    apply_review_standard: bool,
    index_entry_standard: bool,
) -> AgentCallParameter:
    parameter = _build_tui_launch_tui_parameter(
        time_stamp,
        role,
        summary,
        goal,
        file_access_mode,
        original_prompt,
        oracle_and_realization_basic,
        oracle_standard,
        realization_standard,
        review_oracle_standard,
        apply_review_standard,
        index_entry_standard,
    )
    # <work-root>/oracle/src/oracle/acp_builder/basic.py
    # TUI 起動は Structured Output を要求しない対話起動なので schema を渡さない。
    return replace(parameter, structured_output_schema_path=None)


__all__ = ["build_tui_launch_tui_parameter"]
