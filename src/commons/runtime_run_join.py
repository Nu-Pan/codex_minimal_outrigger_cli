"""editing run の join と cleanup で共有する runtime 処理。"""

import os
from collections.abc import Callable, Collection, Mapping
from dataclasses import replace
from pathlib import Path

from .runtime_cli import start_subcommand_step
from .runtime_doctor import run_doctor_preprocess
from .runtime_errors import CmocError
from .runtime_git import (
    branch_exists,
    current_branch,
    delete_branch,
    head_commit,
    literal_pathspec,
    remove_worktree,
    require_clean_worktree,
    run_git,
)
from .runtime_merge_conflict import resolve_merge_conflicts
from .runtime_paths import repo_root, work_root
from .runtime_primary_report import (
    current_primary_report_fields,
    primary_report_finalization_lock,
    set_primary_report_save_failure_handler,
    update_primary_report_fields,
)
from .runtime_primary_report_specs import TerminalClassification
from .runtime_refactor import sync_refactor_state
from .runtime_results import TerminalResult
from .runtime_run import (
    delete_run_process_id,
    run_lifecycle_lock,
    run_process_tracking,
    stop_error_run_process,
    stop_tracked_codex_children,
    write_run_process_id,
)
from .runtime_run_lifecycle import (
    EditingRunContext,
    GitChange,
    commit_work_unit,
    resolve_active_run,
    tree_changes,
    unexpected_run_paths,
)
from .runtime_run_report import write_lifecycle_report
from .runtime_state import RunPart, SessionState, load_state_for_branch, write_state


def doctor_preprocess_changes_for_join() -> dict[Path, tuple[str, set[str]]]:
    """join 前 doctor の修復 path を修復した worktree ごとに返す。"""
    # 修復 path の記録が必要な join で、doctor 前後の HEAD を照会する。
    root = work_root().resolve()
    main_root = repo_root(root).resolve()
    repair_roots = (main_root,) if main_root == root else (main_root, root)
    before = {repair_root: head_commit(repair_root) for repair_root in repair_roots}
    _run_join_doctor(root, main_root)
    # doctor は linked run 起点でも main worktree と current worktree の両方を修復
    # する。修復 path を一つの集合へ潰すと、session 側の commit を run 側の修復
    # と誤って扱うため、各 worktree の HEAD 差分を所有 root ごとに保持する。
    changes: dict[Path, tuple[str, set[str]]] = {}
    for repair_root, before_commit in before.items():
        after_commit = head_commit(repair_root)
        changes[repair_root] = (
            before_commit,
            {
                path
                for change in tree_changes(repair_root, before_commit, after_commit)
                for path in change.paths
            }
            if before_commit != after_commit
            else set(),
        )
    return changes


def doctor_paths_for_join(
    changes: Mapping[Path, tuple[str, Collection[str]]],
    worktree: Path,
    base: str,
) -> set[str]:
    """doctor が追加した path だけを join の差分除外対象へ取り出す。"""
    # 修復 path がなければ除外対象もなく、先行差分の Git 照会は不要。
    repair = changes.get(worktree.resolve())
    if repair is None or not repair[1]:
        return set()
    before_commit, doctor_paths = repair
    preexisting_paths = {
        path
        for change in tree_changes(worktree, base, before_commit)
        for path in change.paths
    }
    # doctor と同じ path に先行する session/run 差分がある場合は、path 全体を
    # 管理差分として扱わず、ユーザーまたは workload の差分検査を維持する。
    return set(doctor_paths).difference(preexisting_paths)


def doctor_preprocess_for_join(*, rollback_on_interruption: bool = False) -> None:
    """修復 path の記録が不要な workload の join 前 doctor を実行する。"""
    # feedback は修復差分を除外しないため、HEAD と変更 path の取得を省く。
    root = work_root().resolve()
    _run_join_doctor(
        root, repo_root(root), rollback_on_interruption=rollback_on_interruption
    )


def _run_join_doctor(
    root: Path, main_root: Path, *, rollback_on_interruption: bool = False
) -> None:
    """active run の kind に合わせて、doctor の entry 同期時点を選ぶ。"""
    # join 前の state を確認し、workload が更新する state の二重同期を避ける。
    sync_refactor_entries = True
    try:
        branch = current_branch(root)
        _, _, state = load_state_for_branch(main_root, branch)
    except CmocError:
        # active run の詳細な事前条件は doctor 後の resolve_active_run で報告する。
        pass
    else:
        # merge 前の entry 同期は refactor state を更新する run で遅延する。
        sync_refactor_entries = state.run.kind not in {
            "realization_refactor",
            "feedback_report",
        }
    if rollback_on_interruption:
        run_doctor_preprocess(
            root,
            sync_refactor_entries=sync_refactor_entries,
            rollback_on_interruption=True,
        )
    else:
        run_doctor_preprocess(root, sync_refactor_entries=sync_refactor_entries)


def validate_run_join(
    context: EditingRunContext,
    warnings: list[str],
    *,
    force_resolve: bool = False,
    run_ignored_paths: Collection[str] = (),
) -> None:
    """明示 join と self-joining workload が共有する clean・差分検査を行う。"""
    # session と run の両 worktree を clean にし、fork 以後の差分を分類する。
    require_clean_worktree(context.session_worktree)
    require_clean_worktree(context.run_worktree)
    run_changes = tree_changes(
        context.run_worktree,
        context.run_fork_commit,
    )
    # session 側の commit 済み変更は file 種別を問わず統合対象にする。
    run_unexpected = unexpected_run_paths(
        context,
        run_changes,
        ignored_paths=run_ignored_paths,
    )
    if run_unexpected and not force_resolve:
        _raise_unexpected(
            context,
            "run branch に想定外差分があります。",
            run_unexpected,
            warnings,
        )
    if run_unexpected:
        # force-resolve は run branch の想定外差分だけを fork commit へ戻す。
        _revert_unexpected_run_paths(context, run_changes, run_unexpected)
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
            ignored_paths=run_ignored_paths,
        )
        if remaining:
            _raise_unexpected(
                context,
                "run branch の想定外差分を解消できませんでした。",
                remaining,
                warnings,
            )


def merge_run(
    context: EditingRunContext,
    state: SessionState,
    warnings: list[str],
    session_head_before_join: str,
    *,
    on_merged: Callable[[str | None, dict[str, object]], None] | None = None,
    feedback_report_cut_path: Path | None = None,
) -> tuple[str | None, str, str | None, str | None, dict[str, object]]:
    """merge 前の失敗は開始時へ戻し、commit 後は未確定作業差分だけ除く。"""
    try:
        return _merge_run_body(
            context,
            state,
            warnings,
            session_head_before_join,
            on_merged=on_merged,
            feedback_report_cut_path=feedback_report_cut_path,
        )
    except BaseException as error:
        try:
            warnings.extend(
                stop_tracked_codex_children(context.repo, context.session_id) or []
            )
        except BaseException as stop_error:
            update_primary_report_fields(
                merge_rollback="not_run",
                process_stop="unconfirmed",
                stop_error=repr(stop_error),
            )
            raise CmocError(
                "join の子 process の停止を確認できません。",
                ["process の停止を確認してから作業差分を復旧してください。"],
                f"stop: {stop_error!r}\nerror: {error!r}",
            ) from error
        update_primary_report_fields(process_stop="confirmed")
        try:
            if head_commit(context.session_worktree) == session_head_before_join:
                restore_session_after_join_failure(context, session_head_before_join)
            else:
                run_git(["reset", "--hard", "HEAD"], context.session_worktree)
                run_git(["clean", "-fd"], context.session_worktree)
        except BaseException as rollback_error:
            update_primary_report_fields(
                merge_rollback="failed", merge_rollback_error=repr(rollback_error)
            )
            raise CmocError(
                "join の作業差分を復旧できませんでした。",
                ["残存資源と差分を確認して復旧してください。"],
                f"error: {error!r}\nrollback: {rollback_error!r}",
            ) from rollback_error
        update_primary_report_fields(
            merge_rollback="completed", process_stop="confirmed"
        )
        delete_run_process_id(context.repo, context.session_id)
        raise


def _merge_run_body(
    context: EditingRunContext,
    state: SessionState,
    warnings: list[str],
    session_head_before_join: str,
    *,
    on_merged: Callable[[str | None, dict[str, object]], None] | None = None,
    feedback_report_cut_path: Path | None = None,
) -> tuple[str | None, str, str | None, str | None, dict[str, object]]:
    """共通 merge と post-join を行い、state 初期化と資源 cleanup は呼出元に残す。"""
    # merge の結果を確定し、workload 固有の state 初期化は呼出元へ返す。
    run_join_commit: str | None
    resolution: dict[str, object] = {
        "agent_status": "not_needed",
        "initial_conflicts": [],
    }
    start_subcommand_step(3, "run branch を session へ merge", "merge run")
    update_primary_report_fields(join_phase="merge")
    merge = run_git(
        ["merge", "--no-ff", context.run_branch],
        context.session_worktree,
        check=False,
    )
    if merge.returncode != 0:
        from oracle.acp_builder.run.join.conflict_resolution import (
            build_run_join_conflict_resolution_parameter,
        )

        run_head = head_commit(context.run_worktree)
        write_run_process_id(context.repo, context.session_id, os.getpid())
        with run_process_tracking(context.repo, context.session_id):
            resolution = resolve_merge_conflicts(
                context.session_worktree,
                build_run_join_conflict_resolution_parameter(
                    run_head,
                    session_head_before_join,
                    context.session_worktree,
                    feedback_report_cut_path=feedback_report_cut_path,
                ),
                purpose="run join conflict resolution",
                before_commit=lambda: warnings.extend(
                    stop_tracked_codex_children(context.repo, context.session_id) or []
                ),
            )
        run_join_commit = head_commit(context.session_worktree)
    else:
        merged_head = head_commit(context.session_worktree)
        run_join_commit = (
            merged_head if merged_head != session_head_before_join else None
        )
    update_primary_report_fields(
        merge_status="merged" if run_join_commit is not None else "no_op",
        run_join_commit=run_join_commit,
        conflict_resolution=resolution,
    )
    if on_merged is not None:
        on_merged(run_join_commit, resolution)
    # merge 後の共通 hook と state 同期を実行する。
    start_subcommand_step(4, "post-join hook と state 同期", "run post-join")
    update_primary_report_fields(join_phase="post-join hook")
    hook_result = "none"
    # 確定前の state object へ比較始点を書き戻さない。
    last_joined_apply_fork_commit = state.session.last_joined_apply_fork_commit
    if context.kind == "realization_apply":
        # lock 内で対象 run を確定した時点の state を使い、error run の比較始点を保つ。
        hook_result = "session.last_joined_apply_fork_commit preserved"
        if context.state_before == "joinable":
            last_joined_apply_fork_commit = context.run_fork_commit
            hook_result = "session.last_joined_apply_fork_commit updated"
            # 取り込みが確定した時点で資格を保存し、後段の失敗で元に戻さない。
            write_state(
                context.state_path,
                replace(
                    state,
                    session=replace(
                        state.session,
                        last_joined_apply_fork_commit=last_joined_apply_fork_commit,
                    ),
                ),
            )
    update_primary_report_fields(
        post_join_hook=hook_result,
        refactor_state_sync_status="started",
        join_phase="refactor state sync",
    )
    try:
        sync_refactor_state(context.session_worktree)
        state_sync_commit = commit_work_unit(
            context.session_worktree,
            "cmoc refactor state sync after run join",
        )
        update_primary_report_fields(
            refactor_state_sync_status="completed",
            refactor_state_sync_commit=state_sync_commit,
        )
    except BaseException as exc:
        update_primary_report_fields(refactor_state_sync_status="failed")
        setattr(exc, "_merge_resolution", resolution)
        setattr(exc, "_merge_commit", run_join_commit)
        setattr(exc, "_post_join_hook", hook_result)
        raise
    return (
        run_join_commit,
        hook_result,
        state_sync_commit,
        last_joined_apply_fork_commit,
        resolution,
    )


def _revert_unexpected_run_paths(
    context: EditingRunContext,
    changes: list[GitChange],
    unexpected_paths: list[str],
) -> None:
    """force-resolve 対象の変更を fork commit へ戻して commit する。"""
    # 検出済み repository path を literal として指定し、rename の両端を一緒に戻す。
    unexpected = set(unexpected_paths)
    paths = sorted(
        {
            path
            for change in changes
            if unexpected.intersection(change.paths)
            for path in change.paths
        }
    )
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


def restore_session_after_join_failure(
    context: EditingRunContext,
    session_head_before_join: str,
) -> None:
    """merge/post-join 失敗後に session worktree を開始時点へ戻す。"""
    # merge --abort が失敗しても、開始前の clean tree へ戻す。
    merge_head = run_git(
        ["rev-parse", "-q", "--verify", "MERGE_HEAD"],
        context.session_worktree,
        check=False,
    )
    if merge_head.returncode == 0:
        run_git(["merge", "--abort"], context.session_worktree, check=False)
    run_git(["reset", "--hard", session_head_before_join], context.session_worktree)
    run_git(["clean", "-fd"], context.session_worktree)


def cleanup_joined_run(
    context: EditingRunContext,
    warnings: list[str],
    report_path: Path | None = None,
) -> str:
    """merge 済み run の worktree と branch を安全条件付きで削除する。"""
    # state、到達可能性、保存済み report の全条件を確認してから削除する。
    try:
        _, _, state = load_state_for_branch(context.repo, context.session_branch)
        saved = (
            report_path is not None
            and report_path.is_file()
            and report_path.stat().st_size > 0
        )
        if state.run.state != "ready" or not saved:
            warnings.append(
                "run cleanup deferred: ready state or saved report was not confirmed"
            )
            return "deferred"
    except Exception:
        warnings.append("run cleanup deferred: state/report check failed")
        return "deferred"
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
        return "deferred"
    if not reachable:
        warnings.append("run branch is not reachable from session branch")
        return "deferred"
    # 削除対象 worktree が cwd の場合は、session worktree へ退避する。
    if Path.cwd().resolve() == context.run_worktree.resolve():
        try:
            os.chdir(context.session_worktree)
        except Exception:
            warnings.append("run worktree cleanup failed")
            return "preserved"
    try:
        warnings.extend(
            stop_tracked_codex_children(context.repo, context.session_id) or []
        )
    except Exception:
        warnings.append("run child process cleanup failed")
        return "preserved"
    if context.run_worktree.exists() or context.run_worktree.is_symlink():
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
    # worktree の削除成功後だけ branch を削除する。
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
    # 差分を report に保存してから、join を中断する。
    update_primary_report_fields(
        state_after=context.state_before,
        run_join_commit=None,
        post_join_hook="not_run",
        cleanup="not_run",
        unexpected_paths=paths,
    )
    raise CmocError(
        summary,
        [
            "run branch のみを修復する場合は `cmoc run join --force-resolve` を実行してください。"
        ],
        "\n".join(paths),
    )


def join_editing_run(
    context: EditingRunContext | None = None,
    *,
    automatic: bool = False,
    force_resolve: bool = False,
    warnings: list[str] | None = None,
    save_report: Callable[[str, TerminalClassification, list[str]], Path] | None = None,
    classification: TerminalClassification = "natural_completion",
) -> TerminalResult:
    """自動・明示 join の検査、取り込み、結果保存、state と資源回収を行う。"""
    # 本命作業の成功と join の成功を分け、同じ run の失敗だけを回収する。
    original = (
        context
        or resolve_active_run({"joinable", "error"}, allow_missing_run_worktree=True)[0]
    )
    report_role = (
        "run join report"
        if save_report is None
        else (
            "feedback invocation report"
            if original.kind == "feedback_report"
            else f"{original.kind.replace('_', ' ')} report"
        )
    )
    warnings = warnings if warnings is not None else []
    report: Path | None = None
    details: dict[str, object] = {
        "join_status": "started",
        "join_preconditions": "not_run",
        "join_diff_validation": "not_run",
        "merge_status": "not_run",
        "run_join_commit": None,
        "post_join_hook": "not_run",
        "refactor_state_sync_status": "not_run",
        "refactor_state_sync_commit": None,
        "workload_post_join": "not_run",
        "state_reset": "not_run",
        "cleanup": "not_run",
        "failure_stage": None,
        "conflict_resolution": {"agent_status": "not_needed", "initial_conflicts": []},
    }

    def persist(state_after: str, terminal: TerminalClassification) -> Path:
        # 個別 workload は本命作業の詳細を保ち、内部 join 用 report を追加しない。
        nonlocal report
        update_primary_report_fields(**details, state_after=state_after)
        if save_report is not None:
            report = save_report(state_after, terminal, warnings)
        else:
            report = write_lifecycle_report(
                original,
                "join",
                state_after=state_after,
                warnings=warnings,
                details=details,
                terminal_classification=terminal,
                exit_code=1 if terminal == "error" else 0,
                report_path=report,
            )
        return report

    with primary_report_finalization_lock(original.repo, original.session_id):
        confirmed = False
        phase = "join preconditions"
        try:
            allowed = {"running"} if automatic else {"joinable", "error"}
            active, state = resolve_active_run(allowed, allow_missing_run_worktree=True)
            if (active.kind, active.run_branch, active.run_fork_commit) != (
                original.kind,
                original.run_branch,
                original.run_fork_commit,
            ):
                raise CmocError(
                    "join 対象の run が変更されています。", [], str(original.state_path)
                )
            confirmed = True
            if automatic:
                state.run.state = "joinable"
                write_state(active.state_path, state)
                active = replace(active, state_before="joinable")
            update_primary_report_fields(
                run_kind=active.kind,
                session_branch=active.session_branch,
                session_fork_commit=active.session_fork_commit,
                run_branch=active.run_branch,
                run_fork_commit=active.run_fork_commit,
                run_worktree=active.run_worktree,
                state_before=original.state_before,
                state_after=state.run.state,
            )
            set_primary_report_save_failure_handler(lambda: restore_run_error(original))
            from sub_commands.feedback.recovery import require_manual_feedback_run

            phase = "feedback recovery boundary"
            require_manual_feedback_run(active)
            phase = "join preconditions"
            if not active.run_worktree.is_dir() or not branch_exists(
                active.repo, active.run_branch
            ):
                raise CmocError(
                    "join に必要な run 資源がありません。",
                    list(join_recovery_actions(active)),
                    str(active.run_worktree),
                )
            # 開始時の doctor 成功に依存せず、merge 直前の状態を検査する。
            phase = "join doctor preprocess"
            start_subcommand_step(
                1, "join: doctor preprocess", "join doctor preprocess"
            )
            repairs = doctor_preprocess_changes_for_join()
            ignored = doctor_paths_for_join(
                repairs, active.run_worktree, active.run_fork_commit
            )
            phase = "join preconditions"
            if active.state_before == "error":
                _tracked, warning = stop_error_run_process(
                    active.repo, active.session_id
                )
                if warning:
                    warnings.append(warning)
            warnings.extend(
                stop_tracked_codex_children(active.repo, active.session_id) or []
            )
            require_clean_worktree(active.session_worktree)
            require_clean_worktree(active.run_worktree)
            details["join_preconditions"] = "completed"
            phase = "join diff validation"
            validate_run_join(
                active, warnings, force_resolve=force_resolve, run_ignored_paths=ignored
            )
            details["join_diff_validation"] = "completed"
            phase = "merge and post-join"
            before = head_commit(active.session_worktree)
            (
                commit,
                hook,
                sync_commit,
                last_apply_commit,
                resolution,
            ) = merge_run(active, state, warnings, before)
            details.update(
                merge_status="merged" if commit else "no_op",
                run_join_commit=commit,
                post_join_hook=hook,
                refactor_state_sync_status="completed",
                refactor_state_sync_commit=sync_commit,
                conflict_resolution=resolution,
            )
            phase = "workload post-join"
            if active.kind == "feedback_report":
                from sub_commands.feedback.recovery import finish_manual_feedback_run

                finish_manual_feedback_run(active, "joined")
            details["workload_post_join"] = "completed"
            # report が保存できるまでは active run を初期化しない。
            phase = "join result save"
            details["join_status"] = "merged"
            details["cleanup"] = "pending"
            persist(state.run.state, classification)
            phase = "state reset"
            ready_state = replace(
                state,
                session=replace(
                    state.session, last_joined_apply_fork_commit=last_apply_commit
                ),
                run=RunPart(),
            )
            write_state(active.state_path, ready_state)
            details["state_reset"] = "completed"
            phase = "cleanup"
            assert report is not None
            details["cleanup"] = cleanup_joined_run(active, warnings, report)
            if details["cleanup"] not in {"completed", "deferred"}:
                raise CmocError(
                    "run の隔離資源 cleanup に失敗しました。", [], "\n".join(warnings)
                )
            delete_run_process_id(active.repo, active.session_id)
            details.update(
                join_status="completed",
                remaining_resources=remaining_run_resources(active),
            )
            phase = "final join result save"
            persist("ready", classification)
        except BaseException as exc:
            if phase == "merge and post-join":
                phase = str(current_primary_report_fields().get("join_phase", phase))
            details.update(
                join_status="error",
                failure_stage=phase,
                error=repr(exc),
                remaining_resources=remaining_run_resources(original),
            )
            if phase == "join preconditions":
                details["join_preconditions"] = "failed"
            elif phase == "join diff validation":
                details["join_diff_validation"] = "failed"
            # merge_run が保存した確定情報を、後段の失敗でも失わない。
            details.update(
                {
                    name: value
                    for name, value in current_primary_report_fields().items()
                    if name
                    in {
                        "merge_status",
                        "run_join_commit",
                        "post_join_hook",
                        "refactor_state_sync_status",
                        "refactor_state_sync_commit",
                        "conflict_resolution",
                    }
                }
            )
            if confirmed:
                try:
                    restore_run_error(original)
                except BaseException as state_error:
                    warnings.append(f"error state save failed: {state_error!r}")
            try:
                _, _, saved = load_state_for_branch(
                    original.repo, original.session_branch
                )
                state_after = saved.run.state
            except BaseException:
                state_after = "unconfirmed"
            try:
                persist(state_after, "error")
            except BaseException as report_error:
                warnings.append(f"join report save failed: {report_error!r}")
            actions = (
                tuple(exc.next_actions)
                if phase == "feedback recovery boundary" and isinstance(exc, CmocError)
                else join_recovery_actions(original)
            )
            update_primary_report_fields(recovery_next_actions=actions)
            raise CmocError(
                "run join または必要な後処理に失敗しました。",
                list(actions),
                repr(exc),
                terminal_result=TerminalResult(
                    primary_report=report
                    if report is not None and report.is_file() and report.stat().st_size
                    else None,
                    primary_report_role=report_role
                    if report is not None and report.is_file() and report.stat().st_size
                    else None,
                    completion_reason="error",
                    details=tuple(details.items()),
                    next_actions=actions,
                    warnings=tuple(warnings),
                ),
            ) from exc
    return TerminalResult(
        primary_report=report,
        primary_report_role=report_role,
        details=tuple(details.items()),
        warnings=tuple(warnings),
    )


def remaining_run_resources(context: EditingRunContext) -> dict[str, object]:
    """部分 cleanup 後も、実在する branch と worktree を区別して返す。"""
    # 診断自体の失敗を、資源が存在しないという結果へ変換しない。
    try:
        branch: object = branch_exists(context.repo, context.run_branch)
    except Exception:
        branch = "unconfirmed"
    try:
        worktree: object = (
            context.run_worktree.exists() or context.run_worktree.is_symlink()
        )
    except Exception:
        worktree = "unconfirmed"
    return {
        "branch": branch,
        "worktree": worktree,
    }


def join_recovery_actions(context: EditingRunContext) -> tuple[str, ...]:
    """取り込みに必要な資源の実在に合わせて次の操作を案内する。"""
    resources = remaining_run_resources(context)
    if resources["branch"] is True and resources["worktree"] is True:
        return (
            "process の停止と両 worktree の未確定差分を確認し、`cmoc run join` で再試行してください。",
            "`cmoc run abandon` で残る隔離資源を破棄できます。取り込み済み commit は保持されます。",
        )
    return (
        "join に必要な資源を確認できません。残存資源を修復するか、`cmoc run abandon` で回収してください。",
    )


def restore_run_error(context: EditingRunContext) -> None:
    """最新の session 項目を保ち、同じ run の復旧情報を error として保存する。"""
    # hook が更新した比較始点を、join 開始時の古い state で上書きしない。
    with run_lifecycle_lock(context.repo, context.session_id):
        _, _, state = load_state_for_branch(context.repo, context.session_branch)
        if state.run.state != "ready" and state.run.branch != context.run_branch:
            raise CmocError(
                "復旧対象とは異なる active run があります。",
                [],
                str(context.state_path),
            )
        state.run = RunPart(
            "error", context.kind, context.run_branch, context.run_fork_commit
        )
        write_state(context.state_path, state)
        delete_run_process_id(context.repo, context.session_id)
        update_primary_report_fields(
            state_after="error",
            remaining_resources=remaining_run_resources(context),
            recovery_next_actions=join_recovery_actions(context),
        )
