"""Codex quota availability probe parameter compatibility builder."""

from importlib import import_module

from basic.acp import AgentCallParameter


def build_quota_availability_probe_parameter(
    base_parameter: AgentCallParameter,
) -> AgentCallParameter:
    # <work-root>/oracle/doc/app_spec/prompt_standard.md
    # <work-root>/oracle/doc/app_spec/codex_exec_rule.md
    builder = import_module("oracle.acp_builder.quota_probe")
    return builder.build_quota_availability_probe_parameter(base_parameter)


__all__ = ["build_quota_availability_probe_parameter"]
