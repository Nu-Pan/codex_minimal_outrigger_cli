"""session/run state schema と managed branch 解析の realization test。"""

import json
import multiprocessing
import os
from multiprocessing.connection import Connection
from pathlib import Path

import pytest
from _git_support import RUN_BRANCH, RUN_ID, SESSION_BRANCH, SESSION_ID

import commons.runtime_state as runtime_state_module
from cmoc_runtime import CmocError
from commons.runtime_state import (
    RunPart,
    SessionPart,
    SessionState,
    active_session_for_home,
    branch_session_id,
    load_session_part_for_branch,
    load_state_for_branch,
    run_branch_session_id,
    session_fork_lock,
    state_path,
    write_state,
)


def _acquire_session_fork_lock(
    root: Path, common_dir: Path, status: Connection
) -> None:
    """別 process から実 lock の競合と取得を通知する。"""
    # spawn でも親の monkeypatch に依存せず、同じ共有 directory を使う。
    with status, pytest.MonkeyPatch.context() as monkeypatch:
        monkeypatch.setattr(
            runtime_state_module, "git_common_dir", lambda _root: common_dir
        )
        original_flock = runtime_state_module.fcntl.flock

        def observe_lock_attempt(fd: int, operation: int) -> None:
            # 親が保持する lock への競合を、時間経過に頼らず確かめる。
            if operation & runtime_state_module.fcntl.LOCK_EX:
                try:
                    original_flock(fd, operation | runtime_state_module.fcntl.LOCK_NB)
                except BlockingIOError:
                    status.send("contended")
            original_flock(fd, operation)

        monkeypatch.setattr(runtime_state_module.fcntl, "flock", observe_lock_attempt)
        assert status.recv() == "acquire"
        with session_fork_lock(root):
            status.send("acquired")


def _valid_state() -> SessionState:
    """永続化 schema を満たす state のテスト値を返す。

    根拠: {{work-root}}/spec/app_spec/session_state.md
    """
    return SessionState(SessionPart("active", "main", "abc", None), RunPart())


@pytest.mark.parametrize(
    "branch",
    [
        "cmoc/session/",
        "cmoc/session/id/extra",
        "cmoc/session/.",
        "cmoc/session/..",
        "cmoc/session/id\x00",
        "cmoc/session/2026-09-29_15-04_07_123456789",
        f"cmoc/session/{RUN_ID}",
        "cmoc/run/id/run",
    ],
)
def test_branch_session_id_rejects_invalid_shape(branch: str) -> None:
    """session branch の不正な形を拒否する。"""
    with pytest.raises(CmocError):
        branch_session_id(branch)


@pytest.mark.parametrize(
    "branch",
    [
        "cmoc/run/",
        "cmoc/run/session",
        f"{RUN_BRANCH}/extra",
        f"cmoc/run/../{RUN_ID}",
        f"cmoc/run/{SESSION_ID}/.",
        f"{RUN_BRANCH}\x00",
        f"cmoc/run/2026-09-29_15-04_07_123456789/{RUN_ID}",
        f"cmoc/run/{SESSION_ID}/2026-09-29_15-04_07_123456789",
        f"cmoc/run/{RUN_ID}/{SESSION_ID}",
    ],
)
def test_run_branch_session_id_rejects_invalid_shape(branch: str) -> None:
    """run branch の不正な形を拒否する。"""
    with pytest.raises(CmocError):
        run_branch_session_id(branch)


def test_load_state_for_run_branch_uses_session_component(tmp_path: Path) -> None:
    """run branch の session component から state file を解決する。"""
    path = state_path(tmp_path, SESSION_ID)
    assert active_session_for_home(tmp_path, "main") is None
    state = _valid_state()
    state.run = RunPart("joinable", "decision_apply", RUN_BRANCH, "abc")
    write_state(path, state)

    session_id, loaded_path, loaded = load_state_for_branch(tmp_path, RUN_BRANCH)

    assert session_id == SESSION_ID
    assert loaded_path == path
    assert loaded == state
    assert active_session_for_home(tmp_path, "main") == path
    assert active_session_for_home(tmp_path, "other") is None

    # JSON 用 snapshot と元の state は双方向に変更を持ち越さない。
    snapshot = state.to_dict()
    snapshot["run"]["state"] = "error"
    assert state.run.state == "joinable"
    state.session.session_home_branch = "開発/作業"
    assert snapshot["session"]["session_home_branch"] == "main"

    # 既存 file の更新でも run payload を消去し、session branch から復元できる。
    state.run = RunPart()
    write_state(path, state)
    assert load_state_for_branch(tmp_path, SESSION_BRANCH) == (SESSION_ID, path, state)
    assert active_session_for_home(tmp_path, "main") is None
    assert active_session_for_home(tmp_path, "開発/作業") == path


@pytest.mark.parametrize("branch", [None, 1])
def test_load_state_rejects_non_string_branch(branch: object) -> None:
    """branch の型異常を raw AttributeError として漏らさない。"""
    # branch の型検証に保存先は不要なので、directory を準備しない。
    with pytest.raises(CmocError, match="cmoc 管理 branch"):
        load_state_for_branch(Path("unused"), branch)  # type: ignore[arg-type]


@pytest.mark.parametrize(
    "session_id",
    [
        "../outside",
        "/outside",
        "nested/id",
        ".",
        "..",
        "bad\ud800",
        "2026-09-29_15-04_07_123456789",
        RUN_ID,
    ],
)
def test_state_path_rejects_noncanonical_session_id(session_id: str) -> None:
    """現行 session ID 以外を state の保存先に使わない。"""
    # ID の書式検証に保存先は不要なので、directory を準備しない。
    with pytest.raises(CmocError, match="session-id"):
        state_path(Path("unused"), session_id)


def test_state_io_rejects_noncanonical_filename(tmp_path: Path) -> None:
    """直接指定や一覧読み取りでも旧 ID の state を受理・上書きしない。"""
    directory = state_path(tmp_path, SESSION_ID).parent
    directory.mkdir(parents=True)
    path = directory / "2026-09-29_15-04_07_123456789.json"
    content = json.dumps(_valid_state().to_dict())
    path.write_text(content)

    with pytest.raises(CmocError, match="session-id"):
        write_state(path, _valid_state())
    with pytest.raises(CmocError, match="session-id"):
        active_session_for_home(tmp_path, "main")

    assert path.read_text() == content


@pytest.mark.parametrize("payload", [b"{", b"\xff"])
def test_load_state_rejects_unreadable_json(tmp_path: Path, payload: bytes) -> None:
    """壊れた JSON または UTF-8 の state file を利用者向けエラーへ変換する。"""
    path = state_path(tmp_path, SESSION_ID)
    path.parent.mkdir(parents=True)
    path.write_bytes(payload)

    with pytest.raises(CmocError) as exc_info:
        load_state_for_branch(tmp_path, SESSION_BRANCH)

    assert "session state file が不正です。" == exc_info.value.summary


def test_load_state_rejects_excessively_nested_json(tmp_path: Path) -> None:
    """JSON parser の recursion error を state error へ変換する。"""
    path = state_path(tmp_path, SESSION_ID)
    path.parent.mkdir(parents=True)
    depth = 10_000
    payload = (
        b'{"session":{"state":"active","session_home_branch":"main",'
        b'"session_fork_commit":"abc","last_joined_apply_fork_commit":null},'
        b'"run":{"state":"ready","kind":null,"branch":null,"fork_commit":'
        + b"[" * depth
        + b"0"
        + b"]" * depth
        + b"}}"
    )
    path.write_bytes(payload)

    with pytest.raises(CmocError) as exc_info:
        load_state_for_branch(tmp_path, SESSION_BRANCH)

    assert exc_info.value.summary == "session state file が不正です。"


@pytest.mark.parametrize("part", ["session", "run"])
@pytest.mark.parametrize("value", [[], {}])
def test_session_state_rejects_non_string_state(part: str, value: object) -> None:
    """session/run state が string でない payload を拒否する。"""
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
    """state payload の string または null 以外の値を拒否する。"""
    data = _valid_state().to_dict()
    data[part][field] = value

    with pytest.raises(CmocError) as exc_info:
        SessionState.from_dict(data)

    assert f"`{part}.{field}` は string または null" in exc_info.value.detail


def test_ready_run_requires_null_payload() -> None:
    """ready run が active run payload を持つ state を拒否する。"""
    data = _valid_state().to_dict()
    data["run"]["kind"] = "decision_apply"

    with pytest.raises(CmocError, match="session state file"):
        SessionState.from_dict(data)


def test_oracle_edit_is_not_a_run_kind() -> None:
    """oracle edit を editing run kind として受け入れない。"""
    data = _valid_state().to_dict()
    data["run"] = {
        "state": "running",
        "kind": "oracle_edit",
        "branch": RUN_BRANCH,
        "fork_commit": "abc",
    }

    with pytest.raises(CmocError, match="session state file"):
        SessionState.from_dict(data)


def test_load_session_part_does_not_validate_run_section(tmp_path: Path) -> None:
    """session 部分の読み込みが未検証の run 部分に依存しない。"""
    path = state_path(tmp_path, SESSION_ID)
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
        tmp_path, SESSION_BRANCH
    )

    assert session_id == SESSION_ID
    assert loaded_path == path
    assert loaded == session


@pytest.mark.parametrize("mutation", ["missing_run", "unknown_top_level"])
def test_load_session_part_rejects_invalid_top_level(
    tmp_path: Path, mutation: str
) -> None:
    """session 部分だけを読む場合も state の top-level schema を守る。"""
    path = state_path(tmp_path, SESSION_ID)
    path.parent.mkdir(parents=True)
    data = _valid_state().to_dict()
    data["run"] = {"not_inspected": True}
    if mutation == "missing_run":
        del data["run"]
    else:
        data["obsolete"] = None
    path.write_text(json.dumps(data))

    with pytest.raises(CmocError) as exc_info:
        load_session_part_for_branch(tmp_path, SESSION_BRANCH)

    assert "top-level" in exc_info.value.detail


@pytest.mark.parametrize("field", ["session_home_branch", "session_fork_commit"])
def test_session_state_requires_session_identity(field: str) -> None:
    """session identity の必須 field が null の state を拒否する。"""
    data = _valid_state().to_dict()
    data["session"][field] = None

    with pytest.raises(CmocError) as exc_info:
        SessionState.from_dict(data)

    assert f"`session.{field}` は string" in exc_info.value.detail


@pytest.mark.parametrize("field", ["session_home_branch", "session_fork_commit"])
def test_load_session_part_requires_session_identity(
    tmp_path: Path, field: str
) -> None:
    """session 部分の読み込みでも session identity を要求する。"""
    path = state_path(tmp_path, SESSION_ID)
    path.parent.mkdir(parents=True)
    data = _valid_state().to_dict()
    data["session"][field] = None
    data["run"] = {"not_inspected": True}
    path.write_text(json.dumps(data))

    with pytest.raises(CmocError) as exc_info:
        load_session_part_for_branch(tmp_path, SESSION_BRANCH)

    assert f"`session.{field}` は string" in exc_info.value.detail


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
def test_session_state_rejects_empty_payload(part: str, field: str) -> None:
    """branch・commit などの state payload に空文字を保存しない。"""
    data = _valid_state().to_dict()
    data[part][field] = ""

    with pytest.raises(CmocError) as exc_info:
        SessionState.from_dict(data)

    assert f"`{part}.{field}`" in exc_info.value.detail


@pytest.mark.parametrize(
    "value", ["main\x00branch", "開発\x00branch", "main\ud800", "開発\ud800"]
)
def test_session_state_rejects_unrepresentable_payload(value: str) -> None:
    """state payload に process/file 境界で扱えない文字を保存しない。"""
    data = _valid_state().to_dict()
    data["session"]["session_home_branch"] = value

    with pytest.raises(CmocError) as exc_info:
        SessionState.from_dict(data)

    assert "保存できない文字" in exc_info.value.detail


@pytest.mark.parametrize("existing", [False, True])
def test_write_state_rejects_invalid_session_identity(
    tmp_path: Path, existing: bool
) -> None:
    """不完全な session state で新規作成・既存 file の上書きをしない。"""
    path = state_path(tmp_path, SESSION_ID)
    if existing:
        path.parent.mkdir(parents=True)
        path.write_text("original\n")

    with pytest.raises(CmocError):
        write_state(path, SessionState())

    if existing:
        assert path.read_text() == "original\n"
    else:
        assert not path.exists()


@pytest.mark.parametrize("location", ["file", "parent", "ancestor"])
@pytest.mark.parametrize("target", ["dangling", "existing", "loop"])
def test_session_state_rejects_symlinked_path_without_writing_target(
    tmp_path: Path, location: str, target: str
) -> None:
    """session state の symlink 経由 read/write で link 先を扱わない。"""
    path = state_path(tmp_path, SESSION_ID)
    link = {"file": path, "parent": path.parent, "ancestor": path.parent.parent}[
        location
    ]
    outside = tmp_path / "outside"
    outside_state = outside if location == "file" else outside / path.relative_to(link)
    if target == "existing":
        outside_state.parent.mkdir(parents=True, exist_ok=True)
        outside_state.write_text("original\n")
    link.parent.mkdir(parents=True, exist_ok=True)
    link.symlink_to(
        link if target == "loop" else outside, target_is_directory=location != "file"
    )

    with pytest.raises(CmocError, match="session state path"):
        state_path(tmp_path, SESSION_ID)
    with pytest.raises(CmocError, match="session state path"):
        write_state(path, _valid_state())
    with pytest.raises(CmocError, match="session state path"):
        load_state_for_branch(tmp_path, SESSION_BRANCH)
    with pytest.raises(CmocError, match="session state path"):
        load_session_part_for_branch(tmp_path, SESSION_BRANCH)
    with pytest.raises(CmocError, match="session state path"):
        active_session_for_home(tmp_path, "main")

    if target == "existing":
        assert outside_state.read_text() == "original\n"
    else:
        assert not outside.exists()


@pytest.mark.parametrize("kind", ["directory", "fifo"])
def test_state_operations_reject_non_regular_path(tmp_path: Path, kind: str) -> None:
    """state path が directory や FIFO の場合に raw open error や停止を起こさない。"""
    path = state_path(tmp_path, SESSION_ID)
    path.parent.mkdir(parents=True)
    if kind == "directory":
        path.mkdir()
    else:
        os.mkfifo(path)

    with pytest.raises(CmocError, match="通常の file"):
        write_state(path, _valid_state())
    with pytest.raises(CmocError, match="通常の file"):
        load_state_for_branch(tmp_path, SESSION_BRANCH)
    with pytest.raises(CmocError, match="通常の file"):
        load_session_part_for_branch(tmp_path, SESSION_BRANCH)


@pytest.mark.parametrize("location", ["parent", "ancestor"])
def test_state_operations_reject_non_directory_parent(
    tmp_path: Path, location: str
) -> None:
    """state directory の親が通常 file の場合に raw exception を漏らさない。"""
    path = state_path(tmp_path, SESSION_ID)
    parent = path.parent if location == "parent" else path.parent.parent
    parent.parent.mkdir(parents=True)
    parent.write_text("not a directory")

    with pytest.raises(CmocError, match="通常の directory"):
        state_path(tmp_path, SESSION_ID)
    with pytest.raises(CmocError, match="通常の directory"):
        write_state(path, _valid_state())
    with pytest.raises(CmocError, match="通常の directory"):
        load_state_for_branch(tmp_path, SESSION_BRANCH)
    with pytest.raises(CmocError, match="通常の directory"):
        load_session_part_for_branch(tmp_path, SESSION_BRANCH)
    with pytest.raises(CmocError, match="通常の directory"):
        active_session_for_home(tmp_path, "main")


def test_write_state_rechecks_parent_after_creation(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """parent 作成中に symlink が置かれても、保存前の検査で link 先を守る。"""
    path = state_path(tmp_path, SESSION_ID)
    outside = tmp_path / "outside"
    outside.mkdir()
    outside_state = outside / path.name
    outside_state.write_text("original\n")
    original_mkdir = Path.mkdir

    def mkdir_with_symlink(self: Path, *args: object, **kwargs: object) -> None:
        if self == path.parent:
            original_mkdir(self.parent, parents=True, exist_ok=True)
            self.symlink_to(outside, target_is_directory=True)
        else:
            original_mkdir(self, *args, **kwargs)

    monkeypatch.setattr(Path, "mkdir", mkdir_with_symlink)

    with pytest.raises(CmocError, match="session state path"):
        write_state(path, _valid_state())

    assert outside_state.read_text() == "original\n"


@pytest.mark.parametrize("state", ["running", "joinable", "error"])
def test_active_run_requires_kind_branch_and_fork_commit(state: str) -> None:
    """active run state が kind・branch・fork commit を必要とする。"""
    data = _valid_state().to_dict()
    data["run"]["state"] = state

    with pytest.raises(CmocError, match="session state file"):
        SessionState.from_dict(data)


@pytest.mark.parametrize(
    "branch",
    [
        "not-a-run-branch",
        SESSION_BRANCH,
        "cmoc/run/session",
        f"{RUN_BRANCH}/extra",
        f"cmoc/run/../{RUN_ID}",
        f"cmoc/run/2026-09-29_15-04_07_123456789/{RUN_ID}",
        f"cmoc/run/{SESSION_ID}/2026-09-29_15-04_07_123456789",
    ],
)
def test_active_run_rejects_noncanonical_branch(branch: str) -> None:
    """active run の branch が canonical naming rule に一致しない state を拒否する。"""
    data = _valid_state().to_dict()
    data["run"] = {
        "state": "running",
        "kind": "decision_apply",
        "branch": branch,
        "fork_commit": "abc",
    }

    with pytest.raises(CmocError, match="session state file"):
        SessionState.from_dict(data)


@pytest.mark.parametrize(
    "part", [None, "session", "run"], ids=["top", "session", "run"]
)
@pytest.mark.parametrize("defect", ["missing", "extra", "replaced"])
def test_session_state_rejects_invalid_field_sets(part, defect) -> None:
    """各階層の欠落・余分な field と、同数の field の置換を拒否する。"""
    data = _valid_state().to_dict()
    fields = data if part is None else data[part]
    if defect in ("missing", "replaced"):
        del fields[next(iter(fields))]
    if defect in ("extra", "replaced"):
        fields["obsolete"] = None

    with pytest.raises(CmocError) as exc_info:
        SessionState.from_dict(data)

    detail = exc_info.value.detail
    assert ("top-level" if part is None else f"`{part}` に") in detail
    assert ("必須 field" in detail) == (defect in ("missing", "replaced"))
    assert ("未定義 field" in detail) == (defect in ("extra", "replaced"))


def test_session_fork_lock_is_shared_across_processes(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """session fork lock が process 間で共有されることを確認する。"""
    root = tmp_path
    common_dir = tmp_path / "common"
    # Git common directory の実解決は test_git_query_reuse.py に残し、
    # ここでは異なる起点からの実 flock の競合・解放後の取得だけを検証する。
    status_parent, status_child = multiprocessing.Pipe()
    process = multiprocessing.Process(
        target=_acquire_session_fork_lock,
        args=(root / "linked", common_dir, status_child),
    )
    monkeypatch.setattr(
        runtime_state_module, "git_common_dir", lambda _root: common_dir
    )
    try:
        # fork で holder の file descriptor を子へ継承させない。
        process.start()
        status_child.close()
        # 親を holder にすることで、取得側に追加の thread と解放用 Pipe を使わない。
        with session_fork_lock(root):
            status_parent.send("acquire")
            assert status_parent.poll(timeout=3)
            assert status_parent.recv() == "contended"
            assert not status_parent.poll()
        assert status_parent.poll(timeout=3)
        assert status_parent.recv() == "acquired"
        process.join(timeout=3)
        assert process.exitcode == 0
    finally:
        if process.is_alive():
            process.terminate()
            process.join(timeout=3)
        process.close()
        status_parent.close()
        status_child.close()
