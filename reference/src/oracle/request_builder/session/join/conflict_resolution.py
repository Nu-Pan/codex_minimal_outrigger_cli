"""session join の統合対象を共通の競合解消 request builder へ渡す。"""

from pathlib import Path

from oracle.request_builder.basic import AgentCallParameter
from oracle.request_builder.common.conflict_resolution import (
    build_merge_conflict_resolution_request,
)


def build_session_join_conflict_resolution_request(
    session_head_commit: str,
    home_head_commit: str,
    session_worktree: Path,
) -> AgentCallParameter:
    """session branch 上で home の変更を統合する call を構築する。

    Args:
        session_head_commit: merge 前に確定した session branch の HEAD。
        home_head_commit: merge 前に確定した home branch の HEAD。
        session_worktree: home の変更を統合中の session worktree。
    """
    # session 固有の branch 対応だけを持ち、指示文と起動条件は共通化する。
    return build_merge_conflict_resolution_request(
        source_commit=home_head_commit,
        target_commit=session_head_commit,
        merge_worktree=session_worktree,
    )
