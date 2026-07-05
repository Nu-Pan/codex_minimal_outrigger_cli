"""Codex quota availability probe parameter builder wrapper."""

from importlib import import_module

from basic.acp import AgentCallParameter


def build_quota_availability_probe_parameter(
    base_parameter: AgentCallParameter,
) -> AgentCallParameter:
    # <work-root>/oracle/doc/app_spec/codex_exec_rule.md
    # <work-root>/oracle/doc/app_spec/prompt_standard.md
    # Probe prompt ownership stays in oracle src; missing canonical builder
    # must fail instead of substituting a realization-owned prompt.
    module = import_module("oracle.acp_builder.quota_probe")
    return module.build_quota_availability_probe_parameter(base_parameter)


__all__ = ["build_quota_availability_probe_parameter"]
