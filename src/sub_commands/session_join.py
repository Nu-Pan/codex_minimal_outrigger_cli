"""`cmoc session join` の本体処理。"""

import sys
from pathlib import Path

from commons.codex import run_codex_exec
from commons.command_runner import run_command
from commons.errors import CmocError
from commons.repo import (
    assert_no_uncommitted_changes,
    current_branch,
    ensure_cmoc_ignored,
    is_session_branch,
    read_session_state,
    run_git,
    session_id_from_branch,
    write_session_state,
)
from commons.timing import StepTimer, start_step

_MANUAL_RESOLUTION_MESSAGE: str = (
    "手動解消が必要です。cmoc は merge 状態をロールバックしていません。"
)


def cmoc_session_join_impl(repo_root: Path | None = None) -> None:
    """現在の session branch を記録済み home branch へ merge する。"""
    # 直接呼び出し時は共通 runner で repo root 解決とエラー整形を行う。
    if repo_root is None:
        run_command(cmoc_session_join_impl)
        return

    timer = StepTimer("session join")
    merge_started = False
    try:
        start_step(timer, 1, 5, "validate session state")
        session_branch = _current_session_branch(repo_root)
        session_id = session_id_from_branch(session_branch)
        state = read_session_state(repo_root, session_id)
        home_branch = _validate_joinable_state(state, session_branch)
        assert_no_uncommitted_changes(repo_root)

        start_step(timer, 2, 5, "ensure .cmoc is ignored")
        ensure_cmoc_ignored(repo_root)

        start_step(timer, 3, 5, "switch to session home branch")
        _assert_local_branch_exists(repo_root, home_branch)
        run_git(repo_root, ["switch", home_branch])

        start_step(timer, 4, 5, "merge session branch")
        merge_started = True
        result = run_git(
            repo_root,
            ["merge", "--no-ff", session_branch],
            check=False,
        )
        if result.returncode != 0:
            _resolve_conflicts(repo_root)

        start_step(timer, 5, 5, "record joined session")
        _mark_session_joined(repo_root, session_id, state)
        _delete_branch_if_safe(repo_root, session_branch)
        print(f"joined session branch: {session_branch}")
        print(f"session home branch: {home_branch}")
        timer.report()
    except Exception:
        # git merge 開始後だけ、残った merge state の手動解決を案内する。
        if merge_started:
            print(_MANUAL_RESOLUTION_MESSAGE, file=sys.stderr)
        raise


def _current_session_branch(repo_root: Path) -> str:
    """現在 checkout している session branch 名を返す。"""
    branch_name = current_branch(repo_root)
    if not is_session_branch(branch_name):
        raise CmocError(
            "`cmoc session join` は session branch 上で実行してください。",
            [
                "`cmoc session fork` で作成した branch へ移動してから再実行してください。",
                "通常 branch 同士の merge は `git merge` を直接実行してください。",
            ],
            f"現在の branch: {branch_name or '(detached HEAD)'}",
        )
    return branch_name


def _validate_joinable_state(
    state: dict[str, object],
    session_branch: str,
) -> str:
    """session join の state 前提条件を検証し、home branch 名を返す。"""
    session = state.get("session")
    apply = state.get("apply")
    if not isinstance(session, dict) or not isinstance(apply, dict):
        raise CmocError(
            "session state ファイルの形式が不正です。",
            ["state JSON の session/apply セクションを確認してください。"],
            f"現在の branch: {session_branch}",
        )
    if session.get("state") != "active":
        raise CmocError(
            "active な session ではありません。",
            [
                "対象 session の state を確認してください。",
                "既に join または abandon 済みの場合は、追加の join は実行できません。",
            ],
            f"session.state: {session.get('state')}",
        )
    if apply.get("state") != "ready":
        raise CmocError(
            "apply run が完了または整理されていません。",
            [
                "`cmoc apply join` または `cmoc apply abandon` を完了してから再実行してください。",
                "session state の apply.state を確認してください。",
            ],
            f"apply.state: {apply.get('state')}",
        )
    home_branch = session.get("session_home_branch")
    if not isinstance(home_branch, str) or not home_branch:
        raise CmocError(
            "session home branch を特定できませんでした。",
            [
                "session state の session.session_home_branch を確認してください。",
                "state が壊れている場合は、手動で merge 先 branch を確認してください。",
            ],
            f"現在の branch: {session_branch}",
        )
    return home_branch


def _assert_local_branch_exists(repo_root: Path, branch_name: str) -> None:
    """記録済み home branch が local branch として存在することを確認する。"""
    result = run_git(
        repo_root,
        ["show-ref", "--verify", f"refs/heads/{branch_name}"],
        check=False,
    )
    if result.returncode != 0:
        raise CmocError(
            "session home branch が見つかりませんでした。",
            [
                "session state に記録された branch 名を確認してください。",
                "削除済みの場合は、手動で復元または merge 先を判断してください。",
            ],
            f"session home branch: {branch_name}",
        )


def _mark_session_joined(
    repo_root: Path,
    session_id: str,
    state: dict[str, object],
) -> None:
    """session state を joined として保存する。"""
    session = state.get("session")
    if not isinstance(session, dict):
        raise CmocError(
            "session state ファイルの形式が不正です。",
            ["state JSON の session セクションを確認してください。"],
        )
    session["state"] = "joined"
    write_session_state(repo_root, session_id, state)


def _resolve_conflicts(repo_root: Path) -> None:
    """Codex CLI へ conflict marker 解消を依頼し、merge commit を作成する。"""
    # merge 直後の conflict 対象を固定し、後続確認でも同じ一覧を使う。
    unmerged = _unmerged_paths(repo_root)
    if not unmerged:
        raise CmocError(
            "git merge が失敗しましたが、unmerged path がありません。",
            [
                "git status を手動で確認してください。",
                "merge 状態を解消してから cmoc を再実行してください。",
            ],
        )

    # conflict 解消用 Codex 呼び出しは INDEX メンテナンス例外として実行する。
    run_codex_exec(
        repo_root,
        _conflict_prompt(repo_root, unmerged),
        purpose="resolve session join conflicts",
        read_only=False,
        expect_json=False,
        skip_index_maintenance=True,
    )

    # Codex が conflict 対象外へ marker を残した場合も、add 前に検出する。
    marker_files = _files_with_conflict_markers(repo_root)
    if marker_files:
        raise CmocError(
            "Codex CLI による解消後も conflict marker が残っています。",
            [
                "残っている conflict marker を手動で解消してください。",
                "merge commit を手動で作成してください。",
            ],
            "\n".join(marker_files),
        )

    # cmoc の責任で conflict 対象を add し、unmerged path が残らないことを確認する。
    for path in unmerged:
        run_git(repo_root, ["add", "--", path])
    if _unmerged_paths(repo_root):
        raise CmocError(
            "conflict 解消後も unmerged path が残っています。",
            [
                "git status を手動で確認してください。",
                "merge を手動で解消して commit してください。",
            ],
            "\n".join(_unmerged_paths(repo_root)),
        )

    # marker 確認と git add が完了してから merge commit を作成する。
    run_git(repo_root, ["commit", "--no-edit"])


def _delete_branch_if_safe(repo_root: Path, branch_name: str) -> None:
    """git に安全判定を任せて session branch 削除を試みる。"""
    # `git branch -d` が拒否した場合は warning に留める。
    result = run_git(repo_root, ["branch", "-d", branch_name], check=False)
    if result.returncode != 0:
        print(f"warning: session branch was not deleted: {branch_name}")


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
    """session join conflict 解消用 prompt を組み立てる。"""
    # Codex CLI には conflict 対象を git 相対パスではなく絶対パスで渡す。
    concrete_repo_root = repo_root.resolve()
    concrete_unmerged = [
        str((concrete_repo_root / relative_path).resolve())
        for relative_path in unmerged
    ]
    oracle_conflicts = [
        path
        for path in unmerged
        if path == "oracles" or path.startswith("oracles/")
    ]

    lines = [
        "あなたは `cmoc session join` の merge conflict 解消担当です。",
        f"`{concrete_repo_root}` の以下の conflict 対象ファイルだけを編集してください:",
        str(concrete_unmerged),
        "完了条件は、conflict marker を削除し、解決内容と未解決ファイルの有無を報告することです。",
        "`git add` と `git commit` は実行禁止です。",
        "conflict 対象外のファイルは編集禁止です。",
        f"`{concrete_repo_root / '.agents'}` は編集禁止です。",
        f"`{concrete_repo_root / 'memo'}` は読み書き禁止です。",
    ]
    if oracle_conflicts:
        concrete_oracle_conflicts = [
            str((concrete_repo_root / relative_path).resolve())
            for relative_path in oracle_conflicts
        ]
        lines.extend(
            [
                "以下の oracle file は conflict marker 解消に限って編集できます:",
                str(concrete_oracle_conflicts),
                "oracle file の意味的な仕様改訂、conflict 対象外 oracle file の編集は禁止です。",
            ]
        )
    else:
        lines.append(f"`{concrete_repo_root / 'oracles'}` は編集禁止です。")
    return "\n".join(lines)
