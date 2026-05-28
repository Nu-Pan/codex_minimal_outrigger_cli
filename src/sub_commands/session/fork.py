"""`cmoc session fork` の本体処理。"""

import fcntl
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path
from time import sleep

from commons.command_runner import run_command
from commons.errors import CmocError
from commons.repo import (
    SESSION_BRANCH_PREFIX,
    active_session_ids_for_home_branch,
    assert_no_uncommitted_changes,
    ensure_cmoc_ignored,
    head_commit,
    initial_session_state,
    is_cmoc_branch,
    run_git,
    session_state_path,
    session_state_root,
    write_session_state,
)
from commons.timing import StepTimer, start_step
from commons.timestamps import make_timestamp


def cmoc_session_fork_impl(repo_root: Path | None = None) -> None:
    """cmoc session branch を作成し、session state を記録する。"""
    # 直接呼び出し時は共通 runner で repo root 解決とエラー整形を行う。
    if repo_root is None:
        run_command(cmoc_session_fork_impl)
        return

    timer = StepTimer("session fork")
    start_step(timer, 1, 4, "validate repository state")
    home_branch = _current_local_branch(repo_root)
    if is_cmoc_branch(home_branch):
        raise CmocError(
            "`cmoc session fork` は cmoc 管理 branch 上では実行できません。",
            [
                "通常の local branch へ移動してから再実行してください。",
                "既存 session を使う場合は、その session branch 上で作業してください。",
            ],
            f"現在の branch: {home_branch}",
        )
    assert_no_uncommitted_changes(repo_root)

    start_step(timer, 2, 4, "ensure .cmoc is ignored")
    ensure_cmoc_ignored(repo_root)
    assert_no_uncommitted_changes(repo_root)

    active_session_ids = active_session_ids_for_home_branch(
        repo_root,
        home_branch,
    )
    _assert_no_active_session(active_session_ids)
    start_commit = head_commit(repo_root)

    start_step(timer, 3, 4, "create session branch")
    state_root = session_state_root(repo_root)
    with _locked_session_creation(state_root):
        active_session_ids = active_session_ids_for_home_branch(
            repo_root,
            home_branch,
        )
        _assert_no_active_session(active_session_ids)
        session_id, branch_name = _create_unique_session_branch(repo_root)

        start_step(timer, 4, 4, "record session state")
        session_state = initial_session_state(home_branch, start_commit)
        try:
            write_session_state(
                state_root,
                session_id,
                session_state,
            )
        except Exception as error:
            _rollback_created_session_branch(
                repo_root,
                state_root,
                home_branch,
                branch_name,
                session_id,
                session_state,
                error,
            )
    print(f"created session branch: {branch_name}")
    print(f"session home branch: {home_branch}")
    timer.report()


def _assert_no_active_session(active_session_ids: list[str]) -> None:
    """同じ home branch の active session が存在しないことを検証する。"""
    if active_session_ids:
        raise CmocError(
            "この branch には active session が既に存在します。",
            [
                "既存 session を join または abandon してから再実行してください。",
                "別の local branch から新しい session を開始してください。",
            ],
            "\n".join(active_session_ids),
        )


@contextmanager
def _locked_session_creation(state_root: Path) -> Iterator[None]:
    """session 作成中の active 判定と state 永続化を直列化する。"""
    # canonical state root 単位で作成処理を直列化し、home branch ごとの一意性を守る。
    lock_dir = state_root / ".cmoc" / "locks"
    lock_dir.mkdir(parents=True, exist_ok=True)
    lock_path = lock_dir / "session-fork.lock"
    with lock_path.open("a+", encoding="utf-8") as lock_file:
        fcntl.flock(lock_file.fileno(), fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(lock_file.fileno(), fcntl.LOCK_UN)


def _current_local_branch(repo_root: Path) -> str:
    """現在 checkout している local branch 名を返す。"""
    result = run_git(
        repo_root,
        ["symbolic-ref", "--quiet", "--short", "HEAD"],
        check=False,
    )
    if result.returncode != 0:
        raise CmocError(
            "`cmoc session fork` は detached HEAD 上では実行できません。",
            [
                "local branch を checkout してから再実行してください。",
                "任意の commit から開始したい場合は、先に branch を作成してください。",
            ],
        )
    branch_name = result.stdout.strip()
    result = run_git(
        repo_root,
        ["show-ref", "--verify", f"refs/heads/{branch_name}"],
        check=False,
    )
    if result.returncode != 0:
        raise CmocError(
            "`cmoc session fork` は local branch 上でのみ実行できます。",
            [
                "local branch を checkout してから再実行してください。",
                "remote-tracking branch や commit hash からは session を開始できません。",
            ],
            f"現在の branch: {branch_name}",
        )
    return branch_name


def _create_unique_session_branch(repo_root: Path) -> tuple[str, str]:
    """衝突時に session id を作り直して branch 作成をリトライする。"""
    # timestamp 衝突に備えて短い sleep を挟みながら最大 10 回リトライする。
    for attempt in range(1, 11):
        session_id = make_timestamp()
        branch_name = f"{SESSION_BRANCH_PREFIX}{session_id}"
        print(f"create session branch attempt ({attempt}/10) {branch_name}")
        result = run_git(
            repo_root,
            ["checkout", "-b", branch_name],
            check=False,
        )
        if result.returncode == 0:
            return session_id, branch_name
        sleep(0.001)
    raise RuntimeError("リトライ後も一意な session branch を作成できませんでした。")


def _rollback_created_session_branch(
    repo_root: Path,
    state_root: Path,
    home_branch: str,
    branch_name: str,
    session_id: str,
    session_state: dict[str, object],
    error: Exception,
) -> None:
    """session state 保存失敗時に作成済み branch を破棄する。"""
    # state と branch を揃って作るため、保存失敗時は開始前の branch へ戻す。
    rollback_errors: list[str] = []
    state_path = session_state_path(state_root, session_id)
    switch_result = run_git(
        repo_root,
        ["switch", home_branch],
        check=False,
    )
    if switch_result.returncode != 0:
        rollback_errors.append(switch_result.stderr.strip())
    else:
        delete_result = run_git(
            repo_root,
            ["branch", "-D", branch_name],
            check=False,
        )
        if delete_result.returncode != 0:
            rollback_errors.append(delete_result.stderr.strip())

    if rollback_errors:
        _ensure_session_state_for_failed_rollback(
            state_root,
            session_id,
            session_state,
            rollback_errors,
        )
    else:
        state_path.unlink(missing_ok=True)

    detail_lines = [str(error)]
    detail_lines.extend(line for line in rollback_errors if line)
    message = "session state の保存に失敗したため session branch 作成を取り消しました。"
    if rollback_errors:
        message = (
            "session state の保存に失敗し、"
            "session branch 作成を完全には取り消せませんでした。"
        )
    raise CmocError(
        message,
        [
            ".cmoc/sessions 配下の権限とディスク状態を確認してください。",
            "rollback に失敗した場合は Detail の branch と state を手動で確認してください。",
        ],
        "\n".join(detail_lines),
    ) from error


def _ensure_session_state_for_failed_rollback(
    state_root: Path,
    session_id: str,
    session_state: dict[str, object],
    rollback_errors: list[str],
) -> None:
    """rollback 失敗時に残存 branch と対応する state を残す。"""
    state_path = session_state_path(state_root, session_id)
    if state_path.exists():
        return
    try:
        write_session_state(state_root, session_id, session_state)
    except Exception as recovery_error:
        rollback_errors.append(f"state recovery failure: {recovery_error}")
