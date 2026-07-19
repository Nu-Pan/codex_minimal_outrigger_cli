from pathlib import Path

from cmoc_runtime import (
    SessionState,
    is_oracle_file_path,
    run_git,
)


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
    changed = set(
        run_git(
            ["diff", "--name-only", start, review_fork_commit, "--", "oracle"], root
        ).stdout.splitlines()
    )
    return [path for path in all_oracle_files if str(path.relative_to(root)) in changed]


def enumerate_review_all_oracle_files(root: Path) -> list[Path]:
    """review 対象候補となる oracle file 全件を列挙する。"""
    return [
        path
        for path in sorted((root / "oracle").rglob("*"))
        if path.is_file() and is_oracle_file_path(root, path)
    ]
