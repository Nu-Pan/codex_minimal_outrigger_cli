"""session/run state schema と managed branch 解析の realization test。"""

import json
import multiprocessing
import threading
from multiprocessing.connection import Connection
from pathlib import Path

import pytest
from _git_support import make_repo

from cmoc_runtime import CmocError
from commons.runtime_state import (
    RunPart,
    SessionPart,
    SessionState,
    branch_session_id,
    load_session_part_for_branch,
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


def _valid_state() -> SessionState:
    """永続化 schema を満たす state のテスト値を返す。

    根拠: {{work-root}}/oracle/doc/app_spec/session_state.md
    """
    return SessionState(SessionPart("active", "main", "abc", None), RunPart())


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
    state = _valid_state()
    state.run = RunPart("joinable", "realization_apply", "cmoc/run/session/run", "abc")
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
    data = _valid_state().to_dict()
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
    data = _valid_state().to_dict()
    data[part][field] = value

    with pytest.raises(CmocError) as exc_info:
        SessionState.from_dict(data)

    assert f"`{part}.{field}` は string または null" in exc_info.value.detail


def test_ready_run_requires_null_payload() -> None:
    data = _valid_state().to_dict()
    data["run"]["kind"] = "realization_apply"

    with pytest.raises(CmocError, match="session state file"):
        SessionState.from_dict(data)


def test_oracle_edit_is_not_a_run_kind() -> None:
    data = _valid_state().to_dict()
    data["run"] = {
        "state": "running",
        "kind": "oracle_edit",
        "branch": "cmoc/run/session/run",
        "fork_commit": "abc",
    }

    with pytest.raises(CmocError, match="session state file"):
        SessionState.from_dict(data)


def test_load_session_part_does_not_validate_run_section(tmp_path: Path) -> None:
    path = state_path(tmp_path, "session")
    path.parent.mkdir(parents=True)
    session = SessionPart("active", "main", "abc", None)
    path.write_text(
        json.dumps(
            {
                "session": {
                    "state": session.state,
                    "session_home_branch": session.session_home_branch,
                    "session_fork_commit": session.session_fork_commit,
                    "last_joined_apply_fork_commit": None,
                },
                "run": {"not_inspected": True},
            }
        )
    )

    session_id, loaded_path, loaded = load_session_part_for_branch(
        tmp_path, "cmoc/session/session"
    )

    assert session_id == "session"
    assert loaded_path == path
    assert loaded == session


@pytest.mark.parametrize("field", ["session_home_branch", "session_fork_commit"])
def test_session_state_requires_session_identity(field: str) -> None:
    data = _valid_state().to_dict()
    data["session"][field] = None

    with pytest.raises(CmocError) as exc_info:
        SessionState.from_dict(data)

    assert f"`session.{field}` は string" in exc_info.value.detail


@pytest.mark.parametrize("field", ["session_home_branch", "session_fork_commit"])
def test_load_session_part_requires_session_identity(
    tmp_path: Path, field: str
) -> None:
    path = state_path(tmp_path, "session")
    path.parent.mkdir(parents=True)
    data = _valid_state().to_dict()
    data["session"][field] = None
    data["run"] = {"not_inspected": True}
    path.write_text(json.dumps(data))

    with pytest.raises(CmocError) as exc_info:
        load_session_part_for_branch(tmp_path, "cmoc/session/session")

    assert f"`session.{field}` は string" in exc_info.value.detail


def test_write_state_rejects_invalid_session_identity(tmp_path: Path) -> None:
    path = state_path(tmp_path, "session")

    with pytest.raises(CmocError):
        write_state(path, SessionState())

    assert not path.exists()


@pytest.mark.parametrize("state", ["running", "joinable", "error"])
def test_active_run_requires_kind_branch_and_fork_commit(state: str) -> None:
    data = _valid_state().to_dict()
    data["run"]["state"] = state

    with pytest.raises(CmocError, match="session state file"):
        SessionState.from_dict(data)


def test_session_state_rejects_unknown_fields() -> None:
    data = _valid_state().to_dict()
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
