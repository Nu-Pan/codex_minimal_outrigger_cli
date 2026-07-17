from pathlib import Path

from cmoc_runtime import CmocError, head_commit, run_git
from commons.runtime_git import status_path_statuses


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


# {{work-root}}/oracle/doc/app_spec/sub_command/review_oracle.md は、
# {{work-root}}/oracle/doc/app_spec/indexing.md の preflight が作った INDEX commit
# も含め、隔離終了時に review branch を merge することを求めている。
def review_branch_has_index_changes(review_worktree: Path, base_commit: str) -> bool:
    """base commit 以降の review branch 差分が INDEX.md だけか確認する。"""
    changed_paths = run_git(
        ["diff", "--name-only", f"{base_commit}..HEAD"], review_worktree
    ).stdout.splitlines()
    non_index = [path for path in changed_paths if Path(path).name != "INDEX.md"]
    if non_index:
        raise CmocError(
            "review branch に INDEX.md 以外の commit 済み差分があります。",
            ["review branch の差分を確認してください。"],
            "\n".join(non_index),
        )
    return bool(changed_paths)


def review_worktree_status_paths(review_worktree: Path) -> list[str]:
    """review worktreeのtracked、staged、untracked変更pathを列挙する。"""
    return [
        str(path.relative_to(review_worktree))
        for _status, path in status_path_statuses(
            review_worktree, include_rename_sources=True
        )
    ]


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
    """INDEX.mdだけのmerge conflictをoursまたは削除で解決してcommitする。"""
    conflicted = run_git(
        ["diff", "--name-only", "--diff-filter=U"], root
    ).stdout.splitlines()
    if not conflicted:
        return False
    if any(Path(path).name != "INDEX.md" for path in conflicted):
        return False
    for path in conflicted:
        if _has_ours_stage(root, path):
            run_git(["checkout", "--ours", "--", path], root)
            run_git(["add", "--", path], root)
        else:
            run_git(["rm", "-f", "--", path], root)
    run_git(["commit", "--no-edit"], root)
    return True


def _has_ours_stage(root: Path, path: str) -> bool:
    """unmerged pathにours stageが存在するかを返す。"""
    unmerged = run_git(["ls-files", "-u", "--", path], root).stdout.splitlines()
    return any(line.split(maxsplit=3)[2] == "2" for line in unmerged)
