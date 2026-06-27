"""apply join の結合、後片付け、異常検出を CLI 経由で検証する。

このファイルは 16,000 文字を超えるが、責務境界は apply run を session へ join する
外部挙動の検証に閉じている。worktree/branch cleanup、state 更新、report 生成、
dirty worktree、想定外差分、merge conflict は同じ join 操作の可否を判断する
境界条件であり、分割すると同じ fixture と git 状態の読み取り文脈が分散する。
現状は apply join の成功条件と拒否条件を一箇所で読む方が凝集性が高い。
"""

import json
import subprocess
from pathlib import Path

import pytest

from _support import (
    apply_worktree_from_state,
    make_repo,
    run_git,
    runner,
)
from main import app
import sub_commands.apply.fork as apply_fork_module
import sub_commands.apply.join as apply_module

def test_apply_join_removes_apply_worktree_and_resets_state(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert runner.invoke(app, ["init"], catch_exceptions=False).exit_code == 0
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )

    class FakeCodexResult:
        output_json = {"findings": []}

    monkeypatch.setattr(
        apply_fork_module,
        "run_codex_exec",
        lambda parameter, **kwargs: FakeCodexResult(),
    )
    assert runner.invoke(app, ["apply", "fork"], catch_exceptions=False).exit_code == 0
    session_branch = run_git(root, "branch", "--show-current").stdout.strip()
    session_id = session_branch.removeprefix("cmoc/session/")
    state_path = root / ".cmoc" / "sessions" / f"{session_id}.json"
    state = json.loads(state_path.read_text())
    apply_branch = state["apply"]["apply_branch"]
    apply_oracle_snapshot_commit = state["apply"]["oracle_snapshot_commit"]
    apply_worktree = apply_worktree_from_state(root, state)

    result = runner.invoke(app, ["apply", "join"], catch_exceptions=False)

    assert result.exit_code == 0
    assert not apply_worktree.exists()
    assert (
        subprocess.run(
            ["git", "rev-parse", "--verify", apply_branch], cwd=root
        ).returncode
        != 0
    )
    state = json.loads(state_path.read_text())
    assert state["apply"]["state"] == "ready"
    assert (
        state["session"]["last_joined_apply_oracle_snapshot_commit"]
        == apply_oracle_snapshot_commit
    )
    report_line = [
        line for line in result.output.splitlines() if line.startswith("- report:")
    ][-1]
    report_path = Path(report_line.split("`")[1])
    assert report_path.is_file()
    assert "# cmoc apply join report" in report_path.read_text()


def test_apply_join_can_run_from_apply_worktree(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert runner.invoke(app, ["init"], catch_exceptions=False).exit_code == 0
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )

    class FakeCodexResult:
        output_json = {"findings": []}

    monkeypatch.setattr(
        apply_fork_module,
        "run_codex_exec",
        lambda parameter, **kwargs: FakeCodexResult(),
    )
    assert runner.invoke(app, ["apply", "fork"], catch_exceptions=False).exit_code == 0
    session_branch = run_git(root, "branch", "--show-current").stdout.strip()
    session_id = session_branch.removeprefix("cmoc/session/")
    state_path = root / ".cmoc" / "sessions" / f"{session_id}.json"
    state = json.loads(state_path.read_text())
    apply_branch = state["apply"]["apply_branch"]
    apply_oracle_snapshot_commit = state["apply"]["oracle_snapshot_commit"]
    apply_worktree = apply_worktree_from_state(root, state)
    monkeypatch.chdir(apply_worktree)

    result = runner.invoke(app, ["apply", "join"], catch_exceptions=False)

    assert result.exit_code == 0
    assert Path.cwd() == root
    assert not apply_worktree.exists()
    assert (
        subprocess.run(
            ["git", "rev-parse", "--verify", apply_branch], cwd=root
        ).returncode
        != 0
    )
    state = json.loads(state_path.read_text())
    assert state["apply"]["state"] == "ready"
    assert (
        state["session"]["last_joined_apply_oracle_snapshot_commit"]
        == apply_oracle_snapshot_commit
    )
    assert "- cleanup_reachable: `True`" in result.output
    assert "  - none" in result.output


def test_apply_join_from_linked_session_worktree_merges_into_current_session(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert runner.invoke(app, ["init"], catch_exceptions=False).exit_code == 0
    linked = root / ".cmoc" / "worktrees" / "linked-session"
    run_git(root, "worktree", "add", "-b", "linked-session-home", str(linked), "HEAD")
    monkeypatch.chdir(linked)
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )

    class FakeCodexResult:
        output_json = {"findings": []}

    monkeypatch.setattr(
        apply_fork_module,
        "run_codex_exec",
        lambda parameter, **kwargs: FakeCodexResult(),
    )
    assert runner.invoke(app, ["apply", "fork"], catch_exceptions=False).exit_code == 0
    session_branch = run_git(linked, "branch", "--show-current").stdout.strip()
    session_id = session_branch.removeprefix("cmoc/session/")
    state_path = root / ".cmoc" / "sessions" / f"{session_id}.json"
    state = json.loads(state_path.read_text())
    apply_worktree = apply_worktree_from_state(root, state)
    (apply_worktree / "JOINED.md").write_text("joined from apply\n")
    run_git(apply_worktree, "add", "JOINED.md")
    run_git(apply_worktree, "commit", "-m", "apply linked session change")
    assert run_git(root, "branch", "--show-current").stdout.strip() == "master"

    result = runner.invoke(app, ["apply", "join"], catch_exceptions=False)

    assert result.exit_code == 0
    assert (linked / "JOINED.md").read_text() == "joined from apply\n"
    assert not (root / "JOINED.md").exists()
    assert json.loads(state_path.read_text())["apply"]["state"] == "ready"
    assert run_git(linked, "branch", "--show-current").stdout.strip() == session_branch
    assert run_git(root, "branch", "--show-current").stdout.strip() == "master"


def test_apply_join_rejects_stale_apply_branch_for_same_session(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert runner.invoke(app, ["init"], catch_exceptions=False).exit_code == 0
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )

    class FakeCodexResult:
        output_json = {"findings": []}

    monkeypatch.setattr(
        apply_fork_module,
        "run_codex_exec",
        lambda parameter, **kwargs: FakeCodexResult(),
    )
    assert runner.invoke(app, ["apply", "fork"], catch_exceptions=False).exit_code == 0
    session_branch = run_git(root, "branch", "--show-current").stdout.strip()
    session_id = session_branch.removeprefix("cmoc/session/")
    state_path = root / ".cmoc" / "sessions" / f"{session_id}.json"
    state = json.loads(state_path.read_text())
    active_apply_branch = state["apply"]["apply_branch"]
    active_apply_worktree = apply_worktree_from_state(root, state)
    stale_apply_branch = f"cmoc/apply/{session_id}/stale"
    stale_apply_worktree = root / ".cmoc" / "worktrees" / session_id / "stale"
    run_git(
        root,
        "worktree",
        "add",
        "-b",
        stale_apply_branch,
        str(stale_apply_worktree),
        session_branch,
    )
    monkeypatch.chdir(stale_apply_worktree)

    result = runner.invoke(app, ["apply", "join"], catch_exceptions=False)

    assert result.exit_code == 1
    assert "現在の apply branch は join 対象" in result.output
    assert f"current_branch: {stale_apply_branch}" in result.output
    assert f"apply_branch: {active_apply_branch}" in result.output
    assert active_apply_worktree.exists()
    assert (
        subprocess.run(
            ["git", "rev-parse", "--verify", active_apply_branch], cwd=root
        ).returncode
        == 0
    )
    assert json.loads(state_path.read_text())["apply"]["state"] == "completed"


def test_apply_join_from_apply_worktree_requires_clean_apply_worktree(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert runner.invoke(app, ["init"], catch_exceptions=False).exit_code == 0
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )

    class FakeCodexResult:
        output_json = {"findings": []}

    monkeypatch.setattr(
        apply_fork_module,
        "run_codex_exec",
        lambda parameter, **kwargs: FakeCodexResult(),
    )
    assert runner.invoke(app, ["apply", "fork"], catch_exceptions=False).exit_code == 0
    session_branch = run_git(root, "branch", "--show-current").stdout.strip()
    session_id = session_branch.removeprefix("cmoc/session/")
    state_path = root / ".cmoc" / "sessions" / f"{session_id}.json"
    state = json.loads(state_path.read_text())
    apply_branch = state["apply"]["apply_branch"]
    apply_worktree = apply_worktree_from_state(root, state)
    (apply_worktree / "dirty.txt").write_text("dirty\n")
    root_log_count = len(
        list((root / ".cmoc" / "log" / "sub_command").glob("*.jsonl"))
    )
    monkeypatch.chdir(apply_worktree)

    result = runner.invoke(app, ["apply", "join"])

    assert result.exit_code != 0
    assert apply_worktree.exists()
    assert (
        subprocess.run(
            ["git", "rev-parse", "--verify", apply_branch], cwd=root
        ).returncode
        == 0
    )
    state = json.loads(state_path.read_text())
    assert state["apply"]["state"] == "completed"
    assert (
        len(list((root / ".cmoc" / "log" / "sub_command").glob("*.jsonl")))
        == root_log_count + 1
    )
    assert not (apply_worktree / ".cmoc" / "log" / "sub_command").exists()
    assert "git 未コミット差分が存在します。" in result.stdout
    assert "git 未コミット差分が存在します。" not in result.stderr


def test_apply_join_from_session_requires_clean_apply_worktree(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert runner.invoke(app, ["init"], catch_exceptions=False).exit_code == 0
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )

    class FakeCodexResult:
        output_json = {"findings": []}

    monkeypatch.setattr(
        apply_fork_module,
        "run_codex_exec",
        lambda parameter, **kwargs: FakeCodexResult(),
    )
    assert runner.invoke(app, ["apply", "fork"], catch_exceptions=False).exit_code == 0
    session_branch = run_git(root, "branch", "--show-current").stdout.strip()
    session_id = session_branch.removeprefix("cmoc/session/")
    state_path = root / ".cmoc" / "sessions" / f"{session_id}.json"
    state = json.loads(state_path.read_text())
    apply_branch = state["apply"]["apply_branch"]
    apply_worktree = apply_worktree_from_state(root, state)
    (apply_worktree / "dirty.txt").write_text("dirty\n")

    result = runner.invoke(app, ["apply", "join"])

    assert result.exit_code != 0
    assert apply_worktree.exists()
    assert (
        subprocess.run(
            ["git", "rev-parse", "--verify", apply_branch], cwd=root
        ).returncode
        == 0
    )
    assert json.loads(state_path.read_text())["apply"]["state"] == "completed"
    assert "git 未コミット差分が存在します。" in result.stdout
    assert "git 未コミット差分が存在します。" not in result.stderr


def test_apply_join_reports_unexpected_apply_diff_and_force_reverts(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert runner.invoke(app, ["init"], catch_exceptions=False).exit_code == 0
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )

    class FakeCodexResult:
        output_json = {"findings": []}

    monkeypatch.setattr(
        apply_fork_module,
        "run_codex_exec",
        lambda parameter, **kwargs: FakeCodexResult(),
    )
    assert runner.invoke(app, ["apply", "fork"], catch_exceptions=False).exit_code == 0
    session_branch = run_git(root, "branch", "--show-current").stdout.strip()
    session_id = session_branch.removeprefix("cmoc/session/")
    state_path = root / ".cmoc" / "sessions" / f"{session_id}.json"
    state = json.loads(state_path.read_text())
    apply_worktree = apply_worktree_from_state(root, state)
    (apply_worktree / "oracle" / "spec.md").write_text("# changed oracle in apply\n")
    run_git(apply_worktree, "add", "oracle/spec.md")
    run_git(apply_worktree, "commit", "-m", "unexpected oracle change")

    normal = runner.invoke(app, ["apply", "join"], catch_exceptions=False)

    assert normal.exit_code == 1
    assert "想定外差分" in normal.output
    report_line = [
        line for line in normal.output.splitlines() if "保存済み report" in line
    ][0]
    report_path = Path(report_line.rsplit(": ", 1)[1])
    report = report_path.read_text()
    assert "join を中止しました" in report
    assert "## Unexpected Changes" in report
    assert "- apply: oracle/spec.md" in report
    assert "## Merge Conflicts" in report
    assert "- none" in report
    forced = runner.invoke(
        app, ["apply", "join", "--force-resolve"], catch_exceptions=False
    )
    assert forced.exit_code == 0
    assert (root / "oracle" / "spec.md").read_text() == "# spec\n"


def test_apply_join_excludes_deleted_apply_paths_from_unexpected_changes(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert runner.invoke(app, ["init"], catch_exceptions=False).exit_code == 0
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )

    class FakeCodexResult:
        output_json = {"findings": []}

    monkeypatch.setattr(
        apply_fork_module,
        "run_codex_exec",
        lambda parameter, **kwargs: FakeCodexResult(),
    )
    assert runner.invoke(app, ["apply", "fork"], catch_exceptions=False).exit_code == 0
    state_path = (
        root
        / ".cmoc"
        / "sessions"
        / f"{run_git(root, 'branch', '--show-current').stdout.strip().removeprefix('cmoc/session/')}.json"
    )
    state = json.loads(state_path.read_text())
    apply_worktree = apply_worktree_from_state(root, state)
    run_git(apply_worktree, "rm", "oracle/spec.md")
    run_git(apply_worktree, "commit", "-m", "delete oracle spec")

    result = runner.invoke(app, ["apply", "join"], catch_exceptions=False)

    assert result.exit_code == 0
    assert "想定外差分" not in result.output
    assert not (root / "oracle" / "spec.md").exists()


def test_apply_join_managed_branch_paths_exclude_deletes_and_use_rename_target(
    tmp_path: Path,
) -> None:
    root = make_repo(tmp_path)
    base = run_git(root, "rev-parse", "HEAD").stdout.strip()
    run_git(root, "checkout", "-b", "changed")
    (root / "docs").mkdir()
    run_git(root, "mv", "README.md", "docs/README.md")
    run_git(root, "rm", "oracle/spec.md")
    run_git(root, "commit", "-m", "rename and delete")

    paths = apply_module.changed_paths_on_managed_branch(root, base, "HEAD")

    assert paths == ["docs/README.md"]


def test_apply_join_allows_gitignore_change_as_apply_diff(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert runner.invoke(app, ["init"], catch_exceptions=False).exit_code == 0
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )

    class FakeCodexResult:
        output_json = {"findings": []}

    monkeypatch.setattr(
        apply_fork_module,
        "run_codex_exec",
        lambda parameter, **kwargs: FakeCodexResult(),
    )
    assert runner.invoke(app, ["apply", "fork"], catch_exceptions=False).exit_code == 0
    state_path = (
        root
        / ".cmoc"
        / "sessions"
        / f"{run_git(root, 'branch', '--show-current').stdout.strip().removeprefix('cmoc/session/')}.json"
    )
    state = json.loads(state_path.read_text())
    apply_worktree = apply_worktree_from_state(root, state)
    changed_gitignore = (apply_worktree / ".gitignore").read_text() + "# expected\n"
    (apply_worktree / ".gitignore").write_text(changed_gitignore)
    run_git(apply_worktree, "add", ".gitignore")
    run_git(apply_worktree, "commit", "-m", "apply gitignore change")

    result = runner.invoke(app, ["apply", "join"], catch_exceptions=False)

    assert result.exit_code == 0
    assert "想定外差分" not in result.output
    assert (root / ".gitignore").read_text() == changed_gitignore


def test_apply_join_reports_unresolved_non_index_conflict(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert runner.invoke(app, ["init"], catch_exceptions=False).exit_code == 0
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )

    class FakeCodexResult:
        output_json = {"findings": []}

    monkeypatch.setattr(
        apply_fork_module,
        "run_codex_exec",
        lambda parameter, **kwargs: FakeCodexResult(),
    )
    assert runner.invoke(app, ["apply", "fork"], catch_exceptions=False).exit_code == 0
    state_path = (
        root
        / ".cmoc"
        / "sessions"
        / f"{run_git(root, 'branch', '--show-current').stdout.strip().removeprefix('cmoc/session/')}.json"
    )
    state = json.loads(state_path.read_text())
    apply_worktree = apply_worktree_from_state(root, state)
    (apply_worktree / "README.md").write_text("# apply\n")
    run_git(apply_worktree, "add", "README.md")
    run_git(apply_worktree, "commit", "-m", "apply readme")
    (root / "README.md").write_text("# session\n")
    run_git(root, "add", "README.md")
    run_git(root, "commit", "-m", "session readme")
    monkeypatch.setattr(
        apply_module, "collect_apply_join_unexpected_changes", lambda *args: {}
    )

    result = runner.invoke(app, ["apply", "join"], catch_exceptions=False)

    assert result.exit_code == 1
    assert "merge conflict が残っています" in result.output
    assert "README.md" in result.output
    report_line = [
        line for line in result.output.splitlines() if "保存済み report" in line
    ][0]
    report_path = Path(report_line.rsplit(": ", 1)[1])
    report = report_path.read_text()
    assert "## Merge Conflicts" in report
    assert "- unresolved: README.md" in report
    assert json.loads(state_path.read_text())["apply"]["state"] == "completed"
    assert apply_worktree.exists()


def test_apply_join_continues_after_resolving_index_conflict_in_normal_mode(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    (root / "INDEX.md").write_text("base\n")
    run_git(root, "add", "INDEX.md")
    run_git(root, "commit", "-m", "add index")
    assert runner.invoke(app, ["init"], catch_exceptions=False).exit_code == 0
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )

    class FakeCodexResult:
        output_json = {"findings": []}

    monkeypatch.setattr(
        apply_fork_module,
        "run_codex_exec",
        lambda parameter, **kwargs: FakeCodexResult(),
    )
    assert runner.invoke(app, ["apply", "fork"], catch_exceptions=False).exit_code == 0
    session_branch = run_git(root, "branch", "--show-current").stdout.strip()
    state_path = (
        root
        / ".cmoc"
        / "sessions"
        / f"{session_branch.removeprefix('cmoc/session/')}.json"
    )
    state = json.loads(state_path.read_text())
    apply_branch = state["apply"]["apply_branch"]
    apply_oracle_snapshot_commit = state["apply"]["oracle_snapshot_commit"]
    apply_worktree = apply_worktree_from_state(root, state)
    (apply_worktree / "INDEX.md").write_text("apply\n")
    run_git(apply_worktree, "add", "INDEX.md")
    run_git(apply_worktree, "commit", "-m", "apply index")
    (root / "INDEX.md").write_text("session\n")
    run_git(root, "add", "INDEX.md")
    run_git(root, "commit", "-m", "session index")

    result = runner.invoke(app, ["apply", "join"], catch_exceptions=False)

    assert result.exit_code == 0
    assert not (root / "INDEX.md").exists()
    assert "merge に失敗しました" not in result.output
    state = json.loads(state_path.read_text())
    assert state["apply"]["state"] == "ready"
    assert (
        state["session"]["last_joined_apply_oracle_snapshot_commit"]
        == apply_oracle_snapshot_commit
    )
    assert not apply_worktree.exists()
    assert (
        subprocess.run(
            ["git", "rev-parse", "--verify", apply_branch], cwd=root
        ).returncode
        != 0
    )
