"""案件一覧の順序と判定ごとの情報を Git・publication の準備なしで検証する。"""

import pytest
from _report_support import report_section

from commons.runtime_feedback_render import (
    feedback_report_summary,
    render_current_cases,
)
from commons.runtime_report_markdown import render_report_document


def _case(number, status):
    return {
        "case_id": f"fbc_{number:06d}_2026-10-08_00-00",
        "issue_id": f"issue-{10 - number}",
        "category": "tooling",
        "summary": "<summary>\n次の行",
        "impact": "<impact>",
        "occurrence_count": 5,
        "affected_session_count": 4,
        "session_digest": {"saturated": number == 0},
        "first_observed_at": "2026-10-07T00:00:00Z",
        "last_observed_at": "2026-10-08T00:00:00Z",
        "representative_evidence": [],
        "verification": {
            "status": status,
            "verified_at": "2026-10-08T01:00:00Z",
            "reason": "<reason>",
            "human_action": "設定を確認する" if status == "human_required" else None,
            "current_evidence": [
                {"path": "README.md", "location": "line 2", "finding": "<finding>"}
            ]
            if status == "human_required"
            else [],
        },
    }


def test_current_cases_follow_case_id_order_and_keep_verdict_details():
    first = _case(0, "human_required")
    second = _case(1, "inconclusive")
    third = _case(2, "human_required")
    secret = "ghp_123456789012345678901234"
    first["representative_evidence"] = [{"path": "README.md", "text": secret}]
    first["verification"]["current_evidence"].extend(
        [
            {"probe_id": "probe-1", "finding": "probe result"},
            {"observation_id": "observation-1", "finding": "observed result"},
        ]
    )
    # 入力順・issue ID・判定のどれも、案件 ID の順序を上書きしない。
    rendered = render_current_cases(
        {case["issue_id"]: case for case in (third, second, first)}
    )
    headings = [
        line.split(maxsplit=1)[1]
        for line in rendered.splitlines()
        if line.startswith("#") and " fbc_" in line
    ]
    assert headings == [case["case_id"] for case in (first, second, third)]
    for case in (first, second, third):
        assert f"- Issue ID: {case['issue_id']}" in rendered
    assert rendered.count("- Latest result: human_required") == 2
    assert rendered.count("- Latest result: inconclusive") == 1
    assert rendered.count("- Human action: 設定を確認する") == 2
    assert f"cmoc feedback close {second['case_id']} --reason" in rendered
    assert "確認できた current evidence はありません" in rendered
    assert "- Category: tooling" in rendered
    assert "- Summary: &lt;summary&gt; 次の行" in rendered
    assert "- Impact: &lt;impact&gt;" in rendered
    assert "- Reason: &lt;reason&gt;" in rendered
    assert "README.md / line 2: &lt;finding&gt;" in rendered
    assert "probe-1 / : probe result" in rendered
    assert "observation-1 / : observed result" in rendered
    assert "- Verified at: 2026-10-08T01:00:00Z" in rendered
    assert "- Occurrences: 5" in rendered
    assert "- Affected sessions: 4+" in rendered
    assert "- Affected sessions: 4\n" in rendered
    assert "- First observed: 2026-10-07T00:00:00Z" in rendered
    assert "- Last observed: 2026-10-08T00:00:00Z" in rendered
    assert secret not in rendered
    assert "[REDACTED:credential]" in rendered
    assert "- Representative evidence:\n  - none" in rendered


def test_empty_current_cases_explains_absence():
    rendered = render_current_cases({})
    assert "未終了の案件はありません。" in rendered
    assert "- Latest result:" not in rendered


@pytest.mark.parametrize(
    ("statuses", "expected"),
    [
        ([], "ok"),
        (["human_required"], "attention"),
        (["inconclusive"], "incomplete"),
        (["human_required", "inconclusive"], "incomplete"),
    ],
)
def test_publication_summary_separates_issue_state_and_unfinished_invocation(
    statuses, expected
):
    issues = {str(index): _case(index, status) for index, status in enumerate(statuses)}
    rendered = render_report_document(
        "cmoc feedback report",
        {
            "command": "cmoc feedback report",
            "report_cut_id": "fixed-cut",
            "final_high_watermark": 7,
            "execution_id": "original-execution",
        },
        feedback_report_summary(
            issues,
            "report 保存時点の記録です。",
            publication_pending=True,
        ),
        render_current_cases(issues),
    )
    result = report_section(rendered, "実行結果")
    attention = report_section(rendered, "要注意事項")
    actions = report_section(rendered, "次の操作")
    assert f"最新状態の要約: {expected}" in result
    assert "保存時点" in result
    assert "未完了" in attention and "未確定" in attention
    assert "元の実行ログ" in actions
    assert "未取り込みの観測や確定後の変化は確認していません" in attention
    if "human_required" in statuses:
        assert "人間対応が必要" in attention
        assert "Human action" in actions
    if "inconclusive" in statuses:
        assert "問題の解決は確認できていません" in attention
        assert "cmoc feedback close" in actions
    assert "fixed-cut" in report_section(rendered, "元の指示")
