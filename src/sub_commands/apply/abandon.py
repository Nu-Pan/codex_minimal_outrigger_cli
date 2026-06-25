import os

import typer

from cmoc_runtime import (
    ApplyPart,
    CmocError,
    branch_exists,
    current_branch,
    delete_branch,
    load_state_for_branch,
    remove_worktree,
    repo_root,
    require_clean_worktree,
    work_root,
    write_state,
)
from sub_commands.apply._runtime import (
    expected_apply_worktree,
    stop_apply_process,
    worktree_for_branch,
)


def cmoc_apply_abandon_impl() -> None:
    """未 join の apply run を破棄して apply state を ready に戻す。"""
    repo = repo_root()
    current_root = work_root()
    branch = current_branch(current_root)
    if not (branch.startswith("cmoc/session/") or branch.startswith("cmoc/apply/")):
        raise CmocError("apply abandon は session branch または apply branch 上で実行してください。", [], branch)
    if branch.startswith("cmoc/apply/"):
        session_id = branch.split("/")[2]
        session_branch = f"cmoc/session/{session_id}"
        root = worktree_for_branch(repo, session_branch)
    else:
        root = repo
    _session_id, path, state = load_state_for_branch(root, branch)
    if state.session.state != "active" or state.apply.state == "ready":
        raise CmocError("破棄対象の active apply run がありません。", [], str(path))
    require_clean_worktree(root)
    previous = state.apply.state
    apply_branch = state.apply.apply_branch
    if not apply_branch:
        raise CmocError(
            "破棄対象 apply run の補助情報を特定できません。",
            ["session state file の apply.apply_branch を確認してください。"],
            str(path),
        )
    if branch.startswith("cmoc/apply/") and branch != apply_branch:
        raise CmocError(
            "現在の apply branch は破棄対象の active apply run ではありません。",
            ["session state file が指す apply branch 上、または session branch 上から再実行してください。"],
            f"current_branch: {branch}\napply_branch: {apply_branch}",
        )
    apply_worktree = expected_apply_worktree(root, apply_branch)
    warnings: list[str] = []
    if previous == "running":
        process_id = state.apply.apply_process_id
        if process_id is None:
            raise CmocError(
                "実行中 apply process を特定できません。",
                ["session state file の apply.apply_process_id を確認してください。"],
                str(path),
            )
        stopped_warning = stop_apply_process(process_id)
        if stopped_warning:
            warnings.append(stopped_warning)
    if branch == apply_branch:
        os.chdir(root)
    if not apply_worktree.exists():
        warnings.append(f"apply worktree already missing: {apply_worktree}")
    remove_worktree(root, apply_worktree)
    if not branch_exists(root, apply_branch):
        warnings.append(f"apply branch already missing: {apply_branch}")
    else:
        delete_branch(root, apply_branch, force=True)
    if apply_worktree and apply_worktree.exists():
        warnings.append(f"orphan apply worktree remains: {apply_worktree}")
    if branch_exists(root, apply_branch):
        warnings.append(f"orphan apply branch remains: {apply_branch}")
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
