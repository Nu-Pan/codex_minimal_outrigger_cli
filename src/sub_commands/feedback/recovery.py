"""Feedback publication 後の cleanup と明示 join/abandon の境界を扱う。

根拠: {{work-root}}/oracle/doc/app_spec/feedback_state.md の
「最新状態の atomic publication」と「run lifecycle との整合」。
"""

from pathlib import Path
from typing import Any

from cmoc_runtime import (
    RunPart,
    TerminalResult,
    branch_exists,
    head_commit,
    load_state_for_branch,
    require_clean_worktree,
    write_state,
)
from commons.runtime_feedback_run_state import new_run_identity, read_run_artifact
from commons.runtime_feedback_state import (
    _durable_unlink,
    _read_canonical_object,
    _require_exact_fields,
    artifact_reference,
    cleanup_published_report,
    current_pointer_path,
    discard_report_cut,
    feedback_writer_lock,
    load_report_cut,
    recover_report_cut_checkpoint_references,
    validate_feedback_state,
)
from commons.runtime_feedback_store import feedback_root, write_immutable_json
from commons.runtime_ids import is_common_id
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
from commons.runtime_run_join_state import confirm_import, join_record, load_join_record
from commons.runtime_run_lifecycle import EditingRunContext


def finish_feedback_run(
    context: EditingRunContext, manifest: dict[str, Any], result: TerminalResult
) -> TerminalResult:
    """work artifact を削除する前に最小の recovery journal を durable 保存する。"""
    from .remediation import _failure

    if result.primary_report is None:
        raise _failure("feedback finalization に durable report がありません。")
    completion = read_run_artifact(context.repo, manifest["run"]["completion"])
    merged = read_run_artifact(context.repo, manifest["run"]["merged"])
    path = feedback_root(context.repo) / "finalization.json"
    # journal には pointer だけを固定し、参照先の検証は lifecycle lock 内で一度行う。
    journal = {
        "schema_version": 1,
        "feedback_run_id": manifest["run"]["feedback_run_id"],
        "report_execution_id": manifest["run"]["targets"]["execution_id"],
        "identity": manifest["run"]["identity"],
        "report_cut_id": manifest["report_cut_id"],
        "report": artifact_reference(context.repo, result.primary_report),
        "current": _read_canonical_object(
            current_pointer_path(context.repo), "feedback current pointer"
        ),
        "completion": completion,
        "merged": merged,
        "result": result.result,
    }
    write_immutable_json(path, journal)
    return _finish_from_journal(_journal_context(context.repo, journal), journal, path)


def recover_finalization(repo: Path, session_branch: str) -> TerminalResult | None:
    """publication 後の cleanup を同じ報告書と join tree から再開する。"""
    path = feedback_root(repo) / "finalization.json"
    if not path.exists() and not path.is_symlink():
        return None
    journal = _read_canonical_object(path, "feedback finalization journal")
    context = _journal_context(repo, journal)
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
                report_path=str(repo / journal["report"]["path"]),
                publication_status="cleanup",
            )
        return _finish_from_journal(context, journal, path)


def _journal_context(repo: Path, journal: dict[str, Any]) -> EditingRunContext:
    """journal の保存先を active session と managed run の正規 path へ照合する。"""
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
        },
        path,
        "feedback finalization journal",
    )
    if (
        type(journal["schema_version"]) is not int
        or journal["schema_version"] != 1
        or not is_common_id(journal["feedback_run_id"], "fbr")
        or not is_common_id(journal["report_execution_id"], "exec")
        or journal["result"] not in {"ok", "attention", "incomplete"}
    ):
        raise _failure("feedback finalization journal の version/result が不正です。")
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
    return context


def _finish_from_journal(
    context: EditingRunContext, journal: dict[str, Any], path: Path
) -> TerminalResult:
    """raw/work cleanup、ready 遷移、隔離資源回収を idempotent に確定する。"""
    from .remediation import _failure

    # 呼び出し側で検証済みの identity を使い、lock 内では最新状態と再照合する。
    repo = context.repo
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
    completion = journal["completion"]
    if (
        completion.get("report_cut_id") != journal["report_cut_id"]
        or completion.get("checks")
        != {"reachability": True, "paths": True, "clean": True, "decision_basis": True}
        or journal["merged"].get("sealed") != completion.get("sealed")
    ):
        raise _failure("feedback finalization の join evidence が不正です。")
    with primary_report_finalization_lock(repo, context.session_id):
        # context 検証後に別 run が state を公開していないことを、変更操作の
        # 直前に同じ lifecycle lock 内でも確認する。
        context = _journal_context(repo, journal)
        _, _, initial_session = load_state_for_branch(repo, context.session_branch)
        state_before = current_primary_report_fields().get(
            "state_before", initial_session.run.state
        )

        def retain_failed_finalization() -> None:
            # journal を保持した自然完了経路は、手動 join/abandon へ切り替えない。
            restore_run_error(context)
            update_primary_report_fields(
                recovery_next_actions=(
                    "`cmoc feedback report` で未完了の publication または cleanup を再開してください。",
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
            # work artifact の cleanup と結果保存の後に state と隔離資源を回収する。
            from .report import save_feedback_invocation_report

            update_primary_report_fields(
                run_kind=context.kind,
                session_branch=context.session_branch,
                session_fork_commit=context.session_fork_commit,
                run_branch=context.run_branch,
                run_fork_commit=context.run_fork_commit,
                run_worktree=context.run_worktree,
                state_before=state_before,
                state_after="joinable",
                publication_established=True,
                publication_report=str(report_path),
                publication_result=journal["result"],
                feedback_run_id=journal["feedback_run_id"],
                report_cut_id=journal["report_cut_id"],
                publication_execution_id=journal["report_execution_id"],
                join_status="merged",
                join_preconditions="completed"
                if state_before == "ready"
                else "previously_completed",
                join_diff_validation="completed"
                if state_before == "ready"
                else "previously_completed",
                merge_status="merged"
                if journal["merged"]["run_join_commit"]
                else "no_op",
                run_join_commit=journal["merged"]["run_join_commit"],
                conflict_resolution=journal["merged"].get("resolution"),
                workload_post_join="completed",
                post_join_hook="none",
                refactor_state_sync_status="completed"
                if state_before == "ready"
                else "previously_completed",
                cleanup="pending",
                state_reset="not_run",
            )
            phase = "invocation report save"
            invocation_report = save_feedback_invocation_report(
                repo,
                "natural_completion",
                TerminalResult(result=journal["result"]),
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
                TerminalResult(result=journal["result"], warnings=tuple(warnings)),
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
                    "`cmoc feedback report` で未完了の publication または cleanup を再開してください。",
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
            report_path=str(report_path),
            state_after="ready",
            cleanup=cleanup,
            result=journal["result"],
        )
    return TerminalResult(
        primary_report=invocation_report,
        primary_report_role="feedback invocation report",
        result=journal["result"],
        details=(
            ("run_kind", "feedback_report"),
            ("run_join_commit", journal["merged"]["run_join_commit"]),
            ("post_join_hook", "none"),
            ("refactor_state_sync", "completed"),
            ("cleanup", cleanup),
        ),
        warnings=tuple(warnings),
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
                "`cmoc feedback report` で publication または cleanup を再開してください。"
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
                "`cmoc feedback report` で publication または cleanup を再開してください。"
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
            result_path = path.parent / "join_result.json"
            write_immutable_json(
                result_path,
                {
                    "schema_version": 1,
                    "publication": False,
                    "identity": manifest["run"]["identity"],
                    "session_commit": head_commit(context.session_worktree),
                    "manifest": artifact_reference(context.repo, path),
                },
            )
            update_primary_report_fields(
                publication_established=False, feedback_work_state=str(result_path)
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
