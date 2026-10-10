"""確定済み history の参照・内容検証を Git や CLI の準備なしで確かめる。"""

import json
from pathlib import Path

import pytest

from commons.runtime_errors import CmocError
from commons.runtime_feedback_history import load_history
from commons.runtime_feedback_store import canonical_json_bytes, sha256_bytes


@pytest.fixture
def saved_history(tmp_path):
    generation = "fbg_000001_2026-10-08_00-00"
    record = {
        "schema_version": 1,
        "generation_id": generation,
        "source": {
            "kind": "report",
            "id": "fbc_019fbb94-cc00-7000-8000-000000000001",
            "execution_id": "exec_000001_2026-10-08_00-00",
        },
        "created_at": "2026-10-08T00:00:00Z",
        "report": ".cmoc/gu/report/feedback/exec_000001_2026-10-08_00-00.md",
        "log": ".cmoc/gu/log/sub_command/exec_000001_2026-10-08_00-00.jsonl",
        "events": [],
        "observations": [],
    }
    path = tmp_path / ".cmoc/gu/feedback/history" / f"{generation}.json"
    path.parent.mkdir(parents=True)
    content = canonical_json_bytes(record)
    path.write_bytes(content)
    reference = {
        "path": path.relative_to(tmp_path).as_posix(),
        "sha256": sha256_bytes(content),
    }
    return tmp_path, path, record, reference


def test_history_load_uses_hash_verified_bytes_and_ignores_staged_history(
    saved_history, monkeypatch
):
    root, path, record, reference = saved_history
    (path.parent / "unpublished.json").write_text("invalid staged history")
    replacement = canonical_json_bytes({**record, "created_at": "2026-10-09T00:00:00Z"})
    original_read = Path.read_bytes

    def replace_after_read(candidate):
        content = original_read(candidate)
        if candidate == path:
            candidate.write_bytes(replacement)
        return content

    monkeypatch.setattr(Path, "read_bytes", replace_after_read)

    # hash を検証した byte 列を採用し、その後の置換内容を混ぜない。
    assert load_history(root, [reference]) == [record]
    with pytest.raises(CmocError, match="SHA256"):
        load_history(root, [reference])


@pytest.mark.parametrize(
    "fault, message",
    [
        ("schema", "identity"),
        ("noncanonical", "canonical JSON object"),
        ("invalid_json", "canonical JSON"),
    ],
)
def test_history_load_rejects_corruption(saved_history, fault, message):
    root, path, record, reference = saved_history
    if fault == "schema":
        content = canonical_json_bytes({**record, "schema_version": 2})
    elif fault == "invalid_json":
        content = b"{"
    else:
        content = json.dumps(record).encode()
    path.write_bytes(content)
    reference["sha256"] = sha256_bytes(content)

    with pytest.raises(CmocError, match=message):
        load_history(root, [reference])


@pytest.mark.parametrize("fault", ["duplicate", "nested"])
def test_history_load_rejects_duplicate_or_nested_paths(saved_history, fault):
    root, path, _, reference = saved_history
    references = [reference, reference]
    if fault == "nested":
        nested = path.parent / "nested" / path.name
        nested.parent.mkdir()
        nested.write_bytes(path.read_bytes())
        references = [{**reference, "path": nested.relative_to(root).as_posix()}]

    with pytest.raises(CmocError, match="path が重複または不正"):
        load_history(root, references)
