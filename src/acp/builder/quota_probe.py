"""Codex quota availability probe parameter builder."""

from basic.acp import (
    AgentCallParameter,
    FileAccessMode,
    ModelClass,
    ReasoningEffort,
)


_PROBE_PROMPT = "Run a minimal quota availability check and answer only: ok"


def build_quota_availability_probe_parameter(
    base_parameter: AgentCallParameter,
) -> AgentCallParameter:
    # <work-root>/oracle/doc/app_spec/codex_exec_rule.md
    # The probe exists only to test Codex CLI availability after quota failure,
    # so it must avoid schema validation, indexing preflight, and write access.
    return AgentCallParameter(
        ModelClass.MINIMUM,
        ReasoningEffort.LOW,
        FileAccessMode.READONLY,
        _PROBE_PROMPT,
        None,
        run_indexing_preflight=False,
        cwd=base_parameter.cwd,
    )


__all__ = ["build_quota_availability_probe_parameter"]
