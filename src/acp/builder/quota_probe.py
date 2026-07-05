"""Codex quota availability probe parameter builder."""

from basic.acp import (
    AgentCallParameter,
    FileAccessMode,
    ModelClass,
    ReasoningEffort,
)


PROBE_PROMPT = "Reply OK."


def build_quota_availability_probe_parameter(
    base_parameter: AgentCallParameter,
) -> AgentCallParameter:
    # <work-root>/oracle/doc/app_spec/codex_exec_rule.md
    # Quota waiting must use a minimal Codex call; no oracle builder exists for
    # this small runtime-only probe, so the realization layer concretizes it.
    return AgentCallParameter(
        ModelClass.MINIMUM,
        ReasoningEffort.LOW,
        FileAccessMode.READONLY,
        PROBE_PROMPT,
        None,
        run_indexing_preflight=False,
        cwd=base_parameter.cwd,
    )


__all__ = ["PROBE_PROMPT", "build_quota_availability_probe_parameter"]
