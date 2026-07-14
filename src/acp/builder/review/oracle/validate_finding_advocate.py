from dataclasses import replace

from oracle.acp_builder.basic import AgentCallParameter as _AgentCallParameter
from oracle.acp_builder.review.oracle.validate_finding_advocate import (
    build_review_oracle_validate_finding_advocate_parameter as _build_parameter,
)

__all__ = ["build_review_oracle_validate_finding_advocate_parameter"]


def build_review_oracle_validate_finding_advocate_parameter(
    finding: str,
    known_advocate_reasons: str,
    known_challenger_reasons: str,
) -> _AgentCallParameter:
    parameter = _build_parameter(
        finding,
        known_advocate_reasons,
        known_challenger_reasons,
    )
    return replace(
        parameter,
        prompt=_fix_oracle_root_goal_typo(parameter.prompt),
    )


def _fix_oracle_root_goal_typo(prompt: str) -> str:
    # Oracle: {{work-root}}/oracle/src/oracle/acp_builder/review/oracle/validate_finding_advocate.py
    # {{work-root}}/oracle/doc/app_spec/prompt_standard.md permits only the
    # minimum correction needed for the oracle src static goal typo; findings
    # and known reasons are dynamic input and must stay byte-for-byte intact.
    # Delete this helper and its tests once oracle src uses "`{{oracle-root}}`".
    return prompt.replace(
        "`{{oracle_root}}` ツリー内の oracle file を具体的な根拠とし",
        "`{{oracle-root}}` ツリー内の oracle file を具体的な根拠とし",
        1,
    )
