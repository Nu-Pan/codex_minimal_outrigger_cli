from oracle.acp_builder.basic import AgentCallParameter
from oracle.acp_builder.review.oracle.merge_finding import *  # noqa: F403
from oracle.acp_builder.review.oracle.merge_finding import (
    build_review_oracle_merge_finding_parameter as _build_parameter,
)


def build_review_oracle_merge_finding_parameter(
    known_findings: str,
) -> AgentCallParameter:
    parameter = _build_parameter(known_findings)
    return type(parameter)(
        parameter.model_class,
        parameter.reasoning_effort,
        parameter.file_access_mode,
        _fix_oracle_root_placeholder_definition(parameter.prompt),
        parameter.structured_output_schema_path,
    )


def _fix_oracle_root_placeholder_definition(prompt: str) -> str:
    # <work-root>/oracle/doc/app_spec/prompt_standard.md permits only the
    # minimum correction needed for an oracle src bug; known findings are input.
    return "".join(
        line.replace("- <<oracle-root>> =", "- <oracle-root> =", 1)
        if line.startswith("- <<oracle-root>> =")
        else line
        for line in prompt.splitlines(keepends=True)
    )
