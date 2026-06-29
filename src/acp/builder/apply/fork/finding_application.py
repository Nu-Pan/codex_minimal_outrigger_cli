"""
`cmoc apply fork` の所見適用 builder。

Oracle: <work-root>/oracle/src/oracle/acp_builder/apply/fork/finding_application.py
"""

from typing import Any

from acp.builder.apply.fork._common import (
    adapt_oracle_parameter,
    ensure_oracle_src_importable,
    resolve_repo_root,
)
from basic.acp import AgentCallParameter


def build_apply_fork_finding_application_parameter(
    findings: list[dict[str, Any]],
) -> AgentCallParameter:
    """所見適用用 agent call parameter を構築する。"""
    repo_root = resolve_repo_root()
    ensure_oracle_src_importable(repo_root)

    from oracle.acp_builder.apply.fork.finding_application import (
        build_apply_fork_finding_application_parameter as build_oracle_parameter,
    )

    return adapt_oracle_parameter(build_oracle_parameter(findings))
