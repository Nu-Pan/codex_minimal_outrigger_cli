"""quota availability probe 用 ACP builder。

Oracle: <work-root>/oracle/doc/app_spec/codex_exec_rule.md
Oracle: <work-root>/oracle/doc/app_spec/prompt_standard.md

現行 oracle src には quota probe 専用 builder がないため、この adapter は
runtime 側に prompt literal を置かないための暫定境界である。削除条件は
`<work-root>/oracle/src/oracle/acp_builder` に同用途の builder が追加されること。
"""

from basic.acp import AgentCallParameter


def build_quota_availability_probe_parameter(
    base_parameter: AgentCallParameter,
) -> AgentCallParameter:
    return AgentCallParameter(
        base_parameter.model_class,
        base_parameter.reasoning_effort,
        base_parameter.file_access_mode,
        "quota availability probe",
        None,
    )
