"""`cmoc session fork` の本体処理。"""

from pathlib import Path
from time import sleep

from commons.command_runner import run_command
from commons.errors import CmocError
from commons.repo import (
    SESSION_BRANCH_PREFIX,
    active_session_ids_for_home_branch,
    assert_no_uncommitted_changes,
    current_branch,
    ensure_cmoc_ignored,
    head_commit,
    initial_session_state,
    is_cmoc_branch,
    run_git,
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
    active_session_ids = active_session_ids_for_home_branch(
        repo_root,
        home_branch,
    )
    if active_session_ids:
        raise CmocError(
            "この branch には active session が既に存在します。",
            [
                "既存 session を join または abandon してから再実行してください。",
                "別の local branch から新しい session を開始してください。",
            ],
            "\n".join(active_session_ids),
        )
    start_commit = head_commit(repo_root)

    start_step(timer, 2, 4, "ensure .cmoc is ignored")
    ensure_cmoc_ignored(repo_root)

    start_step(timer, 3, 4, "create session branch")
    session_id, branch_name = _create_unique_session_branch(repo_root)

    start_step(timer, 4, 4, "record session state")
    write_session_state(
        repo_root,
        session_id,
        initial_session_state(home_branch, start_commit),
    )
    print(f"created session branch: {branch_name}")
    print(f"session home branch: {home_branch}")
    timer.report()


def _current_local_branch(repo_root: Path) -> str:
    """現在 checkout している local branch 名を返す。"""
    branch_name = current_branch(repo_root)
    if not branch_name:
        raise CmocError(
            "`cmoc session fork` は detached HEAD 上では実行できません。",
            [
                "local branch を checkout してから再実行してください。",
                "任意の commit から開始したい場合は、先に branch を作成してください。",
            ],
        )
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
