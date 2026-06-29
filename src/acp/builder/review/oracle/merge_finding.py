from oracle.acp_builder.review.oracle.merge_finding import *  # noqa: F403
from oracle.acp_builder.review.oracle.merge_finding import (
    build_review_oracle_merge_finding_parameter as _build_parameter,
)


def build_review_oracle_merge_finding_parameter(
    known_findings: str,
):
    parameter = _build_parameter(known_findings)
    # <work-root>/oracle/doc/app_spec/prompt_standard.md permits a minimal
    # realization-side patch when the oracle src prompt has a placeholder typo.
    return type(parameter)(
        parameter.model_class,
        parameter.reasoning_effort,
        parameter.file_access_mode,
        parameter.prompt.replace("<<oracle-root>>", "<oracle-root>"),
        parameter.structured_output_schema_path,
    )
