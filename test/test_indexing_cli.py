import multiprocessing

import pytest

from _support import (
    AgentCallParameter,
    FileAccessMode,
    ModelClass,
    Path,
    ReasoningEffort,
    app,
    apply_module,
    cmoc_runtime,
    codex_preflight_module,
    current_branch,
    indexing_module,
    make_repo,
    run_git,
    runner,
    subprocess,
    threading,
    time,
)


def hold_indexing_lock(lock_path: Path, ready, release) -> None:
    import fcntl

    lock_path.parent.mkdir(parents=True, exist_ok=True)
    with lock_path.open("a+") as lock_file:
        fcntl.flock(lock_file.fileno(), fcntl.LOCK_EX)
        ready.send(True)
        release.recv()
        fcntl.flock(lock_file.fileno(), fcntl.LOCK_UN)

def test_resolve_index_conflicts_deletes_index_and_commits(tmp_path: Path) -> None:
    root = make_repo(tmp_path)
    home_branch = current_branch(root)
    (root / "INDEX.md").write_text("base\n")
    run_git(root, "add", "INDEX.md")
    run_git(root, "commit", "-m", "add index")
    run_git(root, "switch", "-c", "side")
    (root / "INDEX.md").write_text("side\n")
    run_git(root, "add", "INDEX.md")
    run_git(root, "commit", "-m", "side index")
    run_git(root, "switch", home_branch)
    (root / "INDEX.md").write_text("home\n")
    run_git(root, "add", "INDEX.md")
    run_git(root, "commit", "-m", "home index")
    merge = subprocess.run(
        ["git", "merge", "--no-ff", "side"], cwd=root, text=True, capture_output=True
    )
    assert merge.returncode != 0

    resolved = apply_module.resolve_index_conflicts(root)

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

    monkeypatch.setattr(indexing_module, "run_codex_exec", fake_run_codex_exec)

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


def test_indexing_uninitialized_clean_repo_fails_without_non_index_diff(
    tmp_path: Path, monkeypatch
) -> None:
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)

    result = runner.invoke(app, ["indexing"], catch_exceptions=False)

    assert result.exit_code != 0
    assert "cmoc init を実行してから再実行してください。" in result.output
    assert not (root / ".gitignore").exists()
    assert not (root / ".cmoc").exists()
    assert not (root / "INDEX.md").exists()
    assert run_git(root, "status", "--short").stdout.strip() == ""


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

    monkeypatch.setattr(indexing_module, "run_codex_exec", lambda parameter, **kwargs: FakeCodexResult()
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

    monkeypatch.setattr(indexing_module, "run_codex_exec", lambda parameter, **kwargs: FakeCodexResult()
    )
    first = runner.invoke(app, ["indexing"], catch_exceptions=False)
    assert first.exit_code == 0
    root_index_before = (root / "INDEX.md").read_text()
    head_before = run_git(root, "rev-parse", "HEAD").stdout.strip()

    calls: list[str] = []

    def fail_if_called(parameter, **kwargs):
        calls.append(kwargs["purpose"])
        raise AssertionError("fresh INDEX.md should not require Codex")

    monkeypatch.setattr(indexing_module, "run_codex_exec", fail_if_called)
    second = runner.invoke(app, ["indexing"], catch_exceptions=False)

    assert second.exit_code == 0
    assert calls == []
    assert (root / "INDEX.md").read_text() == root_index_before
    assert run_git(root, "rev-parse", "HEAD").stdout.strip() == head_before
    assert run_git(root, "status", "--short").stdout.strip() == ""


def test_commit_index_updates_commits_only_index_paths(tmp_path: Path) -> None:
    root = make_repo(tmp_path)
    index_path = root / "INDEX.md"
    index_path.write_text("# generated\n")
    (root / ".gitignore").write_text("/.cmoc/\n")

    indexing_module.commit_index_updates(root, [index_path])

    committed_paths = run_git(
        root, "show", "--name-only", "--pretty=", "HEAD"
    ).stdout.strip()
    assert committed_paths == "INDEX.md"
    assert run_git(root, "status", "--short").stdout.strip() == "?? .gitignore"


def test_indexing_allows_existing_non_index_diff_and_commits_only_index(
    tmp_path: Path, monkeypatch
) -> None:
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert runner.invoke(app, ["init"], catch_exceptions=False).exit_code == 0
    (root / "README.md").write_text("# repo\n\nchanged\n")
    index_path = root / "INDEX.md"

    def fake_update_indexes(update_root: Path, codex_exec=None) -> list[Path]:
        assert update_root == root
        index_path.write_text("# generated\n")
        return [index_path]

    monkeypatch.setattr(indexing_module, "update_indexes", fake_update_indexes)

    result = runner.invoke(app, ["indexing"], catch_exceptions=False)

    assert result.exit_code == 0
    committed_paths = run_git(
        root, "show", "--name-only", "--pretty=", "HEAD"
    ).stdout.splitlines()
    assert committed_paths == ["INDEX.md"]
    assert run_git(root, "status", "--short").stdout == " M README.md\n"


def test_indexing_preflight_allows_existing_non_index_diff_and_commits_only_index(
    tmp_path: Path, monkeypatch
) -> None:
    root = make_repo(tmp_path)
    index_path = root / "INDEX.md"
    (root / "README.md").write_text("# repo\n\nchanged\n")

    def fake_update_indexes(update_root: Path, codex_exec=None) -> list[Path]:
        assert update_root == root
        index_path.write_text("# generated\n")
        return [index_path]

    monkeypatch.setattr(indexing_module, "update_indexes", fake_update_indexes)

    indexing_module.run_indexing_preflight(root, lambda *args, **kwargs: None)

    committed_paths = run_git(
        root, "show", "--name-only", "--pretty=", "HEAD"
    ).stdout.splitlines()
    assert committed_paths == ["INDEX.md"]
    assert run_git(root, "status", "--short").stdout == " M README.md\n"


@pytest.mark.parametrize(
    "entry_lines",
    [
        [
            "# `README.md`",
            "",
            "## hash",
            "- {digest}",
            "",
        ],
        [
            "# `README.md`",
            "",
            "## Summary",
            "",
            "## Read this when",
            "- read README.md",
            "",
            "## Do not read this when",
            "- skip README.md",
            "",
            "## hash",
            "- {digest}",
            "",
        ],
    ],
)
def test_update_indexes_regenerates_malformed_fresh_hash_entry(
    tmp_path: Path, monkeypatch, entry_lines: list[str]
) -> None:
    root = make_repo(tmp_path)
    cmoc_runtime.sync_config(root)
    readme = root / "README.md"
    digest = indexing_module.index_target_hash(root, readme)
    (root / "INDEX.md").write_text(
        "\n".join(line.format(digest=digest) for line in entry_lines)
    )

    calls: list[Path] = []

    def fake_build_index_entry(
        update_root: Path,
        path: Path,
        digest: str | None = None,
        codex_exec=None,
    ) -> str:
        calls.append(path)
        return indexing_module.render_index_entry(
            update_root,
            path,
            {
                "summary": [f"generated {path.name}"],
                "read_this_when": [f"read {path.name}"],
                "do_not_read_this_when": [f"skip {path.name}"],
            },
            digest=digest,
        ).rstrip()

    monkeypatch.setattr(indexing_module, "build_index_entry", fake_build_index_entry)

    updated = indexing_module.update_indexes(root)

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
        update_root: Path,
        path: Path,
        digest: str | None = None,
        codex_exec=None,
    ) -> str:
        nonlocal active, max_active
        if path.parent == docs:
            with lock:
                active += 1
                max_active = max(max_active, active)
            time.sleep(0.05)
            with lock:
                active -= 1
        return indexing_module.render_index_entry(
            update_root,
            path,
            {
                "summary": [path.name],
                "read_this_when": [path.name],
                "do_not_read_this_when": [path.name],
            },
            digest=digest,
        ).rstrip()

    monkeypatch.setattr(indexing_module, "build_index_entry", fake_build_index_entry)

    updated = indexing_module.update_indexes(root)

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
        update_root: Path,
        path: Path,
        digest: str | None = None,
        codex_exec=None,
    ) -> str:
        return indexing_module.render_index_entry(
            update_root,
            path,
            {
                "summary": [path.name],
                "read_this_when": [path.name],
                "do_not_read_this_when": [path.name],
            },
            digest=digest,
        ).rstrip()

    monkeypatch.setattr(indexing_module, "build_index_entry", fake_build_index_entry)

    updated = indexing_module.update_indexes(root)

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

    def fake_update_indexes(update_root: Path, codex_exec=None) -> list[Path]:
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

    indexing_module.enable_indexing_preflight()
    monkeypatch.setattr(indexing_module, "update_indexes", fake_update_indexes)
    monkeypatch.setattr(
        codex_preflight_module, "runtime_run_codex_exec", fake_runtime_run_codex_exec
    )

    result = codex_preflight_module.run_codex_exec(
        parameter, root=root, purpose="apply fork refine findings"
    )

    assert isinstance(result, FakeCodexResult)
    assert events == ["indexing", "codex"]
    assert run_git(root, "log", "-1", "--pretty=%s").stdout.strip() == "cmoc indexing"
    assert run_git(root, "status", "--short").stdout.strip() == ""


def test_command_codex_call_indexes_cwd_worktree_before_root(
    tmp_path: Path, monkeypatch
) -> None:
    root = make_repo(tmp_path)
    worktree = tmp_path / "codex-worktree"
    run_git(root, "worktree", "add", "-b", "codex-work", str(worktree))
    codex_cwd = worktree / "oracle"
    parameter = AgentCallParameter(
        ModelClass.EFFICIENCY,
        ReasoningEffort.LOW,
        FileAccessMode.READONLY,
        "prompt",
        None,
    )
    events: list[str] = []

    def fake_update_indexes(update_root: Path, codex_exec=None) -> list[Path]:
        events.append("indexing")
        assert update_root == worktree
        index_path = update_root / "INDEX.md"
        index_path.write_text("# generated\n")
        return [index_path]

    class FakeCodexResult:
        output_json = None

    def fake_runtime_run_codex_exec(call_parameter, **kwargs):
        events.append("codex")
        assert kwargs["root"] == root
        assert kwargs["cwd"] == codex_cwd
        return FakeCodexResult()

    indexing_module.enable_indexing_preflight()
    monkeypatch.setattr(indexing_module, "update_indexes", fake_update_indexes)
    monkeypatch.setattr(
        codex_preflight_module, "runtime_run_codex_exec", fake_runtime_run_codex_exec
    )

    result = codex_preflight_module.run_codex_exec(
        parameter,
        root=root,
        cwd=codex_cwd,
        purpose="review oracle enumerate findings",
    )

    assert isinstance(result, FakeCodexResult)
    assert events == ["indexing", "codex"]
    assert (
        run_git(worktree, "log", "-1", "--pretty=%s").stdout.strip()
        == "cmoc indexing"
    )
    assert run_git(worktree, "status", "--short").stdout.strip() == ""
    assert run_git(root, "log", "-1", "--pretty=%s").stdout.strip() == "initial"
    assert not (root / "INDEX.md").exists()


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

    def fake_update_indexes(update_root: Path, codex_exec=None) -> list[Path]:
        events.append("indexing")
        assert update_root == root
        index_path.write_text("# generated\n")
        return [index_path]

    def fake_runtime_run_codex_tui(call_parameter, **kwargs):
        events.append("codex")
        assert call_parameter == parameter

    indexing_module.enable_indexing_preflight()
    monkeypatch.setattr(indexing_module, "update_indexes", fake_update_indexes)
    monkeypatch.setattr(
        codex_preflight_module,
        "runtime_run_codex_tui",
        fake_runtime_run_codex_tui,
    )

    codex_preflight_module.run_codex_tui(parameter, root=root, purpose="tui codex")

    assert events == ["indexing", "codex"]
    assert run_git(root, "log", "-1", "--pretty=%s").stdout.strip() == "cmoc indexing"
    assert run_git(root, "status", "--short").stdout.strip() == ""


def test_indexing_preflight_waits_for_repository_lock(
    tmp_path: Path, monkeypatch
) -> None:
    root = make_repo(tmp_path)
    lock_path = indexing_module.indexing_lock_path(root)
    ready_parent, ready_child = multiprocessing.Pipe(duplex=False)
    release_child, release_parent = multiprocessing.Pipe(duplex=False)
    process = multiprocessing.Process(
        target=hold_indexing_lock,
        args=(lock_path, ready_child, release_child),
    )
    events: list[str] = []
    released = False

    def fake_update_indexes(update_root: Path, codex_exec=None) -> list[Path]:
        events.append("updated")
        return []

    monkeypatch.setattr(indexing_module, "update_indexes", fake_update_indexes)

    process.start()
    try:
        assert ready_parent.recv() is True
        thread = threading.Thread(
            target=indexing_module.run_indexing_preflight,
            args=(root, lambda *args, **kwargs: None),
        )
        thread.start()
        time.sleep(0.2)
        assert events == []
        release_parent.send(True)
        released = True
        thread.join(timeout=3)
        assert not thread.is_alive()
        assert events == ["updated"]
    finally:
        if process.is_alive() and not released:
            release_parent.send(True)
        process.join(timeout=3)
        if process.is_alive():
            process.terminate()
            process.join()


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

    def fail_update_indexes(update_root: Path, codex_exec=None) -> list[Path]:
        raise AssertionError("indexing preflight should be skipped")

    def fake_runtime_run_codex_exec(call_parameter, **kwargs):
        calls.append(kwargs["purpose"])
        return FakeCodexResult()

    indexing_module.enable_indexing_preflight()
    monkeypatch.setattr(indexing_module, "update_indexes", fail_update_indexes)
    monkeypatch.setattr(
        codex_preflight_module, "runtime_run_codex_exec", fake_runtime_run_codex_exec
    )

    codex_preflight_module.run_codex_exec(
        parameter, root=root, purpose="indexing index entry for README.md"
    )
    codex_preflight_module.run_codex_exec(
        parameter, root=root, purpose="session join conflict resolution"
    )

    assert calls == [
        "indexing index entry for README.md",
        "session join conflict resolution",
    ]
