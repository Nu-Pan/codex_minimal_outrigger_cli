import subprocess
from pathlib import Path

import pytest

from _support import (
    add_tracked_ignored_oracle_file,
    make_repo,
    run_git,
    runner,
)
from config.cmoc_config import CmocConfig, CmocConfigReviewOracle
from main import app
import sub_commands.review as review_module


def test_review_oracle_writes_report(tmp_path: Path, monkeypatch) -> None:
    ancestor = tmp_path / "oracle"
    ancestor.mkdir()
    root = make_repo(ancestor)
    monkeypatch.chdir(root)
    init_result = runner.invoke(app, ["init"], catch_exceptions=False)
    assert init_result.exit_code == 0
    fork_result = runner.invoke(app, ["session", "fork"], catch_exceptions=False)
    assert fork_result.exit_code == 0
    calls: list[str] = []

    class FakeCodexResult:
        def __init__(self, output_json):
            self.output_json = output_json

    def fake_run_codex_exec(parameter, **kwargs):
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
    assert "# cmoc review oracle report" in rendered
    assert "## Verdict" in rendered
    assert "## Evaluated oracle file" in rendered
    assert "`oracle/spec.md`" in rendered
    assert "review_join_commit: null" in rendered
    assert any(call.startswith("review oracle enumerate findings") for call in calls)
    assert "review oracle merge findings" not in calls


def test_review_oracle_enumerate_receives_only_related_findings(
    tmp_path: Path, monkeypatch
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
        def __init__(self, output_json):
            self.output_json = output_json

    def fake_run_codex_exec(parameter, **kwargs):
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
                                "oracle_path": "oracle/a.md",
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


def test_review_oracle_full_scope_includes_binary_and_excludes_gitignored_oracle_files(
    tmp_path: Path,
    monkeypatch,
) -> None:
    root = make_repo(tmp_path)
    add_tracked_ignored_oracle_file(root)
    (root / "oracle" / "asset.bin").write_bytes(b"\x00\x01binary\n")
    run_git(root, "add", "oracle/asset.bin")
    run_git(root, "commit", "-m", "add binary oracle")
    monkeypatch.chdir(root)
    assert runner.invoke(app, ["init"], catch_exceptions=False).exit_code == 0
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )
    calls: list[str] = []

    class FakeCodexResult:
        def __init__(self, output_json):
            self.output_json = output_json

    def fake_run_codex_exec(parameter, **kwargs):
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
    assert "oracle_count_total: 2" in rendered
    assert "oracle_count_evaluated: 2" in rendered
    assert "`oracle/asset.bin`" in rendered
    assert "`oracle/spec.md`" in rendered
    assert "oracle/ignored.md" not in rendered
    enumerate_calls = [
        call for call in calls if call.startswith("review oracle enumerate findings")
    ]
    assert len(enumerate_calls) == 2


def test_review_oracle_accepts_short_scope_option(tmp_path: Path, monkeypatch) -> None:
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert runner.invoke(app, ["init"], catch_exceptions=False).exit_code == 0
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )

    class FakeCodexResult:
        def __init__(self, output_json):
            self.output_json = output_json

    def fake_run_codex_exec(parameter, **kwargs):
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
    monkeypatch,
) -> None:
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert runner.invoke(app, ["init"], catch_exceptions=False).exit_code == 0
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )
    calls: list[str] = []

    def fail_run_codex_exec(parameter, **kwargs):
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


def test_review_oracle_session_scope_excludes_changed_gitignored_oracle_files(
    tmp_path: Path,
    monkeypatch,
) -> None:
    root = make_repo(tmp_path)
    add_tracked_ignored_oracle_file(root)
    monkeypatch.chdir(root)
    assert runner.invoke(app, ["init"], catch_exceptions=False).exit_code == 0
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )
    (root / "oracle" / "ignored.md").write_text("# ignored changed\n")
    run_git(root, "add", "oracle/ignored.md")
    run_git(root, "commit", "-m", "change ignored oracle")
    calls: list[str] = []

    def fail_run_codex_exec(parameter, **kwargs):
        calls.append(kwargs["purpose"])
        raise AssertionError("gitignored oracle files should not be reviewed")

    monkeypatch.setattr(review_module, "run_codex_exec", fail_run_codex_exec)

    result = runner.invoke(app, ["review", "oracle"], catch_exceptions=False)

    assert result.exit_code == 0
    assert calls == []
    rendered = Path(
        [line for line in result.output.splitlines() if line.startswith("/")][-1]
    ).read_text()
    assert "oracle_count_total: 1" in rendered
    assert "oracle_count_evaluated: 0" in rendered
    assert "oracle/ignored.md" not in rendered
    assert "result: no_targets" in rendered


def test_review_oracle_merges_review_index_changes(tmp_path: Path, monkeypatch) -> None:
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert runner.invoke(app, ["init"], catch_exceptions=False).exit_code == 0
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
        def __init__(self, output_json):
            self.output_json = output_json

    def fake_run_codex_exec(parameter, **kwargs):
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
        assert review_worktree.parent == root / ".cmoc" / "worktrees" / session_id
    assert not any(
        path.name == ".git" for path in (root / ".cmoc" / "worktrees").rglob(".git")
    )
    assert not (root / ".cmoc" / "worktrees" / "review").exists()


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
    tmp_path: Path, monkeypatch
) -> None:
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert runner.invoke(app, ["init"], catch_exceptions=False).exit_code == 0
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )

    class FakeCodexResult:
        def __init__(self, output_json):
            self.output_json = output_json

    def fail_run_codex_exec(parameter, **kwargs):
        schema_name = parameter.structured_output_schema_path.name
        if schema_name == "enumerate_finding.json":
            return FakeCodexResult(
                {
                    "findings": [
                        {
                            "oracle_path": "oracle/spec.md",
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
    assert "[unjudged] unjudged fatal" not in rendered
    assert "レビュー処理が途中で失敗しました。" in rendered
    assert "Error: `judge failed`" in rendered
    assert "# ERROR" in result.stdout
    assert "# ERROR" not in result.stderr


@pytest.mark.parametrize("change_kind", ["unstaged", "staged", "untracked"])
def test_review_oracle_rejects_non_index_worktree_changes(
    tmp_path: Path,
    monkeypatch,
    change_kind: str,
) -> None:
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert runner.invoke(app, ["init"], catch_exceptions=False).exit_code == 0
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )

    class FakeCodexResult:
        def __init__(self, output_json):
            self.output_json = output_json

    def fake_run_codex_exec(parameter, **kwargs):
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
