"""oracle review finding enumeration の realization adapter。

`acp.builder.oracle.review.enumerate_finding` から import する呼び出し元が
残る間だけ維持する。canonical 実装は
`{{work-root}}/oracle/src/oracle/acp_builder/oracle/review/enumerate_finding.py`。
全呼び出し元が canonical oracle path を直接使うようになったら削除できる。
"""

import os as _os
from dataclasses import replace as _replace
from pathlib import Path as _Path

from oracle.acp_builder.oracle.review.enumerate_finding import (
    build_oracle_review_enumerate_finding_parameter as _build_enumerate_parameter,
)

from acp.builder.common.prompt_fence import _protect_code_block_fence
from basic.acp import AgentCallParameter as _AgentCallParameter


def build_oracle_review_enumerate_finding_parameter(
    oracle_path: _Path,
    related_findings: str,
) -> _AgentCallParameter:
    """canonical builder の parameter を再公開し、動的所見の fence を保護する。"""
    parameter = _build_enumerate_parameter(oracle_path, related_findings)
    prompt = parameter.prompt
    if oracle_path.is_absolute() and oracle_path.is_symlink():
        # oracle file の所属は repository path で決まり、link 先ではない。
        # canonical builder の resolve は link 先を埋め込むため、対象 entry を
        # 指す lexical path に戻す。
        # 根拠: {{work-root}}/oracle/src/oracle/prompt_builder/parts/oracle_and_realization_basic.py
        resolved = str(oracle_path.resolve())
        lexical = _os.path.abspath(oracle_path)
        marker = f"- {{{{oracle-path}}}} = {resolved}"
        prefix, separator, suffix = prompt.rpartition(marker)
        if separator:
            prompt = prefix + f"- {{{{oracle-path}}}} = {lexical}" + suffix
    return _replace(
        parameter,
        prompt=_protect_code_block_fence(
            prompt,
            section_heading="# 既知の関連所見",
            section_end_marker="\n\n# place holder definition",
            info_string="text",
        ),
    )


__all__ = ["build_oracle_review_enumerate_finding_parameter"]
