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

def test_apply_join_removes_apply_worktree_and_resets_state(
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

    result = runner.invoke(app, ["apply", "join"], catch_exceptions=False)
    join_commit = run_git(root, "rev-parse", "HEAD").stdout.strip()

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
    assert state["session"]["last_joined_apply_join_commit"] == join_commit
    report_line = [
        line for line in result.output.splitlines() if line.startswith("- report:")
    ][-1]
    report_path = Path(report_line.split("`")[1])
    assert report_path.is_file()
    assert "# cmoc apply join report" in report_path.read_text()


def test_apply_join_can_run_from_apply_worktree(tmp_path: Path, monkeypatch) -> None:
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

    result = runner.invoke(app, ["apply", "join"], catch_exceptions=False)
    join_commit = run_git(root, "rev-parse", "HEAD").stdout.strip()

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
    assert state["session"]["last_joined_apply_join_commit"] == join_commit
    assert "- cleanup_reachable: `True`" in result.output
    assert "  - none" in result.output

def test_apply_join_from_apply_worktree_requires_clean_apply_worktree(
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
    assert "git 未コミット差分が存在します。" in result.stderr
    assert "git 未コミット差分が存在します。" not in result.stdout


def test_apply_join_from_session_requires_clean_apply_worktree(
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
    assert "git 未コミット差分が存在します。" in result.output


def test_apply_join_reports_unexpected_apply_diff_and_force_reverts(
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
    apply_worktree = apply_worktree_from_state(root, state)
    (apply_worktree / "oracle" / "spec.md").write_text("# changed oracle in apply\n")
    run_git(apply_worktree, "add", "oracle/spec.md")
    run_git(apply_worktree, "commit", "-m", "unexpected oracle change")

    normal = runner.invoke(app, ["apply", "join"], catch_exceptions=False)

    assert normal.exit_code == 1
    assert "想定外差分" in normal.output
    forced = runner.invoke(
        app, ["apply", "join", "--force-resolve"], catch_exceptions=False
    )
    assert forced.exit_code == 0
    assert (root / "oracle" / "spec.md").read_text() == "# spec\n"


def test_apply_join_treats_gitignore_change_as_unexpected_apply_diff(
    tmp_path: Path,
    monkeypatch,
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
    state_path = (
        root
        / ".cmoc"
        / "sessions"
        / f"{run_git(root, 'branch', '--show-current').stdout.strip().removeprefix('cmoc/session/')}.json"
    )
    state = json.loads(state_path.read_text())
    apply_worktree = apply_worktree_from_state(root, state)
    original_gitignore = (apply_worktree / ".gitignore").read_text()
    (apply_worktree / ".gitignore").write_text(original_gitignore + "# unexpected\n")
    run_git(apply_worktree, "add", ".gitignore")
    run_git(apply_worktree, "commit", "-m", "unexpected gitignore change")

    normal = runner.invoke(app, ["apply", "join"], catch_exceptions=False)

    assert normal.exit_code == 1
    assert "想定外差分" in normal.output
    assert ".gitignore" in normal.output
    forced = runner.invoke(
        app, ["apply", "join", "--force-resolve"], catch_exceptions=False
    )
    assert forced.exit_code == 0
    assert (root / ".gitignore").read_text() == original_gitignore


def test_apply_join_reports_unresolved_non_index_conflict(
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
