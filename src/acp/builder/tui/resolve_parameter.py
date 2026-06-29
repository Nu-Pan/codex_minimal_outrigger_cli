"""Compatibility import path for TUI resolve-parameter building.

Kept while callers import from `acp.builder.tui.resolve_parameter`; prompt
construction stays delegated to the canonical oracle builder. The realization
schema path is used because the oracle JSON currently has inconsistent
`required` and `properties` keys for the file access profile field.
"""

from pathlib import Path

from oracle.acp_builder.basic import AgentCallParameter
from oracle.acp_builder.tui.resolve_parameter import (
    build_tui_resolve_parameter_parameter as _build_parameter,
)


def build_tui_resolve_parameter_parameter(original_prompt: str) -> AgentCallParameter:
    parameter = _build_parameter(original_prompt)
    return type(parameter)(
        parameter.model_class,
        parameter.reasoning_effort,
        parameter.faprofile,
        parameter.prompt,
        Path(__file__).with_suffix(".json"),
    )


__all__ = ["build_tui_resolve_parameter_parameter"]
