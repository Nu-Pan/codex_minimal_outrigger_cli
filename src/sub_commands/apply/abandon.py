import os

import typer

from cmoc_runtime import (
    ApplyPart,
    CmocError,
    apply_branch_session_id,
    branch_exists,
    current_branch,
    delete_branch,
    load_state_for_branch,
    remove_worktree,
    repo_root,
    require_clean_worktree,
    run_cli_subcommand,
    work_root,
    write_state,
)
from commons.runtime_apply import (
    delete_apply_process_id,
    expected_apply_worktree,
    read_apply_process_id,
    stop_apply_process,
    worktree_for_branch,
)


def cmoc_apply_abandon_impl() -> None:
    """CLI runtime を通して apply abandon を実行する。"""
    run_cli_subcommand(
        _cmoc_apply_abandon_body,
        command_name="apply abandon",
        command_argv=["cmoc", "apply", "abandon"],
    )


def _cmoc_apply_abandon_body() -> None:
    """未 join の apply run を破棄して apply state を ready に戻す。"""
    repo = repo_root()
    current_root = work_root()
    branch = current_branch(current_root)
    if not (branch.startswith("cmoc/session/") or branch.startswith("cmoc/apply/")):
        raise CmocError("apply abandon は session branch または apply branch 上で実行してください。", [], branch)
    if branch.startswith("cmoc/apply/"):
        session_id = apply_branch_session_id(branch)
        session_branch = f"cmoc/session/{session_id}"
        session_worktree = worktree_for_branch(repo, session_branch)
    else:
        session_worktree = current_root
    session_id, path, state = load_state_for_branch(repo, branch)
    if state.session.state != "active" or state.apply.state == "ready":
        raise CmocError("破棄対象の active apply run がありません。", [], str(path))
    require_clean_worktree(session_worktree)
    previous = state.apply.state
    apply_branch = state.apply.apply_branch
    if not apply_branch:
        raise CmocError(
            "破棄対象 apply run の補助情報を特定できません。",
            ["session state file の apply.apply_branch を確認してください。"],
            str(path),
        )
    # <work-root>/oracle/doc/app_spec/sub_command/apply_abandon.md
    # The state file is mutable local state, so cleanup must prove the stored
    # apply branch still belongs to the current session before deleting it.
    apply_session_id = apply_branch_session_id(apply_branch)
    if apply_session_id != session_id:
        raise CmocError(
            "破棄対象 apply run の補助情報を特定できません。",
            ["session state file の apply.apply_branch を確認してください。"],
            f"session_id: {session_id}\napply_branch: {apply_branch}",
        )
    if branch.startswith("cmoc/apply/") and branch != apply_branch:
        raise CmocError(
            "現在の apply branch は破棄対象の active apply run ではありません。",
            ["session state file が指す apply branch 上、または session branch 上から再実行してください。"],
            f"current_branch: {branch}\napply_branch: {apply_branch}",
        )
    apply_worktree = expected_apply_worktree(repo, apply_branch)
    warnings: list[str] = []
    if previous == "running":
        process_id = read_apply_process_id(repo, session_id)
        if process_id is None:
            raise CmocError(
                "実行中 apply process を特定できません。",
                ["apply process id file を確認し、apply process 停止後に再実行してください。"],
                f"session_id: {session_id}",
            )
        stopped_warning = stop_apply_process(
            process_id,
            lambda: read_apply_process_id(repo, session_id),
        )
        if stopped_warning:
            warnings.append(stopped_warning)
    if branch == apply_branch:
        os.chdir(session_worktree)
    if not apply_worktree.exists():
        warnings.append(f"apply worktree already missing: {apply_worktree}")
    remove_worktree(repo, apply_worktree)
    if not branch_exists(repo, apply_branch):
        warnings.append(f"apply branch already missing: {apply_branch}")
    else:
        delete_branch(repo, apply_branch, force=True)
    if apply_worktree and apply_worktree.exists():
        warnings.append(f"orphan apply worktree remains: {apply_worktree}")
    if branch_exists(repo, apply_branch):
        warnings.append(f"orphan apply branch remains: {apply_branch}")
    delete_apply_process_id(repo, session_id)
    state.apply = ApplyPart()
    write_state(path, state)
    warning_lines = [f"  - {warning}" for warning in warnings] if warnings else ["  - none"]
    typer.echo(
        "\n".join(
            [
                "# cmoc apply abandon",
                f"- apply_branch: `{apply_branch}`",
                f"- apply_worktree: `{apply_worktree}`",
                f"- before: `{previous}`",
                "- after: `ready`",
                "- warnings:",
                *warning_lines,
            ]
        )
    )
