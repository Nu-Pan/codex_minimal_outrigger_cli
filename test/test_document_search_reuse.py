"""文書入力片の repository 内再利用と、生成・再利用元の診断を検証する。"""

import json
import shutil
import sqlite3
from concurrent.futures import ThreadPoolExecutor
from contextlib import closing
from dataclasses import replace

import pytest
from _git_support import RUN_BRANCH, RUN_ID, SESSION_ID, run_git
from test_document_search import (
    _fake_node_model,
    _InferenceDouble,
    _repo_with_docs,
    _tuning,
)

from commons.runtime_document_search import (
    DocumentSearch,
    SearchError,
)
from commons.runtime_document_search_types import SEARCH_MATERIALS
from commons.runtime_document_search_worker import NodeSearchWorker
from commons.runtime_git import ensure_cmoc_ignored, remove_worktree
from commons.runtime_paths import repo_root


@pytest.fixture
def model_search(tmp_path, monkeypatch):
    """製品の分割・stream・保存を使い、モデル呼出し入力だけを記録する。"""
    if shutil.which("node") is None:
        pytest.skip("Node.js is unavailable")
    from commons import runtime_document_search_worker as worker_module

    runtime = tmp_path / "model"
    runtime.mkdir()
    _fake_node_model(runtime)
    monkeypatch.setenv(
        "CMOC_TEST_DIMENSIONS", str(SEARCH_MATERIALS.embedding_dimensions)
    )
    monkeypatch.setattr(worker_module, "verify_search_materials", lambda *_: runtime)

    def create(root, config=None, events=None):
        config = config or _tuning()
        installation = repo_root(root)
        return DocumentSearch(
            root,
            config,
            worker=NodeSearchWorker(installation, config, material_base=runtime),
            installation_root=installation,
            event_sink=(
                lambda kind, payload: events.append(
                    json.loads(json.dumps({"event": kind, **payload}))
                )
            )
            if events is not None
            else None,
        )

    def inputs():
        path = runtime / "embedding-inputs.jsonl"
        return (
            [json.loads(line) for line in path.read_text().splitlines()]
            if path.exists()
            else []
        )

    return create, inputs


def _worktree(repository, path, branch=None):
    path.parent.mkdir(parents=True, exist_ok=True)
    args = ("-b", branch) if branch else ("--detach",)
    run_git(repository, "worktree", "add", *args, str(path), "HEAD")
    ensure_cmoc_ignored(path)
    return path


def test_new_run_uses_stale_repository_cache_and_current_locations(
    tmp_path, model_search
):
    create, inputs = model_search
    root = _repo_with_docs(tmp_path)
    original = (root / "oracle/doc/allowed.md").read_text()
    events = []
    with closing(create(root)) as search:
        search.synchronize(unbounded=True)
    assert inputs() == [original]

    # 元索引を最新化せず、接続先だけの配置と検索対象を再構築する。
    (root / "oracle/doc/allowed.md").write_text("# 再利用元だけの未同期本文\n")
    run = _worktree(root, tmp_path / "run")
    (run / "oracle/doc/allowed.md").rename(run / "oracle/doc/moved.md")
    (run / "oracle/doc/copy.md").write_text(original)
    with closing(create(run, events=events)) as search:
        result = search.synchronize()
        assert result.chunk_count == result.reused_embeddings == 2
        assert search.sync_progress["generated_embeddings"] == 0
        assert search.sync_progress["reused_other_worktree"] == 2
        assert inputs() == [original]
        assert {hit["path"] for hit in search.search("原文")["hits"]} == {
            "oracle/doc/moved.md",
            "oracle/doc/copy.md",
        }
        search.synchronize()
        assert search.sync_progress["reused_other_worktree"] == 2
        assert search.sync_progress["reused_same_worktree"] == 0
    finished = [
        event for event in events if event["event"] == "document_search_sync_finished"
    ]
    assert all(event["generated_embedding_count"] == 0 for event in finished)
    assert finished[-1]["reuse_count_unit"] == "chunk_occurrence"
    assert (
        root / "oracle/doc/allowed.md"
    ).read_text() == "# 再利用元だけの未同期本文\n"


def test_partial_edit_generates_unique_missing_inputs_and_retains_unreferenced_cache(
    tmp_path, model_search
):
    create, inputs = model_search
    root = _repo_with_docs(tmp_path)
    path = root / "oracle/doc/allowed.md"
    a, b, changed = "# A\nold\n", "# B\nstable\n", "# A\nnew\n"
    path.write_text(a + b)
    events = []
    with closing(create(root, events=events)) as search:
        search.synchronize()
        path.write_text(changed + b + changed)
        (path.parent / "copy.md").write_text(changed)
        search.synchronize()
        assert inputs() == [a, b, changed]
        assert search.sync_progress["generated_embeddings"] == 1
        assert search.sync_progress["persisted_embeddings"] == 1
        assert search.sync_progress["reused_same_worktree"] == 3
        path.unlink()
        (path.parent / "copy.md").unlink()
        search.synchronize()
        path.write_text(a + b)
        restored = search.synchronize()
        assert restored.reused_embeddings == 2
        assert search.sync_progress["generated_embeddings"] == 0
        assert inputs() == [a, b, changed]
    assert events[-1]["generated_embedding_unit"] == "document_input_piece"


def test_parallel_worktrees_generate_one_embedding_in_total(tmp_path, model_search):
    create, inputs = model_search
    root = _repo_with_docs(tmp_path)
    runs = [_worktree(root, tmp_path / f"run-{index}") for index in range(2)]

    def synchronize(run):
        with closing(create(run)) as search:
            search.synchronize()
            return dict(search.sync_progress)

    with ThreadPoolExecutor(max_workers=2) as executor:
        progress = list(executor.map(synchronize, runs))
    assert inputs() == [(root / "oracle/doc/allowed.md").read_text()]
    assert sum(item["generated_embeddings"] for item in progress) == 1
    assert sum(item["reused_other_worktree"] for item in progress) == 1
    assert sum(item["persisted_embeddings"] for item in progress) == 1


def test_run_removal_preserves_embedding_and_original_producer(tmp_path, model_search):
    create, inputs = model_search
    root = _repo_with_docs(tmp_path)
    run = _worktree(root, root / ".cmoc/gu/worktree" / SESSION_ID / RUN_ID, RUN_BRANCH)
    original = (run / "oracle/doc/allowed.md").read_text()
    with closing(create(run)) as search:
        search.synchronize()
        search.synchronize()
        assert search.sync_progress["reused_same_worktree"] == 1
    assert remove_worktree(root, run).returncode == 0
    assert not run.exists()
    next_run = _worktree(root, tmp_path / "next-run")
    with closing(create(next_run)) as search:
        assert search.synchronize().reused_embeddings == 1
        assert search.sync_progress["generated_embeddings"] == 0
        assert search.sync_progress["reused_other_worktree"] == 1
    assert inputs() == [original]


@pytest.mark.parametrize("change", ["partition", "inference"])
def test_reuse_compatibility_is_independent_of_partition(
    tmp_path, model_search, change
):

    create, inputs = model_search
    root = _repo_with_docs(tmp_path)
    with closing(create(root)) as search:
        first = search.synchronize()
    config = _tuning()
    if change == "partition":
        config = replace(config, chunk_tokens=64, chunk_overlap_tokens=1)
    else:
        config = replace(config, embedding_context_tokens=256)
    with closing(create(root, config)) as search:
        second = search.synchronize()
        assert first.identity != second.identity
        assert search.sync_progress["generated_embeddings"] == (
            1 if change == "inference" else 0
        )
    assert len(inputs()) == (2 if change == "inference" else 1)


@pytest.mark.parametrize(
    "failure_code", ["MODEL_FAILURE", "CANCELLED", "DEADLINE_EXCEEDED"]
)
def test_failed_sync_saved_results_are_reusable_in_another_worktree(
    tmp_path, model_search, failure_code
):
    create, inputs = model_search
    root = _repo_with_docs(tmp_path)
    run = _worktree(root, tmp_path / "run")

    class FailingWorker(_InferenceDouble):
        def stream_chunks(self, documents, resumes, on_event, **kwargs):
            def stop_after_chunk(event):
                on_event(event)
                if event["kind"] == "chunk":
                    raise SearchError(failure_code, "stop after saved embedding")

            super().stream_chunks(documents, resumes, stop_after_chunk, **kwargs)

    with closing(DocumentSearch(root, _tuning(), worker=FailingWorker())) as search:
        with pytest.raises(SearchError) as failure:
            search.synchronize()
        assert failure.value.code == failure_code
        assert search.sync_progress["generated_embeddings"] == 1
        assert search.sync_progress["persisted_embeddings"] == 1
    with closing(create(run)) as search:
        assert search.synchronize().reused_embeddings == 1
        assert search.sync_progress["generated_embeddings"] == 0
    assert inputs() == []


def test_identical_inputs_in_different_repositories_are_not_shared(
    tmp_path, model_search
):
    create, inputs = model_search
    for name in ("first", "second"):
        directory = tmp_path / name
        directory.mkdir()
        root = _repo_with_docs(directory)
        with closing(create(root)) as search:
            search.synchronize()
            assert search.sync_progress["generated_embeddings"] == 1
            assert search.sync_progress["reused_embeddings"] == 0
    assert len(inputs()) == 2


def test_diagnostics_count_actual_duplicate_generation_separately_from_query(tmp_path):
    root = _repo_with_docs(tmp_path)
    original = (root / "oracle/doc/allowed.md").read_text()
    (root / "oracle/doc/copy.md").write_text(original)
    events = []

    class DuplicateWorker(_InferenceDouble):
        def stream_chunks(self, documents, resumes, on_event, **kwargs):
            for path, text in documents.items():
                # 意図的な重複推論も一意な入力数へ丸めず実績として数える。
                super().stream_chunks(
                    {path: text},
                    {path: resumes[path]},
                    on_event,
                    **{**kwargs, "reusable_hashes": set()},
                )

    with closing(
        DocumentSearch(
            root,
            _tuning(),
            worker=DuplicateWorker(),
            event_sink=lambda kind, payload: events.append({"event": kind, **payload}),
        )
    ) as search:
        search.search("query")
    sync = next(
        event for event in events if event["event"] == "document_search_sync_finished"
    )
    assert sync["generated_embedding_count"] == 2
    assert sync["persisted_embedding_count"] == 1
    assert sync["document_inference_call_count"] == 2
    assert events[-1]["query_generated_embedding_count"] == 1
    assert events[-1]["query_inference_call_count"] == 1


def test_cache_save_failure_keeps_generated_count_without_claiming_a_save(
    tmp_path, monkeypatch
):
    from commons import runtime_document_search as module

    root = _repo_with_docs(tmp_path)
    events = []

    def fail_save(*_args):
        raise sqlite3.OperationalError("storage failure")

    monkeypatch.setattr(module._EmbeddingCache, "save", fail_save)
    with closing(
        DocumentSearch(
            root,
            _tuning(),
            worker=_InferenceDouble(),
            event_sink=lambda kind, payload: events.append({"event": kind, **payload}),
        )
    ) as search:
        with pytest.raises(SearchError) as failure:
            search.synchronize()
        assert failure.value.code == "SYNC_FAILED"
    assert events[-1]["generated_embedding_count"] == 1
    assert events[-1]["persisted_embedding_count"] == 0
    assert events[-1]["counts_complete"] is False
