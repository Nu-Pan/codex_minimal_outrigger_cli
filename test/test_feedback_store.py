"""feedback artifact と mutable state の durability・再保存を検証する。

同期の順序・失敗・再試行の検査では、実 fd と file 内容を観測し、ディスク同期を待たない。
実 fsync との結合は、残存 temporary・並行保存の正常系と test_feedback.py の
collector 受理・後続 wave の publication 検査に残す。

対応する oracle file:

- `{{work-root}}/oracle/doc/app_spec/feedback_state.md`
- `{{work-root}}/oracle/doc/app_spec/feedback_observation.md`
"""

import os
import stat
import threading
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import pytest

import commons.runtime_feedback_state as state
import commons.runtime_feedback_store as store


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


def test_immutable_write_flushes_new_data_and_reuses_published_inode(
    tmp_path, monkeypatch
):
    path = tmp_path / "artifacts" / "record.json"
    content = store.canonical_json_bytes({"evidence": "確認した内容"})
    events = []
    temporary_reads = []
    real_rename = os.rename
    real_read, real_open = Path.read_bytes, Path.open

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

    events.clear()
    temporary_reads.clear()
    monkeypatch.setattr(Path, "open", open_without_staging)
    assert store.write_immutable_bytes(path, content) == store.sha256_bytes(content)
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
    tmp_path, published, temporary_kind
):
    path = tmp_path / "record.json"
    content = b"immutable\n"
    if published:
        # durability は専用 test で検証し、ここでは保存済み file だけを用意する。
        path.write_bytes(content)
    temporary = tmp_path / f".{path.name}.interrupted.tmp"
    unrelated = tmp_path / ".other.json.interrupted.tmp"
    unrelated.write_bytes(b"unrelated\n")
    if temporary_kind == "directory":
        temporary.mkdir()
    elif temporary_kind == "symlink":
        temporary.symlink_to(unrelated)
    else:
        temporary.write_bytes(content if temporary_kind == "matching" else b"corrupt\n")

    if temporary_kind == "matching":
        assert store.write_immutable_bytes(path, content) == store.sha256_bytes(content)
        assert path.read_bytes() == content
        assert not temporary.exists()
    else:
        with pytest.raises(store.FeedbackRejected) as rejected:
            store.write_immutable_bytes(path, content)
        assert rejected.value.code == "context_invalid"
        assert temporary.exists()
        assert path.exists() == published
        if published:
            assert path.read_bytes() == content
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
