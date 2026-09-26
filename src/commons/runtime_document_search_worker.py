"""固定資材を検査し、許可済み本文を一時的な Node 推論へ渡す。"""

import hashlib
import json
import os
import signal
import stat
import subprocess
import threading
import time
from importlib import resources
from pathlib import Path

from oracle.other.document_search import (
    INITIAL_SEARCH_MATERIALS,
    DocumentSearchConfig,
)

from .runtime_document_search import SearchError


def materials_directory(installation_root: Path) -> Path:
    """共有モデルと runtime の固定資材を収める場所。"""
    return installation_root / ".cmoc/gu/document_search/materials"


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _runtime_tree_hash(base: Path) -> str:
    """npm が設置した runtime 全体の内容と symlink 構造を識別する。"""
    root = base / "node_modules"
    if root.is_symlink() or not root.is_dir():
        raise ValueError("node runtime is unavailable")
    digest = hashlib.sha256()
    for path in sorted(root.rglob("*")):
        mode = path.lstat().st_mode
        if stat.S_ISDIR(mode):
            continue
        relative = path.relative_to(root).as_posix()
        if stat.S_ISLNK(mode):
            if not path.resolve(strict=True).is_relative_to(root.resolve()):
                raise ValueError("node runtime contains an external symlink")
            value = "link:" + os.readlink(path)
        elif stat.S_ISREG(mode):
            value = "file:" + _sha256(path)
        else:
            raise ValueError("node runtime contains a special file")
        digest.update(relative.encode("utf-8") + b"\0" + value.encode("utf-8") + b"\0")
    return digest.hexdigest()


def verify_search_materials(installation_root: Path) -> Path:
    """推論起動前に配布物と設置済み資材の identity を照合する。"""
    base = materials_directory(installation_root)
    manifest = base / "manifest.json"
    if not manifest.is_file() or manifest.is_symlink():
        raise SearchError("NOT_READY", "document search materials are not installed")
    try:
        data = json.loads(manifest.read_text(encoding="utf-8"))
        with resources.as_file(
            resources.files("commons.document_search_worker").joinpath("worker.mjs")
        ) as source_worker:
            expected_worker_hash = _sha256(source_worker)
        with resources.as_file(
            resources.files("commons.document_search_worker").joinpath("package.json")
        ) as source_package:
            expected_package_hash = _sha256(source_package)
        with resources.as_file(
            resources.files("commons.document_search_worker").joinpath(
                "package-lock.json"
            )
        ) as source_lock:
            expected_lock_hash = _sha256(source_lock)
        try:
            runtime_tree_hash = _runtime_tree_hash(base)
        except (OSError, ValueError) as exc:
            raise SearchError(
                "MODEL_IDENTITY_MISMATCH", "node runtime is incompatible"
            ) from exc
        if data != {
            "worker_sha256": expected_worker_hash,
            "package_sha256": expected_package_hash,
            "lock_sha256": expected_lock_hash,
            "runtime_tree_sha256": runtime_tree_hash,
            "materials": {
                "node_version": INITIAL_SEARCH_MATERIALS.node_version,
                "node_llama_cpp_version": INITIAL_SEARCH_MATERIALS.node_llama_cpp_version,
                "llama_cpp_revision": INITIAL_SEARCH_MATERIALS.llama_cpp_revision,
                "sqlite_vec_version": INITIAL_SEARCH_MATERIALS.sqlite_vec_version,
                "embedding_sha256": INITIAL_SEARCH_MATERIALS.embedding.sha256,
                "reranker_sha256": INITIAL_SEARCH_MATERIALS.reranker.sha256,
            },
        }:
            raise SearchError("MODEL_IDENTITY_MISMATCH", "material manifest mismatch")
        for filename, expected_hash, expected_size in (
            (
                INITIAL_SEARCH_MATERIALS.embedding.filename,
                INITIAL_SEARCH_MATERIALS.embedding.sha256,
                INITIAL_SEARCH_MATERIALS.embedding.size_bytes,
            ),
            (
                INITIAL_SEARCH_MATERIALS.reranker.filename,
                INITIAL_SEARCH_MATERIALS.reranker.sha256,
                INITIAL_SEARCH_MATERIALS.reranker.size_bytes,
            ),
        ):
            path = base / filename
            if path.is_symlink() or not path.is_file():
                raise SearchError("NOT_READY", "document search model is unavailable")
            if path.stat().st_size != expected_size or _sha256(path) != expected_hash:
                raise SearchError("MODEL_IDENTITY_MISMATCH", "model checksum mismatch")
        for filename, expected_hash in (
            ("worker.mjs", expected_worker_hash),
            ("package.json", expected_package_hash),
            ("package-lock.json", expected_lock_hash),
        ):
            path = base / filename
            if (
                path.is_symlink()
                or not path.is_file()
                or _sha256(path) != expected_hash
            ):
                raise SearchError("MODEL_IDENTITY_MISMATCH", "worker material mismatch")
        installed_package = json.loads(
            (base / "node_modules/node-llama-cpp/package.json").read_text(
                encoding="utf-8"
            )
        )
        if (
            installed_package.get("version")
            != INITIAL_SEARCH_MATERIALS.node_llama_cpp_version
        ):
            raise SearchError(
                "MODEL_IDENTITY_MISMATCH", "node-llama-cpp version mismatch"
            )
        node_version = (
            subprocess.run(
                ["node", "--version"],
                capture_output=True,
                text=True,
                check=True,
                timeout=5,
            )
            .stdout.strip()
            .removeprefix("v")
        )
        if node_version != INITIAL_SEARCH_MATERIALS.node_version:
            raise SearchError("MODEL_IDENTITY_MISMATCH", "Node version mismatch")
    except SearchError:
        raise
    except (OSError, ValueError, KeyError, subprocess.SubprocessError) as exc:
        raise SearchError(
            "NOT_READY", "document search materials are incomplete"
        ) from exc
    return base


class NodeSearchWorker:
    """モデルを要求単位でロードし、終了まで常駐枠の fd を保持する。"""

    def __init__(
        self, installation_root: Path, config: DocumentSearchConfig | None
    ) -> None:
        """固定資材の配置を記録する。"""
        self.base = materials_directory(installation_root)
        self.config = config

    def run(
        self,
        operation: str,
        payload: dict[str, object],
        *,
        deadline: float,
        residency_fd: int,
        cancelled: threading.Event | None = None,
    ) -> object:
        """子 process を同期実行し、期限時も停止・回収してから返す。"""
        if self.config is None:
            raise SearchError("NOT_READY", "document search tuning is not configured")
        try:
            parent_start_time = (
                Path(f"/proc/{os.getpid()}/stat")
                .read_text()
                .rsplit(") ", 1)[1]
                .split()[19]
            )
        except (OSError, IndexError) as exc:
            raise SearchError(
                "MODEL_FAILURE", "parent identity is unavailable"
            ) from exc
        request = {
            "operation": operation,
            "payload": payload,
            "embedding_model": str(
                self.base / INITIAL_SEARCH_MATERIALS.embedding.filename
            ),
            "reranker_model": str(
                self.base / INITIAL_SEARCH_MATERIALS.reranker.filename
            ),
            "dimensions": INITIAL_SEARCH_MATERIALS.embedding_dimensions,
            "parent_pid": os.getpid(),
            "parent_start_time": parent_start_time,
        }
        try:
            process = subprocess.Popen(
                ["node", str(self.base / "worker.mjs")],
                cwd=self.base,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding="utf-8",
                pass_fds=(residency_fd,),
                start_new_session=True,
                env={**os.environ, "NODE_LLAMA_CPP_SKIP_DOWNLOAD": "true"},
            )
        except OSError as exc:
            raise SearchError(
                "MODEL_FAILURE", "inference worker could not start"
            ) from exc
        pending_input: str | None = json.dumps(request, ensure_ascii=False)
        try:
            while True:
                if cancelled is not None and cancelled.is_set():
                    raise SearchError("CANCELLED", "document search was cancelled")
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    raise SearchError(
                        "DEADLINE_EXCEEDED", "inference deadline exceeded"
                    )
                try:
                    stdout, _ = process.communicate(
                        pending_input, timeout=min(0.2, remaining)
                    )
                    break
                except subprocess.TimeoutExpired:
                    pending_input = None
        except BaseException as exc:
            try:
                os.killpg(process.pid, signal.SIGTERM)
            except ProcessLookupError:
                pass
            try:
                process.communicate(timeout=self.config.shutdown_grace_seconds)
            except subprocess.TimeoutExpired:
                try:
                    os.killpg(process.pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
                process.communicate()
            if isinstance(exc, KeyboardInterrupt):
                raise SearchError("CANCELLED", "document search was cancelled") from exc
            raise
        if cancelled is not None and cancelled.is_set():
            raise SearchError("CANCELLED", "document search was cancelled")
        if process.returncode != 0:
            raise SearchError("MODEL_FAILURE", "inference worker failed")
        try:
            response = json.loads(stdout)
        except (ValueError, UnicodeError) as exc:
            raise SearchError(
                "MODEL_FAILURE", "inference worker output is invalid"
            ) from exc
        if not isinstance(response, dict) or response.get("status") != "ok":
            raise SearchError("MODEL_FAILURE", "inference worker rejected the request")
        return response.get("result")
