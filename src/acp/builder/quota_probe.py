"""Codex quota availability probe parameter builder。"""

from basic.acp import AgentCallParameter, FileAccessMode, ModelClass, ReasoningEffort

PROBE_PROMPT = "Reply OK."


def build_quota_availability_probe_parameter(
    base_parameter: AgentCallParameter,
) -> AgentCallParameter:
    # <work-root>/oracle/doc/app_spec/codex_exec_rule.md
    # The oracle requirement is only a minimal Codex CLI call; there is no
    # oracle src builder for this purpose, so realization keeps the probe here.
    return AgentCallParameter(
        ModelClass.MINIMUM,
        ReasoningEffort.LOW,
        FileAccessMode.READONLY,
        PROBE_PROMPT,
        None,
        False,
    )


__all__ = ["build_quota_availability_probe_parameter"]
