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

from basic.acp import AgentCallParameter as _AgentCallParameter


def build_oracle_review_enumerate_finding_parameter(
    oracle_path: _Path,
    related_findings: str,
) -> _AgentCallParameter:
    """canonical builderのparameterを作り、symlinkのlexical pathを保持する。"""
    parameter = _build_enumerate_parameter(oracle_path, related_findings)
    if not oracle_path.is_absolute() or not oracle_path.is_symlink():
        return parameter
    # {{work-root}}/oracle/src/oracle/acp_builder/oracle/review/enumerate_finding.py
    # canonical builder は絶対 path を resolve するため、symlink entry をレビュー
    # した事実が prompt から失われないよう、動的な定義行だけ lexical path に戻す。
    resolved = str(oracle_path.resolve())
    lexical = _os.path.abspath(oracle_path)
    marker = f"- {{{{oracle-path}}}} = {resolved}"
    prefix, separator, suffix = parameter.prompt.rpartition(marker)
    if not separator:
        return parameter
    return _replace(
        parameter,
        prompt=prefix + f"- {{{{oracle-path}}}} = {lexical}" + suffix,
    )


__all__ = ["build_oracle_review_enumerate_finding_parameter"]
