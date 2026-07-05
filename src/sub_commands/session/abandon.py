import typer

from cmoc_runtime import (
    CmocError,
    branch_exists,
    current_branch,
    delete_branch,
    load_state_for_branch,
    repo_root,
    require_clean_worktree,
    run_cli_subcommand,
    run_git,
    work_root,
    write_state,
)


def cmoc_session_abandon_impl() -> None:
    """CLI runtime を通して session abandon を実行する。"""
    run_cli_subcommand(
        _cmoc_session_abandon_body,
        command_name="session abandon",
        command_argv=["cmoc", "session", "abandon"],
        use_work_root_runtime=True,
    )


def _cmoc_session_abandon_body() -> None:
    """active session を home branch へ merge せず破棄する。"""
    repo = repo_root()
    work = work_root()
    branch = current_branch(work)
    _session_id, path, state = load_state_for_branch(repo, branch)
    if not branch.startswith("cmoc/session/"):
        raise CmocError("session abandon は session branch 上で実行してください。", [], branch)
    if state.session.state != "active" or state.apply.state != "ready":
        raise CmocError("session abandon の事前条件を満たしていません。", [], str(path))
    require_clean_worktree(work)
    home = state.session.session_home_branch
    if not home:
        raise CmocError("session home branch を特定できません。", [], str(path))
    if not branch_exists(repo, home):
        raise CmocError(
            "session home branch が存在しません。",
            ["session state file と git branch の状態を確認してください。"],
            f"session_home_branch: {home}",
        )
    try:
        run_git(["switch", home], work)
        state.session.state = "abandoned"
        write_state(path, state)
        # <work-root>/oracle/doc/app_spec/sub_command/session_abandon.md
        # requires preserving the home branch while deleting only the session branch.
        delete_result = delete_branch(repo, branch, force=True)
        if delete_result.returncode != 0:
            raise CmocError(
                "session branch の削除に失敗しました。",
                ["git branch の状態を確認してください。"],
                delete_result.stderr,
            )
    except Exception as error:
        cleanup_detail = error.detail if isinstance(error, CmocError) else repr(error)
        rollback_errors: list[str] = []
        state.session.state = "active"
        try:
            write_state(path, state)
        except Exception as rollback_error:
            rollback_errors.append(f"state rollback failed: {rollback_error!r}")
        switched_back = False
        try:
            if branch_exists(repo, branch):
                run_git(["switch", branch], work)
                switched_back = True
        except Exception as rollback_error:
            rollback_errors.append(f"branch rollback failed: {rollback_error!r}")
        details = [
            "cleanup error:",
            cleanup_detail,
            "rollback errors:",
            *(rollback_errors or ["none"]),
            f"current_branch: {current_branch(work)}",
            f"session_branch: {branch}",
            f"session_home_branch: {home}",
            f"session_state_file: {path}",
        ]
        raise CmocError(
            "session abandon の cleanup に失敗しました。",
            [
                "問題を手動解決したうえで `cmoc session abandon` を再実行してください。",
                "state が active で session branch 上に戻っているか確認してください。",
            ],
            "\n".join(details),
        ) from error
    typer.echo(
        "\n".join(
            [
                "# cmoc session abandon",
                f"- abandoned_branch: `{branch}`",
                f"- switched_to: `{home}`",
                "- session_state: `abandoned`",
            ]
        )
    )
