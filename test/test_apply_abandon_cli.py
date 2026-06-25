from _support import (
    Path,
    app,
    apply_module,
    apply_worktree_from_state,
    json,
    main_module,
    make_repo,
    run_git,
    runner,
    subprocess,
)

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

    monkeypatch.setattr(
        main_module, "run_codex_exec", lambda parameter, **kwargs: FakeCodexResult()
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

    monkeypatch.setattr(
        main_module, "run_codex_exec", lambda parameter, **kwargs: FakeCodexResult()
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

    monkeypatch.setattr(
        main_module, "run_codex_exec", lambda parameter, **kwargs: FakeCodexResult()
    )
    assert runner.invoke(app, ["apply", "fork"], catch_exceptions=False).exit_code == 0
    session_branch = run_git(root, "branch", "--show-current").stdout.strip()
    session_id = session_branch.removeprefix("cmoc/session/")
    state_path = root / ".cmoc" / "sessions" / f"{session_id}.json"
    state = json.loads(state_path.read_text())
    apply_branch = state["apply"]["apply_branch"]
    apply_worktree = apply_worktree_from_state(root, state)
    state["apply"]["state"] = "running"
    state["apply"]["apply_process_id"] = 12345
    state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n")
    stopped: list[int] = []

    def fake_stop_apply_process(process_id: int) -> None:
        assert apply_worktree.is_dir()
        assert run_git(root, "rev-parse", "--verify", apply_branch).returncode == 0
        stopped.append(process_id)

    monkeypatch.setattr(apply_module, "stop_apply_process", fake_stop_apply_process)

    result = runner.invoke(app, ["apply", "abandon"], catch_exceptions=False)

    assert result.exit_code == 0
    assert stopped == [12345]
    assert not apply_worktree.exists()
    deleted = subprocess.run(["git", "rev-parse", "--verify", apply_branch], cwd=root)
    assert deleted.returncode != 0
    state = json.loads(state_path.read_text())
    assert state["apply"]["state"] == "ready"
    assert state["apply"]["apply_process_id"] is None


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

    monkeypatch.setattr(
        main_module, "run_codex_exec", lambda parameter, **kwargs: FakeCodexResult()
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

    result = runner.invoke(app, ["apply", "abandon"])

    assert result.exit_code != 0
    assert "実行中 apply process を特定できません。" in result.output
    assert apply_worktree.is_dir()
    remaining = subprocess.run(["git", "rev-parse", "--verify", apply_branch], cwd=root)
    assert remaining.returncode == 0
    state = json.loads(state_path.read_text())
    assert state["apply"]["state"] == "running"
    assert state["apply"]["apply_branch"] == apply_branch


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

    monkeypatch.setattr(
        main_module, "run_codex_exec", lambda parameter, **kwargs: FakeCodexResult()
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


def test_apply_abandon_rejects_stale_apply_branch(tmp_path: Path, monkeypatch) -> None:
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert runner.invoke(app, ["init"], catch_exceptions=False).exit_code == 0
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )

    class FakeCodexResult:
        output_json = {"findings": []}

    monkeypatch.setattr(
        main_module, "run_codex_exec", lambda parameter, **kwargs: FakeCodexResult()
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
