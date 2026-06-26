from _support import (
    Path,
    app,
    apply_abandon_module,
    apply_fork_module,
    apply_worktree_from_state,
    json,
    make_repo,
    run_git,
    runner,
    subprocess,
)
from sub_commands.apply import _runtime as apply_runtime


def setup_linked_session_apply(root: Path, monkeypatch) -> tuple[Path, Path, str, Path]:
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
    tmp_path: Path, monkeypatch
) -> None:
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert runner.invoke(app, ["init"], catch_exceptions=False).exit_code == 0
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )

    class FakeCodexResult:
        output_json = {"findings": []}

    monkeypatch.setattr(apply_fork_module, "run_codex_exec", lambda parameter, **kwargs: FakeCodexResult()
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
    tmp_path: Path, monkeypatch
) -> None:
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert runner.invoke(app, ["init"], catch_exceptions=False).exit_code == 0
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )

    class FakeCodexResult:
        output_json = {"findings": []}

    monkeypatch.setattr(apply_fork_module, "run_codex_exec", lambda parameter, **kwargs: FakeCodexResult()
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
    tmp_path: Path, monkeypatch
) -> None:
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert runner.invoke(app, ["init"], catch_exceptions=False).exit_code == 0
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )

    class FakeCodexResult:
        output_json = {"findings": []}

    monkeypatch.setattr(apply_fork_module, "run_codex_exec", lambda parameter, **kwargs: FakeCodexResult()
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


def test_stop_apply_process_treats_raced_exit_as_stopped(monkeypatch) -> None:
    sent: list[int] = []

    def fake_send_signal(process_fd: int, process_id: int, sig) -> None:
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


def test_send_process_signal_ignores_already_exited_process(monkeypatch) -> None:
    def fake_pidfd_send_signal(process_fd: int, sig) -> None:
        raise ProcessLookupError

    monkeypatch.setattr(
        apply_runtime.signal, "pidfd_send_signal", fake_pidfd_send_signal
    )

    apply_runtime.send_process_signal(10, 12345, apply_runtime.signal.SIGTERM)


def test_stop_apply_process_does_not_signal_reused_pid(monkeypatch) -> None:
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
    tmp_path: Path, monkeypatch
) -> None:
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert runner.invoke(app, ["init"], catch_exceptions=False).exit_code == 0
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )

    class FakeCodexResult:
        output_json = {"findings": []}

    monkeypatch.setattr(apply_fork_module, "run_codex_exec", lambda parameter, **kwargs: FakeCodexResult()
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
    tmp_path: Path, monkeypatch
) -> None:
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


def test_apply_abandon_can_run_from_apply_worktree(tmp_path: Path, monkeypatch) -> None:
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert runner.invoke(app, ["init"], catch_exceptions=False).exit_code == 0
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )

    class FakeCodexResult:
        output_json = {"findings": []}

    monkeypatch.setattr(apply_fork_module, "run_codex_exec", lambda parameter, **kwargs: FakeCodexResult()
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
    tmp_path: Path, monkeypatch
) -> None:
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert runner.invoke(app, ["init"], catch_exceptions=False).exit_code == 0
    linked, state_path, apply_branch, apply_worktree = setup_linked_session_apply(
        root, monkeypatch
    )
    (linked / "README.md").write_text("# dirty\n")

    result = runner.invoke(app, ["apply", "abandon"])

    assert result.exit_code != 0
    assert "git 未コミット差分が存在します。" in result.output
    assert apply_worktree.is_dir()
    assert run_git(root, "rev-parse", "--verify", apply_branch).returncode == 0
    state = json.loads(state_path.read_text())
    assert state["apply"]["state"] == "completed"
    assert state["apply"]["apply_branch"] == apply_branch


def test_apply_abandon_from_linked_apply_worktree_uses_repo_state(
    tmp_path: Path, monkeypatch
) -> None:
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


def test_apply_abandon_rejects_stale_apply_branch(tmp_path: Path, monkeypatch) -> None:
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert runner.invoke(app, ["init"], catch_exceptions=False).exit_code == 0
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )

    class FakeCodexResult:
        output_json = {"findings": []}

    monkeypatch.setattr(apply_fork_module, "run_codex_exec", lambda parameter, **kwargs: FakeCodexResult()
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
