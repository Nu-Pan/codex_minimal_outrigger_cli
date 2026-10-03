"""session join 固有の編集境界を加える conflict resolution builder。

共通 parameter は oracle builder から取得し、この join 用の追加指示だけを付加する。
"""

from dataclasses import replace as _replace
from pathlib import Path as _Path

from oracle.acp_builder.basic import (
    AgentCallParameter as _AgentCallParameter,
)
from oracle.acp_builder.session.join.conflict_resolution import (
    build_session_join_conflict_resolution_parameter as _build_canonical_parameter,
)
from oracle.other.struct_doc import SDHeader as _SDHeader
from oracle.other.struct_doc import (
    render_sd_node_as_markdown as _render_sd_node_as_markdown,
)


def build_session_join_conflict_resolution_parameter(
    session_head_commit: str,
    home_head_commit: str,
    home_worktree: _Path,
) -> _AgentCallParameter:
    """oracle が構築した共通 prompt に session join 固有の境界を加える。"""
    parameter = _build_canonical_parameter(
        session_head_commit,
        home_head_commit,
        home_worktree,
    )
    session_scope = _render_sd_node_as_markdown(
        _SDHeader(
            "session join 固有の編集範囲",
            """
            - この call では進行中の merge の内容競合を解消するために必要な編集と検証だけを行うこと
            - conflict marker の解消に不要な仕様変更、実装改善、または別 file の変更を行ってはならない
            """,
        )
    )
    return _replace(parameter, prompt=f"{parameter.prompt}\n\n{session_scope}")


__all__ = ["build_session_join_conflict_resolution_parameter"]
