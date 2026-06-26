from pathlib import Path

from cmoc_runtime import SessionState, is_binary, is_git_ignored, run_git


def enumerate_review_oracle_targets(
    root: Path, scope: str, state: SessionState
) -> list[Path]:
    """review oracle の scope に応じた oracle file 対象を列挙する。"""
    all_oracle_files = enumerate_review_all_oracle_files(root)
    if scope == "full":
        return all_oracle_files
    start = state.session.session_start_commit
    if not start:
        return []
    changed = set(
        run_git(
            ["diff", "--name-only", start, "HEAD", "--", "oracle"], root
        ).stdout.splitlines()
    )
    return [
        path for path in all_oracle_files if str(path.relative_to(root)) in changed
    ]


def enumerate_review_all_oracle_files(root: Path) -> list[Path]:
    """review 対象候補となる oracle file 全件を列挙する。"""
    return [
        path
        for path in sorted((root / "oracle").rglob("*"))
        if path.is_file()
        and path.name != "INDEX.md"
        and not is_git_ignored(root, path)
        and not is_binary(path)
    ]
