import typer

from cmoc_runtime import (
    CmocError,
    SessionState,
    active_session_for_home,
    current_branch,
    ensure_cmoc_ignored,
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


def cmoc_session_fork_impl() -> None:
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
    require_clean_worktree(work)
    ensure_cmoc_ignored(work)
    existing = active_session_for_home(root, branch)
    if existing:
        raise CmocError(
            "active session が既に存在します。",
            ["既存 session を join または abandon してから再実行してください。"],
            str(existing),
        )
    session_id = timestamp()
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


def cmoc_session_fork_command_impl() -> None:
    run_cli_subcommand(
        cmoc_session_fork_impl,
        command_name="session fork",
        command_argv=["cmoc", "session", "fork"],
    )
