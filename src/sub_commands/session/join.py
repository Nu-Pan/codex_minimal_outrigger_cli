"""共通 merge lifecycle で session を home へ取り込み、session を完了する。"""

from pathlib import Path

from reference.request_builder.session.join.conflict_resolution import (
    build_session_join_conflict_resolution_request,
)

from cmoc_runtime import (
    CmocError,
    TerminalResult,
    branch_exists,
    current_branch,
    head_commit,
    load_state_for_branch,
    repo_root,
    require_clean_worktree,
    run_cli_subcommand,
    run_codex_exec,
    run_git,
    start_subcommand_step,
    work_root,
    write_state,
)
from commons.runtime_doctor import run_doctor_preprocess
from commons.runtime_join import (
    MergeContext,
    confirm_import,
    prepare_and_import,
    rollback_join_preparation,
)
from commons.runtime_primary_report import (
    primary_report_finalization_lock,
    set_primary_report_completion_handler,
    set_primary_report_save_failure_handler,
    update_primary_report_fields,
)
from commons.runtime_results import CodexExecCallable
from commons.runtime_run import delete_run_process_id
from commons.runtime_run_join_state import restore_pending_join
from commons.runtime_session_join import SessionJoinRecord, pending_session_join


def cmoc_session_join_impl() -> None:
    """CLI runtime を通して session join と、その後処理の復旧を実行する。"""
    run_cli_subcommand(
        _cmoc_session_join_body,
        run_codex_exec,
        command_name="session join",
        command_argv=["cmoc", "session", "join"],
        total_steps=4,
        use_work_root_runtime=True,
        doctor_preprocess=False,
    )


def _cmoc_session_join_body(codex_exec: CodexExecCallable) -> TerminalResult:
    """準備前は session、取り込み確定後は home から同じ join を再開する。"""
    root, work = repo_root(), work_root()
    branch = current_branch(work)
    pending = pending_session_join(root, work)
    source_branch = pending.context.source_branch if pending else branch
    session_id, path, state = load_state_for_branch(root, source_branch)
    warnings: list[str] = []
    with primary_report_finalization_lock(root, session_id):
        # lock 待ち前の状態を使わず、session と未完了の run を再検査する。
        pending = pending_session_join(root, work)
        branch = current_branch(work)
        source_branch = pending.context.source_branch if pending else branch
        if pending is None:
            restore_pending_join(root, source_branch)
        session_id, path, state = load_state_for_branch(root, source_branch)
        home = state.session.session_home_branch
        update_primary_report_fields(
            session_branch=source_branch,
            home_branch=home,
            session_state_before=state.session.state,
            session_state_after=state.session.state,
        )
        start_subcommand_step(1, "事前条件と復旧情報を確認", "validate join recovery")
        if not source_branch.startswith("cmoc/session/") or not home:
            raise CmocError("session join の対象を特定できません。", [], source_branch)
        if state.run.state != "ready" or state.session.state not in (
            {"active", "joined", "error"} if pending else {"active"}
        ):
            raise CmocError(
                "session join の事前条件を満たしていません。", [], str(path)
            )
        if branch not in ({source_branch, home} if pending else {source_branch}):
            raise CmocError(
                "session join の作業 branch が変更されています。", [], branch
            )
        if pending is not None and pending.context.source_branch != source_branch:
            raise CmocError("session join の復旧対象が変更されています。", [], "")
        record = pending
        try:
            if record is not None and not confirm_import(record):
                rollback_join_preparation(record)
            if record is None or not record.imported:
                if not branch_exists(root, home):
                    raise CmocError("session home branch が存在しません。", [], home)
                require_clean_worktree(work)
                # doctor の管理更新も共通の準備変更として記録し、失敗時に元へ戻す。
                if record is None:
                    record = SessionJoinRecord(
                        MergeContext(root, session_id, source_branch, work, home, work),
                        original_source_head=head_commit(work),
                    )
                record.preparation_started = True
                record.pending_action = "doctor"
                record.save()
                start_subcommand_step(2, "doctor preprocess", "doctor preprocess")
                run_doctor_preprocess(
                    work, sync_refactor_entries=False, session_join_preparation=True
                )
                start_subcommand_step(
                    3,
                    "session で準備して home へ取り込む",
                    "prepare and import session",
                )
                prepare_and_import(
                    record,
                    build_session_join_conflict_resolution_request,
                    warnings=warnings,
                    codex_exec=codex_exec,
                )
            else:
                # 取り込み済みの復旧で doctor・同期・merge を繰り返さない。
                require_clean_worktree(work)
                if current_branch(work) != home:
                    run_git(["switch", "--no-guess", home], work)
            update_primary_report_fields(
                **record.report_fields(), branch_switch_status="completed"
            )
            # session 固有の state と資源回収だけを、この層で確定する。
            start_subcommand_step(4, "session を完了", "finish session join")
            state.session.state = "joined"
            write_state(path, state)
            update_primary_report_fields(
                session_state_after="joined", state_update_status="completed"
            )
            set_primary_report_save_failure_handler(
                lambda: _mark_session_error(path, source_branch, root, record)
            )
            deleted = not branch_exists(root, source_branch)
            if not deleted:
                source_matches = (
                    run_git(
                        ["rev-parse", "--verify", f"refs/heads/{source_branch}"], root
                    ).stdout.strip()
                    == record.prepared_head
                )
                reachable = (
                    run_git(
                        ["merge-base", "--is-ancestor", source_branch, home],
                        root,
                        check=False,
                    ).returncode
                    == 0
                )
                if source_matches and reachable:
                    deleted = (
                        run_git(
                            ["branch", "-d", source_branch], work, check=False
                        ).returncode
                        == 0
                    )
                if not deleted:
                    warnings.append(f"session branch was not deleted: {source_branch}")
            update_primary_report_fields(
                session_branch_cleanup_status="completed" if deleted else "warning"
            )
            delete_run_process_id(root, session_id)

            def finish() -> None:
                record.finished = True
                record.save()

            if not set_primary_report_completion_handler(finish):
                finish()
            return TerminalResult(
                details=(
                    ("session_id", session_id),
                    ("joined_to", home),
                    ("deleted_session_branch", deleted),
                ),
                warnings=tuple(warnings),
            )
        except BaseException as exc:
            if record is not None:
                try:
                    rollback_join_preparation(record)
                    # 復旧を完了した失敗では session の通常編集と、新しい試行を許可する。
                    if not record.imported:
                        record.finished = True
                        record.save()
                        state.session.state = "active"
                        write_state(path, state)
                        update_primary_report_fields(session_state_after="active")
                        delete_run_process_id(root, session_id)
                    else:
                        _mark_session_error(path, source_branch, root, record)
                except BaseException as recovery_error:
                    update_primary_report_fields(
                        merge_rollback="failed", rollback_error=repr(recovery_error)
                    )
                    _mark_session_error(path, source_branch, root, record)
                update_primary_report_fields(**record.report_fields())
            detail = exc.detail if isinstance(exc, CmocError) else repr(exc)
            raise CmocError(
                exc.summary
                if isinstance(exc, CmocError)
                else "session join に失敗しました。",
                [
                    *(exc.next_actions if isinstance(exc, CmocError) else []),
                    "未解消理由と残存差分を確認し、`cmoc session join` で再試行してください。",
                ],
                detail,
            ) from exc


def _mark_session_error(
    path: Path, source_branch: str, root: Path, record: SessionJoinRecord
) -> None:
    """取り込み済みの結果と削除済み資源を保持し、後処理の再開を可能にする。"""
    record.finished = False
    record.save()
    _, _, current = load_state_for_branch(root, source_branch)
    current.session.state = "error"
    write_state(path, current)
    update_primary_report_fields(session_state_after="error")
