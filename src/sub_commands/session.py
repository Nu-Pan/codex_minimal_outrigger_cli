import json
from pathlib import Path
from typing import Callable

import typer

from acp.builder.session.join.conflict_resolution import (
    build_session_join_conflict_resolution_parameter,
)
from basic.acp import AgentCallParameter
from cmoc_runtime import (
    CmocError,
    SessionState,
    active_session_for_home,
    branch_exists,
    current_branch,
    ensure_cmoc_ignored,
    head_commit,
    is_managed_branch,
    load_state_for_branch,
    repo_root,
    require_clean_worktree,
    run_git,
    state_path,
    timestamp,
    write_state,
)


CodexExec = Callable[..., object]
GitRun = Callable[..., object]


def cmoc_session_fork_impl() -> None:
    """現在の local branch から cmoc session branch を作成する。"""
    root = repo_root()
    branch = current_branch(root)
    if is_managed_branch(branch):
        raise CmocError(
            "cmoc managed branch 上では session fork できません。",
            ["通常の local branch に checkout してから再実行してください。"],
            f"current branch: {branch}",
        )
    require_clean_worktree(root)
    ensure_cmoc_ignored(root)
    existing = active_session_for_home(root, branch)
    if existing:
        raise CmocError(
            "active session が既に存在します。",
            ["既存 session を join または abandon してから再実行してください。"],
            str(existing),
        )
    session_id = timestamp()
    session_branch = f"cmoc/session/{session_id}"
    start_commit = head_commit(root)
    run_git(["switch", "-c", session_branch], root)
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


def cmoc_session_join_impl(codex_exec: CodexExec, git: GitRun = run_git) -> None:
    """active session branch を session home branch へ merge する。"""
    root = repo_root()
    branch = current_branch(root)
    session_id, path, state = load_state_for_branch(root, branch)
    if not branch.startswith("cmoc/session/"):
        raise CmocError("session join は session branch 上で実行してください。", [], branch)
    if state.session.state != "active" or state.apply.state != "ready":
        raise CmocError(
            "session join の事前条件を満たしていません。",
            ["session.state と apply.state を確認してください。"],
            json.dumps(state.to_dict(), ensure_ascii=False, indent=2),
        )
    require_clean_worktree(root)
    ensure_cmoc_ignored(root)
    home = state.session.session_home_branch
    if not home:
        raise CmocError("session home branch を特定できません。", [], str(path))
    run_git(["switch", home], root)
    merge = git(["merge", "--no-ff", branch], root, check=False)
    if merge.returncode != 0:
        resolve_session_join_conflict(root, codex_exec, git)
    state.session.state = "joined"
    state.session.joined_at = timestamp()
    write_state(path, state)
    delete_result = git(["branch", "-d", branch], root, check=False)
    warnings: list[str] = []
    if delete_result.returncode != 0:
        warnings.append(f"session branch was not deleted: {branch}")
    warning_lines = [f"  - {warning}" for warning in warnings] if warnings else ["  - none"]
    typer.echo(
        "\n".join(
            [
                "# cmoc session join",
                f"- session_id: `{session_id}`",
                f"- joined_to: `{home}`",
                f"- deleted_session_branch: `{delete_result.returncode == 0}`",
                "- warnings:",
                *warning_lines,
            ]
        )
    )


def resolve_session_join_conflict(root: Path, codex_exec: CodexExec, git: GitRun = run_git) -> None:
    """session join の merge conflict を Codex CLI へ依頼して解消する。"""
    conflicted_paths = [
        root / line
        for line in git(["diff", "--name-only", "--diff-filter=U"], root).stdout.splitlines()
    ]
    if not conflicted_paths:
        raise CmocError(
            "merge に失敗しましたが conflict 対象ファイルを特定できません。",
            ["git status を確認し、手動解決後に再実行してください。"],
            git(["status", "--short"], root).stdout,
        )
    codex_exec(
        build_session_join_conflict_resolution_parameter(conflicted_paths),
        root=root,
        purpose="session join conflict resolution",
    )
    remaining_markers = [
        path
        for path in conflicted_paths
        if path.exists() and any(marker in path.read_text(errors="ignore") for marker in ("<<<<<<<", "=======", ">>>>>>>"))
    ]
    if remaining_markers:
        raise CmocError(
            "conflict marker が残っています。",
            ["conflict marker を手動で解消してから git commit してください。"],
            "\n".join(str(path) for path in remaining_markers),
        )
    for path in conflicted_paths:
        if path.exists():
            git(["add", str(path.relative_to(root))], root)
    unmerged = git(["diff", "--name-only", "--diff-filter=U"], root).stdout.strip()
    if unmerged:
        raise CmocError(
            "unmerged path が残っています。",
            ["git status を確認し、手動で merge を完了してください。"],
            unmerged,
        )
    git(["commit", "--no-edit"], root)


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
