"""停止要求まで巡回し、検証済みの refactor 成果を確定する workload。"""

import sys
import time
from collections.abc import Collection
from dataclasses import dataclass, field
from pathlib import Path
from typing import NoReturn, TypedDict, cast

from acp.builder.realization.refactor.fork.file_review_and_fix import (
    build_realization_refactor_fork_file_review_and_fix_parameter,
)
from cmoc_runtime import (
    CmocError,
    TerminalResult,
    console_timestamp,
    current_subcommand_logger,
    file_sha256,
    load_config,
    mark_current_subcommand_interrupted,
    refactor_state_path,
    run_cli_subcommand,
    run_codex_exec,
    run_doctor_preprocess,
    run_git,
    start_subcommand_step,
    timestamp,
    work_root,
)
from commons.runtime_codex_recovery import (
    check_recovery_interruption,
    defer_recovery_interruption,
)
from commons.runtime_primary_report import update_primary_report_fields
from commons.runtime_primary_report_render import yaml_scalar
from commons.runtime_refactor import (
    RefactorState,
    load_refactor_state,
    mark_all_refactor_targets_required,
    refactor_cycle_targets,
    sync_refactor_state,
    write_refactor_state,
)
from commons.runtime_results import StructuredOutputValidationIssue
from commons.runtime_run import (
    read_run_process_id,
    run_process_tracking,
    stop_tracked_codex_children,
)
from commons.runtime_run_lifecycle import (
    EditingRunContext,
    GitChange,
    commit_work_unit,
    flattened_change_paths,
    recover_started_run,
    rollback_work_unit,
    session_run_was_ready,
    set_run_error_after_joinable_publication,
    set_run_state,
    start_editing_run,
    tree_changes,
    unexpected_agent_paths,
    unexpected_run_paths,
    worktree_change_paths,
)
from commons.runtime_run_report import _render_changed_path, write_fork_report

_UnresolvedFinding = tuple[str, str, Path]


class _FindingResolution(TypedDict):
    status: str
    summary: str
    verification: str


class _Finding(TypedDict):
    title: str
    changed_paths: list[str]
    resolution: _FindingResolution


class _Verification(TypedDict):
    status: str
    summary: str


class _FileReviewOutput(TypedDict):
    findings: list[_Finding]
    verification: _Verification


class _ChangeSummary(TypedDict):
    category: str
    summary: str
    changed_paths: list[str]


@dataclass
class _RefactorProgress:
    cycle: int = 0
    completed_cycles: int = 0
    phase: str = "doctor preprocess"
    targets: set[str] = field(default_factory=set)
    processed: set[str] = field(default_factory=set)
    deferred: set[str] = field(default_factory=set)
    records: list[str] = field(default_factory=list)
    baseline: str | None = None
    agent_head: str | None = None
    termination_phase: str | None = None
    summaries: list[_ChangeSummary] = field(default_factory=list)
    committed_paths: set[str] = field(default_factory=set)


def cmoc_realization_refactor_fork_impl() -> None:
    """CLI runtime を通して realization refactor fork を実行する。"""
    run_cli_subcommand(
        _cmoc_realization_refactor_fork_body,
        command_name="realization refactor fork",
        command_argv=["cmoc", "realization", "refactor", "fork"],
        # {{work-root}}/oracle/doc/app_spec/subcommand_interruption.md
        interruptible=True,
        doctor_preprocess=False,
        total_steps=6,
    )


def _cmoc_realization_refactor_fork_body() -> TerminalResult:
    """realization file を順に調査・修正し、結果を joinable run として公開する。"""
    context: EditingRunContext | None = None
    units: list[tuple[str, int]] = []
    unresolved_findings: dict[str, list[_UnresolvedFinding]] = {}
    cleanup_warnings: list[str] = []
    joinable_publication_attempted = False
    start_attempted = False
    start_was_ready = False
    progress = _RefactorProgress()
    try:
        # 前処理も fork の停止・rollback 契約に含め、未完了を成功にしない。
        start_subcommand_step(1, "doctor preprocess", "doctor preprocess")
        run_doctor_preprocess(work_root(), rollback_on_interruption=True)
        check_recovery_interruption()
        progress.phase = "create run"
        start_subcommand_step(2, "realization refactor run を作成", "create run")
        start_was_ready = session_run_was_ready()
        start_attempted = True
        context = start_editing_run("realization_refactor")
        progress.baseline = context.run_fork_commit
        update_primary_report_fields(
            run_kind=context.kind,
            session_branch=context.session_branch,
            session_fork_commit=context.session_fork_commit,
            run_branch=context.run_branch,
            run_fork_commit=context.run_fork_commit,
            run_worktree=context.run_worktree,
            state_before=context.state_before,
            state_after="running",
            refactor_state_path=refactor_state_path(context.run_worktree),
        )
        # {{work-root}}/oracle/doc/app_spec/sub_command/editing_run.md
        # fork 内の Codex call を同じ process tracking scope に置き、
        # interrupt/abandon から停止可能にする。
        with run_process_tracking(context.repo, context.session_id):
            while True:
                check_recovery_interruption()
                progress.phase = "initialize cycle"
                pending = _initialize_cycle(context, progress=progress)
                _emit_refactor_progress(progress)
                start_subcommand_step(
                    4, "file 単位の調査と修正を実行", "run refactor loop"
                )
                for target in pending:
                    check_recovery_interruption()
                    state = load_refactor_state(context.run_worktree)
                    progress.targets.intersection_update(
                        set(state) | progress.processed
                    )
                    if target not in state:
                        continue
                    progress.phase = f"review / edit / verify (uncommitted): {target}"
                    _emit_refactor_progress(progress)
                    _run_refactor_unit(
                        context,
                        target,
                        units,
                        unresolved_findings,
                        cleanup_warnings,
                        progress=progress,
                    )
                    _emit_refactor_progress(progress)
                progress.completed_cycles = progress.cycle
                progress.phase = "cycle completed"
                _emit_refactor_progress(progress)
                # 空対象でも停止を受け付けながら再同期する。通常の停止条件は設けない。
                if not pending:
                    time.sleep(0.1)
    except KeyboardInterrupt as interruption:
        if context is None:
            # {{work-root}}/oracle/doc/app_spec/sub_command/editing_run.md
            # fork の共通事前条件失敗では、既存の error run をこの fork の
            # 中断対象として回収してはならない。context 返却前の start failure
            # だけを、公開済み run の回収対象にする。
            if start_attempted and start_was_ready:
                context = _recover_refactor_start(interruption)
            if context is None:
                # {{work-root}}/oracle/doc/app_spec/subcommand_interruption.md
                # run 作成前の fork lifecycle であっても Ctrl+C は正常な中断として
                # 終了し、共通 runner に子 process の失敗として扱わせない。
                mark_current_subcommand_interrupted()
                logger = current_subcommand_logger()
                if logger is not None:
                    logger.event("user_interruption", result="interrupted")
                update_primary_report_fields(
                    completion_reason="user_interruption",
                    refactor_stage=progress.phase,
                    rollback_status="startup rolled back; run not established",
                )
                return TerminalResult(
                    completion_reason="user_interruption",
                    details=(("stage", progress.phase), ("run", "not established")),
                )
        # 中断後の追加 SIGINT は整合化を壊さず、停止完了を rollback の前提にする。
        with defer_recovery_interruption(check_pending=False, propagate=False):
            cleanup_errors = _stop_and_rollback(context, cleanup_warnings, progress)
        with defer_recovery_interruption(check_pending=False, propagate=False):
            if cleanup_errors:
                _raise_refactor_interruption_error(
                    context,
                    units,
                    unresolved_findings,
                    interruption,
                    [*cleanup_warnings, *cleanup_errors],
                    progress=progress,
                )
            try:
                joinable_publication_attempted = True
                set_run_state(context, "joinable")
                update_primary_report_fields(
                    state_after="joinable",
                    completion_reason="user_interruption",
                )
            except BaseException as state_error:
                cleanup_errors.append(f"state update failed: {state_error!r}")
                _raise_refactor_interruption_error(
                    context,
                    units,
                    unresolved_findings,
                    interruption,
                    [*cleanup_warnings, *cleanup_errors],
                    progress=progress,
                    joinable_publication_attempted=joinable_publication_attempted,
                )
            try:
                report = _write_refactor_report(
                    context,
                    "joinable",
                    "user_interruption",
                    units,
                    unresolved_findings,
                    summary=None,
                    cleanup_errors=cleanup_warnings,
                    progress=progress,
                )
            except BaseException as report_error:
                cleanup_errors.append(f"interruption report failed: {report_error!r}")
                _raise_refactor_interruption_error(
                    context,
                    units,
                    unresolved_findings,
                    interruption,
                    [*cleanup_warnings, *cleanup_errors],
                    progress=progress,
                    joinable_publication_attempted=joinable_publication_attempted,
                )
            # {{work-root}}/oracle/doc/app_spec/windows_toast_notification.md
            mark_current_subcommand_interrupted()
            return _completion_result(
                "user_interruption",
                unresolved_findings,
                report,
                cleanup_warnings,
                progress=progress,
            )
    except BaseException as exc:
        if context is None:
            # {{work-root}}/oracle/doc/app_spec/sub_command/editing_run.md
            # 事前条件が ready でなかった場合は既存 run を回収しない。ready を
            # 確認後に別 invocation が先に run を公開しただけの CmocError には
            # 公開済み context が付かないため、その run を回収対象として扱わない。
            if start_attempted and start_was_ready:
                context = _recover_refactor_start(exc)
            if context is None:
                raise
        with defer_recovery_interruption(check_pending=False, propagate=False):
            error_cleanup_errors = _stop_and_rollback(
                context, cleanup_warnings, progress
            )
            _set_refactor_error_state(
                context,
                error_cleanup_errors,
                joinable_publication_attempted=joinable_publication_attempted,
            )
            _raise_refactor_error(
                context,
                units,
                unresolved_findings,
                exc,
                [*cleanup_warnings, *error_cleanup_errors],
                progress=progress,
            )


def _recover_refactor_start(error: BaseException) -> EditingRunContext | None:
    """この invocation が公開した run だけを開始処理の失敗から回収する。"""
    published = getattr(error, "_published_editing_run_context", None)
    if isinstance(published, EditingRunContext):
        return published
    if isinstance(error, CmocError):
        return None
    context = recover_started_run("realization_refactor")
    if context is not None and read_run_process_id(context.repo, context.session_id):
        return context
    # 未記録の並行 run を取り込まず、tracking 失敗時の自身の run は上の
    # 明示的な published context を使って停止失敗として扱う。
    return None


def _stop_and_rollback(
    context: EditingRunContext,
    warnings: list[str],
    progress: _RefactorProgress,
) -> list[str]:
    """書き込み得る子 process の停止を確認してから未確定作業を取り消す。"""
    # 停止確認に失敗した場合は tree を触らず、追跡情報と復旧用資源を保持する。
    progress.termination_phase = progress.phase
    progress.phase = "stop requested; stopping children"
    _emit_refactor_progress(progress)
    try:
        warnings.extend(
            stop_tracked_codex_children(context.repo, context.session_id) or []
        )
    except BaseException as exc:
        progress.phase = "child stop failed; rollback not attempted"
        detail = exc.detail if isinstance(exc, CmocError) else repr(exc)
        return [f"Codex child stop failed: {exc!r}; {detail}; rollback not attempted"]
    history_errors: list[str] = []
    if progress.agent_head is not None:
        try:
            _ensure_agent_did_not_commit(context.run_worktree, progress.agent_head)
        except BaseException as exc:
            try:
                head = run_git(
                    ["rev-parse", "HEAD"], context.run_worktree
                ).stdout.strip()
            except BaseException as head_error:
                return [f"agent history recovery: {exc!r}; {head_error!r}"]
            if head != progress.agent_head:
                return [f"agent history recovery: {exc!r}"]
            # 禁止された commit を除去できた場合も、残る追加 file 等を rollback する。
            history_errors.append(f"agent commit rejected; HEAD restored: {exc!r}")
    progress.phase = "rollback uncommitted work"
    _emit_refactor_progress(progress)
    try:
        rollback_work_unit(context.run_worktree)
    except BaseException as exc:
        progress.phase = "rollback failed"
        return [*history_errors, f"rollback failed: {exc!r}"]
    progress.records.append("- cleanup: children stopped; uncommitted work rolled back")
    return history_errors


def _emit_refactor_progress(progress: _RefactorProgress) -> None:
    """巡の確定実績と未確定作業、利用可能な計測の状態を表示する。"""
    # 呼出しの所要時間を full test の測定に読み替えない。
    latest_change = progress.summaries[-1]["summary"] if progress.summaries else "none"
    print(
        f"# {console_timestamp()} refactor cycle {progress.cycle}: {progress.phase}; "
        f"targets={len(progress.targets)}, confirmed={len(progress.processed)}, "
        f"pending={len(progress.targets - progress.processed)}, "
        f"deferred={len(progress.deferred)}; "
        f"confirmed changes={len(progress.committed_paths)} paths; "
        f"latest confirmed change={latest_change[:160]!r}; "
        f"test timing: unavailable (no comparable completed measurement); "
        f"baseline={progress.baseline}",
        file=sys.stderr,
        flush=True,
    )
    update_primary_report_fields(refactor_stage=progress.phase)
    logger = current_subcommand_logger()
    if logger is not None:
        logger.event(
            "refactor_progress",
            cycle=progress.cycle,
            phase=progress.phase,
            total=len(progress.targets),
            confirmed=len(progress.processed),
            pending=len(progress.targets - progress.processed),
            deferred=len(progress.deferred),
            confirmed_changed_path_count=len(progress.committed_paths),
            latest_confirmed_change=latest_change,
            test_timing="unavailable",
            baseline_revision=progress.baseline,
        )


def _raise_refactor_interruption_error(
    context: EditingRunContext,
    units: list[tuple[str, int]],
    unresolved_findings: dict[str, list[_UnresolvedFinding]],
    interruption: BaseException,
    cleanup_errors: list[str],
    *,
    joinable_publication_attempted: bool = False,
    progress: _RefactorProgress | None = None,
) -> NoReturn:
    """中断後の cleanup failure を error state/report へ変換する。"""
    _set_refactor_error_state(
        context,
        cleanup_errors,
        joinable_publication_attempted=joinable_publication_attempted,
    )
    _raise_refactor_error(
        context,
        units,
        unresolved_findings,
        interruption,
        cleanup_errors,
        progress=progress,
    )


def _raise_refactor_error(
    context: EditingRunContext,
    units: list[tuple[str, int]],
    unresolved_findings: dict[str, list[_UnresolvedFinding]],
    error: BaseException,
    cleanup_errors: list[str],
    *,
    progress: _RefactorProgress | None = None,
) -> NoReturn:
    """error state の refactor report と CLI error を一貫して生成する。"""
    report = _write_refactor_report(
        context,
        "error",
        "error",
        units,
        unresolved_findings,
        summary=None,
        error=error,
        cleanup_errors=cleanup_errors,
        progress=progress,
    )
    terminal_result = _completion_result(
        "error", unresolved_findings, report, cleanup_errors, progress=progress
    )
    cmoc_error = CmocError(
        "realization refactor fork は error state で停止しました。",
        list(terminal_result.next_actions),
        f"report: {report}\nerror: {error!r}",
        terminal_result=terminal_result,
    )
    raise cmoc_error from error


def _set_refactor_error_state(
    context: EditingRunContext,
    cleanup_errors: list[str],
    *,
    joinable_publication_attempted: bool,
) -> None:
    """refactor の失敗を許可済み terminal 遷移として保存する。"""
    state_updated = False
    try:
        set_run_state(context, "error")
        state_updated = True
    except BaseException as state_error:
        if joinable_publication_attempted:
            try:
                set_run_error_after_joinable_publication(context)
                state_updated = True
            except BaseException as recovery_error:
                cleanup_errors.append(
                    f"state update failed: {state_error!r}; "
                    f"joinable publication recovery failed: {recovery_error!r}"
                )
        else:
            cleanup_errors.append(f"state update failed: {state_error!r}")
    if state_updated:
        try:
            update_primary_report_fields(
                state_after="error",
                completion_reason="error",
            )
        except BaseException as report_state_error:
            cleanup_errors.append(
                f"primary report state update failed: {report_state_error!r}"
            )


def _initialize_cycle(
    context: EditingRunContext, *, progress: _RefactorProgress | None = None
) -> list[str]:
    """全対象へ調査要求を設定し、引継ぎ要求を先にする巡の順序を返す。"""
    # 履歴と新目的での調査機会を分離し、同期・列挙は確定区間の外で行う。
    state = sync_refactor_state(context.run_worktree)
    pending = refactor_cycle_targets(state)
    mark_all_refactor_targets_required(state)
    write_refactor_state(context.run_worktree, state)
    unexpected = _unexpected_refresh_paths(
        context,
        [],
        worktree_change_paths(context.run_worktree, include_rename_sources=True),
    )
    if unexpected:
        raise CmocError(
            "refactor cycle に想定外差分があります。",
            ["run worktree の差分を確認してください。"],
            "\n".join(unexpected),
        )
    with defer_recovery_interruption():
        commit_work_unit(context.run_worktree, "cmoc realization refactor cycle")
        if progress is not None:
            progress.cycle += 1
            progress.targets = set(pending)
            progress.processed.clear()
            progress.deferred.clear()
    return pending


def _run_refactor_unit(
    context: EditingRunContext,
    target: str,
    units: list[tuple[str, int]],
    unresolved_findings: dict[str, list[_UnresolvedFinding]],
    cleanup_warnings: list[str],
    *,
    progress: _RefactorProgress | None = None,
) -> None:
    """単一 target の agent call、差分検証、state 更新、commit を実行する。"""
    target_path = context.run_worktree / target
    if not (target_path.is_file() or target_path.is_symlink()):
        sync_refactor_state(context.run_worktree)
        all_unit_paths = worktree_change_paths(
            context.run_worktree,
            include_rename_sources=True,
        )
        unexpected = _unexpected_refactor_unit_paths(
            context,
            changed_agent_paths=[],
            pending_paths=all_unit_paths,
        )
        if unexpected:
            raise CmocError(
                "refactor 処理単位に想定外差分があります。",
                ["run worktree の差分を確認してください。"],
                "\n".join(unexpected),
            )
        with defer_recovery_interruption():
            commit_work_unit(
                context.run_worktree, f"cmoc realization refactor sync {target}"
            )
        if progress is not None:
            progress.targets.discard(target)
        return
    investigated_hash = file_sha256(target_path)
    state_paths_before = set(load_refactor_state(context.run_worktree))
    agent_head = run_git(["rev-parse", "HEAD"], context.run_worktree).stdout.strip()

    if progress is not None:
        progress.agent_head = agent_head
    parameter = build_realization_refactor_fork_file_review_and_fix_parameter(
        target_path,
        context.run_worktree,
    )
    result = run_codex_exec(
        parameter,
        root=context.repo,
        config=load_config(context.run_worktree),
        purpose=f"realization refactor: {target}",
        structured_output_postcondition=lambda output, changed_paths: (
            _changed_path_postcondition(context, output, changed_paths)
        ),
    )
    # HEAD の復元や差分検査より先に、書き込み得る child の停止を確認する。
    cleanup_warnings.extend(
        stop_tracked_codex_children(context.repo, context.session_id) or []
    )
    _ensure_agent_did_not_commit(context.run_worktree, agent_head)
    if progress is not None:
        progress.agent_head = None
    check_recovery_interruption()
    if result.returncode != 0:
        raise CmocError(
            "refactor agent が正常終了しませんでした。",
            ["Codex call log を確認してください。"],
            f"target: {target}\nreturncode: {result.returncode}",
        )
    # file_review_and_fix.json で検証済みの値を、利用境界で一度だけ狭める。
    file_review_output = cast(_FileReviewOutput, result.output_json)
    findings = file_review_output["findings"]
    actual_changed_paths = worktree_change_paths(
        context.run_worktree,
        include_rename_sources=True,
    )
    unexpected = unexpected_agent_paths(context, actual_changed_paths)
    if unexpected:
        # {{work-root}}/oracle/doc/app_spec/sub_command/realization_refactor.md
        # state は cmoc が更新するため、agent call 直後に realization
        # file 以外の差分を拒否し、agent の変更を cmoc の更新として取り込まない。
        raise CmocError(
            "refactor agent が realization file 以外を変更しました。",
            ["Codex call log と run worktree の差分を確認してください。"],
            "\n".join(unexpected),
        )
    # 構文補正とは別の確定条件。検証不足の変更を state とともに積み上げない。
    verification = file_review_output["verification"]
    if actual_changed_paths and verification["status"] != "passed":
        raise CmocError(
            "refactor 変更の品質検証が完了していません。",
            ["Codex call log の検証結果を確認してください。"],
            f"target: {target}\nverification: {verification}",
        )
    check_recovery_interruption()
    normalized_findings = findings
    if (
        findings
        and not actual_changed_paths
        and all(
            finding.get("resolution", {}).get("status") == "fixed"
            for finding in findings
        )
    ):
        # {{work-root}}/oracle/doc/app_spec/sub_command/realization_refactor.md
        # net 差分のない fixed 自己申告は、実行記録を保ったまま処理判定だけを
        # 所見なしへ正規化する。
        normalized_findings = []
    unresolved = [
        finding
        for finding in normalized_findings
        if finding.get("resolution", {}).get("status") == "unresolved"
    ]
    declared_changed_paths = tuple(
        finding["changed_paths"] for finding in normalized_findings
    )
    _update_refactor_state(
        context,
        target,
        investigated_hash,
        bool(normalized_findings),
        actual_changed_paths,
    )
    all_unit_paths = worktree_change_paths(
        context.run_worktree,
        include_rename_sources=True,
    )
    unexpected = _unexpected_refactor_unit_paths(
        context,
        changed_agent_paths=actual_changed_paths,
        pending_paths=all_unit_paths,
    )
    if unexpected:
        raise CmocError(
            "refactor 処理単位に想定外差分があります。",
            ["run worktree の差分を確認してください。"],
            "\n".join(unexpected),
        )
    unresolved_details = [
        (
            str(finding.get("title", "")),
            str(finding.get("resolution", {}).get("summary", "")),
            result.call_log_path.resolve(),
        )
        for finding in unresolved
    ]
    _commit_refactor_unit(
        context,
        target,
        len(normalized_findings),
        unresolved_details,
        units,
        unresolved_findings,
        f"cmoc realization refactor {target}",
        pending_realization_paths=actual_changed_paths,
        state_paths_before=state_paths_before,
        declared_changed_paths=declared_changed_paths,
        progress=progress,
        verification=verification,
        finding_summaries=[
            f"{finding['title']}: {finding['resolution']['status']}: "
            f"{finding['resolution']['summary']}"
            for finding in normalized_findings
        ],
        call_log_path=getattr(result, "call_log_path", None),
    )


def _ensure_agent_did_not_commit(worktree: Path, before_head: str) -> None:
    """agent call 中の commit を開始前の run tree へ戻して拒否する。"""
    after_head = run_git(["rev-parse", "HEAD"], worktree).stdout.strip()
    if after_head == before_head:
        return
    try:
        run_git(["reset", "--hard", before_head], worktree)
    except BaseException as reset_error:
        raise CmocError(
            "refactor agent が commit を作成し、差分を戻せませんでした。",
            ["run worktree の git history と Codex call log を確認してください。"],
            f"before HEAD: {before_head}\nafter HEAD: {after_head}\n"
            f"reset error: {reset_error!r}",
        ) from reset_error
    raise CmocError(
        "refactor agent が git commit を実行しました。",
        ["agent の commit を取り除いてから refactor fork を再実行してください。"],
        f"before HEAD: {before_head}\nafter HEAD: {after_head}",
    )


def _commit_refactor_unit(
    context: EditingRunContext,
    target: str,
    finding_count: int,
    unresolved: list[_UnresolvedFinding],
    units: list[tuple[str, int]],
    unresolved_findings: dict[str, list[_UnresolvedFinding]],
    message: str,
    *,
    pending_realization_paths: Collection[str] = (),
    state_paths_before: Collection[str] = (),
    declared_changed_paths: Collection[Collection[str]] = (),
    progress: _RefactorProgress | None = None,
    verification: _Verification | None = None,
    finding_summaries: Collection[str] = (),
    call_log_path: Path | None = None,
) -> None:
    """commit 済み処理単位の report 進捗を interruption 前に公開する。

    commit 後、呼び出し元へ戻る前にも Ctrl+C が届く。HEAD が進んだ場合は
    その処理単位を確定済みとして記録してから中断処理へ戻し、report の進捗を
    実際の run branch と一致させる。

    根拠: {{work-root}}/oracle/doc/app_spec/sub_command/realization_refactor.md
    """
    # state の読み取りは長い同期と同様、停止可能な準備として区間の外に置く。
    state = load_refactor_state(context.run_worktree)
    if progress is not None:
        progress.phase = f"commit artifacts / refactor state: {target}"
        _emit_refactor_progress(progress)
    with defer_recovery_interruption():
        before_head = run_git(
            ["rev-parse", "HEAD"], context.run_worktree
        ).stdout.strip()
        commit_result: str | None = None
        try:
            commit_result = commit_work_unit(context.run_worktree, message)
        finally:
            # commit_work_unit が返した hash は、commit 成功後の HEAD probe より確定度が
            # 高い。probe 直前の Ctrl+C で、既に commit 済みの処理単位を report から
            # 取り落とさないよう、成功時はその hash をそのまま tree_changes へ渡す。
            after_head: str | None = commit_result
            if after_head is None:
                head_probe = run_git(
                    ["rev-parse", "HEAD"], context.run_worktree, check=False
                )
                if head_probe.returncode == 0:
                    after_head = head_probe.stdout.strip()
            if after_head is not None and after_head != before_head:
                units.append((target, finding_count))
                if progress is not None:
                    progress.processed.add(target)
                    progress.targets.intersection_update(
                        set(state) | progress.processed
                    )
                    if progress.targets <= progress.processed:
                        progress.completed_cycles = progress.cycle
                    progress.committed_paths.update(pending_realization_paths)
                    if unresolved:
                        progress.deferred.add(target)
                    progress.phase = f"confirmed: {target} ({finding_count} findings; {len(pending_realization_paths)} changed paths)"
                    progress.records.extend(
                        [
                            f"- target: {target!r}; commit: `{after_head}`; findings: {finding_count}",
                            f"  - changed paths: {sorted(pending_realization_paths)!r}",
                            f"  - verification: {verification!r}",
                            f"  - resolutions: {list(finding_summaries)!r}",
                            f"  - Codex call log: {call_log_path}",
                        ]
                    )
                    progress.summaries.extend(
                        {
                            "category": "confirmed",
                            "summary": finding,
                            "changed_paths": list(pending_realization_paths),
                        }
                        for finding in finding_summaries
                        if pending_realization_paths
                    )
                unresolved_before = dict(unresolved_findings)
                try:
                    committed_changes = tree_changes(
                        context.run_worktree,
                        before_head,
                        after_head,
                    )
                    rename_paths = {
                        change.paths[0]: change.paths[1]
                        for change in committed_changes
                        if change.status.startswith("R") and len(change.paths) == 2
                    }
                    if declared_changed_paths:
                        # {{work-root}}/oracle/doc/app_spec/sub_command/realization_refactor.md
                        # Git は内容の変更量が大きい rename を delete/add として記録する。
                        # 後続 target の call が以前の unresolved target を rename した場合
                        # もあるため、current target だけでなく commit 前から unresolved だった
                        # path も対応付ける。old/new が同じ finding の changed_paths に含まれ、
                        # 新しい state entry が一つだけのときに限って対応を確定する。
                        new_state_paths = {
                            path
                            for path in pending_realization_paths
                            if path != target
                            and path in state
                            and path not in state_paths_before
                        }
                        sources = [target, *unresolved_findings]
                        for source in sources:
                            if (
                                source in rename_paths
                                or source not in state_paths_before
                                or source in state
                            ):
                                continue
                            candidates = {
                                path
                                for changed_paths in declared_changed_paths
                                if source in changed_paths
                                for path in changed_paths
                                if path in new_state_paths
                            }
                            candidates.difference_update(rename_paths.values())
                            if len(candidates) == 1:
                                rename_paths[source] = next(iter(candidates))
                    _reconcile_unresolved_findings(
                        state,
                        rename_paths,
                        unresolved_findings,
                    )
                    unresolved_findings.pop(rename_paths.get(target, target), None)
                    if progress is not None:
                        progress.deferred = {
                            rename_paths.get(path, path)
                            for path in progress.deferred
                            if rename_paths.get(path, path) in state
                        }
                    if unresolved:
                        # commit 済みの対象だけを current fork 内で保留し、次の対象へ進む。
                        unresolved_target = rename_paths.get(target, target)
                        if unresolved_target in state:
                            unresolved_findings[unresolved_target] = unresolved
                except BaseException:
                    # {{work-root}}/oracle/doc/app_spec/subcommand_interruption.md
                    # commit 後の差分 inspection 中断でも、確定済み finding を report から
                    # 失わない。rename の確定前は旧 target を保守的に保持する。
                    unresolved_findings.clear()
                    unresolved_findings.update(unresolved_before)
                    # rename を確認できなくても、今回の確定結果が同じ起点の
                    # 過去の未解決所見を置き換えた事実は保持する。
                    unresolved_findings.pop(target, None)
                    if unresolved:
                        unresolved_findings[target] = unresolved
                    raise


def _reconcile_unresolved_findings(
    state: RefactorState,
    rename_paths: dict[str, str],
    unresolved_findings: dict[str, list[_UnresolvedFinding]],
) -> None:
    """commit 後の state path に current fork の unresolved を揃える。"""
    # {{work-root}}/oracle/doc/app_spec/sub_command/realization_refactor.md
    # rename は state 上で旧 path の削除と新 path の追加になるため、commit 前の
    # target key をそのまま保持すると report の未解決集合が不一致になる。
    for target in list(unresolved_findings):
        current_target = rename_paths.get(target, target)
        findings = unresolved_findings.pop(target)
        if current_target in state:
            unresolved_findings[current_target] = findings


def _status_change(path: str) -> GitChange:
    """未 commit path を共通の差分分類へ渡す最小 GitChange にする。"""
    return GitChange("M", (path,))


def _unexpected_refactor_unit_paths(
    context: EditingRunContext,
    *,
    changed_agent_paths: Collection[str],
    pending_paths: Collection[str],
) -> list[str]:
    """処理単位の commit 前に想定外の run worktree 差分を返す。"""
    pending = list(pending_paths)
    unexpected = unexpected_run_paths(
        context,
        # {{work-root}}/oracle/doc/app_spec/sub_command/realization_refactor.md
        # status と tree diff の分類は path 単位で同じなので一時 change として扱う。
        [_status_change(path) for path in pending],
    )
    unexpected.extend(
        _unexpected_refresh_paths(context, list(changed_agent_paths), pending)
    )
    return sorted(set(unexpected))


def _unexpected_refresh_paths(
    context: EditingRunContext,
    changed_agent_paths: list[str],
    pending_paths: list[str],
) -> list[str]:
    """state 同期後に増えた cmoc 管理外の差分を返す。"""
    refactor_state = refactor_state_path(context.run_worktree).relative_to(
        context.run_worktree
    )
    agent_paths = set(changed_agent_paths)
    return sorted(
        {
            path
            for path in pending_paths
            if path not in agent_paths and Path(path) != refactor_state
        }
    )


def _update_refactor_state(
    context: EditingRunContext,
    target: str,
    investigated_hash: str,
    has_findings: bool,
    changed_realization: list[str],
) -> None:
    """調査結果と変更された realization の再調査要求を state に保存する。"""
    state = load_refactor_state(context.run_worktree)
    entry = state.get(target)
    if entry is None:
        raise CmocError(
            "refactor target の state entry がありません。",
            ["refactor state を同期してから新しい run を開始してください。"],
            target,
        )
    entry["last_investigated_sha256"] = investigated_hash
    entry["last_investigated_at"] = timestamp()
    entry["last_investigation_result"] = "findings" if has_findings else "no_findings"
    entry["investigation_required"] = has_findings
    write_refactor_state(context.run_worktree, state)
    state = sync_refactor_state(context.run_worktree)
    for changed in changed_realization:
        if changed in state:
            state[changed]["investigation_required"] = True
    write_refactor_state(context.run_worktree, state)


def _changed_path_postcondition(
    context: EditingRunContext,
    output: object,
    artifact_changed_paths: frozenset[str],
) -> tuple[StructuredOutputValidationIssue, ...]:
    """refactor prompt が宣言する changed_paths 照合結果を返す。"""
    # {{work-root}}/oracle/src/oracle/acp_builder/realization/refactor/fork/file_review_and_fix.py
    assert isinstance(output, dict)
    findings = output["findings"]
    unexpected = set(unexpected_agent_paths(context, artifact_changed_paths))
    actual = set(artifact_changed_paths) - unexpected
    declared = {path for finding in findings for path in finding["changed_paths"]}
    if declared == actual:
        return ()
    return (
        StructuredOutputValidationIssue(
            condition=(
                "全所見の changed_paths の和集合が、agent call による realization "
                "file の実際の変更 path 集合と一致する"
            ),
            location="findings[*].changed_paths",
            expected=repr(sorted(actual)),
            observed=repr(sorted(declared)),
        ),
    )


def _write_refactor_report(
    context: EditingRunContext,
    state_after: str,
    reason: str,
    units: list[tuple[str, int]],
    unresolved_findings: dict[str, list[_UnresolvedFinding]],
    *,
    summary: list[_ChangeSummary] | None,
    error: BaseException | None = None,
    cleanup_errors: list[str] | None = None,
    progress: _RefactorProgress | None = None,
) -> Path:
    """refactor cycle の state、findings、変更概要を report として保存する。"""
    report_cleanup_errors = list(cleanup_errors or [])
    try:
        state = load_refactor_state(context.run_worktree)
    except BaseException as state_error:
        state = None
        report_cleanup_errors.append(f"state inspection failed: {state_error!r}")
    counts = _state_counts(state)
    try:
        uncommitted_paths = worktree_change_paths(
            context.run_worktree, include_rename_sources=True
        )
    except BaseException as inspection_error:
        uncommitted_paths = None
        report_cleanup_errors.append(
            f"uncommitted path inspection failed: {inspection_error!r}"
        )
    try:
        changes = tree_changes(context.run_worktree, context.run_fork_commit)
    except BaseException as change_error:
        if reason not in {"error", "user_interruption"}:
            raise
        # {{work-root}}/oracle/doc/app_spec/sub_command/realization_refactor.md
        # error/interruption report は補助的な git inspection の失敗でも保存し、
        # 確認できない変更 path は未確認として warning に残す。
        report_cleanup_errors.append(f"change inspection failed: {change_error!r}")
        changes = None
    progress = progress or _RefactorProgress()
    unresolved_targets = progress.deferred
    uninvestigated_targets = len(progress.targets - progress.processed)
    body = [
        "## Current fork",
        f"- completed cycles: {progress.completed_cycles}",
        f"- current cycle: {progress.cycle}",
        f"- stage: {progress.termination_phase or progress.phase}",
        f"- cycle targets: {len(progress.targets)}",
        f"- cycle confirmed investigations: {len(progress.processed)}",
        f"- cycle pending targets: {uninvestigated_targets}",
        f"- cycle deferred targets: {len(unresolved_targets)}",
        f"- processed targets: {len({target for target, _count in units})}",
        f"- committed processing units: {len(units)}",
        f"- uninvestigated targets: {uninvestigated_targets}",
        "## Processing units",
        *(
            [
                f"{_render_changed_path(target)}: {count} finding(s)"
                for target, count in units
            ]
            or ["- none"]
        ),
        *progress.records,
        "## Unresolved targets",
        f"- count: {len(unresolved_targets)}",
        "- paths:",
        *(
            [
                _render_changed_path(target, "  ")
                for target in sorted(unresolved_targets)
            ]
            or ["  - none"]
        ),
        "## Unresolved findings",
        *_render_unresolved_findings(unresolved_findings),
        "## Refactor state",
        *(
            f"- {label}: {yaml_scalar(counts[key])}"
            for label, key in (
                ("entries", "entries"),
                ("investigation_required", "required"),
                ("not_investigated", "not_investigated"),
                ("no_findings", "no_findings"),
                ("findings", "findings"),
            )
        ),
        "## Change summary",
        *(
            _render_summary(
                progress.summaries if progress.summaries else summary,
                [
                    path
                    for change in changes
                    for path in change.paths
                    if Path(path)
                    != refactor_state_path(context.run_worktree).relative_to(
                        context.run_worktree
                    )
                ],
            )
            if changes is not None
            else ["- unavailable (change inspection failed)"]
        ),
        "## Test timing",
        f"- baseline revision: {progress.baseline}",
        "- full test duration / reduction: unavailable (no comparable completed measurement)",
        "- scope / environment / command / conditions: not fixed; no timing comparison adopted",
        "- verification summaries above are agent reports; rolled-back work is not a measured committed result",
    ]
    if error is not None:
        body.extend(["## Error", repr(error)])
    body.extend(
        [
            "## Cleanup",
            f"- status: {progress.phase}",
            "- observed uncommitted paths (stop confirmation is reported separately):",
            *(
                [_render_changed_path(path, "  ") for path in uncommitted_paths]
                or ["  - none"]
                if uncommitted_paths is not None
                else ["  - unavailable"]
            ),
            "## Cleanup warnings",
            *(
                [f"- {item}" for item in report_cleanup_errors]
                if report_cleanup_errors
                else ["- none"]
            ),
            "## Next actions",
            *[
                f"- {action}"
                for action in _refactor_next_actions(report_cleanup_errors)
            ],
        ]
    )
    changed_paths = flattened_change_paths(changes) if changes is not None else None
    update_primary_report_fields(
        state_after=state_after,
        completion_reason=reason,
        changed_paths=changed_paths,
    )
    return write_fork_report(
        context,
        "realization/refactor/fork",
        state_after=state_after,
        completion_reason=reason,
        changed_paths=changed_paths,
        extra_fields={
            "refactor_state_path": refactor_state_path(context.run_worktree).resolve()
        },
        body_lines=body,
    )


def _state_counts(state: RefactorState | None) -> dict[str, int | None]:
    """refactor state の entry 数と調査結果別の件数を集計する。"""
    if state is None:
        return dict.fromkeys(
            ("entries", "required", "not_investigated", "no_findings", "findings")
        )
    return {
        "entries": len(state),
        "required": sum(entry["investigation_required"] for entry in state.values()),
        "not_investigated": sum(
            entry["last_investigation_result"] == "not_investigated"
            for entry in state.values()
        ),
        "no_findings": sum(
            entry["last_investigation_result"] == "no_findings"
            for entry in state.values()
        ),
        "findings": sum(
            entry["last_investigation_result"] == "findings" for entry in state.values()
        ),
    }


def _render_summary(
    summary: list[_ChangeSummary] | None,
    changed_paths: list[str],
) -> list[str]:
    """change summary を report 用 Markdown 行へ変換する。"""
    if not changed_paths:
        return ["- none"]
    if summary is not None:
        # 処理単位の履歴は、削除を含む確定済み成果物の net 差分と区別する。
        changed_path_set = set(changed_paths)
        lines = []
        for change in summary:
            category = change.get("category", "change")
            description = change.get("summary", "")
            paths = change.get("changed_paths", [])
            if not changed_path_set.intersection(paths):
                continue
            lines.append(f"- {category}: {description}")
            lines.extend(
                _render_changed_path(path, "  ")
                for path in paths
                if isinstance(path, str) and path in changed_path_set
            )
        return lines or ["- none"]
    return [
        _render_changed_path(path, label="committed path: ") for path in changed_paths
    ]


def _render_unresolved_findings(
    unresolved_findings: dict[str, list[_UnresolvedFinding]],
) -> list[str]:
    """unresolved 所見の理由と追跡可能な Codex call log を表示する。"""
    lines = []
    for target in sorted(unresolved_findings):
        for title, summary, call_log_path in unresolved_findings[target]:
            lines.extend(
                [
                    f"{_render_changed_path(target)}: {title}",
                    f"  - resolution.summary: {summary}",
                    _render_changed_path(str(call_log_path), "  ", "Codex call log: "),
                ]
            )
    return lines or ["- none"]


def _completion_result(
    reason: str,
    unresolved_findings: dict[str, list[_UnresolvedFinding]],
    report: Path,
    warnings: list[str],
    *,
    progress: _RefactorProgress | None = None,
) -> TerminalResult:
    """fork 固有の完了理由、report、次の lifecycle 操作を返す。"""
    return TerminalResult(
        primary_report=report,
        primary_report_role="realization refactor fork report",
        completion_reason=reason,
        details=(
            (
                "unresolved targets",
                len(progress.deferred) if progress else len(unresolved_findings),
            ),
        ),
        next_actions=_refactor_next_actions(warnings),
        warnings=tuple(warnings),
    )


def _refactor_next_actions(warnings: list[str]) -> tuple[str, ...]:
    """停止・rollback の確認状況に合わせて取り込みまたは復旧を案内する。"""
    recovery_required = any(
        "failed" in warning or "history recovery" in warning for warning in warnings
    )
    return (
        (
            "残存 process の停止と未確定差分の解消を確認してから `cmoc run join` を実行してください。",
            "`cmoc run abandon` も process の停止を確認してから資源を破棄します。",
        )
        if recovery_required
        else (
            "`cmoc run join` で確定済み成果物を取り込んでください。",
            "`cmoc run abandon` で run 全体を破棄できます。",
        )
    )
