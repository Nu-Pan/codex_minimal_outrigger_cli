"""`cmoc run join` の workload 非依存 merge lifecycle。

この file は 16,000 文字を超えるが、差分検査、merge、post-join state 同期、report、
cleanup は同じ active run の状態と failure rollback を共有する一つの責務である。
分割すると、join の成功・失敗・cleanup pending の不変条件を複数 file で追う必要が
生じるため、現状は run join lifecycle として一箇所に保つ。

根拠: {{work-root}}/oracle/doc/app_spec/oracle_and_realization.md の
「realization file を扱う判断基準」
"""

from dataclasses import replace
from pathlib import Path

import commons.runtime_run_join as runtime_run_join
from cmoc_runtime import (
    CmocError,
    RunPart,
    SessionState,
    TerminalResult,
    head_commit,
    run_cli_subcommand,
    start_subcommand_step,
    work_root,
    write_state,
)
from commons.runtime_primary_report import update_primary_report_fields
from commons.runtime_run import (
    delete_run_process_id,
    run_lifecycle_lock,
    stop_error_run_process,
    stop_tracked_codex_children,
)
from commons.runtime_run_lifecycle import (
    EditingRunContext,
    resolve_active_run,
)
from commons.runtime_run_report import write_lifecycle_report


def cmoc_run_join_impl(force_resolve: bool = False) -> None:
    """CLI runtime を通して active editing run を join する。"""
    run_cli_subcommand(
        _cmoc_run_join_body,
        force_resolve,
        command_name="run join",
        command_argv=[
            "cmoc",
            "run",
            "join",
            *(["--force-resolve"] if force_resolve else []),
        ],
        doctor_preprocess=False,
        total_steps=6,
    )


def _cmoc_run_join_body(force_resolve: bool) -> TerminalResult:
    """active run の差分を検査して merge、post-join 処理、cleanup を行う。"""
    start_subcommand_step(1, "doctor preprocess", "doctor preprocess")
    doctor_state_paths = runtime_run_join.doctor_preprocess_for_join()
    start_subcommand_step(2, "active run と差分を検査", "validate active run")
    initial_context, _ = resolve_active_run({"joinable", "error"})
    with run_lifecycle_lock(initial_context.repo, initial_context.session_id):
        context, state = resolve_active_run({"joinable", "error"})
        from sub_commands.feedback.recovery import require_manual_feedback_run

        require_manual_feedback_run(context)
        update_primary_report_fields(
            run_kind=context.kind,
            session_branch=context.session_branch,
            run_branch=context.run_branch,
            run_fork_commit=context.run_fork_commit,
            run_worktree=context.run_worktree,
            state_before=state.run.state,
            state_after=state.run.state,
        )
        warnings: list[str] = []
        current_worktree = work_root().resolve()
        session_doctor_state_paths = (
            doctor_state_paths
            if current_worktree == context.session_worktree.resolve()
            else set()
        )
        run_doctor_state_paths = (
            doctor_state_paths
            if current_worktree == context.run_worktree.resolve()
            else set()
        )
        if state.run.state == "error":
            _stop_error_run(context, warnings)
        elif state.run.state == "joinable":
            # {{work-root}}/oracle/doc/app_spec/run_isolation.md
            # 既存 state の復旧でも、merge 前に run worktree の descendant を止める。
            warnings.extend(
                stop_tracked_codex_children(context.repo, context.session_id) or []
            )
        runtime_run_join.validate_run_join(
            context,
            warnings,
            force_resolve=force_resolve,
            session_ignored_paths=session_doctor_state_paths,
            run_ignored_paths=run_doctor_state_paths,
        )
        session_head_before_join = head_commit(context.session_worktree)
        try:
            (
                run_join_commit,
                hook_result,
                state_sync_commit,
                cleanup,
                report,
            ) = _merge_and_finalize(
                context,
                state,
                warnings,
                session_head_before_join,
            )
            update_primary_report_fields(
                run_join_commit=run_join_commit,
                post_join_hook=hook_result,
                refactor_state_sync_commit=state_sync_commit,
                cleanup=cleanup,
                state_after="ready" if cleanup == "completed" else "error",
            )
        except BaseException as exc:
            if isinstance(getattr(exc, "terminal_result", None), TerminalResult):
                raise
            report = _record_join_failure(
                context,
                state,
                warnings,
                exc,
                session_head_before_join,
            )
            error = CmocError(
                "run join の merge または post-join 処理に失敗しました。",
                ["run join report を確認してから join または abandon してください。"],
                f"report: {report}\nerror: {exc!r}",
                terminal_result=TerminalResult(
                    primary_report=report,
                    primary_report_role="run join report",
                    warnings=tuple(warnings),
                ),
            )
            raise error from exc
    start_subcommand_step(6, "terminal result を確定", "finalize terminal result")
    next_actions = (
        ("`cmoc run abandon` で残った run 資源の cleanup を再試行してください。",)
        if cleanup != "completed"
        else ()
    )
    return TerminalResult(
        primary_report=report,
        primary_report_role="run join report",
        details=(
            ("run_kind", context.kind),
            ("run_branch", context.run_branch),
            ("run_join_commit", run_join_commit),
            ("post_join_hook", hook_result),
            ("refactor_state_sync_commit", state_sync_commit),
            ("cleanup", cleanup),
        ),
        next_actions=next_actions,
        warnings=tuple(warnings),
    )


def _merge_and_finalize(
    context: EditingRunContext,
    state: SessionState,
    warnings: list[str],
    session_head_before_join: str,
) -> tuple[str | None, str, str | None, str, Path]:
    """merge、hook、state 同期、結果保存、cleanup を一続きで確定する。"""
    run_join_commit, hook_result, state_sync_commit, last_joined_apply_fork_commit = (
        runtime_run_join.merge_run(
            context,
            state,
            warnings,
            session_head_before_join,
        )
    )
    if context.kind == "feedback_report":
        from sub_commands.feedback.recovery import finish_manual_feedback_run

        finish_manual_feedback_run(context, "joined")
    state_after_join = replace(
        state,
        session=replace(
            state.session,
            last_joined_apply_fork_commit=last_joined_apply_fork_commit,
        ),
        run=RunPart(),
    )
    write_state(context.state_path, state_after_join)
    delete_run_process_id(context.repo, context.session_id)
    start_subcommand_step(5, "結果を保存して run 資源を cleanup", "cleanup run")
    cleanup = runtime_run_join.cleanup_joined_run(context, warnings)
    state_after_cleanup = "ready"
    if cleanup != "completed":
        # {{work-root}}/oracle/doc/app_spec/sub_command/editing_run.md
        # cleanup できない run resource を保持したまま ready にすると active run の
        # branch/worktree を state から再解決できず、後続の abandon も受け付けられない。
        # merge 済み成果物は session branch に残し、run resource は error state として
        # abandon で再試行できるようにする。
        state_after_cleanup = "error"
        write_state(
            context.state_path,
            replace(
                state_after_join,
                run=RunPart(
                    state="error",
                    kind=context.kind,
                    branch=context.run_branch,
                    fork_commit=context.run_fork_commit,
                ),
            ),
        )
        delete_run_process_id(context.repo, context.session_id)
    update_primary_report_fields(
        run_join_commit=run_join_commit,
        post_join_hook=hook_result,
        refactor_state_sync_commit=state_sync_commit,
        cleanup=cleanup,
        state_after=state_after_cleanup,
    )
    try:
        report = write_lifecycle_report(
            context,
            "join",
            state_after=state_after_cleanup,
            warnings=warnings,
            details={
                "run_join_commit": run_join_commit,
                "post_join_hook": hook_result,
                "refactor_state_sync_commit": state_sync_commit,
                "cleanup": cleanup,
            },
        )
    except BaseException as report_error:
        # {{work-root}}/oracle/doc/app_spec/sub_command/editing_run.md
        # merge、ready state、cleanup が完了した後の report 保存失敗で、確定済み
        # merge を rollback し、唯一の復旧可能な run commit を失わせてはいけない。
        update_primary_report_fields(
            run_join_commit=run_join_commit,
            post_join_hook=hook_result,
            refactor_state_sync_commit=state_sync_commit,
            cleanup=cleanup,
            state_after=state_after_cleanup,
            report_update="failed",
        )
        raise CmocError(
            "run join report の最終状態を保存できませんでした。",
            ["診断用サブコマンドログを確認してください。"],
            repr(report_error),
            terminal_result=TerminalResult(),
        ) from report_error
    return run_join_commit, hook_result, state_sync_commit, cleanup, report


def _record_join_failure(
    context: EditingRunContext,
    state: SessionState,
    warnings: list[str],
    exc: BaseException,
    session_head_before_join: str,
) -> Path:
    """未確定 post-join 差分を除き、active run を error として report する。"""
    runtime_run_join.restore_session_after_join_failure(
        context, session_head_before_join
    )
    state.run = RunPart(
        state="error",
        kind=context.kind,
        branch=context.run_branch,
        fork_commit=context.run_fork_commit,
    )
    write_state(context.state_path, state)
    update_primary_report_fields(
        state_after="error",
        run_join_commit=None,
        post_join_hook="error",
        cleanup="not_run",
        error=repr(exc),
    )
    return write_lifecycle_report(
        context,
        "join",
        state_after="error",
        warnings=warnings,
        details={
            "run_join_commit": None,
            "post_join_hook": "error",
            "refactor_state_sync_commit": None,
            "cleanup": "not_run",
            "error": repr(exc),
        },
        terminal_classification="error",
        exit_code=1,
    )


def _stop_error_run(context: EditingRunContext, warnings: list[str]) -> None:
    """error state の run process tracking を停止して削除する。"""
    _tracked, warning = stop_error_run_process(context.repo, context.session_id)
    if warning:
        warnings.append(warning)
