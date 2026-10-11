"""intake の参照検証と境界を Git・CLI の準備なしで確かめる。"""

from collections import Counter
from pathlib import Path

import pytest

from commons.runtime_errors import CmocError
from commons.runtime_feedback_intake import (
    capture_high_watermark,
    record_observation_receipt,
)
from commons.runtime_feedback_store import (
    canonical_json_bytes,
    feedback_root,
    observation_path,
    observation_publication_lock,
    read_json_object,
    sha256_bytes,
)


def _raw_input(root, identity, observed_at="2026-10-08T00:00:00Z"):
    # envelope schema は store・wave のテストが検査し、ここでは receipt の内容を扱う。
    path = observation_path(root, identity, observed_at)
    path.parent.mkdir(parents=True, exist_ok=True)
    content = canonical_json_bytes({"observation_id": identity})
    path.write_bytes(content)
    return path, {
        "path": path.relative_to(root).as_posix(),
        "sha256": sha256_bytes(content),
    }


@pytest.fixture
def pending_receipt(tmp_path):
    path, reference = _raw_input(tmp_path, "fbo_" + "1" * 32)
    with observation_publication_lock(tmp_path):
        record_observation_receipt(tmp_path, path)
    return tmp_path, path, reference


def test_capture_reads_each_raw_once_and_preserves_receipt_order(
    pending_receipt, monkeypatch
):
    root, received, _ = pending_receipt
    # raw 保存直後に停止した入力は、ID・日時が古くても今回の受理順序へ追加する。
    orphan, reference = _raw_input(root, "fbo_" + "0" * 32, "2026-10-07T00:00:00Z")
    reads = Counter()
    original_read = Path.read_bytes

    def counted_read(path):
        if path in {received, orphan}:
            reads[path] += 1
        return original_read(path)

    monkeypatch.setattr(Path, "read_bytes", counted_read)

    assert capture_high_watermark(root, 1) == (
        2,
        [{"observation_id": orphan.stem, **reference}],
    )
    assert reads == {received: 1, orphan: 1}
    ledger = read_json_object(feedback_root(root) / "intake.json")
    assert ledger["pending"][received.stem]["sequence"] == 1
    assert ledger["pending"][orphan.stem]["sequence"] == 2
    # 再登録では境界を増やさず、呼び出しを跨いだ検証結果の cache は持たない。
    assert capture_high_watermark(root, 2) == (2, [])
    assert reads == {received: 2, orphan: 2}


@pytest.mark.parametrize(
    "fault", ["hash", "missing", "symlink", "duplicate_path", "receipt_root"]
)
def test_capture_rejects_corrupt_receipt_even_before_requested_boundary(
    pending_receipt, fault
):
    root, raw, _ = pending_receipt
    ledger_path = feedback_root(root) / "intake.json"
    content = raw.read_bytes()
    if fault == "hash":
        raw.write_bytes(canonical_json_bytes({"changed": True}))
    elif fault == "missing":
        raw.unlink()
    elif fault == "symlink":
        target = root / "alias-target.json"
        target.write_bytes(content)
        raw.unlink()
        raw.symlink_to(target)
    elif fault == "receipt_root":
        outside = root / raw.name
        raw.rename(outside)
        ledger = read_json_object(ledger_path)
        ledger["pending"][raw.stem]["path"] = outside.relative_to(root).as_posix()
        ledger_path.write_bytes(canonical_json_bytes(ledger))
    else:
        duplicate, _ = _raw_input(root, raw.stem, "2026-10-09T00:00:00Z")
        assert duplicate.read_bytes() == content

    original_ledger = ledger_path.read_bytes()
    with pytest.raises(CmocError):
        capture_high_watermark(root, 1)
    assert ledger_path.read_bytes() == original_ledger


def test_new_receipt_rejects_raw_outside_observation_store(tmp_path):
    raw, _ = _raw_input(tmp_path, "fbo_" + "1" * 32)
    outside = tmp_path / raw.name
    raw.rename(outside)

    with observation_publication_lock(tmp_path):
        with pytest.raises(CmocError, match="期待 root 外"):
            record_observation_receipt(tmp_path, outside)
    assert outside.is_file()
    assert not (feedback_root(tmp_path) / "intake.json").exists()
