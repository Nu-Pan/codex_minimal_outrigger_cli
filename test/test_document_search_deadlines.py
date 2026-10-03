"""要求の四種類の時計と、回収前後の診断境界を検証する。"""

import fcntl
import json
import os
import shutil
import time
from concurrent.futures import ThreadPoolExecutor
from contextlib import closing
from dataclasses import replace
from pathlib import Path

import pytest
from oracle.other.document_search import DocumentSearchConfig
from test_document_search import _InferenceDouble, _repo_with_docs, _tuning

from commons import runtime_document_search as search_module
from commons.runtime_config import write_config
from commons.runtime_document_search import DocumentSearch, SearchError, _file_lock
from commons.runtime_document_search_observation import (
    SearchLogContext,
    SearchObservation,
    mcp_tool_timeout_seconds,
)
from commons.runtime_document_search_worker import NodeSearchWorker
from commons.runtime_paths import config_path
from config.cmoc_config import CmocConfig


def _observation(tmp_path, *, request=True):
    events = []

    def record(kind, payload):
        events.append(json.loads(json.dumps({"event": kind, **payload})))

    observation = SearchObservation(tmp_path, record, request=request)
    return observation, events


@pytest.mark.parametrize(
    ("kind", "setting"),
    [
        ("resource_wait", "resource_wait_timeout_seconds"),
        ("sync_no_progress", "sync_no_progress_timeout_seconds"),
        ("post_sync_search", "post_sync_search_timeout_seconds"),
        ("search_request", "search_request_timeout_seconds"),
    ],
)
def test_each_deadline_records_decision_before_cleanup(
    tmp_path, document_search_clock, kind, setting
):
    observation, events = _observation(tmp_path)
    observation.configure(
        replace(DocumentSearchConfig(), **{setting: 10.0}), bounded=True
    )
    progress = observation.begin_sync()
    progress.update(document_count=3, persisted_chunks=1, reused_embeddings=2)
    if kind == "resource_wait":
        observation.start_wait()
    if kind == "post_sync_search":
        observation.finish_sync("updated")
        observation.start_post_sync()
    document_search_clock.advance(10)

    with pytest.raises(SearchError) as failure:
        observation.check()
    assert failure.value.code == "DEADLINE_EXCEEDED"
    diagnostic = events[-1]
    assert diagnostic["event"] == "document_search_deadline_exceeded"
    assert diagnostic["deadline_kinds"] == [kind]
    assert diagnostic["measured_seconds"][kind] == 10
    assert diagnostic["last_progress"] is None
    assert diagnostic["progress"]["document_count"] == 3
    assert diagnostic["progress"]["persisted_chunks"] == 1
    if kind == "resource_wait":
        observation.end_wait()
    document_search_clock.advance(3)
    observation.finish_sync()
    observation.finish_request()

    terminal = events[-1]
    assert terminal["elapsed_seconds"] == 13
    assert terminal["cleanup_seconds"] == 3
    assert terminal["decision_seconds"][kind] == 10
    assert terminal["status"] == "deadline_exceeded"
    assert terminal["failure_code"] == "DEADLINE_EXCEEDED"
    if kind != "post_sync_search":
        sync = events[-2]
        assert sync["counts_complete"] is False
        assert sync["persisted_chunk_count"] == 1
        assert sync["checked_document_count"] is None
        assert sync["no_progress_seconds"] == (0 if kind == "resource_wait" else 10)
        assert sync["cleanup_seconds"] == 3
        assert terminal["decision_seconds"]["post_sync_search"] is None


def test_wait_union_pauses_no_progress_and_duplicate_progress_does_not_reset_it(
    tmp_path, document_search_clock
):
    observation, events = _observation(tmp_path)
    observation.configure(
        replace(DocumentSearchConfig(), sync_no_progress_timeout_seconds=10),
        bounded=True,
    )
    observation.begin_sync()
    document_search_clock.advance(3)
    observation.start_wait()
    document_search_clock.advance(7)
    observation.start_wait()
    document_search_clock.advance(5)
    observation.end_wait()
    document_search_clock.advance(3)
    observation.check()
    assert observation.measurements()["resource_wait"] == 15
    assert observation.measurements()["sync_no_progress"] == 3
    observation.end_wait()
    document_search_clock.advance(6)
    observation.progress("document_checked", "a.md")
    document_search_clock.advance(4)
    observation.progress("document_checked", "a.md")
    document_search_clock.advance(6)
    with pytest.raises(SearchError):
        observation.check()
    observation.finish_sync()
    observation.finish_request()
    diagnostic = next(
        e for e in events if e["event"] == "document_search_deadline_exceeded"
    )
    assert diagnostic["measured_seconds"]["resource_wait"] == 15
    assert diagnostic["measured_seconds"]["sync_no_progress"] == 10
    assert diagnostic["last_progress"]["sync_elapsed_seconds"] == 24
    assert events[-2]["longest_no_progress_seconds"] == 10


def test_progress_keeps_longest_interval_and_resync_keeps_parent_clocks(
    tmp_path, document_search_clock
):
    observation, events = _observation(tmp_path)
    observation.configure(DocumentSearchConfig(), bounded=True)
    observation.begin_sync()
    document_search_clock.advance(400)
    observation.progress("document_checked", "a.md")
    document_search_clock.advance(1)
    observation.finish_sync("updated")
    assert events[-1]["no_progress_seconds"] == 1
    assert events[-1]["longest_no_progress_seconds"] == 400
    observation.start_post_sync()
    observation.start_wait()
    document_search_clock.advance(5)
    observation.end_wait()
    for number in range(2):
        observation.begin_sync()
        document_search_clock.advance(2)
        observation.progress("embedding_saved", f"a.md:{number}")
        observation.finish_sync("updated")
        observation.start_post_sync()
    measured = observation.measurements()
    assert measured["search_request"] == 410
    assert measured["post_sync_search"] == 9
    assert measured["resource_wait"] == 5
    observation.decide_success()
    observation.finish_request()
    sync_starts = [e for e in events if e["event"] == "document_search_sync_started"]
    assert [e["sync_sequence"] for e in sync_starts] == [1, 2, 3]
    assert len({e["sync_id"] for e in sync_starts}) == 3
    assert events[-1]["sync_ids"] == [e["sync_id"] for e in sync_starts]


def test_simultaneous_deadlines_and_cleanup_failure_preserve_original_reason(
    tmp_path, document_search_clock
):
    observation, events = _observation(tmp_path)
    observation.configure(
        replace(DocumentSearchConfig(), search_request_timeout_seconds=600),
        bounded=True,
    )
    observation.begin_sync()
    document_search_clock.advance(600)
    with pytest.raises(SearchError):
        observation.check()
    assert set(events[-1]["deadline_kinds"]) == {"search_request", "sync_no_progress"}
    document_search_clock.advance(2)
    observation.fail(OSError("cleanup failed"))
    observation.finish_sync()
    observation.finish_request()
    assert events[-1]["status"] == events[-2]["status"] == "failed"
    assert (
        events[-1]["failure_code"] == events[-2]["failure_code"] == "DEADLINE_EXCEEDED"
    )
    assert events[-1]["cleanup_failure"] == "cleanup failed"
    assert events[-1]["decision_seconds"]["search_request"] == 600


def test_progressing_sync_can_outlast_component_timeout_and_600_seconds(
    tmp_path, document_search_clock
):
    root = _repo_with_docs(tmp_path)
    (root / "oracle/doc/second.md").write_text("# 次の原文\n")
    observation, events = _observation(root)

    class ProgressingWorker(_InferenceDouble):
        def stream_chunks(self, documents, resumes, on_event, **kwargs):
            def progress(event):
                document_search_clock.advance(400)
                on_event(event)

            super().stream_chunks(documents, resumes, progress, **kwargs)

    config = replace(_tuning(), request_timeout_seconds=1)
    with closing(
        DocumentSearch(
            root,
            config,
            worker=ProgressingWorker(),
            installation_root=tmp_path,
        )
    ) as search:
        result = search.search("原文", observation=observation)
    assert result["status"] == "ok" and result["hits"]
    assert events[-1]["elapsed_seconds"] == 1600
    assert events[-1]["deadline_limits"]["search_request"] == 3600
    sync = next(e for e in events if e["event"] == "document_search_sync_finished")
    assert sync["checked_document_count"] == 2
    assert sync["persisted_chunk_count"] == 2
    assert sync["no_progress_seconds"] == 0
    assert sync["longest_no_progress_seconds"] == 400


def test_doctor_sync_has_no_search_deadlines(tmp_path, document_search_clock):
    root = _repo_with_docs(tmp_path)
    (root / "oracle/doc/second.md").write_text("# 次の原文\n")
    events = []

    class SlowWorker(_InferenceDouble):
        def stream_chunks(self, *args, **kwargs):
            assert kwargs["deadline"] is None
            document_search_clock.advance(10000)
            super().stream_chunks(*args, **kwargs)

    with closing(
        DocumentSearch(
            root,
            _tuning(),
            worker=SlowWorker(),
            installation_root=tmp_path,
            event_sink=lambda kind, payload: events.append({"event": kind, **payload}),
        )
    ) as search:
        assert search.synchronize(unbounded=True).chunk_count == 2
    assert [event["event"] for event in events] == [
        "document_search_sync_started",
        "document_search_sync_finished",
    ]
    assert events[-1]["elapsed_seconds"] == 10000
    assert events[-1]["no_progress_seconds"] is None


@pytest.mark.parametrize(
    "setting", ["search_request_timeout_seconds", "shutdown_grace_seconds"]
)
def test_saved_deadline_growth_requires_a_new_codex_connection(tmp_path, setting):
    root = _repo_with_docs(tmp_path)
    initial = _tuning()
    write_config(config_path(root), CmocConfig(document_search=initial))
    events = []
    with closing(
        DocumentSearch(
            root,
            initial,
            worker=_InferenceDouble(),
            use_saved_config=True,
            tool_timeout_seconds=mcp_tool_timeout_seconds(initial),
            event_sink=lambda kind, payload: events.append({"event": kind, **payload}),
        )
    ) as search:
        assert search.search("原文")["status"] == "ok"
        previous_identity = search.sync_progress["identity"]
        lowered = replace(initial, search_request_timeout_seconds=1000)
        write_config(config_path(root), CmocConfig(document_search=lowered))
        assert search.search("原文")["status"] == "ok"
        assert search.sync_progress["identity"] == previous_identity
        assert events[-1]["deadline_limits"]["search_request"] == 1000
        unsafe = replace(initial, **{setting: getattr(initial, setting) + 1})
        write_config(config_path(root), CmocConfig(document_search=unsafe))
        events.clear()
        with pytest.raises(SearchError, match="new Codex call") as failure:
            search.search("原文")
        assert failure.value.code == "NOT_READY"
        assert [event["event"] for event in events] == [
            "document_search_request_started",
            "document_search_request_finished",
        ]
        assert events[-1]["sync_ids"] == []
        assert events[-1]["status"] == "failed"


def test_parallel_requests_log_to_their_own_codex_calls(tmp_path):
    root = _repo_with_docs(tmp_path)
    path = tmp_path / "caller.jsonl"
    path.touch()

    class SlowWorker(_InferenceDouble):
        def stream_chunks(self, *args, **kwargs):
            time.sleep(0.1)
            super().stream_chunks(*args, **kwargs)

    def search_call(call_id):
        sink = SearchLogContext(path, "tui", "exec_test", call_id)
        with closing(
            DocumentSearch(
                root,
                _tuning(),
                worker=SlowWorker(),
                installation_root=tmp_path,
                event_sink=sink.event,
            )
        ) as search:
            return search.search("原文")

    with ThreadPoolExecutor(max_workers=2) as executor:
        assert all(
            value["status"] == "ok"
            for value in executor.map(search_call, ("cc_a", "cc_b"))
        )
    events = [json.loads(line) for line in path.read_text().splitlines()]
    assert len(events) == 10
    starts = [e for e in events if e["event"] == "document_search_request_started"]
    assert len({e["request_id"] for e in starts}) == 2
    identities = set()
    for start in starts:
        records = [e for e in events if e["request_id"] == start["request_id"]]
        assert all(e["codex_call_id"] == start["codex_call_id"] for e in records)
        assert records[-1]["status"] == "succeeded"
        sync = next(e for e in records if e["event"] == "document_search_sync_finished")
        identities.add(sync["index_identity"])
        assert sync["sync_id"] == records[-1]["sync_ids"][0]
    assert len(identities) == 1


def test_timeout_keeps_confirmed_reuse_counts_and_processing_state(
    tmp_path, document_search_clock, monkeypatch
):
    root = _repo_with_docs(tmp_path)
    (root / "oracle/doc/second.md").write_text("# 次の原文\n")
    events = []

    def record(kind, payload):
        events.append(json.loads(json.dumps({"event": kind, **payload})))

    with closing(
        DocumentSearch(
            root,
            _tuning(),
            worker=_InferenceDouble(),
            event_sink=record,
        )
    ) as search:
        search.synchronize(unbounded=True)
        events.clear()
        checked = search_module._checked_cached_vector
        calls = 0

        def stalled_check(value):
            nonlocal calls
            calls += 1
            document_search_clock.advance(700 if calls == 2 else 1)
            return checked(value)

        monkeypatch.setattr(search_module, "_checked_cached_vector", stalled_check)
        with pytest.raises(SearchError) as failure:
            search.search("原文")
        assert failure.value.code == "DEADLINE_EXCEEDED"
    diagnostic = next(
        event
        for event in events
        if event["event"] == "document_search_deadline_exceeded"
    )
    progress = diagnostic["progress"]
    assert progress["reused_embeddings"] == 1
    assert progress["checked_document_count"] == 1
    assert progress["changed_document_count"] == 0
    assert progress["document_states"] == {
        "oracle/doc/allowed.md": "checked",
        "oracle/doc/second.md": "processing",
    }
    assert events[-2]["reused_chunk_count"] == 1
    assert events[-2]["counts_complete"] is False


@pytest.mark.skipif(shutil.which("node") is None, reason="Node.js is unavailable")
def test_deadline_keeps_locks_until_worker_and_descendant_stop(tmp_path):
    base = tmp_path / "worker"
    base.mkdir()
    (base / "worker.mjs").write_text(
        'import fs from "node:fs"; import { spawn } from "node:child_process";\n'
        'process.on("SIGTERM", () => {});\n'
        'const child = spawn(process.execPath, ["-e", '
        "'process.on(\"SIGTERM\", () => {}); setInterval(() => {}, 1000);'"
        '], {stdio: "ignore"});\n'
        'fs.writeFileSync("pids.json", JSON.stringify([process.pid, child.pid]));\n'
        "setInterval(() => {}, 1000);\n"
    )
    observation, events = _observation(tmp_path)
    config = replace(
        _tuning(), sync_no_progress_timeout_seconds=0.4, shutdown_grace_seconds=0.15
    )
    observation.configure(config, bounded=True)
    observation.begin_sync()
    locks = [tmp_path / "index.lock", tmp_path / "model.lock"]

    def before_stop(failure):
        observation.fail(failure)
        assert events[-1]["event"] == "document_search_deadline_exceeded"
        parent, _ = json.loads((base / "pids.json").read_text())
        os.kill(parent, 0)
        for path in locks:
            with path.open("rb") as stream:
                with pytest.raises(BlockingIOError):
                    fcntl.flock(stream.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)

    worker = NodeSearchWorker(
        tmp_path,
        config,
        material_base=base,
        check=observation.check,
        on_failure=before_stop,
    )
    with pytest.raises(SearchError) as failure:
        with _file_lock(locks[0], None, observation=observation):
            with _file_lock(locks[1], None, observation=observation) as descriptor:
                worker.stream_chunks(
                    {"doc.md": "text"},
                    {"doc.md": 0},
                    lambda _: None,
                    reusable_hashes=set(),
                    deadline=None,
                    residency_fd=descriptor,
                )
    assert failure.value.code == "DEADLINE_EXCEEDED"
    observation.finish_sync()
    observation.finish_request()
    parent, descendant = json.loads((base / "pids.json").read_text())
    with pytest.raises(ProcessLookupError):
        os.kill(parent, 0)
    descendant_stat = Path(f"/proc/{descendant}/stat")
    try:
        state = descendant_stat.read_text().rsplit(") ", 1)[1].split()[0]
    except FileNotFoundError:
        state = None
    assert state in {None, "Z", "X", "x"}
    assert events[-1]["cleanup_seconds"] >= 0.1
    assert events[-1]["decision_seconds"]["post_sync_search"] is None
    assert (
        events[-1]["elapsed_seconds"] > events[-1]["decision_seconds"]["search_request"]
    )
