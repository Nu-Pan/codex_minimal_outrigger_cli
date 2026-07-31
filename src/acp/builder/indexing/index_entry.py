"""`{{work-root}}/oracle/src/oracle/acp_builder/indexing/index_entry.py` を再公開する。

既存の `acp.builder.indexing.index_entry` 参照を維持するために残す互換入口。
削除条件は realization 側と利用者向け公開面から同参照がなくなること。
"""

from dataclasses import replace as _replace
from pathlib import Path as _Path

from oracle.acp_builder.indexing.index_entry import (
    build_indexing_index_entry_parameter as _build_indexing_index_entry_parameter,
)

from basic.acp import AgentCallParameter as _AgentCallParameter

from ..common.prompt_fence import (
    _protect_code_block_fence,
)

__all__ = ["build_indexing_index_entry_parameter"]


def build_indexing_index_entry_parameter(
    target_path: _Path,
    target_content: str,
) -> _AgentCallParameter:
    """正本 builder の parameter を再公開し、対象本文の fence を保護する。"""
    parameter = _build_indexing_index_entry_parameter(target_path, target_content)
    return _replace(
        parameter,
        prompt=_protect_code_block_fence(
            parameter.prompt,
            section_heading="# `{{target-path}}` の内容",
            section_end_marker="\n\n# place holder definition",
            info_string=None,
            section_body=target_content,
        ),
    )
