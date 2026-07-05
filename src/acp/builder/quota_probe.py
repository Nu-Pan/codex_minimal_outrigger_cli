"""Codex quota availability probe parameter builder."""

from basic.acp import AgentCallParameter


def build_quota_availability_probe_parameter(
    base_parameter: AgentCallParameter,
) -> AgentCallParameter:
    # Oracle: <work-root>/oracle/src/oracle/acp_builder/quota_probe.py
    # `<work-root>/oracle/doc/app_spec/codex_exec_rule.md` makes each Codex
    # exec call specification an oracle builder responsibility, so this
    # realization module only preserves the legacy import path.
    from oracle.acp_builder.quota_probe import (
        build_quota_availability_probe_parameter as build_oracle_parameter,
    )

    return build_oracle_parameter(base_parameter)


__all__ = ["build_quota_availability_probe_parameter"]
