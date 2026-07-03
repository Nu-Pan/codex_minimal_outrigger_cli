from pathlib import Path

import typer

from cmoc_runtime import (
    CmocError,
    branch_exists,
    current_branch,
    delete_branch,
    ensure_cmoc_ignored,
    load_state_for_branch,
    repo_root,
    require_clean_worktree,
    run_cli_subcommand,
    run_git,
    work_root,
    write_state,
)


type CmocIgnoreSnapshot = tuple[bool, str, bool]


def cmoc_session_abandon_impl() -> None:
    """CLI runtime を通して session abandon を実行する。"""
    run_cli_subcommand(
        _cmoc_session_abandon_body,
        command_name="session abandon",
        command_argv=["cmoc", "session", "abandon"],
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
    ignore_snapshot = _cmoc_ignore_snapshot(work)
    ensure_cmoc_ignored(work)
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
        try:
            _discard_cmoc_ignore_changes_on_current_head(work, ignore_snapshot)
        except Exception as rollback_error:
            rollback_errors.append(f"cmoc ignore discard failed: {rollback_error!r}")
        switched_back = False
        try:
            if branch_exists(repo, branch):
                run_git(["switch", branch], work)
                switched_back = True
        except Exception as rollback_error:
            rollback_errors.append(f"branch rollback failed: {rollback_error!r}")
        if switched_back:
            try:
                _restore_cmoc_ignore_snapshot(work, ignore_snapshot)
            except Exception as rollback_error:
                rollback_errors.append(
                    f"cmoc ignore rollback failed: {rollback_error!r}"
                )
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


def _cmoc_ignore_snapshot(root: Path) -> CmocIgnoreSnapshot:
    gitignore = root / ".gitignore"
    return (
        gitignore.exists(),
        gitignore.read_text() if gitignore.exists() else "",
        bool(run_git(["ls-files", "--", ".cmoc"], root).stdout.strip()),
    )


def _discard_cmoc_ignore_changes_on_current_head(
    root: Path, snapshot: CmocIgnoreSnapshot
) -> None:
    # <work-root>/oracle/doc/app_spec/sub_command/session_abandon.md
    # Carried gitignore/index changes can block switching back to the session branch.
    run_git(["restore", "--staged", "--", ".cmoc"], root, check=False)
    run_git(["restore", "--worktree", "--", ".gitignore"], root, check=False)
    gitignore = root / ".gitignore"
    if not snapshot[0] and gitignore.exists():
        gitignore.unlink()


def _restore_cmoc_ignore_snapshot(root: Path, snapshot: CmocIgnoreSnapshot) -> None:
    # <work-root>/oracle/doc/app_spec/sub_command/session_abandon.md
    # ensure_cmoc_ignored may mutate .gitignore and the index before cleanup fails.
    gitignore_existed, gitignore_content, had_tracked_cmoc = snapshot
    gitignore = root / ".gitignore"
    if gitignore_existed:
        gitignore.write_text(gitignore_content)
    elif gitignore.exists():
        gitignore.unlink()
    if had_tracked_cmoc:
        run_git(["restore", "--staged", "--", ".cmoc"], root, check=False)
    else:
        run_git(["rm", "--cached", "-r", "--ignore-unmatch", ".cmoc"], root)
