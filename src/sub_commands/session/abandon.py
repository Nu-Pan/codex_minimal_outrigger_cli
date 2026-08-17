# {{work-root}}/oracle/doc/app_spec/sub_command/session_abandon.md
from cmoc_runtime import (
    CmocError,
    TerminalResult,
    branch_exists,
    current_branch,
    delete_branch,
    head_commit,
    load_state_for_branch,
    repo_root,
    require_clean_worktree,
    run_cli_subcommand,
    run_git,
    start_subcommand_step,
    work_root,
    write_state,
)
from commons.runtime_primary_report import update_primary_report_fields


def cmoc_session_abandon_impl() -> None:
    """CLI runtime を通して session abandon を実行する。"""
    run_cli_subcommand(
        _cmoc_session_abandon_body,
        command_name="session abandon",
        command_argv=["cmoc", "session", "abandon"],
        use_work_root_runtime=True,
        total_steps=4,
    )


def _cmoc_session_abandon_body() -> TerminalResult:
    """active session を home branch へ merge せず破棄する。"""
    repo = repo_root()
    work = work_root()
    branch = current_branch(work)
    update_primary_report_fields(
        session_branch=branch,
        session_state_before=None,
        session_state_after=None,
    )
    start_subcommand_step(2, "事前条件を確認", "validate preconditions")
    _session_id, path, state = load_state_for_branch(repo, branch)
    if not branch.startswith("cmoc/session/"):
        raise CmocError(
            "session abandon は session branch 上で実行してください。", [], branch
        )
    home = state.session.session_home_branch
    update_primary_report_fields(
        home_branch=home,
        session_state_before=state.session.state,
    )
    if state.session.state != "active" or state.run.state != "ready":
        raise CmocError("session abandon の事前条件を満たしていません。", [], str(path))
    session_commit = head_commit(work)
    update_primary_report_fields(abandoned_branch_start_commit=session_commit)
    require_clean_worktree(work)
    if not home:
        raise CmocError("session home branch を特定できません。", [], str(path))
    if not branch_exists(repo, home):
        raise CmocError(
            "session home branch が存在しません。",
            ["session state file と git branch の状態を確認してください。"],
            f"session_home_branch: {home}",
        )
    start_subcommand_step(3, "session をクリーンアップ", "cleanup session")
    try:
        # {{work-root}}/oracle/doc/branch_model.md
        # session home branch は local branch なので、確認と切替の間に local ref が
        # 消えても同名 remote-tracking branch を別の home branch として推測しない。
        run_git(["switch", "--no-guess", home], work)
        state.session.state = "abandoned"
        write_state(path, state)
        update_primary_report_fields(session_state_after="abandoned")
        # {{work-root}}/oracle/doc/app_spec/sub_command/session_abandon.md
        # home branch を保持したまま session branch だけを削除する必要がある。
        delete_result = delete_branch(repo, branch, force=True)
        if delete_result.returncode != 0:
            raise CmocError(
                "session branch の削除に失敗しました。",
                ["git branch の状態を確認してください。"],
                delete_result.stderr,
            )
    except BaseException as error:
        # {{work-root}}/oracle/doc/app_spec/sub_command/session_abandon.md
        # cleanup 中の利用者中断は cleanup failure として扱い、session を再実行可能な
        # state へ戻さなければならない。
        cleanup_detail = error.detail if isinstance(error, CmocError) else repr(error)
        rollback_errors: list[str] = []
        state.session.state = "active"
        state_rollback_completed = False
        try:
            write_state(path, state)
            state_rollback_completed = True
        except BaseException as rollback_error:
            rollback_errors.append(f"state rollback failed: {rollback_error!r}")
        try:
            # {{work-root}}/oracle/doc/app_spec/sub_command/session_abandon.md
            # 削除処理が副作用後に中断しても、元の commit から session branch を復元する。
            if not branch_exists(repo, branch):
                run_git(["branch", branch, session_commit], repo)
            if branch_exists(repo, branch):
                run_git(["switch", branch], work)
        except BaseException as rollback_error:
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
        update_primary_report_fields(
            session_state_after="active" if state_rollback_completed else None,
            rollback_status="failed" if rollback_errors else "completed",
        )
        raise CmocError(
            "session abandon の cleanup に失敗しました。",
            [
                "問題を手動解決したうえで `cmoc session abandon` を再実行してください。",
                "state が active で session branch 上に戻っているか確認してください。",
            ],
            "\n".join(details),
        ) from error
    start_subcommand_step(4, "terminal result を確定", "finalize terminal result")
    return TerminalResult(
        details=(
            ("abandoned_branch", branch),
            ("switched_to", home),
            ("session_state", "abandoned"),
            ("cleanup", "completed"),
        )
    )
