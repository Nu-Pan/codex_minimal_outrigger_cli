"""Feedback の公開・再確認待ちの終了処理と明示 join/abandon の境界を扱う。

根拠: {{work-root}}/spec/app_spec/feedback_state.md の
「最新状態の atomic publication」と「run lifecycle との整合」。
"""

from dataclasses import replace
from pathlib import Path
from typing import Any

from cmoc_runtime import (
    RunPart,
    SessionState,
    TerminalResult,
    branch_exists,
    head_commit,
    load_state_for_branch,
    require_clean_worktree,
    write_state,
)
from commons.runtime_feedback_run_state import (
    new_run_identity,
    read_run_artifact,
    unpublished_join_record,
)
from commons.runtime_feedback_state import (
    _durable_unlink,
    _read_canonical_object,
    _require_exact_fields,
    artifact_reference,
    cleanup_published_report,
    current_pointer_path,
    discard_report_cut,
    discard_staged_publication,
    feedback_writer_lock,
    load_report_cut,
    recover_report_cut_checkpoint_references,
    validate_feedback_state,
)
from commons.runtime_feedback_store import feedback_root, write_immutable_json
from commons.runtime_ids import is_common_id
from commons.runtime_join import confirm_import
from commons.runtime_logging import current_subcommand_logger
from commons.runtime_primary_report import (
    current_primary_report_fields,
    primary_report_finalization_lock,
    set_primary_report_completion_handler,
    set_primary_report_save_failure_handler,
    update_primary_report_fields,
)
from commons.runtime_run import (
    delete_run_process_id,
    expected_run_worktree,
    worktree_for_branch,
)
from commons.runtime_run_join import (
    cleanup_joined_run,
    remaining_run_resources,
    restore_run_error,
)
from commons.runtime_run_join_state import join_record, load_join_record
from commons.runtime_run_lifecycle import EditingRunContext


def finish_feedback_run(
    context: EditingRunContext, manifest: dict[str, Any], result: TerminalResult
) -> TerminalResult:
    """work artifact を削除する前に最小の recovery journal を durable 保存する。"""
    from .remediation import _failure

    if result.primary_report is None and result.result != "recheck_pending":
        raise _failure("feedback finalization に durable report がありません。")
    completion = read_run_artifact(context.repo, manifest["run"]["completion"])
    merged = read_run_artifact(context.repo, manifest["run"]["merged"])
    path = feedback_root(context.repo) / "finalization.json"
    pointer_path = current_pointer_path(context.repo)
    # journal には pointer だけを固定し、参照先の検証は lifecycle lock 内で一度行う。
    journal = {
        "schema_version": 1,
        "feedback_run_id": manifest["run"]["feedback_run_id"],
        "report_execution_id": manifest["run"]["targets"]["execution_id"],
        "identity": manifest["run"]["identity"],
        "report_cut_id": manifest["report_cut_id"],
        "report": (
            artifact_reference(context.repo, result.primary_report)
            if result.primary_report is not None
            else None
        ),
        "current": (
            _read_canonical_object(pointer_path, "feedback current pointer")
            if pointer_path.exists() or pointer_path.is_symlink()
            else None
        ),
        "completion": completion,
        "merged": merged,
        "result": result.result,
        "recheck_pending_issues": dict(result.details).get(
            "recheck_pending_issues", []
        ),
    }
    write_immutable_json(path, journal)
    return _finish_from_journal(context, journal, path)


def recover_finalization(repo: Path, session_branch: str) -> TerminalResult | None:
    """公開または再確認待ちの終了処理だけを再開し、新しい判定は開始しない。"""
    path = feedback_root(repo) / "finalization.json"
    if not path.exists() and not path.is_symlink():
        return None
    journal = _read_canonical_object(path, "feedback finalization journal")
    context, _ = _journal_context(repo, journal)
    if context.session_branch != session_branch:
        from .remediation import _failure

        raise _failure(
            "別 session の feedback finalization が未完了です。",
            [
                f"{context.session_branch} で `cmoc feedback report` を実行してください。"
            ],
        )
    from .remediation import _indivisible_finalization

    with _indivisible_finalization():
        logger = current_subcommand_logger()
        if logger is not None:
            logger.event(
                "feedback_recovery_started",
                feedback_run_id=journal["feedback_run_id"],
                report_cut_id=journal["report_cut_id"],
                report_execution_id=journal["report_execution_id"],
                report_path=(
                    str(repo / journal["report"]["path"]) if journal["report"] else None
                ),
                publication_status="cleanup",
            )
        return _finish_from_journal(context, journal, path)


def _journal_context(
    repo: Path, journal: dict[str, Any]
) -> tuple[EditingRunContext, SessionState]:
    """journal の identity を照合し、検証した session state とともに返す。"""
    from .remediation import _failure

    path = feedback_root(repo) / "finalization.json"
    _require_exact_fields(
        journal,
        {
            "schema_version",
            "feedback_run_id",
            "report_execution_id",
            "identity",
            "report_cut_id",
            "report",
            "current",
            "completion",
            "merged",
            "result",
            "recheck_pending_issues",
        },
        path,
        "feedback finalization journal",
    )
    if (
        type(journal["schema_version"]) is not int
        or journal["schema_version"] != 1
        or not is_common_id(journal["feedback_run_id"], "fbr")
        or not is_common_id(journal["report_execution_id"], "exec")
        or journal["result"] not in {"ok", "attention", "incomplete", "recheck_pending"}
    ):
        raise _failure("feedback finalization journal の version/result が不正です。")
    pending = journal["recheck_pending_issues"]
    if (
        not isinstance(pending, list)
        or any(not isinstance(item, str) for item in pending)
        or pending != sorted(set(pending))
        or bool(pending) != (journal["result"] == "recheck_pending")
    ):
        raise _failure("feedback finalization journal の再確認対象が不正です。")
    identity = _require_exact_fields(
        journal["identity"],
        set(EditingRunContext.__dataclass_fields__),
        path,
        "feedback run identity",
    )
    converted = dict(identity)
    for field in ("repo", "session_worktree", "state_path", "run_worktree"):
        if not isinstance(identity[field], str):
            raise _failure("feedback finalization identity の path が不正です。")
        converted[field] = Path(identity[field])
    context = EditingRunContext(**converted)
    session_id, state_path, session = load_state_for_branch(
        repo, context.session_branch
    )
    if (
        context.repo != repo.resolve()
        or context.kind != "feedback_report"
        or context.session_id != session_id
        or context.state_path != state_path
        or context.run_worktree != expected_run_worktree(repo, context.run_branch)
        or context.session_worktree != worktree_for_branch(repo, context.session_branch)
        or session.session.state != "active"
        or session.session.session_fork_commit != context.session_fork_commit
    ):
        raise _failure(
            "feedback finalization journal と session identity が一致しません。"
        )
    if session.run.state not in {"ready", "joinable", "error"} or (
        session.run.state != "ready"
        and (
            session.run.branch != context.run_branch
            or session.run.kind != context.kind
            or session.run.fork_commit != context.run_fork_commit
        )
    ):
        raise _failure("feedback finalization の対象とは異なる active run があります。")
    return context, session


def _finalization_report_path(repo: Path, journal: dict[str, Any]) -> Path | None:
    """公開済み report を検証し、再確認待ちには公開 report を割り当てない。"""
    from .remediation import _failure

    if journal["result"] == "recheck_pending":
        if journal["report"] is not None:
            raise _failure(
                "再確認待ちの feedback finalization に公開 report があります。"
            )
        return None
    report_reference = journal["report"]
    if not isinstance(report_reference, dict) or set(report_reference) != {
        "path",
        "sha256",
    }:
        raise _failure("feedback finalization report の reference が不正です。")
    report_root = repo / ".cmoc" / "gu" / "report" / "feedback"
    expected_report_root = (
        report_root / "incomplete" if journal["result"] == "incomplete" else report_root
    )
    if (
        not isinstance(report_reference["path"], str)
        or Path(report_reference["path"]).is_absolute()
    ):
        raise _failure("feedback finalization report の path が不正です。")
    report_path = repo / report_reference["path"]
    if (
        report_path.stem != journal["report_execution_id"]
        or report_path.resolve(strict=False).parent
        != expected_report_root.resolve(strict=False)
        or report_path.suffix != ".md"
        or artifact_reference(repo, report_path) != report_reference
    ):
        raise _failure("feedback finalization report の path/hash が不正です。")
    return report_path


def _finish_from_journal(
    context: EditingRunContext, journal: dict[str, Any], path: Path
) -> TerminalResult:
    """raw/work cleanup、ready 遷移、隔離資源回収を idempotent に確定する。"""
    from .remediation import _failure
    from .report import _recheck_pending_result, save_feedback_invocation_report

    # 呼び出し元の session を排他対象とし、journal は lock 内で最新状態と照合する。
    repo = context.repo
    report_reference = journal["report"]
    report_path = _finalization_report_path(repo, journal)
    published = journal["result"] != "recheck_pending"
    terminal = (
        TerminalResult(result=journal["result"])
        if published
        else _recheck_pending_result(journal["recheck_pending_issues"])
    )
    completion = journal["completion"]
    if (
        completion.get("report_cut_id") != journal["report_cut_id"]
        or completion.get("checks")
        != {"reachability": True, "paths": True, "clean": True}
        or journal["merged"].get("sealed") != completion.get("sealed")
    ):
        raise _failure("feedback finalization の join evidence が不正です。")
    with primary_report_finalization_lock(repo, context.session_id):
        # lock 取得後の identity と最新 state を照合し、同じ snapshot から
        # state_before を得る。lock 取得前の state を使い回さない。
        validated_context, initial_session = _journal_context(repo, journal)
        if validated_context.session_id != context.session_id:
            raise _failure("feedback finalization の排他対象 session が一致しません。")
        context = validated_context
        state_before = current_primary_report_fields().get(
            "state_before", initial_session.run.state
        )

        def retain_failed_finalization() -> None:
            # journal を保持した自然完了経路は、手動 join/abandon へ切り替えない。
            restore_run_error(context)
            update_primary_report_fields(
                recovery_next_actions=(
                    "`cmoc feedback report` で未完了の公開・再確認待ちの終了処理または cleanup を再開してください。",
                )
            )

        set_primary_report_save_failure_handler(retain_failed_finalization)
        phase = "publication recovery validation"
        try:
            # 同じ検証済み snapshot で current pointer と publication point を照合する。
            state = validate_feedback_state(repo)
            if state.current != journal["current"]:
                raise _failure(
                    "feedback finalization 中に current pointer が変更されました。"
                )
            if context.run_worktree.exists():
                require_clean_worktree(context.run_worktree)
                if head_commit(context.run_worktree) != completion["run_head"]:
                    raise _failure(
                        "feedback finalization の run tree が変更されています。"
                    )
            if published:
                if (
                    state.current is None
                    or state.current["report_cut_id"] != journal["report_cut_id"]
                    or state.current["report_path"] != report_reference["path"]
                    or state.current["report_sha256"] != report_reference["sha256"]
                ):
                    raise _failure("feedback publication point を確認できません。")
                # 同じ排他区間で検証した cleanup manifest を再読・再検証しない。
                manifest = state.cleanup_manifest
                if manifest is None:
                    # cleanup 完了後も、別の未完了 cut を見逃さず identity を検査する。
                    work = load_report_cut(repo)
                    manifest = work[0] if work is not None else None
                if manifest is not None:
                    if (
                        manifest["report_cut_id"] != journal["report_cut_id"]
                        or manifest["run"]["identity"] != journal["identity"]
                    ):
                        raise _failure(
                            "feedback finalization の cleanup 対象が一致しません。"
                        )
                    phase = "publication cleanup"
                    update_primary_report_fields(feedback_stage=phase)
                    cleanup_published_report(repo, state)
            else:
                phase = "retain recheck inputs"
                _retain_for_recheck(context, journal)
            # work artifact の cleanup と結果保存の後に state と隔離資源を回収する。
            update_primary_report_fields(
                run_kind=context.kind,
                session_branch=context.session_branch,
                session_fork_commit=context.session_fork_commit,
                run_branch=context.run_branch,
                run_fork_commit=context.run_fork_commit,
                run_worktree=context.run_worktree,
                state_before=state_before,
                state_after="joinable",
                publication_established=published,
                publication_report=str(report_path)
                if report_path is not None
                else None,
                publication_result=journal["result"] if published else None,
                recheck_pending_issues=journal["recheck_pending_issues"],
                processing_status="completed" if published else "recheck_pending",
                feedback_run_id=journal["feedback_run_id"],
                report_cut_id=journal["report_cut_id"],
                publication_execution_id=journal["report_execution_id"],
                join_status="merged",
                join_preconditions=(
                    "completed" if state_before == "ready" else "previously_completed"
                ),
                join_diff_validation=(
                    "completed" if state_before == "ready" else "previously_completed"
                ),
                merge_status=(
                    "merged" if journal["merged"]["run_join_commit"] else "no_op"
                ),
                run_join_commit=journal["merged"]["run_join_commit"],
                conflict_resolution=journal["merged"].get("resolution"),
                workload_post_join="completed",
                post_join_hook="none",
                refactor_state_sync_status=(
                    "completed" if state_before == "ready" else "previously_completed"
                ),
                cleanup="pending",
                state_reset="not_run",
            )
            phase = "invocation report save"
            invocation_report = save_feedback_invocation_report(
                repo,
                "natural_completion",
                terminal,
                publication_report=report_path,
            )
            _, _, session = load_state_for_branch(repo, context.session_branch)
            record = join_record(context)
            record.workload_post_join = True
            record.save()
            phase = "state reset"
            session.run = RunPart()
            write_state(context.state_path, session)
            warnings: list[str] = []
            phase = "run cleanup"
            cleanup = "completed"
            if branch_exists(repo, context.run_branch):
                cleanup = cleanup_joined_run(context, warnings, invocation_report)
                if cleanup not in {"completed", "deferred"}:
                    raise _failure(
                        "feedback run の隔離資源 cleanup に失敗しました。",
                        detail="\n".join(warnings),
                    )
            elif context.run_worktree.exists() or context.run_worktree.is_symlink():
                raise _failure(
                    "feedback run branch がない状態で worktree が残っています。"
                )
            delete_run_process_id(repo, context.session_id)
            update_primary_report_fields(
                state_after="ready",
                state_reset="completed",
                join_status="completed",
                cleanup=cleanup,
                remaining_resources=remaining_run_resources(context),
            )
            phase = "final invocation report save"
            invocation_report = save_feedback_invocation_report(
                repo,
                "natural_completion",
                replace(terminal, warnings=tuple(warnings)),
                publication_report=report_path,
            )

            # 最外側での最後の report 保存が終わるまで recovery の根拠を保持する。
            def finish_join() -> None:
                # 最外側の report 保存後にだけ、次の run を許可する。
                record.finished = True
                record.save()
                _durable_unlink(path)

            if not set_primary_report_completion_handler(finish_join):
                finish_join()
        except BaseException:
            _, _, session = load_state_for_branch(repo, context.session_branch)
            session.run = RunPart(
                state="error",
                kind=context.kind,
                branch=context.run_branch,
                fork_commit=context.run_fork_commit,
            )
            write_state(context.state_path, session)
            update_primary_report_fields(
                state_after="error",
                failure_stage=phase,
                remaining_resources=remaining_run_resources(context),
                recovery_next_actions=(
                    "`cmoc feedback report` で未完了の公開・再確認待ちの終了処理または cleanup を再開してください。",
                ),
            )
            raise
    update_primary_report_fields(
        state_after="ready",
        cleanup=cleanup,
        run_join_commit=journal["merged"]["run_join_commit"],
    )
    logger = current_subcommand_logger()
    if logger is not None:
        logger.event(
            "feedback_finalization_completed",
            feedback_run_id=journal["feedback_run_id"],
            report_cut_id=journal["report_cut_id"],
            report_execution_id=journal["report_execution_id"],
            report_path=str(report_path) if report_path is not None else None,
            state_after="ready",
            cleanup=cleanup,
            result=journal["result"],
        )
    return TerminalResult(
        primary_report=invocation_report,
        primary_report_role="feedback invocation report",
        result=journal["result"],
        next_actions=terminal.next_actions,
        details=(
            ("run_kind", "feedback_report"),
            ("run_join_commit", journal["merged"]["run_join_commit"]),
            ("post_join_hook", "none"),
            ("refactor_state_sync", "completed"),
            ("cleanup", cleanup),
        ),
        warnings=tuple(warnings),
    )


def _retain_for_recheck(context: EditingRunContext, journal: dict[str, Any]) -> None:
    """公開を保留した入力を残し、この run を次回の新規処理から区別する。"""
    from .remediation import _failure, _validate_context

    directory = feedback_root(context.repo) / "work" / journal["report_cut_id"]
    record = load_join_record(context.repo, context.session_id)
    if (
        record is None
        or not confirm_import(record)
        or record.target_commit != journal["completion"]["session_commit"]
        or record.prepared_head != journal["completion"]["run_head"]
    ):
        raise _failure("feedback 再確認待ちの取り込み結果を確認できません。")
    receipt = unpublished_join_record(context.repo, directory)
    if receipt is not None:
        if (
            receipt["identity"] != journal["identity"]
            or receipt["session_commit"] != journal["completion"]["session_commit"]
            or receipt["recheck_pending_issues"] != journal["recheck_pending_issues"]
        ):
            raise _failure("feedback 再確認待ちの終了記録が一致しません。")
        return
    work = load_report_cut(context.repo)
    if work is None or work[1] != directory / "manifest.json":
        raise _failure("feedback 再確認待ちの入力を確認できません。")
    manifest, path = work
    _validate_context(context, manifest)
    if (
        manifest["processing"]["status"] != "recheck_pending"
        or read_run_artifact(context.repo, manifest["run"]["completion"])
        != journal["completion"]
        or sorted(
            {
                item["candidate_id"]
                for item in manifest["processing"]["remediation_checkpoints"]
            }
        )
        != journal["recheck_pending_issues"]
    ):
        raise _failure("feedback 再確認待ちの入力と終了記録が一致しません。")
    # pointer 切替前に保存していた生成物だけを回収する。raw と旧 active は消費しない。
    discard_staged_publication(context.repo, manifest, path)
    _record_unpublished_join(
        context,
        manifest,
        path,
        journal["completion"]["session_commit"],
        journal["recheck_pending_issues"],
    )


def _record_unpublished_join(
    context: EditingRunContext,
    manifest: dict[str, Any],
    path: Path,
    session_commit: str,
    recheck_pending_issues: list[str],
) -> None:
    """未公開のまま取り込んだ run と再確認対象を immutable な記録に残す。"""
    result_path = path.parent / "join_result.json"
    write_immutable_json(
        result_path,
        {
            "schema_version": 1,
            "publication": False,
            "identity": manifest["run"]["identity"],
            "session_commit": session_commit,
            "manifest": artifact_reference(context.repo, path),
            "recheck_pending_issues": recheck_pending_issues,
        },
    )
    update_primary_report_fields(
        publication_established=False, feedback_work_state=str(result_path)
    )


def require_manual_feedback_run(context: EditingRunContext) -> None:
    """自動 join 済み feedback run を明示 join/abandon で破棄させない。"""
    from .remediation import _failure, _validate_context

    if context.kind != "feedback_report":
        return
    finalization_path = feedback_root(context.repo) / "finalization.json"
    if finalization_path.exists() or finalization_path.is_symlink():
        raise _failure(
            "feedback run は自動 join 済みです。",
            [
                "`cmoc feedback report` で公開・再確認待ちの終了処理または cleanup を再開してください。"
            ],
        )
    work = load_report_cut(context.repo)
    if work is None:
        return
    manifest, _ = work
    _validate_context(context, manifest)
    run = manifest["run"]
    joined = run["merged"] is not None
    if not joined and run["join_intent"] is not None:
        record = load_join_record(context.repo, context.session_id)
        joined = record is not None and confirm_import(record)
    if joined:
        raise _failure(
            "feedback run は自動 join 済みです。",
            [
                "`cmoc feedback report` で公開・再確認待ちの終了処理または cleanup を再開してください。"
            ],
        )


def finish_manual_feedback_run(context: EditingRunContext, operation: str) -> None:
    """非 publication join は必要な checkpoint を保持し、abandon は work を破棄する。"""
    if context.kind != "feedback_report":
        return
    with feedback_writer_lock(context.repo):
        work = load_report_cut(context.repo)
        if work is None:
            return
        manifest, path = work
        from .remediation import _validate_context

        _validate_context(context, manifest)
        recover_report_cut_checkpoint_references(context.repo, manifest, path)
        if operation == "joined":
            # 次回の新規 report からは除外し、checkpoint の再利用で publication しない。
            _record_unpublished_join(
                context, manifest, path, head_commit(context.session_worktree), []
            )
            return
        logger = current_subcommand_logger()
        if logger is not None:
            logger.event(
                "feedback_run_manual_completion",
                operation=operation,
                run_identity=new_run_identity(context),
                session_commit=head_commit(context.session_worktree),
                publication=False,
                checkpoints=[
                    read_run_artifact(
                        context.repo,
                        {key: reference[key] for key in ("path", "sha256")},
                    )
                    for reference in manifest["processing"]["remediation_checkpoints"]
                ],
            )
        discard_report_cut(context.repo, manifest, path)
