"""apply abandon の CLI 外部挙動を検証する。

worktree・branch・state の cleanup、実行位置、process 停止を、CLI が返す
成功・警告・失敗として検証する。低レベルな process helper の契約は
`test_runtime_apply.py` に分離している。

根拠:
- {{work-root}}/oracle/doc/app_spec/sub_command/apply_abandon.md
- {{work-root}}/oracle/src/oracle/prompt_builder/parts/realization_standard.py
"""

import json
import subprocess
from pathlib import Path

import pytest
from _apply_support import apply_worktree_from_state
from _cli_support import runner
from _git_support import make_repo, run_git
from _ollama_support import run_doctor

import commons.runtime_apply as apply_runtime
import sub_commands.apply.abandon as apply_abandon_module
import sub_commands.apply.fork as apply_fork_module
from main import app


def setup_linked_session_apply(
    root: Path, monkeypatch: pytest.MonkeyPatch
) -> tuple[Path, Path, str, Path]:
    """linked session 上の active apply run を abandon 境界条件用に作る。"""
    linked = root / ".cmoc" / "gu" / "worktree" / "linked-session-abandon"
    run_git(root, "worktree", "add", "-b", "linked-home", str(linked), "HEAD")
    monkeypatch.chdir(linked)
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )
    session_branch = run_git(linked, "branch", "--show-current").stdout.strip()
    session_id = session_branch.removeprefix("cmoc/session/")
    state_path = root / ".cmoc" / "gu" / "ar" / "session" / f"{session_id}.json"
    state = json.loads(state_path.read_text())
    apply_branch = f"cmoc/apply/{session_id}/manual"
    apply_worktree = root / ".cmoc" / "gu" / "worktree" / session_id / "manual"
    run_git(
        root,
        "worktree",
        "add",
        "-b",
        apply_branch,
        str(apply_worktree),
        session_branch,
    )
    state["apply"] = {
        "state": "completed",
        "apply_branch": apply_branch,
        "oracle_snapshot_commit": run_git(linked, "rev-parse", "HEAD").stdout.strip(),
    }
    state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n")
    return linked, state_path, apply_branch, apply_worktree


def test_apply_abandon_removes_apply_worktree_and_branch(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """completed apply run の worktree、branch、state cleanup を固定する。"""
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert run_doctor(root).exit_code == 0
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )

    class FakeCodexResult:
        """apply fork を findings なしで完了させる fake 結果。"""

        output_json = {"findings": []}

    monkeypatch.setattr(
        apply_fork_module,
        "run_codex_exec",
        lambda parameter, **kwargs: FakeCodexResult(),
    )
    assert runner.invoke(app, ["apply", "fork"], catch_exceptions=False).exit_code == 0
    session_branch = run_git(root, "branch", "--show-current").stdout.strip()
    session_id = session_branch.removeprefix("cmoc/session/")
    state_path = root / ".cmoc" / "gu" / "ar" / "session" / f"{session_id}.json"
    state = json.loads(state_path.read_text())
    apply_branch = state["apply"]["apply_branch"]
    apply_worktree = apply_worktree_from_state(root, state)
    assert apply_worktree.is_dir()

    result = runner.invoke(app, ["apply", "abandon"], catch_exceptions=False)

    assert result.exit_code == 0
    assert f"- apply_branch: `{apply_branch}`" in result.stdout
    assert f"- apply_worktree: `{apply_worktree}`" in result.stdout
    assert "- before: `completed`" in result.stdout
    assert "- after: `ready`" in result.stdout
    assert "- warnings:" in result.stdout
    assert result.stderr == ""
    assert not apply_worktree.exists()
    assert (
        subprocess.run(
            ["git", "rev-parse", "--verify", apply_branch], cwd=root
        ).returncode
        != 0
    )
    state = json.loads(state_path.read_text())
    assert state["apply"]["state"] == "ready"
    assert state["apply"]["apply_branch"] is None
    assert "apply_worktree" not in state["apply"]


def test_apply_abandon_reports_missing_cleanup_targets_as_warnings(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """cleanup 対象が先に消えていても警告として成功扱いにする。"""
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert run_doctor(root).exit_code == 0
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )

    class FakeCodexResult:
        """cleanup 警告経路へ進むための findings なし fake 結果。"""

        output_json = {"findings": []}

    monkeypatch.setattr(
        apply_fork_module,
        "run_codex_exec",
        lambda parameter, **kwargs: FakeCodexResult(),
    )
    assert runner.invoke(app, ["apply", "fork"], catch_exceptions=False).exit_code == 0
    session_branch = run_git(root, "branch", "--show-current").stdout.strip()
    session_id = session_branch.removeprefix("cmoc/session/")
    state_path = root / ".cmoc" / "gu" / "ar" / "session" / f"{session_id}.json"
    state = json.loads(state_path.read_text())
    apply_branch = state["apply"]["apply_branch"]
    apply_worktree = apply_worktree_from_state(root, state)
    run_git(root, "worktree", "remove", "--force", str(apply_worktree))
    run_git(root, "branch", "-D", apply_branch)

    result = runner.invoke(app, ["apply", "abandon"], catch_exceptions=False)

    assert result.exit_code == 0
    assert f"apply worktree already missing: {apply_worktree}" in result.stdout
    assert f"apply branch already missing: {apply_branch}" in result.stdout
    assert f"- apply_worktree: `{apply_worktree}`" in result.stdout
    assert result.stderr == ""
    state = json.loads(state_path.read_text())
    assert state["apply"]["state"] == "ready"
    assert state["apply"]["apply_branch"] is None
    assert "apply_worktree" not in state["apply"]


@pytest.mark.parametrize("apply_state", ["running", "completed", "error"])
def test_apply_abandon_stops_tracked_apply_process_before_cleanup(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, apply_state: str
) -> None:
    """tracked process を止めてから cleanup へ進む。"""
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert run_doctor(root).exit_code == 0
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )

    class FakeCodexResult:
        """running state へ差し替える前提の apply run を作る fake 結果。"""

        output_json = {"findings": []}

    monkeypatch.setattr(
        apply_fork_module,
        "run_codex_exec",
        lambda parameter, **kwargs: FakeCodexResult(),
    )
    assert runner.invoke(app, ["apply", "fork"], catch_exceptions=False).exit_code == 0
    session_branch = run_git(root, "branch", "--show-current").stdout.strip()
    session_id = session_branch.removeprefix("cmoc/session/")
    state_path = root / ".cmoc" / "gu" / "ar" / "session" / f"{session_id}.json"
    state = json.loads(state_path.read_text())
    apply_branch = state["apply"]["apply_branch"]
    apply_worktree = apply_worktree_from_state(root, state)
    state["apply"]["state"] = apply_state
    state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n")
    process_id_path = (
        root / ".cmoc" / "gu" / "ar" / "state" / "apply_processes" / f"{session_id}.pid"
    )
    process_id_path.parent.mkdir(parents=True, exist_ok=True)
    process_id_path.write_text("12345 67890\n")
    stopped: list[int] = []

    def fake_stop_apply_process(
        process: apply_runtime.ApplyProcessIdentity,
        read_after_parent_exit: object = None,
    ) -> str:
        """cleanup 前の worktree と branch がまだ残っていることを観測する。"""
        assert apply_worktree.is_dir()
        assert run_git(root, "rev-parse", "--verify", apply_branch).returncode == 0
        stopped.append(process.process_id)
        return (
            "apply child process already stopped: 23456; "
            "apply process already stopped: 12345"
        )

    monkeypatch.setattr(
        apply_abandon_module, "stop_apply_process", fake_stop_apply_process
    )

    result = runner.invoke(app, ["apply", "abandon"], catch_exceptions=False)

    assert result.exit_code == 0
    assert f"- before: `{apply_state}`" in result.stdout
    assert stopped == [12345]
    assert "apply child process already stopped: 23456" in result.stdout
    assert "apply process already stopped: 12345" in result.stdout
    assert result.stderr == ""
    assert not apply_worktree.exists()
    deleted = subprocess.run(["git", "rev-parse", "--verify", apply_branch], cwd=root)
    assert deleted.returncode != 0
    state = json.loads(state_path.read_text())
    assert state["apply"]["state"] == "ready"
    assert not process_id_path.exists()


def test_apply_abandon_rejects_running_state_without_process_id(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """running state で process identity が無い場合は cleanup 前に拒否する。"""
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert run_doctor(root).exit_code == 0
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )

    class FakeCodexResult:
        """process identity 欠落を作る前提の apply run を作る fake 結果。"""

        output_json = {"findings": []}

    monkeypatch.setattr(
        apply_fork_module,
        "run_codex_exec",
        lambda parameter, **kwargs: FakeCodexResult(),
    )
    assert runner.invoke(app, ["apply", "fork"], catch_exceptions=False).exit_code == 0
    session_branch = run_git(root, "branch", "--show-current").stdout.strip()
    session_id = session_branch.removeprefix("cmoc/session/")
    state_path = root / ".cmoc" / "gu" / "ar" / "session" / f"{session_id}.json"
    state = json.loads(state_path.read_text())
    apply_branch = state["apply"]["apply_branch"]
    apply_worktree = apply_worktree_from_state(root, state)
    state["apply"]["state"] = "running"
    state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n")
    process_id_path = apply_runtime.apply_process_id_path(root, session_id)
    process_id_path.unlink(missing_ok=True)
    assert not process_id_path.exists()

    result = runner.invoke(app, ["apply", "abandon"], catch_exceptions=False)

    assert result.exit_code != 0
    assert "実行中 apply process を特定できません。" in result.stdout
    assert result.stderr == ""
    assert apply_worktree.is_dir()
    remaining = subprocess.run(["git", "rev-parse", "--verify", apply_branch], cwd=root)
    assert remaining.returncode == 0
    state = json.loads(state_path.read_text())
    assert state["apply"]["state"] == "running"
    assert state["apply"]["apply_branch"] == apply_branch


def test_apply_abandon_rejects_apply_branch_without_derivable_worktree(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """state 上の apply branch から worktree が導けない破損状態を拒否する。"""
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert run_doctor(root).exit_code == 0
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )
    session_branch = run_git(root, "branch", "--show-current").stdout.strip()
    session_id = session_branch.removeprefix("cmoc/session/")
    state_path = root / ".cmoc" / "gu" / "ar" / "session" / f"{session_id}.json"
    state = json.loads(state_path.read_text())
    state["apply"]["state"] = "completed"
    state["apply"]["apply_branch"] = "cmoc/apply/malformed"
    state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n")

    result = runner.invoke(app, ["apply", "abandon"])

    assert result.exit_code != 0
    assert "apply branch 名から session-id を特定できません。" in result.stdout
    assert result.stderr == ""
    state = json.loads(state_path.read_text())
    assert state["apply"]["state"] == "completed"
    assert state["apply"]["apply_branch"] == "cmoc/apply/malformed"


def test_apply_abandon_rejects_other_session_apply_branch_from_session_branch(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """state に混入した別 session apply branch は cleanup 前に拒否する。"""
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert run_doctor(root).exit_code == 0
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )
    session_branch = run_git(root, "branch", "--show-current").stdout.strip()
    session_id = session_branch.removeprefix("cmoc/session/")
    state_path = root / ".cmoc" / "gu" / "ar" / "session" / f"{session_id}.json"
    other_session_id = "other-session"
    other_apply_branch = f"cmoc/apply/{other_session_id}/manual"
    other_apply_worktree = (
        root / ".cmoc" / "gu" / "worktree" / other_session_id / "manual"
    )
    run_git(
        root,
        "worktree",
        "add",
        "-b",
        other_apply_branch,
        str(other_apply_worktree),
        session_branch,
    )
    state = json.loads(state_path.read_text())
    state["apply"]["state"] = "completed"
    state["apply"]["apply_branch"] = other_apply_branch
    state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n")

    result = runner.invoke(app, ["apply", "abandon"])

    assert result.exit_code != 0
    assert "破棄対象 apply run の補助情報を特定できません。" in result.stdout
    assert f"session_id: {session_id}" in result.stdout
    assert f"apply_branch: {other_apply_branch}" in result.stdout
    assert result.stderr == ""
    assert other_apply_worktree.is_dir()
    assert run_git(root, "rev-parse", "--verify", other_apply_branch).returncode == 0
    state = json.loads(state_path.read_text())
    assert state["apply"]["state"] == "completed"
    assert state["apply"]["apply_branch"] == other_apply_branch


def test_apply_abandon_can_run_from_apply_worktree(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """apply worktree 内からの abandon は repo root へ戻して cleanup する。"""
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert run_doctor(root).exit_code == 0
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )

    class FakeCodexResult:
        """apply worktree から abandon する前提の apply run を作る fake 結果。"""

        output_json = {"findings": []}

    monkeypatch.setattr(
        apply_fork_module,
        "run_codex_exec",
        lambda parameter, **kwargs: FakeCodexResult(),
    )
    assert runner.invoke(app, ["apply", "fork"], catch_exceptions=False).exit_code == 0
    session_branch = run_git(root, "branch", "--show-current").stdout.strip()
    session_id = session_branch.removeprefix("cmoc/session/")
    state_path = root / ".cmoc" / "gu" / "ar" / "session" / f"{session_id}.json"
    state = json.loads(state_path.read_text())
    apply_branch = state["apply"]["apply_branch"]
    apply_worktree = apply_worktree_from_state(root, state)
    monkeypatch.chdir(apply_worktree)

    result = runner.invoke(app, ["apply", "abandon"], catch_exceptions=False)

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


def test_apply_abandon_checks_linked_session_worktree_dirty(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """linked session worktree の未コミット差分がある abandon を拒否する。"""
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert run_doctor(root).exit_code == 0
    linked, state_path, apply_branch, apply_worktree = setup_linked_session_apply(
        root, monkeypatch
    )
    (linked / "README.md").write_text("# dirty\n")

    result = runner.invoke(app, ["apply", "abandon"])

    assert result.exit_code != 0
    assert "git 未コミット差分が存在します。" in result.stdout
    assert "git 未コミット差分が存在します。" not in result.stderr
    assert apply_worktree.is_dir()
    assert run_git(root, "rev-parse", "--verify", apply_branch).returncode == 0
    state = json.loads(state_path.read_text())
    assert state["apply"]["state"] == "completed"
    assert state["apply"]["apply_branch"] == apply_branch


def test_apply_abandon_from_linked_apply_worktree_uses_repo_state(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """linked apply worktree からでも repo 側 state を正として cleanup する。"""
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert run_doctor(root).exit_code == 0
    linked, state_path, apply_branch, apply_worktree = setup_linked_session_apply(
        root, monkeypatch
    )
    monkeypatch.chdir(apply_worktree)

    result = runner.invoke(app, ["apply", "abandon"], catch_exceptions=False)

    assert result.exit_code == 0
    assert Path.cwd() == linked
    assert not apply_worktree.exists()
    assert (
        subprocess.run(
            ["git", "rev-parse", "--verify", apply_branch], cwd=root
        ).returncode
        != 0
    )
    state = json.loads(state_path.read_text())
    assert state["apply"]["state"] == "ready"
    assert state["apply"]["apply_branch"] is None


def test_apply_abandon_rejects_stale_apply_branch(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """同じ session の古い apply branch から active run 破棄を拒否する。"""
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert run_doctor(root).exit_code == 0
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )

    class FakeCodexResult:
        """stale apply branch を追加する前提の active run を作る fake 結果。"""

        output_json = {"findings": []}

    monkeypatch.setattr(
        apply_fork_module,
        "run_codex_exec",
        lambda parameter, **kwargs: FakeCodexResult(),
    )
    assert runner.invoke(app, ["apply", "fork"], catch_exceptions=False).exit_code == 0
    session_branch = run_git(root, "branch", "--show-current").stdout.strip()
    session_id = session_branch.removeprefix("cmoc/session/")
    state_path = root / ".cmoc" / "gu" / "ar" / "session" / f"{session_id}.json"
    state = json.loads(state_path.read_text())
    apply_branch = state["apply"]["apply_branch"]
    apply_worktree = apply_worktree_from_state(root, state)
    stale_branch = f"cmoc/apply/{session_id}/stale"
    stale_worktree = root / ".cmoc" / "gu" / "worktree" / session_id / "stale"
    run_git(
        root,
        "worktree",
        "add",
        "-b",
        stale_branch,
        str(stale_worktree),
        session_branch,
    )
    monkeypatch.chdir(stale_worktree)

    result = runner.invoke(app, ["apply", "abandon"])

    assert result.exit_code != 0
    assert (
        "現在の apply branch は破棄対象の active apply run ではありません。"
        in result.stdout
    )
    assert f"current_branch: {stale_branch}" in result.stdout
    assert f"apply_branch: {apply_branch}" in result.stdout
    assert result.stderr == ""
    assert apply_worktree.is_dir()
    assert run_git(root, "rev-parse", "--verify", apply_branch).returncode == 0
    state = json.loads(state_path.read_text())
    assert state["apply"]["state"] == "completed"
    assert state["apply"]["apply_branch"] == apply_branch
