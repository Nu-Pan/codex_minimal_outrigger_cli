from dataclasses import replace as _replace

from oracle.acp_builder.basic import AgentCallParameter as _AgentCallParameter
from oracle.acp_builder.oracle.review.validate_finding_advocate import (
    build_oracle_review_validate_finding_advocate_parameter as _build_parameter,
)

from acp.builder.common.prompt_fence import (
    _protect_review_sections,
)

__all__ = ["build_oracle_review_validate_finding_advocate_parameter"]


def build_oracle_review_validate_finding_advocate_parameter(
    finding: str,
    known_advocate_reasons: str,
    known_challenger_reasons: str,
) -> _AgentCallParameter:
    """canonical parameterを作り、既知のtypoと動的所見の fence だけを補正する。"""
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
    prompt = _fix_oracle_root_goal_typo(parameter.prompt)
    prompt = _protect_review_sections(prompt, section_specs)
    return _replace(parameter, prompt=prompt)


def _fix_oracle_root_goal_typo(prompt: str) -> str:
    """canonical promptに残るoracle root placeholderのtypoを一箇所だけ補正する。"""
    # 正本: {{work-root}}/oracle/src/oracle/acp_builder/oracle/review/validate_finding_advocate.py
    # {{work-root}}/oracle/doc/app_spec/prompt_standard.md は oracle src の static goal typo
    # に必要な最小 correction だけを許可する。finding と known reason は dynamic input
    # なので byte-for-byte で保持する。
    # oracle src が "`{{oracle-root}}`" を使うようになったら、この helper と test を削除する。
    return prompt.replace(
        "`{{oracle_root}}` ツリー内の oracle file を具体的な根拠とし",
        "`{{oracle-root}}` ツリー内の oracle file を具体的な根拠とし",
        1,
    )
