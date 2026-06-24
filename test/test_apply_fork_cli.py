from _support import (
    Path,
    app,
    apply_worktree_from_state,
    json,
    main_module,
    make_repo,
    run_git,
    runner,
)

def test_apply_fork_runs_codex_loop_and_updates_state(
    tmp_path: Path, monkeypatch
) -> None:
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    init_result = runner.invoke(app, ["init"], catch_exceptions=False)
    assert init_result.exit_code == 0
    fork_result = runner.invoke(app, ["session", "fork"], catch_exceptions=False)
    assert fork_result.exit_code == 0
    calls: list[str] = []

    class FakeCodexResult:
        def __init__(self, output_json):
            self.output_json = output_json

    def fake_run_codex_exec(parameter, **kwargs):
        calls.append(kwargs["purpose"])
        if parameter.structured_output_schema_path is None:
            return FakeCodexResult(None)
        return FakeCodexResult({"findings": []})

    monkeypatch.setattr(main_module, "run_codex_exec", fake_run_codex_exec)

    result = runner.invoke(
        app, ["apply", "fork", "--scope", "full"], catch_exceptions=False
    )

    assert result.exit_code == 0
    branch = run_git(root, "branch", "--show-current").stdout.strip()
    assert branch.startswith("cmoc/session/")
    session_id = branch.removeprefix("cmoc/session/")
    state = json.loads((root / ".cmoc" / "sessions" / f"{session_id}.json").read_text())
    assert state["apply"]["state"] == "completed"
    assert state["apply"]["apply_branch"].startswith(f"cmoc/apply/{session_id}/")
    run_id = state["apply"]["apply_branch"].removeprefix(f"cmoc/apply/{session_id}/")
    apply_worktree = apply_worktree_from_state(root, state)
    assert apply_worktree == root / ".cmoc" / "worktrees" / session_id / run_id
    assert apply_worktree.is_dir()
    assert not (root / ".cmoc" / "worktrees" / "apply").exists()
    assert "apply_worktree" not in state["apply"]
    assert calls
    assert any(call.startswith("apply fork enumerate findings") for call in calls)
    assert "apply fork refine findings" in calls


def test_apply_fork_writes_report_with_change_summary(
    tmp_path: Path, monkeypatch
) -> None:
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert runner.invoke(app, ["init"], catch_exceptions=False).exit_code == 0
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )
    finding = {
        "title": "Update README",
        "evidences": [
            {
                "path": str(root / "README.md"),
                "line_start": 1,
                "line_end": 1,
                "summary": "readme",
            }
        ],
        "oracle_requirement": "test requirement",
        "observed_implementation": "old",
        "reason": "needs update",
        "suggested_fix": "update readme",
    }
    calls: list[str] = []

    class FakeCodexResult:
        def __init__(self, output_json=None, output_text: str = ""):
            self.output_json = output_json
            self.output_text = output_text

    def fake_run_codex_exec(parameter, **kwargs):
        calls.append(kwargs["purpose"])
        schema = (
            parameter.structured_output_schema_path.name
            if parameter.structured_output_schema_path
            else None
        )
        if kwargs["purpose"].startswith("apply fork enumerate findings"):
            return FakeCodexResult({"findings": [finding]})
        if kwargs["purpose"] == "apply fork refine findings":
            return FakeCodexResult({"findings": [finding]})
        if kwargs["purpose"] == "apply fork finding application":
            (Path.cwd() / "README.md").write_text("# updated\n")
            return FakeCodexResult(None)
        if kwargs["purpose"] == "apply fork commit message":
            return FakeCodexResult(output_text="Update README from apply finding\n")
        if schema == "change_summary.json":
            return FakeCodexResult(
                {
                    "changes": [
                        {
                            "category": "ドキュメント",
                            "summary": "README を更新した",
                            "changed_paths": ["README.md"],
                        }
                    ]
                }
            )
        raise AssertionError(kwargs["purpose"])

    monkeypatch.setattr(main_module, "run_codex_exec", fake_run_codex_exec)

    result = runner.invoke(
        app, ["apply", "fork", "--scope", "full"], catch_exceptions=False
    )

    assert result.exit_code == 2
    report_lines = [
        line for line in result.output.splitlines() if line.startswith("- report:")
    ]
    assert report_lines
    report_path = Path(report_lines[-1].split("`")[1])
    assert report_path.is_file()
    rendered = report_path.read_text()
    assert "result: unconverged" in rendered
    assert "# cmoc apply fork report" in rendered
    assert "## Finding Count" in rendered
    assert "ドキュメント: README を更新した (README.md)" in rendered
    assert "apply fork change summary" in calls
    assert "apply fork commit message" in calls
    assert "- returncode: `2`" in result.output
    branch = run_git(root, "branch", "--show-current").stdout.strip()
    session_id = branch.removeprefix("cmoc/session/")
    state = json.loads((root / ".cmoc" / "sessions" / f"{session_id}.json").read_text())
    apply_branch = state["apply"]["apply_branch"]
    assert (
        run_git(root, "log", "-1", "--pretty=%s", apply_branch).stdout.strip()
        == "Update README from apply finding"
    )


def test_apply_fork_rechecks_dirty_files_until_converged(
    tmp_path: Path, monkeypatch
) -> None:
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert runner.invoke(app, ["init"], catch_exceptions=False).exit_code == 0
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )
    finding = {
        "title": "Update README",
        "evidences": [
            {
                "path": str(root / "README.md"),
                "line_start": 1,
                "line_end": 1,
                "summary": "readme",
            }
        ],
        "oracle_requirement": "test requirement",
        "observed_implementation": "old",
        "reason": "needs update",
        "suggested_fix": "update readme",
    }
    enumerate_calls = 0

    class FakeCodexResult:
        def __init__(self, output_json=None, output_text: str = ""):
            self.output_json = output_json
            self.output_text = output_text

    def fake_run_codex_exec(parameter, **kwargs):
        nonlocal enumerate_calls
        purpose = kwargs["purpose"]
        if purpose.startswith("apply fork enumerate findings"):
            enumerate_calls += 1
            return FakeCodexResult(
                {"findings": [finding] if enumerate_calls == 1 else []}
            )
        if purpose == "apply fork refine findings":
            return FakeCodexResult(
                {"findings": [finding] if enumerate_calls == 1 else []}
            )
        if purpose == "apply fork finding application":
            (Path.cwd() / "README.md").write_text("# updated\n")
            return FakeCodexResult(None)
        if purpose == "apply fork commit message":
            return FakeCodexResult(output_text="Update README from apply finding\n")
        if purpose == "apply fork change summary":
            return FakeCodexResult({"changes": []})
        raise AssertionError(purpose)

    monkeypatch.setattr(main_module, "run_codex_exec", fake_run_codex_exec)

    result = runner.invoke(
        app, ["apply", "fork", "--scope", "full"], catch_exceptions=False
    )

    assert result.exit_code == 0
    assert enumerate_calls >= 2
    report_line = [
        line for line in result.output.splitlines() if line.startswith("- report:")
    ][-1]
    report_path = Path(report_line.split("`")[1])
    assert "result: converged" in report_path.read_text()


def test_apply_fork_rejects_forbidden_agents_diff(tmp_path: Path, monkeypatch) -> None:
    root = make_repo(tmp_path)
    (root / ".agents").mkdir()
    (root / ".agents" / "skill.md").write_text("original\n")
    run_git(root, "add", ".agents/skill.md")
    run_git(root, "commit", "-m", "add agents")
    monkeypatch.chdir(root)
    assert runner.invoke(app, ["init"], catch_exceptions=False).exit_code == 0
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )
    finding = {
        "title": "Bad agents edit",
        "evidences": [
            {
                "path": str(root / "README.md"),
                "line_start": 1,
                "line_end": 1,
                "summary": "readme",
            }
        ],
        "oracle_requirement": "test requirement",
        "observed_implementation": "old",
        "reason": "needs update",
        "suggested_fix": "update agents",
    }

    class FakeCodexResult:
        def __init__(self, output_json=None, output_text: str = ""):
            self.output_json = output_json
            self.output_text = output_text

    def fake_run_codex_exec(parameter, **kwargs):
        purpose = kwargs["purpose"]
        if purpose.startswith("apply fork enumerate findings"):
            return FakeCodexResult({"findings": [finding]})
        if purpose == "apply fork refine findings":
            return FakeCodexResult({"findings": [finding]})
        if purpose == "apply fork finding application":
            (Path.cwd() / ".agents" / "skill.md").write_text("forbidden\n")
            return FakeCodexResult()
        raise AssertionError(purpose)

    monkeypatch.setattr(main_module, "run_codex_exec", fake_run_codex_exec)

    result = runner.invoke(app, ["apply", "fork", "--scope", "full"])

    assert result.exit_code != 0
    assert "編集禁止対象" in result.output
    branch = run_git(root, "branch", "--show-current").stdout.strip()
    session_id = branch.removeprefix("cmoc/session/")
    state = json.loads((root / ".cmoc" / "sessions" / f"{session_id}.json").read_text())
    assert state["apply"]["state"] == "error"

def test_apply_fork_rolling_uses_previous_apply_join_commit(
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
    apply_branch = f"cmoc/apply/{session_id}/manual"
    apply_worktree = root / ".cmoc" / "worktrees" / session_id / "manual"
    oracle_snapshot_commit = run_git(root, "rev-parse", "HEAD").stdout.strip()
    run_git(root, "worktree", "add", "-b", apply_branch, str(apply_worktree), "HEAD")
    (apply_worktree / "README.md").write_text("# updated by apply\n")
    run_git(apply_worktree, "add", "README.md")
    run_git(apply_worktree, "commit", "-m", "update readme from apply")
    state = json.loads(state_path.read_text())
    state["apply"] = {
        "state": "completed",
        "apply_branch": apply_branch,
        "oracle_snapshot_commit": oracle_snapshot_commit,
    }
    state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n")

    assert (
        runner.invoke(app, ["apply", "join"], catch_exceptions=False).exit_code == 0
    )
    join_commit = run_git(root, "rev-parse", "HEAD").stdout.strip()
    (root / "oracle" / "spec.md").write_text("# changed after join\n")
    run_git(root, "add", "oracle/spec.md")
    run_git(root, "commit", "-m", "change oracle after apply join")

    class FakeCodexResult:
        def __init__(self, output_json=None):
            self.output_json = output_json

    target_rels: list[str] = []

    def enumerate_findings(root_arg, targets, config, **kwargs):
        target_rels.extend(
            sorted(str(path.relative_to(root_arg)) for path in targets)
        )
        return []

    monkeypatch.setattr(
        main_module, "enumerate_apply_findings_for_targets", enumerate_findings
    )
    monkeypatch.setattr(
        main_module,
        "run_codex_exec",
        lambda parameter, **kwargs: FakeCodexResult({"findings": []}),
    )

    result = runner.invoke(app, ["apply", "fork"], catch_exceptions=False)

    assert result.exit_code == 0
    assert target_rels == ["oracle/spec.md"]
    assert (
        json.loads(state_path.read_text())["session"]["last_joined_apply_commit"]
        == join_commit
    )
