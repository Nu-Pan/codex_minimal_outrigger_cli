"""review oracle の finding path と対象列挙を検証する。

根拠:
- {{work-root}}/oracle/src/oracle/prompt_builder/parts/oracle_and_realization_basic.py
- {{work-root}}/oracle/src/oracle/prompt_builder/parts/realization_standard.py
- {{work-root}}/oracle/doc/app_spec/sub_command/review_oracle.md
- {{work-root}}/oracle/doc/dev_rule/coding_rule.md
- {{work-root}}/oracle/doc/dev_rule/test_rule.md
"""

from pathlib import Path

import pytest
from _cli_support import runner
from _git_support import add_tracked_ignored_oracle_file, make_repo, run_git
from _ollama_support import run_doctor

import sub_commands.review.oracle as review_module
from cmoc_runtime import SessionState
from main import app
from sub_commands.review_paths import finding_oracle_path, oracle_path_key
from sub_commands.review_targets import enumerate_review_all_oracle_files


class _FakeCodexResult:
    """Structured Output payload だけを保持する review oracle fake。"""

    def __init__(self, output_json: dict[str, object]) -> None:
        """Codex fake が返す JSON payload を保存する。"""
        self.output_json = output_json


def _empty_finding_response(parameter: object) -> _FakeCodexResult:
    """enumerate_finding 用の空 Structured Output 応答を返す。"""
    schema_name = parameter.structured_output_schema_path.name
    if schema_name != "enumerate_finding.json":
        raise AssertionError(schema_name)
    return _FakeCodexResult({"findings": []})


def test_finding_oracle_path_rejects_relative_without_placeholder(
    tmp_path: Path,
) -> None:
    """placeholder のない相対 finding path を拒否し、oracle alias を解決する。"""
    assert finding_oracle_path({"oracle_path": "oracle/spec.md"}, tmp_path) is None
    assert (
        finding_oracle_path({"oracle_path": "{{oracle-root}}/spec.md"}, tmp_path)
        == (tmp_path / "oracle" / "spec.md").resolve()
    )


def test_finding_oracle_path_resolves_work_root_from_review_worktree(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """{{work-root}} finding path を review worktree 基準で解決する。"""
    review_parent = tmp_path / "review"
    review_parent.mkdir()
    unrelated = make_repo(tmp_path)
    review_worktree = make_repo(review_parent)
    monkeypatch.chdir(unrelated)

    assert (
        finding_oracle_path(
            {"oracle_path": "{{work-root}}/oracle/spec.md"}, review_worktree
        )
        == (review_worktree / "oracle" / "spec.md").resolve()
    )


def test_finding_oracle_path_preserves_absolute_symlink_entry(
    tmp_path: Path,
) -> None:
    """absolute symlink の finding path を link 先へ追跡しない。"""
    (tmp_path / "oracle").mkdir()
    target = tmp_path / "memo.md"
    target.write_text("# memo\n")
    link = tmp_path / "oracle" / "memo-link.md"
    link.symlink_to("../memo.md")

    assert finding_oracle_path({"oracle_path": str(link)}, tmp_path) == link


def test_oracle_path_key_rejects_external_oracle_suffix(tmp_path: Path) -> None:
    """root 外の任意の `oracle` component を現在の repository と同一視しない。"""
    root = tmp_path / "repo"
    external = tmp_path / "other" / "oracle" / "spec.md"

    assert oracle_path_key(root, external) is None


def test_review_oracle_full_scope_keeps_tracked_ignored_oracle_files(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """full scope が追跡済み oracle file と symlink を対象に含める。"""
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

    def fake_run_codex_exec(parameter: object, **kwargs: object) -> object:
        """呼び出し目的を記録し、対象列挙には空の finding を返す。"""
        calls.append(kwargs["purpose"])
        return _empty_finding_response(parameter)

    monkeypatch.setattr(review_module, "run_codex_exec", fake_run_codex_exec)

    result = runner.invoke(
        app, ["oracle", "review", "--scope", "full"], catch_exceptions=False
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


def test_review_oracle_session_scope_reports_total_and_no_targets(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """session scope に対象がない場合、Codex を呼ばず no_targets を出力する。"""
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert run_doctor(root).exit_code == 0
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )
    calls: list[str] = []

    def fail_run_codex_exec(parameter: object, **kwargs: object) -> None:
        """対象なしのsession scopeからCodexが呼ばれた場合に失敗させる。"""
        calls.append(kwargs["purpose"])
        raise AssertionError(
            "no session-scope oracle targets should skip review Codex calls"
        )

    monkeypatch.setattr(review_module, "run_codex_exec", fail_run_codex_exec)

    result = runner.invoke(app, ["oracle", "review"], catch_exceptions=False)

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


def test_review_oracle_session_scope_keeps_changed_tracked_ignored_oracle_files(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """session scope が review fork 時点で変更された追跡済み oracle file を保つ。"""
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

    def fake_run_codex_exec(parameter: object, **kwargs: object) -> object:
        """呼び出し目的を記録し、対象列挙には空の finding を返す。"""
        calls.append(kwargs["purpose"])
        return _empty_finding_response(parameter)

    monkeypatch.setattr(review_module, "run_codex_exec", fake_run_codex_exec)

    result = runner.invoke(app, ["oracle", "review"], catch_exceptions=False)

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
