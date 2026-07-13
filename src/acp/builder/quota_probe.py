"""`<work-root>/oracle/src/oracle/acp_builder/quota_probe.py` の互換入口。"""

from basic.acp import AgentCallParameter


__all__ = ["build_quota_availability_probe_parameter"]


def build_quota_availability_probe_parameter(
    base_parameter: AgentCallParameter,
) -> AgentCallParameter:
    """正本 builder の結果をそのまま返す。"""
    from oracle.acp_builder.quota_probe import (
        build_quota_availability_probe_parameter as build_oracle_parameter,
    )

    return build_oracle_parameter(base_parameter)
