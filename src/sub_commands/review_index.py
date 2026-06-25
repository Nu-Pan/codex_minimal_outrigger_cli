from pathlib import Path

from cmoc_runtime import CmocError, head_commit, run_git


def commit_review_index_changes(review_worktree: Path) -> bool:
    """review worktree 上の INDEX.md 変更だけを commit する。"""
    changed_paths = review_worktree_status_paths(review_worktree)
    non_index = [path for path in changed_paths if Path(path).name != "INDEX.md"]
    if non_index:
        raise CmocError(
            "review oracle が INDEX.md 以外の差分を作成しました。",
            ["review worktree の差分を確認してください。"],
            "\n".join(non_index),
        )
    changed_index_paths = [
        path for path in changed_paths if Path(path).name == "INDEX.md"
    ]
    if not changed_index_paths:
        return False
    run_git(["add", "-A", "--", *changed_index_paths], review_worktree)
    staged = run_git(
        ["diff", "--cached", "--name-only"], review_worktree
    ).stdout.splitlines()
    if staged:
        run_git(["commit", "-m", "cmoc review oracle indexing"], review_worktree)
        return True
    return False


def review_worktree_status_paths(review_worktree: Path) -> list[str]:
    fields = run_git(
        ["status", "--porcelain=v1", "-z"], review_worktree
    ).stdout.split("\0")
    paths: list[str] = []
    index = 0
    while index < len(fields) and fields[index]:
        field = fields[index]
        status = field[:2]
        paths.append(field[3:])
        index += 1
        if status[0] in {"R", "C"}:
            paths.append(fields[index])
            index += 1
    return paths


def merge_review_branch(root: Path, review_branch: str) -> str:
    """review branch を session branch へ merge し、merge 後 HEAD を返す。"""
    merge = run_git(["merge", "--no-ff", review_branch], root, check=False)
    if merge.returncode != 0:
        if not resolve_review_index_conflicts(root):
            raise CmocError(
                "review branch の merge に失敗しました。",
                ["git status を確認し、手動で解決してください。"],
                merge.stderr,
            )
    return head_commit(root)


def resolve_review_index_conflicts(root: Path) -> bool:
    conflicted = run_git(
        ["diff", "--name-only", "--diff-filter=U"], root
    ).stdout.splitlines()
    if not conflicted:
        return False
    if any(Path(path).name != "INDEX.md" for path in conflicted):
        return False
    for path in conflicted:
        run_git(["checkout", "--ours", "--", path], root)
        run_git(["add", path], root)
    run_git(["commit", "--no-edit"], root)
    return True
