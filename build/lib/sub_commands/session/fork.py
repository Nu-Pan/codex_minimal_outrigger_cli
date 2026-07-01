from pathlib import Path

import typer

from cmoc_runtime import (
    CmocError,
    SessionState,
    active_session_for_home,
    branch_exists,
    current_branch,
    ensure_cmoc_ignored_in_exclude,
    head_commit,
    is_managed_branch,
    repo_root,
    require_clean_worktree,
    run_cli_subcommand,
    run_git,
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
    )


def _cmoc_session_fork_body() -> None:
    """現在の local branch から cmoc session branch を作成する。"""
    root = repo_root()
    work = work_root()
    branch = current_branch(work)
    if is_managed_branch(branch):
        raise CmocError(
            "cmoc managed branch 上では session fork できません。",
            ["通常の local branch に checkout してから再実行してください。"],
            f"current branch: {branch}",
        )
    ensure_cmoc_ignored_in_exclude(work)
    require_clean_worktree(work)
    existing = active_session_for_home(root, branch)
    if existing:
        raise CmocError(
            "active session が既に存在します。",
            ["既存 session を join または abandon してから再実行してください。"],
            str(existing),
        )
    session_id = _new_session_id(root)
    session_branch = f"cmoc/session/{session_id}"
    start_commit = head_commit(work)
    run_git(["switch", "-c", session_branch], work)
    state = SessionState()
    state.session.session_home_branch = branch
    state.session.session_start_commit = start_commit
    write_state(state_path(root, session_id), state)
    typer.echo(
        "\n".join(
            [
                "# cmoc session fork",
                f"- session_branch: `{session_branch}`",
                f"- session_home_branch: `{branch}`",
                f"- session_state_file: `{state_path(root, session_id)}`",
            ]
        )
    )


def _new_session_id(root: Path) -> str:
    # 根拠: <work-root>/oracle/doc/app_spec/sub_command/session_fork.md
    # 根拠: <work-root>/oracle/doc/app_spec/session_state.md
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
