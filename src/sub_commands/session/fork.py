from pathlib import Path

import typer

from cmoc_runtime import (
    CmocError,
    SessionState,
    active_session_for_home,
    branch_exists,
    current_branch,
    delete_branch,
    ensure_cmoc_ignored_in_exclude,
    head_commit,
    is_managed_branch,
    repo_root,
    require_clean_worktree,
    run_cli_subcommand,
    run_git,
    session_fork_lock,
    start_subcommand_step,
    state_path,
    timestamp,
    work_root,
    write_state,
)


MAX_SESSION_ID_ATTEMPTS = 32


def cmoc_session_fork_impl() -> None:
    """CLI runtime を通して session fork を実行する。"""
    run_cli_subcommand(
        _cmoc_session_fork_body,
        pre_log_check=ensure_cmoc_ignored_in_exclude,
        command_name="session fork",
        command_argv=["cmoc", "session", "fork"],
        use_work_root_runtime=True,
        total_steps=7,
    )


def _cmoc_session_fork_body() -> None:
    """現在の local branch から cmoc session branch を作成する。"""
    root = repo_root()
    work = work_root()
    start_subcommand_step(2, "現在の local branch を取得", "get current branch")
    branch = current_branch(work)
    if is_managed_branch(branch):
        raise CmocError(
            "cmoc managed branch 上では session fork できません。",
            ["通常の local branch に checkout してから再実行してください。"],
            f"current branch: {branch}",
        )
    ensure_cmoc_ignored_in_exclude(work)
    require_clean_worktree(work)
    with session_fork_lock(root):
        # {{work-root}}/oracle/doc/app_spec/sub_command/session_fork.md
        # active session と session-id を lock 内で再確認し、同じ home branch に
        # 複数の session branch/state が公開される競合を防ぐ。
        existing = active_session_for_home(root, branch)
        if existing:
            raise CmocError(
                "active session が既に存在します。",
                ["既存 session を join または abandon してから再実行してください。"],
                str(existing),
            )
        start_subcommand_step(3, "現在の HEAD commit を取得", "get HEAD commit")
        start_commit = head_commit(work)
        start_subcommand_step(4, "session-id を生成", "generate session id")
        session_id = _new_session_id(root)
        session_branch = f"cmoc/session/{session_id}"
        path = state_path(root, session_id)
        state = SessionState()
        state.session.session_home_branch = branch
        state.session.session_start_commit = start_commit
        start_subcommand_step(
            5, "session branch を作成して checkout", "create session branch"
        )
        try:
            run_git(["switch", "-c", session_branch], work)
            start_subcommand_step(6, "session state を保存", "write session state")
            write_state(path, state)
        except BaseException as error:
            rollback_errors: list[str] = []
            if branch_exists(root, session_branch):
                try:
                    run_git(["switch", branch], work)
                except BaseException as rollback_error:
                    rollback_errors.append(
                        f"home branch rollback failed: {rollback_error!r}"
                    )
                try:
                    delete_result = delete_branch(root, session_branch, force=True)
                    if delete_result.returncode != 0:
                        rollback_errors.append(
                            f"session branch deletion failed: {delete_result.stderr.strip()}"
                        )
                except BaseException as rollback_error:
                    rollback_errors.append(
                        f"session branch deletion failed: {rollback_error!r}"
                    )
            try:
                path.unlink(missing_ok=True)
            except BaseException as rollback_error:
                rollback_errors.append(
                    f"session state cleanup failed: {rollback_error!r}"
                )
            details = [
                f"original error: {error!r}",
                "rollback errors:",
                *(rollback_errors or ["none"]),
                f"current_branch: {current_branch(work)}",
                f"session_branch: {session_branch}",
                f"session_branch_exists: {branch_exists(root, session_branch)}",
                f"session_state_file: {path}",
                f"session_state_file_exists: {path.exists()}",
            ]
            guidance = (
                [
                    "残存した branch と state file を手動で確認・復旧してから再実行してください。"
                ]
                if rollback_errors
                else [
                    "作成前の状態を確認してから `cmoc session fork` を再実行してください。"
                ]
            )
            raise CmocError(
                "session fork の作成に失敗しました。", guidance, "\n".join(details)
            ) from error
        start_subcommand_step(7, "作成結果を表示", "show session result")
        typer.echo(
            "\n".join(
                [
                    "# cmoc session fork",
                    f"- session_branch: `{session_branch}`",
                    f"- session_home_branch: `{branch}`",
                    f"- session_state_file: `{path}`",
                ]
            )
        )


def _new_session_id(root: Path) -> str:
    # 根拠: {{work-root}}/oracle/doc/app_spec/sub_command/session_fork.md
    # 根拠: {{work-root}}/oracle/doc/app_spec/session_state.md
    # state file が残った joined/abandoned session との衝突も session-id 衝突として扱う。
    for _ in range(MAX_SESSION_ID_ATTEMPTS):
        session_id = timestamp()
        if not branch_exists(root, f"cmoc/session/{session_id}") and not state_path(
            root, session_id
        ).exists():
            return session_id
    raise CmocError(
        "一意な session-id を生成できませんでした。",
        ["時間を置いてから `cmoc session fork` を再実行してください。"],
        f"attempts: {MAX_SESSION_ID_ATTEMPTS}",
    )
