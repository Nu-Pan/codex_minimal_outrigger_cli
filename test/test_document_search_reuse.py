"""文書入力片の repository 内再利用と、生成・再利用元の診断を検証する。"""

import json
import sqlite3
import struct
import threading
from concurrent.futures import ThreadPoolExecutor
from contextlib import closing
from dataclasses import replace

import pytest
from _git_support import RUN_BRANCH, RUN_ID, SESSION_ID, run_git
from test_document_search import (
    _InferenceDouble,
    _repo_with_docs,
    _tuning,
)

from commons.runtime_document_search import (
    DocumentSearch,
    SearchError,
    _EmbeddingCache,
)
from commons.runtime_document_search_observation import SearchObservation
from commons.runtime_document_search_types import SEARCH_MATERIALS
from commons.runtime_git import remove_worktree


def _event_sink(events):
    """診断の可変な進捗を、通知時点の値で保存する。"""
    if events is None:
        return None

    def record(kind, payload):
        events.append(json.loads(json.dumps({"event": kind, **payload})))

    return record


@pytest.fixture
def cache_search():
    """cache の寿命・共有・互換性には一文書一入力の double を使う。"""
    # 分割・Node stream・重複入力の連携は test_document_search.py に残す。
    # cache の寿命・共有・互換性では、その連携の検査を重ねない。
    generated_inputs = []

    class CacheWorker(_InferenceDouble):
        def stream_chunks(self, documents, resumes, on_event, **kwargs):
            def record_input(event):
                if event["kind"] == "chunk":
                    source = documents[event["path"]]
                    generated_inputs.append(source[event["start"] : event["end"]])
                on_event(event)

            super().stream_chunks(documents, resumes, record_input, **kwargs)

    def create(root, config=None, *, events=None):
        return DocumentSearch(
            root,
            config or _tuning(),
            worker=CacheWorker(),
            event_sink=_event_sink(events),
        )

    return create, lambda: list(generated_inputs)


def _worktree(repository, path, branch=None):
    path.parent.mkdir(parents=True, exist_ok=True)
    args = ("-b", branch) if branch else ("--detach",)
    # _repo_with_docs の commit 済み ignore 規則を使い、修復を重ねない。
    run_git(repository, "worktree", "add", *args, str(path), "HEAD")
    return path


def test_cache_lookup_and_listing_discard_corrupt_entries(tmp_path):
    """単一取得と一覧取得で、破損結果を除外し前後の正常な結果を保持する。"""
    vector = struct.pack("<f", 1.0) + bytes(
        4 * (SEARCH_MATERIALS.embedding_dimensions - 1)
    )
    producer = "a" * 64
    entries = [
        (vector, producer),
        ("not a blob", producer),
        (b"short", producer),
        (struct.pack("<f", float("nan")) + vector[4:], producer),
        (struct.pack("<f", float("inf")) + vector[4:], producer),
        (bytes(len(vector)), producer),
        (vector, "short"),
        (vector, b"a" * 64),
        (vector, "b" * 64),
    ]
    rows = [(f"{index:064x}", *entry) for index, entry in enumerate(entries)]
    valid = {rows[0][0], rows[-1][0]}
    path = tmp_path / "cache.sqlite3"
    with closing(_EmbeddingCache(path)) as cache:
        # 同じ破損条件を両入口へ渡し、一覧の途中削除で後続を見落とす回帰も検出する。
        for lookup in ("single", "listing"):
            with cache.connection:
                cache.connection.executemany(
                    "insert or replace into embeddings values(?, ?, ?)", rows
                )
            if lookup == "single":
                found = {digest for digest, *_ in rows if cache.get(digest) is not None}
            else:
                # 破損行の削除後に取消が来ても transaction を残さず、再検査できる。
                checked = 0

                def cancel_after_invalid_entry():
                    nonlocal checked
                    checked += 1
                    if checked == 3:
                        raise SearchError("CANCELLED", "stop during cache validation")

                with pytest.raises(SearchError) as failure:
                    cache.hashes(cancel_after_invalid_entry)
                assert failure.value.code == "CANCELLED"
                assert not cache.connection.in_transaction
                found = cache.hashes(lambda: None)
            assert found == valid
            # 呼出元 connection の見かけだけでなく、削除が確定済みであることも確認する。
            with closing(sqlite3.connect(path)) as observer:
                assert {
                    digest
                    for (digest,) in observer.execute(
                        "select excerpt_sha256 from embeddings"
                    )
                } == valid
            assert cache.get(rows[0][0]) == (vector, producer)
            assert cache.get(rows[-1][0]) == (vector, "b" * 64)
            assert cache.get("missing") is None


def test_new_run_uses_stale_repository_cache_and_current_locations(
    tmp_path, cache_search
):
    create, inputs = cache_search
    root = _repo_with_docs(tmp_path, committed=True)
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
        # 検索の初回同期で再利用と現在位置を共に検査し、直前の明示同期を重ねない。
        hits = search.search("原文")["hits"]
        assert len(hits) == 2
        assert search.sync_progress["reused_embeddings"] == 2
        assert search.sync_progress["generated_embeddings"] == 0
        assert search.sync_progress["reused_other_worktree"] == 2
        assert search.sync_progress["reused_same_worktree"] == 0
        assert inputs() == [original]
        assert {hit["path"] for hit in hits} == {
            "oracle/doc/moved.md",
            "oracle/doc/copy.md",
        }
    finished = [
        event for event in events if event["event"] == "document_search_sync_finished"
    ]
    assert all(event["generated_embedding_count"] == 0 for event in finished)
    assert finished[-1]["reuse_count_unit"] == "chunk_occurrence"
    assert (
        root / "oracle/doc/allowed.md"
    ).read_text() == "# 再利用元だけの未同期本文\n"


def test_parallel_worktrees_generate_one_embedding_in_total(
    tmp_path, cache_search, monkeypatch
):
    """実際に競合する同期でも、待機後に不足分を確認して重複生成を避ける。"""
    # 分割・Node stream は部分編集で検査し、ここでは実 Git・cache・lock を使う。
    create, inputs = cache_search
    root = _repo_with_docs(tmp_path, committed=True)
    # 主 worktree と linked worktree を競合させ、複製は一つだけ作る。
    runs = [root, _worktree(root, tmp_path / "run")]
    contender_waiting = threading.Event()
    start_wait = SearchObservation.start_wait

    def observe_wait(observation):
        start_wait(observation)
        contender_waiting.set()

    monkeypatch.setattr(SearchObservation, "start_wait", observe_wait)

    def synchronize(run):
        with closing(create(run)) as search:
            stream_chunks = search.worker.stream_chunks

            def stream_after_contention(*args, **kwargs):
                # 固定 sleep や Node 起動時間に頼らず、後続同期の資源待ちを確かめる。
                assert contender_waiting.wait(5), "second sync did not contend"
                stream_chunks(*args, **kwargs)

            search.worker.stream_chunks = stream_after_contention
            search.synchronize()
            return dict(search.sync_progress)

    with ThreadPoolExecutor(max_workers=2) as executor:
        progress = list(executor.map(synchronize, runs))
    assert inputs() == [(root / "oracle/doc/allowed.md").read_text()]
    assert sum(item["generated_embeddings"] for item in progress) == 1
    assert sum(item["reused_other_worktree"] for item in progress) == 1
    assert sum(item["persisted_embeddings"] for item in progress) == 1


def test_run_removal_preserves_embedding_and_original_producer(tmp_path, cache_search):
    create, inputs = cache_search
    root = _repo_with_docs(tmp_path, committed=True)
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


def test_reuse_compatibility_is_independent_of_partition(
    document_repository, cache_search, monkeypatch, unsynced_search_storage
):
    """入力片を固定し、分割条件と推論条件による cache の互換性だけを検査する。"""
    from commons import runtime_document_search as module

    # Git 分類・共有範囲は実 repository の再利用 test に残す。
    create, inputs = cache_search
    root = document_repository
    original = (root / "oracle/doc/allowed.md").read_text()
    with closing(create(root)) as search:
        first = search.synchronize()
    assert inputs() == [original]

    # 互換な二条件を先に調べ、非互換条件ごとに新規生成を確認する。
    # 初期生成だけを共有し、各条件は元の設定・materials から個別に変える。
    for change in ("partition", "runtime", "inference", "contract", "model"):
        previous_inputs = inputs()
        config = _tuning()
        materials = SEARCH_MATERIALS
        if change == "partition":
            config = replace(config, chunk_tokens=64, chunk_overlap_tokens=1)
        elif change == "inference":
            config = replace(config, embedding_context_tokens=256)
        elif change == "runtime":
            materials = replace(
                SEARCH_MATERIALS,
                node_version="different-node",
                node_llama_cpp_version="different-library",
                llama_cpp_release="different-release",
                llama_cpp_revision="different-revision",
            )
        elif change == "contract":
            materials = replace(
                SEARCH_MATERIALS, document_embedding_contract="changed-input"
            )
        else:
            materials = replace(
                SEARCH_MATERIALS,
                embedding=replace(SEARCH_MATERIALS.embedding, sha256="different-model"),
            )
        generated = 1 if change in ("inference", "contract", "model") else 0
        with monkeypatch.context() as patch:
            patch.setattr(module, "SEARCH_MATERIALS", materials)
            with closing(create(root, config)) as search:
                second = search.synchronize()
                assert first.identity != second.identity, change
                assert search.sync_progress["generated_embeddings"] == generated, change
                assert second.reused_embeddings == 1 - generated, change
        assert inputs() == previous_inputs + [original] * generated, change


def test_failed_sync_saved_results_are_reusable_in_another_worktree(
    tmp_path, cache_search
):
    """失敗の種類ごとに未保存の入力を使い、途中保存結果を別 worktree で再利用する。"""
    create, inputs = cache_search
    root = _repo_with_docs(tmp_path, committed=True)
    run = _worktree(root, tmp_path / "run")

    # Git の準備だけを共有し、各失敗では新規生成・保存を必ず通す。
    # 失敗後の同一 worktree での再開は test_incomplete_stream_keeps_verified_chunks_and_resumes に残す。
    for failure_code in ("MODEL_FAILURE", "CANCELLED", "DEADLINE_EXCEEDED"):
        source = f"# {failure_code}\n途中で保存する本文\n"
        for worktree in (root, run):
            (worktree / "oracle/doc/allowed.md").write_text(source)

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
            assert search.sync_progress["reused_other_worktree"] == 1
    assert inputs() == []


def test_identical_inputs_in_different_repositories_are_not_shared(
    tmp_path, cache_search
):
    create, inputs = cache_search
    for name in ("first", "second"):
        directory = tmp_path / name
        directory.mkdir()
        root = _repo_with_docs(directory)
        with closing(create(root)) as search:
            search.synchronize()
            assert search.sync_progress["generated_embeddings"] == 1
            assert search.sync_progress["reused_embeddings"] == 0
    assert len(inputs()) == 2


def test_diagnostics_count_actual_duplicate_generation_separately_from_query(
    document_repository,
):
    # 診断件数の検査には、確認済みの文書集合を渡して Git 準備を重ねない。
    root = document_repository
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
    document_repository, monkeypatch
):
    from commons import runtime_document_search as module

    root = document_repository
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
