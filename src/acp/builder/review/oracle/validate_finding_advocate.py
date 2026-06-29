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
    """所見擁護検証 prompt の oracle src typo を実行用に最小補正する。"""
    parameter = _build_parameter(
        finding,
        known_advocate_reasons,
        known_challenger_reasons,
    )
    # NOTE: <work-root>/oracle/doc/app_spec/prompt_standard.md は oracle src 側
    # typo の必要最小限の realization 側補正を許容する。
    return type(parameter)(
        parameter.model_class,
        parameter.reasoning_effort,
        parameter.file_access_mode,
        parameter.prompt.replace("<oracle_root>", "<oracle-root>"),
        parameter.structured_output_schema_path,
    )
