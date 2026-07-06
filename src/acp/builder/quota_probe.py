"""Codex quota availability probe parameter builder."""

from basic.acp import (
    AgentCallParameter,
    FileAccessMode,
    ModelClass,
    ReasoningEffort,
)


_PROBE_PROMPT = "quota 回復確認のための最小実行です。短く完了してください。"


def build_quota_availability_probe_parameter(
    base_parameter: AgentCallParameter,
) -> AgentCallParameter:
    # <work-root>/oracle/doc/app_spec/prompt_standard.md
    # <work-root>/oracle/doc/app_spec/codex_exec_rule.md
    # oracle src lacks a quota probe builder, but quota recovery cannot depend
    # on a missing module. Keep this realization-only completion minimal.
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
