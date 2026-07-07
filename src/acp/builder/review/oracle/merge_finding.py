from oracle.acp_builder.basic import AgentCallParameter as _AgentCallParameter
from oracle.acp_builder.review.oracle.merge_finding import (
    build_review_oracle_merge_finding_parameter as _build_parameter,
)

__all__ = ["build_review_oracle_merge_finding_parameter"]


def build_review_oracle_merge_finding_parameter(
    known_findings: str,
) -> _AgentCallParameter:
    """正本 builder の parameter へ、既知 typo の prompt 補正だけを適用する。

    Oracle:
        `<work-root>/oracle/src/oracle/acp_builder/review/oracle/merge_finding.py`
    """
    parameter = _build_parameter(known_findings)
    return type(parameter)(
        parameter.model_class,
        parameter.reasoning_effort,
        parameter.file_access_mode,
        _fix_oracle_root_placeholder_definition(parameter.prompt),
        parameter.structured_output_schema_path,
        parameter.run_indexing_preflight,
    )


def _fix_oracle_root_placeholder_definition(prompt: str) -> str:
    """正本 prompt の placeholder 定義 typo だけを限定的に補正する。

    Oracle:
        `<work-root>/oracle/src/oracle/acp_builder/review/oracle/merge_finding.py`
    """
    # Oracle: <work-root>/oracle/src/oracle/acp_builder/review/oracle/merge_finding.py
    # <work-root>/oracle/doc/app_spec/prompt_standard.md permits only the
    # minimum correction needed for an oracle src bug; known findings are input.
    # Delete this helper and its tests once oracle src emits "- <oracle-root> =".
    marker = "\n# place holder definition\n"
    marker_index = prompt.rfind(marker)
    if marker_index == -1:
        return prompt
    prefix_end = marker_index + len(marker)
    prefix = prompt[:prefix_end]
    lines = prompt[prefix_end:].splitlines(keepends=True)
    for index, line in enumerate(lines):
        if line.startswith("- <<oracle-root>> ="):
            lines[index] = line.replace("- <<oracle-root>> =", "- <oracle-root> =", 1)
            break
    return prefix + "".join(lines)
