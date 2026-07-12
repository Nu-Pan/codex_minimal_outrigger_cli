"""Compatibility adapter for the canonical quota availability probe builder.

The canonical prompt and call settings belong to
`<work-root>/oracle/src/oracle/acp_builder/quota_probe.py`.
"""

from basic.acp import AgentCallParameter


__all__ = ["build_quota_availability_probe_parameter"]


def build_quota_availability_probe_parameter(
    base_parameter: AgentCallParameter,
) -> AgentCallParameter:
    """Delegate quota probe construction to the oracle builder."""
    # Keep this import lazy so the compatibility module remains importable in
    # layouts where the human-owned oracle builder has not been installed yet;
    # there is intentionally no realization-side prompt or parameter fallback.
    from oracle.acp_builder.quota_probe import (
        build_quota_availability_probe_parameter as build_oracle_parameter,
    )

    return build_oracle_parameter(base_parameter)
