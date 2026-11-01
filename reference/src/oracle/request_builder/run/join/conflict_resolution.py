"""run join の統合対象を共通の競合解消 request builder へ渡す。"""

from pathlib import Path

from oracle.request_builder.basic import AgentCallParameter
from oracle.request_builder.common.conflict_resolution import (
    build_merge_conflict_resolution_request,
)


def build_run_join_conflict_resolution_request(
    run_head_commit: str,
    session_head_commit: str,
    run_worktree: Path,
    *,
    feedback_report_cut_path: Path | None = None,
) -> AgentCallParameter:
    """run 上で session の変更を統合し、必要なら封印済み結果を検証する。

    Args:
        run_head_commit: 差分検査と必要な取消の後、session 統合直前の run HEAD。
        session_head_commit: 今回の準備で基準とする session HEAD。
        run_worktree: session を統合する merge が進行中の run worktree。
        feedback_report_cut_path: 自然完了した feedback の封印済み report cut。
    """
    # 準備中の merge は session → run。自動・明示 join で同じ入力対応を使う。
    return build_merge_conflict_resolution_request(
        source_commit=session_head_commit,
        target_commit=run_head_commit,
        merge_worktree=run_worktree,
        feedback_report_cut_path=feedback_report_cut_path,
    )
