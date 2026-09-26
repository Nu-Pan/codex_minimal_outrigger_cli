"""文書検索の範囲、現在本文との同期、失敗公開を検証する。"""

import json
import os
import select
import shutil
import subprocess
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import pytest
from _cli_support import run_doctor, runner, terminal_primary_report
from _git_support import make_repo, run_git
from oracle.acp_builder.basic import DocumentSearchScope
from oracle.other.document_search import INITIAL_SEARCH_MATERIALS, DocumentSearchConfig

from commons.runtime_document_search import DocumentSearch, SearchError, scan_documents
from commons.runtime_document_search_mcp import _response
from commons.runtime_document_search_worker import NodeSearchWorker, materials_directory
from commons.runtime_git import ensure_cmoc_ignored
from main import app


def _tuning() -> DocumentSearchConfig:
    """推論 double にだけ使う、製品既定値ではない test 設定。"""
    return DocumentSearchConfig(32, 0, 3, 128, 128, 128, 1, 10.0, 30.0, 1.0)


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
        deadline: float,
        residency_fd: int,
        cancelled: threading.Event | None = None,
    ) -> object:
        """実モデル以外の同期・cache 境界に対する確定的な応答。"""
        self.operations.append(operation)
        vector = [1.0] + [0.0] * (INITIAL_SEARCH_MATERIALS.embedding_dimensions - 1)
        if operation == "chunk_embed":
            documents = payload["documents"]
            assert isinstance(documents, dict)
            self.texts.extend(documents.values())
            return {
                path: [{"start": 0, "end": len(text), "embedding": vector}]
                for path, text in documents.items()
            }
        if operation == "embed_query":
            return vector
        assert operation == "rerank"
        documents = payload["documents"]
        assert isinstance(documents, list)
        self.texts.extend(documents)
        return [0.8 for _ in documents]


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
        def run(
            self,
            operation: str,
            payload: dict[str, object],
            *,
            deadline: float,
            residency_fd: int,
            cancelled: threading.Event | None = None,
        ) -> object:
            if operation == "chunk_embed":
                started.set()
                assert release.wait(5)
            return normal_worker.run(
                operation,
                payload,
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


def test_indexing_accepts_dirty_tree_and_reports_not_ready(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """明示同期は既存差分を commit せず、未設定を機械的に報告する。"""
    root = _repo_with_docs(tmp_path)
    monkeypatch.chdir(root)
    assert run_doctor(root).exit_code == 0
    before_head = run_git(root, "rev-parse", "HEAD").stdout.strip()
    (root / "README.md").write_text("# dirty\n")
    outcome = runner.invoke(app, ["indexing"], catch_exceptions=False)
    assert outcome.exit_code == 1
    assert run_git(root, "rev-parse", "HEAD").stdout.strip() == before_head
    assert (root / "README.md").read_text() == "# dirty\n"
    report = terminal_primary_report(outcome).read_text()
    assert 'failure_code: "NOT_READY"' in report
    assert "updated_indexes" not in report
