"""文書検索の範囲、現在本文との同期、失敗公開を検証する。"""

import hashlib
import json
import math
import os
import select
import shutil
import sqlite3
import struct
import subprocess
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from contextlib import ExitStack, closing
from dataclasses import asdict, replace
from importlib import resources
from pathlib import Path
from types import SimpleNamespace
from typing import get_args

import pytest
from _git_support import init_repo, run_git
from jsonschema.validators import Draft202012Validator
from oracle.mcp.document_search import (
    SEARCH_TOOL_INPUT_SCHEMA,
    SEARCH_TOOL_OUTPUT_SCHEMA,
    SearchErrorCode,
    build_search_tool_description,
)
from oracle.other.cmoc_config import DocumentSearchConfig

from cmoc_runtime import write_config
from commons.runtime_document_search import (
    DocumentSearch,
    SearchError,
    _file_lock,
    scan_documents,
)
from commons.runtime_document_search_mcp import _response
from commons.runtime_document_search_types import SEARCH_MATERIALS
from commons.runtime_document_search_worker import (
    NodeSearchWorker,
    _heading_ranges,
    materials_directory,
)
from config.cmoc_config import CmocConfig


def _tuning() -> DocumentSearchConfig:
    """推論 double にだけ使う、製品既定値ではない test 設定。"""
    return DocumentSearchConfig(
        chunk_tokens=32,
        chunk_overlap_tokens=0,
        embedding_context_tokens=128,
        batch_tokens=128,
        threads=1,
        startup_timeout_seconds=10.0,
        request_timeout_seconds=30.0,
        shutdown_grace_seconds=1.0,
    )


@pytest.mark.parametrize("cancel_wait", [False, True])
def test_file_lock_measures_contended_wait(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, cancel_wait: bool
) -> None:
    """取得成功と取消のどちらでも、保持時間を含めず取得待ちを計測する。"""
    from commons import runtime_document_search as module

    # 実 file lock を競合させ、時計と所有者の解放だけを制御する。
    lock_path = tmp_path / "index.lock"
    cancelled = threading.Event()
    waits: list[float] = []
    clock = SimpleNamespace(now=0.0)

    def advance_wait(_seconds: float) -> None:
        clock.now += 1.0
        if clock.now == 3.0:
            if cancel_wait:
                cancelled.set()
            else:
                holder.close()

    monkeypatch.setattr(
        module,
        "time",
        SimpleNamespace(monotonic=lambda: clock.now, sleep=advance_wait),
    )
    with ExitStack() as holder:
        holder.enter_context(_file_lock(lock_path, None))
        if cancel_wait:
            with pytest.raises(SearchError, match="cancelled") as failure:
                with _file_lock(lock_path, None, cancelled, on_wait=waits.append):
                    pytest.fail("cancelled acquisition unexpectedly succeeded")
            assert failure.value.code == "CANCELLED"
        else:
            with _file_lock(lock_path, None, on_wait=waits.append):
                # 取得後の保持時間が待ち時間へ混ざる回帰も検出する。
                clock.now += 7.0
    assert waits == [3.0]


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
        vector = [1.0] + [0.0] * (SEARCH_MATERIALS.embedding_dimensions - 1)
        assert operation == "embed_query"
        return vector

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
        vector = [1.0] + [0.0] * (SEARCH_MATERIALS.embedding_dimensions - 1)
        self.texts.extend(documents.values())
        for path, source in documents.items():
            if resumes[path] == 0:
                digest = hashlib.sha256(source.encode()).hexdigest()
                on_event(
                    {
                        "kind": "reuse" if digest in reusable_hashes else "chunk",
                        "path": path,
                        "ordinal": 0,
                        "start": 0,
                        "end": len(source),
                        "embedding": vector,
                    }
                )
                reusable_hashes.add(digest)
            on_event({"kind": "document_complete", "path": path, "chunk_count": 1})


def _repo_with_docs(tmp_path: Path, *, committed: bool = False) -> Path:
    """索引を Git 非追跡にした隔離 repository を作る。"""
    # 履歴を使わない検査は未追跡の文書で行い、worktree 複製時だけ stage と HEAD を作る。
    # ignore 修復は test_runtime_git_ignore.py に委ね、複製先にも規則を引き継ぐ。
    root = tmp_path / "repo"
    root.mkdir()
    init_repo(root)
    docs = root / "spec"
    docs.mkdir(parents=True)
    (docs / "allowed.md").write_text("# 許可された原文\n最初の内容\n")
    (root / ".gitignore").write_text("spec/ignored.md\n/.cmoc/gu/\n")
    (docs / "ignored.md").write_text("# 非公開の本文\n")
    if committed:
        run_git(root, "add", ".gitignore", "spec")
        run_git(root, "commit", "-m", "add docs")
    return root


def _test_node_runtime(base: Path) -> None:
    """worker の隔離配置から、テスト用の実 Node を起動できるようにする。"""
    node = base / "node/bin/node"
    node.parent.mkdir(parents=True)
    node.symlink_to(shutil.which("node"))


def _fake_node_model(base: Path, *, tokens_per_character: float = 1.0) -> None:
    """実 chunker に処理量を記録する tokenizer と推論を与える。"""
    source = resources.files("commons.document_search_worker").joinpath("worker.mjs")
    (base / "worker.mjs").write_bytes(source.read_bytes())
    _test_node_runtime(base)
    package = base / "node_modules/node-llama-cpp"
    package.mkdir(parents=True)
    (package / "package.json").write_text(
        json.dumps({"type": "module", "exports": "./index.mjs"})
    )
    # 入力ログは終了後に読むため、破棄時に一括追記し、複数起動分は保持する。
    (package / "index.mjs").write_text(
        f"const tokensPerCharacter = {tokens_per_character};\n"
        """import { appendFileSync, writeFileSync } from "node:fs";
export async function getLlama() {
  return { async loadModel() {
    let tokenizedCharacters = 0;
    const embeddingInputs = [];
    return {
      tokenize(text) {
        const length = Array.from(text).length;
        tokenizedCharacters += length;
        return Array(Math.ceil(length * tokensPerCharacter));
      },
      async dispose() {
        writeFileSync("tokenized-characters.json", String(tokenizedCharacters));
        if (embeddingInputs.length) {
          appendFileSync("embedding-inputs.jsonl", embeddingInputs.join("\\n") + "\\n");
        }
      },
      async createEmbeddingContext() {
        return {
          async getEmbeddingFor(text) {
            embeddingInputs.push(JSON.stringify(text));
            const dimensions = Number(process.env.CMOC_TEST_DIMENSIONS || 2);
            return { vector: [1, ...Array(dimensions - 1).fill(0.125)] };
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
        (
            "> # *引用* [link][ref]\r\n> 本文\r\n\r\n[ref]: /target\r\n\r\n"
            "## **次** `code`\r\n本文😀\r\n",
            [
                "> # *引用* [link][ref]\r\n> 本文\r\n\r\n[ref]: /target\r\n\r\n",
                "## **次** `code`\r\n本文😀\r\n",
            ],
        ),
        (
            "冒頭😀\r\r*装飾* [link](url)\r======\r本文\r# 次\r末尾",
            ["冒頭😀\r\r", "*装飾* [link](url)\r======\r本文\r", "# 次\r末尾"],
        ),
        ("見出しなし\n本文\n", ["見出しなし\n本文\n"]),
    ],
)
def test_heading_ranges_follow_markdown_structure(body: str, parts: list[str]) -> None:
    """装飾・引用・改行形式を含む見出しを、コード fence と区別して原文で区切る。"""
    assert [body[start:end] for start, end in _heading_ranges(body)] == parts


def test_search_only_reads_oracle_doc_markdown(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """分類と spec・拡張子の条件を本文の open より前に適用する。"""
    root = _repo_with_docs(tmp_path)
    for relative in (
        "spec/AGENTS.md",
        "spec/note.txt",
        "reference/src/code.md",
        "specument/other.md",
        "realization.md",
    ):
        target = root / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text("対象外の本文\n")
    from commons import runtime_document_search as module

    original = module._secure_read
    opened: list[str] = []

    def tracked_read(work_root: Path, relative: str) -> bytes:
        opened.append(relative)
        return original(work_root, relative)

    monkeypatch.setattr(module, "_secure_read", tracked_read)
    result = scan_documents(root)
    assert set(result) == {"spec/allowed.md"}
    assert opened == ["spec/allowed.md"]


def test_search_syncs_edits_and_reuses_unchanged_embeddings(
    tmp_path: Path, document_repository: Path, unsynced_search_storage: None
) -> None:
    """編集・空白化・削除後の旧本文を返さず、無変更推論を再実行しない。"""
    pytest.importorskip("sqlite_vec")
    # Git 分類・ignore は直前の読取り範囲 test と実 worktree の再利用 test に残す。
    # 物理同期は途中保存・再開・worktree 間の再利用 test に残し、ここでは
    # 実 DB の更新・検索結果と推論回数を検査する。
    root = document_repository
    worker = _InferenceDouble()
    with closing(
        DocumentSearch(root, _tuning(), worker=worker, installation_root=tmp_path)
    ) as search:
        first = search.search("内容")
        assert first["status"] == "ok"
        assert [hit["path"] for hit in first["hits"]] == ["spec/allowed.md"]
        assert first["hits"][0]["ranges"] == [
            {"start_line": 1, "end_line": 2, "max_similarity": 1.0}
        ]
        assert worker.operations == ["chunk_embed", "embed_query"]

        unchanged = search.search("内容")
        assert unchanged == first
        assert len(worker.operations) == 2
        (root / "spec/allowed.md").write_text("# 変更後\n次の内容\n追加の行\n")
        changed = search.search("内容")
        assert changed["hits"] == [
            {
                "path": "spec/allowed.md",
                "ranges": [{"start_line": 1, "end_line": 3, "max_similarity": 1.0}],
            }
        ]
        assert worker.texts[-1] == "# 変更後\n次の内容\n追加の行\n"
        assert worker.operations.count("chunk_embed") == 2
        assert worker.operations.count("embed_query") == 1

        (root / "spec/allowed.md").write_text(" \n\t")
        assert search.search("内容") == {"status": "ok", "hits": []}
        (root / "spec/allowed.md").unlink()
        sync = search.synchronize()
        assert sync.deleted == 1 and sync.chunk_count == 0


@pytest.mark.parametrize(
    "edit_at", [None, "document_prepared", "chunk", "document_complete", "after_stream"]
)
def test_sync_rechecks_event_source_without_rereading_other_documents(
    document_repository, monkeypatch, edit_at, unsynced_search_storage
):
    """保存直前は対象本文だけを読み、通知時の編集も公開前に拒否する。"""
    from commons import runtime_document_search as module

    # Git 分類は専用ケースに残し、ここでは各確定時の本文読取りを検査する。
    root = document_repository
    docs = root / "spec"
    (docs / "second.md").write_text("# second\n本文\n")
    opened = []
    secure_read = module._secure_read

    def tracked_read(work_root, relative):
        opened.append(relative)
        return secure_read(work_root, relative)

    monkeypatch.setattr(module, "_secure_read", tracked_read)

    class ObservedWorker(_InferenceDouble):
        def stream_chunks(self, documents, resumes, on_event, **kwargs):
            def edit_source():
                (docs / "allowed.md").write_text("# 同期終了前に変更された本文\n")

            def observe(event):
                opened.clear()
                if event["kind"] == edit_at:
                    edit_source()
                on_event(event)
                # 保存時に他文書を読み直す回帰と、通知だけで再走査する回帰を検出する。
                assert opened == (
                    [event["path"]] if event["kind"] in ("chunk", "reuse") else []
                )

            for path in documents:
                observe({"kind": "document_prepared", "path": path, "chunk_count": 1})
            super().stream_chunks(documents, resumes, observe, **kwargs)
            if edit_at == "after_stream":
                edit_source()

    with closing(DocumentSearch(root, _tuning(), worker=ObservedWorker())) as search:
        if edit_at is not None:
            with pytest.raises(SearchError) as failure:
                search.synchronize()
            assert failure.value.code == "SOURCE_CHANGED"
            if edit_at in ("document_prepared", "chunk"):
                assert search.sync_progress["persisted_embeddings"] == 0
        else:
            result = search.synchronize()
            assert result.document_count == result.chunk_count == 2


@pytest.mark.parametrize(
    "change,code",
    [
        ("edit", "SOURCE_CHANGED"),
        ("ignore", "SOURCE_CHANGED"),
        ("invalid_utf8", "READ_FAILED"),
        ("unsafe_tree", "ENUMERATION_FAILED"),
    ],
)
def test_sync_rejects_changed_or_unreadable_source_before_saving(
    cli_repository, change, code, unsynced_search_storage
):
    """現在の分類・本文・安全性を確認できない生成結果は保存しない。"""
    root = cli_repository
    ignore = root / ".gitignore"
    ignore.write_text(".cmoc/gu/\n")
    document = root / "spec/fresh.md"
    document.parent.mkdir(parents=True)
    document.write_text("# 生成に使用した本文\n")

    class ChangingWorker(_InferenceDouble):
        def stream_chunks(self, documents, resumes, on_event, **kwargs):
            if change == "edit":
                document.write_text("# 生成後に編集された本文\n")
            elif change == "ignore":
                ignore.write_text(ignore.read_text() + "spec/fresh.md\n")
            elif change == "invalid_utf8":
                document.write_bytes(b"\xff")
            else:
                (root / "unsafe").symlink_to(root / "missing")
            super().stream_chunks(documents, resumes, on_event, **kwargs)

    with closing(DocumentSearch(root, _tuning(), worker=ChangingWorker())) as search:
        with pytest.raises(SearchError) as failure:
            search.synchronize()
        assert failure.value.code == code
        assert search.sync_progress["persisted_embeddings"] == 0
        assert search.sync_progress["persisted_chunks"] == 0
        _, index, _, _ = search._paths()
        with closing(sqlite3.connect(index)) as database:
            assert database.execute("select count(*) from chunks").fetchone()[0] == 0


@pytest.mark.parametrize(
    "failure_code", ["MODEL_FAILURE", "CANCELLED", "DEADLINE_EXCEEDED"]
)
def test_incomplete_stream_keeps_verified_chunks_and_resumes(
    tmp_path: Path, document_repository: Path, failure_code: str
) -> None:
    """途中失敗を成功扱いせず、保存済み chunk の再計算を避ける。"""
    pytest.importorskip("sqlite_vec")
    # 分類済みの文書を使い、途中保存と再開の検査に Git 準備を重ねない。
    root = document_repository
    document = root / "spec/allowed.md"
    document.write_text("# 前半の原文\n後半の原文\n")
    vector = [1.0] + [0.0] * (SEARCH_MATERIALS.embedding_dimensions - 1)

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
    # 再開と結果公開を一度の自動同期で検査し、明示同期直後の再同期を省く。
    resumed = search.search("原文")
    assert worker.resumes == [
        {"spec/allowed.md": 0},
        {"spec/allowed.md": 1},
    ]
    assert search.sync_progress["reused_embeddings"] == 1
    assert search.sync_progress["persisted_chunks"] == 1
    assert resumed["status"] == "ok"
    assert [hit["path"] for hit in resumed["hits"]] == ["spec/allowed.md"]
    assert sorted(
        resumed["hits"][0]["ranges"], key=lambda location: location["start_line"]
    ) == [
        {"start_line": 1, "end_line": 1, "max_similarity": 1.0},
        {"start_line": 2, "end_line": 2, "max_similarity": 1.0},
    ]


def test_deadline_after_first_chunk_preserves_it_for_retry(
    tmp_path: Path, document_repository: Path, document_search_clock
) -> None:
    """期限超過後の検索を失敗にし、有効な途中 chunk を再利用する。"""
    pytest.importorskip("sqlite_vec")
    root = document_repository
    vector = [1.0] + [0.0] * (SEARCH_MATERIALS.embedding_dimensions - 1)

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
                    document_search_clock.advance(0.25)
            on_event({"kind": "document_complete", "path": path, "chunk_count": 2})

    tuning = replace(_tuning(), sync_no_progress_timeout_seconds=0.15)
    worker = PausingWorker()
    search = DocumentSearch(
        root,
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
def test_worker_streams_utf8_chunks_and_reuse_through_small_pipe(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """入力のバイト境界と出力の部分書込みを一度の実 worker 起動で検査する。"""
    _fake_node_model(tmp_path)
    # OS の pipe 分割や sleep に依存せず、実入力のバイト境界を固定する。
    preload = tmp_path / "fragmented-stdin.mjs"
    preload.write_text("""import { readFileSync } from "node:fs";
import { Readable } from "node:stream";
// 実 runtime と同様に stdout を初期化し、非同期 pipe の部分書込みを再現する。
void process.stdout;
const input = readFileSync(0);
const fragments = [];
for (let start = 0; start < input.length; start++) {
  fragments.push(input.subarray(start, start + 1));
}
Object.defineProperty(process, "stdin", { value: Readable.from(fragments) });
""")
    text = "# 日本語\néあ😀 と ASCII\n受信境界をまたいでも末尾まで保つ。\n"
    config = _tuning()
    documents = {
        "日本語.md": text,
        "next.md": "別の本文",
        "reuse.md": text,
    }
    parsed_bodies = []

    def tracked_heading_ranges(body):
        parsed_bodies.append(body)
        return _heading_ranges(body)

    # 重複文書も原文位置を保ちつつ、同じ本文の見出し解析を重ねない。
    monkeypatch.setattr(
        "commons.runtime_document_search_worker._heading_ranges", tracked_heading_ranges
    )
    request = NodeSearchWorker(tmp_path, config)._request(
        "chunk_stream",
        {
            "documents": documents,
            "resume": dict.fromkeys(documents, 0),
            "config": asdict(config),
        },
    )
    assert sorted(parsed_bodies) == sorted(set(documents.values()))
    dimensions = SEARCH_MATERIALS.embedding_dimensions
    result = subprocess.run(
        ["node", "--import", str(preload), str(tmp_path / "worker.mjs")],
        input=json.dumps(request, ensure_ascii=False).encode("utf-8"),
        cwd=tmp_path,
        env={**os.environ, "CMOC_TEST_DIMENSIONS": str(dimensions)},
        capture_output=True,
        pipesize=4096,
        timeout=10,
        check=False,
    )
    assert result.returncode == 0, result.stderr.decode("utf-8")
    events = [json.loads(line) for line in result.stdout.splitlines()]
    chunks = [event for event in events if event["kind"] == "chunk"]
    inputs = [
        json.loads(line)
        for line in (tmp_path / "embedding-inputs.jsonl").read_text().splitlines()
    ]
    # バイト分割した 2・3・4 byte の文字が推論入力と原文位置を保つ。
    for chunk, excerpt in zip(chunks, inputs, strict=True):
        body = documents[chunk["path"]]
        assert 0 <= chunk["start"] < chunk["end"] <= len(body)
        assert body[chunk["start"] : chunk["end"]] == excerpt

    # 複数 chunk・別文書・再利用を含め、pipe より大きい各イベントを順送する。
    expected = []
    for path, body in documents.items():
        source_path = "日本語.md" if path == "reuse.md" else path
        source_chunks = [chunk for chunk in chunks if chunk["path"] == source_path]
        assert source_chunks
        expected.append(
            {
                "kind": "document_prepared",
                "path": path,
                "chunk_count": len(source_chunks),
            }
        )
        end = 0
        for ordinal, chunk in enumerate(source_chunks):
            assert chunk["start"] == end
            end = chunk["end"]
            event = {
                "kind": "reuse" if path == "reuse.md" else "chunk",
                "path": path,
                "ordinal": ordinal,
                "start": chunk["start"],
                "end": end,
            }
            if event["kind"] == "chunk":
                event["embedding"] = [1] + [0.125] * (dimensions - 1)
                assert len(json.dumps(event).encode("utf-8")) > 4096
            expected.append(event)
        assert end == len(body)
        expected.append(
            {
                "kind": "document_complete",
                "path": path,
                "chunk_count": len(source_chunks),
            }
        )
    assert events == [*expected, {"kind": "done"}]


@pytest.mark.skipif(shutil.which("node") is None, reason="Node.js is unavailable")
@pytest.mark.parametrize("operation", ["chunk_stream", "chunk_embed"])
def test_worker_reports_closed_output_pipe(tmp_path: Path, operation: str) -> None:
    """受信側の切断を送信失敗として終了し、完了待ちで停止し続けない。"""
    _fake_node_model(tmp_path)
    config = _tuning()
    request = NodeSearchWorker(tmp_path, config)._request(
        operation,
        {
            "documents": {"doc.md": "本文"},
            "resume": {"doc.md": 0},
            "config": asdict(config),
        },
    )
    request["dimensions"] = 2
    read_fd, write_fd = os.pipe()
    os.close(read_fd)
    with os.fdopen(write_fd, "wb") as output:
        result = subprocess.run(
            ["node", str(tmp_path / "worker.mjs")],
            input=json.dumps(request).encode(),
            cwd=tmp_path,
            stdout=output,
            stderr=subprocess.PIPE,
            timeout=10,
            check=False,
        )
    assert result.returncode != 0
    assert b"document search worker failed:" in result.stderr
    assert b"EPIPE" in result.stderr


@pytest.mark.skipif(shutil.which("node") is None, reason="Node.js is unavailable")
@pytest.mark.parametrize("tokens_per_character", [0.25, 1.0, 2.0])
def test_worker_limits_overlap_and_tokenization_to_heading_sections(
    tmp_path: Path, tokens_per_character: float
) -> None:
    """長い節を過剰に tokenize せず、token 上限・Unicode の位置・overlap を保つ。"""
    _fake_node_model(tmp_path, tokens_per_character=tokens_per_character)
    body = "冒頭 éあ😀\n# A\n" + "長い本文" * 256 + "\n## B\n短い本文é😀\n"
    tuning = replace(_tuning(), chunk_tokens=12, chunk_overlap_tokens=3)
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
    response = json.loads(process.stdout)
    assert response["status"] == "ok"
    chunks = response["result"]["doc.md"]
    inputs = [
        json.loads(line)
        for line in (tmp_path / "embedding-inputs.jsonl").read_text().splitlines()
    ]
    assert chunks[0]["start"] == 0 and chunks[-1]["end"] == len(body)
    sections = _heading_ranges(body)
    for chunk, excerpt in zip(chunks, inputs, strict=True):
        assert any(
            start <= chunk["start"] < chunk["end"] <= end for start, end in sections
        )
        assert body[chunk["start"] : chunk["end"]] == excerpt
        assert math.ceil(len(excerpt) * tokens_per_character) <= tuning.chunk_tokens
    if tokens_per_character <= 1.0:
        assert body[chunks[-1]["start"] : chunks[-1]["end"]] == "## B\n短い本文é😀\n"
    for previous, current in zip(chunks, chunks[1:]):
        overlap = max(0, previous["end"] - current["start"])
        assert math.ceil(overlap * tokens_per_character) <= tuning.chunk_overlap_tokens
        if any(
            start <= previous["start"] < current["end"] <= end
            for start, end in sections
        ):
            assert overlap > 0
    covered = {
        index for chunk in chunks for index in range(chunk["start"], chunk["end"])
    }
    assert all(
        index in covered for index, char in enumerate(body) if not char.isspace()
    )
    # 残り全文や確認済み範囲の反復 token 化を、実時間のばらつきなしで検出する。
    tokenized_characters = int((tmp_path / "tokenized-characters.json").read_text())
    assert tokenized_characters < 17 * len(body)


@pytest.mark.skipif(shutil.which("node") is None, reason="Node.js is unavailable")
def test_changed_sections_and_moved_files_reuse_saved_embeddings(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    document_repository: Path,
    unsynced_search_storage,
) -> None:
    """実 chunker で変更・重複・移動・削除後の再利用と現在位置を検査する。"""
    pytest.importorskip("sqlite_vec")
    from commons import runtime_document_search_worker as worker_module

    # Git 分類は読取り範囲・同期競合・worktree 再利用の test で検査する。
    # 実 Node の分割・cache・現在位置を通し、各 event の Git 走査を重ねない。
    root = document_repository
    document = root / "spec/allowed.md"
    a, b, c = "# A\nalpha\n", "# B\nbravo\n", "# C\ncharlie\n"
    document.write_text(a + b + c)
    runtime = tmp_path / "fake-worker"
    runtime.mkdir()
    _fake_node_model(runtime)
    monkeypatch.setenv(
        "CMOC_TEST_DIMENSIONS", str(SEARCH_MATERIALS.embedding_dimensions)
    )
    monkeypatch.setattr(worker_module, "verify_search_materials", lambda *_: runtime)
    vector = [1.0] + [0.0] * (SEARCH_MATERIALS.embedding_dimensions - 1)

    class QueryWorker(NodeSearchWorker):
        def __init__(self) -> None:
            super().__init__(root, _tuning(), material_base=runtime)
            self.operations: list[str] = []

        def run(self, operation, payload, *, deadline, residency_fd, cancelled=None):
            self.operations.append(operation)
            assert operation == "embed_query"
            return vector

    worker = QueryWorker()
    events = []
    search = DocumentSearch(
        root,
        _tuning(),
        worker=worker,
        installation_root=root,
        event_sink=lambda kind, payload: events.append({"event": kind, **payload}),
    )

    def model_inputs() -> list[str]:
        return [
            json.loads(line)
            for line in (runtime / "embedding-inputs.jsonl").read_text().splitlines()
        ]

    def hit_lines() -> dict[str, dict[int, str]]:
        # 公開位置から現在原文を読み、移動前の位置や抜粋に依存しない。
        locations = {}
        for hit in search.search("sections")["hits"]:
            lines = (root / hit["path"]).read_text().splitlines(keepends=True)
            ranges = {}
            for location in hit["ranges"]:
                start, end = location["start_line"], location["end_line"]
                ranges[start] = "".join(lines[start - 1 : end])
            locations[hit["path"]] = ranges
        return locations

    path = document.relative_to(root).as_posix()
    with closing(search):
        # 初回も検索の自動同期で生成数と現在位置を一緒に検査する。
        assert hit_lines() == {path: {1: a, 3: b, 5: c}}
        assert search.sync_progress["persisted_chunks"] == 3
        assert model_inputs() == [a, b, c]

        edited_a = "# A\nalpha edited\nextra\n"
        document.write_text(edited_a + b + c + edited_a)
        # 元文書を先に処理し、文書内の初生成後と別文書での再利用を共に通す。
        copy = document.with_name("z-copy.md")
        copy.write_text(edited_a)
        # 同期一回で、未保存の同一入力が文書内・別文書に現れる場合も検査する。
        assert hit_lines() == {
            path: {1: edited_a, 4: b, 6: c, 8: edited_a},
            copy.relative_to(root).as_posix(): {1: edited_a},
        }
        assert search.sync_progress["status"] == "updated"
        assert search.sync_progress["generated_embeddings"] == 1
        assert search.sync_progress["persisted_embeddings"] == 1
        assert search.sync_progress["reused_same_worktree"] == 4
        assert search.sync_progress["reused_embeddings"] == 4
        assert search.sync_progress["persisted_chunks"] == 1
        assert search.sync_progress["changed_document_count"] == 2
        assert model_inputs() == [a, b, c, edited_a]
        # 同じ節の再配置・重複では分割を重ねず、新規推論入力の検査だけを加える。
        tokenized_characters = int((runtime / "tokenized-characters.json").read_text())
        assert tokenized_characters <= len(edited_a + b + c) + len(edited_a)

        revised_heading = "## A revised\nalpha edited\nextra\n"
        copy.unlink()
        # 見出し編集と並べ替えを一度の同期で検査し、同じ節の再利用に Node を再起動しない。
        # 本文を変えない移動と、全参照を失った後の復元は後続の同期で独立に保つ。
        document.write_text(b + c + revised_heading)
        assert hit_lines() == {path: {1: b, 3: c, 5: revised_heading}}
        assert search.sync_progress["reused_embeddings"] == 2
        assert search.sync_progress["persisted_chunks"] == 1
        assert model_inputs() == [a, b, c, edited_a, revised_heading]

        moved_file = document.with_name("moved.md")
        document.rename(moved_file)
        assert hit_lines() == {
            moved_file.relative_to(root).as_posix(): {1: b, 3: c, 5: revised_heading}
        }
        assert search.sync_progress["status"] == "updated"
        assert search.sync_progress["reused_embeddings"] == 3
        assert search.sync_progress["persisted_chunks"] == 0
        assert model_inputs() == [a, b, c, edited_a, revised_heading]

        # 全参照を失っても元の入力片を保持し、復元時に推論を重ねない。
        moved_file.unlink()
        assert hit_lines() == {}
        document.write_text(a + b + c)
        assert hit_lines() == {path: {1: a, 3: b, 5: c}}
        assert search.sync_progress["reused_embeddings"] == 3
        assert search.sync_progress["generated_embeddings"] == 0
        assert model_inputs() == [a, b, c, edited_a, revised_heading]
        # 短い節は一度の token 化で収まり、全再利用時には推論用の再検査も不要。
        tokenized_characters = int((runtime / "tokenized-characters.json").read_text())
        assert tokenized_characters <= len(a + b + c)
        assert worker.operations == ["embed_query"]
    finished = [
        event for event in events if event["event"] == "document_search_sync_finished"
    ]
    assert finished[-1]["generated_embedding_unit"] == "document_input_piece"


@pytest.mark.skipif(shutil.which("node") is None, reason="Node.js is unavailable")
def test_streaming_worker_delivers_chunk_before_cancellation(tmp_path: Path) -> None:
    """Node の応答完了を待たず chunk を受け取り、取消時は子を回収する。"""
    base = materials_directory(tmp_path)
    base.mkdir(parents=True)
    _test_node_runtime(base)
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


def test_database_symlink_cannot_redirect_index_writes(
    tmp_path: Path, document_repository: Path
) -> None:
    """管理 DB の symlink を拒否し、対象外 path に書き込まない。"""
    pytest.importorskip("sqlite_vec")
    # Git 分類・ignore 検査は専用ケースに残し、DB の拒否と外部への非書込みを通す。
    root = document_repository
    search = DocumentSearch(
        root,
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


def test_config_change_reclaims_only_inactive_index(
    tmp_path: Path, document_repository: Path, unsynced_search_storage: None
) -> None:
    """互換条件の変更後は旧索引を再利用せず、未参照なら回収する。"""
    pytest.importorskip("sqlite_vec")
    root = document_repository
    with (
        closing(
            DocumentSearch(
                root,
                _tuning(),
                worker=_InferenceDouble(),
                installation_root=tmp_path,
            )
        ) as previous,
        closing(
            DocumentSearch(
                root,
                replace(_tuning(), chunk_tokens=16),
                worker=_InferenceDouble(),
                installation_root=tmp_path,
            )
        ) as current,
    ):
        # 同期も検索と同じ lease・回収を通るため、query 推論・保存・順位付けを重ねない。
        # query と検索結果は同期・候補の専用 test、実行中の保護は次の test に残す。
        previous.synchronize()
        _, old_index, _, _ = previous._paths()
        assert old_index.is_file()
        result = current.synchronize()
        assert result.document_count == result.chunk_count == 1
        assert current._paths()[1] != old_index
        assert old_index.is_file()
        previous.close()
        current.synchronize()
        assert not old_index.exists()


def test_config_change_preserves_index_while_request_uses_it(
    tmp_path: Path, document_repository: Path, unsynced_search_storage: None
) -> None:
    """旧設定の要求が推論中なら、接続を閉じてもその索引を回収しない。"""
    pytest.importorskip("sqlite_vec")
    root = document_repository
    started = threading.Event()
    release = threading.Event()

    class WaitingWorker(_InferenceDouble):
        def run(self, *args, **kwargs):
            started.set()
            assert release.wait(5)
            return super().run(*args, **kwargs)

    with (
        closing(
            DocumentSearch(
                root,
                _tuning(),
                worker=_InferenceDouble(),
                installation_root=tmp_path,
            )
        ) as previous,
        closing(
            DocumentSearch(
                root,
                replace(_tuning(), chunk_tokens=16),
                worker=_InferenceDouble(),
                installation_root=tmp_path,
            )
        ) as current,
    ):
        # 索引の準備と回収は同期だけで行い、保護対象の要求だけを query 推論で止める。
        previous.synchronize()
        current.synchronize()
        _, old_index, _, _ = previous._paths()
        previous.worker = WaitingWorker()
        with ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(previous.search, "未計算の query")
            try:
                assert started.wait(5)
                assert current.synchronize().chunk_count == 1
                previous.close()
                current.synchronize()
                assert old_index.is_file()
            finally:
                release.set()
            assert future.result(timeout=5)["status"] == "ok"
        current.synchronize()
        assert not old_index.exists()


def test_zero_hit_search_rechecks_source_before_return(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    document_repository: Path,
    unsynced_search_storage: None,
) -> None:
    """空白文書の同期直後に本文が変わったら、ゼロ件を成功として返さない。"""
    pytest.importorskip("sqlite_vec")
    root = document_repository
    document = root / "spec/allowed.md"
    document.write_text(" \n")
    search = DocumentSearch(
        root,
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


def _listed_search_tool(search):
    response = _response({"jsonrpc": "2.0", "id": 0, "method": "tools/list"}, search)
    return response["result"]["tools"][0]


def _assert_search_result(response, schema, *, error):
    # stdio で送信する JSON を検査し、text と構造化結果の相違も検出する。
    result = json.loads(json.dumps(response, allow_nan=False))["result"]
    structured = result["structuredContent"]
    Draft202012Validator(schema).validate(structured)
    assert result["isError"] is error
    assert result["content"][0]["type"] == "text"
    assert json.loads(result["content"][0]["text"]) == structured
    if structured["status"] == "ok":
        assert all(
            location["start_line"] <= location["end_line"]
            for hit in structured["hits"]
            for location in hit["ranges"]
        )
    return structured


@pytest.mark.parametrize(
    "arguments",
    [
        {},
        {"query": ""},
        {"query": " \n\t"},
        {"query": None},
        {"query": "内容", "work_root": "/elsewhere"},
        {"query": "内容", "path": "spec/allowed.md"},
        *({"query": "内容", "limit": limit} for limit in (None, True, 19, 51, 20.5)),
    ],
)
def test_mcp_rejects_invalid_arguments_before_search(tmp_path, monkeypatch, arguments):
    """公開引数 schema に違反する入力は検索せず protocol error にする。"""
    search = DocumentSearch(tmp_path, None)
    tool = _listed_search_tool(search)
    assert not Draft202012Validator(tool["inputSchema"]).is_valid(arguments)
    monkeypatch.setattr(search, "search", lambda *a, **kw: pytest.fail("search called"))
    response = _response(
        {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {"name": "search", "arguments": arguments},
        },
        search,
    )
    assert response["error"]["code"] == -32602
    assert "result" not in response


@pytest.fixture
def candidate_worker(monkeypatch, unsynced_search_storage):
    """候補の順位・上限・統合は、零埋めを省いた同じコサイン類似度で検査する。"""
    from commons import runtime_document_search as module

    # この検査のベクトルは元から先頭二成分だけを使う。
    # 実次元数での連携は worker の小容量 pipe・部分編集と資材検証に残す。
    monkeypatch.setattr(
        module,
        "SEARCH_MATERIALS",
        replace(SEARCH_MATERIALS, embedding_dimensions=2),
    )

    class _CandidateWorker:
        def __init__(self, ranges, *, vectors=None):
            self.operations = []
            self.ranges = ranges
            self.vectors = vectors
            self.query_vector = (1, 0)

        def run(self, operation, payload, **kwargs):
            self.operations.append(operation)
            assert operation == "embed_query"
            return list(self.query_vector)

        def stream_chunks(self, documents, resumes, on_event, **kwargs):
            for path, source in documents.items():
                lines = source.splitlines(keepends=True)
                ranges = self.ranges[path]
                for ordinal in range(resumes[path], len(ranges)):
                    start, end = ranges[ordinal]
                    embedding = list(
                        self.vectors[path][ordinal]
                        if self.vectors is not None
                        else (1, 0)
                    )
                    on_event(
                        {
                            "kind": "chunk",
                            "path": path,
                            "ordinal": ordinal,
                            "start": len("".join(lines[: start - 1])),
                            "end": len("".join(lines[:end])),
                            "embedding": embedding,
                        }
                    )
                on_event(
                    {
                        "kind": "document_complete",
                        "path": path,
                        "chunk_count": len(ranges),
                    }
                )

    return _CandidateWorker


@pytest.mark.parametrize(
    "candidate_count,candidates,limit_cases",
    [
        # 上限を一件超える候補で切捨てを検出し、同じ検証のための余分な保存を省く。
        # 件数条件は負の同点候補で通し、類似度の境界を全上限と直積にしない。
        # 引数の最大値 50 は設定上限 20 のケースで検査し、同じ 50 件の検索を重ねない。
        (50, [((1, 0), -0.6)] * 51, [(None, 50), (20, 20)]),
        (20, [((1, 0), -0.6)] * 21, [(None, 20), (50, 20)]),
        # -1・0・1 は三候補の一検索で検査し、境界値ごとの同期・query 保存を重ねない。
        # 順位と件数による値の不変性は専用ケースで保つ。
        (50, [((-3, 4), 1.0), ((-4, -3), 0.0), ((3, -4), -1.0)], [(None, 3)]),
        (50, [], [(None, 0)]),
    ],
    ids=["candidate-cap", "configured-cap", "similarity-boundaries", "empty"],
)
def test_mcp_success_schema_and_candidate_limits(
    tmp_path,
    document_repository,
    candidate_worker,
    candidate_count,
    candidates,
    limit_cases,
):
    """負値・境界値・同点でも、集約前に既定・設定・引数の件数上限を適用する。"""
    # 同じ embedding の候補は本文も共有し、各行の位置と件数を保って cache 保存を減らす。
    root = document_repository
    path = "spec/allowed.md"
    available = len(candidates)
    similarities = sorted((similarity for _, similarity in candidates), reverse=True)
    (root / path).write_text("".join(f"候補 {vector}\n" for vector, _ in candidates))
    worker = candidate_worker(
        {path: [(i + 1, i + 1) for i in range(available)]},
        vectors={path: [vector for vector, _ in candidates]},
    )
    # 負の成分を含む非単位 query で、query 側の正規化も検証する。
    worker.query_vector = (-3, 4)
    with closing(
        DocumentSearch(
            root,
            replace(_tuning(), candidate_count=candidate_count),
            worker=worker,
            installation_root=tmp_path,
        )
    ) as search:
        tool = _listed_search_tool(search)
        # query を変え、各上限で推論経路を残す。
        for request_id, (limit, expected) in enumerate(limit_cases, start=1):
            worker.operations.clear()
            arguments = {"query": f"候補 {request_id}"}
            if limit is not None:
                arguments["limit"] = limit
            Draft202012Validator(tool["inputSchema"]).validate(arguments)
            response = _response(
                {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "method": "tools/call",
                    "params": {"name": "search", "arguments": arguments},
                },
                search,
            )
            result = _assert_search_result(response, tool["outputSchema"], error=False)
            assert result["status"] == "ok"
            if expected:
                assert len(result["hits"]) == 1
                assert result["hits"][0]["path"] == path
                ranges = result["hits"][0]["ranges"]
                assert len(ranges) == expected
                assert all(
                    1 <= location["start_line"] == location["end_line"] <= available
                    and location["max_similarity"]
                    == pytest.approx(candidates[location["start_line"] - 1][1])
                    for location in ranges
                )
                assert [
                    location["max_similarity"] for location in ranges
                ] == pytest.approx(similarities[:expected])
            else:
                assert result["hits"] == []
            assert worker.operations == (["embed_query"] if expected else [])


def test_mcp_aggregates_current_locations_without_excerpts(
    tmp_path, document_repository, candidate_worker
):
    """重複・入れ子・連鎖する重なりの最大値を保ち、ファイルと範囲を類似度順に返す。"""
    root = document_repository
    path = "spec/allowed.md"
    other = "spec/second.md"
    (root / other).write_text("別の原文\n")
    (root / path).write_text("".join(f"原文 {i}\n" for i in range(81)))
    worker = candidate_worker(
        {
            path: [(10, 24), (20, 30), (10, 24), (70, 81), (1, 1), (29, 40), (12, 12)],
            other: [(1, 1)],
        },
        vectors={
            path: [(3, 4), (-3, 4), (3, 4), (4, 3), (-4, 3), (0, 1), (0, 1)],
            other: [(1, 0)],
        },
    )
    with closing(
        DocumentSearch(
            root,
            _tuning(),
            worker=worker,
            installation_root=tmp_path,
        )
    ) as search:
        tool = _listed_search_tool(search)
        response = _response(
            {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "tools/call",
                "params": {"name": "search", "arguments": {"query": "原文"}},
            },
            search,
        )
        result = _assert_search_result(response, tool["outputSchema"], error=False)
    assert result["hits"] == [
        {
            "path": other,
            "ranges": [{"start_line": 1, "end_line": 1, "max_similarity": 1.0}],
        },
        {
            "path": path,
            "ranges": [
                {
                    "start_line": 70,
                    "end_line": 81,
                    "max_similarity": pytest.approx(0.8),
                },
                {
                    "start_line": 10,
                    "end_line": 40,
                    "max_similarity": pytest.approx(0.6),
                },
                {"start_line": 1, "end_line": 1, "max_similarity": pytest.approx(-0.8)},
            ],
        },
    ]


@pytest.mark.parametrize("code", [*get_args(SearchErrorCode.__value__), None])
def test_mcp_search_failures_match_output_schema(tmp_path, monkeypatch, code):
    """定義済みの検索失敗と予期しない例外は、成功を併記しない構造化結果にする。"""
    search = DocumentSearch(tmp_path, None)
    tool = _listed_search_tool(search)

    def fail(*args, **kwargs):
        if code is None:
            raise RuntimeError("unexpected failure")
        raise SearchError(code, "search failed")

    monkeypatch.setattr(search, "search", fail)
    response = _response(
        {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/call",
            "params": {"name": "search", "arguments": {"query": "内容"}},
        },
        search,
    )
    result = _assert_search_result(response, tool["outputSchema"], error=True)
    assert result == {
        "status": "error",
        "code": code or "SYNC_FAILED",
        "message": "search failed" if code else "document search failed",
    }


def test_mcp_cosine_ranking_is_independent_of_candidate_limit(
    tmp_path, document_repository, candidate_worker
):
    """既知の embedding の順位と値を、同じ query の異なる返却件数で検証する。"""
    root = document_repository
    path = "spec/allowed.md"
    # 異なる合法上限 20・21 と未採用候補一件で順位と値を検査する。50 の境界は別ケースで保つ。
    candidate_count = 21
    available = candidate_count + 1
    (root / path).write_text("".join(f"候補 {i}\n" for i in range(available)))
    vectors = [(i - available // 2, 20) for i in range(available)]
    worker = candidate_worker(
        {path: [(i + 1, i + 1) for i in range(available)]}, vectors={path: vectors}
    )
    expected = {i + 1: x / math.hypot(x, y) for i, (x, y) in enumerate(vectors)}
    results = []
    with closing(
        DocumentSearch(
            root,
            replace(_tuning(), candidate_count=candidate_count),
            worker=worker,
            installation_root=tmp_path,
        )
    ) as search:
        tool = _listed_search_tool(search)
        # 省略時の上限は件数境界のケースで検査し、ここでは異なる上限の値を比べる。
        for limit in (20, candidate_count):
            response = _response(
                {
                    "jsonrpc": "2.0",
                    "id": 1,
                    "method": "tools/call",
                    "params": {
                        "name": "search",
                        "arguments": {"query": "候補", "limit": limit},
                    },
                },
                search,
            )
            result = _assert_search_result(response, tool["outputSchema"], error=False)
            assert [hit["path"] for hit in result["hits"]] == [path]
            ranges = result["hits"][0]["ranges"]
            assert [location["start_line"] for location in ranges] == list(
                range(available, available - limit, -1)
            )
            assert all(
                location["start_line"] == location["end_line"]
                and location["max_similarity"]
                == pytest.approx(expected[location["start_line"]], abs=1e-7)
                for location in ranges
            )
            results.append(
                {
                    location["start_line"]: location["max_similarity"]
                    for location in ranges
                }
            )
    limited, expanded = results
    assert all(value == expanded[line] for line, value in limited.items())


def test_mcp_candidate_limit_applies_before_range_merging(
    tmp_path, document_repository, candidate_worker
):
    """採用候補が一範囲へ統合されても、残りの候補で件数を補充しない。"""
    root = document_repository
    path = "spec/allowed.md"
    # 20・21 件の採用で統合前の上限違反を検出する。50 の境界は別ケースで保つ。
    candidate_count = 21
    # 上位 20 件は同じ本文片にし、22 件の候補を三種類の cache 保存だけで用意する。
    # 21 位は上位と重なり、22 位は離す。統合後の補充や上限無視で結果が変わる。
    # 異なる embedding の厳密な順位は直前の専用ケースに残す。
    (root / path).write_text("上限外\n重なる候補\n上位の重複候補\n")
    worker = candidate_worker(
        {path: [(1, 1), (2, 3)] + [(3, 3)] * 20},
        vectors={path: [(0, 1), (3, 4)] + [(1, 0)] * 20},
    )
    with closing(
        DocumentSearch(
            root,
            replace(_tuning(), candidate_count=candidate_count),
            worker=worker,
            installation_root=tmp_path,
        )
    ) as search:
        tool = _listed_search_tool(search)
        # 同じ query の上限だけを変え、索引と query embedding を再利用する。
        for limit, start_line in ((20, 3), (candidate_count, 2)):
            response = _response(
                {
                    "jsonrpc": "2.0",
                    "id": limit,
                    "method": "tools/call",
                    "params": {
                        "name": "search",
                        "arguments": {"query": "候補", "limit": limit},
                    },
                },
                search,
            )
            result = _assert_search_result(response, tool["outputSchema"], error=False)
            assert result["hits"] == [
                {
                    "path": path,
                    "ranges": [
                        {
                            "start_line": start_line,
                            "end_line": 3,
                            "max_similarity": 1.0,
                        }
                    ],
                }
            ], limit


def test_mcp_rejects_invalid_similarity_even_outside_candidate_limit(
    tmp_path, monkeypatch, document_repository, candidate_worker
):
    """採用上限外へ隠れる異常値や演算失敗も、成功を併記せず MODEL_FAILURE にする。"""
    from commons import runtime_document_search as module

    root = document_repository
    path = "spec/allowed.md"
    # 採用上限を満たす正常候補と、上限外にある異常候補一つを用意する。
    candidate_count = 20
    available = candidate_count + 1
    # 同じ正常ベクトルの本文も共有し、位置・件数を保って余分な cache 保存を省く。
    (root / path).write_text("異常候補\n" + "正常候補\n" * candidate_count)
    worker = candidate_worker(
        {path: [(i + 1, i + 1) for i in range(available)]},
        vectors={path: [(0, 1)] + [(1, 0)] * candidate_count},
    )
    original_open = module._open_database

    def cosine_distance(embedding, query):
        nonlocal invalid_distance_evaluated
        if struct.unpack_from("<f", embedding)[0] != 0:
            return 0.0
        invalid_distance_evaluated = True
        if isinstance(distance, Exception):
            raise distance
        return distance

    def open_with_invalid_distance(database):
        connection = original_open(database)
        connection.create_function("vec_distance_cosine", 2, cosine_distance)
        return connection

    monkeypatch.setattr(module, "_open_database", open_with_invalid_distance)
    with closing(
        DocumentSearch(
            root,
            replace(_tuning(), candidate_count=candidate_count),
            worker=worker,
            installation_root=tmp_path,
        )
    ) as search:
        tool = _listed_search_tool(search)
        # 変えるのは距離演算だけなので、索引と query embedding を再利用する。
        for request_id, distance in enumerate(
            [
                None,
                "invalid",
                "0.25",
                b"bad",
                math.nan,
                math.inf,
                -math.inf,
                -0.001,
                2.001,
                RuntimeError("cosine calculation failed"),
            ],
            start=1,
        ):
            invalid_distance_evaluated = False
            response = _response(
                {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "method": "tools/call",
                    "params": {
                        "name": "search",
                        "arguments": {"query": "候補"},
                    },
                },
                search,
            )
            result = _assert_search_result(response, tool["outputSchema"], error=True)
            # 同じ query の失敗を再利用して、後続の異常条件を素通りさせない。
            assert invalid_distance_evaluated, repr(distance)
            assert result["status"] == "error", repr(distance)
            assert result["code"] == "MODEL_FAILURE", repr(distance)


@pytest.mark.parametrize(
    "value",
    [
        {"status": "ok"},
        {"status": "ok", "hits": [], "code": "SYNC_FAILED"},
        {"status": "error", "code": "UNKNOWN", "message": "failed"},
        {"status": "error", "code": "SYNC_FAILED"},
        *(
            {"status": "ok", "hits": [hit]}
            for hit in [
                {
                    "path": "spec/a.md",
                    "start_line": 1,
                    "end_line": 2,
                    "excerpt": "old",
                },
                {"path": "spec/a.md", "ranges": []},
                {"path": "spec/a.md", "ranges": [[1, 2]]},
                *(
                    {"path": "spec/a.md", "ranges": [location]}
                    for location in [
                        {"start_line": 1, "end_line": 2},
                        {"start_line": 0, "end_line": 2, "max_similarity": 0.5},
                        {"start_line": True, "end_line": 2, "max_similarity": 0.5},
                        {"start_line": 1, "end_line": 0, "max_similarity": 0.5},
                        {"start_line": 1, "end_line": False, "max_similarity": 0.5},
                        {
                            "start_line": 1,
                            "end_line": 2,
                            "max_similarity": 0.5,
                            "excerpt": "extra",
                        },
                        *(
                            {"start_line": 1, "end_line": 2, "max_similarity": value}
                            for value in (True, "0.5", None, -1.001, 1.001)
                        ),
                    ]
                ),
                {
                    "path": "spec/a.md",
                    "ranges": [{"start_line": 1, "end_line": 2, "max_similarity": 0.5}],
                    "excerpt": "extra",
                },
            ]
        ),
    ],
)
def test_output_schema_rejects_malformed_results(value):
    """旧形式や成功・失敗の混在、行範囲の型違いを公開 schema で検出する。"""
    # 公開値の一致は stdio test で検査し、schema 単体の検査には検索 context を作らない。
    assert not Draft202012Validator(SEARCH_TOOL_OUTPUT_SCHEMA).is_valid(value)


def test_worker_change_rebuilds_index_and_reuses_compatible_embeddings(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    document_repository: Path,
    unsynced_search_storage: None,
) -> None:
    """分割実装の変更では索引を再構築し、互換な同一入力片を引き継ぐ。"""
    from commons import runtime_document_search as module

    root = document_repository
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
                _tuning(),
                worker=_InferenceDouble(),
                installation_root=tmp_path,
            )
        ) as search:
            result = search.synchronize()
            results.append(result)
    first, second = results
    assert second.identity != first.identity
    assert second.chunk_count == first.chunk_count > 0
    assert second.reused_embeddings == second.chunk_count


def test_search_rechecks_saved_config_for_each_request(
    tmp_path: Path, document_repository: Path, unsynced_search_storage: None
) -> None:
    """起動後の有効な変更は新索引を使い、不備は旧設定へ戻さず拒否する。"""
    root = document_repository
    path = root / ".cmoc/gt/config.json"
    write_config(path, CmocConfig())
    search = DocumentSearch(
        root,
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
        assert "手動" in str(exc_info.value)
    finally:
        search.close()


def test_stdio_mcp_discovers_only_search_and_reports_not_ready(
    tmp_path: Path,
) -> None:
    """実 stdio 境界で正本の公開定義を伝え、未準備を識別できる。"""
    # 未準備の応答は文書同期より前に返るため、Git と検索文書を準備しない。
    root = tmp_path / "repo"
    root.mkdir()
    log_path = tmp_path / "caller.jsonl"
    log_path.touch()
    context = {
        "work_root": str(root),
        "config": None,
        "log_context": {
            "path": str(log_path),
            "command": "oracle investigation",
            "execution_id": "exec_test",
            "codex_call_id": "cc_test",
        },
    }
    project = Path(__file__).resolve().parents[1]
    environment = {
        **os.environ,
        "PYTHONPATH": os.pathsep.join(
            (str(project / "src"), str(project / "reference/src"))
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
        tool = listed["result"]["tools"][0]
        assert tool["inputSchema"] == SEARCH_TOOL_INPUT_SCHEMA
        assert tool["outputSchema"] == SEARCH_TOOL_OUTPUT_SCHEMA
        for schema in (tool["inputSchema"], tool["outputSchema"]):
            Draft202012Validator.check_schema(schema)
        assert tool["description"] == build_search_tool_description(root)
        failed = request(
            3, "tools/call", {"name": "search", "arguments": {"query": "内容"}}
        )
        failure = _assert_search_result(failed, tool["outputSchema"], error=True)
        assert failure["code"] == "NOT_READY"
        invalid = request(
            4,
            "tools/call",
            {"name": "search", "arguments": {"query": "内容", "limit": 19}},
        )
        assert invalid["error"]["code"] == -32602
        assert "result" not in invalid
        process.stdin.close()
        assert process.wait(timeout=5) == 0
    events = [json.loads(line) for line in log_path.read_text().splitlines()]
    assert [event["event"] for event in events] == [
        "document_search_request_started",
        "document_search_request_finished",
    ]
    assert events[0]["request_id"] == events[-1]["request_id"]
    assert events[-1]["failure_code"] == "NOT_READY"
    assert events[-1]["decision_seconds"]["post_sync_search"] is None
    assert all(event["codex_call_id"] == "cc_test" for event in events)
    assert all(event["command"] == "oracle investigation" for event in events)


@pytest.mark.skipif(shutil.which("node") is None, reason="Node.js is unavailable")
def test_worker_cancellation_reaps_process_before_releasing_owner(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """通信のタイムアウト後も取消を検出し、実子 process を回収してから返す。"""
    base = materials_directory(tmp_path)
    base.mkdir(parents=True)
    _test_node_runtime(base)
    (base / "worker.mjs").write_text(
        "console.log(process.pid); setInterval(() => {}, 1000);\n"
    )
    worker = NodeSearchWorker(tmp_path, _tuning())
    cancelled = threading.Event()
    processes = []

    def cancel_during_communication(process, input, *, timeout):
        # 起動通知を受けてから取消し、実時間の通信 timeout と監視 thread を省く。
        # TimeoutExpired 後の再判定は製品の loop を通し、停止・wait も実行する。
        assert not processes, "worker communicated again after cancellation"
        processes.append(process)
        assert json.loads(input)["operation"] == "embed_query"
        readable, _, _ = select.select([process.stdout], [], [], 5)
        assert readable, "worker did not announce startup"
        assert int(process.stdout.readline()) == process.pid
        assert process.poll() is None
        cancelled.set()
        raise subprocess.TimeoutExpired(process.args, timeout)

    monkeypatch.setattr(subprocess.Popen, "communicate", cancel_during_communication)
    descriptor = os.open(tmp_path / "lock", os.O_CREAT | os.O_RDWR, 0o600)
    try:
        with pytest.raises(SearchError) as failure:
            worker.run(
                "embed_query",
                {"text": "test"},
                deadline=time.monotonic() + 10,
                residency_fd=descriptor,
                cancelled=cancelled,
            )
        assert failure.value.code == "CANCELLED"
        assert len(processes) == 1
        assert processes[0].returncode is not None
        with pytest.raises(ProcessLookupError):
            os.kill(processes[0].pid, 0)
    finally:
        # 回収の回帰があっても、test が起動した子 process を残さない。
        for process in processes:
            if process.poll() is None:
                process.kill()
            process.wait(timeout=5)
            for pipe in (process.stdin, process.stdout, process.stderr):
                if pipe is not None:
                    pipe.close()
        os.close(descriptor)
