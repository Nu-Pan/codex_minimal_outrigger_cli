"""apply join の結合、後片付け、異常検出を CLI 経由で検証する。

このファイルは 16,000 文字を超えるが、責務境界は apply run を session へ join する
外部挙動の検証に閉じている。worktree/branch cleanup、state 更新、report 生成、
dirty worktree、想定外差分、merge conflict は同じ join 操作の可否を判断する
境界条件であり、分割すると同じ fixture と git 状態の読み取り文脈が分散する。
現状は apply join の成功条件と拒否条件を一箇所で読む方が凝集性が高い。
根拠: <work-root>/oracle/src/oracle/prompt_builder/parts/realization_standard.py
"""

import json
import subprocess
from pathlib import Path

import pytest

from _support import (
    apply_worktree_from_state,
    current_branch,
    make_repo,
    run_git,
    runner,
    run_doctor,
)
from main import app
import sub_commands.apply.fork as apply_fork_module
import sub_commands.apply.join as apply_module

def test_apply_join_removes_apply_worktree_and_resets_state(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert run_doctor(root).exit_code == 0
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
    state_path = root / ".cmoc" / "local" / "session" / f"{session_id}.json"
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
    assert "# cmoc apply join 結果レポート" in report_path.read_text()


def test_apply_join_can_run_from_apply_worktree(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert run_doctor(root).exit_code == 0
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
    state_path = root / ".cmoc" / "local" / "session" / f"{session_id}.json"
    state = json.loads(state_path.read_text())
    apply_branch = state["apply"]["apply_branch"]
    apply_oracle_snapshot_commit = state["apply"]["oracle_snapshot_commit"]
    apply_worktree = apply_worktree_from_state(root, state)
    monkeypatch.chdir(apply_worktree)

    result = runner.invoke(app, ["apply", "join"], catch_exceptions=False)

    assert result.exit_code == 0
    assert Path.cwd() == apply_worktree
    assert apply_worktree.exists()
    assert (
        subprocess.run(
            ["git", "rev-parse", "--verify", apply_branch], cwd=root
        ).returncode
        == 0
    )
    state = json.loads(state_path.read_text())
    assert state["apply"]["state"] == "ready"
    assert (
        state["session"]["last_joined_apply_oracle_snapshot_commit"]
        == apply_oracle_snapshot_commit
    )
    assert "- cleanup_reachable: `True`" in result.output
    assert "apply worktree remains because it is current cwd" in result.output


def test_apply_join_from_linked_session_worktree_merges_into_current_session(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = make_repo(tmp_path)
    root_branch = current_branch(root)
    monkeypatch.chdir(root)
    assert run_doctor(root).exit_code == 0
    linked = root / ".cmoc" / "local" / "worktree" / "linked-session"
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
    state_path = root / ".cmoc" / "local" / "session" / f"{session_id}.json"
    state = json.loads(state_path.read_text())
    apply_worktree = apply_worktree_from_state(root, state)
    joined = apply_worktree / "src" / "joined.py"
    joined.parent.mkdir()
    joined.write_text("value = 'joined from apply'\n")
    run_git(apply_worktree, "add", "src/joined.py")
    run_git(apply_worktree, "commit", "-m", "apply linked session change")
    assert current_branch(root) == root_branch

    result = runner.invoke(app, ["apply", "join"], catch_exceptions=False)

    assert result.exit_code == 0
    assert (
        (linked / "src" / "joined.py").read_text()
        == "value = 'joined from apply'\n"
    )
    assert not (root / "src" / "joined.py").exists()
    assert json.loads(state_path.read_text())["apply"]["state"] == "ready"
    assert run_git(linked, "branch", "--show-current").stdout.strip() == session_branch
    assert current_branch(root) == root_branch


def test_apply_join_rejects_stale_apply_branch_for_same_session(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert run_doctor(root).exit_code == 0
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
    state_path = root / ".cmoc" / "local" / "session" / f"{session_id}.json"
    state = json.loads(state_path.read_text())
    active_apply_branch = state["apply"]["apply_branch"]
    active_apply_worktree = apply_worktree_from_state(root, state)
    stale_apply_branch = f"cmoc/apply/{session_id}/stale"
    stale_apply_worktree = root / ".cmoc" / "local" / "worktree" / session_id / "stale"
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
    assert run_doctor(root).exit_code == 0
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
    state_path = root / ".cmoc" / "local" / "session" / f"{session_id}.json"
    state = json.loads(state_path.read_text())
    apply_branch = state["apply"]["apply_branch"]
    apply_worktree = apply_worktree_from_state(root, state)
    (apply_worktree / "dirty.txt").write_text("dirty\n")
    root_log_count = len(
        list((root / ".cmoc" / "local" / "log" / "sub_command").glob("*.jsonl"))
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
        len(list((root / ".cmoc" / "local" / "log" / "sub_command").glob("*.jsonl")))
        == root_log_count + 1
    )
    assert not (apply_worktree / ".cmoc" / "local" / "log" / "sub_command").exists()
    assert "git 未コミット差分が存在します。" in result.stdout
    assert "git 未コミット差分が存在します。" not in result.stderr


def test_apply_join_from_session_requires_clean_apply_worktree(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert run_doctor(root).exit_code == 0
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
    state_path = root / ".cmoc" / "local" / "session" / f"{session_id}.json"
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
    assert run_doctor(root).exit_code == 0
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
    state_path = root / ".cmoc" / "local" / "session" / f"{session_id}.json"
    state = json.loads(state_path.read_text())
    apply_worktree = apply_worktree_from_state(root, state)
    (apply_worktree / "README.md").write_text("# apply\n")
    (apply_worktree / "oracle" / "spec.md").write_text("# changed oracle in apply\n")
    broken_link = apply_worktree / ".codex" / "broken"
    broken_link.parent.mkdir(exist_ok=True)
    broken_link.symlink_to("missing-target")
    run_git(apply_worktree, "add", "README.md", "oracle/spec.md", ".codex/broken")
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
    assert "## 想定外差分" in report
    assert "- apply: .codex/broken, README.md, oracle/spec.md" in report
    assert "## マージコンフリクト" in report
    assert "- なし" in report
    forced = runner.invoke(
        app, ["apply", "join", "--force-resolve"], catch_exceptions=False
    )
    assert forced.exit_code == 0
    assert (root / "README.md").read_text() == "# repo\n"
    assert (root / "oracle" / "spec.md").read_text() == "# spec\n"
    assert not (root / ".codex" / "broken").exists()
    assert not (root / ".codex" / "broken").is_symlink()


def test_apply_join_reports_codex_apply_diff_and_force_reverts(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = make_repo(tmp_path)
    codex_config = root / ".codex" / "config.toml"
    codex_config.parent.mkdir()
    codex_config.write_text('model = "base"\n')
    run_git(root, "add", ".codex/config.toml")
    run_git(root, "commit", "-m", "add tracked codex config")
    monkeypatch.chdir(root)
    assert run_doctor(root).exit_code == 0
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
        / ".cmoc" / "local" / "session"
        / f"{run_git(root, 'branch', '--show-current').stdout.strip().removeprefix('cmoc/session/')}.json"
    )
    state = json.loads(state_path.read_text())
    apply_worktree = apply_worktree_from_state(root, state)
    (apply_worktree / ".codex" / "config.toml").write_text('model = "apply"\n')
    run_git(apply_worktree, "add", ".codex/config.toml")
    run_git(apply_worktree, "commit", "-m", "unexpected codex config")

    normal = runner.invoke(app, ["apply", "join"], catch_exceptions=False)

    assert normal.exit_code == 1
    assert "想定外差分" in normal.output
    report_line = [
        line for line in normal.output.splitlines() if "保存済み report" in line
    ][0]
    report = Path(report_line.rsplit(": ", 1)[1]).read_text()
    assert "- apply: .codex/config.toml" in report
    forced = runner.invoke(
        app, ["apply", "join", "--force-resolve"], catch_exceptions=False
    )
    assert forced.exit_code == 0
    assert codex_config.read_text() == 'model = "base"\n'


def test_apply_join_reports_session_oracle_agents_diff_and_force_reverts(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert run_doctor(root).exit_code == 0
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
    agents = root / "oracle" / "AGENTS.md"
    agents.write_text("session agents\n")
    run_git(root, "add", "oracle/AGENTS.md")
    run_git(root, "commit", "-m", "session oracle agents")

    normal = runner.invoke(app, ["apply", "join"], catch_exceptions=False)

    assert normal.exit_code == 1
    assert "想定外差分" in normal.output
    report_line = [
        line for line in normal.output.splitlines() if "保存済み report" in line
    ][0]
    report_path = Path(report_line.rsplit(": ", 1)[1])
    report = report_path.read_text()
    assert "- session: oracle/AGENTS.md" in report
    forced = runner.invoke(
        app, ["apply", "join", "--force-resolve"], catch_exceptions=False
    )
    assert forced.exit_code == 0
    assert not agents.exists()
    state_path = root / ".cmoc" / "local" / "session" / f"{session_id}.json"
    assert json.loads(state_path.read_text())["apply"]["state"] == "ready"


@pytest.mark.parametrize("side", ["apply", "session"])
def test_apply_join_force_reverts_unexpected_rename_source(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    side: str,
) -> None:
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert run_doctor(root).exit_code == 0
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
    state_path = root / ".cmoc" / "local" / "session" / f"{session_id}.json"
    state = json.loads(state_path.read_text())
    changed_root = apply_worktree_from_state(root, state) if side == "apply" else root
    (changed_root / "docs").mkdir()
    run_git(changed_root, "mv", "README.md", "docs/README.md")
    run_git(changed_root, "commit", "-m", f"{side} unexpected rename")

    normal = runner.invoke(app, ["apply", "join"], catch_exceptions=False)

    assert normal.exit_code == 1
    report_line = [
        line for line in normal.output.splitlines() if "保存済み report" in line
    ][0]
    assert (
        f"- {side}: docs/README.md"
        in Path(report_line.rsplit(": ", 1)[1]).read_text()
    )
    forced = runner.invoke(
        app, ["apply", "join", "--force-resolve"], catch_exceptions=False
    )
    assert forced.exit_code == 0
    assert (root / "README.md").read_text() == "# repo\n"
    assert not (root / "docs" / "README.md").exists()


def test_apply_join_excludes_deleted_apply_paths_from_unexpected_changes(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert run_doctor(root).exit_code == 0
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
        / ".cmoc" / "local" / "session"
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


@pytest.mark.parametrize("path", ["memo", "memo/note.md"])
def test_apply_join_classifies_root_memo_as_session_change(
    tmp_path: Path,
    path: str,
) -> None:
    root = make_repo(tmp_path)

    assert apply_module.is_expected_apply_change(root, path) is False
    assert apply_module.is_expected_session_change(root, path) is True


def test_apply_join_allows_session_oracle_symlink_to_outside_root(
    tmp_path: Path,
) -> None:
    root = make_repo(tmp_path)
    outside_target = tmp_path / "outside-oracle.md"
    outside_target.write_text("# outside\n")
    with (root / ".gitignore").open("a") as file:
        file.write("oracle/ignored-link.md\n")
    (root / "oracle" / "ignored-link.md").symlink_to(outside_target)
    run_git(root, "add", "-f", ".gitignore", "oracle/ignored-link.md")
    run_git(root, "commit", "-m", "add ignored oracle symlink")

    path = "oracle/ignored-link.md"

    assert apply_module.is_expected_apply_change(root, path) is False
    assert apply_module.is_expected_session_change(root, path) is True


@pytest.mark.parametrize(
    "path",
    [
        "AGENTS.md",
        ".codex/config.toml",
        ".gitignore",
        "README.md",
        "test/test_app.py",
    ],
)
def test_apply_join_rejects_non_realization_apply_paths(
    tmp_path: Path,
    path: str,
) -> None:
    root = make_repo(tmp_path)

    assert apply_module.is_expected_apply_change(root, path) is False


def test_apply_join_allows_tracked_ignored_src_apply_diff(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    root = make_repo(tmp_path)
    ignored_src = root / "src" / "ignored.py"
    ignored_src.parent.mkdir()
    ignored_src.write_text("value = 1\n")
    (root / ".gitignore").write_text("src/ignored.py\n")
    run_git(root, "add", "-f", ".gitignore", "src/ignored.py")
    run_git(root, "commit", "-m", "add tracked ignored src")
    monkeypatch.chdir(root)
    assert run_doctor(root).exit_code == 0
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
        / ".cmoc" / "local" / "session"
        / f"{run_git(root, 'branch', '--show-current').stdout.strip().removeprefix('cmoc/session/')}.json"
    )
    state = json.loads(state_path.read_text())
    apply_worktree = apply_worktree_from_state(root, state)
    (apply_worktree / "src" / "ignored.py").write_text("value = 2\n")
    run_git(apply_worktree, "add", "src/ignored.py")
    run_git(apply_worktree, "commit", "-m", "apply ignored implementation change")

    result = runner.invoke(app, ["apply", "join"], catch_exceptions=False)

    assert result.exit_code == 0
    assert "想定外差分" not in result.output
    assert (root / "src" / "ignored.py").read_text() == "value = 2\n"


def test_apply_join_reports_unresolved_non_index_conflict(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert run_doctor(root).exit_code == 0
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
        / ".cmoc" / "local" / "session"
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
    assert "## マージコンフリクト" in report
    assert "- 未解決: README.md" in report
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
    assert run_doctor(root).exit_code == 0
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
        / ".cmoc" / "local" / "session"
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
