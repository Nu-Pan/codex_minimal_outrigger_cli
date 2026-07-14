"""review finding enumeration の互換 import 経路。

`acp.builder.review.oracle.enumerate_finding` から import する呼び出し元が
残る間だけ維持する。canonical 実装は
`<work-root>/oracle/src/oracle/acp_builder/review/oracle/enumerate_finding.py`。
全呼び出し元が canonical oracle path を直接使うようになったら削除できる。
"""

import os
from dataclasses import replace
from pathlib import Path

from basic.acp import AgentCallParameter
from oracle.acp_builder.review.oracle.enumerate_finding import (
    build_review_oracle_enumerate_finding_parameter as _build_enumerate_parameter,
)


def build_review_oracle_enumerate_finding_parameter(
    oracle_path: Path,
    related_findings: str,
) -> AgentCallParameter:
    parameter = _build_enumerate_parameter(oracle_path, related_findings)
    if not oracle_path.is_absolute() or not oracle_path.is_symlink():
        return parameter
    # <work-root>/oracle/src/oracle/acp_builder/review/oracle/enumerate_finding.py
    # canonical builder は絶対 path を resolve するため、symlink entry をレビュー
    # した事実が prompt から失われないよう、動的な定義行だけ lexical path に戻す。
    resolved = str(oracle_path.resolve())
    lexical = os.path.abspath(oracle_path)
    marker = f"- <oracle-path> = {resolved}"
    return replace(
        parameter,
        prompt=parameter.prompt.replace(marker, f"- <oracle-path> = {lexical}"),
    )


__all__ = ["build_review_oracle_enumerate_finding_parameter"]
