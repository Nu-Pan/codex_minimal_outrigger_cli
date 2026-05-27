"""`cmoc apply abandon` の本体処理。"""

import os
from pathlib import Path

from commons.command_runner import run_command
from commons.errors import CmocError
from commons.repo import (
    apply_worktree_path_from_branch,
    assert_no_uncommitted_changes,
    current_branch,
    is_apply_branch,
    is_session_branch,
    read_session_state,
    run_git,
    session_id_from_branch,
    session_state_repo_root,
    write_session_state,
)
from commons.timing import StepTimer, start_step


def cmoc_apply_abandon_impl(repo_root: Path | None = None) -> None:
    """現在の session に紐づく未 join apply run を破棄する。"""
    # 直接呼び出し時は共通 runner で repo root 解決とエラー整形を行う。
    if repo_root is None:
        run_command(cmoc_apply_abandon_impl)
        return

    timer = StepTimer("apply abandon")
    start_step(timer, 1, 3, "validate apply state")
    branch_name = current_branch(repo_root)
    session_id = session_id_from_branch(branch_name)
    cmoc_root = session_state_repo_root(repo_root, session_id)
    os.chdir(cmoc_root)
    state = read_session_state(cmoc_root, session_id)
    abandon_state = _validate_abandonable_state(
        cmoc_root,
        state,
        branch_name,
        session_id,
    )
    assert_no_uncommitted_changes(cmoc_root)

    start_step(timer, 2, 3, "cleanup apply artifacts")
    warnings = _cleanup_apply_artifacts(cmoc_root, abandon_state)

    start_step(timer, 3, 3, "record ready apply state")
    _mark_apply_ready(cmoc_root, session_id, state)

    print(f"abandoned apply branch: {abandon_state.apply_branch}")
    print(f"abandoned apply worktree: {abandon_state.apply_worktree}")
    print(f"previous apply.state: {abandon_state.previous_apply_state}")
    print("current apply.state: ready")
    for warning in warnings:
        print(f"warning: {warning}")
    timer.report()


class _AbandonState:
    """apply abandon に必要な state 値。"""

    def __init__(
        self,
        *,
        apply_branch: str,
        apply_worktree: Path,
        previous_apply_state: str,
    ) -> None:
        self.apply_branch = apply_branch
        self.apply_worktree = apply_worktree
        self.previous_apply_state = previous_apply_state


def _validate_abandonable_state(
    repo_root: Path,
    state: dict[str, object],
    current_branch_name: str,
    session_id: str,
) -> _AbandonState:
    """apply abandon の state 前提条件を検証する。"""
    session = state.get("session")
    apply = state.get("apply")
    if not isinstance(session, dict) or not isinstance(apply, dict):
        raise CmocError(
            "session state ファイルの形式が不正です。",
            ["state JSON の session/apply セクションを確認してください。"],
            f"現在の branch: {current_branch_name}",
        )
    session_branch = f"cmoc/session/{session_id}"
    if session.get("state") != "active":
        raise CmocError(
            "active な session ではありません。",
            [
                "対象 session の state を確認してください。",
                "既に join または abandon 済みの場合は、新しい session を開始してください。",
            ],
            f"session.state: {session.get('state')}",
        )
    apply_state = apply.get("state")
    if apply_state == "ready":
        raise CmocError(
            "破棄対象の apply run がありません。",
            [
                "`cmoc apply fork` で apply run を開始してから実行してください。",
                "session state の apply.state を確認してください。",
            ],
            f"apply.state: {apply_state}",
        )
    if not isinstance(apply_state, str) or not apply_state:
        raise CmocError(
            "apply state を session state から特定できませんでした。",
            ["session state の apply.state を確認してください。"],
            f"apply.state: {apply_state}",
        )
    if apply_state == "running":
        raise CmocError(
            "running 状態の apply run を安全に破棄できません。",
            [
                "現在の実装では実行中 apply プロセスの停止と終了確認に必要な情報を保持していません。",
                "apply プロセスの終了を確認して state を completed または error に復旧してから再実行してください。",
            ],
            f"apply.state: {apply_state}",
        )
    if apply_state not in {"completed", "error"}:
        raise CmocError(
            "session state ファイルの apply.state が不正です。",
            [
                "apply.state は ready/running/completed/error のいずれかである必要があります。",
                "破損した session state を復旧してから再実行してください。",
            ],
            f"apply.state: {apply_state}",
        )
    apply_branch = apply.get("apply_branch")
    if not isinstance(apply_branch, str) or not is_apply_branch(apply_branch):
        raise CmocError(
            "apply branch を session state から特定できませんでした。",
            [
                "session state の apply.apply_branch を確認してください。",
                "state が壊れている場合は、手動で apply branch を確認してください。",
            ],
            f"apply.apply_branch: {apply_branch}",
        )
    apply_worktree = apply_worktree_path_from_branch(repo_root, apply_branch)
    if current_branch_name not in {session_branch, apply_branch}:
        raise CmocError(
            "`cmoc apply abandon` は session branch または apply branch 上で実行してください。",
            [
                "対象 session の session branch か、対応する apply branch へ移動してください。",
                "通常 branch の削除は `git branch -D` を直接実行してください。",
            ],
            f"現在の branch: {current_branch_name or '(detached HEAD)'}",
        )
    if not is_session_branch(session_branch):
        raise CmocError(
            "session branch 名が不正です。",
            [
                "session state ファイル名と branch 名を確認してください。",
                "正しい session branch 上で `cmoc apply abandon` を再実行してください。",
            ],
            f"session branch: {session_branch}",
        )
    return _AbandonState(
        apply_branch=apply_branch,
        apply_worktree=apply_worktree,
        previous_apply_state=apply_state,
    )


def _cleanup_apply_artifacts(
    repo_root: Path,
    abandon_state: _AbandonState,
) -> list[str]:
    """apply worktree と apply branch を強制削除する。"""
    warnings: list[str] = []
    if abandon_state.apply_worktree.exists():
        worktree_result = run_git(
            repo_root,
            ["worktree", "remove", "--force", str(abandon_state.apply_worktree)],
            check=False,
        )
        if worktree_result.returncode != 0:
            warnings.append(
                "apply worktree was not deleted: "
                f"{abandon_state.apply_worktree}"
            )
            detail = worktree_result.stderr.strip()
            if detail:
                warnings.append(detail)
    else:
        warnings.append(
            f"apply worktree was already missing: {abandon_state.apply_worktree}"
        )

    branch_exists = run_git(
        repo_root,
        ["show-ref", "--verify", f"refs/heads/{abandon_state.apply_branch}"],
        check=False,
    )
    if branch_exists.returncode == 0:
        branch_result = run_git(
            repo_root,
            ["branch", "-D", abandon_state.apply_branch],
            check=False,
        )
        if branch_result.returncode != 0:
            warnings.append(
                f"apply branch was not deleted: {abandon_state.apply_branch}"
            )
            detail = branch_result.stderr.strip()
            if detail:
                warnings.append(detail)
    else:
        warnings.append(
            f"apply branch was already missing: {abandon_state.apply_branch}"
        )
    return warnings


def _mark_apply_ready(
    repo_root: Path,
    session_id: str,
    state: dict[str, object],
) -> None:
    """apply セクションを ready に戻し、固定 field を null 初期化する。"""
    apply = state.get("apply")
    if not isinstance(apply, dict):
        raise CmocError(
            "session state ファイルの形式が不正です。",
            ["state JSON の apply セクションを確認してください。"],
        )
    state["apply"] = {
        "state": "ready",
        "apply_branch": None,
        "oracle_snapshot_commit": None,
    }
    write_session_state(repo_root, session_id, state)
