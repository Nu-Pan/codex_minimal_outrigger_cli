from _support import (
    AgentCallParameter,
    FileAccessMode,
    ModelClass,
    Path,
    ReasoningEffort,
    app,
    cmoc_runtime,
    main_module,
    make_repo,
    run_git,
    runner,
    subprocess,
    threading,
    time,
)

def test_resolve_index_conflicts_deletes_index_and_commits(tmp_path: Path) -> None:
    root = make_repo(tmp_path)
    (root / "INDEX.md").write_text("base\n")
    run_git(root, "add", "INDEX.md")
    run_git(root, "commit", "-m", "add index")
    run_git(root, "switch", "-c", "side")
    (root / "INDEX.md").write_text("side\n")
    run_git(root, "add", "INDEX.md")
    run_git(root, "commit", "-m", "side index")
    run_git(root, "switch", "master")
    (root / "INDEX.md").write_text("master\n")
    run_git(root, "add", "INDEX.md")
    run_git(root, "commit", "-m", "master index")
    merge = subprocess.run(
        ["git", "merge", "--no-ff", "side"], cwd=root, text=True, capture_output=True
    )
    assert merge.returncode != 0

    resolved = main_module.resolve_index_conflicts(root)

    assert resolved is True
    assert not (root / "INDEX.md").exists()
    assert (
        subprocess.run(
            ["git", "diff", "--name-only", "--diff-filter=U"],
            cwd=root,
            text=True,
            capture_output=True,
        ).stdout.strip()
        == ""
    )
    assert "Merge branch 'side'" in run_git(root, "log", "-1", "--pretty=%B").stdout

def test_indexing_uses_codex_index_entry_builder_and_commits(
    tmp_path: Path, monkeypatch
) -> None:
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert runner.invoke(app, ["init"], catch_exceptions=False).exit_code == 0
    calls: list[str] = []

    class FakeCodexResult:
        output_json = {
            "summary": ["generated summary"],
            "read_this_when": ["generated read condition"],
            "do_not_read_this_when": ["generated skip condition"],
        }

    def fake_run_codex_exec(parameter, **kwargs):
        calls.append(kwargs["purpose"])
        assert parameter.structured_output_schema_path.name == "index_entry.json"
        return FakeCodexResult()

    monkeypatch.setattr(main_module, "run_codex_exec", fake_run_codex_exec)

    result = runner.invoke(app, ["indexing"], catch_exceptions=False)

    assert result.exit_code == 0
    assert calls
    root_index = root / "INDEX.md"
    assert root_index.is_file()
    rendered = root_index.read_text()
    assert "generated summary" in rendered
    assert "generated read condition" in rendered
    assert "generated skip condition" in rendered
    assert run_git(root, "status", "--short").stdout.strip() == ""
    assert "cmoc indexing" in run_git(root, "log", "--oneline", "-1").stdout


def test_indexing_targets_current_linked_worktree(
    tmp_path: Path, monkeypatch
) -> None:
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert runner.invoke(app, ["init"], catch_exceptions=False).exit_code == 0
    main_head = run_git(root, "rev-parse", "HEAD").stdout.strip()
    linked = root / ".cmoc" / "worktrees" / "indexing"
    run_git(root, "worktree", "add", "-b", "linked-indexing", str(linked), "HEAD")

    class FakeCodexResult:
        output_json = {
            "summary": ["linked summary"],
            "read_this_when": ["linked read condition"],
            "do_not_read_this_when": ["linked skip condition"],
        }

    monkeypatch.setattr(
        main_module, "run_codex_exec", lambda parameter, **kwargs: FakeCodexResult()
    )
    monkeypatch.chdir(linked)

    result = runner.invoke(app, ["indexing"], catch_exceptions=False)

    assert result.exit_code == 0
    assert (linked / "INDEX.md").is_file()
    assert not (root / "INDEX.md").exists()
    assert run_git(linked, "log", "-1", "--pretty=%s").stdout.strip() == "cmoc indexing"
    assert run_git(root, "rev-parse", "HEAD").stdout.strip() == main_head
    assert run_git(linked, "status", "--short").stdout.strip() == ""


def test_indexing_skips_codex_when_existing_hashes_are_fresh(
    tmp_path: Path, monkeypatch
) -> None:
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert runner.invoke(app, ["init"], catch_exceptions=False).exit_code == 0

    class FakeCodexResult:
        output_json = {
            "summary": ["generated summary"],
            "read_this_when": ["generated read condition"],
            "do_not_read_this_when": ["generated skip condition"],
        }

    monkeypatch.setattr(
        main_module, "run_codex_exec", lambda parameter, **kwargs: FakeCodexResult()
    )
    first = runner.invoke(app, ["indexing"], catch_exceptions=False)
    assert first.exit_code == 0
    root_index_before = (root / "INDEX.md").read_text()
    head_before = run_git(root, "rev-parse", "HEAD").stdout.strip()

    calls: list[str] = []

    def fail_if_called(parameter, **kwargs):
        calls.append(kwargs["purpose"])
        raise AssertionError("fresh INDEX.md should not require Codex")

    monkeypatch.setattr(main_module, "run_codex_exec", fail_if_called)
    second = runner.invoke(app, ["indexing"], catch_exceptions=False)

    assert second.exit_code == 0
    assert calls == []
    assert (root / "INDEX.md").read_text() == root_index_before
    assert run_git(root, "rev-parse", "HEAD").stdout.strip() == head_before
    assert run_git(root, "status", "--short").stdout.strip() == ""


def test_update_indexes_regenerates_malformed_fresh_hash_entry(
    tmp_path: Path, monkeypatch
) -> None:
    root = make_repo(tmp_path)
    cmoc_runtime.sync_config(root)
    readme = root / "README.md"
    digest = main_module.index_target_hash(root, readme)
    (root / "INDEX.md").write_text(
        "\n".join(
            [
                "# `README.md`",
                "",
                "## hash",
                f"- {digest}",
                "",
            ]
        )
    )

    calls: list[Path] = []

    def fake_build_index_entry(
        update_root: Path, path: Path, digest: str | None = None
    ) -> str:
        calls.append(path)
        return main_module.render_index_entry(
            update_root,
            path,
            {
                "summary": [f"generated {path.name}"],
                "read_this_when": [f"read {path.name}"],
                "do_not_read_this_when": [f"skip {path.name}"],
            },
            digest=digest,
        ).rstrip()

    monkeypatch.setattr(main_module, "build_index_entry", fake_build_index_entry)

    updated = main_module.update_indexes(root)

    assert root / "INDEX.md" in updated
    assert readme in calls
    rendered = (root / "INDEX.md").read_text()
    assert "generated README.md" in rendered
    assert "## Summary" in rendered
    assert "## Read this when" in rendered
    assert "## Do not read this when" in rendered


def test_update_indexes_generates_sibling_entries_in_parallel(
    tmp_path: Path, monkeypatch
) -> None:
    root = make_repo(tmp_path)
    docs = root / "docs"
    docs.mkdir()
    (docs / "a.txt").write_text("a\n")
    (docs / "b.txt").write_text("b\n")
    cmoc_runtime.sync_config(root)
    active = 0
    max_active = 0
    lock = threading.Lock()

    def fake_build_index_entry(
        update_root: Path, path: Path, digest: str | None = None
    ) -> str:
        nonlocal active, max_active
        if path.parent == docs:
            with lock:
                active += 1
                max_active = max(max_active, active)
            time.sleep(0.05)
            with lock:
                active -= 1
        return main_module.render_index_entry(
            update_root,
            path,
            {
                "summary": [path.name],
                "read_this_when": [path.name],
                "do_not_read_this_when": [path.name],
            },
            digest=digest,
        ).rstrip()

    monkeypatch.setattr(main_module, "build_index_entry", fake_build_index_entry)

    updated = main_module.update_indexes(root)

    assert docs / "INDEX.md" in updated
    assert max_active >= 2


def test_update_indexes_indexes_nested_memo_directory(tmp_path: Path, monkeypatch) -> None:
    root = make_repo(tmp_path)
    root_memo = root / "memo"
    root_memo_child = root_memo / "child"
    nested_memo = root / "docs" / "memo"
    root_memo_child.mkdir(parents=True)
    nested_memo.mkdir(parents=True)
    (root_memo / "private.txt").write_text("private\n")
    (root_memo_child / "deeper.txt").write_text("deeper\n")
    (nested_memo / "note.txt").write_text("note\n")
    cmoc_runtime.sync_config(root)

    def fake_build_index_entry(
        update_root: Path, path: Path, digest: str | None = None
    ) -> str:
        return main_module.render_index_entry(
            update_root,
            path,
            {
                "summary": [path.name],
                "read_this_when": [path.name],
                "do_not_read_this_when": [path.name],
            },
            digest=digest,
        ).rstrip()

    monkeypatch.setattr(main_module, "build_index_entry", fake_build_index_entry)

    updated = main_module.update_indexes(root)

    assert root_memo / "INDEX.md" not in updated
    assert not (root_memo / "INDEX.md").exists()
    assert root_memo_child / "INDEX.md" not in updated
    assert not (root_memo_child / "INDEX.md").exists()
    assert nested_memo / "INDEX.md" in updated
    assert (nested_memo / "INDEX.md").is_file()
    assert "# `memo`" in (root / "docs" / "INDEX.md").read_text()


def test_command_codex_call_runs_indexing_preflight(
    tmp_path: Path, monkeypatch
) -> None:
    root = make_repo(tmp_path)
    index_path = root / "INDEX.md"
    parameter = AgentCallParameter(
        ModelClass.EFFICIENCY,
        ReasoningEffort.LOW,
        FileAccessMode.READONLY,
        "prompt",
        None,
    )
    events: list[str] = []

    def fake_update_indexes(update_root: Path) -> list[Path]:
        events.append("indexing")
        assert update_root == root
        index_path.write_text("# generated\n")
        return [index_path]

    class FakeCodexResult:
        output_json = None

    def fake_runtime_run_codex_exec(call_parameter, **kwargs):
        events.append("codex")
        assert call_parameter == parameter
        return FakeCodexResult()

    monkeypatch.setattr(main_module, "update_indexes", fake_update_indexes)
    monkeypatch.setattr(
        main_module, "runtime_run_codex_exec", fake_runtime_run_codex_exec
    )

    result = main_module.run_codex_exec(
        parameter, root=root, purpose="apply fork refine findings"
    )

    assert isinstance(result, FakeCodexResult)
    assert events == ["indexing", "codex"]
    assert run_git(root, "log", "-1", "--pretty=%s").stdout.strip() == "cmoc indexing"
    assert run_git(root, "status", "--short").stdout.strip() == ""


def test_command_tui_codex_call_runs_indexing_preflight(
    tmp_path: Path, monkeypatch
) -> None:
    root = make_repo(tmp_path)
    index_path = root / "INDEX.md"
    parameter = AgentCallParameter(
        ModelClass.EFFICIENCY,
        ReasoningEffort.LOW,
        FileAccessMode.READONLY,
        "prompt",
        None,
    )
    events: list[str] = []

    def fake_update_indexes(update_root: Path) -> list[Path]:
        events.append("indexing")
        assert update_root == root
        index_path.write_text("# generated\n")
        return [index_path]

    def fake_runtime_run_codex_tui(call_parameter, **kwargs):
        events.append("codex")
        assert call_parameter == parameter

    monkeypatch.setattr(main_module, "update_indexes", fake_update_indexes)
    monkeypatch.setattr(
        main_module, "runtime_run_codex_tui", fake_runtime_run_codex_tui
    )

    main_module.run_codex_tui(parameter, root=root, purpose="tui codex")

    assert events == ["indexing", "codex"]
    assert run_git(root, "log", "-1", "--pretty=%s").stdout.strip() == "cmoc indexing"
    assert run_git(root, "status", "--short").stdout.strip() == ""


def test_command_codex_call_skips_indexing_for_index_entry_and_conflict_resolution(
    tmp_path: Path,
    monkeypatch,
) -> None:
    root = make_repo(tmp_path)
    parameter = AgentCallParameter(
        ModelClass.EFFICIENCY,
        ReasoningEffort.LOW,
        FileAccessMode.READONLY,
        "prompt",
        None,
    )
    calls: list[str] = []

    class FakeCodexResult:
        output_json = None

    def fail_update_indexes(update_root: Path) -> list[Path]:
        raise AssertionError("indexing preflight should be skipped")

    def fake_runtime_run_codex_exec(call_parameter, **kwargs):
        calls.append(kwargs["purpose"])
        return FakeCodexResult()

    monkeypatch.setattr(main_module, "update_indexes", fail_update_indexes)
    monkeypatch.setattr(
        main_module, "runtime_run_codex_exec", fake_runtime_run_codex_exec
    )

    main_module.run_codex_exec(
        parameter, root=root, purpose="indexing index entry for README.md"
    )
    main_module.run_codex_exec(
        parameter, root=root, purpose="session join conflict resolution"
    )

    assert calls == [
        "indexing index entry for README.md",
        "session join conflict resolution",
    ]
