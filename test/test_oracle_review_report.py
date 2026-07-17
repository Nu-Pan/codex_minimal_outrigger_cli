"""oracle review の report と CLI 出力を検証する。

根拠:
- `{{work-root}}/oracle/doc/app_spec/sub_command/oracle_review.md`
- `{{work-root}}/oracle/doc/app_spec/codex_exec_rule.md`
- `{{work-root}}/oracle/doc/dev_rule/test_rule.md`
- `{{work-root}}/oracle/doc/dev_rule/coding_rule.md`
- `{{work-root}}/oracle/src/oracle/prompt_builder/parts/realization_standard.py`
"""

from pathlib import Path

import pytest
from _cli_support import runner
from _git_support import make_repo, run_git
from _ollama_support import run_doctor

import sub_commands.eval_oracle as eval_oracle_module
import sub_commands.oracle.review as review_module
from cmoc_runtime import SessionState
from config.cmoc_config import CmocConfig, CmocConfigOracleReview
from main import app


class _FakeCodexResult:
    """テスト用 Codex 実行結果として Structured Output を保持する。"""

    def __init__(self, output_json: dict[str, object]) -> None:
        """review 処理が読む JSON payload を保存する。"""
        self.output_json = output_json


def test_oracle_review_interrupt_reports_only_completed_enumerations(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Ctrl+C 後は列挙完了済み oracle だけを interrupted report に含める。"""
    root = make_repo(tmp_path)
    (root / "oracle" / "z.md").write_text("# z\n")
    run_git(root, "add", "oracle/z.md")
    run_git(root, "commit", "-m", "add second oracle")
    monkeypatch.chdir(root)
    assert run_doctor(root).exit_code == 0
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )
    monkeypatch.setattr(
        review_module,
        "load_config",
        lambda _root: CmocConfig(
            oracle_review=CmocConfigOracleReview(
                num_enumerate_findings_loop=1,
                num_merge_findings_loop=0,
                num_validate_findings_loop=1,
            )
        ),
    )
    calls: list[str] = []

    def interrupt_second_enumeration(
        parameter: object, **kwargs: object
    ) -> _FakeCodexResult:
        """最初の列挙だけ完了させ、二つ目の agent call を中断する。"""
        purpose = str(kwargs["purpose"])
        calls.append(purpose)
        if len(calls) == 1:
            return _FakeCodexResult({"findings": []})
        raise KeyboardInterrupt

    monkeypatch.setattr(
        review_module,
        "run_codex_exec",
        interrupt_second_enumeration,
    )

    result = runner.invoke(
        app,
        ["oracle", "review", "--scope", "full"],
        catch_exceptions=False,
    )

    assert result.exit_code == 0
    assert "# ERROR" not in result.output
    assert "ユーザー中断要求" in result.output
    assert len(calls) == 2
    report_path = Path(
        [line for line in result.output.splitlines() if line.startswith("/")][-1]
    )
    rendered = report_path.read_text()
    assert "result: interrupted" in rendered
    assert "oracle_count_total: 2" in rendered
    assert "oracle_count_evaluated: 1" in rendered
    assert "対象範囲のレビュー完了を保証しません" in rendered
    assert "`oracle/spec.md`" in rendered
    assert "`oracle/z.md`" not in rendered
    assert run_git(root, "branch", "--list", "cmoc/run/*").stdout == ""
    logs = sorted(
        (root / ".cmoc" / "gu" / "ar" / "log" / "sub_command").glob("*.jsonl")
    )
    assert '"event": "user_interruption"' in logs[-1].read_text()


def test_eval_oracle_delegates_to_oracle_review_impl(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """`eval-oracle` が scope を oracle review 実装へ渡すことを検証する。"""
    calls: list[str] = []

    def fake_oracle_review_impl(scope: str) -> None:
        """委譲された scope を記録する fake callback。"""
        calls.append(scope)

    monkeypatch.setattr(
        eval_oracle_module, "cmoc_oracle_review_impl", fake_oracle_review_impl
    )

    result = runner.invoke(app, ["eval-oracle", "-s", "full"], catch_exceptions=False)

    assert result.exit_code == 0
    assert calls == ["full"]


def test_oracle_review_writes_report(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """空の所見結果から report の節順と実行情報を検証する。"""
    ancestor = tmp_path / "oracle"
    ancestor.mkdir()
    root = make_repo(ancestor)
    monkeypatch.chdir(root)
    doctor_result = run_doctor(root)
    assert doctor_result.exit_code == 0
    fork_result = runner.invoke(app, ["session", "fork"], catch_exceptions=False)
    assert fork_result.exit_code == 0
    calls: list[str] = []

    def fake_run_codex_exec(parameter: object, **kwargs: object) -> _FakeCodexResult:
        """Structured Output schema に対応する最小の fake 応答を返す。"""
        calls.append(kwargs["purpose"])
        schema_name = parameter.structured_output_schema_path.name
        if schema_name == "enumerate_finding.json":
            return _FakeCodexResult({"findings": []})
        if schema_name in {
            "validate_finding_challenger.json",
            "validate_finding_advocate.json",
        }:
            return _FakeCodexResult({"reasons": []})
        if schema_name == "judge_finding.json":
            return _FakeCodexResult({"verdict": "reject", "reason": "no finding"})
        raise AssertionError(schema_name)

    monkeypatch.setattr(review_module, "run_codex_exec", fake_run_codex_exec)

    result = runner.invoke(
        app, ["oracle", "review", "--scope", "full"], catch_exceptions=False
    )

    assert result.exit_code == 0
    report_path = Path(
        [line for line in result.output.splitlines() if line.startswith("/")][-1]
    )
    assert report_path.is_file()
    rendered = report_path.read_text()
    required_sections = [
        "# cmoc oracle review report",
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
    assert any(call.startswith("oracle review enumerate findings") for call in calls)
    assert "oracle review merge findings" not in calls


def test_oracle_review_report_outputs_accepted_and_rejected_findings(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """accepted/rejected finding が severity 別の report 節へ分類されることを検証する。"""
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert run_doctor(root).exit_code == 0
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )
    enumerated = False

    def fake_run_codex_exec(parameter: object, **kwargs: object) -> _FakeCodexResult:
        """Structured Output schema に対応する最小の fake 応答を返す。"""
        nonlocal enumerated
        schema_name = parameter.structured_output_schema_path.name
        if schema_name == "enumerate_finding.json":
            if enumerated:
                return _FakeCodexResult({"findings": []})
            enumerated = True
            return _FakeCodexResult(
                {
                    "findings": [
                        {
                            "oracle_path": "{{oracle-root}}/spec.md",
                            "severity": "fatal",
                            "title": "accepted fatal",
                            "reason": "fatal accepted reason",
                        },
                        {
                            "oracle_path": "{{oracle-root}}/spec.md",
                            "severity": "fatal",
                            "title": "rejected fatal",
                            "reason": "fatal reason",
                        },
                        {
                            "oracle_path": "{{oracle-root}}/spec.md",
                            "severity": "minor",
                            "title": "accepted minor",
                            "reason": "minor reason",
                        },
                        {
                            "oracle_path": "{{oracle-root}}/spec.md",
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
            return _FakeCodexResult({"reasons": []})
        if schema_name == "merge_finding.json":
            return _FakeCodexResult({"operations": []})
        if schema_name == "judge_finding.json":
            if kwargs["purpose"].endswith(("finding-0001", "finding-0003")):
                return _FakeCodexResult({"verdict": "accept", "reason": "accepted"})
            return _FakeCodexResult({"verdict": "reject", "reason": "rejected"})
        raise AssertionError(schema_name)

    monkeypatch.setattr(review_module, "run_codex_exec", fake_run_codex_exec)

    result = runner.invoke(
        app, ["oracle", "review", "--scope", "full"], catch_exceptions=False
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
def test_oracle_review_report_includes_rejected_findings(
    tmp_path: Path,
    severity: str,
    expected_fatal_count: int,
    expected_minor_count: int,
) -> None:
    """rejected finding が severity 別の節と件数へ出力されることを検証する。"""
    root = tmp_path
    rendered = review_module.render_oracle_review_report(
        root,
        "full",
        "cmoc/session/session-1",
        SessionState(),
        1,
        [root / "oracle" / "spec.md"],
        [
            {
                "finding_id": "finding-0001",
                "oracle_path": "{{oracle-root}}/spec.md",
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


def test_oracle_review_report_counts_oracle_root_alias_findings(
    tmp_path: Path,
) -> None:
    """`{{oracle-root}}` alias の finding が report の path 件数へ反映されることを検証する。"""
    root = tmp_path
    rendered = review_module.render_oracle_review_report(
        root,
        "full",
        "cmoc/session/session-1",
        SessionState(),
        1,
        [
            root
            / ".cmoc"
            / "gu"
            / "worktree"
            / "session-1"
            / "run-1"
            / "oracle"
            / "a.md"
        ],
        [
            {
                "finding_id": "finding-0001",
                "oracle_path": "{{oracle-root}}/a.md",
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


def test_oracle_review_report_counts_symlink_findings_by_repository_path(
    tmp_path: Path,
) -> None:
    """oracle 配下 symlink の finding を link 先ではなく対象行へ集計する。"""
    root = tmp_path
    (root / "oracle").mkdir()
    target = root / "memo.md"
    target.write_text("# memo\n")
    oracle_link = root / "oracle" / "memo-link.md"
    oracle_link.symlink_to("../memo.md")
    rendered = review_module.render_oracle_review_report(
        root,
        "full",
        "cmoc/session/session-1",
        SessionState(),
        1,
        [oracle_link],
        [
            {
                "finding_id": "finding-0001",
                "oracle_path": "{{oracle-root}}/memo-link.md",
                "severity": "fatal",
                "verdict": "accept",
                "title": "accepted symlink finding",
                "reason": "symlink reason",
            }
        ],
        "cmoc/run/session-1/run-1",
        "fork",
        None,
    )

    assert "| 1 | `oracle/memo-link.md` | 1 |" in rendered


def test_oracle_review_accepts_short_scope_option(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """短縮 `-s` option が report の scope に反映されることを検証する。"""
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert run_doctor(root).exit_code == 0
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )

    def fake_run_codex_exec(parameter: object, **kwargs: object) -> _FakeCodexResult:
        """Structured Output schema に対応する最小の fake 応答を返す。"""
        schema_name = parameter.structured_output_schema_path.name
        if schema_name == "enumerate_finding.json":
            return _FakeCodexResult({"findings": []})
        if schema_name in {
            "validate_finding_challenger.json",
            "validate_finding_advocate.json",
        }:
            return _FakeCodexResult({"reasons": []})
        if schema_name == "judge_finding.json":
            return _FakeCodexResult({"verdict": "reject", "reason": "no finding"})
        raise AssertionError(schema_name)

    monkeypatch.setattr(review_module, "run_codex_exec", fake_run_codex_exec)

    result = runner.invoke(
        app, ["oracle", "review", "-s", "full"], catch_exceptions=False
    )

    assert result.exit_code == 0
    report_path = Path(
        [line for line in result.output.splitlines() if line.startswith("/")][-1]
    )
    rendered = report_path.read_text()
    assert "scope: full" in rendered


def test_oracle_review_writes_error_report_on_processing_failure(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """judge 失敗時の error report 保存・提示と未判定 finding の扱いを検証する。

    根拠:
        {{work-root}}/oracle/doc/app_spec/sub_command/oracle_review.md
        {{work-root}}/oracle/doc/dev_rule/coding_rule.md
    """
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert run_doctor(root).exit_code == 0
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )

    def fail_run_codex_exec(parameter: object, **kwargs: object) -> _FakeCodexResult:
        """列挙・検証は成功させ、judge 呼び出しだけを失敗させる fake callback。"""
        schema_name = parameter.structured_output_schema_path.name
        if schema_name == "enumerate_finding.json":
            return _FakeCodexResult(
                {
                    "findings": [
                        {
                            "oracle_path": "{{oracle-root}}/spec.md",
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
            return _FakeCodexResult({"reasons": []})
        if schema_name == "merge_finding.json":
            return _FakeCodexResult({"operations": []})
        assert schema_name == "judge_finding.json"
        purpose = kwargs.get("purpose")
        assert isinstance(purpose, str) and "judge" in purpose
        raise RuntimeError("judge failed")

    monkeypatch.setattr(review_module, "run_codex_exec", fail_run_codex_exec)

    result = runner.invoke(app, ["oracle", "review", "--scope", "full"])

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
