import json
import subprocess
from pathlib import Path

import cmoc_runtime
from basic.acp import FileAccessMode
from cmoc_runtime import CmocError
import pytest

from _support import (
    current_branch,
    make_repo,
    run_git,
    runner,
)
from main import app
import sub_commands.session.abandon as session_module
import sub_commands.session.fork as session_fork_module
import sub_commands.session.join as session_join_module


def session_state_path(root: Path, session_branch: str) -> Path:
    session_id = session_branch.removeprefix("cmoc/session/")
    return root / ".cmoc" / "sessions" / f"{session_id}.json"


def session_home_branch(root: Path, session_branch: str) -> str:
    state = json.loads(session_state_path(root, session_branch).read_text())
    return state["session"]["session_home_branch"]


def write_abandoned_state(root: Path, session_id: str) -> Path:
    path = root / ".cmoc" / "sessions" / f"{session_id}.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(
            {"session": {"state": "abandoned", "session_home_branch": "old-home"}},
            ensure_ascii=False,
            indent=2,
        )
        + "\n"
    )
    return path


def test_session_fork_creates_session_branch_and_state(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    home_branch = current_branch(root)
    init_result = runner.invoke(app, ["init"], catch_exceptions=False)
    assert init_result.exit_code == 0

    result = runner.invoke(app, ["session", "fork"], catch_exceptions=False)

    assert result.exit_code == 0
    branch = current_branch(root)
    assert branch.startswith("cmoc/session/")
    state = json.loads(session_state_path(root, branch).read_text())
    assert state["session"]["state"] == "active"
    assert state["session"]["session_home_branch"] == home_branch
    assert state["session"]["last_joined_apply_oracle_snapshot_commit"] is None
    assert state["apply"]["state"] == "ready"


def test_session_fork_does_not_overwrite_existing_state_on_session_id_collision(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    session_id = "2026-06-27_01-02_03_000000000"
    path = write_abandoned_state(root, session_id)
    original = path.read_text()
    home_branch = current_branch(root)
    monkeypatch.setattr(session_fork_module, "timestamp", lambda: session_id)
    monkeypatch.setattr(session_fork_module, "MAX_SESSION_ID_ATTEMPTS", 2)

    result = runner.invoke(app, ["session", "fork"])

    assert result.exit_code != 0
    assert "一意な session-id を生成できませんでした。" in result.stdout
    assert path.read_text() == original
    assert current_branch(root) == home_branch
    assert (
        subprocess.run(
            ["git", "rev-parse", "--verify", f"cmoc/session/{session_id}"],
            cwd=root,
        ).returncode
        != 0
    )


def test_session_fork_retries_session_id_collision(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    collision_id = "2026-06-27_01-02_03_000000000"
    next_id = "2026-06-27_01-02_03_000000001"
    old_path = write_abandoned_state(root, collision_id)
    original = old_path.read_text()
    ids = iter([collision_id, next_id])
    monkeypatch.setattr(session_fork_module, "timestamp", lambda: next(ids))

    result = runner.invoke(app, ["session", "fork"], catch_exceptions=False)

    assert result.exit_code == 0
    assert current_branch(root) == f"cmoc/session/{next_id}"
    assert old_path.read_text() == original
    assert (root / ".cmoc" / "sessions" / f"{next_id}.json").is_file()
    assert f"- session_branch: `cmoc/session/{next_id}`" in result.output


def test_session_fork_initializes_cmoc_ignore_before_logging(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    home_branch = current_branch(root)

    result = runner.invoke(app, ["session", "fork"], catch_exceptions=False)

    assert result.exit_code == 0
    branch = current_branch(root)
    assert branch.startswith("cmoc/session/")
    assert session_home_branch(root, branch) == home_branch
    assert not (root / ".gitignore").exists()
    assert (
        subprocess.run(
            ["git", "check-ignore", "-q", ".cmoc/.__cmoc_ignore_probe__"],
            cwd=root,
        ).returncode
        == 0
    )
    assert len(list((root / ".cmoc" / "log" / "sub_command").glob("*.jsonl"))) == 1
    assert run_git(root, "status", "--short").stdout.strip() == ""


def test_session_fork_uses_linked_worktree_branch_and_head(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert runner.invoke(app, ["init"], catch_exceptions=False).exit_code == 0
    root_branch = current_branch(root)
    linked = root / ".cmoc" / "worktrees" / "linked"
    run_git(root, "worktree", "add", "-b", "linked-home", str(linked), "HEAD")
    (linked / "README.md").write_text("# linked\n")
    run_git(linked, "add", "README.md")
    run_git(linked, "commit", "-m", "linked change")
    linked_commit = run_git(linked, "rev-parse", "HEAD").stdout.strip()
    monkeypatch.chdir(linked)

    result = runner.invoke(app, ["session", "fork"], catch_exceptions=False)

    assert result.exit_code == 0
    session_branch = current_branch(linked)
    assert session_branch.startswith("cmoc/session/")
    assert current_branch(root) == root_branch
    state = json.loads(session_state_path(root, session_branch).read_text())
    assert state["session"]["session_home_branch"] == "linked-home"
    assert state["session"]["session_start_commit"] == linked_commit
    assert run_git(linked, "rev-parse", session_branch).stdout.strip() == linked_commit


def test_session_abandon_switches_home_and_marks_state(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert runner.invoke(app, ["init"], catch_exceptions=False).exit_code == 0
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )
    session_branch = current_branch(root)
    state_path = session_state_path(root, session_branch)
    home_branch = session_home_branch(root, session_branch)
    home_commit = run_git(root, "rev-parse", home_branch).stdout.strip()

    result = runner.invoke(app, ["session", "abandon"], catch_exceptions=False)

    assert result.exit_code == 0
    assert current_branch(root) == home_branch
    assert run_git(root, "rev-parse", home_branch).stdout.strip() == home_commit
    assert (
        subprocess.run(
            ["git", "rev-parse", "--verify", session_branch], cwd=root
        ).returncode
        != 0
    )
    state = json.loads(state_path.read_text())
    assert state["session"]["state"] == "abandoned"
    assert f"- abandoned_branch: `{session_branch}`" in result.output
    assert "- session_state: `abandoned`" in result.output


def test_session_abandon_uses_linked_worktree_branch(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert runner.invoke(app, ["init"], catch_exceptions=False).exit_code == 0
    root_branch = current_branch(root)
    linked = root / ".cmoc" / "worktrees" / "linked"
    run_git(root, "worktree", "add", "-b", "linked-home", str(linked), "HEAD")
    monkeypatch.chdir(linked)
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )
    session_branch = current_branch(linked)
    state_path = session_state_path(root, session_branch)
    home_branch = session_home_branch(root, session_branch)
    home_commit = run_git(root, "rev-parse", home_branch).stdout.strip()

    result = runner.invoke(app, ["session", "abandon"], catch_exceptions=False)

    assert result.exit_code == 0
    assert current_branch(root) == root_branch
    assert current_branch(linked) == home_branch
    assert run_git(root, "rev-parse", home_branch).stdout.strip() == home_commit
    assert (
        subprocess.run(
            ["git", "rev-parse", "--verify", session_branch], cwd=root
        ).returncode
        != 0
    )
    state = json.loads(state_path.read_text())
    assert state["session"]["state"] == "abandoned"
    assert f"- abandoned_branch: `{session_branch}`" in result.output


def test_session_abandon_requires_existing_home_branch(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert runner.invoke(app, ["init"], catch_exceptions=False).exit_code == 0
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )
    session_branch = current_branch(root)
    home_branch = session_home_branch(root, session_branch)
    home_commit = run_git(root, "rev-parse", home_branch).stdout.strip()
    run_git(root, "branch", "-D", home_branch)
    run_git(root, "tag", home_branch, home_commit)

    result = runner.invoke(app, ["session", "abandon"])

    assert result.exit_code != 0
    assert "completed session abandon" in result.output
    assert "- sub_command_log: `" in result.output
    assert "- step_execute_elapsed: `" in result.output
    assert "- elapsed: `" in result.output
    assert "- quota_wait: `" in result.output
    assert "- returncode: `1`" in result.output
    assert current_branch(root) == session_branch
    assert "session home branch が存在しません。" in result.stdout
    assert "session home branch が存在しません。" not in result.stderr
    assert (
        subprocess.run(
            ["git", "rev-parse", "--verify", session_branch], cwd=root
        ).returncode
        == 0
    )


def test_session_abandon_rolls_back_state_and_branch_on_cleanup_failure(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert runner.invoke(app, ["init"], catch_exceptions=False).exit_code == 0
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )
    session_branch = current_branch(root)
    state_path = session_state_path(root, session_branch)
    original_delete_branch = session_module.delete_branch

    def fake_delete_branch(root: Path, branch: str, force: bool = False) -> None:
        if branch == session_branch:
            raise CmocError("delete failed", ["next"], "branch delete failed")
        return original_delete_branch(root, branch, force)

    monkeypatch.setattr(session_module, "delete_branch", fake_delete_branch)

    result = runner.invoke(app, ["session", "abandon"])

    assert result.exit_code != 0
    assert "session abandon の cleanup に失敗しました。" in result.stdout
    assert "`cmoc session abandon` を再実行してください。" in result.stdout
    assert "session abandon の cleanup に失敗しました。" not in result.stderr
    assert current_branch(root) == session_branch
    assert (
        subprocess.run(
            ["git", "rev-parse", "--verify", session_branch], cwd=root
        ).returncode
        == 0
    )
    state = json.loads(state_path.read_text())
    assert state["session"]["state"] == "active"


def test_session_join_resolves_oracle_conflict_with_realization_write_profile(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = make_repo(tmp_path)
    target = root / "oracle" / "spec.md"
    other_oracle_file = root / "oracle" / "other.md"
    other_oracle_file.write_text("# other\n")
    run_git(root, "add", "oracle/other.md")
    run_git(root, "commit", "-m", "add other oracle")
    monkeypatch.chdir(root)
    assert runner.invoke(app, ["init"], catch_exceptions=False).exit_code == 0
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )
    session_branch = current_branch(root)
    home_branch = session_home_branch(root, session_branch)
    target.write_text("session change\n")
    run_git(root, "add", "oracle/spec.md")
    run_git(root, "commit", "-m", "session change")
    run_git(root, "switch", home_branch)
    target.write_text("home change\n")
    run_git(root, "add", "oracle/spec.md")
    run_git(root, "commit", "-m", "home change")
    run_git(root, "switch", session_branch)
    calls: list[str] = []
    modes: list[FileAccessMode] = []

    class FakeCodexResult:
        output_json = None

    def fake_run_codex_exec(parameter: object, **kwargs: object) -> object:
        calls.append(kwargs["purpose"])
        modes.append(parameter.file_access_mode)
        assert kwargs["extra_writable_paths"] == [target]
        target.write_text("resolved change\nTitle\n=======\n")
        return FakeCodexResult()

    monkeypatch.setattr(session_join_module, "run_codex_exec", fake_run_codex_exec)

    result = runner.invoke(app, ["session", "join"], catch_exceptions=False)

    assert result.exit_code == 0
    assert current_branch(root) == home_branch
    assert target.read_text() == "resolved change\nTitle\n=======\n"
    assert calls == ["session join conflict resolution"]
    assert modes == [FileAccessMode.REALIZATION_WRITE]


def test_session_join_conflict_marker_detection_uses_marker_block() -> None:
    assert not session_join_module._has_conflict_marker_block("Title\n=======\n")
    assert session_join_module._has_conflict_marker_block(
        "<<<<<<< HEAD\nhome\n=======\nsession\n>>>>>>> branch\n"
    )
    assert session_join_module._has_conflict_marker_block(
        "<<<<<<< HEAD\nhome\n========\nsession\n>>>>>>> branch\n"
    )


def test_session_join_uses_linked_worktree_branch(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert runner.invoke(app, ["init"], catch_exceptions=False).exit_code == 0
    root_branch = current_branch(root)
    linked = root / ".cmoc" / "worktrees" / "linked"
    run_git(root, "worktree", "add", "-b", "linked-home", str(linked), "HEAD")
    monkeypatch.chdir(linked)
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )
    session_branch = current_branch(linked)
    home_branch = session_home_branch(root, session_branch)
    (linked / "README.md").write_text("linked session change\n")
    run_git(linked, "add", "README.md")
    run_git(linked, "commit", "-m", "linked session change")

    result = runner.invoke(app, ["session", "join"], catch_exceptions=False)

    assert result.exit_code == 0
    assert current_branch(root) == root_branch
    assert current_branch(linked) == home_branch
    assert (linked / "README.md").read_text() == "linked session change\n"
    state = json.loads(session_state_path(root, session_branch).read_text())
    assert state["session"]["state"] == "joined"
    assert "joined_at" not in state["session"]


def test_session_join_stages_delete_conflict_resolution(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert runner.invoke(app, ["init"], catch_exceptions=False).exit_code == 0
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )
    session_branch = current_branch(root)
    home_branch = session_home_branch(root, session_branch)
    (root / "README.md").unlink()
    run_git(root, "add", "README.md")
    run_git(root, "commit", "-m", "session deletes readme")
    run_git(root, "switch", home_branch)
    (root / "README.md").write_text("home change\n")
    run_git(root, "add", "README.md")
    run_git(root, "commit", "-m", "home changes readme")
    run_git(root, "switch", session_branch)

    class FakeCodexResult:
        output_json = None

    def fake_run_codex_exec(parameter: object, **kwargs: object) -> object:
        (root / "README.md").unlink()
        return FakeCodexResult()

    monkeypatch.setattr(session_join_module, "run_codex_exec", fake_run_codex_exec)

    result = runner.invoke(app, ["session", "join"], catch_exceptions=False)

    assert result.exit_code == 0
    assert current_branch(root) == home_branch
    assert not (root / "README.md").exists()
    assert run_git(root, "diff", "--name-only", "--diff-filter=U").stdout == ""


def test_session_join_warns_when_session_branch_cannot_be_deleted(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert runner.invoke(app, ["init"], catch_exceptions=False).exit_code == 0
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )
    session_branch = current_branch(root)
    home_branch = session_home_branch(root, session_branch)
    original_run_git = session_join_module.run_git

    def fake_run_git(args: list[str], cwd: Path, check: bool = True) -> object:
        if args == ["branch", "-d", session_branch]:
            return cmoc_runtime.CommandResult(1, "", "branch is checked out elsewhere")
        return original_run_git(args, cwd, check=check)

    monkeypatch.setattr(session_join_module, "run_git", fake_run_git)

    result = runner.invoke(app, ["session", "join"], catch_exceptions=False)

    assert result.exit_code == 0
    assert current_branch(root) == home_branch
    assert (
        subprocess.run(
            ["git", "rev-parse", "--verify", session_branch], cwd=root
        ).returncode
        == 0
    )
    assert "- deleted_session_branch: `False`" in result.output
    assert f"session branch was not deleted: {session_branch}" in result.output


def test_session_join_error_report_is_written_to_stdout(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert runner.invoke(app, ["init"], catch_exceptions=False).exit_code == 0
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )
    (root / "README.md").write_text("dirty\n")

    result = runner.invoke(app, ["session", "join"])

    assert result.exit_code != 0
    assert "completed session join" in result.stdout
    assert "# ERROR" in result.stdout
    assert "git 未コミット差分が存在します。" in result.stdout
    assert "# ERROR" not in result.stderr
    assert "git 未コミット差分が存在します。" not in result.stderr


def test_session_join_unexpected_error_after_merge_is_written_to_stderr(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = make_repo(tmp_path)
    target = root / "README.md"
    monkeypatch.chdir(root)
    assert runner.invoke(app, ["init"], catch_exceptions=False).exit_code == 0
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )
    session_branch = current_branch(root)
    home_branch = session_home_branch(root, session_branch)
    target.write_text("session change\n")
    run_git(root, "add", "README.md")
    run_git(root, "commit", "-m", "session change")
    run_git(root, "switch", home_branch)
    target.write_text("home change\n")
    run_git(root, "add", "README.md")
    run_git(root, "commit", "-m", "home change")
    run_git(root, "switch", session_branch)

    class FakeCodexResult:
        output_json = None

    def fake_run_codex_exec(parameter: object, **kwargs: object) -> object:
        target.write_text("<<<<<<< HEAD\nhome\n========\nsession\n>>>>>>> branch\n")
        return FakeCodexResult()

    monkeypatch.setattr(session_join_module, "run_codex_exec", fake_run_codex_exec)

    result = runner.invoke(app, ["session", "join"])

    assert result.exit_code != 0
    assert current_branch(root) == home_branch
    assert "# ERROR" not in result.stdout
    assert "conflict marker が残っています。" not in result.stdout
    assert "# ERROR" in result.stderr
    assert "conflict marker が残っています。" in result.stderr
