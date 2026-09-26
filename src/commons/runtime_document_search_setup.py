"""固定文書検索資材を cmoc installation の非追跡領域へ準備する。"""

import hashlib
import importlib
import json
import math
import os
import shutil
import sqlite3
import subprocess
import sys
import tempfile
import time
import urllib.request
from importlib import resources
from pathlib import Path
from urllib.parse import quote

from oracle.other.document_search import INITIAL_SEARCH_MATERIALS, ModelArtifact

from .runtime_document_search_worker import (
    _runtime_tree_hash,
    _sha256,
    materials_directory,
)
from .runtime_git import ensure_cmoc_ignored, require_cmoc_ignored
from .runtime_paths import cmoc_root


def _download_model(base: Path, artifact: ModelArtifact) -> None:
    """固定 revision の GGUF をサイズと SHA-256 で確認して公開する。"""
    destination = base / artifact.filename
    if destination.is_file() and not destination.is_symlink():
        if (
            destination.stat().st_size == artifact.size_bytes
            and _sha256(destination) == artifact.sha256
        ):
            return
    url = (
        f"https://huggingface.co/{artifact.repository}/resolve/"
        f"{artifact.revision}/{quote(artifact.filename)}"
    )
    descriptor, temporary = tempfile.mkstemp(prefix=f".{artifact.filename}.", dir=base)
    temporary_path = Path(temporary)
    digest = hashlib.sha256()
    size = 0
    try:
        with (
            os.fdopen(descriptor, "wb") as output,
            urllib.request.urlopen(url, timeout=60) as source,
        ):
            while block := source.read(1024 * 1024):
                output.write(block)
                digest.update(block)
                size += len(block)
                if size > artifact.size_bytes:
                    raise ValueError("downloaded model exceeds fixed size")
            output.flush()
            os.fsync(output.fileno())
        if size != artifact.size_bytes or digest.hexdigest() != artifact.sha256:
            raise ValueError(f"model checksum mismatch: {artifact.filename}")
        os.replace(temporary_path, destination)
    finally:
        temporary_path.unlink(missing_ok=True)


def _copy_worker_source(base: Path, filename: str) -> str:
    """package に固定した worker file を配置し hash を返す。"""
    source = resources.files("commons.document_search_worker").joinpath(filename)
    with resources.as_file(source) as path:
        digest = _sha256(path)
        target = base / filename
        if not target.is_file() or target.is_symlink() or _sha256(target) != digest:
            shutil.copyfile(path, target)
        return digest


def _runtime_versions(base: Path) -> None:
    """Node と sqlite-vec を固定版として確認する。"""
    node = (
        subprocess.run(
            ["node", "--version"], check=True, capture_output=True, text=True, timeout=5
        )
        .stdout.strip()
        .removeprefix("v")
    )
    if node != INITIAL_SEARCH_MATERIALS.node_version:
        raise ValueError("Node version does not match fixed materials")
    sqlite_vec = importlib.import_module("sqlite_vec")

    connection = sqlite3.connect(":memory:")
    try:
        connection.enable_load_extension(True)
        sqlite_vec.load(connection)
        connection.enable_load_extension(False)
        version = connection.execute("select vec_version()").fetchone()[0]
    finally:
        connection.close()
    if version.removeprefix("v") != INITIAL_SEARCH_MATERIALS.sqlite_vec_version:
        raise ValueError("sqlite-vec version does not match fixed materials")
    package = json.loads(
        (base / "node_modules/node-llama-cpp/package.json").read_text(encoding="utf-8")
    )
    if package.get("version") != INITIAL_SEARCH_MATERIALS.node_llama_cpp_version:
        raise ValueError("node-llama-cpp version does not match fixed materials")


def _compatibility_probe(base: Path) -> None:
    """固定 3.20.0 の embedding と raw rerank を実モデルで通す。"""
    start_time = (
        Path(f"/proc/{os.getpid()}/stat").read_text().rsplit(") ", 1)[1].split()[19]
    )
    config = {
        "chunk_tokens": 128,
        "chunk_overlap_tokens": 0,
        "candidate_count": 1,
        "embedding_context_tokens": 512,
        "reranker_context_tokens": 512,
        "batch_tokens": 512,
        "threads": 1,
        "startup_timeout_seconds": 120.0,
        "request_timeout_seconds": 600.0,
        "shutdown_grace_seconds": 5.0,
    }
    common = {
        "embedding_model": str(base / INITIAL_SEARCH_MATERIALS.embedding.filename),
        "reranker_model": str(base / INITIAL_SEARCH_MATERIALS.reranker.filename),
        "dimensions": INITIAL_SEARCH_MATERIALS.embedding_dimensions,
        "parent_pid": os.getpid(),
        "parent_start_time": start_time,
    }
    cases = (
        ("embed_query", {"text": "日本語の検索", "config": config}),
        (
            "rerank",
            {
                "query": "日本語の検索",
                "documents": ["関連する日本語の文書です。"],
                "config": config,
                "input_format": "gguf_template_yes_no",
            },
        ),
    )
    for operation, payload in cases:
        result = subprocess.run(
            ["node", str(base / "worker.mjs")],
            input=json.dumps(
                {**common, "operation": operation, "payload": payload},
                ensure_ascii=False,
            ),
            cwd=base,
            capture_output=True,
            text=True,
            timeout=600,
            env={**os.environ, "NODE_LLAMA_CPP_SKIP_DOWNLOAD": "true"},
            check=True,
        )
        value = json.loads(result.stdout)
        if value.get("status") != "ok" or not isinstance(value.get("result"), list):
            raise ValueError(f"inference compatibility check failed: {operation}")
        if len(value["result"]) != (
            INITIAL_SEARCH_MATERIALS.embedding_dimensions
            if operation == "embed_query"
            else 1
        ):
            raise ValueError(f"inference output is incomplete: {operation}")
        if not all(
            type(item) in (int, float) and math.isfinite(item)
            for item in value["result"]
        ):
            raise ValueError(f"inference output is invalid: {operation}")
        if operation == "embed_query" and not any(value["result"]):
            raise ValueError("embedding compatibility check returned zero vector")


def setup_document_search() -> Path:
    """共有 root の非追跡保証後、固定資材と互換性検査を完了する。"""
    root = cmoc_root()
    ensure_cmoc_ignored(root)
    require_cmoc_ignored(root)
    base = materials_directory(root)
    from .runtime_document_search import _file_lock, _safe_directory

    _safe_directory(base)

    residency = base.parent / "residency/model.lock"
    with _file_lock(residency, time.monotonic() + 900):
        worker_sha = _copy_worker_source(base, "worker.mjs")
        package_sha = _copy_worker_source(base, "package.json")
        lock_sha = _copy_worker_source(base, "package-lock.json")
        subprocess.run(
            ["npm", "ci", "--ignore-scripts", "--no-audit", "--no-fund"],
            cwd=base,
            env={**os.environ, "npm_config_cache": str(base / "npm-cache")},
            check=True,
        )
        _runtime_versions(base)
        _download_model(base, INITIAL_SEARCH_MATERIALS.embedding)
        _download_model(base, INITIAL_SEARCH_MATERIALS.reranker)
        _compatibility_probe(base)
        manifest = {
            "worker_sha256": worker_sha,
            "package_sha256": package_sha,
            "lock_sha256": lock_sha,
            "runtime_tree_sha256": _runtime_tree_hash(base),
            "materials": {
                "node_version": INITIAL_SEARCH_MATERIALS.node_version,
                "node_llama_cpp_version": INITIAL_SEARCH_MATERIALS.node_llama_cpp_version,
                "llama_cpp_revision": INITIAL_SEARCH_MATERIALS.llama_cpp_revision,
                "sqlite_vec_version": INITIAL_SEARCH_MATERIALS.sqlite_vec_version,
                "embedding_sha256": INITIAL_SEARCH_MATERIALS.embedding.sha256,
                "reranker_sha256": INITIAL_SEARCH_MATERIALS.reranker.sha256,
            },
        }
        temporary = base / "manifest.json.tmp"
        temporary.write_text(
            json.dumps(manifest, sort_keys=True) + "\n", encoding="utf-8"
        )
        os.replace(temporary, base / "manifest.json")
    return base


def main() -> None:
    """セットアップ専用 entrypoint。"""
    try:
        print(setup_document_search())
    except (OSError, ValueError, subprocess.SubprocessError) as exc:
        print(f"document search setup failed: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc


if __name__ == "__main__":
    main()
