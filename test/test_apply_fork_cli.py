from _support import (
    Path,
    app,
    apply_fork_module,
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
    assert "apply_process_id" not in state["apply"]
    assert not (
        root / ".cmoc" / "state" / "apply_processes" / f"{session_id}.pid"
    ).exists()
    assert calls
    assert any(call.startswith("apply fork enumerate findings") for call in calls)


def test_apply_fork_does_not_rewrite_session_gitignore(
    tmp_path: Path, monkeypatch
) -> None:
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert runner.invoke(app, ["init"], catch_exceptions=False).exit_code == 0
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )
    (root / ".gitignore").write_text(".cmoc/\n")
    run_git(root, "add", ".gitignore")
    run_git(root, "commit", "-m", "use alternate cmoc ignore pattern")

    class FakeCodexResult:
        def __init__(self, output_json):
            self.output_json = output_json

    monkeypatch.setattr(
        main_module,
        "run_codex_exec",
        lambda parameter, **kwargs: FakeCodexResult({"findings": []}),
    )

    result = runner.invoke(
        app, ["apply", "fork", "--scope", "full"], catch_exceptions=False
    )

    assert result.exit_code == 0
    assert (root / ".gitignore").read_text() == ".cmoc/\n"
    assert run_git(root, "status", "--short").stdout.strip() == ""


def test_apply_fork_config_error_does_not_start_apply_run(
    tmp_path: Path, monkeypatch
) -> None:
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert runner.invoke(app, ["init"], catch_exceptions=False).exit_code == 0
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )
    branch = run_git(root, "branch", "--show-current").stdout.strip()
    session_id = branch.removeprefix("cmoc/session/")
    state_path = root / ".cmoc" / "sessions" / f"{session_id}.json"
    (root / ".cmoc" / "config.json").write_text("{invalid\n")

    result = runner.invoke(app, ["apply", "fork", "--scope", "full"])

    assert result.exit_code != 0
    state = json.loads(state_path.read_text())
    assert state["apply"]["state"] == "ready"
    assert "apply_process_id" not in state["apply"]
    assert not (
        root / ".cmoc" / "state" / "apply_processes" / f"{session_id}.pid"
    ).exists()
    assert run_git(root, "branch", "--list", f"cmoc/apply/{session_id}/*").stdout == ""


def test_apply_fork_can_target_and_edit_gitignore(tmp_path: Path, monkeypatch) -> None:
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert runner.invoke(app, ["init"], catch_exceptions=False).exit_code == 0
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )
    finding = {
        "title": "Update gitignore",
        "evidences": [
            {
                "path": str(root / ".gitignore"),
                "line_start": 1,
                "line_end": 1,
                "summary": "gitignore",
            }
        ],
        "oracle_requirement": "test requirement",
        "observed_implementation": "old",
        "reason": "needs update",
        "suggested_fix": "update gitignore",
    }
    target_rels_by_call: list[list[str]] = []
    current_findings = [finding]

    class FakeCodexResult:
        def __init__(self, output_json=None, output_text: str = ""):
            self.output_json = output_json
            self.output_text = output_text

    def enumerate_findings(root_arg, target, config, codex_exec, **kwargs):
        nonlocal current_findings
        target_rels_by_call.append([str(target.relative_to(root_arg))])
        current_findings = [finding] if len(target_rels_by_call) == 1 else []
        return current_findings

    def fake_run_codex_exec(parameter, **kwargs):
        purpose = kwargs["purpose"]
        if purpose == "apply fork finding application":
            (Path.cwd() / ".gitignore").write_text("/.cmoc/\n# editable\n")
            return FakeCodexResult()
        if purpose == "apply fork commit message":
            return FakeCodexResult(output_text="Update gitignore\n")
        if purpose == "apply fork change summary":
            return FakeCodexResult({"changes": []})
        raise AssertionError(purpose)

    monkeypatch.setattr(
        apply_fork_module, "enumerate_apply_findings_for_target", enumerate_findings
    )
    monkeypatch.setattr(main_module, "run_codex_exec", fake_run_codex_exec)

    result = runner.invoke(
        app, ["apply", "fork", "--scope", "full"], catch_exceptions=False
    )

    assert result.exit_code == 0
    assert ".gitignore" in target_rels_by_call[0]
    assert [".gitignore"] in target_rels_by_call
    branch = run_git(root, "branch", "--show-current").stdout.strip()
    session_id = branch.removeprefix("cmoc/session/")
    state = json.loads((root / ".cmoc" / "sessions" / f"{session_id}.json").read_text())
    assert (
        run_git(root, "show", f"{state['apply']['apply_branch']}:.gitignore").stdout
        == "/.cmoc/\n# editable\n"
    )


def test_apply_fork_target_normalization_keeps_nested_memo_directory(
    tmp_path: Path,
) -> None:
    root = make_repo(tmp_path)
    (root / "memo").mkdir()
    (root / "memo" / "root.txt").write_text("private\n")
    (root / "docs" / "memo").mkdir(parents=True)
    nested = root / "docs" / "memo" / "public.txt"
    nested.write_text("target\n")

    targets = apply_fork_module.normalize_apply_targets(
        root,
        {root / "memo" / "root.txt", nested},
    )

    assert targets == [nested.resolve()]


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
    assert "未収束: 回数上限に達したためループを終了しました。まだ所見が残っている可能性があります。" in rendered
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
    target_rels: list[str] = []

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
        if purpose == "apply fork finding application":
            (Path.cwd() / "README.md").write_text("# updated\n")
            (Path.cwd() / "INDEX.md").write_text("generated index\n")
            return FakeCodexResult(None)
        if purpose == "apply fork commit message":
            return FakeCodexResult(output_text="Update README from apply finding\n")
        if purpose == "apply fork change summary":
            return FakeCodexResult({"changes": []})
        raise AssertionError(purpose)

    monkeypatch.setattr(main_module, "run_codex_exec", fake_run_codex_exec)
    original_enumerate = apply_fork_module.enumerate_apply_findings_for_target

    def enumerate_findings(root_arg, target, config, codex_exec, **kwargs):
        target_rels.append(str(target.relative_to(root_arg)))
        return original_enumerate(root_arg, target, config, codex_exec, **kwargs)

    monkeypatch.setattr(
        apply_fork_module, "enumerate_apply_findings_for_target", enumerate_findings
    )

    result = runner.invoke(
        app, ["apply", "fork", "--scope", "full"], catch_exceptions=False
    )

    assert result.exit_code == 0
    assert enumerate_calls >= 2
    assert "README.md" in target_rels
    assert "INDEX.md" not in target_rels
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
    readme_finding = {
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
    agents_finding = {
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
    applications = 0
    calls: list[str] = []

    class FakeCodexResult:
        def __init__(self, output_json=None, output_text: str = ""):
            self.output_json = output_json
            self.output_text = output_text

    def fake_run_codex_exec(parameter, **kwargs):
        nonlocal applications
        purpose = kwargs["purpose"]
        calls.append(purpose)
        if purpose.startswith("apply fork enumerate findings"):
            return FakeCodexResult({"findings": [readme_finding, agents_finding]})
        if purpose == "apply fork finding application":
            applications += 1
            if applications == 1:
                (Path.cwd() / "README.md").write_text("# updated before error\n")
            else:
                (Path.cwd() / ".agents" / "skill.md").write_text("forbidden\n")
            return FakeCodexResult()
        if purpose == "apply fork commit message":
            return FakeCodexResult(output_text="Update README before error\n")
        if purpose == "apply fork change summary":
            raise AssertionError("error report must not call change summary")
        raise AssertionError(purpose)

    monkeypatch.setattr(main_module, "run_codex_exec", fake_run_codex_exec)

    result = runner.invoke(app, ["apply", "fork", "--scope", "full"])

    assert result.exit_code != 0
    assert "編集禁止対象" in result.output
    report_lines = [
        line for line in result.output.splitlines() if line.startswith("- report:")
    ]
    assert report_lines
    report_path = Path(report_lines[-1].split("`")[1])
    assert report_path.is_file()
    rendered = report_path.read_text()
    assert "result: error" in rendered
    assert "変更要約生成なし: 変更 path のみを機械的に記録しました。 (README.md)" in rendered
    assert "apply fork change summary" not in calls
    branch = run_git(root, "branch", "--show-current").stdout.strip()
    session_id = branch.removeprefix("cmoc/session/")
    state = json.loads((root / ".cmoc" / "sessions" / f"{session_id}.json").read_text())
    assert state["apply"]["state"] == "error"


def test_apply_fork_rolling_uses_previous_apply_oracle_snapshot_commit(
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
    (root / "oracle" / "spec.md").write_text("# changed after join\n")
    run_git(root, "add", "oracle/spec.md")
    run_git(root, "commit", "-m", "change oracle after apply join")

    class FakeCodexResult:
        def __init__(self, output_json=None):
            self.output_json = output_json

    target_rels: list[str] = []

    def enumerate_findings(root_arg, target, config, codex_exec, **kwargs):
        target_rels.append(str(target.relative_to(root_arg)))
        return []

    monkeypatch.setattr(
        apply_fork_module, "enumerate_apply_findings_for_target", enumerate_findings
    )
    monkeypatch.setattr(
        main_module,
        "run_codex_exec",
        lambda parameter, **kwargs: FakeCodexResult({"findings": []}),
    )

    result = runner.invoke(app, ["apply", "fork"], catch_exceptions=False)

    assert result.exit_code == 0
    assert target_rels == ["README.md", "oracle/spec.md"]
    assert (
        json.loads(state_path.read_text())["session"][
            "last_joined_apply_oracle_snapshot_commit"
        ]
        == oracle_snapshot_commit
    )
