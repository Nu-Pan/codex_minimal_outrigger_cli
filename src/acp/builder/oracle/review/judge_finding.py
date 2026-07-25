"""oracle review finding judgment の realization adapter。

`acp.builder.oracle.review.judge_finding` から import する caller が残る間だけ維持する。
canonical 実装は
`{{work-root}}/oracle/src/oracle/acp_builder/oracle/review/judge_finding.py`。
全 caller が canonical oracle path を直接使うようになったら削除する。
"""

from dataclasses import replace as _replace

from oracle.acp_builder.basic import AgentCallParameter as _AgentCallParameter
from oracle.acp_builder.oracle.review.judge_finding import (
    build_oracle_review_judge_finding_parameter as _build_parameter,
)

from acp.builder.common.prompt_fence import _protect_code_block_fence

__all__ = ["build_oracle_review_judge_finding_parameter"]


def build_oracle_review_judge_finding_parameter(
    finding: str,
    advocate_reasons: str,
    challenger_reasons: str,
) -> _AgentCallParameter:
    """canonical builder の parameter を再公開し、動的所見の fence を保護する。"""
    parameter = _build_parameter(finding, advocate_reasons, challenger_reasons)
    prompt = _protect_code_block_fence(
        parameter.prompt,
        section_heading="# 所見の内容",
        section_end_marker="\n\n# 所見が妥当であるとする理由",
        info_string="text",
        section_body=finding,
    )
    prompt = _protect_code_block_fence(
        prompt,
        section_heading="# 所見が妥当であるとする理由",
        section_end_marker="\n\n# 所見が妥当ではないとする理由",
        info_string="text",
        section_body=advocate_reasons,
    )
    prompt = _protect_code_block_fence(
        prompt,
        section_heading="# 所見が妥当ではないとする理由",
        section_end_marker="\n\n# place holder definition",
        info_string="text",
        section_body=challenger_reasons,
    )
    return _replace(parameter, prompt=prompt)
