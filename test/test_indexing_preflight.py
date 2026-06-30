import multiprocessing
import threading
import time
from collections.abc import Callable
from multiprocessing.connection import Connection
from pathlib import Path

import pytest
import commons.runtime_codex_preflight as codex_preflight_module
from basic.acp import AgentCallParameter, FileAccessMode, ModelClass, ReasoningEffort

from _support import (
    make_repo,
    run_git,
)
import commons.indexing as indexing_module


def hold_indexing_lock(lock_path: Path, ready: Connection, release: Connection) -> None:
    import fcntl

    lock_path.parent.mkdir(parents=True, exist_ok=True)
    with lock_path.open("a+") as lock_file:
        fcntl.flock(lock_file.fileno(), fcntl.LOCK_EX)
        ready.send(True)
        release.recv()
        fcntl.flock(lock_file.fileno(), fcntl.LOCK_UN)


def test_command_codex_call_runs_indexing_preflight(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
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

    def fake_update_indexes(
        update_root: Path, codex_exec: Callable[..., object] | None = None
    ) -> list[Path]:
        events.append("indexing")
        assert update_root == root
        index_path.write_text("# generated\n")
        return [index_path]

    class FakeCodexResult:
        output_json = None

    def fake_runtime_run_codex_exec(
        call_parameter: AgentCallParameter, **kwargs: object
    ) -> FakeCodexResult:
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
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
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

    def fake_update_indexes(
        update_root: Path, codex_exec: Callable[..., object] | None = None
    ) -> list[Path]:
        events.append("indexing")
        assert update_root == worktree
        index_path = update_root / "INDEX.md"
        index_path.write_text("# generated\n")
        return [index_path]

    class FakeCodexResult:
        output_json = None

    def fake_runtime_run_codex_exec(
        call_parameter: AgentCallParameter, **kwargs: object
    ) -> FakeCodexResult:
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
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
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

    def fake_update_indexes(
        update_root: Path, codex_exec: Callable[..., object] | None = None
    ) -> list[Path]:
        events.append("indexing")
        assert update_root == root
        index_path.write_text("# generated\n")
        return [index_path]

    def fake_runtime_run_codex_tui(
        call_parameter: AgentCallParameter, **kwargs: object
    ) -> None:
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
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
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

    def fake_update_indexes(
        update_root: Path, codex_exec: Callable[..., object] | None = None
    ) -> list[Path]:
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
    monkeypatch: pytest.MonkeyPatch,
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

    def fail_update_indexes(
        update_root: Path, codex_exec: Callable[..., object] | None = None
    ) -> list[Path]:
        raise AssertionError("indexing preflight should be skipped")

    def fake_runtime_run_codex_exec(
        call_parameter: AgentCallParameter, **kwargs: object
    ) -> FakeCodexResult:
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
