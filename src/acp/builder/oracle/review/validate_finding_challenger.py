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

from ...common.prompt_fence import (
    _protect_review_sections,
)

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
    section_specs = (
        (
            "# 対象所見",
            "\n\n# 既知の妥当であるとする理由",
            finding,
        ),
        (
            "# 既知の妥当であるとする理由",
            "\n\n# 既知の妥当ではないとする理由",
            known_advocate_reasons,
        ),
        (
            "# 既知の妥当ではないとする理由",
            "\n\n# place holder definition",
            known_challenger_reasons,
        ),
    )
    return _replace(
        parameter,
        prompt=_protect_review_sections(parameter.prompt, section_specs),
    )
