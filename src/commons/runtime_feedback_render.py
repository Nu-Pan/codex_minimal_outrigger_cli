"""最新の案件一覧を report と close に共通の形式で描画する。"""

import html
import json
from typing import Any

from .runtime_feedback_store import mask_feedback_text


def render_current_cases(issues: dict[str, dict[str, Any]]) -> str:
    """案件 ID 順に最新の判定と人間が読める根拠を示す。"""
    # 終了案件と旧判定は、この一覧に混在させない。
    lines = ["## 現在の案件一覧", ""]
    for status in ("human_required", "inconclusive"):
        selected = sorted(
            (
                issue
                for issue in issues.values()
                if issue["verification"]["status"] == status
            ),
            key=lambda issue: issue["case_id"],
        )
        if not selected:
            continue
        lines.extend([f"### {status} の案件", ""])
        for issue in selected:
            verification = issue["verification"]
            session_count = str(issue["affected_session_count"])
            if issue["session_digest"]["saturated"]:
                session_count += "+"
            lines.extend(
                [
                    f"#### {issue['case_id']}",
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
    if not issues:
        lines.extend(["未終了の案件はありません。", ""])
    return "\n".join(lines)


def publication_notice(log_path: str) -> str:
    """保存時点の未完了処理と終了時の記録先を明示する。"""
    # Immutable report へ後続処理の成功を先取りしない。
    return (
        "保存時点では publication・cleanup・終了処理は未完了です。\n"
        f"それらの処理結果と最終 state は元の実行ログ `{_text(log_path)}` と terminal result に記録します。\n"
        "この一覧は対応する generation の確定範囲を示します。未取り込みの観測や確定後の変化は確認していません。\n"
    )


def _text(value: object) -> str:
    return html.escape(mask_feedback_text(str(value)), quote=False).replace("\n", " ")
