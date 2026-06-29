from oracle.acp_builder.basic import AgentCallParameter
from oracle.acp_builder.review.oracle.merge_finding import *  # noqa: F403
from oracle.acp_builder.review.oracle.merge_finding import (
    build_review_oracle_merge_finding_parameter as _build_parameter,
)


def build_review_oracle_merge_finding_parameter(
    known_findings: str,
) -> AgentCallParameter:
    """所見マージ prompt の oracle src typo を実行用に最小補正する。"""
    parameter = _build_parameter(known_findings)
    # NOTE: <work-root>/oracle/doc/app_spec/prompt_standard.md は oracle src 側
    # typo の必要最小限の realization 側補正を許容する。
    return type(parameter)(
        parameter.model_class,
        parameter.reasoning_effort,
        parameter.file_access_mode,
        parameter.prompt.replace("<<oracle-root>>", "<oracle-root>"),
        parameter.structured_output_schema_path,
    )
