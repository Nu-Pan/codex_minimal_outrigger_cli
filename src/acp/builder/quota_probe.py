"""quota availability probe builder の旧 import 互換 adapter。

Oracle: <work-root>/oracle/src/oracle/acp_builder/quota_probe.py
"""

from importlib import import_module

from basic.acp import AgentCallParameter


def build_quota_availability_probe_parameter(
    base_parameter: AgentCallParameter,
) -> AgentCallParameter:
    # <work-root>/oracle/doc/app_spec/codex_exec_rule.md
    # Individual `codex exec` call parameters are canonical only under oracle.
    module = import_module("oracle.acp_builder.quota_probe")
    build_parameter = module.build_quota_availability_probe_parameter
    return build_parameter(base_parameter)


__all__ = ["build_quota_availability_probe_parameter"]
