"""oracle review の worktree と INDEX 統合を検証する。

仕様根拠: {{work-root}}/oracle/doc/app_spec/sub_command/oracle_review.md、
{{work-root}}/oracle/doc/app_spec/run_isolation.md、
{{work-root}}/oracle/doc/branch_model.md、
{{work-root}}/oracle/doc/app_spec/indexing.md。
"""

import subprocess
from pathlib import Path

import pytest
from _cli_support import run_doctor, runner
from _git_support import make_repo, run_git

import commons.indexing as indexing_module
import commons.runtime_codex_preflight as codex_preflight_module
import sub_commands.oracle.review as review_module
from basic.acp import AgentCallParameter
from main import app


class _FakeCodexResult:
    """oracle review が読む構造化出力だけを保持する fake。

    根拠: {{work-root}}/oracle/doc/app_spec/sub_command/oracle_review.md
    """

    def __init__(self, output_json: dict[str, object]) -> None:
        """Codex CLI を起動せず、テスト用の構造化出力を保持する。"""
        self.output_json = output_json


def _schema_name(parameter: AgentCallParameter) -> str:
    """fake callback が検証する Structured Output schema 名を返す。

    根拠: {{work-root}}/oracle/doc/app_spec/sub_command/oracle_review.md。
    """
    schema_path = parameter.structured_output_schema_path
    if schema_path is None:
        raise AssertionError("oracle review requires a Structured Output schema")
    return schema_path.name


def test_oracle_review_uses_linked_worktree_branch_and_oracle(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """linked worktree の session branch と oracle を review 対象にする。

    根拠: {{work-root}}/oracle/doc/app_spec/run_isolation.md、
    {{work-root}}/oracle/doc/branch_model.md。
    """

    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert run_doctor(root).exit_code == 0
    linked = root / ".cmoc" / "gu" / "worktree" / "linked-review"
    run_git(root, "worktree", "add", "-b", "linked-review-home", str(linked), "HEAD")
    (linked / "oracle" / "linked.md").write_text("# linked oracle\n")
    run_git(linked, "add", "oracle/linked.md")
    run_git(linked, "commit", "-m", "linked oracle change")
    monkeypatch.chdir(linked)
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )
    session_head = run_git(linked, "rev-parse", "HEAD").stdout.strip()
    calls: list[str] = []
    review_worktrees: list[Path] = []

    def fake_run_codex_exec(
        parameter: AgentCallParameter, **kwargs: object
    ) -> _FakeCodexResult:
        """finding 列挙の応答と review worktree を記録する。

        根拠: {{work-root}}/oracle/doc/app_spec/sub_command/oracle_review.md。
        """

        review_worktrees.append(Path.cwd())
        calls.append(str(kwargs["purpose"]))
        schema_name = _schema_name(parameter)
        if schema_name == "enumerate_finding.json":
            return _FakeCodexResult({"findings": []})
        raise AssertionError(schema_name)

    monkeypatch.setattr(review_module, "run_codex_exec", fake_run_codex_exec)

    result = runner.invoke(
        app, ["oracle", "review", "--scope", "full"], catch_exceptions=False
    )

    assert result.exit_code == 0
    report_path = Path(
        [line for line in result.output.splitlines() if line.startswith("/")][-1]
    )
    assert report_path.is_relative_to(root / ".cmoc" / "gu" / "ar" / "report")
    assert not report_path.is_relative_to(linked)
    rendered = report_path.read_text()
    assert f"review_fork_commit: {session_head}" in rendered
    assert "`oracle/linked.md`" in rendered
    branch = run_git(linked, "branch", "--show-current").stdout.strip()
    assert branch.startswith("cmoc/session/")
    session_id = branch.removeprefix("cmoc/session/")
    assert review_worktrees
    for review_worktree in review_worktrees:
        assert review_worktree.parent == root / ".cmoc" / "gu" / "worktree" / session_id
        assert not review_worktree.is_relative_to(linked)
    assert any("linked.md" in call for call in calls)


def test_oracle_review_forks_from_snapshot_commit(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """session branch が進んでも review run は取得済み snapshot から fork する。

    根拠: {{work-root}}/oracle/doc/app_spec/run_isolation.md。
    """

    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert run_doctor(root).exit_code == 0
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )
    snapshot_commit = run_git(root, "rev-parse", "HEAD").stdout.strip()
    original_create_run_worktree = review_module.create_run_worktree
    start_points: list[str] = []
    forked_commits: list[str] = []

    def advance_session_before_run_creation(
        root_arg: Path, branch: str, worktree: Path, start_point: str
    ) -> Path:
        """run worktree 作成直前に session branch を進めて fork point を検証する。"""
        (root / "README.md").write_text("# session advanced\n")
        run_git(root, "add", "README.md")
        run_git(root, "commit", "-m", "advance session before review run")
        start_points.append(start_point)
        created = original_create_run_worktree(root_arg, branch, worktree, start_point)
        forked_commits.append(run_git(worktree, "rev-parse", "HEAD").stdout.strip())
        return created

    monkeypatch.setattr(
        review_module,
        "create_run_worktree",
        advance_session_before_run_creation,
    )

    def fake_run_codex_exec(
        parameter: AgentCallParameter, **kwargs: object
    ) -> _FakeCodexResult:
        """review の構造化出力を空にして、fork point の検証だけを行う。"""
        assert _schema_name(parameter) == "enumerate_finding.json"
        return _FakeCodexResult({"findings": []})

    monkeypatch.setattr(review_module, "run_codex_exec", fake_run_codex_exec)

    result = runner.invoke(
        app, ["oracle", "review", "--scope", "full"], catch_exceptions=False
    )

    assert result.exit_code == 0, result.output
    assert start_points == [snapshot_commit]
    assert forked_commits == [snapshot_commit]


@pytest.mark.parametrize(
    ("relative_path", "content"),
    [
        ("oracle/uncommitted.md", "# uncommitted\n"),
        ("README.md", "dirty\n"),
    ],
)
def test_oracle_review_rejects_uncommitted_worktree_changes(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    relative_path: str,
    content: str,
) -> None:
    """session fork 後に未コミット差分がある worktree を拒否する。

    根拠: {{work-root}}/oracle/doc/app_spec/sub_command/oracle_review.md。
    """

    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert run_doctor(root).exit_code == 0
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )
    (root / relative_path).write_text(content)

    result = runner.invoke(app, ["oracle", "review"])

    assert result.exit_code != 0
    assert "git 未コミット差分" in result.output
    assert relative_path in result.output


def test_oracle_review_merges_review_index_changes(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """review worktree で生成された INDEX.md だけを session に統合する。

    根拠: {{work-root}}/oracle/doc/app_spec/sub_command/oracle_review.md、
    {{work-root}}/oracle/doc/app_spec/indexing.md。
    """

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

    def fake_run_codex_exec(
        parameter: AgentCallParameter, **kwargs: object
    ) -> _FakeCodexResult:
        """finding 検証を空結果にし、review worktree の INDEX を更新する。

        根拠: {{work-root}}/oracle/doc/app_spec/sub_command/oracle_review.md、
        {{work-root}}/oracle/doc/app_spec/indexing.md。
        """

        review_worktrees.append(Path.cwd())
        schema_name = _schema_name(parameter)
        if schema_name == "enumerate_finding.json":
            (Path.cwd() / "INDEX.md").write_text("# generated review index\n")
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
    assert (root / "INDEX.md").read_text() == "# generated review index\n"
    rendered = Path(
        [line for line in result.output.splitlines() if line.startswith("/")][-1]
    ).read_text()
    assert "review_join_commit: null" not in rendered
    assert review_worktrees
    for review_worktree in review_worktrees:
        assert review_worktree.parent == root / ".cmoc" / "gu" / "worktree" / session_id
    assert not any(
        path.name == ".git"
        for path in (root / ".cmoc" / "gu" / "worktree").rglob(".git")
    )
    assert all(not path.exists() for path in review_worktrees)


def test_oracle_review_merges_preflight_committed_index_changes(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """preflight が review worktree にコミットした INDEX.md を統合する。

    根拠: {{work-root}}/oracle/doc/app_spec/run_isolation.md、
    {{work-root}}/oracle/doc/app_spec/indexing.md。
    """

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
        """preflight の INDEX 更新先を記録し、生成結果を返す。

        根拠: {{work-root}}/oracle/doc/app_spec/indexing.md。
        """

        review_worktrees.append(update_root)
        index_path = update_root / "INDEX.md"
        index_path.write_text("# preflight review index\n")
        return [index_path]

    def fake_runtime_run_codex_exec(
        parameter: AgentCallParameter, **kwargs: object
    ) -> _FakeCodexResult:
        """preflight 中の finding 列挙を空結果に置き換える。

        根拠: {{work-root}}/oracle/doc/app_spec/sub_command/oracle_review.md。
        """

        schema_name = _schema_name(parameter)
        if schema_name == "enumerate_finding.json":
            return _FakeCodexResult({"findings": []})
        raise AssertionError(schema_name)

    monkeypatch.setattr(indexing_module, "update_indexes", fake_update_indexes)
    monkeypatch.setattr(
        codex_preflight_module, "runtime_run_codex_exec", fake_runtime_run_codex_exec
    )

    result = runner.invoke(
        app, ["oracle", "review", "--scope", "full"], catch_exceptions=False
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


def test_oracle_review_resolves_index_conflict_when_session_deleted_index(
    tmp_path: Path,
) -> None:
    """session 側で削除された INDEX.md の merge conflict を解決する。

    根拠: {{work-root}}/oracle/doc/app_spec/sub_command/oracle_review.md。
    """

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
    assert run_git(root, "diff", "--name-only", "--diff-filter=U").stdout.strip() == ""
    assert "Merge branch 'review'" in run_git(root, "log", "-1", "--pretty=%B").stdout


def test_commit_review_index_changes_accepts_nested_untracked_index(
    tmp_path: Path,
) -> None:
    """未追跡 directory 配下でも INDEX.md だけなら commit する。

    根拠: {{work-root}}/oracle/doc/app_spec/sub_command/oracle_review.md、
    {{work-root}}/oracle/doc/app_spec/indexing.md。
    """

    root = make_repo(tmp_path)
    generated_index = root / "generated" / "INDEX.md"
    generated_index.parent.mkdir()
    generated_index.write_text("# generated\n")

    assert review_module.commit_review_index_changes(root) is True
    assert (
        run_git(root, "show", "--format=", "--name-only", "HEAD").stdout.strip()
        == "generated/INDEX.md"
    )


@pytest.mark.parametrize("change_kind", ["unstaged", "staged", "untracked"])
def test_oracle_review_rejects_non_index_worktree_changes(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    change_kind: str,
) -> None:
    """review worktree が INDEX.md 以外を変更した場合に失敗させる。

    根拠: {{work-root}}/oracle/doc/app_spec/sub_command/oracle_review.md、
    {{work-root}}/oracle/doc/app_spec/indexing.md。
    """

    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert run_doctor(root).exit_code == 0
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )

    def fake_run_codex_exec(
        parameter: AgentCallParameter, **kwargs: object
    ) -> _FakeCodexResult:
        """finding 列挙時に指定された種類の不正な差分を作る。

        根拠: {{work-root}}/oracle/doc/app_spec/sub_command/oracle_review.md。
        """

        schema_name = _schema_name(parameter)
        if schema_name == "enumerate_finding.json":
            if change_kind == "untracked":
                (Path.cwd() / "generated.txt").write_text("unexpected\n")
            else:
                (Path.cwd() / "README.md").write_text("unexpected\n")
                if change_kind == "staged":
                    run_git(Path.cwd(), "add", "README.md")
            return _FakeCodexResult({"findings": []})
        raise AssertionError(schema_name)

    monkeypatch.setattr(review_module, "run_codex_exec", fake_run_codex_exec)

    result = runner.invoke(app, ["oracle", "review", "--scope", "full"])

    assert result.exit_code != 0
    assert "oracle review が INDEX.md 以外の差分を作成しました。" in result.output
    assert (root / "README.md").read_text() == "# repo\n"
    assert not (root / "generated.txt").exists()
