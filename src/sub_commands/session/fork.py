from pathlib import Path

import typer

from cmoc_runtime import (
    CmocError,
    SessionState,
    active_session_for_home,
    current_branch,
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
    """CLI runtime を通して session fork を実行する。"""
    run_cli_subcommand(
        _cmoc_session_fork_body,
        pre_log_check=ensure_cmoc_ignored_for_session_fork,
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
    ensure_cmoc_ignored_for_session_fork(work)
    require_clean_worktree(work)
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

def ensure_cmoc_ignored_for_session_fork(root: Path) -> None:
    # session fork は clean worktree を保ったまま、ログ作成前に .cmoc を ignore する必要がある。
    exclude_path = root / run_git(
        ["rev-parse", "--git-path", "info/exclude"], root
    ).stdout.strip()
    content = exclude_path.read_text() if exclude_path.exists() else ""
    if "/.cmoc/" not in content.splitlines():
        exclude_path.parent.mkdir(parents=True, exist_ok=True)
        newline = "" if content == "" or content.endswith("\n") else "\n"
        exclude_path.write_text(f"{content}{newline}/.cmoc/\n")
    tracked = run_git(["ls-files", "--", ".cmoc"], root).stdout.strip()
    ignored = run_git(
        ["check-ignore", "-q", ".cmoc/.__cmoc_ignore_probe__"],
        root,
        check=False,
    )
    if tracked or ignored.returncode != 0:
        raise CmocError(
            ".cmoc を git 追跡対象外にできませんでした。",
            [".gitignore と git index の状態を確認してください。"],
            f"tracked:\n{tracked}\ncheck-ignore returncode: {ignored.returncode}",
        )
