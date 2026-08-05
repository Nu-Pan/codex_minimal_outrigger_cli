"""oracle review の merge operation 適用契約を検証する。

テストの根拠:

- {{work-root}}/oracle/doc/app_spec/sub_command/oracle_review.md
- {{work-root}}/oracle/doc/dev_rule/test_rule.md
"""

import sub_commands.oracle.review as review_module
import sub_commands.oracle.review_loop as review_loop_module


def test_apply_finding_merge_operations_enforces_kind_contract() -> None:
    """delete/replace/merge の kind 契約を検証して finding を更新する。

    根拠: {{work-root}}/oracle/doc/app_spec/sub_command/oracle_review.md
    """
    findings = [
        {"finding_id": "finding-0001", "title": "delete"},
        {"finding_id": "finding-0002", "title": "replace"},
        {"finding_id": "finding-0003", "title": "merge a"},
        {"finding_id": "finding-0004", "title": "merge b"},
    ]
    merged, added_count = review_module.apply_finding_merge_operations(
        findings,
        [
            {"kind": "delete", "target_ids": ["finding-0001"], "finding": None},
            {
                "kind": "replace",
                "target_ids": ["finding-0002"],
                "finding": {
                    "oracle_path": "{{oracle-root}}/spec.md",
                    "severity": "fatal",
                    "title": "replacement",
                    "reason": "replacement reason",
                },
            },
            {
                "kind": "merge",
                "target_ids": ["finding-0003", "finding-0004"],
                "finding": {
                    "oracle_path": "{{oracle-root}}/spec.md",
                    "severity": "fatal",
                    "title": "merged",
                    "reason": "merged reason",
                },
            },
        ],
        5,
    )

    assert added_count == 2
    assert merged == [
        {
            "oracle_path": "{{oracle-root}}/spec.md",
            "severity": "fatal",
            "title": "replacement",
            "reason": "replacement reason",
            "finding_id": "finding-0005",
            "advocate_reasons": [],
            "challenger_reasons": [],
            "verdict": None,
            "judge_reason": None,
        },
        {
            "oracle_path": "{{oracle-root}}/spec.md",
            "severity": "fatal",
            "title": "merged",
            "reason": "merged reason",
            "finding_id": "finding-0006",
            "advocate_reasons": [],
            "challenger_reasons": [],
            "verdict": None,
            "judge_reason": None,
        },
    ]


def test_merge_target_id_postcondition_reports_unknown_input_id() -> None:
    """入力 finding_id 集合にない参照を field 位置つきで報告する。"""
    findings = [{"finding_id": "finding-0001"}]
    output = {
        "operations": [
            {
                "kind": "delete",
                "target_ids": ["finding-0001", "finding-9999"],
                "finding": None,
            }
        ]
    }

    issues = review_loop_module._merge_target_id_postcondition(
        findings, output, frozenset()
    )

    assert len(issues) == 1
    assert issues[0].location == "operations[0].target_ids[1]"
    assert issues[0].expected == "['finding-0001']"
    assert issues[0].observed == "'finding-9999'"
