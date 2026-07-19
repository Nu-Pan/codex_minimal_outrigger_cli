"""oracle review の merge operation 適用契約を検証する。

テストの根拠:

- {{work-root}}/oracle/doc/app_spec/sub_command/oracle_review.md
- {{work-root}}/oracle/doc/dev_rule/test_rule.md
"""

import pytest

import sub_commands.oracle.review as review_module


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


@pytest.mark.parametrize(
    "operation",
    [
        {"kind": "delete", "target_ids": ["finding-0001"], "finding": {}},
        {
            "kind": "replace",
            "target_ids": ["finding-0001", "finding-0002"],
            "finding": {},
        },
        {"kind": "replace", "target_ids": ["finding-0001"], "finding": None},
        {"kind": "merge", "target_ids": ["finding-0001"], "finding": {}},
        {
            "kind": "merge",
            "target_ids": ["finding-0001", "finding-9999"],
            "finding": {},
        },
        {
            "kind": "delete",
            "target_ids": ["finding-0001", "finding-0001"],
            "finding": None,
        },
    ],
)
def test_apply_finding_merge_operations_rejects_invalid_operations(
    operation: dict,
) -> None:
    """対象や payload が不正な merge operation を拒否する。

    根拠: {{work-root}}/oracle/doc/app_spec/sub_command/oracle_review.md
    """
    with pytest.raises(ValueError):
        review_module.apply_finding_merge_operations(
            [{"finding_id": "finding-0001"}, {"finding_id": "finding-0002"}],
            [operation],
            3,
        )


@pytest.mark.parametrize(
    "operations",
    [
        [
            {"kind": "replace", "target_ids": ["finding-0001"], "finding": {}},
            {"kind": "replace", "target_ids": ["finding-0001"], "finding": {}},
        ],
        [
            {
                "kind": "merge",
                "target_ids": ["finding-0001", "finding-0002"],
                "finding": {},
            },
            {"kind": "delete", "target_ids": ["finding-0002"], "finding": None},
        ],
        [
            {"kind": "delete", "target_ids": ["finding-0001"], "finding": None},
            {
                "kind": "merge",
                "target_ids": ["finding-0001", "finding-0002"],
                "finding": {},
            },
        ],
    ],
)
def test_apply_finding_merge_operations_rejects_reused_targets(
    operations: list[dict],
) -> None:
    """複数 operation に同じ finding_id を再利用する入力を拒否する。

    根拠: {{work-root}}/oracle/doc/app_spec/sub_command/oracle_review.md
    """
    with pytest.raises(ValueError):
        review_module.apply_finding_merge_operations(
            [{"finding_id": "finding-0001"}, {"finding_id": "finding-0002"}],
            operations,
            3,
        )
