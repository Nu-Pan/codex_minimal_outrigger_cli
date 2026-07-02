"""Codex quota availability probe parameter の互換 wrapper。

Oracle: <work-root>/oracle/src/oracle/acp_builder/quota_probe.py
"""

from acp.builder.apply.fork._common import (
    adapt_oracle_parameter,
    ensure_oracle_src_importable,
    resolve_repo_root,
)
from basic.acp import AgentCallParameter


def build_quota_availability_probe_parameter(
    base_parameter: AgentCallParameter,
) -> AgentCallParameter:
    """quota probe parameter を oracle src の正本 builder から取得する。"""
    ensure_oracle_src_importable(resolve_repo_root())

    try:
        from oracle.acp_builder.quota_probe import (
            build_quota_availability_probe_parameter as build_oracle_parameter,
        )
    except ModuleNotFoundError as exc:
        if exc.name != "oracle.acp_builder.quota_probe":
            raise
        raise RuntimeError(
            "oracle quota probe builder is missing: "
            "oracle.acp_builder.quota_probe"
        ) from exc

    return adapt_oracle_parameter(build_oracle_parameter(base_parameter))


__all__ = ["build_quota_availability_probe_parameter"]
