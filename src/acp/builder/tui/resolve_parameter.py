"""TUI resolve-parameter building の realization adapter。

`acp.builder.tui.resolve_parameter` から import する caller が残る間だけ維持する。
canonical builder は
`{{work-root}}/oracle/src/oracle/acp_builder/tui/resolve_parameter.py` にある。
"""

from dataclasses import replace as _replace

from oracle.acp_builder.basic import AgentCallParameter as _AgentCallParameter
from oracle.acp_builder.tui.resolve_parameter import (
    build_tui_resolve_parameter_parameter as _build_parameter,
)

from acp.builder.common.prompt_fence import _protect_code_block_fence

__all__ = ["build_tui_resolve_parameter_parameter"]


def build_tui_resolve_parameter_parameter(
    original_prompt: str,
) -> _AgentCallParameter:
    """正本 builder の prompt を再公開し、入力 prompt の fence を保護する。"""
    parameter = _build_parameter(original_prompt)
    return _replace(
        parameter,
        prompt=_protect_code_block_fence(
            parameter.prompt,
            section_heading="# オリジナルプロンプト",
            section_end_marker="\n</cmoc_block>",
            info_string="markdown",
        ),
    )
