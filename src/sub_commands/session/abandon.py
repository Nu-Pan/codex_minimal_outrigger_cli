import typer

from cmoc_runtime import (
    CmocError,
    branch_exists,
    current_branch,
    ensure_cmoc_ignored,
    load_state_for_branch,
    repo_root,
    require_clean_worktree,
    run_git,
    write_state,
)


def cmoc_session_abandon_impl() -> None:
    """active session を home branch へ merge せず破棄する。"""
    root = repo_root()
    branch = current_branch(root)
    _session_id, path, state = load_state_for_branch(root, branch)
    if not branch.startswith("cmoc/session/"):
        raise CmocError("session abandon は session branch 上で実行してください。", [], branch)
    if state.session.state != "active" or state.apply.state != "ready":
        raise CmocError("session abandon の事前条件を満たしていません。", [], str(path))
    require_clean_worktree(root)
    ensure_cmoc_ignored(root)
    home = state.session.session_home_branch
    if not home:
        raise CmocError("session home branch を特定できません。", [], str(path))
    if not branch_exists(root, home):
        raise CmocError(
            "session home branch が存在しません。",
            ["session state file と git branch の状態を確認してください。"],
            f"session_home_branch: {home}",
        )
    try:
        run_git(["switch", home], root)
        state.session.state = "abandoned"
        write_state(path, state)
        run_git(["branch", "-D", branch], root)
    except Exception as error:
        cleanup_detail = error.detail if isinstance(error, CmocError) else repr(error)
        rollback_errors: list[str] = []
        state.session.state = "active"
        try:
            write_state(path, state)
        except Exception as rollback_error:
            rollback_errors.append(f"state rollback failed: {rollback_error!r}")
        try:
            if branch_exists(root, branch):
                run_git(["switch", branch], root)
        except Exception as rollback_error:
            rollback_errors.append(f"branch rollback failed: {rollback_error!r}")
        details = [
            "cleanup error:",
            cleanup_detail,
            "rollback errors:",
            *(rollback_errors or ["none"]),
            f"current_branch: {current_branch(root)}",
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
                f"- joined_at: `{state.session.joined_at}`",
            ]
        )
    )
