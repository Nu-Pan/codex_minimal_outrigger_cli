"""確定済み runtime 情報から fallback primary report を描画する。

根拠:
- {{work-root}}/oracle/doc/app_spec/console_and_file_log.md
- {{work-root}}/oracle/doc/app_spec/sub_command/feedback_report.md
"""

import json
import re
from pathlib import Path
from typing import Any

from .runtime_feedback_store import mask_feedback_text
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
    if spec.template == "feedback_invocation":
        body = _feedback_invocation_body(
            classification,
            result,
            logger,
            dict(fields),
        )
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
    for call in calls:
        value = call.get("output_path")
        if not isinstance(value, str) or value in seen:
            continue
        seen.add(value)
        path = Path(value)
        if not path.is_file():
            continue
        content = path.read_text(encoding="utf-8", errors="replace")
        fence = "`" * max(
            3, 1 + max((len(run) for run in re.findall(r"`+", content)), default=0)
        )
        lines.extend(
            [f"出力: {path}", "", fence + "text", content.rstrip("\n"), fence, ""]
        )
    if not seen:
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
        fence = "`" * max(
            3, 1 + max((len(run) for run in re.findall(r"`+", content)), default=0)
        )
        lines.extend(
            [str(observation["observation_id"]), "", fence + "json", content, fence, ""]
        )
    if not observations:
        lines.extend(["新規に受理された observation はありません。", ""])
    return "\n".join(lines)


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
