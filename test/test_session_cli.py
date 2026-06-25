from _support import (
    CmocError,
    Path,
    app,
    cmoc_runtime,
    json,
    main_module,
    make_repo,
    run_git,
    runner,
    session_module,
    subprocess,
)

def test_session_fork_creates_session_branch_and_state(
    tmp_path: Path, monkeypatch
) -> None:
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    init_result = runner.invoke(app, ["init"], catch_exceptions=False)
    assert init_result.exit_code == 0

    result = runner.invoke(app, ["session", "fork"], catch_exceptions=False)

    assert result.exit_code == 0
    branch = run_git(root, "branch", "--show-current").stdout.strip()
    assert branch.startswith("cmoc/session/")
    session_id = branch.removeprefix("cmoc/session/")
    state = json.loads((root / ".cmoc" / "sessions" / f"{session_id}.json").read_text())
    assert state["session"]["state"] == "active"
    assert state["session"]["session_home_branch"] in {"master", "main"}
    assert state["apply"]["state"] == "ready"


def test_session_abandon_switches_home_and_marks_state(
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

    result = runner.invoke(app, ["session", "abandon"], catch_exceptions=False)

    assert result.exit_code == 0
    assert run_git(root, "branch", "--show-current").stdout.strip() == "master"
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
    assert "- joined_at: `None`" in result.output


def test_session_abandon_requires_existing_home_branch(
    tmp_path: Path, monkeypatch
) -> None:
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert runner.invoke(app, ["init"], catch_exceptions=False).exit_code == 0
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )
    session_branch = run_git(root, "branch", "--show-current").stdout.strip()
    home_commit = run_git(root, "rev-parse", "master").stdout.strip()
    run_git(root, "branch", "-D", "master")
    run_git(root, "tag", "master", home_commit)

    result = runner.invoke(app, ["session", "abandon"])

    assert result.exit_code != 0
    assert "completed handler" in result.output
    assert "- sub_command_log: `" in result.output
    assert "- step_execute_elapsed: `" in result.output
    assert "- elapsed: `" in result.output
    assert "- quota_wait: `" in result.output
    assert "- returncode: `1`" in result.output
    assert run_git(root, "branch", "--show-current").stdout.strip() == session_branch
    assert "session home branch が存在しません。" in result.stderr
    assert "session home branch が存在しません。" not in result.stdout
    assert (
        subprocess.run(
            ["git", "rev-parse", "--verify", session_branch], cwd=root
        ).returncode
        == 0
    )


def test_session_abandon_rolls_back_state_and_branch_on_cleanup_failure(
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
    original_run_git = session_module.run_git

    def fake_run_git(args, cwd, check=True):
        if args == ["branch", "-D", session_branch]:
            raise CmocError("delete failed", ["next"], "branch delete failed")
        return original_run_git(args, cwd, check)

    monkeypatch.setattr(session_module, "run_git", fake_run_git)

    result = runner.invoke(app, ["session", "abandon"])

    assert result.exit_code != 0
    assert "session abandon の cleanup に失敗しました。" in result.output
    assert "`cmoc session abandon` を再実行してください。" in result.output
    assert run_git(root, "branch", "--show-current").stdout.strip() == session_branch
    assert (
        subprocess.run(
            ["git", "rev-parse", "--verify", session_branch], cwd=root
        ).returncode
        == 0
    )
    state = json.loads(state_path.read_text())
    assert state["session"]["state"] == "active"

def test_session_join_resolves_conflict_with_codex(tmp_path: Path, monkeypatch) -> None:
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert runner.invoke(app, ["init"], catch_exceptions=False).exit_code == 0
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )
    session_branch = run_git(root, "branch", "--show-current").stdout.strip()
    (root / "README.md").write_text("session change\n")
    run_git(root, "add", "README.md")
    run_git(root, "commit", "-m", "session change")
    run_git(root, "switch", "master")
    (root / "README.md").write_text("home change\n")
    run_git(root, "add", "README.md")
    run_git(root, "commit", "-m", "home change")
    run_git(root, "switch", session_branch)
    calls: list[str] = []

    class FakeCodexResult:
        output_json = None

    def fake_run_codex_exec(parameter, **kwargs):
        calls.append(kwargs["purpose"])
        (root / "README.md").write_text("resolved change\n")
        return FakeCodexResult()

    monkeypatch.setattr(main_module, "run_codex_exec", fake_run_codex_exec)

    result = runner.invoke(app, ["session", "join"], catch_exceptions=False)

    assert result.exit_code == 0
    assert run_git(root, "branch", "--show-current").stdout.strip() == "master"
    assert (root / "README.md").read_text() == "resolved change\n"
    assert calls == ["session join conflict resolution"]


def test_session_join_stages_delete_conflict_resolution(
    tmp_path: Path, monkeypatch
) -> None:
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert runner.invoke(app, ["init"], catch_exceptions=False).exit_code == 0
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )
    session_branch = run_git(root, "branch", "--show-current").stdout.strip()
    (root / "README.md").unlink()
    run_git(root, "add", "README.md")
    run_git(root, "commit", "-m", "session deletes readme")
    run_git(root, "switch", "master")
    (root / "README.md").write_text("home change\n")
    run_git(root, "add", "README.md")
    run_git(root, "commit", "-m", "home changes readme")
    run_git(root, "switch", session_branch)

    class FakeCodexResult:
        output_json = None

    def fake_run_codex_exec(parameter, **kwargs):
        (root / "README.md").unlink()
        return FakeCodexResult()

    monkeypatch.setattr(main_module, "run_codex_exec", fake_run_codex_exec)

    result = runner.invoke(app, ["session", "join"], catch_exceptions=False)

    assert result.exit_code == 0
    assert run_git(root, "branch", "--show-current").stdout.strip() == "master"
    assert not (root / "README.md").exists()
    assert run_git(root, "diff", "--name-only", "--diff-filter=U").stdout == ""


def test_session_join_warns_when_session_branch_cannot_be_deleted(
    tmp_path: Path, monkeypatch
) -> None:
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert runner.invoke(app, ["init"], catch_exceptions=False).exit_code == 0
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )
    session_branch = run_git(root, "branch", "--show-current").stdout.strip()
    original_run_git = main_module.run_git

    def fake_run_git(args, cwd, check=True):
        if args == ["branch", "-d", session_branch]:
            return cmoc_runtime.CommandResult(1, "", "branch is checked out elsewhere")
        return original_run_git(args, cwd, check=check)

    monkeypatch.setattr(main_module, "run_git", fake_run_git)

    result = runner.invoke(app, ["session", "join"], catch_exceptions=False)

    assert result.exit_code == 0
    assert run_git(root, "branch", "--show-current").stdout.strip() == "master"
    assert (
        subprocess.run(
            ["git", "rev-parse", "--verify", session_branch], cwd=root
        ).returncode
        == 0
    )
    assert "- deleted_session_branch: `False`" in result.output
    assert f"session branch was not deleted: {session_branch}" in result.output
