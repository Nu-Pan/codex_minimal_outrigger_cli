"""確定済み runtime 情報から fallback primary report を描画する。

根拠:
- {{work-root}}/oracle/doc/app_spec/console_and_file_log.md
- {{work-root}}/oracle/doc/app_spec/sub_command/feedback_report.md
- {{work-root}}/oracle/doc/app_spec/sub_command/oracle_review.md
"""

import json
from pathlib import Path

from .runtime_logging import SubcommandLogger
from .runtime_primary_report_specs import PrimaryReportSpec, TerminalClassification
from .runtime_results import TerminalResult


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
    if spec.template == "oracle_review":
        body = _oracle_review_body(classification, result, logger)
    elif spec.template == "feedback_invocation":
        body = _feedback_invocation_body(
            classification,
            result,
            logger,
            dict(fields),
        )
    else:
        body = _summary_body(spec.title, classification, result, logger)
    return "\n".join([*front_matter, *body, ""])


def oracle_edit_statuses(logger: SubcommandLogger) -> dict[str, object]:
    """Codex event から本命・仕様削減 agent call の実行状況を確定する。"""
    return {
        "main_agent_call_status": _agent_call_status(logger, "oracle edit main"),
        "reduction_agent_call_status": _agent_call_status(
            logger, "oracle edit reduction"
        ),
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
        return json.dumps(value, ensure_ascii=False, sort_keys=True)
    return json.dumps(str(value), ensure_ascii=False)


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
        "## 終端結果",
        *_terminal_lines(classification, result),
        "## warning とエラー",
        *_warning_error_lines(classification, result, logger),
        "## 次の操作",
        *([f"- {action}" for action in result.next_actions] or ["- なし"]),
        "## 関連ログ",
        *_log_lines(logger),
    ]


def _oracle_review_body(
    classification: TerminalClassification,
    result: TerminalResult,
    logger: SubcommandLogger,
) -> list[str]:
    """早期終了でも oracle review の必須セクションを保つ。"""
    reason = (
        _detail_value(result, "理由") or "通常のレビュー処理を完了できませんでした。"
    )
    verdict = (
        "ユーザー中断要求により、確定済みの部分結果だけで完了しました。"
        if classification == "user_interruption"
        else f"レビュー開始前または処理途中でエラーになりました。理由: {reason}"
    )
    return [
        "# cmoc oracle review report",
        "## Verdict",
        verdict,
        "## Evaluated oracle file",
        "| No. | Oracle file | Findings |",
        "|---:|---|---:|",
        "| - | 未確定 | - |",
        "## Fatal findings",
        "- 確定済み所見なし",
        "## Minor findings",
        "- 確定済み所見なし",
        "## 実行段階",
        *_step_lines(logger, classification),
        "## warning とエラー",
        *_warning_error_lines(classification, result, logger),
        "## 関連ログ",
        *_log_lines(logger),
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
        "- verification checkpoint: "
        f"`{_field_status(fields.get('verification_checkpoint_count'))}`",
        f"- 確定済み部分結果: `{_field_status(fields.get('partial_result_count'))}`",
        "## 維持した state と未実行処理",
        f"- processing status: `{_field_status(fields.get('processing_status'))}`",
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
    """確定した warning と error detail を重複なく描画する。"""
    lines = [f"- warning: {_inline_text(value)}" for value in logger.warning_messages]
    if classification == "error":
        lines.extend(
            f"- {name}: `{_inline_text(value)}`" for name, value in result.details
        )
    return lines or ["- なし"]


def _log_lines(logger: SubcommandLogger) -> list[str]:
    """診断用 subcommand log と実行済み Codex call log を列挙する。"""
    lines = [f"- 診断用サブコマンドログ: `{logger.path.resolve(strict=False)}`"]
    for event in logger.codex_call_records():
        call_path = event.get("call_log_path")
        if not isinstance(call_path, str):
            continue
        purpose = _inline_text(event.get("purpose", "Codex call"))
        status = _inline_text(event.get("status", "unknown"))
        lines.append(
            f"- Codex call ({purpose}, {status}): `{Path(call_path).resolve(strict=False)}`"
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
    step_fragment = (
        "本命 agent call" if purpose.endswith("main") else "仕様削減 agent call"
    )
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


def _detail_value(result: TerminalResult, name: str) -> str | None:
    """terminal detail の指定値を一行表示へ変換する。"""
    for item_name, value in result.details:
        if item_name == name:
            return _inline_text(value)
    return None


def _inline_text(value: object) -> str:
    """任意の確定値を Markdown の一行へ安全に収める。"""
    if isinstance(value, Path):
        text = str(value.resolve(strict=False))
    else:
        text = str(value)
    return text.replace("`", "'").replace("\r", " ").replace("\n", " | ")


def _field_status(value: object) -> str:
    """未確定値を完了済みの 0 件と混同せず一行表示する。"""
    return "not_fixed" if value is None else _inline_text(value)
