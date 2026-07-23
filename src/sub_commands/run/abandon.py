"""`cmoc run abandon` の workload 非依存 cleanup lifecycle。"""

import os
from pathlib import Path

import typer

from cmoc_runtime import (
    CmocError,
    RunPart,
    branch_exists,
    delete_branch,
    remove_worktree,
    require_clean_worktree,
    run_cli_subcommand,
    run_doctor_preprocess,
    start_subcommand_step,
    work_root,
    write_state,
)
from commons.runtime_run import (
    delete_run_process_id,
    read_run_process_id,
    run_lifecycle_lock,
    stop_run_process,
)
from sub_commands.run.lifecycle import EditingRunContext, resolve_active_run
from sub_commands.run.report import write_lifecycle_report


def cmoc_run_abandon_impl() -> None:
    """CLI runtime を通して active editing run を破棄する。"""
    run_cli_subcommand(
        _cmoc_run_abandon_body,
        command_name="run abandon",
        command_argv=["cmoc", "run", "abandon"],
        doctor_preprocess=False,
        total_steps=4,
    )


def _cmoc_run_abandon_body() -> None:
    start_subcommand_step(1, "doctor preprocess", "doctor preprocess")
    # {{work-root}}/oracle/doc/app_spec/doctor_preprocess.md
    # abandon は run branch を merge しないため、entry 集合を通常どおり同期する。
    run_doctor_preprocess(work_root())
    start_subcommand_step(2, "active run を特定", "resolve active run")
    initial_context, _ = resolve_active_run(
        {"running", "joinable", "error"},
        allow_missing_run_worktree=True,
    )
    with run_lifecycle_lock(initial_context.repo, initial_context.session_id):
        context, state = resolve_active_run(
            {"running", "joinable", "error"},
            allow_missing_run_worktree=True,
        )
        require_clean_worktree(context.session_worktree)
        warnings: list[str] = []
        stopped = "not_running"
        if state.run.state == "running":
            stopped = _stop_running_run(context, warnings)
        start_subcommand_step(3, "run worktree と branch を破棄", "cleanup run")
        if Path.cwd().resolve() == context.run_worktree.resolve():
            os.chdir(context.session_worktree)
        worktree_removed = _remove_run_worktree(context, warnings)
        branch_removed = _remove_run_branch(context, warnings)
        if not worktree_removed or not branch_removed:
            raise CmocError(
                "active run の cleanup を完了できません。",
                ["git worktree list と run branch を確認して再実行してください。"],
                f"worktree_removed: {worktree_removed}\nbranch_removed: {branch_removed}",
            )
        state.run = RunPart()
        write_state(context.state_path, state)
        delete_run_process_id(context.repo, context.session_id)
        report = write_lifecycle_report(
            context,
            "abandon",
            state_after="ready",
            warnings=warnings,
            details={
                "process_stop": stopped,
                "worktree_removed": worktree_removed,
                "branch_removed": branch_removed,
                "cleanup": "completed",
            },
        )
    start_subcommand_step(4, "abandon 結果を表示", "show abandon result")
    typer.echo(
        "\n".join(
            [
                "# cmoc run abandon",
                f"- run_kind: `{context.kind}`",
                f"- run_branch: `{context.run_branch}`",
                f"- run_worktree: `{context.run_worktree}`",
                f"- process_stop: `{stopped}`",
                "- cleanup: `completed`",
                f"- report: `{report}`",
            ]
        )
    )


def _stop_running_run(
    context: EditingRunContext,
    warnings: list[str],
) -> str:
    process = read_run_process_id(context.repo, context.session_id)
    if process is None:
        warnings.append("run process tracking was absent or stale")
        return "already_stopped"
    warning = stop_run_process(
        process,
        lambda: read_run_process_id(context.repo, context.session_id),
    )
    if warning:
        warnings.append(warning)
    return "stopped"


def _remove_run_worktree(
    context: EditingRunContext,
    warnings: list[str],
) -> bool:
    if not context.run_worktree.exists():
        warnings.append("run worktree was already absent")
    result = remove_worktree(context.repo, context.run_worktree)
    if result.returncode != 0 and context.run_worktree.exists():
        warnings.append(result.stderr.strip() or "run worktree removal failed")
        return False
    return not context.run_worktree.exists()


def _remove_run_branch(
    context: EditingRunContext,
    warnings: list[str],
) -> bool:
    if not branch_exists(context.repo, context.run_branch):
        warnings.append("run branch was already absent")
        return True
    result = delete_branch(context.repo, context.run_branch, force=True)
    if result.returncode != 0:
        warnings.append(result.stderr.strip() or "run branch removal failed")
        return False
    return not branch_exists(context.repo, context.run_branch)
