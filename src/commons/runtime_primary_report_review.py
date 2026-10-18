"""固定した primary report を確認し、本命の結果を変えず確認状態を加える。"""

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from oracle.acp_builder.primary_report_review import (
    build_primary_report_review_request,
)

from .runtime_codex_exec import run_codex_exec
from .runtime_codex_recovery import (
    check_recovery_interruption,
    isolated_recovery_interruption,
)
from .runtime_errors import CmocError, CodexProcessStopError, safe_text
from .runtime_logging import SubcommandLogger
from .runtime_paths import codex_log_dir
from .runtime_primary_report_render import execution_record_markdown
from .runtime_report_markdown import fenced_text, inline_code


@dataclass
class PrimaryReportReviewState:
    """同じ invocation の取消と、固定入力の保存先の採番を保持する。"""

    cancelled: bool = False
    input_count: int = 0


def add_primary_report_review(
    repository: Path,
    content: str,
    logger: SubcommandLogger,
    state: PrimaryReportReviewState,
) -> str:
    """共通の回復・補正を使って確認し、その記録を機械生成版へ追記する。"""
    # oracle/doc/app_spec/console_and_file_log.md の「重要事項確認用 call」。
    # 入力の固定後は確認自身の記録を戻さず、report を再帰的に確認しない。
    first_event = len(logger.event_records())
    input_path: Path | None = None
    accepted: dict[str, Any] | None = None
    status = "not_started"
    reason = "同じ invocation で確認が取り消されたため開始していません。"
    if not state.cancelled:
        try:
            with isolated_recovery_interruption() as cancellation:
                state.input_count += 1
                input_path = (
                    codex_log_dir(repository)
                    / logger.execution_id
                    / f"primary_report_review_{state.input_count}.md"
                ).resolve()
                input_path.parent.mkdir(parents=True, exist_ok=True)
                with input_path.open("x", encoding="utf-8", newline="") as stream:
                    stream.write(content)
                logger.event(
                    "primary_report_review",
                    status="input_frozen",
                    input_path=str(input_path),
                )
                # builder は oracle の定義を直接使用し、MCP の選択も引き継ぐ。
                try:
                    parameter = build_primary_report_review_request(
                        mechanical_report_path=input_path,
                        agent_call_cwd=repository,
                    )
                except ValueError as exc:
                    reason = f"確認の起動条件を満たせませんでした: {safe_text(exc)}"
                else:
                    # 0.163.0 の exec は初回・resume とも schema を turn/start へ渡す。
                    # https://github.com/openai/codex/blob/83086188ae0614bd882818ff1aa23f3194962012/codex-rs/exec/src/lib.rs#L893-L923
                    # https://github.com/openai/codex/blob/83086188ae0614bd882818ff1aa23f3194962012/codex-rs/exec/src/lib.rs#L956-L974
                    result = run_codex_exec(
                        parameter,
                        root=repository,
                        purpose="primary report review",
                        subcommand_logger=logger,
                    )
                    check_recovery_interruption()
                    # schema 検証を終えた正式な結果だけを掲載する。
                    accepted = result.output_json["result"]
                    status = "accepted"
                    reason = ""
        except KeyboardInterrupt:
            state.cancelled = True
            accepted = None
            status = "cancelled"
            reason = "重要事項の確認が取り消されました。"
        except CodexProcessStopError:
            # 停止確認の失敗を、確認未完了の例外で成功へ変換しない。
            state.cancelled = cancellation.is_set()
            raise
        except CmocError as exc:
            status = "failed"
            reason = f"{safe_text(exc.summary)}\n{safe_text(exc.detail)}"

    # 必要な記録の保存失敗は呼び出し元のエラー処理へ返す。
    logger.event(
        "primary_report_review",
        status=status,
        input_path=str(input_path) if input_path is not None else None,
        accepted_status=accepted["status"] if accepted is not None else None,
        reason=reason,
    )
    events = logger.event_records()[first_event:]
    review = _review_markdown(accepted, reason)
    record = _review_record(logger, input_path, status, accepted, events)
    intro, separator, rest = content.partition("\n\n## 元の指示\n\n")
    body, footer, information = rest.rpartition("\n\n## 実行情報\n\n")
    if not separator or not footer:
        raise ValueError(
            "primary report is missing its instruction or metadata section"
        )
    return (
        intro
        + "\n\n"
        + review
        + separator
        + body
        + "\n\n"
        + record
        + footer
        + information
    )


def _review_markdown(accepted: dict[str, Any] | None, reason: str) -> str:
    # 表示責務を prompt/schema に持ち込まず、未完了の固定文言も cmoc が生成する。
    status = accepted["status"] if accepted is not None else "incomplete"
    lines = ["## 重要事項の確認結果", ""]
    if status == "incomplete":
        lines.extend(
            [
                "エージェントによる重要事項の確認は完了していません。",
                "",
                "理由:",
                fenced_text(accepted["reason"] if accepted is not None else reason),
                "確認範囲:",
                fenced_text(
                    accepted["reviewed_scope"]
                    if accepted is not None
                    else "受理した応答がないため、確認できた範囲は不明です。"
                ),
            ]
        )
    elif status == "no_findings":
        lines.append(
            "固定した機械生成版の全文を確認した範囲では該当なし。"
            "実作業の正しさや report 外の問題の不存在を保証するものではありません。"
        )
    else:
        lines.append("固定した機械生成版の全文を確認し、重要事項を抽出しました。")
    for finding in accepted["findings"] if accepted is not None else ():
        lines.extend(["", fenced_text(finding["summary"])])
        for evidence in finding["evidence"]:
            lines.extend(
                [
                    "根拠位置: " + inline_code(evidence["location"]),
                    "原文引用:",
                    fenced_text(evidence["quote"]),
                ]
            )
    return "\n".join(lines)


def _review_record(
    logger: SubcommandLogger,
    input_path: Path | None,
    status: str,
    accepted: dict[str, Any] | None,
    events: tuple[dict[str, Any], ...],
) -> str:
    # 回復 probe・補正・不受理出力も含め、確認自身の取得済み本文を省略しない。
    lines = [
        "## 重要事項確認の実行記録",
        "",
        "この確認自身の実行記録と確認結果は、固定した確認入力の対象外です。",
        f"- 確認入力: {inline_code(str(input_path)) if input_path else '未作成'}",
        f"- 終了状況: {status}",
        f"- 出力の受理: {accepted['status'] if accepted is not None else '未受理'}",
    ]
    frozen = next(
        (event for event in events if event.get("status") == "input_frozen"), None
    )
    lines.append(f"- 確認入力の固定時刻: {frozen['timestamp'] if frozen else '未固定'}")
    calls = [event for event in events if event["event"] == "codex_call"]
    if not calls:
        lines.append("- Codex call: 未開始")
    for call in calls:
        lines.append(
            f"- call {inline_code(str(call['codex_call_id']))}: "
            f"{call['purpose']} / {call['status']} / {inline_code(str(call['call_log_path']))}"
        )
    record = execution_record_markdown(
        None,
        saved_events=events,
        execution_id=logger.execution_id,
        subcommand_log_path=logger.path,
    )
    # 元の実行記録と区別し、Markdown の階層もこの章内に収める。
    record = record.removeprefix("## 実行記録\n\n")
    return "\n".join(lines) + "\n\n" + record.rstrip("\n")
