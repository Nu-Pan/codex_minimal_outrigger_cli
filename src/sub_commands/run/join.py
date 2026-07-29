"""`cmoc run join` の workload 非依存 merge lifecycle。

この file は 16,000 文字を超えるが、差分検査、merge、post-join state 同期、report、
cleanup は同じ active run の状態と failure rollback を共有する一つの責務である。
分割すると、join の成功・失敗・cleanup pending の不変条件を複数 file で追う必要が
生じるため、現状は run join lifecycle として一箇所に保つ。

根拠: {{work-root}}/oracle/src/oracle/prompt_builder/parts/realization_standard.py
"""

import os
from dataclasses import replace
from pathlib import Path

import typer

from cmoc_runtime import (
    CmocError,
    RunPart,
    SessionState,
    branch_exists,
    current_branch,
    delete_branch,
    head_commit,
    load_state_for_branch,
    refactor_state_path,
    remove_worktree,
    repo_root,
    require_clean_worktree,
    run_cli_subcommand,
    run_doctor_preprocess,
    run_git,
    start_subcommand_step,
    work_root,
    write_state,
)
from commons.runtime_git import literal_pathspec
from commons.runtime_refactor import sync_refactor_state
from commons.runtime_run import (
    delete_run_process_id,
    run_lifecycle_lock,
    run_process_tracking,
    stop_error_run_process,
    stop_tracked_codex_children,
    write_run_process_id,
)
from commons.runtime_run_lifecycle import (
    EditingRunContext,
    commit_work_unit,
    refresh_indexes,
    resolve_active_run,
    tree_changes,
    unexpected_run_paths,
    unexpected_session_paths,
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


def _cmoc_run_join_body(force_resolve: bool) -> None:
    """active run の差分を検査して merge、post-join 処理、cleanup を行う。"""
    start_subcommand_step(1, "doctor preprocess", "doctor preprocess")
    doctor_state_paths = _doctor_preprocess_for_join()
    start_subcommand_step(2, "active run と差分を検査", "validate active run")
    initial_context, _ = resolve_active_run({"joinable", "error"})
    with run_lifecycle_lock(initial_context.repo, initial_context.session_id):
        context, state = resolve_active_run({"joinable", "error"})
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
            ignored_paths=session_doctor_state_paths,
        )
        if session_unexpected:
            _raise_unexpected(
                context,
                "session branch に想定外差分があります。",
                session_unexpected,
                warnings,
            )
        run_unexpected = unexpected_run_paths(
            context,
            run_changes,
            ignored_paths=run_doctor_state_paths,
        )
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
            remaining = unexpected_run_paths(
                context,
                run_changes,
                ignored_paths=run_doctor_state_paths,
            )
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
            ) = _merge_and_finalize(
                context,
                state,
                warnings,
                session_head_before_join,
            )
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


def _doctor_preprocess_for_join() -> set[str]:
    """join 前の refactor state 同期を active run kind に合わせる。"""
    root = work_root()
    before = head_commit(root)
    sync_refactor_entries = True
    try:
        branch = current_branch(root)
        _, _, state = load_state_for_branch(repo_root(root), branch)
    except CmocError:
        # active run の詳細な事前条件は doctor 後の resolve_active_run で報告する。
        pass
    else:
        # {{work-root}}/oracle/doc/app_spec/doctor_preprocess.md
        # merge 前の entry 同期遅延は refactor run だけに限定する。
        sync_refactor_entries = state.run.kind != "realization_refactor"
    run_doctor_preprocess(root, sync_refactor_entries=sync_refactor_entries)
    after = head_commit(root)
    if before == after:
        return set()
    # {{work-root}}/oracle/doc/app_spec/doctor_preprocess.md
    # doctor 自身が merge 前に同期した refactor state だけを session の差分から除外する。
    refactor_state = refactor_state_path(root).relative_to(root)
    return {
        path
        for change in tree_changes(root, before, after)
        for path in change.paths
        if Path(path) == refactor_state
    }


def _merge_and_finalize(
    context: EditingRunContext,
    state: SessionState,
    warnings: list[str],
    session_head_before_join: str,
) -> tuple[str, str, str | None, str, Path]:
    """merge、hook、state 同期、結果保存、cleanup を一続きで確定する。"""
    start_subcommand_step(3, "run branch を session へ merge", "merge run")
    merge = run_git(
        ["merge", "--no-ff", context.run_branch],
        context.session_worktree,
        check=False,
    )
    if merge.returncode != 0:
        run_join_commit = _resolve_index_only_conflict_or_fail(
            context,
            state,
            warnings,
            session_head_before_join,
        )
    else:
        run_join_commit = head_commit(context.session_worktree)
    start_subcommand_step(4, "post-join hook と state 同期", "run post-join")
    hook_result = "none"
    # {{work-root}}/oracle/doc/app_spec/session_state.md
    # post-join 処理の失敗時は merge を戻して error state にするため、成功確定まで
    # last_joined_apply_fork_commit を state object へ書き戻さない。
    last_joined_apply_fork_commit = state.session.last_joined_apply_fork_commit
    if context.kind == "realization_apply":
        last_joined_apply_fork_commit = context.run_fork_commit
        # {{work-root}}/oracle/doc/app_spec/sub_command/editing_run.md
        # common の run_fork_commit と同じ commit を workload 固有名で重複掲載しない。
        hook_result = "session.last_joined_apply_fork_commit updated"
    _refresh_join_indexes(context, warnings)
    sync_refactor_state(context.session_worktree)
    state_sync_commit = commit_work_unit(
        context.session_worktree,
        "cmoc refactor state sync after run join",
    )
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


def _refresh_join_indexes(
    context: EditingRunContext,
    warnings: list[str],
) -> None:
    """post-merge の INDEX 生成を追跡し、INDEX 外の副作用を拒否する。"""
    # {{work-root}}/oracle/doc/app_spec/run_isolation.md
    # join 自身が起動する Codex も run process tracking に登録し、descendant が
    # session worktree を変更し続ける競合を止めてから clean 状態を検査する。
    with run_process_tracking(context.repo, context.session_id):
        write_run_process_id(context.repo, context.session_id, os.getpid())
        try:
            refresh_indexes(context.session_worktree, commit=True)
        finally:
            try:
                warnings.extend(
                    stop_tracked_codex_children(context.repo, context.session_id) or []
                )
            finally:
                delete_run_process_id(context.repo, context.session_id)
    # INDEX commit が拾わない Codex の副作用を state sync commit へ混入させない。
    require_clean_worktree(context.session_worktree)


def _record_join_failure(
    context: EditingRunContext,
    state: SessionState,
    warnings: list[str],
    exc: BaseException,
    session_head_before_join: str,
) -> Path:
    """未確定 post-join 差分を除き、active run を error として report する。"""
    _restore_session_after_join_failure(context, session_head_before_join)
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


def _restore_session_after_join_failure(
    context: EditingRunContext,
    session_head_before_join: str,
) -> None:
    """merge/post-join 失敗後に session worktree を開始時点へ戻す。"""
    merge_head = run_git(
        ["rev-parse", "-q", "--verify", "MERGE_HEAD"],
        context.session_worktree,
        check=False,
    )
    if merge_head.returncode == 0:
        run_git(["merge", "--abort"], context.session_worktree, check=False)
    # {{work-root}}/oracle/doc/app_spec/sub_command/editing_run.md
    # merge --abort が失敗しても、join 開始前の clean tree へ戻せなければ
    # error state から join/abandon を再実行できない。
    run_git(["reset", "--hard", session_head_before_join], context.session_worktree)
    run_git(["clean", "-fd"], context.session_worktree)


def _stop_error_run(context: EditingRunContext, warnings: list[str]) -> None:
    """error state の run process tracking を停止して削除する。"""
    _tracked, warning = stop_error_run_process(context.repo, context.session_id)
    if warning:
        warnings.append(warning)


def _revert_unexpected_run_paths(
    context: EditingRunContext,
    paths: list[str],
) -> None:
    """force-resolve 対象の想定外 path を fork commit へ戻して commit する。"""
    # {{work-root}}/oracle/doc/app_spec/sub_command/editing_run.md
    # Git pathspec の wildcard 解釈で別 path を巻き込まないよう、検出済み
    # repository path を literal として指定する。
    run_git(
        [
            "restore",
            "--source",
            context.run_fork_commit,
            "--staged",
            "--worktree",
            "--",
            *[literal_pathspec(path) for path in paths],
        ],
        context.run_worktree,
    )
    commit_work_unit(context.run_worktree, "cmoc run force resolve")


def _resolve_index_only_conflict_or_fail(
    context: EditingRunContext,
    state: SessionState,
    warnings: list[str],
    session_head_before_join: str,
) -> str:
    """INDEX.md だけの conflict を再生成し、それ以外は error report へ移す。"""
    fields = run_git(
        ["diff", "--name-only", "-z", "--diff-filter=U"],
        context.session_worktree,
    ).stdout.split("\0")
    conflicts = [path for path in fields if path]
    if conflicts and all(Path(path).name == "INDEX.md" for path in conflicts):
        for path in conflicts:
            if _has_ours_conflict_stage(context.session_worktree, path):
                run_git(
                    ["checkout", "--ours", "--", literal_pathspec(path)],
                    context.session_worktree,
                )
                run_git(
                    ["add", "--", literal_pathspec(path)],
                    context.session_worktree,
                )
            else:
                # {{work-root}}/oracle/doc/app_spec/sub_command/editing_run.md
                # session 側で削除された INDEX.md には ours stage がないため、削除を
                # stage してから再生成処理へ渡す。
                run_git(
                    ["rm", "-f", "--", literal_pathspec(path)],
                    context.session_worktree,
                )
        run_git(["commit", "--no-edit"], context.session_worktree)
        merge_commit = head_commit(context.session_worktree)
        _refresh_join_indexes(context, warnings)
        warnings.append("INDEX.md conflicts were regenerated")
        return merge_commit
    _restore_session_after_join_failure(context, session_head_before_join)
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


def _has_ours_conflict_stage(root: Path, path: str) -> bool:
    """unmerged path に session 側の stage 2 が存在するか判定する。"""
    fields = run_git(
        ["ls-files", "-u", "-z", "--", literal_pathspec(path)], root
    ).stdout.split("\0")
    for field in fields:
        metadata, separator, _path = field.partition("\t")
        if separator and len(metadata.split()) >= 3 and metadata.split()[2] == "2":
            return True
    return False


def _cleanup_joined_run(
    context: EditingRunContext,
    warnings: list[str],
) -> str:
    """merge 済み run の worktree と branch を安全条件付きで削除する。"""
    try:
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
    except Exception:
        warnings.append("run branch reachability check failed")
        return "preserved"
    if not reachable:
        warnings.append("run branch is not reachable from session branch")
        return "preserved"
    if Path.cwd().resolve() == context.run_worktree.resolve():
        try:
            os.chdir(context.session_worktree)
        except Exception:
            warnings.append("run worktree cleanup failed")
            return "preserved"
    try:
        removal = remove_worktree(context.repo, context.run_worktree)
    except Exception:
        warnings.append("run worktree cleanup failed")
        return "preserved"
    if (
        removal.returncode != 0
        or context.run_worktree.exists()
        or context.run_worktree.is_symlink()
    ):
        warnings.append("run worktree cleanup failed")
        return "preserved"
    try:
        branch_present = branch_exists(context.repo, context.run_branch)
    except Exception:
        warnings.append("run branch cleanup failed")
        return "branch_preserved"
    if branch_present:
        try:
            deletion = delete_branch(context.repo, context.run_branch)
            branch_present = deletion.returncode != 0 or branch_exists(
                context.repo, context.run_branch
            )
        except Exception:
            warnings.append("run branch cleanup failed")
            return "branch_preserved"
        if branch_present:
            warnings.append("run branch cleanup failed")
            return "branch_preserved"
    return "completed"


def _raise_unexpected(
    context: EditingRunContext,
    summary: str,
    paths: list[str],
    warnings: list[str],
) -> None:
    """想定外差分を report に記録して join failure として送出する。"""
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
