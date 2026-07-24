"""oracle review challenger validation の realization adapter。

`acp.builder.oracle.review.validate_finding_challenger` から import する caller が残る間だけ
維持する。canonical 実装は
`{{work-root}}/oracle/src/oracle/acp_builder/oracle/review/validate_finding_challenger.py`。
全 caller が canonical oracle path を直接使うようになったら削除する。
"""

from dataclasses import replace as _replace

from oracle.acp_builder.basic import AgentCallParameter as _AgentCallParameter
from oracle.acp_builder.oracle.review.validate_finding_challenger import (
    build_oracle_review_validate_finding_challenger_parameter as _build_parameter,
)

from acp.builder.common.prompt_fence import _protect_code_block_fence

__all__ = ["build_oracle_review_validate_finding_challenger_parameter"]


def build_oracle_review_validate_finding_challenger_parameter(
    finding: str,
    known_advocate_reasons: str,
    known_challenger_reasons: str,
) -> _AgentCallParameter:
    """canonical builder の parameter を再公開し、動的所見の fence を保護する。"""
    parameter = _build_parameter(
        finding,
        known_advocate_reasons,
        known_challenger_reasons,
    )
    prompt = _protect_code_block_fence(
        parameter.prompt,
        section_heading="# 対象所見",
        section_end_marker="\n\n# 既知の妥当であるとする理由",
        info_string="text",
    )
    prompt = _protect_code_block_fence(
        prompt,
        section_heading="# 既知の妥当であるとする理由",
        section_end_marker="\n\n# 既知の妥当ではないとする理由",
        info_string="text",
    )
    prompt = _protect_code_block_fence(
        prompt,
        section_heading="# 既知の妥当ではないとする理由",
        section_end_marker="\n\n# place holder definition",
        info_string="text",
        # challenger reasons is the final dynamic section, so a placeholder-like
        # heading in its content must not outrank the actual prompt boundary.
        # {{work-root}}/oracle/doc/app_spec/prompt_standard.md
        prefer_last_end_marker=True,
    )
    return _replace(parameter, prompt=prompt)
