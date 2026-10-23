"""最新の案件一覧を report と close に共通の形式で描画する。"""

import json
from typing import Any

from .runtime_feedback_history import state_summary
from .runtime_feedback_store import mask_feedback_text
from .runtime_report_markdown import ReportSummary, inline_code


def feedback_report_summary(
    issues: dict[str, dict[str, Any]],
    outcome: str,
    *,
    scope: tuple[str, ...] = (),
    publication_pending: bool = False,
    notices: tuple[str, ...] = (),
) -> ReportSummary:
    """案件の残件と invocation の成否を分け、必要な確認と操作を示す。"""
    # 未確認事項を解決済みへ読み替えず、generation に含まれる判定だけを数える。
    human = sum(
        issue["verification"]["status"] == "human_required" for issue in issues.values()
    )
    inconclusive = sum(
        issue["verification"]["status"] == "inconclusive" for issue in issues.values()
    )
    attention = list(notices)
    actions: list[str] = []
    if publication_pending:
        attention.append(
            "保存時点では publication・cleanup・終了処理は未完了です。invocation の終端結果は未確定です。"
        )
        actions.append(
            "保存後の publication・cleanup・最終 state と terminal result を、実行情報に示す元の実行ログで確認してください。"
        )
    if human:
        attention.append(f"人間対応が必要な案件（human_required）: {human} 件。")
        actions.append(
            "案件一覧の Human action に従って対応し、`cmoc feedback report` で再確認してください。"
        )
    if inconclusive:
        attention.append(
            f"判定不能の案件（inconclusive）: {inconclusive} 件。最新状態の要約は incomplete です。問題の解決は確認できていません。"
        )
        actions.append(
            "判定不能の理由と根拠を確認してください。外部解決を人間が確認した案件は `cmoc feedback close <案件ID> --reason <理由>` で終了できます。"
        )
    attention.append(
        "確認範囲はこの generation の入力境界までです。未取り込みの観測や確定後の変化は確認していません。"
    )
    return ReportSummary(
        outcome,
        (
            *scope,
            f"最新状態の要約: {state_summary(issues)} / human_required: {human} 件 / inconclusive: {inconclusive} 件",
        ),
        tuple(attention),
        tuple(actions),
    )


def render_current_cases(issues: dict[str, dict[str, Any]]) -> str:
    """案件 ID 順に最新の判定と人間が読める根拠を示す。"""
    # 終了案件と旧判定は、この一覧に混在させない。
    lines = ["## 現在の案件一覧", ""]
    selected = sorted(
        (
            issue
            for issue in issues.values()
            if issue["verification"]["status"] in {"human_required", "inconclusive"}
        ),
        key=lambda issue: issue["case_id"],
    )
    for issue in selected:
        verification = issue["verification"]
        status = verification["status"]
        session_count = str(issue["affected_session_count"])
        if issue["session_digest"]["saturated"]:
            session_count += "+"
        lines.extend(
            [
                f"### {issue['case_id']}",
                "",
                f"- Issue ID: {issue['issue_id']}",
                f"- Latest result: {status}",
                f"- Verified at: {verification['verified_at']}",
                f"- Category: {_text(issue['category'])}",
                f"- Summary: {_text(issue['summary'])}",
                f"- Impact: {_text(issue['impact'])}",
                f"- Reason: {_text(verification['reason'])}",
                f"- Occurrences: {issue['occurrence_count']}",
                f"- Affected sessions: {session_count}",
                f"- First observed: {issue['first_observed_at']}",
                f"- Last observed: {issue['last_observed_at']}",
            ]
        )
        if status == "human_required":
            lines.append(f"- Human action: {_text(verification['human_action'])}")
        else:
            lines.append(
                "- 外部解決を人間が確認した場合: "
                + f'`cmoc feedback close {issue["case_id"]} --reason "外部で修正し、人間が解決を確認した"`'
            )
        lines.append("- Current evidence:")
        for evidence in verification["current_evidence"]:
            subject = (
                evidence.get("path")
                or evidence.get("probe_id")
                or evidence.get("observation_id", "unknown")
            )
            lines.append(
                f"  - {_text(subject)} / {_text(evidence.get('location', ''))}: {_text(evidence.get('finding', ''))}"
            )
        if not verification["current_evidence"]:
            lines.append(
                "  - 確認できた current evidence はありません。判定不能の理由は Reason に記載しています。"
            )
        lines.append("- Representative evidence:")
        lines.extend(
            f"  - {_text(json.dumps(evidence, ensure_ascii=False, sort_keys=True))}"
            for evidence in issue["representative_evidence"]
        )
        if not issue["representative_evidence"]:
            lines.append("  - none")
        lines.append("")
    if not selected:
        lines.extend(["未終了の案件はありません。", ""])
    return "\n".join(lines)


def publication_notice(log_path: str) -> str:
    """保存時点の未完了処理と終了時の記録先を明示する。"""
    # Immutable report へ後続処理の成功を先取りしない。
    return (
        "保存時点では publication・cleanup・終了処理は未完了です。\n"
        f"それらの処理結果と最終 state は元の実行ログ {_text(log_path)} と terminal result に記録します。\n"
        "この一覧は対応する generation の確定範囲を示します。未取り込みの観測や確定後の変化は確認していません。\n"
    )


def _text(value: object) -> str:
    # マスク済みの本文を一行へ収め、HTML 文字参照へ変換せず表示する。
    text = mask_feedback_text(str(value)).replace("\r\n", " ")
    return inline_code(text.replace("\r", " ").replace("\n", " "))
