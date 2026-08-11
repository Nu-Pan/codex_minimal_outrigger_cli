"""oracle review finding enumeration の realization adapter。

`acp.builder.oracle.review.enumerate_finding` から import する呼び出し元が
残る間だけ維持する。canonical 実装は
`{{work-root}}/oracle/src/oracle/acp_builder/oracle/review/enumerate_finding.py`。
全呼び出し元が canonical oracle path を直接使うようになったら削除できる。
"""

from dataclasses import replace as _replace
from pathlib import Path as _Path

from oracle.acp_builder.oracle.review.enumerate_finding import (
    build_oracle_review_enumerate_finding_parameter as _build_enumerate_parameter,
)

from basic.acp import AgentCallParameter as _AgentCallParameter

from ...common.prompt_fence import _protect_code_block_fence


def build_oracle_review_enumerate_finding_parameter(
    oracle_path: _Path,
    related_findings: str,
) -> _AgentCallParameter:
    """canonical builder の parameter を再公開し、動的所見の fence を保護する。"""
    parameter = _build_enumerate_parameter(oracle_path, related_findings)
    return _replace(
        parameter,
        prompt=_protect_code_block_fence(
            parameter.prompt,
            section_heading="# 既知の関連所見",
            section_end_marker="\n\n# place holder definition",
            info_string="text",
            section_body=related_findings,
        ),
    )


__all__ = ["build_oracle_review_enumerate_finding_parameter"]
