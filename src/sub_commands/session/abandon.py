"""`cmoc session abandon` の本体処理。"""

from copy import deepcopy
from dataclasses import dataclass
from pathlib import Path

from commons.command_runner import run_command
from commons.errors import CmocError
from commons.repo import (
    assert_no_uncommitted_changes,
    assert_no_uncommitted_changes_outside_cmoc,
    current_branch,
    ensure_cmoc_ignored_and_committed,
    is_session_branch,
    read_session_state,
    resolve_session_home_branch,
    run_git,
    session_id_from_branch,
    session_state_root,
    write_session_state,
)
from commons.timing import StepTimer, start_step


@dataclass(frozen=True)
class _AbandonRollbackSnapshot:
    """cleanup 開始前に復元すべき git 状態。"""

    session_branch: str
    session_head: str
    home_branch: str
    home_head: str
    session_state: dict[str, object]


def cmoc_session_abandon_impl(repo_root: Path | None = None) -> None:
    """現在の session branch を merge せず破棄する。"""
    # 直接呼び出し時は共通 runner で repo root 解決とエラー整形を行う。
    if repo_root is None:
        run_command(
            cmoc_session_abandon_impl,
            command_path="cmoc session abandon",
        )
        return

    timer = StepTimer("session abandon")
    start_step(timer, 1, 4, "session 状態検証")
    session_branch = _current_session_branch(repo_root)
    session_id = session_id_from_branch(session_branch)
    state_root = session_state_root(repo_root)
    state = read_session_state(state_root, session_id)
    _validate_abandonable_state(state, session_branch)
    home_branch = resolve_session_home_branch(
        repo_root,
        state,
        session_branch,
    )
    _assert_local_branch_exists(repo_root, home_branch)
    assert_no_uncommitted_changes_outside_cmoc(repo_root)
    rollback_snapshot = _capture_rollback_snapshot(
        repo_root,
        session_branch,
        home_branch,
        state,
    )

    try:
        start_step(timer, 2, 4, ".cmoc ignore 確認")
        ensure_cmoc_ignored_and_committed(repo_root)
        assert_no_uncommitted_changes(repo_root)
        _record_session_home_branch(state_root, session_id, state, home_branch)

        start_step(timer, 3, 4, "session home branch 切替")
        run_git(repo_root, ["switch", home_branch])
        ensure_cmoc_ignored_and_committed(repo_root)
        assert_no_uncommitted_changes(repo_root)
        start_step(timer, 4, 4, "session abandon 記録・session branch 削除")
        _mark_session_abandoned(state_root, session_id, state)
        run_git(repo_root, ["branch", "-D", session_branch])
    except Exception as error:
        restore_errors = _restore_abandon_state(
            repo_root,
            state_root,
            session_id,
            state,
            rollback_snapshot,
        )
        detail = _cleanup_failure_detail(error, restore_errors)
        message = "session abandon のクリーンアップに失敗しました。"
        actions = [
            "Detail を確認して問題を手動で解消してから `cmoc session abandon` を再実行してください。",
            "session branch と session state が active に戻っていることを確認してください。",
        ]
        raise CmocError(
            message,
            actions,
            detail,
        ) from error

    print(f"abandoned session branch: {session_branch}")
    print(f"session home branch: {home_branch}")
    timer.report()


def _current_session_branch(repo_root: Path) -> str:
    """現在 checkout している session branch 名を返す。"""
    branch_name = current_branch(repo_root)
    if not is_session_branch(branch_name):
        raise CmocError(
            "`cmoc session abandon` は session branch 上で実行してください。",
            [
                "`cmoc session fork` で作成した branch へ移動してから"
                "再実行してください。",
                "通常 branch を削除する場合は `git branch -D` を直接実行してください。",
            ],
            f"現在の branch: {branch_name or '(detached HEAD)'}",
        )
    return branch_name


def _validate_abandonable_state(
    state: dict[str, object],
    session_branch: str,
) -> None:
    """session abandon の state 前提条件を検証する。"""
    session = state.get("session")
    apply = state.get("apply")
    if not isinstance(session, dict) or not isinstance(apply, dict):
        raise CmocError(
            "session state ファイルの形式が不正です。",
            [
                "state JSON の session/apply セクションを確認して復旧してください。",
                "復旧できない場合は、現在の session を使わず新しい session を開始してください。",
            ],
            f"現在の branch: {session_branch}",
        )
    if session.get("state") != "active":
        raise CmocError(
            "active な session ではありません。",
            [
                "対象 session の state を確認してください。",
                "既に join または abandon 済みの場合は、追加の abandon は実行できません。",
            ],
            f"session.state: {session.get('state')}",
        )
    if apply.get("state") != "ready":
        raise CmocError(
            "apply run が完了または整理されていません。",
            [
                "残っている apply run を `cmoc apply abandon` で破棄してから"
                "再実行してください。",
                "session state の apply.state を確認してください。",
            ],
            f"apply.state: {apply.get('state')}",
        )


def _record_session_home_branch(
    repo_root: Path,
    session_id: str,
    state: dict[str, object],
    home_branch: str,
) -> None:
    """復元済み session home branch を state に保存する。"""
    session = state.get("session")
    if not isinstance(session, dict):
        raise CmocError(
            "session state ファイルの形式が不正です。",
            [
                "state JSON の session セクションを確認して復旧してください。",
                "復旧できない場合は、現在の session を使わず新しい session を開始してください。",
            ],
        )
    if session.get("session_home_branch") == home_branch:
        return
    session["session_home_branch"] = home_branch
    write_session_state(repo_root, session_id, state)


def _capture_rollback_snapshot(
    repo_root: Path,
    session_branch: str,
    home_branch: str,
    state: dict[str, object],
) -> _AbandonRollbackSnapshot:
    """cleanup 開始前の branch HEAD を保存する。"""
    return _AbandonRollbackSnapshot(
        session_branch=session_branch,
        session_head=_branch_head(repo_root, session_branch),
        home_branch=home_branch,
        home_head=_branch_head(repo_root, home_branch),
        session_state=deepcopy(state),
    )


def _branch_head(repo_root: Path, branch_name: str) -> str:
    """local branch の HEAD commit を返す。"""
    result = run_git(repo_root, ["rev-parse", "--verify", branch_name])
    return result.stdout.strip()


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
                "削除済みの場合は、手動で復元または戻り先を判断してください。",
            ],
            f"session home branch: {branch_name}",
        )


def _mark_session_abandoned(
    repo_root: Path,
    session_id: str,
    state: dict[str, object],
) -> None:
    """session state を abandoned として保存する。"""
    session = state.get("session")
    if not isinstance(session, dict):
        raise CmocError(
            "session state ファイルの形式が不正です。",
            [
                "state JSON の session セクションを確認して復旧してください。",
                "復旧できない場合は、現在の session を使わず新しい session を開始してください。",
            ],
        )
    session["state"] = "abandoned"
    write_session_state(repo_root, session_id, state)


def _restore_abandon_state(
    repo_root: Path,
    state_root: Path,
    session_id: str,
    state: dict[str, object],
    rollback_snapshot: _AbandonRollbackSnapshot,
) -> list[str]:
    """cleanup 失敗時に再実行しやすい状態へ戻す。"""
    restore_errors: list[str] = []
    restore_errors.extend(
        _restore_session_state(
            state_root,
            session_id,
            rollback_snapshot.session_state,
        )
    )

    restore_errors.extend(
        _restore_branch_head(
            repo_root,
            rollback_snapshot.home_branch,
            rollback_snapshot.home_head,
        )
    )
    restore_errors.extend(
        _restore_branch_head(
            repo_root,
            rollback_snapshot.session_branch,
            rollback_snapshot.session_head,
        )
    )

    branch_exists = run_git(
        repo_root,
        ["show-ref", "--verify", f"refs/heads/{rollback_snapshot.session_branch}"],
        check=False,
    )
    if branch_exists.returncode != 0:
        restore_errors.append(
            "branch restore failed: "
            f"session branch does not exist: {rollback_snapshot.session_branch}"
        )
        return restore_errors

    switch_result = run_git(
        repo_root,
        ["switch", rollback_snapshot.session_branch],
        check=False,
    )
    if switch_result.returncode != 0:
        detail = switch_result.stderr.strip() or switch_result.stdout.strip()
        if not detail:
            detail = (
                f"git switch {rollback_snapshot.session_branch} exited with code "
                f"{switch_result.returncode}"
            )
        restore_errors.append(f"branch restore failed: {detail}")
    return restore_errors


def _restore_branch_head(
    repo_root: Path,
    branch_name: str,
    expected_head: str,
) -> list[str]:
    """branch HEAD を cleanup 開始前の commit へ戻す。"""
    current = current_branch(repo_root)
    if current == branch_name:
        result = run_git(repo_root, ["reset", "--hard", expected_head], check=False)
    else:
        result = run_git(
            repo_root,
            ["branch", "-f", branch_name, expected_head],
            check=False,
        )

    if result.returncode == 0:
        return []

    detail = result.stderr.strip() or result.stdout.strip()
    if not detail:
        detail = f"git restore branch head exited with code {result.returncode}"
    return [f"branch head restore failed: {branch_name}: {detail}"]


def _restore_session_state(
    state_root: Path,
    session_id: str,
    expected_state: dict[str, object],
) -> list[str]:
    """session state file を cleanup 開始前の内容へ戻す。"""
    write_error: Exception | None = None
    try:
        write_session_state(state_root, session_id, deepcopy(expected_state))
    except Exception as error:
        write_error = error

    try:
        restored = read_session_state(state_root, session_id)
    except Exception as error:
        errors = [f"state restore failed: {error}"]
        if write_error is not None:
            errors.insert(0, f"state restore write failed: {write_error}")
        return errors

    if restored == expected_state:
        return []

    errors = []
    if write_error is not None:
        errors.append(f"state restore write failed: {write_error}")
    errors.append("state restore failed: restored state differs from rollback snapshot")
    return errors


def _cleanup_failure_detail(
    error: Exception,
    restore_errors: list[str],
) -> str:
    """cleanup 失敗と rollback 失敗の detail をまとめる。"""
    detail_lines = [
        f"cleanup failure: {_error_detail(error)}",
    ]
    detail_lines.extend(f"rollback failure: {line}" for line in restore_errors)
    return "\n".join(detail_lines)


def _error_detail(error: Exception) -> str:
    """例外から利用者向け detail に含める本文を取り出す。"""
    stderr = getattr(error, "stderr", None)
    if isinstance(stderr, str) and stderr.strip():
        return stderr.strip()
    return str(error)
