from pathlib import Path

from cmoc_runtime import (
    SessionState,
    run_git,
)
from commons.runtime_git import enumerate_oracle_and_realization_files


def enumerate_oracle_review_targets(
    root: Path, scope: str, state: SessionState, review_fork_commit: str
) -> list[Path]:
    """oracle review の scope に応じた oracle file 対象を列挙する。"""
    all_oracle_files = enumerate_review_all_oracle_files(root)
    if scope == "full":
        return all_oracle_files
    start = state.session.session_fork_commit
    if not start:
        return []
    # {{work-root}}/oracle/doc/app_spec/sub_command/oracle_review.md
    # session scope は review fork 時点の oracle snapshot を対象に固定する。
    # 通常の name-only 出力は改行を quote するため、NUL 区切りで path を保つ。
    changed = {
        path
        for path in run_git(
            ["diff", "--name-only", "-z", start, review_fork_commit, "--", "oracle"],
            root,
        ).stdout.split("\0")
        if path
    }
    return [path for path in all_oracle_files if str(path.relative_to(root)) in changed]


def enumerate_review_all_oracle_files(root: Path) -> list[Path]:
    """review 対象候補となる oracle file 全件を列挙する。"""
    # {{work-root}}/oracle/doc/app_spec/misc_spec.md
    # full scope と state 同期で同じ full-tree 分類結果を使用する。
    oracle_files, _ = enumerate_oracle_and_realization_files(root)
    return oracle_files
