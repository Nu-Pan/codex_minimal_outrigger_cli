"""Codex quota availability probe parameter builder."""

from importlib import import_module

from basic.acp import (
    AgentCallParameter,
    FileAccessMode,
    ModelClass,
    ReasoningEffort,
)

_FALLBACK_PROMPT = "Codex CLI quota 回復確認のため、短く ok とだけ応答してください。"


def _fallback_parameter(base_parameter: AgentCallParameter) -> AgentCallParameter:
    # <work-root>/oracle/doc/app_spec/codex_exec_rule.md
    # <work-root>/oracle/doc/app_spec/prompt_standard.md
    # oracle quota probe builder is absent in the current oracle src. This
    # narrow fallback keeps mandatory quota polling executable until the oracle
    # builder is added; it must disappear when that canonical builder exists.
    return AgentCallParameter(
        ModelClass.MINIMUM,
        ReasoningEffort.LOW,
        FileAccessMode.READONLY,
        _FALLBACK_PROMPT,
        None,
        run_indexing_preflight=False,
        cwd=base_parameter.cwd,
    )


def build_quota_availability_probe_parameter(
    base_parameter: AgentCallParameter,
) -> AgentCallParameter:
    try:
        module = import_module("oracle.acp_builder.quota_probe")
    except ModuleNotFoundError as error:
        if error.name != "oracle.acp_builder.quota_probe":
            raise
        return _fallback_parameter(base_parameter)
    return module.build_quota_availability_probe_parameter(base_parameter)


__all__ = ["build_quota_availability_probe_parameter"]
