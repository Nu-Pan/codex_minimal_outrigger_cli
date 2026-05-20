"""`cmoc merge` の本体処理。"""

import sys
from pathlib import Path

from commons.codex import run_codex_exec
from commons.command_runner import run_command
from commons.errors import CmocError
from commons.repo import (
    assert_no_uncommitted_changes,
    ensure_cmoc_ignored,
    is_cmoc_branch,
    run_git,
)
from commons.timing import StepTimer

_MANUAL_RESOLUTION_MESSAGE: str = (
    "Manual resolution is required. cmoc did not roll back the merge state."
)


def cmoc_merge_impl(
    repo_root: Path | None = None,
    cmoc_branch: str | None = None,
) -> None:
    """cmoc ブランチを現在の HEAD へ merge する。"""
    # 直接呼び出し時は共通 runner で repo root 解決とエラー整形を行う。
    if repo_root is None:
        run_command(
            lambda resolved_repo_root: cmoc_merge_impl(
                resolved_repo_root,
                cmoc_branch,
            )
        )
        return

    # merge 全体のステップ時間を計測しながら前提条件を検証する。
    timer = StepTimer("merge")
    merge_started = False
    try:
        timer.start("validate repository state")
        print("merge (1/4) validate repository state")
        assert_no_uncommitted_changes(repo_root)
        ensure_cmoc_ignored(repo_root)

        # 明示引数が無い場合は未マージ cmoc ブランチを best effort で 1 件に絞る。
        timer.start("resolve source branch")
        print("merge (2/4) resolve source branch")
        source_branch = cmoc_branch or _resolve_source_branch(repo_root)

        # 通常 merge を試し、conflict 時だけ Codex CLI に marker 解消を依頼する。
        timer.start("run git merge")
        print("merge (3/4) run git merge")
        merge_started = True
        result = run_git(
            repo_root,
            ["merge", "--no-ff", source_branch],
            check=False,
        )
        if result.returncode != 0:
            _resolve_conflicts(repo_root)

        # merge 完了後、git が安全と判断できる場合だけ作業ブランチを削除する。
        timer.start("delete source branch if safe")
        print("merge (4/4) delete source branch if safe")
        _delete_branch_if_safe(repo_root, source_branch)
        print(f"merged branch: {source_branch}")
        timer.report()
    except Exception:
        # git merge 開始後だけ、残った merge state の手動解決を案内する。
        if merge_started:
            print(_MANUAL_RESOLUTION_MESSAGE, file=sys.stderr)
        raise


def _resolve_source_branch(repo_root: Path) -> str:
    """未マージの cmoc ブランチを best effort で 1 件に絞る。"""
    # 未マージ branch のうち cmoc 命名規則に一致するものだけを候補にする。
    result = run_git(repo_root, ["branch", "--no-merged"])
    candidates = [
        line.strip().lstrip("* ").strip()
        for line in result.stdout.splitlines()
        if is_cmoc_branch(line.strip().lstrip("* ").strip())
    ]
    if len(candidates) != 1:
        # 0 件または複数件の場合は利用者に明示指定を求める。
        raise CmocError(
            "Failed to resolve cmoc branch automatically.",
            [
                "Pass the cmoc branch name explicitly.",
                "Delete or merge extra cmoc branches, then run the command "
                "again.",
            ],
            "\n".join(candidates) or "No cmoc branch candidates.",
        )
    return candidates[0]


def _resolve_conflicts(repo_root: Path) -> None:
    """Codex CLI へ conflict marker 解消を依頼し、merge commit を作成する。"""
    # merge 直後の conflict 対象を固定し、後続確認でも同じ一覧を使う。
    unmerged = _unmerged_paths(repo_root)
    if not unmerged:
        raise CmocError(
            "git merge failed without unmerged paths.",
            [
                "Inspect git status manually.",
                "Resolve the merge state, then run cmoc again.",
            ],
        )

    # conflict 解消用 Codex 呼び出しは INDEX メンテナンス例外として実行する。
    run_codex_exec(
        repo_root,
        _conflict_prompt(repo_root, unmerged),
        read_only=False,
        expect_json=False,
        skip_index_maintenance=True,
    )

    # Codex が conflict 対象外へ marker を残した場合も、add 前に検出する。
    marker_files = _files_with_conflict_markers(repo_root)
    if marker_files:
        raise CmocError(
            "Conflict markers remain after Codex CLI resolution.",
            [
                "Resolve remaining conflict markers manually.",
                "Commit the merge manually.",
            ],
            "\n".join(marker_files),
        )

    # cmoc の責任で conflict 対象を add し、unmerged path が残らないことを確認する。
    for path in unmerged:
        run_git(repo_root, ["add", "--", path])
    if _unmerged_paths(repo_root):
        raise CmocError(
            "Unmerged paths remain after conflict resolution.",
            [
                "Inspect git status manually.",
                "Resolve and commit the merge manually.",
            ],
            "\n".join(_unmerged_paths(repo_root)),
        )

    # marker 確認と git add が完了してから merge commit を作成する。
    run_git(repo_root, ["commit", "--no-edit"])


def _delete_branch_if_safe(repo_root: Path, branch_name: str) -> None:
    """git に安全判定を任せて cmoc ブランチ削除を試みる。"""
    # `git branch -d` が拒否した場合は warning に留める。
    result = run_git(repo_root, ["branch", "-d", branch_name], check=False)
    if result.returncode != 0:
        print(f"warning: source branch was not deleted: {branch_name}")


def _files_with_conflict_markers(
    repo_root: Path,
    paths: list[str] | None = None,
) -> list[str]:
    """conflict marker が残るファイルを列挙する。"""
    # paths は後方互換のため受け取るが、仕様上は git 管理対象全体を検査する。
    del paths
    matches: list[str] = []
    result = run_git(repo_root, ["ls-files", "-z"])
    tracked_paths = {
        relative
        for relative in result.stdout.split("\0")
        if relative
    }
    for relative in sorted(tracked_paths):
        path = repo_root / relative
        if not path.exists() or not path.is_file():
            continue
        for line in path.read_text(
            encoding="utf-8",
            errors="ignore",
        ).splitlines():
            if (
                line.startswith("<<<<<<<")
                or line == "======="
                or line.startswith(">>>>>>>")
            ):
                matches.append(relative)
                break
    return matches


def _unmerged_paths(repo_root: Path) -> list[str]:
    """unmerged path を git から取得する。"""
    # git diff の unmerged filter で現在残っている conflict path を読む。
    result = run_git(repo_root, ["diff", "--name-only", "--diff-filter=U"])
    return [line for line in result.stdout.splitlines() if line]


def _conflict_prompt(repo_root: Path, unmerged: list[str]) -> str:
    """merge conflict 解消用 prompt を組み立てる。"""
    # Codex CLI には conflict 対象を git 相対パスではなく絶対パスで渡す。
    concrete_repo_root = repo_root.resolve()
    concrete_unmerged = [
        str((concrete_repo_root / relative_path).resolve())
        for relative_path in unmerged
    ]

    # workspace-write 実行なので oracles と .agents は常に編集禁止として明示する。
    return "\n".join(
        [
            "あなたは merge conflict の解消担当です。",
            f"`{concrete_repo_root}` の以下のファイルについて conflict marker を",
            f"解消してください: {concrete_unmerged}",
            "完了条件は、conflict marker を削除し、解決内容と未解決ファイルの有無を報告することです。",
            "`git add` と `git commit` は実行禁止です。",
            f"`{concrete_repo_root / 'oracles'}` は編集禁止です。",
            f"`{concrete_repo_root / '.agents'}` は編集禁止です。",
            f"`{concrete_repo_root / 'memo'}` は読み書き禁止です。",
        ]
    )
