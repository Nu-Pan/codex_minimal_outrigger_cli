"""`cmoc run join` の workload 非依存 merge lifecycle。"""

import os
from pathlib import Path

import typer

from cmoc_runtime import (
    CmocError,
    RunPart,
    SessionState,
    branch_exists,
    delete_branch,
    head_commit,
    remove_worktree,
    require_clean_worktree,
    run_cli_subcommand,
    run_doctor_preprocess,
    run_git,
    start_subcommand_step,
    work_root,
    write_state,
)
from commons.runtime_refactor import sync_refactor_state
from commons.runtime_run import (
    delete_run_process_id,
    read_run_process_id,
    run_lifecycle_lock,
    stop_run_process,
)
from sub_commands.run.lifecycle import (
    EditingRunContext,
    commit_work_unit,
    refresh_indexes,
    resolve_active_run,
    tree_changes,
    unexpected_run_paths,
    unexpected_session_paths,
)
from sub_commands.run.report import write_lifecycle_report


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


def _cmoc_run_join_body(force_resolve: bool) -> None:
    start_subcommand_step(1, "doctor preprocess", "doctor preprocess")
    run_doctor_preprocess(work_root(), sync_refactor_entries=False)
    start_subcommand_step(2, "active run と差分を検査", "validate active run")
    initial_context, _ = resolve_active_run({"joinable", "error"})
    with run_lifecycle_lock(initial_context.repo, initial_context.session_id):
        context, state = resolve_active_run({"joinable", "error"})
        warnings: list[str] = []
        if state.run.state == "error":
            _stop_error_run(context, warnings)
        require_clean_worktree(context.session_worktree)
        require_clean_worktree(context.run_worktree)
        run_changes = tree_changes(
            context.run_worktree,
            context.run_fork_commit,
        )
        session_changes = tree_changes(
            context.session_worktree,
            context.run_fork_commit,
        )
        session_unexpected = unexpected_session_paths(
            context.session_worktree,
            session_changes,
        )
        if session_unexpected:
            _raise_unexpected(
                context,
                "session branch に想定外差分があります。",
                session_unexpected,
                warnings,
            )
        run_unexpected = unexpected_run_paths(context, run_changes)
        if run_unexpected and not force_resolve:
            _raise_unexpected(
                context,
                "run branch に想定外差分があります。",
                run_unexpected,
                warnings,
            )
        if run_unexpected:
            _revert_unexpected_run_paths(context, run_unexpected)
            warnings.append(
                "--force-resolve reverted unexpected run paths: "
                + ", ".join(run_unexpected)
            )
            run_changes = tree_changes(
                context.run_worktree,
                context.run_fork_commit,
            )
            remaining = unexpected_run_paths(context, run_changes)
            if remaining:
                _raise_unexpected(
                    context,
                    "run branch の想定外差分を解消できませんでした。",
                    remaining,
                    warnings,
                )
        session_head_before_join = head_commit(context.session_worktree)
        try:
            (
                run_join_commit,
                hook_result,
                state_sync_commit,
                cleanup,
                report,
            ) = _merge_and_finalize(context, state, warnings)
        except BaseException as exc:
            if getattr(exc, "cmoc_stdout", None) is not None:
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
            )
            setattr(error, "cmoc_stdout", f"- run join report: `{report}`")
            raise error from exc
    start_subcommand_step(6, "join 結果を表示", "show join result")
    typer.echo(
        "\n".join(
            [
                "# cmoc run join",
                f"- run_kind: `{context.kind}`",
                f"- run_branch: `{context.run_branch}`",
                f"- run_join_commit: `{run_join_commit}`",
                f"- post_join_hook: `{hook_result}`",
                f"- refactor_state_sync_commit: `{state_sync_commit}`",
                f"- cleanup: `{cleanup}`",
                f"- report: `{report}`",
            ]
        )
    )


def _merge_and_finalize(
    context: EditingRunContext,
    state: SessionState,
    warnings: list[str],
) -> tuple[str, str, str | None, str, Path]:
    """merge、hook、state 同期、結果保存、cleanup を一続きで確定する。"""
    start_subcommand_step(3, "run branch を session へ merge", "merge run")
    merge = run_git(
        ["merge", "--no-ff", context.run_branch],
        context.session_worktree,
        check=False,
    )
    if merge.returncode != 0:
        run_join_commit = _resolve_index_only_conflict_or_fail(context, state, warnings)
    else:
        run_join_commit = head_commit(context.session_worktree)
    start_subcommand_step(4, "post-join hook と state 同期", "run post-join")
    hook_result = "none"
    if context.kind == "realization_apply":
        state.session.last_joined_apply_fork_commit = context.run_fork_commit
        hook_result = f"session.last_joined_apply_fork_commit={context.run_fork_commit}"
    refresh_indexes(context.session_worktree, commit=True)
    sync_refactor_state(context.session_worktree)
    state_sync_commit = commit_work_unit(
        context.session_worktree,
        "cmoc refactor state sync after run join",
    )
    state.run = RunPart()
    write_state(context.state_path, state)
    delete_run_process_id(context.repo, context.session_id)
    start_subcommand_step(5, "結果を保存して run 資源を cleanup", "cleanup run")
    report = write_lifecycle_report(
        context,
        "join",
        state_after="ready",
        warnings=[*warnings, "cleanup pending"],
        details={
            "run_join_commit": run_join_commit,
            "post_join_hook": hook_result,
            "refactor_state_sync_commit": state_sync_commit,
            "cleanup": "pending",
        },
    )
    cleanup = _cleanup_joined_run(context, warnings)
    report = write_lifecycle_report(
        context,
        "join",
        state_after="ready",
        warnings=warnings,
        details={
            "run_join_commit": run_join_commit,
            "post_join_hook": hook_result,
            "refactor_state_sync_commit": state_sync_commit,
            "cleanup": cleanup,
        },
        report_path=report,
    )
    return run_join_commit, hook_result, state_sync_commit, cleanup, report


def _record_join_failure(
    context: EditingRunContext,
    state: SessionState,
    warnings: list[str],
    exc: BaseException,
    session_head_before_join: str,
) -> Path:
    """未確定 post-join 差分を除き、active run を error として report する。"""
    merge_head = run_git(
        ["rev-parse", "-q", "--verify", "MERGE_HEAD"],
        context.session_worktree,
        check=False,
    )
    if merge_head.returncode == 0:
        run_git(["merge", "--abort"], context.session_worktree, check=False)
    run_git(
        ["reset", "--hard", session_head_before_join],
        context.session_worktree,
    )
    run_git(["clean", "-fd"], context.session_worktree)
    state.run = RunPart(
        state="error",
        kind=context.kind,
        branch=context.run_branch,
        fork_commit=context.run_fork_commit,
    )
    write_state(context.state_path, state)
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
    )


def _stop_error_run(context: EditingRunContext, warnings: list[str]) -> None:
    process = read_run_process_id(context.repo, context.session_id)
    if process is None:
        warnings.append("run process tracking was absent or stale")
        delete_run_process_id(context.repo, context.session_id)
        return
    warning = stop_run_process(
        process,
        lambda: read_run_process_id(context.repo, context.session_id),
    )
    if warning:
        warnings.append(warning)
    delete_run_process_id(context.repo, context.session_id)


def _revert_unexpected_run_paths(
    context: EditingRunContext,
    paths: list[str],
) -> None:
    run_git(
        [
            "restore",
            "--source",
            context.run_fork_commit,
            "--staged",
            "--worktree",
            "--",
            *paths,
        ],
        context.run_worktree,
    )
    commit_work_unit(context.run_worktree, "cmoc run force resolve")


def _resolve_index_only_conflict_or_fail(
    context: EditingRunContext,
    state: SessionState,
    warnings: list[str],
) -> str:
    fields = run_git(
        ["diff", "--name-only", "-z", "--diff-filter=U"],
        context.session_worktree,
    ).stdout.split("\0")
    conflicts = [path for path in fields if path]
    if conflicts and all(Path(path).name == "INDEX.md" for path in conflicts):
        run_git(["checkout", "--ours", "--", *conflicts], context.session_worktree)
        run_git(["add", "--", *conflicts], context.session_worktree)
        run_git(["commit", "--no-edit"], context.session_worktree)
        merge_commit = head_commit(context.session_worktree)
        refresh_indexes(context.session_worktree, commit=True)
        warnings.append("INDEX.md conflicts were regenerated")
        return merge_commit
    run_git(["merge", "--abort"], context.session_worktree, check=False)
    state.run.state = "error"
    write_state(context.state_path, state)
    report = write_lifecycle_report(
        context,
        "join",
        state_after="error",
        warnings=warnings,
        details={
            "run_join_commit": None,
            "post_join_hook": "not_run",
            "refactor_state_sync_commit": None,
            "cleanup": "not_run",
            "conflict_paths": ", ".join(conflicts),
        },
    )
    error = CmocError(
        "INDEX.md 以外の merge conflict が発生しました。",
        ["run report を確認し、run を join または abandon してください。"],
        "\n".join(conflicts) or "merge failed without unmerged paths",
    )
    setattr(error, "cmoc_stdout", f"- run join report: `{report}`")
    raise error


def _cleanup_joined_run(
    context: EditingRunContext,
    warnings: list[str],
) -> str:
    reachable = (
        run_git(
            [
                "merge-base",
                "--is-ancestor",
                context.run_branch,
                context.session_branch,
            ],
            context.session_worktree,
            check=False,
        ).returncode
        == 0
    )
    if not reachable:
        warnings.append("run branch is not reachable from session branch")
        return "preserved"
    if Path.cwd().resolve() == context.run_worktree.resolve():
        os.chdir(context.session_worktree)
    removal = remove_worktree(context.repo, context.run_worktree)
    if removal.returncode != 0 and context.run_worktree.exists():
        warnings.append("run worktree cleanup failed")
        return "preserved"
    if branch_exists(context.repo, context.run_branch):
        deletion = delete_branch(context.repo, context.run_branch)
        if deletion.returncode != 0:
            warnings.append("run branch cleanup failed")
            return "branch_preserved"
    return "completed"


def _raise_unexpected(
    context: EditingRunContext,
    summary: str,
    paths: list[str],
    warnings: list[str],
) -> None:
    report = write_lifecycle_report(
        context,
        "join",
        state_after=context.state_before,
        warnings=warnings,
        details={
            "run_join_commit": None,
            "post_join_hook": "not_run",
            "refactor_state_sync_commit": None,
            "cleanup": "not_run",
            "unexpected_paths": ", ".join(paths),
        },
    )
    error = CmocError(
        summary,
        [
            "run branch のみを自動修復する場合は `cmoc run join --force-resolve` を実行してください。",
            "session branch の成果物は手動で確認してください。",
        ],
        "\n".join(paths),
    )
    setattr(error, "cmoc_stdout", f"- run join report: `{report}`")
    raise error
