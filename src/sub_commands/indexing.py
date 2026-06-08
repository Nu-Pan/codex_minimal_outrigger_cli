"""`cmoc indexing` の本体処理。"""

from pathlib import Path

from commons.command_runner import run_command
from commons.indexing import maintain_indexes
from commons.repo import assert_no_uncommitted_changes
from commons.timing import StepTimer, start_step


def cmoc_indexing_impl(
    repo_root: Path | None = None,
) -> None:
    """INDEX.md メンテナンスを明示実行し、発生差分を commit する。"""
    if repo_root is None:
        run_command(
            lambda resolved_repo_root: cmoc_indexing_impl(resolved_repo_root),
            command_path="cmoc indexing",
        )
        return

    timer = StepTimer("indexing")
    start_step(timer, 1, 2, "repository 状態検証")
    assert_no_uncommitted_changes(repo_root)

    start_step(timer, 2, 2, "INDEX.md メンテナンス")
    changed = maintain_indexes(repo_root)
    if changed:
        print("committed INDEX.md maintenance changes")
    else:
        print("no INDEX.md maintenance changes")
