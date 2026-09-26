"""確定済み runtime 情報から fallback primary report を描画する。

根拠:
- {{work-root}}/oracle/doc/app_spec/console_and_file_log.md
- {{work-root}}/oracle/doc/app_spec/sub_command/feedback_report.md
"""

import json
import re
from decimal import Decimal
from pathlib import Path
from typing import Any, NamedTuple

from .runtime_errors import safe_text
from .runtime_feedback_store import mask_feedback_text
from .runtime_logging import SubcommandLogger
from .runtime_primary_report_specs import PrimaryReportSpec, TerminalClassification
from .runtime_results import TerminalResult


class _JsonObjectPairs(NamedTuple):
    """同名キーも含め、JSON object の出現順を表示用に保持する。"""

    entries: list[tuple[str, Any]]


def render_primary_report(
    spec: PrimaryReportSpec,
    fields: list[tuple[str, object]],
    classification: TerminalClassification,
    result: TerminalResult,
    logger: SubcommandLogger,
) -> str:
    """個別 template を使い、確定済み情報だけから report を構築する。"""
    front_matter = [
        "---",
        *[f"{name}: {yaml_scalar(value)}" for name, value in fields],
        "---",
    ]
    field_values = dict(fields)
    if spec.template == "feedback_invocation":
        body = _feedback_invocation_body(
            classification,
            result,
            logger,
            field_values,
        )
    elif spec.template == "doctor":
        body = _doctor_body(spec.title, classification, result, logger)
    elif spec.template == "indexing":
        body = _indexing_body(classification, result, logger, field_values)
    elif spec.template == "session_fork":
        body = _session_fork_body(classification, result, logger, field_values)
    elif spec.template == "refactor_fork":
        body = _refactor_fork_body(classification, result, logger)
    elif spec.template == "session_join":
        body = _session_join_body(classification, result, logger, field_values)
    elif spec.template == "session_abandon":
        body = _session_abandon_body(classification, result, logger, field_values)
    elif spec.template == "oracle_edit":
        body = _oracle_edit_body(classification, result, logger, field_values)
    elif spec.template == "apply_fork":
        body = _apply_fork_body(classification, result, logger, field_values)
    elif spec.template == "run_join":
        body = _run_join_body(classification, result, logger, field_values)
    elif spec.template == "run_abandon":
        body = _run_abandon_body(classification, result, logger, field_values)
    else:
        body = _summary_body(spec.title, classification, result, logger)
    return "\n".join([*front_matter, *body, "", execution_record_markdown(logger)])


def execution_record_markdown(
    logger: SubcommandLogger | None,
    *,
    saved_events: tuple[dict[str, Any], ...] = (),
) -> str:
    """各 Codex call の最終出力と新規 observation を実行記録として掲載する。"""
    lines = ["## 実行記録", "", "### Codex 最終出力", ""]
    events = (*saved_events, *(logger.event_records() if logger else ()))
    calls = (event for event in events if event.get("event") == "codex_call")
    seen: set[str] = set()
    rendered_output = False
    for call in calls:
        value = call.get("output_path")
        if not isinstance(value, str) or value in seen:
            continue
        seen.add(value)
        path = Path(value)
        if not path.is_file():
            continue
        is_structured = isinstance(call.get("schema_path"), str)
        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            content = path.read_text(
                encoding="utf-8",
                errors="backslashreplace" if is_structured else "replace",
            )
            invalid_utf8 = True
        else:
            invalid_utf8 = False
        display = content
        notes: list[str] = []
        if is_structured:
            # 受理判定には触れず、call ごとの保存済み原文を report 用にだけ整える。
            if call.get("status") in {
                "output_correction_requested",
                "structured_output_validation_failed",
            }:
                notes.append("検証不合格（正式な結果ではありません）。")
            elif call.get("status") != "succeeded":
                notes.append("正式な結果ではありません。")
            if invalid_utf8:
                notes.append("JSON として解析できません。取得できた原文を示します。")
            else:
                try:
                    parsed = json.loads(
                        content,
                        object_pairs_hook=_JsonObjectPairs,
                        parse_float=Decimal,
                        parse_constant=_reject_json_constant,
                    )
                except (ValueError, RecursionError):
                    notes.append(
                        "JSON として解析できません。取得できた原文を示します。"
                    )
                else:
                    display = _render_structured_value(parsed)
        fence = _code_fence(display)
        rendered_output = True
        lines.extend(
            [
                f"出力: {_path_code_span(path)}",
                *notes,
                "",
                fence + "text",
                display,
                fence,
                "",
            ]
        )
    if not rendered_output:
        lines.extend(["取得済みの最終出力はありません。", ""])
    lines.extend(["### 新規 feedback observation", ""])
    observations = [
        event
        for event in events
        if event.get("event") == "feedback_observation_accepted"
    ]
    for observation in observations:
        content = mask_feedback_text(
            json.dumps(observation["payload"], ensure_ascii=False, indent=2)
        )
        fence = _code_fence(content)
        lines.extend(
            [str(observation["observation_id"]), "", fence + "json", content, fence, ""]
        )
    if not observations:
        lines.extend(["新規に受理された observation はありません。", ""])
    return "\n".join(lines)


def _reject_json_constant(value: str) -> None:
    """JSON 仕様外の非有限数を表示上も有効な JSON と誤認しない。"""
    # Python の json.loads は標準外の NaN/Infinity を既定で受け取る。
    raise ValueError(f"non-standard JSON constant: {value}")


def _render_structured_value(value: Any) -> str:
    """JSON の階層と型を保ち、文字列内の改行だけを実際の改行にする。"""
    # parse 済みの値だけをたどり、深い JSON でも再帰上限で report を失わない。
    fragments: list[str] = []
    pending: list[tuple[str, Any, int]] = [("value", value, 0)]
    while pending:
        kind, current, depth = pending.pop()
        if kind == "text":
            fragments.append(current)
        elif isinstance(current, (_JsonObjectPairs, list)):
            entries: list[tuple[Any, Any]]
            if isinstance(current, _JsonObjectPairs):
                is_object = True
                entries = current.entries
                opening, closing = "{", "}"
            else:
                is_object = False
                entries = list(enumerate(current))
                opening, closing = "[", "]"
            if not entries:
                fragments.append("{}" if is_object else "[]")
                continue
            fragments.append(opening + "\n")
            pending.append(("text", "\n" + "  " * depth + closing, 0))
            for index in range(len(entries) - 1, -1, -1):
                key, item = entries[index]
                pending.append(("text", ",\n" if index < len(entries) - 1 else "", 0))
                pending.append(("value", item, depth + 1))
                prefix = "  " * (depth + 1)
                if is_object:
                    prefix += _display_json_string(str(key)) + ": "
                pending.append(("text", prefix, 0))
        elif isinstance(current, str):
            fragments.append(_display_json_string(current))
        elif isinstance(current, Decimal):
            fragments.append(str(current))
        else:
            fragments.append(json.dumps(current, ensure_ascii=False))
    return "".join(fragments)


def _display_json_string(value: str) -> str:
    """引用符とバックスラッシュを区切りと区別して一度だけ表示する。"""
    # 改行で先に分割し、元のリテラル \\n を再解釈しない。
    segments = [
        json.dumps(segment, ensure_ascii=False)[1:-1]
        .encode("utf-8", errors="backslashreplace")
        .decode("utf-8")
        for segment in value.split("\n")
    ]
    return '"' + "\n".join(segments) + '"'


def _code_fence(value: str) -> str:
    """本文中の backtick run より長い Markdown fence を選ぶ。"""
    # 文字列の内容を escape せず掲載できる区切りを選ぶ。
    return "`" * max(
        3, 1 + max((len(run) for run in re.findall(r"`+", value)), default=0)
    )


def _path_code_span(path: Path) -> str:
    """元の出力 path の backtick も保持して参照として示す。"""
    # code span の delimiter を path に含まれる backtick より長くする。
    value = safe_text(path.resolve(strict=False))
    delimiter = "`" * max(
        1, 1 + max((len(run) for run in re.findall(r"`+", value)), default=0)
    )
    padding = " " if value.startswith("`") or value.endswith("`") else ""
    return f"{delimiter}{padding}{value}{padding}{delimiter}"


def oracle_edit_statuses(logger: SubcommandLogger) -> dict[str, object]:
    """Codex event から 1 回目・2 回目の編集 agent call の実行状況を確定する。"""
    return {
        "first_agent_call_status": _agent_call_status(logger, "oracle edit first"),
        "second_agent_call_status": _agent_call_status(logger, "oracle edit second"),
    }


def feedback_statuses(logger: SubcommandLogger) -> dict[str, object]:
    """publication point の log event だけから feedback の実行状況を返す。"""
    events = logger.event_records()
    published = any(
        event.get("event") == "feedback_report_published" for event in events
    )
    incomplete = any(
        event.get("event") == "feedback_report_incomplete" for event in events
    )
    return {
        "normal_publication_status": "completed" if published else "not_completed",
        "incomplete_diagnostic_status": "completed" if incomplete else "not_completed",
        "current_pointer_update_status": "completed" if published else "not_completed",
    }


def yaml_scalar(value: object) -> str:
    """report の YAML scalar として安全に表現する。"""
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return str(value)
    if isinstance(value, (list, dict)):
        return json.dumps(_safe_json_value(value), ensure_ascii=False, sort_keys=True)
    return json.dumps(safe_text(value), ensure_ascii=False)


def execution_step_lines(
    logger: SubcommandLogger,
    classification: TerminalClassification,
) -> list[str]:
    """別の primary report writer へ実行済み step の要約を渡す。"""
    return _step_lines(logger, classification)


def related_log_lines(logger: SubcommandLogger) -> list[str]:
    """別の primary report writer へ診断用・Codex call log 一覧を渡す。"""
    return _log_lines(logger)


def _summary_body(
    title: str,
    classification: TerminalClassification,
    result: TerminalResult,
    logger: SubcommandLogger,
) -> list[str]:
    """通常の機械的 invocation summary を要点先行で描画する。"""
    return [
        f"# {title}",
        _outcome_sentence(classification),
        "## 実行段階",
        *_step_lines(logger, classification),
        *_standard_tail(classification, result, logger),
    ]


def _standard_tail(
    classification: TerminalClassification,
    result: TerminalResult,
    logger: SubcommandLogger,
) -> list[str]:
    """全 fallback report に共通する終端、警告、次操作、ログを描画する。"""
    return [
        "## 終端結果",
        *_terminal_lines(classification, result),
        "## warning とエラー",
        *_warning_error_lines(classification, result, logger),
        "## 次の操作",
        *([f"- {action}" for action in result.next_actions] or ["- なし"]),
        "## 関連ログ",
        *_log_lines(logger),
    ]


def _doctor_body(
    title: str,
    classification: TerminalClassification,
    result: TerminalResult,
    logger: SubcommandLogger,
) -> list[str]:
    """doctor preprocess の実行有無と結果を fallback report に残す。"""
    return [
        f"# {title}",
        _outcome_sentence(classification),
        "## doctor preprocess",
        f"- 検査と修復: `{_stage_status(logger, classification)}`",
        *_standard_tail(classification, result, logger),
    ]


def _indexing_body(
    classification: TerminalClassification,
    result: TerminalResult,
    logger: SubcommandLogger,
    fields: dict[str, object],
) -> list[str]:
    """文書検索索引の同期実績と失敗を fallback report に残す。"""
    sync = fields.get("sync_result")
    sync_fields = sync if isinstance(sync, dict) else {}
    elapsed = sync_fields.get("elapsed_seconds", fields.get("elapsed_seconds"))
    return [
        "# cmoc indexing report",
        _outcome_sentence(classification),
        "## 文書検索索引の同期",
        f"- 実行状態: `{_operation_status(fields.get('indexing_status'), classification)}`",
        f"- 実効閲覧範囲: `{_field_status(fields.get('scope_identity'))}`",
        f"- 索引 identity: `{_field_status(fields.get('index_identity'))}`",
        f"- 許可文書数: `{_field_status(sync_fields.get('document_count'))}`",
        f"- chunk 数: `{_field_status(sync_fields.get('chunk_count'))}`",
        f"- 追加: `{_field_status(sync_fields.get('added'))}`",
        f"- 変更: `{_field_status(sync_fields.get('changed'))}`",
        f"- 削除: `{_field_status(sync_fields.get('deleted'))}`",
        f"- 空白化: `{_field_status(sync_fields.get('blanked'))}`",
        f"- 埋め込み再利用: `{_field_status(sync_fields.get('reused_embeddings'))}`",
        f"- 所要秒数: `{_field_status(elapsed)}`",
        f"- 失敗 code: `{_field_status(fields.get('failure_code'))}`",
        f"- 失敗理由: `{_field_status(fields.get('failure_reason'))}`",
        f"- 次の操作: `{_indexing_next_action(fields)}`",
        *_standard_tail(classification, result, logger),
    ]


def _indexing_next_action(fields: dict[str, object]) -> str:
    """確定した同期状態から、必要な次の操作だけを示す。"""
    if fields.get("indexing_status") in {"updated", "unchanged"}:
        return "なし"
    if fields.get("failure_code") == "NOT_READY":
        return "文書検索の tuning と固定資材を準備する"
    return "診断用ログと失敗理由を確認する"


def _session_fork_body(
    classification: TerminalClassification,
    result: TerminalResult,
    logger: SubcommandLogger,
    fields: dict[str, object],
) -> list[str]:
    """session fork の branch、state、rollback の確定値を描画する。"""
    session_branch = fields.get("session_branch")
    state_after = fields.get("session_state_after")
    branch_status = (
        "completed"
        if state_after == "active"
        else "未確認"
        if session_branch is not None
        else "未実行"
    )
    state_status = "completed" if state_after is not None else "未実行"
    return [
        "# cmoc session fork report",
        _outcome_sentence(classification),
        "## branch の作成と checkout",
        f"- home branch: `{_field_status(fields.get('home_branch'))}`",
        f"- session branch: `{_field_status(session_branch)}`",
        f"- fork commit: `{_field_status(fields.get('session_fork_commit'))}`",
        f"- branch 作成と checkout: `{branch_status}`",
        "## session state file と状態遷移",
        f"- session state file 作成と保存: `{state_status}`",
        "- session state file path: `not_fixed`",
        "- session state: "
        f"`{_field_status(fields.get('session_state_before'))}` -> "
        f"`{_field_status(state_after)}`",
        "## rollback と残存資源",
        f"- rollback: `{_operation_status(fields.get('rollback_status'), classification)}`",
        "- 残存 branch・state file: `未確認`",
        *_standard_tail(classification, result, logger),
    ]


def _feedback_invocation_body(
    classification: TerminalClassification,
    result: TerminalResult,
    logger: SubcommandLogger,
    fields: dict[str, object],
) -> list[str]:
    """feedback publication と混同しない invocation summary を描画する。"""
    statuses = feedback_statuses(logger)
    return [
        "# cmoc feedback report invocation summary",
        _outcome_sentence(classification),
        "この report は feedback publication または active state ではありません。",
        "## 実行段階",
        *_step_lines(logger, classification),
        "## 確定済みの部分結果",
        f"- 正常 publication: `{statuses['normal_publication_status']}`",
        f"- incomplete 診断: `{statuses['incomplete_diagnostic_status']}`",
        f"- current pointer 更新: `{statuses['current_pointer_update_status']}`",
        "## checkpoint と部分結果",
        f"- report cut: `{_field_status(fields.get('report_cut_id'))}`",
        "- normalization checkpoint: "
        f"`{_field_status(fields.get('normalization_checkpoint_count'))}`",
        "- remediation checkpoint: "
        f"`{_field_status(fields.get('remediation_checkpoint_count'))}`",
        f"- 確定済み部分結果: `{_field_status(fields.get('partial_result_count'))}`",
        "## 維持した state と未実行処理",
        f"- processing status: `{_field_status(fields.get('processing_status'))}`",
        f"- cleanup: `{_feedback_cleanup_status(logger, fields)}`",
        "- publication 完了 event がない処理は、完了済みとして扱っていません。",
        "- 再開可能な report cut と checkpoint の詳細は診断用ログを参照してください。",
        "## warning とエラー",
        *_warning_error_lines(classification, result, logger),
        "## 次の操作",
        *(
            [f"- {action}" for action in result.next_actions]
            or ["- 状態を確認して再実行してください。"]
        ),
        "## 関連ログ",
        *_log_lines(logger),
    ]


def _refactor_fork_body(
    classification: TerminalClassification,
    result: TerminalResult,
    logger: SubcommandLogger,
) -> list[str]:
    """refactor 固有 report の未確定項目を fallback でも明示する。"""
    not_fixed = "not_fixed"
    return [
        "# cmoc realization refactor fork report",
        _outcome_sentence(classification),
        "## Current fork",
        f"- processed targets: {not_fixed}",
        f"- uninvestigated targets: {not_fixed}",
        "## Processing units",
        f"- {not_fixed}",
        "## Unresolved targets",
        f"- count: {not_fixed}",
        "- paths:",
        f"  - {not_fixed}",
        "## Unresolved findings",
        f"- {not_fixed}",
        "## Refactor state",
        f"- entries: {not_fixed}",
        f"- investigation_required: {not_fixed}",
        f"- not_investigated: {not_fixed}",
        f"- no_findings: {not_fixed}",
        f"- findings: {not_fixed}",
        "## Change summary",
        f"- {not_fixed}",
        "## 終端結果",
        *_terminal_lines(classification, result),
        "## warning とエラー",
        *_warning_error_lines(classification, result, logger),
        "## 次の操作",
        *([f"- {action}" for action in result.next_actions] or ["- なし"]),
        "## 関連ログ",
        *_log_lines(logger),
    ]


def _session_join_body(
    classification: TerminalClassification,
    result: TerminalResult,
    logger: SubcommandLogger,
    fields: dict[str, object],
) -> list[str]:
    """session join 固有の実行要約を、確定済み情報だけから描画する。"""
    merge_status = _operation_status(fields.get("merge_status"), classification)
    conflict_paths = fields.get("conflict_paths")
    if isinstance(conflict_paths, list):
        conflict_lines = [f"- `{_inline_text(path)}`" for path in conflict_paths] or [
            "- なし"
        ]
    else:
        conflict_lines = [
            "- 未実行"
            if fields.get("merge_status") is None
            else "- conflict は発生していません。"
        ]
    conflict_call_status = fields.get("conflict_resolution_status")
    if conflict_call_status is None:
        conflict_call = (
            "未実行（conflict なし）"
            if fields.get("merge_status") == "completed"
            else "未実行"
        )
    else:
        conflict_call = _operation_status(conflict_call_status, classification)
    conflict_result = _operation_status(
        fields.get("conflict_resolution_result"), classification
    )
    agent_report = fields.get("conflict_agent_report")
    if isinstance(agent_report, str) and agent_report.strip():
        fence = "`" * max(
            3, 1 + max((len(run) for run in re.findall(r"`+", agent_report)), default=0)
        )
        agent_lines = [fence + "text", agent_report.rstrip("\n"), fence]
    else:
        agent_lines = ["- 未実行または出力なし"]
    incidental = fields.get("conflict_incidental_paths")
    incidental_lines = (
        [f"- `{_inline_text(path)}`" for path in incidental]
        if isinstance(incidental, list) and incidental
        else ["- なし"]
    )
    state_before = _field_status(fields.get("session_state_before"))
    state_after = _field_status(fields.get("session_state_after"))
    return [
        "# cmoc session join report",
        _outcome_sentence(classification),
        "## 事前検証",
        *_step_lines(logger, classification),
        "## branch 切替と merge",
        f"- session branch: `{_field_status(fields.get('session_branch'))}`",
        f"- home branch: `{_field_status(fields.get('home_branch'))}`",
        "- branch 切替: "
        f"`{_operation_status(fields.get('branch_switch_status'), classification)}`",
        "- merge 前の session branch HEAD: "
        f"`{_field_status(fields.get('session_branch_head_before_merge'))}`",
        "- merge 前の home branch HEAD: "
        f"`{_field_status(fields.get('home_branch_head_before_merge'))}`",
        f"- merge 結果: `{merge_status}`",
        f"- 作成した merge commit: `{_field_status(fields.get('merge_commit'))}`",
        "## conflict 解消",
        "- conflict path:",
        *conflict_lines,
        f"- conflict 解消用 agent call: `{conflict_call}`",
        f"- 確定した解消結果: `{conflict_result}`",
        "### agent の判断と検証",
        *agent_lines,
        "### 付随編集",
        *incidental_lines,
        "## state 遷移",
        f"- session state: `{state_before}` -> `{state_after}`",
        "- state 更新: "
        f"`{_operation_status(fields.get('state_update_status'), classification)}`",
        "## session branch の cleanup",
        "- cleanup: "
        f"`{_operation_status(fields.get('session_branch_cleanup_status'), classification)}`",
        "## 終端結果",
        *_terminal_lines(classification, result),
        "## warning とエラー",
        *_warning_error_lines(classification, result, logger),
        "## 次の操作",
        *([f"- {action}" for action in result.next_actions] or ["- なし"]),
        "## 関連ログ",
        *_log_lines(logger),
    ]


def _session_abandon_body(
    classification: TerminalClassification,
    result: TerminalResult,
    logger: SubcommandLogger,
    fields: dict[str, object],
) -> list[str]:
    """session abandon の対象、state、cleanup、rollback を描画する。"""
    state_after = fields.get("session_state_after")
    cleanup = _detail_or_field(fields, result, "cleanup")
    cleanup_status = _operation_status(cleanup, classification)
    if cleanup is None and state_after == "abandoned":
        cleanup_status = "completed"
    return [
        "# cmoc session abandon report",
        _outcome_sentence(classification),
        "## 破棄対象",
        f"- session branch: `{_field_status(fields.get('session_branch'))}`",
        f"- home branch: `{_field_status(fields.get('home_branch'))}`",
        "- branch 上の commit: "
        f"`{_field_status(fields.get('abandoned_branch_start_commit'))}`",
        "## branch 切替と state 遷移",
        f"- home branch への切替: `{_branch_switch_status(fields, classification)}`",
        "- session state: "
        f"`{_field_status(fields.get('session_state_before'))}` -> "
        f"`{_field_status(state_after)}`",
        f"- state 更新: `{_state_update_status(state_after)}`",
        "## branch 削除と cleanup",
        f"- branch 削除と cleanup: `{cleanup_status}`",
        f"- cleanup detail: `{_field_status(cleanup)}`",
        "## rollback と残存資源",
        f"- rollback: `{_operation_status(fields.get('rollback_status'), classification)}`",
        "- 残存 branch・state file: `未確認`",
        *_standard_tail(classification, result, logger),
    ]


def _oracle_edit_body(
    classification: TerminalClassification,
    result: TerminalResult,
    logger: SubcommandLogger,
    fields: dict[str, object],
) -> list[str]:
    """oracle edit の二つの agent call 状態を描画する。"""
    return [
        "# cmoc oracle edit report",
        _outcome_sentence(classification),
        "## agent call",
        f"- first agent call: `{_field_status(fields.get('first_agent_call_status'))}`",
        "- second agent call: "
        f"`{_field_status(fields.get('second_agent_call_status'))}`",
        "## 編集結果",
        "- oracle file の編集結果は agent call log と差分を参照してください。",
        *_standard_tail(classification, result, logger),
    ]


def _apply_fork_body(
    classification: TerminalClassification,
    result: TerminalResult,
    logger: SubcommandLogger,
    fields: dict[str, object],
) -> list[str]:
    """realization apply fork の run、差分、Codex、feedback を描画する。"""
    return [
        "# cmoc realization apply fork report",
        _outcome_sentence(classification),
        "## run",
        f"- run kind: `{_field_status(fields.get('run_kind'))}`",
        f"- session branch: `{_field_status(fields.get('session_branch'))}`",
        f"- session fork commit: `{_field_status(fields.get('session_fork_commit'))}`",
        f"- run branch: `{_field_status(fields.get('run_branch'))}`",
        f"- run fork commit: `{_field_status(fields.get('run_fork_commit'))}`",
        f"- run worktree: `{_field_status(fields.get('run_worktree'))}`",
        "- state: "
        f"`{_field_status(fields.get('state_before'))}` -> "
        f"`{_field_status(fields.get('state_after'))}`",
        f"- completion reason: `{_field_status(fields.get('completion_reason'))}`",
        "## 追従差分と Codex result",
        f"- diff base commit: `{_field_status(fields.get('diff_base_commit'))}`",
        f"- Codex returncode: `{_field_status(fields.get('codex_returncode'))}`",
        f"- changed paths: `{_field_status(fields.get('changed_paths'))}`",
        "## feedback observation",
        "- accepted observation count: "
        f"`{_field_status(fields.get('feedback_observation_count'))}`",
        f"- accepted observations: `{_field_status(fields.get('feedback_observations'))}`",
        *_standard_tail(classification, result, logger),
    ]


def _run_join_body(
    classification: TerminalClassification,
    result: TerminalResult,
    logger: SubcommandLogger,
    fields: dict[str, object],
) -> list[str]:
    """run join の差分検査、取り込み、hook、state、cleanup を描画する。"""
    run_join_commit = _detail_or_field(fields, result, "run_join_commit")
    return [
        "# cmoc run join report",
        _outcome_sentence(classification),
        "## run join",
        f"- run kind: `{_field_status(fields.get('run_kind'))}`",
        f"- session branch: `{_field_status(fields.get('session_branch'))}`",
        f"- run branch: `{_field_status(fields.get('run_branch'))}`",
        f"- run worktree: `{_field_status(fields.get('run_worktree'))}`",
        "- state: "
        f"`{_field_status(fields.get('state_before'))}` -> "
        f"`{_field_status(fields.get('state_after'))}`",
        "## 差分検査と merge / no-op join",
        f"- run fork commit: `{_field_status(fields.get('run_fork_commit'))}`",
        f"- run join commit: `{_field_status(run_join_commit)}`",
        "- 差分検査: `未実行`",
        "- 想定外差分: `未確認`",
        "- merge または no-op join: "
        f"`{_operation_status(run_join_commit, classification)}`",
        "## post-join と cleanup",
        f"- post-join hook: `{_field_status(fields.get('post_join_hook'))}`",
        f"- refactor state 同期: `{_field_status(fields.get('refactor_state_sync_commit'))}`",
        f"- cleanup: `{_field_status(fields.get('cleanup'))}`",
        "- 残存資源: `未確認`",
        *_standard_tail(classification, result, logger),
    ]


def _run_abandon_body(
    classification: TerminalClassification,
    result: TerminalResult,
    logger: SubcommandLogger,
    fields: dict[str, object],
) -> list[str]:
    """run abandon の process、対象、state、cleanup を描画する。"""
    return [
        "# cmoc run abandon report",
        _outcome_sentence(classification),
        "## process と cleanup",
        f"- process stop: `{_field_status(fields.get('process_stop'))}`",
        f"- worktree: `{_field_status(fields.get('run_worktree'))}`",
        f"- branch: `{_field_status(fields.get('run_branch'))}`",
        f"- worktree removed: `{_field_status(fields.get('worktree_removed'))}`",
        f"- branch removed: `{_field_status(fields.get('branch_removed'))}`",
        f"- cleanup: `{_field_status(fields.get('cleanup'))}`",
        "- 残存資源: `未確認`",
        "## state 遷移",
        "- state: "
        f"`{_field_status(fields.get('state_before'))}` -> "
        f"`{_field_status(fields.get('state_after'))}`",
        *_standard_tail(classification, result, logger),
    ]


def _detail_or_field(
    fields: dict[str, object], result: TerminalResult, name: str
) -> object:
    """front matter context を優先し、terminal result の detail を補う。"""
    if name in fields:
        return fields[name]
    return next(
        (value for detail_name, value in result.details if detail_name == name), None
    )


def _operation_status(value: object, classification: TerminalClassification) -> str:
    """operation の未実行・失敗・完了を report 用の短い値へ変換する。"""
    if value is None:
        return "未実行"
    if value == "started":
        return "失敗または未完了" if classification == "error" else "実行中"
    if value == "not_confirmed":
        return "未確認"
    return _inline_text(value)


def _branch_switch_status(
    fields: dict[str, object], classification: TerminalClassification
) -> str:
    """branch 名から switch の実行を推測せず、確定可能な状態だけを示す。"""
    if fields.get("session_state_after") == "abandoned":
        return "completed"
    if fields.get("home_branch") is None:
        return "未実行"
    return _operation_status("not_confirmed", classification)


def _state_update_status(value: object) -> str:
    """state の値を、更新操作の status として安全に表示する。"""
    return "completed" if value is not None else "未実行"


def _stage_status(
    logger: SubcommandLogger, classification: TerminalClassification
) -> str:
    """step 記録から doctor preprocess の実行状態を要約する。"""
    doctor_steps = [
        step for step in logger.step_timings if "doctor preprocess" in step.description
    ]
    if not doctor_steps:
        return "未実行"
    step = doctor_steps[-1]
    if classification == "error" and logger.step_timings[-1] is step:
        return "error"
    if classification == "user_interruption" and logger.step_timings[-1] is step:
        return "user_interruption"
    return "completed" if step.elapsed_sec is not None else "started"


def _step_lines(
    logger: SubcommandLogger, classification: TerminalClassification
) -> list[str]:
    """開始済み step だけを、最終 step の終端状態とともに列挙する。"""
    if not logger.step_timings:
        return ["- サブコマンド固有の処理段階は未開始"]
    lines: list[str] = []
    last_index = len(logger.step_timings) - 1
    for index, step in enumerate(logger.step_timings):
        if index == last_index and classification == "error":
            status = "error"
        elif index == last_index and classification == "user_interruption":
            status = "user_interruption"
        elif step.elapsed_sec is None:
            status = "started"
        else:
            status = "completed"
        lines.append(f"- `{step.index}` {step.description}: `{status}`")
    return lines


def _terminal_lines(
    classification: TerminalClassification, result: TerminalResult
) -> list[str]:
    """共通分類とサブコマンド固有結果を簡潔に描画する。"""
    lines = [f"- terminal classification: `{classification}`"]
    if result.result is not None:
        lines.append(f"- result: `{_inline_text(result.result)}`")
    if result.completion_reason is not None:
        lines.append(f"- completion_reason: `{_inline_text(result.completion_reason)}`")
    lines.extend(f"- {name}: `{_inline_text(value)}`" for name, value in result.details)
    return lines


def _warning_error_lines(
    classification: TerminalClassification,
    result: TerminalResult,
    logger: SubcommandLogger,
) -> list[str]:
    """確定した warning と error/interruption detail を描画する。"""
    lines = [f"- warning: {_inline_text(value)}" for value in logger.warning_messages]
    if classification in {"error", "user_interruption"}:
        lines.extend(
            f"- {name}: `{_inline_text(value)}`" for name, value in result.details
        )
    return lines or ["- なし"]


def _feedback_cleanup_status(
    logger: SubcommandLogger, fields: dict[str, object]
) -> str:
    """publication 後の cleanup が未完了かを invocation summary に示す。

    根拠: {{work-root}}/oracle/doc/app_spec/sub_command/feedback_report.md
    """
    events = logger.event_records()
    published = any(
        event.get("event") == "feedback_report_published" for event in events
    )
    if not published:
        return "not_started"
    if (
        any(
            event.get("event")
            in {"feedback_report_cleanup_failed", "feedback_report_interrupted"}
            for event in events
        )
        or fields.get("processing_status") == "publication_ready"
    ):
        return "not_completed"
    return "completed"


def _log_lines(logger: SubcommandLogger) -> list[str]:
    """診断用 subcommand log と実行済み Codex call log を列挙する。"""
    lines = [f"- 診断用サブコマンドログ: `{_inline_text(logger.path)}`"]
    for event in logger.codex_call_records():
        call_path = event.get("call_log_path")
        if not isinstance(call_path, str):
            continue
        purpose = _inline_text(event.get("purpose", "Codex call"))
        status = _inline_text(event.get("status", "unknown"))
        lines.append(
            f"- Codex call ({purpose}, {status}): `{_inline_text(Path(call_path))}`"
        )
    return lines


def _agent_call_status(logger: SubcommandLogger, purpose: str) -> str:
    """指定 purpose の event と開始 step から四状態を返す。"""
    matching = [
        event
        for event in logger.codex_call_records()
        if event.get("purpose") == purpose
    ]
    if any(event.get("status") == "succeeded" for event in matching):
        return "succeeded"
    failure_statuses = {
        "failed",
        "output_correction_failed",
        "structured_output_validation_failed",
    }
    if any(event.get("status") in failure_statuses for event in matching):
        return "failed"
    pass_number = 1 if purpose.endswith("first") else 2
    step_fragment = f"{pass_number} 回目の編集 agent call"
    if matching or any(
        step_fragment in step.description for step in logger.step_timings
    ):
        return "started"
    return "not_started"


def _outcome_sentence(classification: TerminalClassification) -> str:
    """report 冒頭へ共通分類の要点を一文で置く。"""
    return {
        "natural_completion": "この invocation は自然完了しました。",
        "user_interruption": "この invocation はユーザー中断要求により完了しました。",
        "error": "この invocation はエラー終了しました。",
    }[classification]


def _inline_text(value: object) -> str:
    """任意の確定値を Markdown の一行へ安全に収める。"""
    if isinstance(value, Path):
        text = safe_text(value.resolve(strict=False))
    else:
        text = safe_text(value)
    return text.replace("`", "'").replace("\r", " ").replace("\n", " | ")


def _safe_json_value(value: object) -> object:
    """report の JSON/YAML 値から Unicode surrogate を除く。"""
    if isinstance(value, str):
        return safe_text(value)
    if isinstance(value, list):
        return [_safe_json_value(item) for item in value]
    if isinstance(value, dict):
        return {safe_text(key): _safe_json_value(item) for key, item in value.items()}
    return value


def _field_status(value: object) -> str:
    """未確定値を完了済みの 0 件と混同せず一行表示する。"""
    return "not_fixed" if value is None else _inline_text(value)
