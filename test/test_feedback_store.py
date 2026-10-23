"""feedback artifact と mutable state の durability・再保存を検証する。

同期の順序・失敗・再試行の検査では、実 fd と file 内容を観測し、ディスク同期を待たない。
実 fsync との結合は、並行保存の正常系と test_feedback.py の
collector 受理・後続 wave の publication 検査に残す。

対応する oracle file:

- `{{work-root}}/spec/app_spec/feedback_state.md`
- `{{work-root}}/spec/app_spec/feedback_observation.md`
"""

import errno
import os
import stat
import threading
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import pytest

import commons.runtime_feedback_state as state
import commons.runtime_feedback_store as store


def test_evidence_fingerprint_rechecks_metadata_and_read_failures(
    tmp_path, monkeypatch
):
    """種類の照会を重ねず、次回の内容と取得段階ごとの失敗を取り直す。"""
    path = tmp_path / "evidence.txt"
    original_stat, original_read = Path.stat, Path.read_bytes
    inspections, reads = [], []
    stat_error = read_error = None

    def inspect(target, *args, **kwargs):
        if target == path:
            inspections.append(target)
            if stat_error:
                raise stat_error
        return original_stat(target, *args, **kwargs)

    def read(target):
        reads.append(target)
        if read_error:
            raise read_error
        return original_read(target)

    monkeypatch.setattr(Path, "stat", inspect)
    monkeypatch.setattr(Path, "read_bytes", read)

    def capture(expected_state, content=None):
        inspections.clear()
        reads.clear()
        assert store._fingerprint(path) == {
            "normalized_path": str(path),
            "state": expected_state,
            "sha256": store.sha256_bytes(content) if content is not None else None,
        }
        assert inspections == [path]
        assert reads == ([path] if content is not None or read_error else [])

    capture("missing")
    path.mkdir()
    capture("not_file")
    path.rmdir()
    path.write_bytes(b"original evidence")
    capture("hashed", b"original evidence")
    path.write_bytes(b"updated evidence")
    capture("hashed", b"updated evidence")
    target = tmp_path / "target.txt"
    path.rename(target)
    path.symlink_to(target)
    capture("hashed", b"updated evidence")
    target.unlink()
    capture("missing")
    path.unlink()
    path.write_bytes(b"evidence")

    stat_error = PermissionError("injected stat failure")
    capture("unreadable")
    for code in (errno.ENOENT, errno.ENOTDIR, errno.EBADF, errno.ELOOP):
        stat_error = OSError(code, "injected missing path")
        capture("missing")
    stat_error = ValueError("unencodable path")
    capture("missing")
    stat_error = None
    for read_error in (PermissionError("unreadable"), FileNotFoundError("removed")):
        capture("unreadable")
    read_error = None
    capture("hashed", b"evidence")


def test_symlink_check_keeps_lexical_ancestors_and_rechecks_changes(
    tmp_path, monkeypatch
):
    directory = tmp_path / "入力"
    directory.mkdir()
    regular = directory / "record.json"
    regular.write_bytes(b"{}\n")
    alias = tmp_path / "alias"
    alias.mkdir()
    monkeypatch.chdir(tmp_path)

    for path in (
        Path("/"),
        Path("."),
        regular,
        regular / "not-a-directory" / "missing.json",
        alias / "missing" / "record.json",
    ):
        assert not store._has_symlink_component(path)

    # 同じ path でも次回は取り直し、.. の解決前や欠落した子の先の親を検査する。
    alias.rmdir()
    alias.symlink_to(directory, target_is_directory=True)
    for path in (
        Path("alias/record.json"),
        alias / "missing" / "record.json",
        alias / ".." / "入力" / "record.json",
        alias / "invalid\0name",
    ):
        assert store._has_symlink_component(path)

    alias.unlink()
    alias.symlink_to("alias")
    assert store._has_symlink_component(alias / "missing" / "record.json")
    alias.unlink()
    alias.symlink_to(tmp_path / "missing-directory", target_is_directory=True)
    assert store._has_symlink_component(alias / "missing" / "record.json")


def test_symlink_check_propagates_unreadable_parent(tmp_path, monkeypatch):
    blocked = tmp_path / "blocked"
    original_lstat = os.lstat

    def lstat(path, *args, **kwargs):
        if os.fspath(path) == str(blocked):
            raise PermissionError("unreadable parent")
        return original_lstat(path, *args, **kwargs)

    monkeypatch.setattr(os, "lstat", lstat)
    with pytest.raises(PermissionError, match="unreadable parent"):
        store._has_symlink_component(blocked / "missing.json")


@pytest.mark.parametrize("failure", [None, "file", "directory"])
def test_mutable_write_flushes_before_publication_and_preserves_failure_state(
    tmp_path, monkeypatch, failure
):
    """pointer の切替前後を区別し、同期失敗を隠さず回復用の内容を保つ。"""
    path = tmp_path / "current.json"
    previous = store.canonical_json_bytes({"generation": "previous"})
    value = {"generation": "next"}
    content = store.canonical_json_bytes(value)
    path.write_bytes(previous)
    events = []

    def fsync(fd):
        metadata = os.fstat(fd)
        kind = "directory" if stat.S_ISDIR(metadata.st_mode) else "file"
        events.append(kind)
        if kind == "file":
            assert metadata.st_size == len(content)
        assert path.read_bytes() == (previous if kind == "file" else content)
        if kind == failure:
            raise OSError("injected flush failure")

    monkeypatch.setattr(os, "fsync", fsync)

    if failure is None:
        assert state._atomic_write_json(path, value) == store.sha256_bytes(content)
    else:
        with pytest.raises(OSError, match="injected flush failure"):
            state._atomic_write_json(path, value)

    assert events == (["file"] if failure == "file" else ["file", "directory"])
    assert path.read_bytes() == (previous if failure == "file" else content)
    assert list(tmp_path.iterdir()) == [path]


def test_immutable_artifact_reference_reuses_saved_hash_and_checks_replays(
    tmp_path, monkeypatch
):
    path = tmp_path / "artifacts" / "record.json"
    value = {"evidence": "確認した内容"}
    content = store.canonical_json_bytes(value)
    reference = {
        "path": "artifacts/record.json",
        "sha256": store.sha256_bytes(content),
    }
    reads = []
    original_read = Path.read_bytes

    def read(candidate):
        if candidate == path:
            reads.append(candidate)
        return original_read(candidate)

    # 同期の契約は下の durability test に残し、保存・参照作成の I/O を観測する。
    monkeypatch.setattr(os, "fsync", lambda _fd: None)
    monkeypatch.setattr(Path, "read_bytes", read)
    assert state.write_immutable_artifact(tmp_path, path, value) == reference
    assert reads == []
    assert original_read(path) == content

    assert state.write_immutable_artifact(tmp_path, path, value) == reference
    assert reads == [path]
    path.write_bytes(b"changed\n")
    with pytest.raises(store.FeedbackRejected):
        state.write_immutable_artifact(tmp_path, path, value)
    assert reads == [path, path]
    assert original_read(path) == b"changed\n"


def test_immutable_write_flushes_new_data_and_reuses_published_inode(
    tmp_path, monkeypatch
):
    path = tmp_path / "artifacts" / "record.json"
    content = store.canonical_json_bytes({"evidence": "確認した内容"})
    events = []
    temporary_reads = []
    real_rename = os.rename
    real_read, real_open, real_stat = Path.read_bytes, Path.open, Path.stat

    def fsync(fd):
        kind = "directory" if stat.S_ISDIR(os.fstat(fd).st_mode) else "file"
        events.append(kind)
        if kind == "file":
            assert not path.exists()
        else:
            assert path.read_bytes() == content

    def rename(source, destination):
        assert events == ["file"]
        assert Path(source).read_bytes() == content
        assert destination == path
        assert not path.exists()
        events.append("rename")
        real_rename(source, destination)

    def read(candidate):
        if candidate.name.endswith(".tmp"):
            temporary_reads.append(candidate)
        return real_read(candidate)

    monkeypatch.setattr(os, "fsync", fsync)
    monkeypatch.setattr(os, "rename", rename)
    monkeypatch.setattr(Path, "read_bytes", read)
    assert store.write_immutable_bytes(path, content) == store.sha256_bytes(content)
    assert events == ["file", "rename", "directory"]
    # rename の観測で読み取った一回だけ。保存処理自身による読み戻しは不要。
    assert len(temporary_reads) == 1
    assert list(path.parent.iterdir()) == [path]
    inode = path.stat().st_ino

    def open_without_staging(candidate, mode="r", *args, **kwargs):
        assert mode != "xb", "replay must reuse the published artifact"
        return real_open(candidate, mode, *args, **kwargs)

    inspections = []

    def inspect(candidate, *args, **kwargs):
        if candidate == path:
            inspections.append(kwargs.get("follow_symlinks", True))
        return real_stat(candidate, *args, **kwargs)

    events.clear()
    temporary_reads.clear()
    monkeypatch.setattr(Path, "open", open_without_staging)
    monkeypatch.setattr(Path, "stat", inspect)
    assert store.write_immutable_bytes(path, content) == store.sha256_bytes(content)
    assert inspections == [False]
    assert events == ["directory"]
    assert temporary_reads == []
    assert path.stat().st_ino == inode
    assert path.read_bytes() == content


@pytest.mark.parametrize(
    "target", ["file", "directory", "symlink", "dangling", "parent"]
)
def test_immutable_write_rejects_conflicting_or_irregular_target(tmp_path, target):
    directory = tmp_path / "artifacts"
    directory.mkdir()
    path = directory / "record.json"
    original = tmp_path / "original.json"
    original.write_bytes(b"original\n")
    if target == "file":
        path.write_bytes(original.read_bytes())
    elif target == "directory":
        path.mkdir()
    elif target == "symlink":
        path.symlink_to(original)
    elif target == "dangling":
        path.symlink_to(tmp_path / "missing.json")
    else:
        alias = tmp_path / "alias"
        alias.symlink_to(directory, target_is_directory=True)
        path = alias / path.name

    with pytest.raises(store.FeedbackRejected) as rejected:
        store.write_immutable_bytes(path, b"replacement\n")
    assert rejected.value.code == "context_invalid"
    assert original.read_bytes() == b"original\n"
    if target == "file":
        assert path.read_bytes() == b"original\n"
    assert not list(directory.glob("*.tmp"))


@pytest.mark.parametrize("published", [False, True])
@pytest.mark.parametrize(
    "temporary_kind", ["matching", "conflicting", "symlink", "directory"]
)
def test_immutable_write_checks_leftover_temporaries(
    tmp_path, monkeypatch, published, temporary_kind
):
    path = tmp_path / "record.json"
    content = b"immutable\n"
    if published:
        # durability は専用 test で検証し、ここでは保存済み file だけを用意する。
        path.write_bytes(content)
    matching = tmp_path / f".{path.name}.complete.tmp"
    matching.write_bytes(content)
    temporary = tmp_path / f".{path.name}.interrupted.tmp"
    unrelated_paths = [
        tmp_path / ".other.json.interrupted.tmp",
        tmp_path / f"{path.name}.interrupted.tmp",
        tmp_path / f".{path.name}.interrupted.tmp.bak",
    ]
    for unrelated in unrelated_paths:
        unrelated.write_bytes(b"unrelated\n")
    if temporary_kind == "directory":
        temporary.mkdir()
    elif temporary_kind == "symlink":
        temporary.symlink_to(unrelated_paths[0])
    else:
        temporary.write_bytes(content if temporary_kind == "matching" else b"corrupt\n")

    # cleanup 後の directory 同期を観測し、実ディスクの同期待ちは繰り返さない。
    events = []

    def fsync(fd):
        mode = os.fstat(fd).st_mode
        if stat.S_ISDIR(mode):
            assert path.read_bytes() == content
            assert not matching.exists()
            assert not temporary.exists()
            events.append("directory")
        else:
            assert stat.S_ISREG(mode)
            assert not path.exists()
            events.append("file")

    monkeypatch.setattr(os, "fsync", fsync)
    inspections = []
    real_stat = Path.stat

    def inspect(candidate, *args, **kwargs):
        if candidate in (matching, temporary):
            inspections.append((candidate, kwargs.get("follow_symlinks", True)))
        return real_stat(candidate, *args, **kwargs)

    monkeypatch.setattr(Path, "stat", inspect)

    if temporary_kind == "matching":
        assert store.write_immutable_bytes(path, content) == store.sha256_bytes(content)
        # cleanup と assert 内の照会は除き、内容の照合前には symlink を追わない。
        assert set(inspections[:2]) == {(matching, False), (temporary, False)}
        assert events == (["directory"] if published else ["file", "directory"])
        assert path.read_bytes() == content
        assert not matching.exists()
        assert not temporary.exists()
    else:
        with pytest.raises(store.FeedbackRejected) as rejected:
            store.write_immutable_bytes(path, content)
        assert rejected.value.code == "context_invalid"
        assert events == []
        assert matching.read_bytes() == content
        assert temporary.exists()
        assert path.exists() == published
        if published:
            assert path.read_bytes() == content
    for unrelated in unrelated_paths:
        assert unrelated.read_bytes() == b"unrelated\n"


@pytest.mark.parametrize("failure", ["file", "directory"])
def test_immutable_write_retries_flush_failure(tmp_path, monkeypatch, failure):
    path = tmp_path / "record.json"
    content = b"immutable\n"
    failed = False
    events = []

    def fsync(fd):
        nonlocal failed
        kind = "directory" if stat.S_ISDIR(os.fstat(fd).st_mode) else "file"
        events.append(kind)
        if not failed and kind == failure:
            failed = True
            raise OSError("injected flush failure")

    monkeypatch.setattr(os, "fsync", fsync)
    with pytest.raises(OSError, match="injected flush failure"):
        store.write_immutable_bytes(path, content)
    assert path.exists() == (failure == "directory")
    assert not list(tmp_path.glob("*.tmp"))
    inode = path.stat().st_ino if path.exists() else None
    events.clear()

    assert store.write_immutable_bytes(path, content) == store.sha256_bytes(content)
    assert events == (
        ["directory"] if failure == "directory" else ["file", "directory"]
    )
    assert path.read_bytes() == content
    if inode is not None:
        assert path.stat().st_ino == inode


@pytest.mark.parametrize("same_content", [False, True])
def test_concurrent_immutable_writes_do_not_overwrite(tmp_path, same_content):
    path = tmp_path / "record.json"
    contents = [b"first\n", b"first\n" if same_content else b"second\n"]
    started = threading.Barrier(2, timeout=5)

    def write(content):
        started.wait()
        try:
            return store.write_immutable_bytes(path, content)
        except store.FeedbackRejected as rejected:
            assert rejected.code == "context_invalid"
            return None

    with ThreadPoolExecutor(max_workers=2) as writers:
        outcomes = list(writers.map(write, contents))
    stored = path.read_bytes()
    assert stored in contents
    assert outcomes.count(store.sha256_bytes(stored)) == (2 if same_content else 1)
    assert outcomes.count(None) == (0 if same_content else 1)
    assert list(tmp_path.iterdir()) == [path]
