"""session fork/join/abandon の CLI 外部挙動をまとめて検証する。

このファイルは 16,000 文字を超えるが、責務境界は session branch と session state の
ライフサイクルに閉じている。fork、join、abandon、linked worktree、state cleanup、
dirty worktree 拒否は同じ session 状態遷移の観測点であり、分割すると同じ branch/state
fixture を追う文脈が分散する。現状は session CLI 回帰として一箇所に保つ方が凝集性が高い。
根拠: <work-root>/oracle/src/oracle/prompt_builder/parts/realization_standard.py
"""

import json
import subprocess
import tomllib
from pathlib import Path

import cmoc_runtime
from basic.acp import AgentCallParameter, FileAccessMode
from cmoc_runtime import CmocError
from commons.runtime_codex_profile import build_codex_profile
from config.cmoc_config import CmocConfig
import pytest

from _support import (
    current_branch,
    make_repo,
    run_git,
    runner,
    run_doctor,
)
from main import app
import sub_commands.session.abandon as session_module
import sub_commands.session.fork as session_fork_module
import sub_commands.session.join as session_join_module


def session_state_path(root: Path, session_branch: str) -> Path:
    session_id = session_branch.removeprefix("cmoc/session/")
    return root / ".cmoc" / "local" / "session" / f"{session_id}.json"


def session_home_branch(root: Path, session_branch: str) -> str:
    state = json.loads(session_state_path(root, session_branch).read_text())
    return state["session"]["session_home_branch"]


def write_abandoned_state(root: Path, session_id: str) -> Path:
    path = root / ".cmoc" / "local" / "session" / f"{session_id}.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(
            {
                "session": {
                    "state": "abandoned",
                    "session_home_branch": "old-home",
                    "session_start_commit": "old-commit",
                    "last_joined_apply_oracle_snapshot_commit": None,
                    "joined_at": None,
                },
                "apply": {
                    "state": "ready",
                    "apply_branch": None,
                    "oracle_snapshot_commit": None,
                },
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n"
    )
    return path


def break_preprocess_invariants(work: Path) -> Path:
    gitignore = work / ".gitignore"
    gitignore.write_text(
        "\n".join(
            line
            for line in gitignore.read_text().splitlines()
            if line != "/.cmoc/local/"
        )
        + "\n"
    )
    tracked_probe = work / ".cmoc" / "local" / "tracked-probe"
    tracked_probe.parent.mkdir(parents=True, exist_ok=True)
    tracked_probe.write_text("tracked\n")
    run_git(work, "add", ".gitignore")
    run_git(work, "add", "-f", ".cmoc/local/tracked-probe")
    run_git(work, "rm", ".agents/.gitkeep")
    run_git(work, "commit", "-m", "break preprocess invariants")
    return gitignore


def test_session_fork_creates_session_branch_and_state(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    home_branch = current_branch(root)
    doctor_result = run_doctor(root)
    assert doctor_result.exit_code == 0

    result = runner.invoke(app, ["session", "fork"], catch_exceptions=False)

    assert result.exit_code == 0
    branch = current_branch(root)
    assert branch.startswith("cmoc/session/")
    state = json.loads(session_state_path(root, branch).read_text())
    assert state["session"]["state"] == "active"
    assert state["session"]["session_home_branch"] == home_branch
    assert state["session"]["last_joined_apply_oracle_snapshot_commit"] is None
    assert state["session"]["joined_at"] is None
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
    assert (root / ".cmoc" / "local" / "session" / f"{next_id}.json").is_file()
    assert f"- session_branch: `cmoc/session/{next_id}`" in result.output


def test_session_fork_rejects_corrupt_state_without_active_session_message(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    home_branch = current_branch(root)
    path = root / ".cmoc" / "local" / "session" / "broken.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps({"session": {"session_home_branch": home_branch}, "apply": {}})
        + "\n"
    )

    result = runner.invoke(app, ["session", "fork"])

    assert result.exit_code != 0
    assert "session state file が不正です。" in result.stdout
    assert "active session が既に存在します。" not in result.stdout
    assert current_branch(root) == home_branch


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
    assert "/.cmoc/local/" in (root / ".gitignore").read_text()
    assert (
        subprocess.run(
            ["git", "check-ignore", "-q", ".cmoc/local/.__cmoc_ignore_probe__"],
            cwd=root,
        ).returncode
        == 0
    )
    assert len(list((root / ".cmoc" / "local" / "log" / "sub_command").glob("*.jsonl"))) == 1
    assert run_git(root, "status", "--short").stdout.strip() == ""


def test_session_fork_uses_linked_worktree_branch_and_head(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert run_doctor(root).exit_code == 0
    root_branch = current_branch(root)
    linked = root / ".cmoc" / "local" / "worktree" / "linked"
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
    assert run_doctor(root).exit_code == 0
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
    assert state["session"]["joined_at"] is None
    assert f"- abandoned_branch: `{session_branch}`" in result.output
    assert "- session_state: `abandoned`" in result.output


def test_session_abandon_uses_linked_worktree_branch(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert run_doctor(root).exit_code == 0
    root_branch = current_branch(root)
    linked = root / ".cmoc" / "local" / "worktree" / "linked"
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
    assert state["session"]["joined_at"] is None
    assert f"- abandoned_branch: `{session_branch}`" in result.output


def test_session_abandon_preprocesses_linked_worktree_before_preconditions(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert run_doctor(root).exit_code == 0
    linked = root / ".cmoc" / "local" / "worktree" / "linked"
    run_git(root, "worktree", "add", "-b", "linked-home", str(linked), "HEAD")
    monkeypatch.chdir(linked)
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )
    session_branch = current_branch(linked)
    home_branch = session_home_branch(root, session_branch)
    gitignore = break_preprocess_invariants(linked)
    run_git(root, "branch", "-D", home_branch)

    result = runner.invoke(app, ["session", "abandon"])

    assert result.exit_code != 0
    assert current_branch(linked) == session_branch
    assert "session home branch が存在しません。" in result.stdout
    assert "/.cmoc/local/" in gitignore.read_text().splitlines()
    assert run_git(linked, "ls-files", "--", ".cmoc/local").stdout == ""
    assert run_git(linked, "ls-files", "--", ".agents").stdout.splitlines() == [
        ".agents/.gitkeep"
    ]
    assert run_git(linked, "status", "--short").stdout.strip() == ""


def test_session_abandon_requires_existing_home_branch(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert run_doctor(root).exit_code == 0
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )
    session_branch = current_branch(root)
    home_branch = session_home_branch(root, session_branch)
    home_commit = run_git(root, "rev-parse", home_branch).stdout.strip()
    gitignore = root / ".gitignore"
    gitignore.write_text(
        "\n".join(
            line for line in gitignore.read_text().splitlines() if line != "/.cmoc/local/"
        )
        + "\n"
    )
    tracked_probe = root / ".cmoc" / "local" / "tracked-probe"
    tracked_probe.parent.mkdir(parents=True, exist_ok=True)
    tracked_probe.write_text("tracked\n")
    run_git(root, "add", ".gitignore")
    run_git(root, "add", "-f", ".cmoc/local/tracked-probe")
    run_git(root, "commit", "-m", "track cmoc probe on session")
    run_git(root, "branch", "-D", home_branch)
    run_git(root, "tag", home_branch, home_commit)

    result = runner.invoke(app, ["session", "abandon"])

    assert result.exit_code != 0
    assert "完了 session abandon" in result.output
    assert "- サブコマンドログ: `" in result.output
    assert "- ステップ経過時間[2/3 実行 session abandon]: `" in result.output
    assert "- 経過時間: `" in result.output
    assert "- quota 待機時間: `" in result.output
    assert "- 終了コード: `1`" in result.output
    assert current_branch(root) == session_branch
    assert "session home branch が存在しません。" in result.stdout
    assert "session home branch が存在しません。" not in result.stderr
    assert (
        subprocess.run(
            ["git", "rev-parse", "--verify", session_branch], cwd=root
        ).returncode
        == 0
    )
    assert "/.cmoc/local/" in gitignore.read_text().splitlines()
    assert run_git(root, "ls-files", "--", ".cmoc/local").stdout == ""


@pytest.mark.parametrize(
    "cleanup_error",
    [
        CmocError("delete failed", ["next"], "branch delete failed"),
        KeyboardInterrupt(),
    ],
)
def test_session_abandon_rolls_back_state_and_branch_on_cleanup_failure(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, cleanup_error: BaseException
) -> None:
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert run_doctor(root).exit_code == 0
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )
    session_branch = current_branch(root)
    state_path = session_state_path(root, session_branch)
    gitignore = root / ".gitignore"
    gitignore.write_text(
        "\n".join(
            line for line in gitignore.read_text().splitlines() if line != "/.cmoc/local/"
        )
        + "\n"
    )
    tracked_probe = root / ".cmoc" / "local" / "tracked-probe"
    tracked_probe.parent.mkdir(parents=True, exist_ok=True)
    tracked_probe.write_text("tracked\n")
    run_git(root, "add", ".gitignore")
    run_git(root, "add", "-f", ".cmoc/local/tracked-probe")
    run_git(root, "commit", "-m", "track cmoc probe on session")
    original_delete_branch = session_module.delete_branch

    def fake_delete_branch(root: Path, branch: str, force: bool = False) -> None:
        if branch == session_branch:
            raise cleanup_error
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
    assert state["session"]["joined_at"] is None
    assert "/.cmoc/local/" in gitignore.read_text().splitlines()
    assert run_git(root, "ls-files", "--", ".cmoc/local").stdout == ""
    assert run_git(root, "status", "--short").stdout.strip() == ""


@pytest.mark.parametrize("command", ["abandon", "join"])
def test_session_completion_rejects_missing_state_fields(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, command: str
) -> None:
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert run_doctor(root).exit_code == 0
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )
    session_branch = current_branch(root)
    path = session_state_path(root, session_branch)
    broken_state = {
        "session": {"session_home_branch": session_home_branch(root, session_branch)}
    }
    path.write_text(json.dumps(broken_state) + "\n")

    result = runner.invoke(app, ["session", command])

    assert result.exit_code != 0
    assert "session state file が不正です。" in result.stdout
    assert "必須 field" in result.stdout
    assert current_branch(root) == session_branch


def test_session_join_resolves_oracle_conflict_with_repo_write_profile(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = make_repo(tmp_path)
    target = root / "oracle" / "spec.md"
    monkeypatch.chdir(root)
    assert run_doctor(root).exit_code == 0
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

    def fake_run_codex_exec(parameter: AgentCallParameter, **kwargs: object) -> object:
        calls.append(kwargs["purpose"])
        modes.append(parameter.file_access_mode)
        assert kwargs["extra_writable_paths"] == [target]
        assert kwargs["allow_oracle_conflict_writes"] is True
        profile = build_codex_profile(
            parameter,
            CmocConfig(),
            root,
            extra_writable_paths=kwargs["extra_writable_paths"],
            allow_oracle_conflict_writes=kwargs["allow_oracle_conflict_writes"],
        )
        writable_roots = set(
            tomllib.loads(profile)["sandbox_workspace_write"]["writable_roots"]
        )
        assert writable_roots == {
            str(path.resolve())
            for path in (
                root / ".gitignore",
                root / "README.md",
                root / "oracle" / "spec.md",
            )
        }
        target.write_text("resolved change\nTitle\n=======\n")
        return FakeCodexResult()

    monkeypatch.setattr(session_join_module, "run_codex_exec", fake_run_codex_exec)

    result = runner.invoke(app, ["session", "join"], catch_exceptions=False)

    assert result.exit_code == 0, result.output
    assert current_branch(root) == home_branch
    assert target.read_text() == "resolved change\nTitle\n=======\n"
    assert calls == ["session join conflict resolution"]
    assert modes == [FileAccessMode.REPO_WRITE]


def test_session_join_rejects_non_conflict_changes_from_conflict_agent(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = make_repo(tmp_path)
    target = root / "oracle" / "spec.md"
    extra = root / "src" / "extra.py"
    monkeypatch.chdir(root)
    assert run_doctor(root).exit_code == 0
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

    class FakeCodexResult:
        output_json = None

    def fake_run_codex_exec(parameter: object, **kwargs: object) -> object:
        target.write_text("resolved change\n")
        extra.parent.mkdir(exist_ok=True)
        extra.write_text("extra\n")
        return FakeCodexResult()

    monkeypatch.setattr(session_join_module, "run_codex_exec", fake_run_codex_exec)

    result = runner.invoke(app, ["session", "join"])

    assert result.exit_code != 0
    assert current_branch(root) == home_branch
    assert "conflict 解消以外の差分が残っています。" in result.stderr
    assert "src/extra.py" in result.stderr
    assert "session change" not in run_git(root, "log", "--oneline", "-1").stdout


def test_session_join_rejects_staged_non_conflict_change_with_quoted_status_path(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = make_repo(tmp_path)
    target = root / "oracle" / "spec.md"
    extra = root / "src" / "extra file.py"
    extra.parent.mkdir()
    extra.write_text("base\n")
    run_git(root, "add", "src/extra file.py")
    run_git(root, "commit", "-m", "add extra")
    monkeypatch.chdir(root)
    assert run_doctor(root).exit_code == 0
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )
    session_branch = current_branch(root)
    home_branch = session_home_branch(root, session_branch)
    target.write_text("session change\n")
    extra.write_text("session extra\n")
    run_git(root, "add", "oracle/spec.md", "src/extra file.py")
    run_git(root, "commit", "-m", "session changes")
    run_git(root, "switch", home_branch)
    target.write_text("home change\n")
    run_git(root, "add", "oracle/spec.md")
    run_git(root, "commit", "-m", "home change")
    run_git(root, "switch", session_branch)

    class FakeCodexResult:
        output_json = None

    def fake_run_codex_exec(parameter: object, **kwargs: object) -> object:
        target.write_text("resolved change\n")
        extra.write_text("agent extra\n")
        run_git(root, "add", "src/extra file.py")
        return FakeCodexResult()

    monkeypatch.setattr(session_join_module, "run_codex_exec", fake_run_codex_exec)

    result = runner.invoke(app, ["session", "join"])

    assert result.exit_code != 0
    assert current_branch(root) == home_branch
    assert "conflict 解消以外の差分が残っています。" in result.stderr
    assert "src/extra file.py" in result.stderr
    assert "session changes" not in run_git(root, "log", "--oneline", "-1").stdout


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
    assert run_doctor(root).exit_code == 0
    root_branch = current_branch(root)
    linked = root / ".cmoc" / "local" / "worktree" / "linked"
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
    assert state["session"]["joined_at"] is None


def test_session_join_preprocesses_linked_worktree_before_preconditions(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert run_doctor(root).exit_code == 0
    linked = root / ".cmoc" / "local" / "worktree" / "linked"
    run_git(root, "worktree", "add", "-b", "linked-home", str(linked), "HEAD")
    monkeypatch.chdir(linked)
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )
    session_branch = current_branch(linked)
    home_branch = session_home_branch(root, session_branch)
    gitignore = break_preprocess_invariants(linked)
    run_git(root, "branch", "-D", home_branch)

    result = runner.invoke(app, ["session", "join"])

    assert result.exit_code != 0
    assert current_branch(linked) == session_branch
    assert "git コマンドが失敗しました。" in result.stderr
    assert "git コマンドが失敗しました。" not in result.stdout
    assert "/.cmoc/local/" in gitignore.read_text().splitlines()
    assert run_git(linked, "ls-files", "--", ".cmoc/local").stdout == ""
    assert run_git(linked, "ls-files", "--", ".agents").stdout.splitlines() == [
        ".agents/.gitkeep"
    ]
    assert run_git(linked, "status", "--short").stdout.strip() == ""


def test_session_join_stages_delete_conflict_resolution(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert run_doctor(root).exit_code == 0
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
    assert run_doctor(root).exit_code == 0
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


def test_session_join_does_not_delete_when_local_branch_reachability_check_fails(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert run_doctor(root).exit_code == 0
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )
    session_branch = current_branch(root)
    home_branch = session_home_branch(root, session_branch)
    original_run_git = session_join_module.run_git
    delete_calls = 0

    def fake_run_git(args: list[str], cwd: Path, check: bool = True) -> object:
        nonlocal delete_calls
        if args == ["merge-base", "--is-ancestor", session_branch, "HEAD"]:
            return cmoc_runtime.CommandResult(1, "", "")
        if args == ["branch", "-d", session_branch]:
            delete_calls += 1
        return original_run_git(args, cwd, check=check)

    monkeypatch.setattr(session_join_module, "run_git", fake_run_git)

    result = runner.invoke(app, ["session", "join"], catch_exceptions=False)

    assert result.exit_code == 0
    assert current_branch(root) == home_branch
    assert delete_calls == 0
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
    assert run_doctor(root).exit_code == 0
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )
    (root / "README.md").write_text("dirty\n")

    result = runner.invoke(app, ["session", "join"])

    assert result.exit_code != 0
    assert "完了 session join" in result.stdout
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
    assert run_doctor(root).exit_code == 0
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
