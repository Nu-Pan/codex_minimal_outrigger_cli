"""`cmoc merge` の本体処理。"""

from pathlib import Path

from commons.codex import run_codex_exec
from commons.errors import CmocError
from commons.repo import (
    assert_no_uncommitted_changes,
    ensure_cmoc_ignored,
    is_cmoc_branch,
    run_git,
)


def cmoc_merge_impl(repo_root: Path, cmoc_branch: str | None) -> None:
    """cmoc ブランチを現在の HEAD へ merge する。"""
    print("merge (1/4) validate repository state")
    assert_no_uncommitted_changes(repo_root)
    ensure_cmoc_ignored(repo_root)

    print("merge (2/4) resolve source branch")
    source_branch = cmoc_branch or _resolve_source_branch(repo_root)

    print("merge (3/4) run git merge")
    result = run_git(repo_root, ["merge", "--no-ff", source_branch], check=False)
    if result.returncode != 0:
        _resolve_conflicts(repo_root)

    print("merge (4/4) delete source branch if safe")
    _delete_branch_if_safe(repo_root, source_branch)
    print(f"merged branch: {source_branch}")


def _resolve_source_branch(repo_root: Path) -> str:
    """未マージの cmoc ブランチを best effort で 1 件に絞る。"""
    result = run_git(repo_root, ["branch", "--no-merged"])
    candidates = [
        line.strip().lstrip("* ").strip()
        for line in result.stdout.splitlines()
        if is_cmoc_branch(line.strip().lstrip("* ").strip())
    ]
    if len(candidates) != 1:
        raise CmocError(
            "Failed to resolve cmoc branch automatically.",
            [
                "Pass the cmoc branch name explicitly.",
                "Delete or merge extra cmoc branches, then run the command again.",
            ],
            "\n".join(candidates) or "No cmoc branch candidates.",
        )
    return candidates[0]


def _resolve_conflicts(repo_root: Path) -> None:
    """Codex CLI へ conflict marker 解消を依頼し、merge commit を作成する。"""
    unmerged = _unmerged_paths(repo_root)
    if not unmerged:
        raise CmocError(
            "git merge failed without unmerged paths.",
            ["Inspect git status manually.", "Resolve the merge state, then run cmoc again."],
        )

    run_codex_exec(
        repo_root,
        _conflict_prompt(repo_root, unmerged),
        read_only=False,
        expect_json=False,
    )
    if _files_with_conflict_markers(repo_root):
        raise CmocError(
            "Conflict markers remain after Codex CLI resolution.",
            ["Resolve remaining conflict markers manually.", "Commit the merge manually."],
            "\n".join(_files_with_conflict_markers(repo_root)),
        )
    for path in unmerged:
        run_git(repo_root, ["add", "--", path])
    if _unmerged_paths(repo_root):
        raise CmocError(
            "Unmerged paths remain after conflict resolution.",
            ["Inspect git status manually.", "Resolve and commit the merge manually."],
            "\n".join(_unmerged_paths(repo_root)),
        )
    run_git(repo_root, ["commit", "--no-edit"])


def _delete_branch_if_safe(repo_root: Path, branch_name: str) -> None:
    """git に安全判定を任せて cmoc ブランチ削除を試みる。"""
    result = run_git(repo_root, ["branch", "-d", branch_name], check=False)
    if result.returncode != 0:
        print(f"warning: source branch was not deleted: {branch_name}")


def _unmerged_paths(repo_root: Path) -> list[str]:
    """unmerged path を git から取得する。"""
    result = run_git(repo_root, ["diff", "--name-only", "--diff-filter=U"])
    return [line for line in result.stdout.splitlines() if line]


def _files_with_conflict_markers(repo_root: Path) -> list[str]:
    """conflict marker が残るファイルを列挙する。"""
    matches: list[str] = []
    for relative in _unmerged_paths(repo_root):
        path = repo_root / relative
        if not path.exists() or not path.is_file():
            continue
        content = path.read_text(encoding="utf-8", errors="ignore")
        if "<<<<<<<" in content or "=======" in content or ">>>>>>>" in content:
            matches.append(relative)
    return matches


def _conflict_prompt(repo_root: Path, unmerged: list[str]) -> str:
    """merge conflict 解消用 prompt を組み立てる。"""
    return "\n".join(
        [
            "You are a merge conflict resolver.",
            f"Resolve conflict markers in repository `{repo_root}` for these files: {unmerged}.",
            "The task is complete when conflict markers are removed and unresolved files are reported.",
            "Do not run git add or git commit.",
            f"Do not edit `{repo_root / 'oracles'}` unless a conflict already exists there.",
            f"Do not edit `{repo_root / '.agents'}`.",
        ]
    )
