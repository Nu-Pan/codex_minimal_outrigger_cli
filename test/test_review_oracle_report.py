"""review oracle の report と CLI 出力を検証する。"""

from pathlib import Path

import pytest

from _cli_support import runner
from _git_support import make_repo
from _ollama_support import run_doctor
from cmoc_runtime import SessionState
from main import app
import sub_commands.eval_oracle as eval_oracle_module
import sub_commands.review.oracle as review_module

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
    assert rendered.index("## Minor findings") < rendered.index("accepted minor")
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
    assert rendered.index("## Fatal findings") < rendered.index("## Minor findings")
    finding_offset = rendered.index("rejected finding")
    if severity == "fatal":
        assert rendered.index("### Rejected fatal findings") < finding_offset
        assert rendered.index("## Minor findings") < finding_offset
    else:
        assert rendered.index("## Minor findings") < finding_offset
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

