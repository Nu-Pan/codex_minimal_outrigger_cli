"""oracle review finding merge の realization adapter。

canonical 実装は
`{{work-root}}/oracle/src/oracle/acp_builder/oracle/review/merge_finding.py`。
"""

from dataclasses import replace as _replace

from oracle.acp_builder.basic import AgentCallParameter as _AgentCallParameter
from oracle.acp_builder.oracle.review.merge_finding import (
    build_oracle_review_merge_finding_parameter as _build_parameter,
)

from acp.builder.common.prompt_fence import _protect_code_block_fence

__all__ = ["build_oracle_review_merge_finding_parameter"]


def build_oracle_review_merge_finding_parameter(
    findings: str,
) -> _AgentCallParameter:
    """canonical builder の parameter を再公開し、動的所見の fence を保護する。"""
    parameter = _build_parameter(findings)
    return _replace(
        parameter,
        prompt=_protect_code_block_fence(
            parameter.prompt,
            section_heading="# 現状の所見リスト",
            section_end_marker="\n\n# place holder definition",
            info_string="text",
            # findings is dynamic and may contain a placeholder-like heading;
            # the final marker is the canonical prompt boundary.
            # {{work-root}}/oracle/doc/app_spec/prompt_standard.md
            prefer_last_end_marker=True,
        ),
    )
