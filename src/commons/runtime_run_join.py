"""editing run の join と cleanup で共有する runtime 処理。"""

import os
from collections.abc import Callable, Collection
from dataclasses import replace
from functools import partial
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
from .runtime_paths import repo_root, reuse_root_queries, work_root
from .runtime_primary_report import (
    current_primary_report_fields,
    primary_report_finalization_lock,
    set_primary_report_completion_handler,
    set_primary_report_save_failure_handler,
    update_primary_report_fields,
)
from .runtime_primary_report_specs import TerminalClassification
from .runtime_refactor import merge_refactor_states
from .runtime_results import TerminalResult
from .runtime_run import (
    delete_run_process_id,
    run_lifecycle_lock,
    run_process_tracking,
    stop_error_run_process,
    stop_tracked_codex_children,
    write_run_process_id,
)
from .runtime_run_join_state import (
    JoinRecord,
    confirm_import,
    join_record,
    load_join_record,
    tree_id,
)
from .runtime_run_lifecycle import (
    EditingRunContext,
    GitChange,
    commit_work_unit,
    resolve_active_run,
    tree_changes,
    unexpected_run_paths,
    worktree_change_paths,
)
from .runtime_run_report import write_lifecycle_report
from .runtime_state import RunPart, SessionState, load_state_for_branch, write_state


def doctor_preprocess_for_join(*, rollback_on_interruption: bool = False) -> None:
    """join と feedback 開始前の doctor を、復旧と同期の境界に従って実行する。"""
    # 元の成果の検査範囲は journal が固定し、doctor の path 除外は不要。
    # 両 root の探索だけを共有し、復旧・修復処理へ metadata を持ち越さない。
    with reuse_root_queries():
        root = work_root()
        main_root = repo_root(root)
    _run_join_doctor(root, main_root, rollback_on_interruption=rollback_on_interruption)


def _run_join_doctor(
    root: Path, main_root: Path, *, rollback_on_interruption: bool = False
) -> None:
    """全 workload の join 同期を run 側へ遅延し、取り込み後は再実行しない。"""
    # 新規 workload の通常 doctor は維持し、join 記録を先に照合する。
    sync_refactor_entries = True
    record: JoinRecord | None = None
    try:
        branch = current_branch(root)
        session_id, _, state = load_state_for_branch(main_root, branch)
    except CmocError:
        # active run の詳細な事前条件は doctor 後の resolve_active_run で報告する。
        pass
    else:
        record = load_join_record(main_root, session_id)
        if record is not None and not record.finished:
            if confirm_import(record):
                update_primary_report_fields(
                    **record.report_fields(), join_recovery="post_join"
                )
                return
            rollback_join_preparation(record)
            record.preparation_started = True
            record.pending_action = "doctor"
            record.save()
        sync_refactor_entries = state.run.state == "ready"
    if rollback_on_interruption:
        run_doctor_preprocess(
            root,
            sync_refactor_entries=sync_refactor_entries,
            rollback_on_interruption=True,
        )
    else:
        run_doctor_preprocess(root, sync_refactor_entries=sync_refactor_entries)
    if record is not None and not record.finished:
        record.owned_run_head = _require_preparation_ownership(record)
        record.pending_action = None
        record.save()


def validate_run_join(
    context: EditingRunContext,
    warnings: list[str],
    *,
    force_resolve: bool = False,
    run_ignored_paths: Collection[str] = (),
    original_run_head: str | None = None,
) -> None:
    """明示 join と self-joining workload が共有する clean・差分検査を行う。"""
    # session と run の両 worktree を clean にし、fork 以後の差分を分類する。
    require_clean_worktree(context.session_worktree)
    require_clean_worktree(context.run_worktree)
    run_changes = tree_changes(
        context.run_worktree,
        context.run_fork_commit,
        original_run_head or "HEAD",
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
        record = join_record(context)
        record.pending_action = "force"
        record.force_paths = sorted(
            {
                path
                for change in run_changes
                if set(run_unexpected).intersection(change.paths)
                for path in change.paths
            }
        )
        record.save()
        _revert_unexpected_run_paths(context, run_changes, run_unexpected)
        record.owned_run_head = _require_preparation_ownership(record)
        record.pending_action = None
        record.force_paths = []
        record.save()
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


def rollback_join_preparation(record: JoinRecord) -> None:
    """停止確認後、run の準備だけを元の成果へ戻す。"""
    # 取り込み済みなら、run の履歴も session の成果も巻き戻さない。
    if confirm_import(record) or not record.preparation_started:
        return
    context = record.context
    stop_tracked_codex_children(context.repo, context.session_id)
    _require_preparation_ownership(record)
    # 最終 merge の未確定結果だけを中止し、人間の差分があれば保持する。
    merge_head = run_git(
        ["rev-parse", "-q", "--verify", "MERGE_HEAD"],
        context.session_worktree,
        check=False,
    )
    if merge_head.returncode == 0:
        if (
            merge_head.stdout.strip() != record.prepared_run_head
            or head_commit(context.session_worktree) != record.session_head
            or run_git(["write-tree"], context.session_worktree).stdout.strip()
            != tree_id(context.repo, record.prepared_run_head or "")
            or run_git(
                ["diff", "--quiet"], context.session_worktree, check=False
            ).returncode
            or run_git(
                ["ls-files", "--others", "--exclude-standard"], context.session_worktree
            ).stdout
        ):
            raise CmocError("session の未確定差分の帰属を確認できません。", [], "")
        run_git(["merge", "--abort"], context.session_worktree)
    run_git(["merge", "--abort"], context.run_worktree, check=False)
    run_git(["reset", "--hard", record.original_run_head], context.run_worktree)
    run_git(["clean", "-fd"], context.run_worktree)
    record.attempts.append(
        {
            "session_head": record.session_head,
            "prepared_run_head": record.prepared_run_head,
            "sync_commit": record.sync_commit,
            "resolution": record.resolution,
        }
    )
    record.session_head = record.prepared_run_head = record.sync_commit = None
    record.resolution = {}
    record.preparation_started = False
    record.owned_run_head = record.original_run_head
    record.pending_action = None
    record.force_paths = []
    record.save()
    update_primary_report_fields(merge_rollback="completed", process_stop="confirmed")


def _require_preparation_ownership(record: JoinRecord) -> str:
    # commit 作成と記録保存の間に停止した場合だけ、保留した操作と履歴を照合する。
    # 確認した HEAD を直後の記録にも使い、次の操作後は改めて検査する。
    context = record.context
    head = head_commit(context.run_worktree)
    pending_paths = set(
        worktree_change_paths(context.run_worktree, include_rename_sources=True)
    )
    if not _preparation_paths_match(record, pending_paths):
        raise CmocError(
            "run の未確定差分の帰属を確認できません。",
            [],
            "\n".join(sorted(pending_paths)),
        )
    if head == record.owned_run_head:
        if record.pending_action is None:
            require_clean_worktree(context.run_worktree)
        return head
    parents = run_git(["show", "-s", "--format=%P", head], context.repo).stdout.split()
    expected = [record.owned_run_head]
    allowed = False
    if record.pending_action == "merge":
        allowed = parents == [record.owned_run_head, record.session_head] or (
            head == record.session_head
            and run_git(
                ["merge-base", "--is-ancestor", record.owned_run_head or "", head],
                context.repo,
                check=False,
            ).returncode
            == 0
        )
    elif parents == expected and record.pending_action in {"doctor", "force", "sync"}:
        paths = {
            path
            for change in tree_changes(context.repo, record.owned_run_head or "", head)
            for path in change.paths
        }
        if record.pending_action in {"sync", "doctor"}:
            allowed = _preparation_paths_match(record, paths)
        else:
            allowed = (
                paths <= set(record.force_paths)
                and run_git(
                    [
                        "diff",
                        "--quiet",
                        head,
                        context.run_fork_commit,
                        "--",
                        *[literal_pathspec(path) for path in record.force_paths],
                    ],
                    context.repo,
                    check=False,
                ).returncode
                == 0
            )
    if not allowed:
        raise CmocError(
            "run の準備変更の帰属を確認できません。",
            ["残存する run の履歴と差分を確認してください。"],
            head,
        )
    return head


def _preparation_paths_match(record: JoinRecord, paths: set[str]) -> bool:
    # 管理更新の保留中に、無関係な差分を巻き込んで戻さない。
    if record.pending_action == "force":
        return paths <= set(record.force_paths)
    if record.pending_action == "sync":
        return paths <= {".cmoc/gt/realization/refactor/state.json"}
    if record.pending_action == "doctor":
        return all(
            path
            in {
                ".gitignore",
                ".cmoc/gt/config.json",
                ".cmoc/gt/realization/refactor/state.json",
            }
            or path.startswith(".agents/")
            for path in paths
        )
    return record.pending_action == "merge" or not paths


def merge_run(
    context: EditingRunContext,
    state: SessionState,
    warnings: list[str],
    session_head_before_join: str,
    *,
    on_merged: Callable[[str | None, dict[str, object]], None] | None = None,
    feedback_report_cut_path: Path | None = None,
    verify_prepared: Callable[[JoinRecord], None] | None = None,
) -> tuple[str | None, str, str | None, str | None, dict[str, object]]:
    """run 側で準備を確定してから同じ tree を取り込み、後処理を行う。"""
    record = join_record(context)
    try:
        recovered = confirm_import(record)
        update_primary_report_fields(
            join_recovery="post_join" if recovered else "initial"
        )
        if not recovered:
            require_clean_worktree(context.session_worktree)
            require_clean_worktree(context.run_worktree)
            record.session_head = session_head_before_join
            record.preparation_started = True
            run_head = head_commit(context.run_worktree)
            record.owned_run_head = run_head
            record.pending_action = "merge"
            record.save()
            update_primary_report_fields(
                join_phase="run preparation", **record.report_fields()
            )
            start_subcommand_step(3, "session を run へ統合", "prepare run join")
            merge = run_git(
                ["merge", "--ff", "--no-edit", record.session_head],
                context.run_worktree,
                check=False,
            )
            resolution: dict[str, object] = {
                "agent_status": "not_needed",
                "initial_conflicts": [],
            }
            if merge.returncode != 0:
                from oracle.acp_builder.run.join.conflict_resolution import (
                    build_run_join_conflict_resolution_parameter,
                )

                write_run_process_id(context.repo, context.session_id, os.getpid())
                with run_process_tracking(context.repo, context.session_id):
                    resolution = resolve_merge_conflicts(
                        context.run_worktree,
                        partial(
                            build_run_join_conflict_resolution_parameter,
                            run_head,
                            record.session_head,
                            context.run_worktree,
                            feedback_report_cut_path=feedback_report_cut_path,
                        ),
                        purpose="run join conflict resolution",
                        before_commit=lambda: warnings.extend(
                            stop_tracked_codex_children(
                                context.repo, context.session_id
                            )
                            or []
                        ),
                        sync_managed_entries=False,
                    )
            merged_run_head = _require_preparation_ownership(record)
            # 検証記録は同期前の tree と結び付け、同期後にも適用可能性を検査する。
            record.resolution = {
                **resolution,
                "verified_run_commit": merged_run_head,
            }
            record.owned_run_head = merged_run_head
            record.pending_action = "sync"
            record.save()
            update_primary_report_fields(join_phase="refactor state sync")
            merge_refactor_states(context.run_worktree, (run_head, record.session_head))
            record.sync_commit = commit_work_unit(
                context.run_worktree, "cmoc refactor state sync before run join"
            )
            prepared_run_head = _require_preparation_ownership(record)
            require_clean_worktree(context.run_worktree)
            record.prepared_run_head = prepared_run_head
            record.owned_run_head = record.prepared_run_head
            record.pending_action = None
            if verify_prepared is not None:
                verify_prepared(record)
            record.save()
            update_primary_report_fields(
                join_phase="session import", **record.report_fields()
            )
            # 準備中に session が進んだ場合は、次回の準備に委ねる。
            require_clean_worktree(context.session_worktree)
            require_clean_worktree(context.run_worktree)
            if (
                head_commit(context.session_worktree) != record.session_head
                or head_commit(context.run_worktree) != record.prepared_run_head
            ):
                raise CmocError(
                    "準備中に session または run HEAD が変更されました。", [], ""
                )
            if record.prepared_run_head == record.session_head:
                record.session_commit = record.session_head
                record.session_tree = tree_id(context.repo, record.session_commit)
                record.imported = True
                record.save()
            else:
                # commit 前にも基準 HEAD と準備済み tree を照合する。
                run_git(
                    ["merge", "--no-ff", "--no-commit", record.prepared_run_head],
                    context.session_worktree,
                )
                if (
                    head_commit(context.session_worktree) != record.session_head
                    or run_git(["write-tree"], context.session_worktree).stdout.strip()
                    != tree_id(context.repo, record.prepared_run_head)
                    or run_git(
                        ["diff", "--quiet"], context.session_worktree, check=False
                    ).returncode
                ):
                    raise CmocError("session の取り込み条件が変更されました。", [], "")
                run_git(["commit", "--no-edit"], context.session_worktree)
                # 取り込み直後の人間の commit を、取り込み commit と誤認しない。
                if not confirm_import(record):
                    raise CmocError(
                        "session への取り込み成立を確認できません。", [], ""
                    )
        update_primary_report_fields(**record.report_fields())
        if on_merged is not None:
            on_merged(record.join_commit, record.resolution)
        # apply の資格は今回の開始時 state だけから判断する。
        update_primary_report_fields(join_phase="post-join hook")
        last_apply = state.session.last_joined_apply_fork_commit
        if record.hook is None:
            record.hook = "none"
            if context.kind == "realization_apply":
                record.hook = "session.last_joined_apply_fork_commit preserved"
                if context.state_before == "joinable":
                    last_apply = context.run_fork_commit
                    record.hook = "session.last_joined_apply_fork_commit updated"
                    write_state(
                        context.state_path,
                        replace(
                            state,
                            session=replace(
                                state.session, last_joined_apply_fork_commit=last_apply
                            ),
                        ),
                    )
            record.save()
        update_primary_report_fields(post_join_hook=record.hook)
        return (
            record.join_commit,
            record.hook,
            record.sync_commit,
            last_apply,
            record.resolution,
        )
    except BaseException as exc:
        try:
            warnings.extend(
                stop_tracked_codex_children(context.repo, context.session_id) or []
            )
            record = join_record(context)
            rollback_join_preparation(record)
        except BaseException as recovery_error:
            update_primary_report_fields(
                merge_rollback="failed", rollback_error=repr(recovery_error)
            )
            raise CmocError(
                "join の準備を復旧できませんでした。", [], repr(recovery_error)
            ) from exc
        update_primary_report_fields(**record.report_fields())
        raise


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


def cleanup_joined_run(
    context: EditingRunContext,
    warnings: list[str],
    report_path: Path | None = None,
) -> str:
    """merge 済み run の worktree と branch を安全条件付きで削除する。"""
    # state、到達可能性、保存済み report の全条件を確認してから削除する。
    try:
        record = load_join_record(context.repo, context.session_id)
        if (
            record is None
            or not confirm_import(record)
            or not record.workload_post_join
        ):
            warnings.append(
                "run cleanup deferred: join recovery record was not confirmed"
            )
            return "deferred"
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
                    record.prepared_run_head or "",
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
    if not _cleanup_run_matches_prepared(context, record):
        warnings.append("run cleanup deferred: run resources changed")
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


def _cleanup_run_matches_prepared(
    context: EditingRunContext, record: JoinRecord
) -> bool:
    # 削除前に branch と残存 worktree の両方を準備完了成果へ照合する。
    try:
        # 存在確認と HEAD 取得を一度に行い、不在 (1) と照会失敗を区別する。
        branch = run_git(
            ["rev-parse", "--verify", "--quiet", f"refs/heads/{context.run_branch}"],
            context.repo,
            check=False,
        )
        if branch.returncode not in {0, 1} or (
            branch.returncode == 0 and branch.stdout.strip() != record.prepared_run_head
        ):
            return False
        if context.run_worktree.exists():
            require_clean_worktree(context.run_worktree)
            return head_commit(context.run_worktree) == record.prepared_run_head
        return True
    except Exception:
        return False


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
            existing = load_join_record(active.repo, active.session_id)
            recovered_import = (
                existing is not None
                and existing.context.run_branch == active.run_branch
                and confirm_import(existing)
            )
            if not recovered_import and (
                not active.run_worktree.is_dir()
                or not branch_exists(active.repo, active.run_branch)
            ):
                raise CmocError(
                    "join に必要な run 資源がありません。",
                    list(join_recovery_actions(active)),
                    str(active.run_worktree),
                )
            # doctor による run の管理更新より先に元の成果を固定する。
            if not recovered_import:
                if active.state_before == "error":
                    _tracked, warning = stop_error_run_process(
                        active.repo, active.session_id
                    )
                    if warning:
                        warnings.append(warning)
                warnings.extend(
                    stop_tracked_codex_children(active.repo, active.session_id) or []
                )
            # 停止後の確定済み成果を固定し、doctor の管理更新より先に保存する。
            record = join_record(active)
            recovered_import = confirm_import(record)
            if not recovered_import:
                rollback_join_preparation(record)
                for worktree in (active.session_worktree, active.run_worktree):
                    # 未 ignore の管理領域は doctor が修復する。既存の作業差分は保持する。
                    status = run_git(
                        [
                            "status",
                            "--porcelain",
                            "--untracked-files=all",
                            "--",
                            ".",
                            ":(exclude).cmoc/gu",
                        ],
                        worktree,
                    ).stdout
                    require_clean_worktree(worktree, status=status)
            details.update(
                record.report_fields(),
                join_recovery="post_join" if recovered_import else "initial",
            )
            # 取り込み後の復旧では削除済み run を要求しない。
            phase = "join doctor preprocess"
            start_subcommand_step(
                1, "join: doctor preprocess", "join doctor preprocess"
            )
            if not recovered_import:
                doctor_preprocess_for_join()
                record = join_record(active)
            phase = "join preconditions"
            if not recovered_import:
                require_clean_worktree(active.session_worktree)
                require_clean_worktree(active.run_worktree)
            details["join_preconditions"] = "completed"
            phase = "join diff validation"
            if not recovered_import:
                record.session_head = head_commit(active.session_worktree)
                record.preparation_started = True
                record.save()
                validate_run_join(
                    active,
                    warnings,
                    force_resolve=force_resolve,
                    original_run_head=record.original_run_head,
                )
            details["join_diff_validation"] = (
                "reused" if recovered_import else "completed"
            )
            phase = "merge and post-join"
            before = head_commit(active.session_worktree)
            (
                commit,
                hook,
                sync_commit,
                last_apply_commit,
                resolution,
            ) = merge_run(active, state, warnings, before)
            record = join_record(active)
            details.update(
                merge_status="merged" if commit else "no_op",
                run_join_commit=commit,
                post_join_hook=hook,
                refactor_state_sync_status="completed",
                refactor_state_sync_commit=sync_commit,
                conflict_resolution=resolution,
                **{
                    key: value
                    for key, value in record.report_fields().items()
                    if key
                    not in {
                        "merge_status",
                        "run_join_commit",
                        "refactor_state_sync_status",
                        "refactor_state_sync_commit",
                        "conflict_resolution",
                    }
                },
            )
            phase = "workload post-join"
            record = join_record(active)
            if active.kind == "feedback_report" and not record.workload_post_join:
                from sub_commands.feedback.recovery import finish_manual_feedback_run

                finish_manual_feedback_run(active, "joined")
            record.workload_post_join = True
            record.save()
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

            def finish_join() -> None:
                # 最外側の保存まで停止復旧の根拠を残す。
                record.finished = True
                record.save()

            if not set_primary_report_completion_handler(finish_join):
                finish_join()
        except BaseException as exc:
            failed_record = load_join_record(original.repo, original.session_id)
            if (
                failed_record is not None
                and failed_record.context.run_branch == original.run_branch
            ):
                try:
                    rollback_join_preparation(failed_record)
                    details.update(failed_record.report_fields())
                except BaseException as rollback_error:
                    details.update(
                        merge_rollback="failed", rollback_error=repr(rollback_error)
                    )
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
    record = load_join_record(context.repo, context.session_id)
    if (
        record is not None
        and record.context.run_branch == context.run_branch
        and confirm_import(record)
    ):
        return (
            "`cmoc run join` で未完了の後処理を再開してください。",
            "`cmoc run abandon` で残る隔離資源を破棄できます。取り込み済み commit は保持されます。",
        )
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
        record = load_join_record(context.repo, context.session_id)
        if record is not None and record.context.run_branch == context.run_branch:
            record.finished = False
            record.save()
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
