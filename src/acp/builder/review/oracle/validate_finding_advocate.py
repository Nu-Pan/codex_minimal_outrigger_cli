from oracle.acp_builder.basic import AgentCallParameter
from oracle.acp_builder.review.oracle.validate_finding_advocate import *  # noqa: F403
from oracle.acp_builder.review.oracle.validate_finding_advocate import (
    build_review_oracle_validate_finding_advocate_parameter as _build_parameter,
)


def build_review_oracle_validate_finding_advocate_parameter(
    finding: str,
    known_advocate_reasons: str,
    known_challenger_reasons: str,
) -> AgentCallParameter:
    parameter = _build_parameter(
        finding,
        known_advocate_reasons,
        known_challenger_reasons,
    )
    return type(parameter)(
        parameter.model_class,
        parameter.reasoning_effort,
        parameter.faprofile,
        _fix_oracle_root_goal_typo(parameter.prompt),
        parameter.structured_output_schema_path,
    )


def _fix_oracle_root_goal_typo(prompt: str) -> str:
    # Oracle: <work-root>/oracle/src/oracle/acp_builder/review/oracle/validate_finding_advocate.py
    # <work-root>/oracle/doc/app_spec/prompt_standard.md permits only the
    # minimum correction needed for the oracle src static goal typo; findings
    # and known reasons are dynamic input and must stay byte-for-byte intact.
    # Delete this helper and its tests once oracle src uses "`<oracle-root>`".
    return prompt.replace(
        "`<oracle_root>` ツリー内の oracle file を具体的な根拠とし",
        "`<oracle-root>` ツリー内の oracle file を具体的な根拠とし",
        1,
    )
