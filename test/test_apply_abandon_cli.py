"""apply abandon の cleanup と process 停止を CLI 経由で検証する。

このファイルは 16,000 文字を超えるが、責務境界は active apply run を破棄する
外部挙動の検証に閉じている。worktree/branch/state cleanup、実行位置の判定、
running process の停止は同じ abandon 操作の成功・警告・失敗条件を共有するため、
分割すると同じ state fixture と境界条件を複数ファイルで読み直すことになる。
現状は apply abandon の読み取り文脈を一箇所に保つ方が凝集性が高い。
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
import sub_commands.apply.abandon as apply_abandon_module
import sub_commands.apply.fork as apply_fork_module
from sub_commands.apply import _runtime as apply_runtime


def setup_linked_session_apply(
    root: Path, monkeypatch: pytest.MonkeyPatch
) -> tuple[Path, Path, str, Path]:
    """linked session 上の active apply run を abandon 境界条件用に作る。"""
    linked = root / ".cmoc" / "worktrees" / "linked-session-abandon"
    run_git(root, "worktree", "add", "-b", "linked-home", str(linked), "HEAD")
    monkeypatch.chdir(linked)
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )
    session_branch = run_git(linked, "branch", "--show-current").stdout.strip()
    session_id = session_branch.removeprefix("cmoc/session/")
    state_path = root / ".cmoc" / "sessions" / f"{session_id}.json"
    state = json.loads(state_path.read_text())
    apply_branch = f"cmoc/apply/{session_id}/manual"
    apply_worktree = root / ".cmoc" / "worktrees" / session_id / "manual"
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
    assert runner.invoke(app, ["init"], catch_exceptions=False).exit_code == 0
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
    state_path = root / ".cmoc" / "sessions" / f"{session_id}.json"
    state = json.loads(state_path.read_text())
    apply_branch = state["apply"]["apply_branch"]
    apply_worktree = apply_worktree_from_state(root, state)
    assert apply_worktree.is_dir()

    result = runner.invoke(app, ["apply", "abandon"], catch_exceptions=False)

    assert result.exit_code == 0
    assert f"- apply_branch: `{apply_branch}`" in result.output
    assert f"- apply_worktree: `{apply_worktree}`" in result.output
    assert "- before: `completed`" in result.output
    assert "- after: `ready`" in result.output
    assert "- warnings:" in result.output
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
    assert runner.invoke(app, ["init"], catch_exceptions=False).exit_code == 0
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
    state_path = root / ".cmoc" / "sessions" / f"{session_id}.json"
    state = json.loads(state_path.read_text())
    apply_branch = state["apply"]["apply_branch"]
    apply_worktree = apply_worktree_from_state(root, state)
    run_git(root, "worktree", "remove", "--force", str(apply_worktree))
    run_git(root, "branch", "-D", apply_branch)

    result = runner.invoke(app, ["apply", "abandon"], catch_exceptions=False)

    assert result.exit_code == 0
    assert f"apply worktree already missing: {apply_worktree}" in result.output
    assert f"apply branch already missing: {apply_branch}" in result.output
    assert f"- apply_worktree: `{apply_worktree}`" in result.output
    state = json.loads(state_path.read_text())
    assert state["apply"]["state"] == "ready"
    assert state["apply"]["apply_branch"] is None
    assert "apply_worktree" not in state["apply"]


def test_apply_abandon_stops_running_apply_process_before_cleanup(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """running apply process を停止してから git cleanup へ進む順序を固定する。"""
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert runner.invoke(app, ["init"], catch_exceptions=False).exit_code == 0
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
    state_path = root / ".cmoc" / "sessions" / f"{session_id}.json"
    state = json.loads(state_path.read_text())
    apply_branch = state["apply"]["apply_branch"]
    apply_worktree = apply_worktree_from_state(root, state)
    state["apply"]["state"] = "running"
    state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n")
    process_id_path = (
        root / ".cmoc" / "state" / "apply_processes" / f"{session_id}.pid"
    )
    process_id_path.parent.mkdir(parents=True, exist_ok=True)
    process_id_path.write_text("12345 67890\n")
    stopped: list[int] = []

    def fake_stop_apply_process(process: apply_runtime.ApplyProcessIdentity) -> None:
        """cleanup 前の worktree と branch がまだ残っていることを観測する。"""
        assert apply_worktree.is_dir()
        assert run_git(root, "rev-parse", "--verify", apply_branch).returncode == 0
        stopped.append(process.process_id)

    monkeypatch.setattr(
        apply_abandon_module, "stop_apply_process", fake_stop_apply_process
    )

    result = runner.invoke(app, ["apply", "abandon"], catch_exceptions=False)

    assert result.exit_code == 0
    assert stopped == [12345]
    assert not apply_worktree.exists()
    deleted = subprocess.run(["git", "rev-parse", "--verify", apply_branch], cwd=root)
    assert deleted.returncode != 0
    state = json.loads(state_path.read_text())
    assert state["apply"]["state"] == "ready"
    assert "apply_process_id" not in state["apply"]
    assert not process_id_path.exists()


def test_stop_apply_process_stops_tracked_child_group_before_parent(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Codex subprocess は親 apply process より先に専用 process group ごと止める。"""
    order: list[str] = []

    def fake_stop_child(process: apply_runtime.ProcessIdentity) -> None:
        order.append(f"child:{process.process_id}")

    def fake_send_signal(process_fd: int, process_id: int, sig: int) -> None:
        order.append(f"parent:{process_id}:{sig}")

    monkeypatch.setattr(apply_runtime, "stop_child_process_group", fake_stop_child)
    monkeypatch.setattr(apply_runtime, "open_process_fd", lambda process_id: 10)
    monkeypatch.setattr(apply_runtime, "process_start_time", lambda process_id: 20)
    monkeypatch.setattr(apply_runtime, "send_process_signal", fake_send_signal)
    monkeypatch.setattr(
        apply_runtime, "wait_process_fd_exit", lambda process_fd, timeout: True
    )
    monkeypatch.setattr(apply_runtime.os, "close", lambda process_fd: None)

    warning = apply_runtime.stop_apply_process(
        apply_runtime.ApplyProcessIdentity(
            12345, 20, (apply_runtime.ProcessIdentity(23456, 30),)
        )
    )

    assert warning is None
    assert order == [f"child:23456", f"parent:12345:{apply_runtime.signal.SIGTERM}"]


def test_apply_process_id_reads_tracked_child_processes(tmp_path: Path) -> None:
    """running abandon が親 PID と同時に記録済み Codex child PID を読める。"""
    root = tmp_path
    path = root / ".cmoc" / "state" / "apply_processes" / "session.pid"
    path.parent.mkdir(parents=True)
    path.write_text("12345 20\nchild 23456 30\n")

    process = apply_runtime.read_apply_process_id(root, "session")

    assert process == apply_runtime.ApplyProcessIdentity(
        12345, 20, (apply_runtime.ProcessIdentity(23456, 30),)
    )


def test_stop_child_process_group_accepts_exited_zombie_leader(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """終了済み child が親の reap 待ちで group に残っても親停止へ進める。"""
    sent: list[int] = []

    monkeypatch.setattr(apply_runtime, "process_start_time", lambda process_id: 30)
    monkeypatch.setattr(apply_runtime.os, "getpgid", lambda process_id: process_id)
    monkeypatch.setattr(apply_runtime, "open_process_fd", lambda process_id, name: 10)
    monkeypatch.setattr(
        apply_runtime,
        "send_process_group_signal",
        lambda process_group_id, sig: sent.append(sig),
    )
    monkeypatch.setattr(
        apply_runtime,
        "wait_process_group_exit",
        lambda process_group_id, timeout: False,
    )
    monkeypatch.setattr(
        apply_runtime,
        "process_group_has_no_running_members",
        lambda process_fd, pgid: True,
    )
    monkeypatch.setattr(apply_runtime.os, "close", lambda process_fd: None)

    warning = apply_runtime.stop_child_process_group(
        apply_runtime.ProcessIdentity(23456, 30)
    )

    assert warning is None
    assert sent == [apply_runtime.signal.SIGTERM]


def test_stop_apply_process_treats_raced_exit_as_stopped(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """SIGTERM 後に先に終了した process を正常停止として扱う。"""
    sent: list[int] = []

    def fake_send_signal(process_fd: int, process_id: int, sig: int) -> None:
        """送信した signal だけを観測し、process 実体には触れない。"""
        sent.append(sig)

    monkeypatch.setattr(apply_runtime, "open_process_fd", lambda process_id: 10)
    monkeypatch.setattr(apply_runtime, "process_start_time", lambda process_id: 20)
    monkeypatch.setattr(apply_runtime, "send_process_signal", fake_send_signal)
    monkeypatch.setattr(
        apply_runtime, "wait_process_fd_exit", lambda process_fd, timeout: True
    )
    monkeypatch.setattr(apply_runtime.os, "close", lambda process_fd: None)

    warning = apply_runtime.stop_apply_process(
        apply_runtime.ApplyProcessIdentity(12345, 20)
    )

    assert warning is None
    assert sent == [apply_runtime.signal.SIGTERM]


def test_send_process_signal_ignores_already_exited_process(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """pidfd signal 時点で終了済みの process を cleanup 失敗にしない。"""

    def fake_pidfd_send_signal(process_fd: int, sig: int) -> None:
        """Linux pidfd API が返す終了済み process の例外だけを再現する。"""
        raise ProcessLookupError

    monkeypatch.setattr(
        apply_runtime.signal, "pidfd_send_signal", fake_pidfd_send_signal
    )

    apply_runtime.send_process_signal(10, 12345, apply_runtime.signal.SIGTERM)


def test_stop_apply_process_does_not_signal_reused_pid(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """保存時と開始時刻が異なる PID reuse では signal を送らない。"""
    sent: list[int] = []

    monkeypatch.setattr(apply_runtime, "open_process_fd", lambda process_id: 10)
    monkeypatch.setattr(apply_runtime, "process_start_time", lambda process_id: 99)
    monkeypatch.setattr(
        apply_runtime,
        "send_process_signal",
        lambda process_fd, process_id, sig: sent.append(sig),
    )
    monkeypatch.setattr(apply_runtime.os, "close", lambda process_fd: None)

    warning = apply_runtime.stop_apply_process(
        apply_runtime.ApplyProcessIdentity(12345, 20)
    )

    assert warning == "stale apply process id ignored: 12345"
    assert sent == []


def test_apply_abandon_rejects_running_state_without_process_id(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """running state で process identity が無い場合は cleanup 前に拒否する。"""
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert runner.invoke(app, ["init"], catch_exceptions=False).exit_code == 0
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
    state_path = root / ".cmoc" / "sessions" / f"{session_id}.json"
    state = json.loads(state_path.read_text())
    apply_branch = state["apply"]["apply_branch"]
    apply_worktree = apply_worktree_from_state(root, state)
    state["apply"]["state"] = "running"
    state["apply"].pop("apply_process_id", None)
    state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n")

    result = runner.invoke(app, ["apply", "abandon"], catch_exceptions=False)

    assert result.exit_code != 0
    assert "実行中 apply process を特定できません。" in result.output
    assert apply_worktree.is_dir()
    remaining = subprocess.run(["git", "rev-parse", "--verify", apply_branch], cwd=root)
    assert remaining.returncode == 0
    state = json.loads(state_path.read_text())
    assert state["apply"]["state"] == "running"
    assert state["apply"]["apply_branch"] == apply_branch
    assert "apply_process_id" not in state["apply"]


def test_apply_abandon_rejects_apply_branch_without_derivable_worktree(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """state 上の apply branch から worktree が導けない破損状態を拒否する。"""
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert runner.invoke(app, ["init"], catch_exceptions=False).exit_code == 0
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )
    session_branch = run_git(root, "branch", "--show-current").stdout.strip()
    session_id = session_branch.removeprefix("cmoc/session/")
    state_path = root / ".cmoc" / "sessions" / f"{session_id}.json"
    state = json.loads(state_path.read_text())
    state["apply"]["state"] = "completed"
    state["apply"]["apply_branch"] = "cmoc/apply/malformed"
    state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n")

    result = runner.invoke(app, ["apply", "abandon"])

    assert result.exit_code != 0
    assert "apply worktree を特定できません。" in result.output
    state = json.loads(state_path.read_text())
    assert state["apply"]["state"] == "completed"
    assert state["apply"]["apply_branch"] == "cmoc/apply/malformed"


def test_apply_abandon_can_run_from_apply_worktree(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """apply worktree 内からの abandon は repo root へ戻して cleanup する。"""
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert runner.invoke(app, ["init"], catch_exceptions=False).exit_code == 0
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
    state_path = root / ".cmoc" / "sessions" / f"{session_id}.json"
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
    assert runner.invoke(app, ["init"], catch_exceptions=False).exit_code == 0
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
    assert runner.invoke(app, ["init"], catch_exceptions=False).exit_code == 0
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
    assert runner.invoke(app, ["init"], catch_exceptions=False).exit_code == 0
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
    state_path = root / ".cmoc" / "sessions" / f"{session_id}.json"
    state = json.loads(state_path.read_text())
    apply_branch = state["apply"]["apply_branch"]
    apply_worktree = apply_worktree_from_state(root, state)
    stale_branch = f"cmoc/apply/{session_id}/stale"
    stale_worktree = root / ".cmoc" / "worktrees" / session_id / "stale"
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
    assert "現在の apply branch は破棄対象の active apply run ではありません。" in result.output
    assert f"current_branch: {stale_branch}" in result.output
    assert f"apply_branch: {apply_branch}" in result.output
    assert apply_worktree.is_dir()
    assert run_git(root, "rev-parse", "--verify", apply_branch).returncode == 0
    state = json.loads(state_path.read_text())
    assert state["apply"]["state"] == "completed"
    assert state["apply"]["apply_branch"] == apply_branch
