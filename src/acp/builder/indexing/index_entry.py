"""`{{work-root}}/oracle/src/oracle/acp_builder/indexing/index_entry.py` を再公開する。

既存の `acp.builder.indexing.index_entry` 参照を維持するために残す互換入口。
削除条件は realization 側と利用者向け公開面から同参照がなくなること。

prompt の受け渡し根拠: `{{work-root}}/oracle/doc/app_spec/prompt_standard.md`
"""

from pathlib import Path as _Path

from oracle.acp_builder.indexing.index_entry import (
    build_indexing_index_entry_parameter as _build_indexing_index_entry_parameter,
)

from basic.acp import AgentCallParameter as _AgentCallParameter

__all__ = ["build_indexing_index_entry_parameter"]


def build_indexing_index_entry_parameter(
    target_path: _Path,
    target_content: str,
    agent_call_cwd: _Path,
) -> _AgentCallParameter:
    """正本 builder の parameter をそのまま再公開する。"""
    return _build_indexing_index_entry_parameter(
        target_path, target_content, agent_call_cwd
    )
