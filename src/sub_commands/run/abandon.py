"""`cmoc run abandon` の workload 非依存 cleanup lifecycle。"""

import os
from pathlib import Path

from cmoc_runtime import (
    CmocError,
    RunPart,
    TerminalResult,
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
from commons.runtime_primary_report import update_primary_report_fields
from commons.runtime_run import (
    delete_run_process_id,
    read_run_process_id,
    run_lifecycle_lock,
    run_process_id_path,
    stop_error_run_process,
    stop_run_process,
    stop_tracked_codex_children,
    worktree_for_branch_optional,
)
from commons.runtime_run_lifecycle import EditingRunContext, resolve_active_run
from commons.runtime_run_report import write_lifecycle_report


def cmoc_run_abandon_impl() -> None:
    """CLI runtime を通して active editing run を破棄する。"""
    run_cli_subcommand(
        _cmoc_run_abandon_body,
        command_name="run abandon",
        command_argv=["cmoc", "run", "abandon"],
        doctor_preprocess=False,
        total_steps=4,
    )


def _cmoc_run_abandon_body() -> TerminalResult:
    """active run を停止し、worktree・branch・state を cleanup する。"""
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
        update_primary_report_fields(
            run_kind=context.kind,
            session_branch=context.session_branch,
            run_branch=context.run_branch,
            run_fork_commit=context.run_fork_commit,
            run_worktree=context.run_worktree,
            state_before=state.run.state,
            state_after=state.run.state,
        )
        require_clean_worktree(context.session_worktree)
        warnings: list[str] = []
        stopped = "not_running"
        if state.run.state == "running":
            stopped = _stop_running_run(context, warnings)
        elif state.run.state == "error":
            stopped = _stop_error_run(context, warnings)
        else:
            stopped = _stop_joinable_run(context, warnings)
        start_subcommand_step(3, "run worktree と branch を破棄", "cleanup run")
        if Path.cwd().resolve() == context.run_worktree.resolve():
            os.chdir(context.session_worktree)
        worktree_removed = _remove_run_worktree(context, warnings)
        # {{work-root}}/oracle/doc/app_spec/sub_command/editing_run.md
        # worktree が残った場合は branch を保持し、同じ managed target で cleanup を
        # 再試行できるようにする。
        branch_removed = (
            _remove_run_branch(context, warnings) if worktree_removed else False
        )
        if not worktree_removed or not branch_removed:
            update_primary_report_fields(
                process_stop=stopped,
                worktree_removed=worktree_removed,
                branch_removed=branch_removed,
                cleanup="failed",
            )
            raise CmocError(
                "active run の cleanup を完了できません。",
                ["git worktree list と run branch を確認して再実行してください。"],
                f"worktree_removed: {worktree_removed}\nbranch_removed: {branch_removed}",
                terminal_result=TerminalResult(warnings=tuple(warnings)),
            )
        state.run = RunPart()
        write_state(context.state_path, state)
        delete_run_process_id(context.repo, context.session_id)
        update_primary_report_fields(
            state_after="ready",
            process_stop=stopped,
            worktree_removed=worktree_removed,
            branch_removed=branch_removed,
            cleanup="completed",
        )
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
    start_subcommand_step(4, "terminal result を確定", "finalize terminal result")
    return TerminalResult(
        primary_report=report,
        primary_report_role="run abandon report",
        details=(
            ("run_kind", context.kind),
            ("run_branch", context.run_branch),
            ("run_worktree", context.run_worktree),
            ("process_stop", stopped),
            ("cleanup", "completed"),
        ),
        warnings=tuple(warnings),
    )


def _stop_running_run(
    context: EditingRunContext,
    warnings: list[str],
) -> str:
    """running run の追跡 process を停止し、警告を収集する。"""
    process = read_run_process_id(context.repo, context.session_id)
    if process is None:
        # {{work-root}}/oracle/doc/app_spec/sub_command/editing_run.md
        # running の process 停止を確認できないまま run 資源を破棄しない。
        tracking_path = run_process_id_path(context.repo, context.session_id)
        raise CmocError(
            "running run の process 停止を確認できません。",
            [
                "process tracking file と process の停止を確認してから再実行してください。",
            ],
            f"tracking path: {tracking_path}",
        )
    warning = stop_run_process(
        process,
        lambda: read_run_process_id(context.repo, context.session_id),
    )
    if warning:
        warnings.append(warning)
    return "stopped"


def _stop_error_run(
    context: EditingRunContext,
    warnings: list[str],
) -> str:
    """error state の残存 process を停止し、tracking を削除する。

    根拠: {{work-root}}/oracle/doc/app_spec/sub_command/editing_run.md
    """
    tracked, warning = stop_error_run_process(context.repo, context.session_id)
    if warning:
        warnings.append(warning)
    return "stopped" if tracked else "already_stopped"


def _stop_joinable_run(
    context: EditingRunContext,
    warnings: list[str],
) -> str:
    """joinable run に残った Codex child を cleanup 前に停止する。"""
    # {{work-root}}/oracle/doc/app_spec/run_isolation.md
    # joinable の通常経路では tracking file が消えるが、既存 state や中断後に
    # 残った descendant があれば run worktree の破棄前に停止する。
    tracked = read_run_process_id(context.repo, context.session_id)
    warnings.extend(stop_tracked_codex_children(context.repo, context.session_id) or [])
    return (
        "stopped" if tracked is not None and tracked.child_processes else "not_running"
    )


def _remove_run_worktree(
    context: EditingRunContext,
    warnings: list[str],
) -> bool:
    """active run の worktree を削除し、削除結果を返す。"""
    if not context.run_worktree.exists() and not context.run_worktree.is_symlink():
        warnings.append("run worktree was already absent")
        # {{work-root}}/oracle/doc/app_spec/sub_command/editing_run.md
        # Git の登録も消えている場合は、管理外 path として扱わず cleanup 済みとする。
        if (
            worktree_for_branch_optional(
                context.repo,
                context.run_branch,
                allow_missing=True,
            )
            is None
        ):
            return True
    result = remove_worktree(context.repo, context.run_worktree)
    if result.returncode != 0 and (
        context.run_worktree.exists() or context.run_worktree.is_symlink()
    ):
        warnings.append(result.stderr.strip() or "run worktree removal failed")
        return False
    return not context.run_worktree.exists() and not context.run_worktree.is_symlink()


def _remove_run_branch(
    context: EditingRunContext,
    warnings: list[str],
) -> bool:
    """active run の branch を強制削除し、削除結果を返す。"""
    if not branch_exists(context.repo, context.run_branch):
        warnings.append("run branch was already absent")
        return True
    result = delete_branch(context.repo, context.run_branch, force=True)
    if result.returncode != 0:
        warnings.append(result.stderr.strip() or "run branch removal failed")
        return False
    return not branch_exists(context.repo, context.run_branch)
