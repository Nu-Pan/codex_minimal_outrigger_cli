"""realization refactor の change summary builder を適合させる adapter。

対応する oracle file:
`{{work-root}}/oracle/src/oracle/acp_builder/realization/refactor/fork/change_summary.py`
`{{work-root}}/oracle/src/oracle/acp_builder/realization/refactor/fork/change_summary.json`。
"""

from dataclasses import replace as _replace

from oracle.acp_builder.basic import AgentCallParameter as _AgentCallParameter
from oracle.acp_builder.realization.refactor.fork.change_summary import (
    build_realization_refactor_fork_change_summary_parameter as _build_parameter,
)

from ....common.prompt_fence import (
    _protect_code_block_fence,
)

__all__ = ["build_realization_refactor_fork_change_summary_parameter"]


def build_realization_refactor_fork_change_summary_parameter(
    raw_git_diff: str,
) -> _AgentCallParameter:
    """正本 builder の prompt を再公開し、raw diff の fence を保護する。"""
    parameter = _build_parameter(raw_git_diff)
    return _replace(
        parameter,
        prompt=_protect_code_block_fence(
            parameter.prompt,
            section_heading="# run branch 上の refactor 差分",
            section_end_marker="\n\n# place holder definition",
            info_string="diff",
            section_body=raw_git_diff,
        ),
    )
