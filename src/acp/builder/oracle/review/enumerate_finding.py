"""oracle review finding enumeration の realization adapter。

`acp.builder.oracle.review.enumerate_finding` から import する呼び出し元が
残る間だけ維持する。canonical 実装は
`{{work-root}}/oracle/src/oracle/acp_builder/oracle/review/enumerate_finding.py`。
全呼び出し元が canonical oracle path を直接使うようになったら削除できる。
"""

from pathlib import Path as _Path

from oracle.acp_builder.oracle.review.enumerate_finding import (
    build_oracle_review_enumerate_finding_parameter as _build_enumerate_parameter,
)

from basic.acp import AgentCallParameter as _AgentCallParameter


def build_oracle_review_enumerate_finding_parameter(
    oracle_path: _Path,
    related_findings: str,
) -> _AgentCallParameter:
    """canonical builder の parameter をそのまま再公開する。"""
    return _build_enumerate_parameter(oracle_path, related_findings)


__all__ = ["build_oracle_review_enumerate_finding_parameter"]
