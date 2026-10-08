"""外部解決を宣言した inconclusive 案件を、agent call なしで終了する。"""

from pathlib import Path
from typing import Any

from cmoc_runtime import (
    CmocError,
    TerminalResult,
    repo_root,
    run_cli_subcommand,
    work_root,
)
from commons.runtime_doctor import run_doctor_preprocess
from commons.runtime_feedback_close_state import (
    close_work_path,
    complete_close,
    load_close_work,
)
from commons.runtime_feedback_history import history_artifact, state_summary
from commons.runtime_feedback_render import publication_notice, render_current_cases
from commons.runtime_feedback_state import (
    ActiveState,
    current_generation_artifacts,
    feedback_writer_lock,
    generation_artifacts,
    load_active_state,
    load_report_cut,
    new_generation_id,
    new_report_cut_id,
    validate_feedback_state,
)
from commons.runtime_feedback_store import (
    canonical_json_bytes,
    feedback_root,
    mask_feedback_text,
    rfc3339_now,
    sha256_bytes,
    write_immutable_bytes,
    write_immutable_json,
)
from commons.runtime_ids import is_common_id
from commons.runtime_logging import current_execution_id, current_subcommand_logger
from commons.runtime_paths import sessions_dir
from commons.runtime_primary_report import update_primary_report_fields
from commons.runtime_primary_report_render import execution_record_markdown, yaml_scalar
from commons.runtime_state import SessionState, _read_state_data


def cmoc_feedback_close_impl(case_id: str | None, reason: str | None) -> None:
    """入力違反と事前条件違反も invocation report に残す CLI 本処理。"""
    # 理由の欠落を parser の終了へ任せず、最外側 runtime で報告する。
    argv = ["cmoc", "feedback", "close"]
    if case_id is not None:
        argv.append(case_id)
    if reason is not None:
        argv.extend(["--reason", reason])
    run_cli_subcommand(
        _close_body,
        case_id,
        reason,
        command_name="feedback close",
        command_argv=argv,
        doctor_preprocess=False,
    )


def cmoc_feedback_close_parse_error_impl(arguments: list[str], detail: str) -> None:
    """CLI parser が拒否した close の入力も共通 invocation report に残す。"""

    # 未受理の引数を対象案件への更新に使わない。
    def failed_input() -> None:
        update_primary_report_fields(
            rejected_arguments=arguments, publication_status="not_started"
        )
        raise CmocError(
            "feedback close の CLI 引数が不正です。",
            [
                "案件 ID 1 つと非空の --reason を指定してください。--report は使用できません。"
            ],
            detail,
        )

    run_cli_subcommand(
        failed_input, command_name="feedback close", command_argv=["cmoc", *arguments]
    )


def _close_body(case_id: str | None, reason: str | None) -> TerminalResult:
    repository = repo_root()
    update_primary_report_fields(
        case_id=case_id,
        human_reason=reason,
        publication_status="not_started",
        cleanup="not_started",
        next_operation="同じ案件 ID と保存済み理由で close を再実行してください。",
    )
    run_doctor_preprocess(work_root())
    if (
        not is_common_id(case_id, "fbc")
        or not isinstance(reason, str)
        or not reason.strip()
    ):
        raise CmocError(
            "feedback close の案件 ID と非空の --reason が必要です。",
            [
                '`cmoc feedback close <案件ID> --reason "外部での解決を確認した理由"` を指定してください。'
            ],
            "feedback close",
        )
    assert case_id is not None
    with feedback_writer_lock(repository):
        fixed_update: dict[str, Any] | None = None
        cleanup_completed = False
        try:
            state = validate_feedback_state(repository)
            _require_no_feedback_run(repository)
            work = load_close_work(repository)
            if work is not None:
                fixed_update = work
                published = (
                    state.current is not None
                    and state.current["generation_id"]
                    == work["generation"]["generation_id"]
                )
                if work["case_id"] != case_id or (
                    not published and work["reason"] != mask_feedback_text(reason)
                ):
                    raise CmocError(
                        "未完了の close と対象または理由が異なります。",
                        [
                            f"案件 {work['case_id']} と固定済み理由による close を再実行してください。"
                        ],
                        str(close_work_path(repository)),
                    )
                path = complete_close(repository, work)
                cleanup_completed = True
                return _completed(
                    repository,
                    path,
                    "already_closed" if published else "closed",
                    work,
                    reason,
                )
            # 終了済み案件は確定履歴から照合し、再発の案件に読み替えない。
            prior: tuple[dict[str, Any], dict[str, Any]] | None = None
            for history in state.history:
                for event in history["events"]:
                    if event["case_id"] == case_id and event["kind"] in {
                        "manual_close",
                        "resolved",
                    }:
                        prior = history, event
            if prior is not None:
                history, event = prior
                if event["kind"] != "manual_close":
                    raise CmocError(
                        "この案件は agent の判定により終了しており close の対象外です。",
                        [
                            f"履歴 {feedback_root(repository) / 'history' / (history['generation_id'] + '.json')} を確認してください。"
                        ],
                        "feedback close",
                    )
                path = _already_closed_report(repository, state, history, event, reason)
                return _completed(
                    repository,
                    path,
                    "already_closed",
                    {
                        "execution_id": history["source"]["execution_id"],
                        "case_id": case_id,
                    },
                    reason,
                )
            target = next(
                (
                    issue
                    for issue in state.issues.values()
                    if issue["case_id"] == case_id
                ),
                None,
            )
            if target is None:
                raise CmocError(
                    "指定案件 ID が見つかりません。",
                    ["最新の feedback report にある案件 ID を指定してください。"],
                    "feedback close",
                )
            if target["verification"]["status"] != "inconclusive":
                raise CmocError(
                    "human_required の案件は手動 close の対象外です。",
                    [
                        "案件の human action に従って対応し、`cmoc feedback report` で再確認してください。"
                    ],
                    "feedback close",
                )
            fixed = _prepare_close(repository, state, target, reason)
            fixed_update = fixed
            write_immutable_json(close_work_path(repository), fixed)
            path = complete_close(repository, fixed)
            cleanup_completed = True
            return _completed(repository, path, "closed", fixed, reason)
        except BaseException:
            # 確定後の失敗でも最新状態を戻さず、invocation の不足と区別する。
            try:
                state = load_active_state(repository)
                published = (
                    fixed_update is not None
                    and state.current is not None
                    and state.current["generation_id"]
                    == fixed_update["generation"]["generation_id"]
                )
                update_primary_report_fields(
                    publication_status="completed" if published else "not_completed",
                    current_generation=state.current,
                    remaining_cases=len(state.issues),
                    latest_state_summary=state_summary(state.issues),
                    cleanup="completed" if cleanup_completed else "not_completed",
                )
            except (CmocError, OSError, ValueError):
                pass
            raise


def _require_no_feedback_run(repo: Path) -> None:
    if (
        load_report_cut(repo) is not None
        or (feedback_root(repo) / "finalization.json").exists()
    ):
        raise CmocError(
            "未完了の feedback run/publication/cleanup があるため close を開始できません。",
            [
                "自動 join 済みなら `cmoc feedback report` で recovery し、未 join なら対象 session で `cmoc run join` または `cmoc run abandon` を実行してください。"
            ],
            "feedback close",
        )
    directory = sessions_dir(repo)
    if directory.exists():
        for path in directory.glob("*.json"):
            session = SessionState.from_dict(_read_state_data(path), path)
            if session.run.kind == "feedback_report" and session.run.state != "ready":
                raise CmocError(
                    "未終了の feedback run があります。",
                    [
                        f"session {path.stem} の run を join/abandon または feedback report recovery してください。"
                    ],
                    "feedback close",
                )


def _prepare_close(
    repo: Path, state: ActiveState, before: dict[str, Any], reason: str
) -> dict[str, Any]:
    # 初回の実行情報と全 byte 列を一度だけ固定し、再開時には作り直さない。
    assert state.current is not None and state.generation_manifest is not None
    execution_id = current_execution_id(repo)
    operation_id, generation_id = new_report_cut_id(), new_generation_id(repo)
    closed_at = rfc3339_now()
    source = {"kind": "close", "id": operation_id, "execution_id": execution_id}
    report_path = repo / f".cmoc/gu/report/feedback/close/{execution_id}.md"
    logger = current_subcommand_logger()
    assert logger is not None
    log_path = logger.path.relative_to(repo).as_posix()
    reason = mask_feedback_text(reason)
    history_record = {
        "schema_version": 1,
        "generation_id": generation_id,
        "source": source,
        "created_at": closed_at,
        "report": report_path.relative_to(repo).as_posix(),
        "log": log_path,
        "events": [
            {
                "kind": "manual_close",
                "case_id": before["case_id"],
                "issue_id": before["issue_id"],
                "before": before,
                "after": None,
                "agent_result": None,
                "human_reason": reason,
            }
        ],
        "observations": [],
    }
    history_path, history_content, history_reference = history_artifact(
        repo, history_record
    )
    issues = {
        identity: issue
        for identity, issue in state.issues.items()
        if identity != before["issue_id"]
    }
    generation, artifacts, _reference = generation_artifacts(
        repo,
        generation_id=generation_id,
        report_cut_id=operation_id,
        created_at=closed_at,
        session_commit=state.generation_manifest["session_commit"],
        issues=issues,
        machine_aggregates=state.machine_aggregates,
        source=source,
        base_current=state.current,
        input_boundary=state.generation_manifest["input_boundary"],
        history=[*state.generation_manifest["history"], history_reference],
    )
    report = _render_close_report(
        repo,
        state,
        issues,
        before,
        reason,
        closed_at,
        generation_id,
        history_path,
        execution_id,
        logger.path,
    )
    return {
        "schema_version": 1,
        "operation_id": operation_id,
        "execution_id": execution_id,
        "case_id": before["case_id"],
        "reason": reason,
        "closed_at": closed_at,
        "base_current": state.current,
        "before": before,
        "before_sha256": sha256_bytes(canonical_json_bytes(before)),
        "generation": generation,
        "artifacts": [
            _fixed_artifact(repo, path, content) for path, content in artifacts
        ],
        "history": _fixed_artifact(repo, history_path, history_content),
        "report": _fixed_artifact(repo, report_path, report.encode()),
        "old_generation": current_generation_artifacts(repo, state),
    }


def _fixed_artifact(repo: Path, path: Path, content: bytes) -> dict[str, Any]:
    return {
        "path": path.relative_to(repo).as_posix(),
        "sha256": sha256_bytes(content),
        "content": content.decode(),
    }


def _render_close_report(
    repo: Path,
    state: ActiveState,
    issues: dict[str, Any],
    before: dict[str, Any],
    reason: str,
    closed_at: str,
    generation_id: str,
    history_path: Path,
    execution_id: str,
    log_path: Path,
) -> str:
    fields = {
        "command": "cmoc feedback close",
        "execution_id": execution_id,
        "subcommand_log_path": str(log_path),
        "generated_at": closed_at,
        "repo_root": str(repo),
        "case_id": before["case_id"],
        "issue_id": before["issue_id"],
        "previous_agent_result": before["verification"]["status"],
        "human_reason": reason,
        "closed_at": closed_at,
        "base_generation_id": state.current["generation_id"] if state.current else None,
        "active_generation_id": generation_id,
        "result": "closed",
        "latest_state_summary": state_summary(issues),
        "remaining_cases": len(issues),
        "input_boundary": state.generation_manifest["input_boundary"]
        if state.generation_manifest
        else None,
    }
    return "\n".join(
        [
            "---",
            *[f"{key}: {yaml_scalar(value)}" for key, value in fields.items()],
            "---",
            "# cmoc feedback close",
            "",
            "人間の外部解決の宣言による更新です。agent の解決判定を生成せず、他の案件の再確認は行っていません。",
            "",
            f"History: `{history_path}`",
            "",
            publication_notice(str(log_path)),
            "",
            render_current_cases(issues),
            "",
            execution_record_markdown(current_subcommand_logger()),
        ]
    )


def _already_closed_report(
    repo: Path,
    state: ActiveState,
    history: dict[str, Any],
    event: dict[str, Any],
    reason: str,
) -> Path:
    execution_id = current_execution_id(repo)
    logger = current_subcommand_logger()
    assert logger is not None
    path = repo / f".cmoc/gu/report/feedback/close/{execution_id}.md"
    fields = {
        "command": "cmoc feedback close",
        "execution_id": execution_id,
        "generated_at": rfc3339_now(),
        "repo_root": str(repo),
        "subcommand_log_path": str(logger.path),
        "case_id": event["case_id"],
        "issue_id": event["issue_id"],
        "result": "already_closed",
        "input_reason": mask_feedback_text(reason),
        "original_human_reason": event["human_reason"],
        "original_closed_at": history["created_at"],
        "original_report": history["report"],
        "current_generation_id": state.current["generation_id"]
        if state.current
        else None,
        "latest_state_summary": state_summary(state.issues),
    }
    content = "\n".join(
        [
            "---",
            *[f"{key}: {yaml_scalar(value)}" for key, value in fields.items()],
            "---",
            "# cmoc feedback close: already_closed",
            "",
            "確定済みの終了記録を確認しました。今回の理由は元の理由・履歴を変更しません。state の publication は行っていません。",
            "",
            f"History: `{feedback_root(repo) / 'history' / (history['generation_id'] + '.json')}`",
            "",
            render_current_cases(state.issues),
            "",
            execution_record_markdown(logger),
        ]
    )
    write_immutable_bytes(path, content.encode())
    return path


def _completed(
    repo: Path, path: Path, result: str, record: dict[str, Any], input_reason: str
) -> TerminalResult:
    state = load_active_state(repo)
    logger = current_subcommand_logger()
    if logger is not None:
        logger.event(
            "feedback_close_completed",
            case_id=record["case_id"],
            report_execution_id=record["execution_id"],
            report_path=str(path),
            input_reason=mask_feedback_text(input_reason),
            result=result,
            latest_state_summary=state_summary(state.issues),
            remaining_cases=len(state.issues),
            current=state.current,
            cleanup="completed",
        )
    update_primary_report_fields(
        publication_status="completed",
        cleanup="completed",
        current_generation=state.current,
    )
    return TerminalResult(
        primary_report=path,
        primary_report_role="feedback close report",
        result=result,
        details=(
            ("latest_state_summary", state_summary(state.issues)),
            ("remaining_cases", len(state.issues)),
            ("cleanup", "completed"),
        ),
    )
