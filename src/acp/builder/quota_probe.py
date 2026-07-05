"""Codex quota availability probe parameter builder."""

from importlib import import_module
from typing import Callable

from basic.acp import (
    AgentCallParameter,
    FileAccessMode,
    ModelClass,
    ReasoningEffort,
)


_PROBE_PROMPT = "Reply OK."


def _oracle_builder() -> Callable[[AgentCallParameter], AgentCallParameter] | None:
    try:
        module = import_module("oracle.acp_builder.quota_probe")
    except ModuleNotFoundError as error:
        if error.name != "oracle.acp_builder.quota_probe":
            raise
        return None
    return module.build_quota_availability_probe_parameter


def build_quota_availability_probe_parameter(
    base_parameter: AgentCallParameter,
) -> AgentCallParameter:
    if (builder := _oracle_builder()) is not None:
        return builder(base_parameter)

    # <work-root>/oracle/doc/app_spec/codex_exec_rule.md
    # Quota probe is a Codex exec call. Until a writable oracle builder exists,
    # keep this fallback minimal and isolated so it can disappear cleanly.
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
