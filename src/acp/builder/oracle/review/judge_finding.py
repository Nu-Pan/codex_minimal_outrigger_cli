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

from acp.builder.common.prompt_fence import (
    _protect_review_sections,
)

__all__ = ["build_oracle_review_judge_finding_parameter"]


def build_oracle_review_judge_finding_parameter(
    finding: str,
    advocate_reasons: str,
    challenger_reasons: str,
) -> _AgentCallParameter:
    """canonical builder の parameter を再公開し、動的所見の fence を保護する。"""
    parameter = _build_parameter(finding, advocate_reasons, challenger_reasons)
    section_specs = (
        (
            "# 所見の内容",
            "\n\n# 所見が妥当であるとする理由",
            finding,
        ),
        (
            "# 所見が妥当であるとする理由",
            "\n\n# 所見が妥当ではないとする理由",
            advocate_reasons,
        ),
        (
            "# 所見が妥当ではないとする理由",
            "\n\n# place holder definition",
            challenger_reasons,
        ),
    )
    return _replace(
        parameter,
        prompt=_protect_review_sections(parameter.prompt, section_specs),
    )
