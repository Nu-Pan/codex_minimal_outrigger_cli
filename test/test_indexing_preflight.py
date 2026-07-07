import multiprocessing
import threading
import time
from collections.abc import Callable, Iterator
from multiprocessing.connection import Connection
from pathlib import Path

import pytest
import commons.runtime_codex_preflight as codex_preflight_module
from basic.acp import AgentCallParameter, FileAccessMode, ModelClass, ReasoningEffort
from config.cmoc_config import CmocConfig

from _support import (
    make_repo,
    run_git,
    setup_codex_home,
    write_python_executable,
)
import commons.indexing as indexing_module


@pytest.fixture(autouse=True)
def reset_indexing_preflight() -> Iterator[None]:
    codex_preflight_module.disable_indexing_preflight()
    yield
    codex_preflight_module.disable_indexing_preflight()


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


def test_command_codex_call_skips_indexing_when_parameter_disables_preflight(
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
        False,
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


def test_file_access_violation_does_not_trigger_recovery_indexing_preflight(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = make_repo(tmp_path)
    setup_codex_home(tmp_path, monkeypatch)
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    counter = tmp_path / "count.txt"
    write_python_executable(
        bin_dir / "codex",
        [
            "import json, pathlib, sys",
            f"counter = pathlib.Path({str(counter)!r})",
            "count = int(counter.read_text()) if counter.exists() else 0",
            "counter.write_text(str(count + 1))",
            "args = sys.argv[1:]",
            "output = pathlib.Path(args[args.index('--output-last-message') + 1])",
            "blocked = pathlib.Path('oracle/blocked.md')",
            "blocked.write_text('blocked\\n')",
            "output.write_text('{}\\n')",
            "print(json.dumps({'type': 'turn.completed'}))",
        ],
    )
    monkeypatch.setenv("PATH", f"{bin_dir}:{Path('/usr/bin')}")
    index_path = root / "INDEX.md"
    events: list[Path] = []
    parameter = AgentCallParameter(
        ModelClass.EFFICIENCY,
        ReasoningEffort.LOW,
        FileAccessMode.REALIZATION_WRITE,
        "prompt",
        None,
    )

    def fake_update_indexes(
        update_root: Path, codex_exec: Callable[..., object] | None = None
    ) -> list[Path]:
        events.append(update_root)
        index_path.write_text(f"# generated {len(events)}\n")
        return [index_path]

    indexing_module.enable_indexing_preflight()
    monkeypatch.setattr(indexing_module, "update_indexes", fake_update_indexes)

    codex_preflight_module.run_codex_exec(
        parameter,
        root=root,
        capacity_initial_sleep_sec=0,
        config=CmocConfig(),
        purpose="apply fork refine findings",
    )

    assert counter.read_text() == "1"
    assert events == [root]
    assert (root / "oracle" / "blocked.md").read_text() == "blocked\n"
