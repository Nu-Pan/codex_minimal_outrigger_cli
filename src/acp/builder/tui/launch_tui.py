"""TUI 起動 parameter builder の realization adapter。"""

from dataclasses import replace as _replace

from oracle.acp_builder.basic import AgentCallParameter as _AgentCallParameter
from oracle.acp_builder.tui.launch_tui import (
    build_tui_launch_tui_parameter as _build_parameter,
)


def build_tui_launch_tui_parameter(
    time_stamp: str,
    original_prompt: str,
    oracle_standard: bool,
    realization_standard: bool,
    oracle_review_standard: bool,
    apply_review_standard: bool,
) -> _AgentCallParameter:
    """正本 builder を呼び、TUI の非 Structured Output 契約を適用する。

    根拠: `{{work-root}}/oracle/src/oracle/acp_builder/tui/launch_tui.py`
    """
    # TUI は free-form prompt を受けるため schema 不要。正本の
    # `Path(__file__).with_suffix(".json")` は存在しない launch_tui.json を指す。
    return _replace(
        _build_parameter(
            time_stamp,
            original_prompt,
            oracle_standard,
            realization_standard,
            oracle_review_standard,
            apply_review_standard,
        ),
        structured_output_schema_path=None,
    )


__all__ = ["build_tui_launch_tui_parameter"]
