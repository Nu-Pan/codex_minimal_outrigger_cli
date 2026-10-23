"""確定済み history の参照・内容検証を Git や CLI の準備なしで確かめる。"""

import json
from pathlib import Path

import pytest

from commons.runtime_errors import CmocError
from commons.runtime_feedback_history import load_history
from commons.runtime_feedback_state import (
    ActiveState,
    agent_canonical_key,
    issue_id,
    machine_canonical_key,
)
from commons.runtime_feedback_store import canonical_json_bytes, sha256_bytes
from sub_commands.feedback import report


@pytest.fixture
def history_input(tmp_path):
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
    return tmp_path, path, record


def _save_history(root, path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(content)
    return {
        "path": path.relative_to(root).as_posix(),
        "sha256": sha256_bytes(content),
    }


@pytest.fixture
def saved_history(history_input):
    root, path, record = history_input
    reference = _save_history(root, path, canonical_json_bytes(record))
    return root, path, record, reference


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
def test_history_load_rejects_corruption(history_input, fault, message):
    root, path, record = history_input
    if fault == "schema":
        content = canonical_json_bytes({**record, "schema_version": 2})
    elif fault == "invalid_json":
        content = b"{"
    else:
        content = json.dumps(record).encode()
    # 拒否対象だけを保存し、直後に上書きする正常 file は準備しない。
    reference = _save_history(root, path, content)

    with pytest.raises(CmocError, match=message):
        load_history(root, [reference])


def test_history_load_rejects_duplicate_paths(saved_history):
    root, _, _, reference = saved_history

    with pytest.raises(CmocError, match="path が重複または不正"):
        load_history(root, [reference, reference])


@pytest.mark.parametrize(
    "field, value, message",
    [
        ("path", None, "path"),
        ("path", "/outside.json", "path"),
        ("path", ".cmoc/gu/feedback/history/nested/record.json", "path"),
        ("path", ".cmoc/gu/feedback/history/../record.json", "path"),
        ("path", ".cmoc/gu/feedback/elsewhere/record.json", "path"),
        ("sha256", None, "SHA256"),
        ("sha256", "invalid", "SHA256"),
    ],
)
def test_history_load_rejects_invalid_references_before_reading(
    history_input, monkeypatch, field, value, message
):
    root, path, record = history_input
    # 参照は内容の読込前に拒否されるため、directory と file は不要。
    reference = {
        "path": path.relative_to(root).as_posix(),
        "sha256": sha256_bytes(canonical_json_bytes(record)),
        field: value,
    }
    monkeypatch.setattr(
        Path,
        "read_bytes",
        lambda _path: pytest.fail("invalid reference must not be read"),
    )

    with pytest.raises(CmocError, match=message):
        load_history(root, [reference])


@pytest.mark.parametrize("root_kind", ["relative", "symlink"])
def test_history_load_preserves_reference_order_with_repository_aliases(
    saved_history, monkeypatch, root_kind
):
    root, path, record, reference = saved_history
    next_record = {
        **record,
        "generation_id": "fbg_000002_2026-10-08_00-00",
        "created_at": "2026-10-09T00:00:00Z",
    }
    next_path = path.with_name(f"{next_record['generation_id']}.json")
    content = canonical_json_bytes(next_record)
    next_reference = _save_history(root, next_path, content)
    if root_kind == "relative":
        monkeypatch.chdir(root)
        repository = Path(".")
    else:
        repository = root / "repository-alias"
        repository.symlink_to(root, target_is_directory=True)

    # timestamp や directory 順ではなく、確定済み参照の順に採用する。
    assert load_history(repository, [next_reference, reference]) == [
        next_record,
        record,
    ]
    assert load_history(repository, [reference, next_reference]) == [
        record,
        next_record,
    ]


@pytest.mark.parametrize("link_kind", ["file", "directory"])
def test_history_load_rejects_symlink_before_reading(
    saved_history, monkeypatch, link_kind
):
    root, path, _, reference = saved_history
    if link_kind == "file":
        alias = path.with_name("alias.json")
        alias.symlink_to(path)
        reference["path"] = alias.relative_to(root).as_posix()
    else:
        saved = path.parent.with_name("saved-history")
        path.parent.rename(saved)
        path.parent.symlink_to(saved, target_is_directory=True)
    monkeypatch.setattr(
        Path, "read_bytes", lambda _path: pytest.fail("symlink target must not be read")
    )

    with pytest.raises(CmocError, match="symlink"):
        load_history(root, [reference])


def test_publication_history_maps_consumed_inputs_without_repeated_scans(
    history_input, monkeypatch
):
    """入力の採用先を保ち、観測ごとの候補・入力一覧の再走査を検出する。"""
    root, _, record = history_input
    scan_steps = 0

    class ScannedList(list):
        def __iter__(self):
            nonlocal scan_steps
            for value in super().__iter__():
                scan_steps += 1
                yield value

        def __contains__(self, value):
            return any(item == value for item in self)

    # hash・schema の検証と破損時の publication 阻止は test_feedback.py に残す。
    # ここでは検証済み入力の対応付けと、実 history の schema・canonical byte 列を検査する。
    observations = {}
    entries = ScannedList()
    for index in range(69):
        identity = f"fbo_{index:06d}_2026-10-08_00-00"
        observations[identity] = {"source": "agent_report"}
        entries.append(
            {
                "observation_id": identity,
                "path": f".cmoc/gu/feedback/observation/v1/2026-10-08/{identity}.json",
                "sha256": f"{index:064x}",
            }
        )
    agent_ids = list(observations)[:64]
    machine_ids = list(observations)[64:68]
    for identity, subject in zip(
        machine_ids,
        (
            "reporter:missing",
            "reporter:missing",
            "collector:missing",
            "transport:missing",
        ),
        strict=True,
    ):
        observations[identity] = {
            "source": "machine_rule",
            "payload": {
                "rule_id": "feedback.reporter_unavailable.v1",
                "subject_type": "reporter_component",
                "normalized_subject_id": subject,
            },
        }
    machine_key = machine_canonical_key(observations[machine_ids[0]])
    aggregate_key = machine_canonical_key(observations[machine_ids[2]])
    agent_key = agent_canonical_key(agent_ids[0])
    agent_issue, machine_issue = issue_id(agent_key), issue_id(machine_key)
    candidates = {
        agent_issue: {
            "canonical_key": agent_key,
            "summary": "agent issue",
            "source_observation_ids": ScannedList(reversed(agent_ids)),
        },
        machine_issue: {
            "canonical_key": machine_key,
            "summary": "machine issue",
            # 一件は source ID と key の両方に一致し、もう一件は key だけに一致する。
            "source_observation_ids": ScannedList(machine_ids[:1]),
        },
    }
    manifest = {
        "inputs": {"references": [], "observations": entries},
        "run": {
            "invocation_log": record["log"],
            "targets": {"case_ids": dict.fromkeys(candidates)},
        },
    }
    verdicts = {
        identity: {
            "status": "not_actionable",
            "reason": "確認済み",
            "current_evidence": [],
        }
        for identity in candidates
    }
    # 読込順に依存せず canonical order へ並べ、未採用の machine／agent 入力を残す。
    monkeypatch.setattr(
        report,
        "_read_cut_observations",
        lambda *_args: dict(reversed(observations.items())),
    )

    _, content, reference = report._publication_history(
        root,
        manifest,
        ActiveState(None, None, {}, {}, None, None),
        candidates,
        verdicts,
        {},
        {aggregate_key: {}},
        record["source"],
        record["generation_id"],
        record["created_at"],
        root / record["report"],
    )

    history = json.loads(content)
    expected = [
        {
            **entry,
            "issue_ids": [agent_issue]
            if entry["observation_id"] in agent_ids
            else [machine_issue]
            if entry["observation_id"] in machine_ids[:2]
            else [],
            "aggregate_keys": [aggregate_key]
            if entry["observation_id"] == machine_ids[2]
            else [],
        }
        for entry in entries[:-2]
    ]
    assert history["observations"] == expected
    assert reference["sha256"] == sha256_bytes(content)
    assert content == canonical_json_bytes(history)
    # 時間閾値ではなく走査量で、入力数に比例する処理と二乗の再走査を区別する。
    assert scan_steps <= 4 * (len(entries) + len(agent_ids) + 1)
