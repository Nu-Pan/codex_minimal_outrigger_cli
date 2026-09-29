"""文書検索の範囲、現在本文との同期、失敗公開を検証する。"""

import json
import os
import select
import shutil
import sqlite3
import subprocess
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from contextlib import closing
from dataclasses import asdict
from importlib import resources
from pathlib import Path

import pytest
from _git_support import make_repo, run_git
from oracle.acp_builder.basic import DocumentSearchScope
from oracle.other.document_search import INITIAL_SEARCH_MATERIALS, DocumentSearchConfig

from cmoc_runtime import write_config
from commons.runtime_document_search import (
    DocumentSearch,
    SearchError,
    _file_lock,
    scan_documents,
)
from commons.runtime_document_search_mcp import _response
from commons.runtime_document_search_worker import (
    NodeSearchWorker,
    _heading_ranges,
    materials_directory,
)
from commons.runtime_git import ensure_cmoc_ignored
from config.cmoc_config import CmocConfig


def _tuning() -> DocumentSearchConfig:
    """推論 double にだけ使う、製品既定値ではない test 設定。"""
    return DocumentSearchConfig(32, 0, 3, 128, 128, 128, 1, 10.0, 30.0, 1.0)


@pytest.mark.parametrize("cancel_wait", [False, True])
def test_file_lock_measures_contended_wait(tmp_path: Path, cancel_wait: bool) -> None:
    """取得成功と取消のどちらでも、保持時間を含めず取得待ちを計測する。"""
    lock_path = tmp_path / "index.lock"
    held = threading.Event()
    release = threading.Event()
    cancelled = threading.Event()
    waits: list[float] = []

    def hold_lock() -> None:
        with _file_lock(lock_path, None):
            held.set()
            release.wait(3)

    holder = threading.Thread(target=hold_lock)
    holder.start()
    timer = threading.Timer(0.15, cancelled.set if cancel_wait else release.set)
    try:
        assert held.wait(2)
        timer.start()
        if cancel_wait:
            with pytest.raises(SearchError, match="cancelled"):
                with _file_lock(lock_path, None, cancelled, on_wait=waits.append):
                    pytest.fail("cancelled acquisition unexpectedly succeeded")
        else:
            with _file_lock(lock_path, None, on_wait=waits.append):
                pass
        assert len(waits) == 1
        assert 0.1 <= waits[0] < 2
    finally:
        release.set()
        holder.join(2)
        if timer.is_alive():
            timer.join(2)
    assert not holder.is_alive()


class _InferenceDouble:
    """許可された本文と cache 再利用を観測する test worker。"""

    def __init__(self) -> None:
        self.operations: list[str] = []
        self.texts: list[str] = []

    def run(
        self,
        operation: str,
        payload: dict[str, object],
        *,
        deadline: float | None,
        residency_fd: int,
        cancelled: threading.Event | None = None,
    ) -> object:
        """実モデル以外の同期・cache 境界に対する確定的な応答。"""
        self.operations.append(operation)
        vector = [1.0] + [0.0] * (INITIAL_SEARCH_MATERIALS.embedding_dimensions - 1)
        if operation == "embed_query":
            return vector
        assert operation == "rerank"
        documents = payload["documents"]
        assert isinstance(documents, list)
        self.texts.extend(documents)
        return [0.8 for _ in documents]

    def stream_chunks(
        self,
        documents,
        resumes,
        on_event,
        *,
        reusable_hashes,
        deadline,
        residency_fd,
        cancelled,
    ):
        self.operations.append("chunk_embed")
        vector = [1.0] + [0.0] * (INITIAL_SEARCH_MATERIALS.embedding_dimensions - 1)
        self.texts.extend(documents.values())
        for path, source in documents.items():
            if resumes[path] == 0:
                on_event(
                    {
                        "kind": "chunk",
                        "path": path,
                        "ordinal": 0,
                        "start": 0,
                        "end": len(source),
                        "embedding": vector,
                    }
                )
            on_event({"kind": "document_complete", "path": path, "chunk_count": 1})


def _repo_with_docs(tmp_path: Path) -> Path:
    """索引を Git 非追跡にした隔離 repository を作る。"""
    root = make_repo(tmp_path)
    docs = root / "oracle/doc"
    docs.mkdir()
    (docs / "allowed.md").write_text("# 許可された原文\n最初の内容\n")
    (docs / "secret.md").write_text("# 非公開の本文\n")
    run_git(root, "add", "oracle/doc")
    run_git(root, "commit", "-m", "add docs")
    ensure_cmoc_ignored(root)
    return root


def _fake_node_model(base: Path) -> None:
    """実 chunker に文字単位 tokenizer と記録可能な推論を与える。"""
    source = resources.files("commons.document_search_worker").joinpath("worker.mjs")
    (base / "worker.mjs").write_bytes(source.read_bytes())
    package = base / "node_modules/node-llama-cpp"
    package.mkdir(parents=True)
    (package / "package.json").write_text(
        json.dumps({"type": "module", "exports": "./index.mjs"})
    )
    (package / "index.mjs").write_text(
        """import { appendFileSync } from "node:fs";
export async function getLlama() {
  return { async loadModel() {
    return {
      tokenize: (text) => Array.from(text),
      async dispose() {},
      async createEmbeddingContext() {
        return {
          async getEmbeddingFor(text) {
            appendFileSync("embedding-inputs.jsonl", JSON.stringify(text) + "\\n");
            const dimensions = Number(process.env.CMOC_TEST_DIMENSIONS || 2);
            return { vector: [1, ...Array(dimensions - 1).fill(0)] };
          },
          async dispose() {},
        };
      },
    };
  } };
}
"""
    )


@pytest.mark.parametrize(
    ("body", "parts"),
    [
        (
            "冒頭\n# 第一\n本文\n### 下位\n続き\n",
            ["冒頭\n", "# 第一\n本文\n", "### 下位\n続き\n"],
        ),
        (
            "冒頭\n\n見出し\n=======\n本文\n\n次の見出し\n---\n末尾",
            ["冒頭\n\n", "見出し\n=======\n本文\n\n", "次の見出し\n---\n末尾"],
        ),
        (
            "```md\n# 偽見出し\n````\n# 本物\n本文\n",
            ["```md\n# 偽見出し\n````\n", "# 本物\n本文\n"],
        ),
        ("見出しなし\n本文\n", ["見出しなし\n本文\n"]),
    ],
)
def test_heading_ranges_follow_markdown_structure(body: str, parts: list[str]) -> None:
    """階層・Setext・冒頭・コード fence を原文 offset で区切る。"""
    assert [body[start:end] for start, end in _heading_ranges(body)] == parts


def test_scope_only_reads_allowed_oracle_docs(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """除外と component 境界を本文の open より前に適用する。"""
    root = _repo_with_docs(tmp_path)
    from commons import runtime_document_search as module

    original = module._secure_read
    opened: list[str] = []

    def tracked_read(work_root: Path, relative: str) -> bytes:
        opened.append(relative)
        return original(work_root, relative)

    monkeypatch.setattr(module, "_secure_read", tracked_read)
    scope = DocumentSearchScope(
        allowed_subtrees=("oracle/doc",), excluded_files=("oracle/doc/secret.md",)
    )
    result = scan_documents(root, scope)
    assert set(result) == {"oracle/doc/allowed.md"}
    assert opened == ["oracle/doc/allowed.md"]
    assert scan_documents(root, DocumentSearchScope()) == {}
    with pytest.raises(SearchError, match="scope") as error:
        DocumentSearch(
            root, DocumentSearchScope(allowed_files=("../secret",)), _tuning()
        )
    assert error.value.code == "INVALID_SCOPE"


def test_search_syncs_edits_and_reuses_unchanged_embeddings(tmp_path: Path) -> None:
    """編集・空白化・削除後の旧本文を返さず、無変更推論を再実行しない。"""
    pytest.importorskip("sqlite_vec")
    root = _repo_with_docs(tmp_path)
    worker = _InferenceDouble()
    scope = DocumentSearchScope(allowed_files=("oracle/doc/allowed.md",))
    search = DocumentSearch(
        root, scope, _tuning(), worker=worker, installation_root=tmp_path
    )
    first = search.search("内容")
    assert first["status"] == "ok"
    assert [hit["path"] for hit in first["hits"]] == ["oracle/doc/allowed.md"]
    assert "最初の内容" in first["hits"][0]["excerpt"]
    assert worker.operations == ["chunk_embed", "embed_query", "rerank"]

    unchanged = search.search("内容")
    assert unchanged == first
    assert len(worker.operations) == 3
    (root / "oracle/doc/allowed.md").write_text("# 変更後\n次の内容\n")
    changed = search.search("内容")
    assert changed["hits"] and "次の内容" in changed["hits"][0]["excerpt"]
    assert "最初の内容" not in str(changed)
    assert worker.operations.count("chunk_embed") == 2
    assert worker.operations.count("embed_query") == 1

    (root / "oracle/doc/allowed.md").write_text(" \n\t")
    assert search.search("内容") == {"status": "ok", "hits": []}
    (root / "oracle/doc/allowed.md").unlink()
    sync = search.synchronize()
    assert sync.deleted == 1 and sync.chunk_count == 0
    assert "非公開の本文" not in str(worker.texts)


@pytest.mark.parametrize(
    "failure_code", ["MODEL_FAILURE", "CANCELLED", "DEADLINE_EXCEEDED"]
)
def test_incomplete_stream_keeps_verified_chunks_and_resumes(
    tmp_path: Path, failure_code: str
) -> None:
    """途中失敗を成功扱いせず、保存済み chunk の再計算を避ける。"""
    pytest.importorskip("sqlite_vec")
    root = _repo_with_docs(tmp_path)
    document = root / "oracle/doc/allowed.md"
    document.write_text("# 前半の原文\n後半の原文\n")
    vector = [1.0] + [0.0] * (INITIAL_SEARCH_MATERIALS.embedding_dimensions - 1)

    class StreamingWorker(_InferenceDouble):
        def __init__(self) -> None:
            super().__init__()
            self.fail = True
            self.resumes: list[dict[str, int]] = []

        def stream_chunks(
            self,
            documents,
            resumes,
            on_event,
            *,
            reusable_hashes,
            deadline,
            residency_fd,
            cancelled,
        ):
            self.resumes.append(dict(resumes))
            for path, text in documents.items():
                split = text.index("\n") + 1
                chunks = [(0, split), (split, len(text))]
                for ordinal in range(resumes[path], len(chunks)):
                    start, end = chunks[ordinal]
                    on_event(
                        {
                            "kind": "chunk",
                            "path": path,
                            "ordinal": ordinal,
                            "start": start,
                            "end": end,
                            "embedding": vector,
                        }
                    )
                    if self.fail:
                        raise SearchError(failure_code, "stopped after one chunk")
                on_event({"kind": "document_complete", "path": path, "chunk_count": 2})

    worker = StreamingWorker()
    search = DocumentSearch(
        root,
        DocumentSearchScope(allowed_files=("oracle/doc/allowed.md",)),
        _tuning(),
        worker=worker,
        installation_root=tmp_path,
    )
    with pytest.raises(SearchError, match="stopped after one chunk") as failure:
        search.search("原文")
    assert failure.value.code == failure_code
    assert search.sync_progress["persisted_chunks"] == 1
    _, index, _, _ = search._paths()
    with sqlite3.connect(index) as database:
        assert database.execute("select count(*) from chunks").fetchone()[0] == 1
        assert database.execute("select complete from documents").fetchone()[0] == 0

    worker.fail = False
    resumed = search.synchronize()
    assert worker.resumes == [
        {"oracle/doc/allowed.md": 0},
        {"oracle/doc/allowed.md": 1},
    ]
    assert resumed.chunk_count == 2
    assert resumed.reused_embeddings == 1
    assert search.search("原文")["status"] == "ok"


def test_unbounded_sync_outlasts_search_deadline(tmp_path: Path) -> None:
    """doctor 用同期は検索期限を超えて完了し、通常検索は期限を守る。"""
    pytest.importorskip("sqlite_vec")
    root = _repo_with_docs(tmp_path)
    vector = [1.0] + [0.0] * (INITIAL_SEARCH_MATERIALS.embedding_dimensions - 1)

    class SlowWorker(_InferenceDouble):
        def stream_chunks(
            self,
            documents,
            resumes,
            on_event,
            *,
            reusable_hashes,
            deadline,
            residency_fd,
            cancelled,
        ):
            assert len(documents) == 1
            assert deadline is None
            time.sleep(0.15)
            for path, source in documents.items():
                on_event(
                    {
                        "kind": "chunk",
                        "path": path,
                        "ordinal": 0,
                        "start": 0,
                        "end": len(source),
                        "embedding": vector,
                    }
                )
                on_event(
                    {
                        "kind": "document_complete",
                        "path": path,
                        "chunk_count": 1,
                    }
                )

    tuning = _tuning()
    tuning = DocumentSearchConfig(
        tuning.chunk_tokens,
        tuning.chunk_overlap_tokens,
        tuning.candidate_count,
        tuning.embedding_context_tokens,
        tuning.reranker_context_tokens,
        tuning.batch_tokens,
        tuning.threads,
        tuning.startup_timeout_seconds,
        0.05,
        tuning.shutdown_grace_seconds,
    )
    search = DocumentSearch(
        root,
        DocumentSearchScope(allowed_files=("oracle/doc/allowed.md",)),
        tuning,
        worker=SlowWorker(),
        installation_root=tmp_path,
    )
    assert search.synchronize(unbounded=True).chunk_count == 1


def test_deadline_after_first_chunk_preserves_it_for_retry(tmp_path: Path) -> None:
    """期限超過後の検索を失敗にし、有効な途中 chunk を再利用する。"""
    pytest.importorskip("sqlite_vec")
    root = _repo_with_docs(tmp_path)
    vector = [1.0] + [0.0] * (INITIAL_SEARCH_MATERIALS.embedding_dimensions - 1)

    class PausingWorker(_InferenceDouble):
        def __init__(self) -> None:
            super().__init__()
            self.pause = True
            self.resumes: list[int] = []

        def stream_chunks(
            self,
            documents,
            resumes,
            on_event,
            *,
            reusable_hashes,
            deadline,
            residency_fd,
            cancelled,
        ):
            path, source = next(iter(documents.items()))
            self.resumes.append(resumes[path])
            middle = source.index("\n") + 1
            for ordinal, (start, end) in enumerate(
                ((0, middle), (middle, len(source)))
            ):
                if ordinal < resumes[path]:
                    continue
                on_event(
                    {
                        "kind": "chunk",
                        "path": path,
                        "ordinal": ordinal,
                        "start": start,
                        "end": end,
                        "embedding": vector,
                    }
                )
                if ordinal == 0 and self.pause:
                    time.sleep(0.25)
            on_event({"kind": "document_complete", "path": path, "chunk_count": 2})

    tuning = _tuning()
    tuning = DocumentSearchConfig(
        tuning.chunk_tokens,
        tuning.chunk_overlap_tokens,
        tuning.candidate_count,
        tuning.embedding_context_tokens,
        tuning.reranker_context_tokens,
        tuning.batch_tokens,
        tuning.threads,
        tuning.startup_timeout_seconds,
        0.15,
        tuning.shutdown_grace_seconds,
    )
    worker = PausingWorker()
    search = DocumentSearch(
        root,
        DocumentSearchScope(allowed_files=("oracle/doc/allowed.md",)),
        tuning,
        worker=worker,
        installation_root=tmp_path,
    )
    with pytest.raises(SearchError) as failure:
        search.search("内容")
    assert failure.value.code == "DEADLINE_EXCEEDED"
    assert search.sync_progress["persisted_chunks"] == 1
    worker.pause = False
    assert search.synchronize().reused_embeddings == 1
    assert worker.resumes == [0, 1]


@pytest.mark.skipif(shutil.which("node") is None, reason="Node.js is unavailable")
@pytest.mark.parametrize("operation", ["chunk_stream", "chunk_embed"])
@pytest.mark.parametrize("fragment_size", [1, 65536], ids=["bytewise", "whole"])
def test_worker_preserves_text_across_utf8_input_fragments(
    tmp_path: Path, operation: str, fragment_size: int
) -> None:
    """実 worker が受信境界をまたぐ文字と、その原文上の位置を保つ。"""
    _fake_node_model(tmp_path)
    entrypoint = tmp_path / "worker.mjs"
    # OS の pipe 分割や sleep に依存せず、実入力のバイト境界を固定する。
    preload = tmp_path / "fragmented-stdin.mjs"
    preload.write_text(
        """import { readFileSync } from "node:fs";
import { Readable } from "node:stream";
const input = readFileSync(0);
const size = Number(process.env.CMOC_TEST_FRAGMENT_SIZE);
const fragments = [];
for (let start = 0; start < input.length; start += size) {
  fragments.push(input.subarray(start, start + size));
}
Object.defineProperty(process, "stdin", { value: Readable.from(fragments) });
"""
    )
    text = "# 日本語\néあ😀 と ASCII\n受信境界をまたいでも末尾まで保つ。\n"
    config = _tuning()
    request = NodeSearchWorker(tmp_path, config)._request(
        operation,
        {
            "documents": {"doc.md": text},
            "resume": {"doc.md": 0},
            "config": asdict(config),
        },
    )
    request["dimensions"] = 2
    result = subprocess.run(
        ["node", "--import", str(preload), str(entrypoint)],
        input=json.dumps(request, ensure_ascii=False).encode("utf-8"),
        cwd=tmp_path,
        env={**os.environ, "CMOC_TEST_FRAGMENT_SIZE": str(fragment_size)},
        capture_output=True,
        timeout=10,
        check=False,
    )
    assert result.returncode == 0, result.stderr.decode("utf-8")
    if operation == "chunk_stream":
        events = [json.loads(line) for line in result.stdout.splitlines()]
        chunks = [event for event in events if event["kind"] == "chunk"]
        assert events[-2:] == [
            {"kind": "document_complete", "path": "doc.md", "chunk_count": len(chunks)},
            {"kind": "done"},
        ]
        assert [chunk["ordinal"] for chunk in chunks] == list(range(len(chunks)))
        assert all(chunk["path"] == "doc.md" for chunk in chunks)
    else:
        response = json.loads(result.stdout)
        assert response["status"] == "ok"
        chunks = response["result"]["doc.md"]
    inputs = [
        json.loads(line)
        for line in (tmp_path / "embedding-inputs.jsonl").read_text().splitlines()
    ]
    assert "".join(inputs) == text
    assert len(chunks) == len(inputs)
    assert chunks[0]["start"] == 0 and chunks[-1]["end"] == len(text)
    for chunk, excerpt in zip(chunks, inputs, strict=True):
        assert 0 <= chunk["start"] < chunk["end"] <= len(text)
        assert text[chunk["start"] : chunk["end"]] == excerpt


@pytest.mark.skipif(shutil.which("node") is None, reason="Node.js is unavailable")
def test_worker_limits_overlap_to_heading_sections(tmp_path: Path) -> None:
    """長い節の overlap が次の短い節へ越境せず、本文を落とさない。"""
    _fake_node_model(tmp_path)
    body = "冒頭\n# A\n" + "長い本文" * 8 + "\n## B\n短い本文\n"
    tuning = DocumentSearchConfig(12, 3, 3, 128, 128, 128, 1, 10.0, 30.0, 1.0)
    request = NodeSearchWorker(tmp_path, tuning)._request(
        "chunk_embed", {"documents": {"doc.md": body}, "config": asdict(tuning)}
    )
    request["dimensions"] = 2
    process = subprocess.run(
        ["node", str(tmp_path / "worker.mjs")],
        input=json.dumps(request, ensure_ascii=False),
        cwd=tmp_path,
        text=True,
        capture_output=True,
        timeout=10,
        check=False,
    )
    assert process.returncode == 0, process.stderr
    chunks = json.loads(process.stdout)["result"]["doc.md"]
    sections = _heading_ranges(body)
    for chunk in chunks:
        assert any(
            start <= chunk["start"] < chunk["end"] <= end for start, end in sections
        )
    assert body[chunks[-1]["start"] : chunks[-1]["end"]] == "## B\n短い本文\n"
    covered = {
        index for chunk in chunks for index in range(chunk["start"], chunk["end"])
    }
    assert all(
        index in covered for index, char in enumerate(body) if not char.isspace()
    )


@pytest.mark.skipif(shutil.which("node") is None, reason="Node.js is unavailable")
def test_changed_sections_and_moved_files_reuse_saved_embeddings(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """実 chunker で変更節だけを再推論し、現在位置と採点 cache を保つ。"""
    pytest.importorskip("sqlite_vec")
    from commons import runtime_document_search_worker as worker_module

    root = make_repo(tmp_path)
    document = root / "oracle/doc/sections.md"
    document.parent.mkdir()
    a, b, c = "# A\nalpha\n", "# B\nbravo\n", "# C\ncharlie\n"
    document.write_text(a + b + c)
    run_git(root, "add", "oracle/doc")
    run_git(root, "commit", "-m", "add sections")
    ensure_cmoc_ignored(root)
    runtime = tmp_path / "fake-worker"
    runtime.mkdir()
    _fake_node_model(runtime)
    monkeypatch.setenv(
        "CMOC_TEST_DIMENSIONS", str(INITIAL_SEARCH_MATERIALS.embedding_dimensions)
    )
    monkeypatch.setattr(worker_module, "verify_search_materials", lambda *_: runtime)
    vector = [1.0] + [0.0] * (INITIAL_SEARCH_MATERIALS.embedding_dimensions - 1)

    class QueryWorker(NodeSearchWorker):
        def __init__(self) -> None:
            super().__init__(root, _tuning(), material_base=runtime)
            self.operations: list[str] = []

        def run(self, operation, payload, *, deadline, residency_fd, cancelled=None):
            self.operations.append(operation)
            if operation == "embed_query":
                return vector
            assert operation == "rerank"
            return [0.5] * len(payload["documents"])

    worker = QueryWorker()
    search = DocumentSearch(
        root,
        DocumentSearchScope(allowed_subtrees=("oracle/doc",)),
        _tuning(),
        worker=worker,
        installation_root=root,
    )

    def model_inputs() -> list[str]:
        return [
            json.loads(line)
            for line in (runtime / "embedding-inputs.jsonl").read_text().splitlines()
        ]

    def hit_lines() -> dict[str, int]:
        return {
            hit["excerpt"]: hit["start_line"]
            for hit in search.search("sections", limit=3)["hits"]
        }

    with closing(search):
        first = search.synchronize()
        assert first.chunk_count == 3
        assert search.sync_progress["persisted_chunks"] == 3
        assert model_inputs() == [a, b, c]
        assert hit_lines() == {a: 1, b: 3, c: 5}

        edited_a = "# A\nalpha edited\nextra\n"
        document.write_text(edited_a + b + c)
        changed = search.synchronize()
        assert changed.status == "updated"
        assert changed.reused_embeddings == 2
        assert search.sync_progress["persisted_chunks"] == 1
        assert search.sync_progress["changed_document_count"] == 1
        assert model_inputs() == [a, b, c, edited_a]
        assert hit_lines() == {edited_a: 1, b: 4, c: 6}

        revised_heading = "## A revised\nalpha edited\nextra\n"
        document.write_text(revised_heading + b + c)
        heading_change = search.synchronize()
        assert heading_change.reused_embeddings == 2
        assert search.sync_progress["persisted_chunks"] == 1
        assert model_inputs() == [a, b, c, edited_a, revised_heading]
        assert hit_lines() == {revised_heading: 1, b: 4, c: 6}

        document.write_text(b + c + revised_heading)
        moved_sections = search.synchronize()
        assert moved_sections.status == "updated"
        assert moved_sections.reused_embeddings == 3
        assert search.sync_progress["persisted_chunks"] == 0
        assert model_inputs() == [a, b, c, edited_a, revised_heading]
        assert hit_lines() == {b: 1, c: 3, revised_heading: 5}

        moved_file = document.with_name("moved.md")
        document.rename(moved_file)
        moved_document = search.synchronize()
        assert moved_document.status == "updated"
        assert moved_document.reused_embeddings == 3
        assert search.sync_progress["persisted_chunks"] == 0
        assert model_inputs() == [a, b, c, edited_a, revised_heading]
        hits = search.search("sections", limit=3)["hits"]
        assert {hit["path"] for hit in hits} == {"oracle/doc/moved.md"}
        assert {hit["excerpt"]: hit["start_line"] for hit in hits} == {
            b: 1,
            c: 3,
            revised_heading: 5,
        }
        assert worker.operations == ["embed_query", "rerank", "rerank", "rerank"]


@pytest.mark.skipif(shutil.which("node") is None, reason="Node.js is unavailable")
def test_streaming_worker_delivers_chunk_before_cancellation(tmp_path: Path) -> None:
    """Node の応答完了を待たず chunk を受け取り、取消時は子を回収する。"""
    base = materials_directory(tmp_path)
    base.mkdir(parents=True)
    (base / "worker.mjs").write_text(
        'import fs from "node:fs"; '
        "for await (const _part of process.stdin) {} "
        'fs.writeFileSync("started.pid", String(process.pid)); '
        'process.stdout.write(JSON.stringify({kind:"chunk",path:"doc.md",'
        'ordinal:0,start:0,end:1,embedding:[1]})+"\\n"); '
        "setInterval(() => {}, 1000);\n"
    )
    worker = NodeSearchWorker(tmp_path, _tuning())
    cancelled = threading.Event()
    descriptor = os.open(tmp_path / "lock", os.O_CREAT | os.O_RDWR, 0o600)
    received: list[object] = []
    try:
        with pytest.raises(SearchError) as failure:
            worker.stream_chunks(
                {"doc.md": "x"},
                {"doc.md": 0},
                lambda event: (received.append(event), cancelled.set()),
                reusable_hashes=set(),
                deadline=None,
                residency_fd=descriptor,
                cancelled=cancelled,
            )
        assert failure.value.code == "CANCELLED"
        assert len(received) == 1
        process_id = int((base / "started.pid").read_text())
        with pytest.raises(ProcessLookupError):
            os.kill(process_id, 0)
    finally:
        os.close(descriptor)


def test_database_symlink_cannot_redirect_index_writes(tmp_path: Path) -> None:
    """管理 DB の symlink を拒否し、対象外 path に書き込まない。"""
    pytest.importorskip("sqlite_vec")
    root = _repo_with_docs(tmp_path)
    search = DocumentSearch(
        root,
        DocumentSearchScope(allowed_files=("oracle/doc/allowed.md",)),
        _tuning(),
        worker=_InferenceDouble(),
        installation_root=tmp_path,
    )
    _identity, index, _lock, _residency = search._paths()
    index.parent.mkdir(parents=True)
    outside = tmp_path / "outside.sqlite3"
    index.symlink_to(outside)

    with pytest.raises(SearchError) as failure:
        search.search("内容")
    assert failure.value.code == "SYNC_FAILED"
    assert not outside.exists()


def test_scope_change_reclaims_only_inactive_index(tmp_path: Path) -> None:
    """範囲が狭くなった後は旧索引を再利用せず、未参照なら回収する。"""
    pytest.importorskip("sqlite_vec")
    root = _repo_with_docs(tmp_path)
    worker = _InferenceDouble()
    broad = DocumentSearch(
        root,
        DocumentSearchScope(allowed_subtrees=("oracle/doc",)),
        _tuning(),
        worker=worker,
        installation_root=tmp_path,
    )
    assert len(broad.search("内容")["hits"]) == 2
    _, old_index, _, _ = broad._paths()
    assert old_index.is_file()

    narrow = DocumentSearch(
        root,
        DocumentSearchScope(allowed_files=("oracle/doc/allowed.md",)),
        _tuning(),
        worker=worker,
        installation_root=tmp_path,
    )
    result = narrow.search("内容")
    assert [hit["path"] for hit in result["hits"]] == ["oracle/doc/allowed.md"]
    assert old_index.is_file()
    broad.close()
    narrow.search("内容")
    assert not old_index.exists()
    assert "非公開の本文" not in str(result)


def test_scope_change_preserves_index_while_request_uses_it(tmp_path: Path) -> None:
    """旧範囲の要求が推論待機中なら、新範囲はその索引を回収しない。"""
    pytest.importorskip("sqlite_vec")
    root = _repo_with_docs(tmp_path)
    broad = DocumentSearch(
        root,
        DocumentSearchScope(allowed_subtrees=("oracle/doc",)),
        _tuning(),
        worker=_InferenceDouble(),
        installation_root=tmp_path,
    )
    broad.search("内容")
    _, old_index, _, _ = broad._paths()
    started = threading.Event()
    release = threading.Event()
    normal_worker = _InferenceDouble()

    class _WaitingWorker(_InferenceDouble):
        def stream_chunks(
            self,
            documents,
            resumes,
            on_event,
            *,
            reusable_hashes,
            deadline,
            residency_fd,
            cancelled,
        ):
            started.set()
            assert release.wait(5)
            normal_worker.stream_chunks(
                documents,
                resumes,
                on_event,
                reusable_hashes=reusable_hashes,
                deadline=deadline,
                residency_fd=residency_fd,
                cancelled=cancelled,
            )

    broad.worker = _WaitingWorker()
    (root / "oracle/doc/secret.md").write_text("# 変更された本文\n")
    narrow = DocumentSearch(
        root,
        DocumentSearchScope(),
        _tuning(),
        worker=_InferenceDouble(),
        installation_root=tmp_path,
    )
    with ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.submit(broad.search, "内容")
        try:
            assert started.wait(5)
            assert narrow.search("内容")["status"] == "ok"
            assert old_index.is_file()
            broad.close()
            assert old_index.is_file()
        finally:
            release.set()
        assert future.result(timeout=5)["status"] == "ok"
    narrow.search("内容")
    assert not old_index.exists()


def test_zero_hit_search_rechecks_source_before_return(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """空白文書の同期直後に本文が変わったら、ゼロ件を成功として返さない。"""
    pytest.importorskip("sqlite_vec")
    root = _repo_with_docs(tmp_path)
    document = root / "oracle/doc/allowed.md"
    document.write_text(" \n")
    search = DocumentSearch(
        root,
        DocumentSearchScope(allowed_files=("oracle/doc/allowed.md",)),
        _tuning(),
        worker=_InferenceDouble(),
        installation_root=tmp_path,
    )
    from commons import runtime_document_search as module

    original = module.scan_documents
    scanned = 0

    def change_after_scan(*args: object, **kwargs: object) -> object:
        nonlocal scanned
        result = original(*args, **kwargs)
        scanned += 1
        if scanned == 1:
            document.write_text("# 新しい本文\n")
        return result

    monkeypatch.setattr(module, "scan_documents", change_after_scan)
    with pytest.raises(SearchError) as failure:
        search.search("内容")
    assert failure.value.code == "SOURCE_CHANGED"


def test_unset_tuning_and_mcp_failure_are_distinct_from_zero_hits(
    tmp_path: Path,
) -> None:
    """未設定は NOT_READY、MCP 引数 null は入力エラーにする。"""
    root = _repo_with_docs(tmp_path)
    search = DocumentSearch(root, DocumentSearchScope(), None)
    with pytest.raises(SearchError) as error:
        search.search("内容")
    assert error.value.code == "NOT_READY"
    invalid = _response(
        {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {"name": "search", "arguments": {"query": "内容", "limit": None}},
        },
        search,
    )
    assert invalid is not None and invalid["error"]["code"] == -32602
    failed = _response(
        {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/call",
            "params": {"name": "search", "arguments": {"query": "内容"}},
        },
        search,
    )
    assert failed is not None and failed["result"]["isError"] is True
    assert failed["result"]["structuredContent"]["code"] == "NOT_READY"


def test_worker_change_rebuilds_index_without_reusing_embeddings(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """worker 修正前の本文から計算された embedding を新索引へ引き継がない。"""
    from commons import runtime_document_search as module

    root = _repo_with_docs(tmp_path)
    package = tmp_path / "worker-source"
    package.mkdir()
    original_files = resources.files
    for name in ("worker.mjs", "package-lock.json"):
        (package / name).write_bytes(
            original_files("commons.document_search_worker").joinpath(name).read_bytes()
        )
    monkeypatch.setattr(
        module.resources,
        "files",
        lambda anchor: (
            package
            if anchor == "commons.document_search_worker"
            else original_files(anchor)
        ),
    )
    source = (package / "worker.mjs").read_bytes()
    results = []
    for revision in (b"", b"\n// Updated input handling.\n"):
        (package / "worker.mjs").write_bytes(source + revision)
        with closing(
            DocumentSearch(
                root,
                DocumentSearchScope(allowed_subtrees=("oracle/doc",)),
                _tuning(),
                worker=_InferenceDouble(),
                installation_root=tmp_path,
            )
        ) as search:
            result = search.synchronize()
            assert search.sync_progress["persisted_chunks"] == result.chunk_count
            results.append(result)
    first, second = results
    assert second.identity != first.identity
    assert second.chunk_count == first.chunk_count > 0
    assert second.reused_embeddings == 0


def test_search_rechecks_saved_config_for_each_request(tmp_path: Path) -> None:
    """起動後の有効な変更は新索引を使い、不備は旧設定へ戻さず拒否する。"""
    root = _repo_with_docs(tmp_path)
    path = root / ".cmoc/gt/config.json"
    write_config(path, CmocConfig())
    search = DocumentSearch(
        root,
        DocumentSearchScope(allowed_subtrees=("oracle/doc",)),
        CmocConfig().document_search,
        worker=_InferenceDouble(),
        installation_root=tmp_path,
        use_saved_config=True,
    )
    try:
        first = search.synchronize()
        data = json.loads(path.read_text())
        data["document_search"]["chunk_tokens"] = 256
        path.write_text(json.dumps(data) + "\n")

        second = search.synchronize()
        assert second.identity != first.identity

        data["document_search"] = None
        path.write_text(json.dumps(data) + "\n")
        with pytest.raises(SearchError) as exc_info:
            search.search("内容")
        assert exc_info.value.code == "NOT_READY"
        assert "cmoc doctor" in str(exc_info.value)
    finally:
        search.close()


def test_stdio_mcp_discovers_only_search_and_reports_not_ready(tmp_path: Path) -> None:
    """実 stdio 境界で discovery と機械的な失敗を読める。"""
    root = _repo_with_docs(tmp_path)
    context = {
        "work_root": str(root),
        "scope": {
            "allowed_files": [],
            "allowed_subtrees": ["oracle/doc"],
            "excluded_files": [],
            "excluded_subtrees": [],
        },
        "config": None,
    }
    project = Path(__file__).resolve().parents[1]
    environment = {
        **os.environ,
        "PYTHONPATH": os.pathsep.join(
            (str(project / "src"), str(project / "oracle/src"))
        ),
    }
    with subprocess.Popen(
        [
            sys.executable,
            "-m",
            "commons.runtime_document_search_mcp",
            json.dumps(context),
        ],
        cwd=root,
        env=environment,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    ) as process:
        assert process.stdin is not None and process.stdout is not None

        def request(request_id: int, method: str, params: dict[str, object]) -> dict:
            process.stdin.write(
                json.dumps(
                    {
                        "jsonrpc": "2.0",
                        "id": request_id,
                        "method": method,
                        "params": params,
                    }
                )
                + "\n"
            )
            process.stdin.flush()
            readable, _, _ = select.select([process.stdout], [], [], 5)
            assert readable
            return json.loads(process.stdout.readline())

        initialized = request(1, "initialize", {"protocolVersion": "2025-06-18"})
        assert initialized["result"]["capabilities"] == {
            "tools": {"listChanged": False}
        }
        listed = request(2, "tools/list", {})
        assert [tool["name"] for tool in listed["result"]["tools"]] == ["search"]
        failed = request(
            3, "tools/call", {"name": "search", "arguments": {"query": "内容"}}
        )
        assert failed["result"]["isError"] is True
        assert failed["result"]["structuredContent"]["code"] == "NOT_READY"
        process.stdin.close()
        assert process.wait(timeout=5) == 0


@pytest.mark.skipif(shutil.which("node") is None, reason="Node.js is unavailable")
def test_worker_cancellation_reaps_process_before_releasing_owner(
    tmp_path: Path,
) -> None:
    """推論中の取消で子 process を停止・回収してから失敗を返す。"""
    base = materials_directory(tmp_path)
    base.mkdir(parents=True)
    (base / "worker.mjs").write_text(
        'import fs from "node:fs"; '
        'fs.writeFileSync("started.pid", String(process.pid)); '
        "setInterval(() => {}, 1000);\n"
    )
    worker = NodeSearchWorker(tmp_path, _tuning())
    cancelled = threading.Event()
    descriptor = os.open(tmp_path / "lock", os.O_CREAT | os.O_RDWR, 0o600)
    try:
        with ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(
                worker.run,
                "embed_query",
                {"text": "test"},
                deadline=time.monotonic() + 10,
                residency_fd=descriptor,
                cancelled=cancelled,
            )
            marker = base / "started.pid"
            until = time.monotonic() + 5
            while (
                not marker.exists() and not future.done() and time.monotonic() < until
            ):
                time.sleep(0.02)
            assert marker.is_file()
            process_id = int(marker.read_text())
            cancelled.set()
            with pytest.raises(SearchError) as failure:
                future.result(timeout=5)
            assert failure.value.code == "CANCELLED"
            with pytest.raises(ProcessLookupError):
                os.kill(process_id, 0)
    finally:
        os.close(descriptor)
