"""review oracle の worktree と INDEX 統合を検証する。"""

import subprocess
from pathlib import Path

import pytest

import commons.indexing as indexing_module
import commons.runtime_codex_preflight as codex_preflight_module
from _cli_support import runner
from _git_support import make_repo, run_git
from _ollama_support import run_doctor
from main import app
import sub_commands.review.oracle as review_module

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

