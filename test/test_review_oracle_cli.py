"""review oracle の report 生成と所見 loop を CLI 経由で検証する。

このファイルは 16,000 文字を超えるが、責務境界は oracle review の外部挙動と
所見評価 loop の制御を検証することに閉じている。対象 oracle の選択、report 生成、
列挙・検証・judge・merge、上限到達、join commit の扱いは同じ review run の状態と
出力を共有するため、分割すると同じ fake Codex 応答と report 文脈が分散する。
現状は review oracle の読み取り文脈を一箇所に保つ方が凝集性が高い。
根拠: <work-root>/oracle/src/oracle/prompt_builder/parts/realization_standard.py
"""

import subprocess
from pathlib import Path

import pytest

import commons.indexing as indexing_module
import commons.runtime_codex_preflight as codex_preflight_module
from _support import (
    add_tracked_ignored_oracle_file,
    make_repo,
    run_git,
    runner,
    run_doctor,
)
from cmoc_runtime import CmocError, SessionState
from config.cmoc_config import CmocConfig, CmocConfigReviewOracle
from main import app
import sub_commands.eval_oracle as eval_oracle_module
import sub_commands.review.oracle as review_module
from sub_commands.review_paths import finding_oracle_path
from sub_commands.review_targets import enumerate_review_all_oracle_files


def test_eval_oracle_delegates_to_review_oracle_impl(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls: list[str] = []

    def fake_review_oracle_impl(scope: str) -> None:
        calls.append(scope)

    monkeypatch.setattr(
        eval_oracle_module, "cmoc_review_oracle_impl", fake_review_oracle_impl
    )

    result = runner.invoke(app, ["eval-oracle", "-s", "full"], catch_exceptions=False)

    assert result.exit_code == 0
    assert calls == ["full"]


def test_finding_oracle_path_rejects_relative_without_placeholder(tmp_path: Path) -> None:
    assert finding_oracle_path({"oracle_path": "oracle/spec.md"}, tmp_path) is None
    assert (
        finding_oracle_path({"oracle_path": "<oracle-root>/spec.md"}, tmp_path)
        == (tmp_path / "oracle" / "spec.md").resolve()
    )


def test_finding_oracle_path_resolves_work_root_from_review_worktree(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    review_parent = tmp_path / "review"
    review_parent.mkdir()
    unrelated = make_repo(tmp_path)
    review_worktree = make_repo(review_parent)
    monkeypatch.chdir(unrelated)

    assert finding_oracle_path(
        {"oracle_path": "<work-root>/oracle/spec.md"}, review_worktree
    ) == (review_worktree / "oracle" / "spec.md").resolve()


def test_review_oracle_writes_report(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    ancestor = tmp_path / "oracle"
    ancestor.mkdir()
    root = make_repo(ancestor)
    monkeypatch.chdir(root)
    doctor_result = run_doctor(root)
    assert doctor_result.exit_code == 0
    fork_result = runner.invoke(app, ["session", "fork"], catch_exceptions=False)
    assert fork_result.exit_code == 0
    calls: list[str] = []

    class FakeCodexResult:
        def __init__(self, output_json: dict[str, object]) -> None:
            self.output_json = output_json

    def fake_run_codex_exec(parameter: object, **kwargs: object) -> object:
        calls.append(kwargs["purpose"])
        schema_name = parameter.structured_output_schema_path.name
        if schema_name == "enumerate_finding.json":
            return FakeCodexResult({"findings": []})
        if schema_name in {
            "validate_finding_challenger.json",
            "validate_finding_advocate.json",
        }:
            return FakeCodexResult({"reasons": []})
        if schema_name == "judge_finding.json":
            return FakeCodexResult({"verdict": "reject", "reason": "no finding"})
        raise AssertionError(schema_name)

    monkeypatch.setattr(review_module, "run_codex_exec", fake_run_codex_exec)

    result = runner.invoke(
        app, ["review", "oracle", "--scope", "full"], catch_exceptions=False
    )

    assert result.exit_code == 0
    report_path = Path(
        [line for line in result.output.splitlines() if line.startswith("/")][-1]
    )
    assert report_path.is_file()
    rendered = report_path.read_text()
    required_sections = [
        "# cmoc review oracle report",
        "## Verdict",
        "## Evaluated oracle file",
        "## Fatal findings",
        "## Minor findings",
    ]
    section_offsets = [rendered.index(section) for section in required_sections]
    assert section_offsets == sorted(section_offsets)
    h2_sections = [line for line in rendered.splitlines() if line.startswith("## ")]
    assert h2_sections[: len(required_sections) - 1] == required_sections[1:]
    assert "`oracle/spec.md`" in rendered
    assert "review_join_commit: null" in rendered
    assert "session_id:" not in rendered
    assert any(call.startswith("review oracle enumerate findings") for call in calls)
    assert "review oracle merge findings" not in calls


def test_review_oracle_report_outputs_accepted_and_rejected_findings(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert run_doctor(root).exit_code == 0
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )
    enumerated = False

    class FakeCodexResult:
        def __init__(self, output_json: dict[str, object]) -> None:
            self.output_json = output_json

    def fake_run_codex_exec(parameter: object, **kwargs: object) -> object:
        nonlocal enumerated
        schema_name = parameter.structured_output_schema_path.name
        if schema_name == "enumerate_finding.json":
            if enumerated:
                return FakeCodexResult({"findings": []})
            enumerated = True
            return FakeCodexResult(
                {
                    "findings": [
                        {
                            "oracle_path": "<oracle-root>/spec.md",
                            "severity": "fatal",
                            "title": "accepted fatal",
                            "reason": "fatal accepted reason",
                        },
                        {
                            "oracle_path": "<oracle-root>/spec.md",
                            "severity": "fatal",
                            "title": "rejected fatal",
                            "reason": "fatal reason",
                        },
                        {
                            "oracle_path": "<oracle-root>/spec.md",
                            "severity": "minor",
                            "title": "accepted minor",
                            "reason": "minor reason",
                        },
                        {
                            "oracle_path": "<oracle-root>/spec.md",
                            "severity": "minor",
                            "title": "rejected minor",
                            "reason": "minor rejected reason",
                        },
                    ]
                }
            )
        if schema_name in {
            "validate_finding_challenger.json",
            "validate_finding_advocate.json",
        }:
            return FakeCodexResult({"reasons": []})
        if schema_name == "merge_finding.json":
            return FakeCodexResult({"operations": []})
        if schema_name == "judge_finding.json":
            if kwargs["purpose"].endswith(("finding-0001", "finding-0003")):
                return FakeCodexResult({"verdict": "accept", "reason": "accepted"})
            return FakeCodexResult({"verdict": "reject", "reason": "rejected"})
        raise AssertionError(schema_name)

    monkeypatch.setattr(review_module, "run_codex_exec", fake_run_codex_exec)

    result = runner.invoke(
        app, ["review", "oracle", "--scope", "full"], catch_exceptions=False
    )

    assert result.exit_code == 0
    rendered = Path(
        [line for line in result.output.splitlines() if line.startswith("/")][-1]
    ).read_text()
    h2_sections = [line for line in rendered.splitlines() if line.startswith("## ")]
    assert h2_sections[:4] == [
        "## Verdict",
        "## Evaluated oracle file",
        "## Fatal findings",
        "## Minor findings",
    ]
    detail_order = [
        "### Accepted fatal findings",
        "accepted fatal",
        "### Accepted minor findings",
        "accepted minor",
        "### Rejected fatal findings",
        "rejected fatal",
        "### Rejected minor findings",
        "rejected minor",
    ]
    assert [rendered.index(text) for text in detail_order] == sorted(
        rendered.index(text) for text in detail_order
    )
    assert rendered.index("## Minor findings") < rendered.index("## Finding details")
    assert rendered.index("accepted minor") < rendered.index("rejected fatal")
    assert "result: fatal" in rendered
    assert "fatal_findings_accepted_count: 1" in rendered
    assert "minor_findings_accepted_count: 1" in rendered
    assert "fatal_findings_rejected_count: 1" in rendered
    assert "minor_findings_rejected_count: 1" in rendered
    assert "judge reason: accepted" in rendered
    assert "judge reason: rejected" in rendered


@pytest.mark.parametrize(
    ("severity", "expected_fatal_count", "expected_minor_count"),
    [
        ("fatal", 1, 0),
        ("minor", 0, 1),
    ],
)
def test_review_oracle_report_includes_rejected_findings(
    tmp_path: Path,
    severity: str,
    expected_fatal_count: int,
    expected_minor_count: int,
) -> None:
    root = tmp_path
    rendered = review_module.render_review_oracle_report(
        root,
        "full",
        "cmoc/session/session-1",
        SessionState(),
        1,
        [root / "oracle" / "spec.md"],
        [
            {
                "finding_id": "finding-0001",
                "oracle_path": "<oracle-root>/spec.md",
                "severity": severity,
                "verdict": "reject",
                "title": "rejected finding",
                "reason": "rejected reason",
                "judge_reason": "judge rejected reason",
            }
        ],
        "cmoc/run/session-1/run-1",
        "fork",
        None,
    )

    assert "result: ok" in rendered
    assert "レビュー対象の oracle file に、問題は何ら見つかりませんでした。" in rendered
    assert f"fatal_findings_rejected_count: {expected_fatal_count}" in rendered
    assert f"minor_findings_rejected_count: {expected_minor_count}" in rendered
    assert "## Fatal findings" in rendered
    assert "## Minor findings" in rendered
    h2_sections = [line for line in rendered.splitlines() if line.startswith("## ")]
    assert h2_sections[:4] == [
        "## Verdict",
        "## Evaluated oracle file",
        "## Fatal findings",
        "## Minor findings",
    ]
    assert "### Rejected fatal findings" in rendered
    assert "### Rejected minor findings" in rendered
    assert "rejected finding" in rendered
    assert "## Finding details" in rendered
    assert rendered.index("## Fatal findings") < rendered.index("## Minor findings")
    assert rendered.index("## Minor findings") < rendered.index("## Finding details")
    finding_offset = rendered.index("rejected finding")
    if severity == "fatal":
        assert rendered.index("### Rejected fatal findings") < finding_offset
    else:
        assert rendered.index("### Rejected minor findings") < finding_offset
    assert "rejected reason" in rendered
    assert "judge reason: judge rejected reason" in rendered
    assert "session_id:" not in rendered


def test_review_oracle_report_counts_oracle_root_alias_findings(
    tmp_path: Path,
) -> None:
    root = tmp_path
    rendered = review_module.render_review_oracle_report(
        root,
        "full",
        "cmoc/session/session-1",
        SessionState(),
        1,
        [root / ".cmoc" / "local" / "worktree" / "session-1" / "run-1" / "oracle" / "a.md"],
        [
            {
                "finding_id": "finding-0001",
                "oracle_path": "<oracle-root>/a.md",
                "severity": "fatal",
                "verdict": "accept",
                "title": "accepted finding",
                "reason": "accepted reason",
            }
        ],
        "cmoc/run/session-1/run-1",
        "fork",
        None,
    )

    assert "| 1 | `oracle/a.md` | 1 |" in rendered


def test_review_oracle_uses_linked_worktree_branch_and_oracle(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """linked worktree 上の session branch と oracle を review 対象にする。"""
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert run_doctor(root).exit_code == 0
    linked = root / ".cmoc" / "local" / "worktree" / "linked-review"
    run_git(root, "worktree", "add", "-b", "linked-review-home", str(linked), "HEAD")
    (linked / "oracle" / "linked.md").write_text("# linked oracle\n")
    run_git(linked, "add", "oracle/linked.md")
    run_git(linked, "commit", "-m", "linked oracle change")
    linked_commit = run_git(linked, "rev-parse", "HEAD").stdout.strip()
    monkeypatch.chdir(linked)
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )
    calls: list[str] = []
    review_worktrees: list[Path] = []

    class FakeCodexResult:
        def __init__(self, output_json: dict[str, object]) -> None:
            self.output_json = output_json

    def fake_run_codex_exec(parameter: object, **kwargs: object) -> object:
        review_worktrees.append(Path.cwd())
        calls.append(kwargs["purpose"])
        schema_name = parameter.structured_output_schema_path.name
        if schema_name == "enumerate_finding.json":
            return FakeCodexResult({"findings": []})
        raise AssertionError(schema_name)

    monkeypatch.setattr(review_module, "run_codex_exec", fake_run_codex_exec)

    result = runner.invoke(
        app, ["review", "oracle", "--scope", "full"], catch_exceptions=False
    )

    assert result.exit_code == 0
    report_path = Path(
        [line for line in result.output.splitlines() if line.startswith("/")][-1]
    )
    assert report_path.is_relative_to(root / ".cmoc" / "local" / "report")
    assert not report_path.is_relative_to(linked)
    rendered = report_path.read_text()
    assert f"review_fork_commit: {linked_commit}" in rendered
    assert "`oracle/linked.md`" in rendered
    branch = run_git(linked, "branch", "--show-current").stdout.strip()
    assert branch.startswith("cmoc/session/")
    session_id = branch.removeprefix("cmoc/session/")
    assert review_worktrees
    for review_worktree in review_worktrees:
        assert review_worktree.parent == root / ".cmoc" / "local" / "worktree" / session_id
        assert not review_worktree.is_relative_to(linked)
    assert any("linked.md" in call for call in calls)


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
                            "challenger_reasons": ["old challenger reason"],
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
                        {"oracle_path": "<oracle-root>/spec.md", "title": "a"},
                        {"oracle_path": "<oracle-root>/spec.md", "title": "b"},
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
                            "finding": {"title": "merged"},
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
                {"findings": [{"oracle_path": "<oracle-root>/spec.md", "title": "a"}]}
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
                "finding": {"title": "replacement"},
            },
            {
                "kind": "merge",
                "target_ids": ["finding-0003", "finding-0004"],
                "finding": {"title": "merged"},
            },
        ],
        5,
    )

    assert added_count == 2
    assert merged == [
        {
            "title": "replacement",
            "finding_id": "finding-0005",
            "advocate_reasons": [],
            "challenger_reasons": [],
            "verdict": None,
            "judge_reason": None,
        },
        {
            "title": "merged",
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


def test_review_oracle_full_scope_keeps_tracked_ignored_oracle_files(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    root = make_repo(tmp_path)
    add_tracked_ignored_oracle_file(root)
    outside_target = tmp_path / "ignored-link-target.md"
    outside_target.write_text("# outside\n")
    with (root / ".gitignore").open("a") as file:
        file.write("oracle/ignored-link.md\noracle/untracked-ignored.md\n")
    (root / "oracle" / "ignored-link.md").symlink_to(outside_target)
    (root / "oracle" / "untracked-ignored.md").write_text("# untracked ignored\n")
    (root / "oracle" / "asset.bin").write_bytes(b"\x00\x01binary\n")
    (root / "memo" / "oracle").mkdir(parents=True)
    (root / "memo" / "oracle" / "draft.md").write_text("# memo draft\n")
    (root / "oracle" / "memo").mkdir()
    (root / "oracle" / "memo" / "kept.md").write_text("# oracle memo dir\n")
    (root / "oracle" / "memo-link.md").symlink_to("../memo/oracle/draft.md")
    run_git(
        root,
        "add",
        "-f",
        ".gitignore",
        "oracle/asset.bin",
        "oracle/ignored-link.md",
        "memo/oracle/draft.md",
        "oracle/memo/kept.md",
        "oracle/memo-link.md",
    )
    run_git(root, "commit", "-m", "add binary and memo-shaped oracle")
    monkeypatch.chdir(root)
    assert run_doctor(root).exit_code == 0
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )
    calls: list[str] = []

    class FakeCodexResult:
        def __init__(self, output_json: dict[str, object]) -> None:
            self.output_json = output_json

    def fake_run_codex_exec(parameter: object, **kwargs: object) -> object:
        calls.append(kwargs["purpose"])
        schema_name = parameter.structured_output_schema_path.name
        if schema_name == "enumerate_finding.json":
            return FakeCodexResult({"findings": []})
        raise AssertionError(schema_name)

    monkeypatch.setattr(review_module, "run_codex_exec", fake_run_codex_exec)

    result = runner.invoke(
        app, ["review", "oracle", "--scope", "full"], catch_exceptions=False
    )

    assert result.exit_code == 0
    rendered = Path(
        [line for line in result.output.splitlines() if line.startswith("/")][-1]
    ).read_text()
    assert "oracle_count_total: 6" in rendered
    assert "oracle_count_evaluated: 6" in rendered
    assert "`oracle/asset.bin`" in rendered
    assert "`oracle/ignored-link.md`" in rendered
    assert "`oracle/ignored.md`" in rendered
    assert "`oracle/memo/kept.md`" in rendered
    assert "`oracle/memo-link.md`" in rendered
    assert "`oracle/spec.md`" in rendered
    assert "oracle/untracked-ignored.md" not in rendered
    assert "memo/oracle/draft.md" not in rendered
    enumerate_calls = [
        call for call in calls if call.startswith("review oracle enumerate findings")
    ]
    assert len(enumerate_calls) == 6


def test_review_oracle_accepts_short_scope_option(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert run_doctor(root).exit_code == 0
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )

    class FakeCodexResult:
        def __init__(self, output_json: dict[str, object]) -> None:
            self.output_json = output_json

    def fake_run_codex_exec(parameter: object, **kwargs: object) -> object:
        schema_name = parameter.structured_output_schema_path.name
        if schema_name == "enumerate_finding.json":
            return FakeCodexResult({"findings": []})
        if schema_name in {
            "validate_finding_challenger.json",
            "validate_finding_advocate.json",
        }:
            return FakeCodexResult({"reasons": []})
        if schema_name == "judge_finding.json":
            return FakeCodexResult({"verdict": "reject", "reason": "no finding"})
        raise AssertionError(schema_name)

    monkeypatch.setattr(review_module, "run_codex_exec", fake_run_codex_exec)

    result = runner.invoke(
        app, ["review", "oracle", "-s", "full"], catch_exceptions=False
    )

    assert result.exit_code == 0
    report_path = Path(
        [line for line in result.output.splitlines() if line.startswith("/")][-1]
    )
    rendered = report_path.read_text()
    assert "scope: full" in rendered


def test_review_oracle_session_scope_reports_total_and_no_targets(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert run_doctor(root).exit_code == 0
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )
    calls: list[str] = []

    def fail_run_codex_exec(parameter: object, **kwargs: object) -> None:
        calls.append(kwargs["purpose"])
        raise AssertionError(
            "no session-scope oracle targets should skip review Codex calls"
        )

    monkeypatch.setattr(review_module, "run_codex_exec", fail_run_codex_exec)

    result = runner.invoke(app, ["review", "oracle"], catch_exceptions=False)

    assert result.exit_code == 0
    assert calls == []
    report_path = Path(
        [line for line in result.output.splitlines() if line.startswith("/")][-1]
    )
    rendered = report_path.read_text()
    assert "scope: session" in rendered
    assert "oracle_count_total: 1" in rendered
    assert "oracle_count_evaluated: 0" in rendered
    assert "result: no_targets" in rendered
    assert "レビュー対象 oracle が 0 件でした。" in rendered


@pytest.mark.parametrize(
    ("relative_path", "content"),
    [
        ("oracle/uncommitted.md", "# uncommitted\n"),
        ("README.md", "dirty\n"),
    ],
)
def test_review_oracle_rejects_uncommitted_worktree_changes(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    relative_path: str,
    content: str,
) -> None:
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert run_doctor(root).exit_code == 0
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )
    (root / relative_path).write_text(content)

    result = runner.invoke(app, ["review", "oracle"])

    assert result.exit_code != 0
    assert "git 未コミット差分" in result.output
    assert relative_path in result.output


def test_review_oracle_session_scope_keeps_changed_tracked_ignored_oracle_files(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    root = make_repo(tmp_path)
    add_tracked_ignored_oracle_file(root)
    outside_target = tmp_path / "ignored-link-target.md"
    outside_target.write_text("# outside\n")
    with (root / ".gitignore").open("a") as file:
        file.write("oracle/ignored-link.md\n")
    (root / "oracle" / "ignored-link.md").symlink_to(outside_target)
    run_git(root, "add", "-f", ".gitignore", "oracle/ignored-link.md")
    run_git(root, "commit", "-m", "add ignored oracle symlink")
    monkeypatch.chdir(root)
    assert run_doctor(root).exit_code == 0
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )
    (root / "oracle" / "ignored.md").write_text("# ignored changed\n")
    changed_target = tmp_path / "changed-ignored-link-target.md"
    changed_target.write_text("# changed outside\n")
    (root / "oracle" / "ignored-link.md").unlink()
    (root / "oracle" / "ignored-link.md").symlink_to(changed_target)
    run_git(root, "add", "oracle/ignored.md")
    run_git(root, "add", "-f", "oracle/ignored-link.md")
    run_git(root, "commit", "-m", "change ignored oracle")
    calls: list[str] = []

    class FakeCodexResult:
        def __init__(self, output_json: dict[str, object]) -> None:
            self.output_json = output_json

    def fake_run_codex_exec(parameter: object, **kwargs: object) -> object:
        calls.append(kwargs["purpose"])
        schema_name = parameter.structured_output_schema_path.name
        if schema_name == "enumerate_finding.json":
            return FakeCodexResult({"findings": []})
        raise AssertionError(schema_name)

    monkeypatch.setattr(review_module, "run_codex_exec", fake_run_codex_exec)

    result = runner.invoke(app, ["review", "oracle"], catch_exceptions=False)

    assert result.exit_code == 0
    enumerate_calls = [
        call for call in calls if call.startswith("review oracle enumerate findings")
    ]
    assert len(enumerate_calls) == 2
    rendered = Path(
        [line for line in result.output.splitlines() if line.startswith("/")][-1]
    ).read_text()
    assert "oracle_count_total: 3" in rendered
    assert "oracle_count_evaluated: 2" in rendered
    assert "`oracle/ignored-link.md`" in rendered
    assert "`oracle/ignored.md`" in rendered


def test_review_oracle_session_scope_uses_review_fork_commit(
    tmp_path: Path,
) -> None:
    """session scope の差分終点は実行時 HEAD ではなく review fork commit に固定する。"""
    root = make_repo(tmp_path)
    state = SessionState()
    state.session.session_start_commit = run_git(
        root, "rev-parse", "HEAD"
    ).stdout.strip()
    (root / "oracle" / "fork.md").write_text("# fork\n")
    run_git(root, "add", "oracle/fork.md")
    run_git(root, "commit", "-m", "review fork target")
    review_fork_commit = run_git(root, "rev-parse", "HEAD").stdout.strip()
    (root / "oracle" / "after.md").write_text("# after\n")
    run_git(root, "add", "oracle/after.md")
    run_git(root, "commit", "-m", "after review fork")

    targets = review_module.enumerate_review_oracle_targets(
        root, "session", state, review_fork_commit
    )

    assert targets == [(root / "oracle" / "fork.md").resolve()]


def test_review_oracle_target_enumeration_excludes_agents_and_index(
    tmp_path: Path,
) -> None:
    """oracle file 定義から外れる AGENTS.md と INDEX.md をレビュー対象にしない。"""
    root = make_repo(tmp_path)
    spec = root / "oracle" / "spec.md"
    agents = root / "oracle" / "AGENTS.md"
    index = root / "oracle" / "INDEX.md"
    spec.write_text("# spec\n")
    agents.write_text("# agents\n")
    index.write_text("# index\n")

    assert enumerate_review_all_oracle_files(root) == [spec.resolve()]


def test_review_oracle_target_enumeration_classifies_oracle_symlink_by_repo_path(
    tmp_path: Path,
) -> None:
    """oracle 配下 symlink は link 先ではなく repository path で分類する。"""
    root = make_repo(tmp_path)
    (root / "memo").mkdir()
    (root / "memo" / "draft.md").write_text("# draft\n")
    oracle_link = root / "oracle" / "memo-link.md"
    oracle_link.symlink_to("../memo/draft.md")
    run_git(root, "add", "memo/draft.md", "oracle/memo-link.md")
    run_git(root, "commit", "-m", "add oracle symlink")

    assert oracle_link.absolute() in enumerate_review_all_oracle_files(root)


def test_review_oracle_merges_review_index_changes(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert run_doctor(root).exit_code == 0
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )
    session_id = (
        run_git(root, "branch", "--show-current")
        .stdout.strip()
        .removeprefix("cmoc/session/")
    )
    review_worktrees: list[Path] = []

    class FakeCodexResult:
        def __init__(self, output_json: dict[str, object]) -> None:
            self.output_json = output_json

    def fake_run_codex_exec(parameter: object, **kwargs: object) -> object:
        review_worktrees.append(Path.cwd())
        schema_name = parameter.structured_output_schema_path.name
        if schema_name == "enumerate_finding.json":
            (Path.cwd() / "INDEX.md").write_text("# generated review index\n")
            return FakeCodexResult({"findings": []})
        if schema_name in {
            "validate_finding_challenger.json",
            "validate_finding_advocate.json",
        }:
            return FakeCodexResult({"reasons": []})
        if schema_name == "judge_finding.json":
            return FakeCodexResult({"verdict": "reject", "reason": "no finding"})
        raise AssertionError(schema_name)

    monkeypatch.setattr(review_module, "run_codex_exec", fake_run_codex_exec)

    result = runner.invoke(
        app, ["review", "oracle", "--scope", "full"], catch_exceptions=False
    )

    assert result.exit_code == 0
    assert (root / "INDEX.md").read_text() == "# generated review index\n"
    rendered = Path(
        [line for line in result.output.splitlines() if line.startswith("/")][-1]
    ).read_text()
    assert "review_join_commit: null" not in rendered
    assert review_worktrees
    for review_worktree in review_worktrees:
        assert review_worktree.parent == root / ".cmoc" / "local" / "worktree" / session_id
    assert not any(
        path.name == ".git" for path in (root / ".cmoc" / "local" / "worktree").rglob(".git")
    )
    assert not (root / ".cmoc" / "local" / "worktree" / "review").exists()


def test_review_oracle_merges_preflight_committed_index_changes(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert run_doctor(root).exit_code == 0
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )
    review_worktrees: list[Path] = []

    def fake_update_indexes(
        update_root: Path, codex_exec: object | None = None
    ) -> list[Path]:
        review_worktrees.append(update_root)
        index_path = update_root / "INDEX.md"
        index_path.write_text("# preflight review index\n")
        return [index_path]

    class FakeCodexResult:
        def __init__(self, output_json: dict[str, object]) -> None:
            self.output_json = output_json

    def fake_runtime_run_codex_exec(parameter: object, **kwargs: object) -> object:
        schema_name = parameter.structured_output_schema_path.name
        if schema_name == "enumerate_finding.json":
            return FakeCodexResult({"findings": []})
        raise AssertionError(schema_name)

    monkeypatch.setattr(indexing_module, "update_indexes", fake_update_indexes)
    monkeypatch.setattr(
        codex_preflight_module, "runtime_run_codex_exec", fake_runtime_run_codex_exec
    )

    result = runner.invoke(
        app, ["review", "oracle", "--scope", "full"], catch_exceptions=False
    )

    assert result.exit_code == 0
    assert (root / "INDEX.md").read_text() == "# preflight review index\n"
    assert review_worktrees and all(path != root for path in review_worktrees)
    assert (
        run_git(root, "log", "--first-parent", "-1", "--pretty=%s").stdout.strip()
        != "cmoc indexing"
    )
    rendered = Path(
        [line for line in result.output.splitlines() if line.startswith("/")][-1]
    ).read_text()
    assert "review_join_commit: null" not in rendered


def test_review_oracle_resolves_index_conflict_when_session_deleted_index(
    tmp_path: Path,
) -> None:
    root = make_repo(tmp_path)
    home_branch = run_git(root, "branch", "--show-current").stdout.strip()
    (root / "INDEX.md").write_text("base\n")
    run_git(root, "add", "INDEX.md")
    run_git(root, "commit", "-m", "add index")
    run_git(root, "switch", "-c", "review")
    (root / "INDEX.md").write_text("review\n")
    run_git(root, "add", "INDEX.md")
    run_git(root, "commit", "-m", "review index")
    run_git(root, "switch", home_branch)
    (root / "INDEX.md").unlink()
    run_git(root, "add", "INDEX.md")
    run_git(root, "commit", "-m", "delete index")
    merge = subprocess.run(
        ["git", "merge", "--no-ff", "review"],
        cwd=root,
        text=True,
        capture_output=True,
    )
    assert merge.returncode != 0

    resolved = review_module.resolve_review_index_conflicts(root)

    assert resolved is True
    assert not (root / "INDEX.md").exists()
    assert (
        run_git(root, "diff", "--name-only", "--diff-filter=U").stdout.strip() == ""
    )
    assert "Merge branch 'review'" in run_git(root, "log", "-1", "--pretty=%B").stdout


def test_review_oracle_writes_error_report_on_processing_failure(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert run_doctor(root).exit_code == 0
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )

    class FakeCodexResult:
        def __init__(self, output_json: dict[str, object]) -> None:
            self.output_json = output_json

    def fail_run_codex_exec(parameter: object, **kwargs: object) -> None:
        schema_name = parameter.structured_output_schema_path.name
        if schema_name == "enumerate_finding.json":
            return FakeCodexResult(
                {
                    "findings": [
                        {
                            "oracle_path": "<oracle-root>/spec.md",
                            "severity": "fatal",
                            "title": "unjudged fatal",
                            "reason": "judge did not run",
                        }
                    ]
                }
            )
        if schema_name in {
            "validate_finding_challenger.json",
            "validate_finding_advocate.json",
        }:
            return FakeCodexResult({"reasons": []})
        raise RuntimeError("judge failed")

    monkeypatch.setattr(review_module, "run_codex_exec", fail_run_codex_exec)

    result = runner.invoke(app, ["review", "oracle", "--scope", "full"])

    assert result.exit_code != 0
    report_path = Path(
        [line for line in result.output.splitlines() if line.startswith("/")][-1]
    )
    rendered = report_path.read_text()
    assert "result: error" in rendered
    assert "fatal_findings_rejected_count: 0" in rendered
    assert "minor_findings_rejected_count: 0" in rendered
    assert "[unjudged] unjudged fatal" not in rendered
    assert "レビュー処理が途中で失敗しました。" in rendered
    assert "Error: `judge failed`" in rendered
    assert "# ERROR" in result.stdout
    assert "# ERROR" not in result.stderr


@pytest.mark.parametrize("change_kind", ["unstaged", "staged", "untracked"])
def test_review_oracle_rejects_non_index_worktree_changes(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    change_kind: str,
) -> None:
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert run_doctor(root).exit_code == 0
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )

    class FakeCodexResult:
        def __init__(self, output_json: dict[str, object]) -> None:
            self.output_json = output_json

    def fake_run_codex_exec(parameter: object, **kwargs: object) -> object:
        schema_name = parameter.structured_output_schema_path.name
        if schema_name == "enumerate_finding.json":
            if change_kind == "untracked":
                (Path.cwd() / "generated.txt").write_text("unexpected\n")
            else:
                (Path.cwd() / "README.md").write_text("unexpected\n")
                if change_kind == "staged":
                    run_git(Path.cwd(), "add", "README.md")
            return FakeCodexResult({"findings": []})
        raise AssertionError(schema_name)

    monkeypatch.setattr(review_module, "run_codex_exec", fake_run_codex_exec)

    result = runner.invoke(app, ["review", "oracle", "--scope", "full"])

    assert result.exit_code != 0
    assert "review oracle が INDEX.md 以外の差分を作成しました。" in result.output
    assert (root / "README.md").read_text() == "# repo\n"
    assert not (root / "generated.txt").exists()
