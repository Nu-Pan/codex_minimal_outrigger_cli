"""session/run state schema と managed branch 解析の realization test。"""

import multiprocessing
import threading
from multiprocessing.connection import Connection
from pathlib import Path

import pytest
from _git_support import make_repo

from cmoc_runtime import CmocError
from commons.runtime_state import (
    RunPart,
    SessionState,
    branch_session_id,
    load_state_for_branch,
    run_branch_session_id,
    session_fork_lock,
    state_path,
    write_state,
)


def hold_session_fork_lock(root: Path, ready: Connection, release: Connection) -> None:
    with session_fork_lock(root):
        ready.send(True)
        release.recv()


@pytest.mark.parametrize(
    "branch",
    ["cmoc/session/", "cmoc/session/id/extra", "cmoc/run/id/run"],
)
def test_branch_session_id_rejects_invalid_shape(branch: str) -> None:
    with pytest.raises(CmocError):
        branch_session_id(branch)


@pytest.mark.parametrize(
    "branch",
    ["cmoc/run/", "cmoc/run/session", "cmoc/run/session/run/extra"],
)
def test_run_branch_session_id_rejects_invalid_shape(branch: str) -> None:
    with pytest.raises(CmocError):
        run_branch_session_id(branch)


def test_load_state_for_run_branch_uses_session_component(tmp_path: Path) -> None:
    path = state_path(tmp_path, "session")
    state = SessionState()
    state.run = RunPart("joinable", "oracle_edit", "cmoc/run/session/run", "abc")
    write_state(path, state)

    session_id, loaded_path, loaded = load_state_for_branch(
        tmp_path, "cmoc/run/session/run"
    )

    assert session_id == "session"
    assert loaded_path == path
    assert loaded == state


@pytest.mark.parametrize("part", ["session", "run"])
@pytest.mark.parametrize("value", [[], {}])
def test_session_state_rejects_non_string_state(part: str, value: object) -> None:
    data = SessionState().to_dict()
    data[part]["state"] = value

    with pytest.raises(CmocError) as exc_info:
        SessionState.from_dict(data)

    assert f"`{part}.state` が不正です" in exc_info.value.detail


@pytest.mark.parametrize(
    ("part", "field"),
    [
        ("session", "session_home_branch"),
        ("session", "session_fork_commit"),
        ("session", "last_joined_apply_fork_commit"),
        ("run", "kind"),
        ("run", "branch"),
        ("run", "fork_commit"),
    ],
)
@pytest.mark.parametrize("value", [[], {}, 1, False])
def test_session_state_rejects_non_string_payload(
    part: str, field: str, value: object
) -> None:
    data = SessionState().to_dict()
    data[part][field] = value

    with pytest.raises(CmocError) as exc_info:
        SessionState.from_dict(data)

    assert f"`{part}.{field}` は string または null" in exc_info.value.detail


def test_ready_run_requires_null_payload() -> None:
    data = SessionState().to_dict()
    data["run"]["kind"] = "oracle_edit"

    with pytest.raises(CmocError, match="session state file"):
        SessionState.from_dict(data)


@pytest.mark.parametrize("state", ["running", "joinable", "error"])
def test_active_run_requires_kind_branch_and_fork_commit(state: str) -> None:
    data = SessionState().to_dict()
    data["run"]["state"] = state

    with pytest.raises(CmocError, match="session state file"):
        SessionState.from_dict(data)


def test_session_state_rejects_unknown_fields() -> None:
    data = SessionState().to_dict()
    data["run"]["obsolete"] = None

    with pytest.raises(CmocError) as exc_info:
        SessionState.from_dict(data)

    assert "未定義 field" in exc_info.value.detail


def test_session_fork_lock_is_shared_across_processes(tmp_path: Path) -> None:
    root = make_repo(tmp_path)
    ready_parent, ready_child = multiprocessing.Pipe(duplex=False)
    release_child, release_parent = multiprocessing.Pipe(duplex=False)
    process = multiprocessing.Process(
        target=hold_session_fork_lock,
        args=(root, ready_child, release_child),
    )
    process.start()
    acquired = threading.Event()
    worker = threading.Thread(target=lambda: _acquire_lock(root, acquired))
    released = False
    try:
        assert ready_parent.recv()
        worker.start()
        assert not acquired.wait(timeout=0.2)
        release_parent.send(True)
        released = True
        assert acquired.wait(timeout=3)
    finally:
        if not released:
            release_parent.send(True)
        worker.join(timeout=3)
        process.join(timeout=3)
        if process.is_alive():
            process.terminate()
            process.join(timeout=3)
    assert not worker.is_alive()
    assert not process.is_alive()


def _acquire_lock(root: Path, acquired: threading.Event) -> None:
    with session_fork_lock(root):
        acquired.set()
