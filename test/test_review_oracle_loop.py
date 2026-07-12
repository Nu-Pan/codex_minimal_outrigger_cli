"""review oracle の finding loop と merge operation を検証する。"""

from pathlib import Path

import pytest

from _git_support import make_repo
from cmoc_runtime import CmocError
from config.cmoc_config import CmocConfig, CmocConfigReviewOracle
import sub_commands.review.oracle as review_module
import sub_commands.review_loop as review_loop_module

def test_review_oracle_enumerate_receives_only_related_findings(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = make_repo(tmp_path)
    (root / "oracle" / "a.md").write_text("# a\n")
    (root / "oracle" / "b.md").write_text("# b\n")
    monkeypatch.chdir(root)
    prompts_by_target: dict[str, list[str]] = {}
    config = CmocConfig(
        review_oracle=CmocConfigReviewOracle(
            num_enumerate_findings_loop=2,
            num_merge_findings_loop=0,
            num_validate_findings_loop=1,
        ),
    )

    class FakeCodexResult:
        def __init__(self, output_json: dict[str, object]) -> None:
            self.output_json = output_json

    def fake_run_codex_exec(parameter: object, **kwargs: object) -> object:
        schema_name = parameter.structured_output_schema_path.name
        if schema_name == "enumerate_finding.json":
            target = Path(
                kwargs["purpose"].removeprefix(
                    "review oracle enumerate findings for "
                )
            ).name
            prompts_by_target.setdefault(target, []).append(parameter.prompt)
            if target == "a.md" and len(prompts_by_target[target]) == 1:
                return FakeCodexResult(
                    {
                        "findings": [
                            {
                                "oracle_path": "<oracle-root>/a.md",
                                "severity": "fatal",
                                "title": "a finding",
                                "reason": "a reason",
                            }
                        ]
                    }
                )
            return FakeCodexResult({"findings": []})
        if schema_name in {
            "validate_finding_challenger.json",
            "validate_finding_advocate.json",
        }:
            return FakeCodexResult({"reasons": []})
        if schema_name == "judge_finding.json":
            return FakeCodexResult({"verdict": "reject", "reason": "no finding"})
        raise AssertionError(schema_name)

    review_module.run_review_oracle_loop(
        root,
        root,
        [root / "oracle" / "a.md", root / "oracle" / "b.md"],
        config,
        fake_run_codex_exec,
    )

    assert "a finding" not in prompts_by_target["b.md"][0]
    assert "a finding" in prompts_by_target["a.md"][1]

def test_review_oracle_advocate_receives_same_round_challenger_reasons(
    tmp_path: Path,
) -> None:
    root = make_repo(tmp_path)
    advocate_prompts: list[str] = []
    config = CmocConfig(
        review_oracle=CmocConfigReviewOracle(
            num_enumerate_findings_loop=1,
            num_merge_findings_loop=0,
            num_validate_findings_loop=1,
        ),
    )

    class FakeCodexResult:
        def __init__(self, output_json: dict[str, object]) -> None:
            self.output_json = output_json

    def fake_run_codex_exec(parameter: object, **kwargs: object) -> object:
        schema_name = parameter.structured_output_schema_path.name
        if schema_name == "enumerate_finding.json":
            return FakeCodexResult(
                {
                    "findings": [
                        {
                            "oracle_path": "<oracle-root>/spec.md",
                            "severity": "fatal",
                            "title": "finding",
                            "reason": "reason",
                        }
                    ]
                }
            )
        if schema_name == "validate_finding_challenger.json":
            return FakeCodexResult({"reasons": ["same-round challenger reason"]})
        if schema_name == "validate_finding_advocate.json":
            advocate_prompts.append(parameter.prompt)
            return FakeCodexResult({"reasons": []})
        if schema_name == "judge_finding.json":
            return FakeCodexResult({"verdict": "reject", "reason": "rejected"})
        raise AssertionError(schema_name)

    review_module.run_review_oracle_loop(
        root,
        root,
        [root / "oracle" / "spec.md"],
        config,
        fake_run_codex_exec,
    )

    assert advocate_prompts
    assert "same-round challenger reason" in advocate_prompts[0]

def test_review_oracle_advocate_keeps_existing_challenger_reasons(
    tmp_path: Path,
) -> None:
    root = make_repo(tmp_path)
    advocate_prompts: list[str] = []
    config = CmocConfig(
        review_oracle=CmocConfigReviewOracle(
            num_enumerate_findings_loop=1,
            num_merge_findings_loop=0,
            num_validate_findings_loop=1,
        ),
    )
    findings = [
        {
            "finding_id": "finding-0001",
            "oracle_path": "<oracle-root>/spec.md",
            "severity": "fatal",
            "title": "finding",
            "reason": "reason",
            "advocate_reasons": [],
            "challenger_reasons": ["old challenger reason"],
            "verdict": None,
            "judge_reason": None,
        }
    ]

    class FakeCodexResult:
        def __init__(self, output_json: dict[str, object]) -> None:
            self.output_json = output_json

    def fake_run_codex_exec(parameter: object, **kwargs: object) -> object:
        schema_name = parameter.structured_output_schema_path.name
        if schema_name == "validate_finding_challenger.json":
            return FakeCodexResult({"reasons": ["same-round challenger reason"]})
        if schema_name == "validate_finding_advocate.json":
            advocate_prompts.append(parameter.prompt)
            return FakeCodexResult({"reasons": []})
        if schema_name == "judge_finding.json":
            return FakeCodexResult({"verdict": "reject", "reason": "rejected"})
        raise AssertionError(schema_name)

    review_loop_module._validate_and_judge_findings(
        root,
        root,
        findings,
        config,
        fake_run_codex_exec,
    )

    assert advocate_prompts
    assert "old challenger reason" in advocate_prompts[0]
    assert "same-round challenger reason" in advocate_prompts[0]

def test_review_oracle_retries_semantic_merge_finding_failure(
    tmp_path: Path,
) -> None:
    root = make_repo(tmp_path)
    merge_calls = 0
    config = CmocConfig(
        review_oracle=CmocConfigReviewOracle(
            num_enumerate_findings_loop=1,
            num_merge_findings_loop=1,
            num_validate_findings_loop=1,
        ),
    )

    class FakeCodexResult:
        def __init__(self, output_json: dict[str, object]) -> None:
            self.output_json = output_json

    def fake_run_codex_exec(parameter: object, **kwargs: object) -> object:
        nonlocal merge_calls
        schema_name = parameter.structured_output_schema_path.name
        if schema_name == "enumerate_finding.json":
            return FakeCodexResult(
                {
                    "findings": [
                        {"oracle_path": "<oracle-root>/spec.md", "severity": "fatal", "title": "a", "reason": "reason a"},
                        {"oracle_path": "<oracle-root>/spec.md", "severity": "fatal", "title": "b", "reason": "reason b"},
                    ]
                }
            )
        if schema_name == "merge_finding.json":
            merge_calls += 1
            if merge_calls == 1:
                return FakeCodexResult(
                    {
                        "operations": [
                            {
                                "kind": "delete",
                                "target_ids": ["finding-9999"],
                                "finding": None,
                            }
                        ]
                    }
                )
            return FakeCodexResult(
                {
                    "operations": [
                        {
                            "kind": "merge",
                            "target_ids": ["finding-0001", "finding-0002"],
                            "finding": {"oracle_path": "<oracle-root>/spec.md", "severity": "fatal", "title": "merged", "reason": "merged reason"},
                        }
                    ]
                }
            )
        if schema_name in {
            "validate_finding_challenger.json",
            "validate_finding_advocate.json",
        }:
            return FakeCodexResult({"reasons": []})
        if schema_name == "judge_finding.json":
            return FakeCodexResult({"verdict": "reject", "reason": "rejected"})
        raise AssertionError(schema_name)

    findings = review_module.run_review_oracle_loop(
        root,
        root,
        [root / "oracle" / "spec.md"],
        config,
        fake_run_codex_exec,
    )

    assert merge_calls == 2
    assert [finding["finding_id"] for finding in findings] == ["finding-0003"]
    assert findings[0]["title"] == "merged"

def test_review_oracle_fails_after_merge_finding_semantic_retries(
    tmp_path: Path,
) -> None:
    root = make_repo(tmp_path)
    merge_calls = 0
    config = CmocConfig(
        review_oracle=CmocConfigReviewOracle(
            num_enumerate_findings_loop=1,
            num_merge_findings_loop=1,
            num_validate_findings_loop=1,
        ),
    )

    class FakeCodexResult:
        def __init__(self, output_json: dict[str, object]) -> None:
            self.output_json = output_json

    def fake_run_codex_exec(parameter: object, **kwargs: object) -> object:
        nonlocal merge_calls
        schema_name = parameter.structured_output_schema_path.name
        if schema_name == "enumerate_finding.json":
            return FakeCodexResult(
                {"findings": [{"oracle_path": "<oracle-root>/spec.md", "severity": "fatal", "title": "a", "reason": "reason a"}]}
            )
        if schema_name == "merge_finding.json":
            merge_calls += 1
            return FakeCodexResult(
                {
                    "operations": [
                        {
                            "kind": "delete",
                            "target_ids": ["finding-9999"],
                            "finding": None,
                        }
                    ]
                }
            )
        raise AssertionError(schema_name)

    with pytest.raises(CmocError, match="merge finding"):
        review_module.run_review_oracle_loop(
            root,
            root,
            [root / "oracle" / "spec.md"],
            config,
            fake_run_codex_exec,
        )

    assert merge_calls == 3

def test_apply_finding_merge_operations_enforces_kind_contract() -> None:
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
                    "oracle_path": "<oracle-root>/spec.md",
                    "severity": "fatal",
                    "title": "replacement",
                    "reason": "replacement reason",
                },
            },
            {
                "kind": "merge",
                "target_ids": ["finding-0003", "finding-0004"],
                "finding": {
                    "oracle_path": "<oracle-root>/spec.md",
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
            "oracle_path": "<oracle-root>/spec.md",
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
            "oracle_path": "<oracle-root>/spec.md",
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
    with pytest.raises(ValueError):
        review_module.apply_finding_merge_operations(
            [{"finding_id": "finding-0001"}, {"finding_id": "finding-0002"}],
            operations,
            3,
        )



