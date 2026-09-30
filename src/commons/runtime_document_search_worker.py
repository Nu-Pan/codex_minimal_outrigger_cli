"""固定資材を検査し、許可済み本文を一時的な Node 推論へ渡す。"""

import hashlib
import importlib
import json
import os
import platform
import re
import select
import signal
import sqlite3
import stat
import subprocess
import sys
import threading
import time
from dataclasses import asdict
from importlib import resources
from pathlib import Path
from typing import Callable

from markdown_it import MarkdownIt
from oracle.other.document_search import (
    EMBEDDING_QUERY_TEMPLATE,
    INITIAL_SEARCH_MATERIALS,
    RAW_RANKING_API,
    RERANKER_INPUT_FORMAT,
    DocumentSearchConfig,
)

from .runtime_document_search import SearchError
from .runtime_document_search_observation import inference_config


def materials_directory(installation_root: Path) -> Path:
    """共有モデルと runtime の固定資材を収める場所。"""
    return installation_root / ".cmoc/gu/document_search/materials"


def _heading_ranges(text: str) -> list[tuple[int, int]]:
    """Markdown の見出し行で区切り、原文の文字 offset を保つ。"""
    line_starts = [0]
    line_starts.extend(match.end() for match in re.finditer(r"\r\n|\n|\r", text))
    boundaries = [0]
    for token in MarkdownIt("commonmark").parse(text):
        if token.type == "heading_open" and token.map is not None:
            offset = line_starts[token.map[0]]
            if offset != boundaries[-1]:
                boundaries.append(offset)
    boundaries.append(len(text))
    return list(zip(boundaries, boundaries[1:]))


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


def verification_condition(config: DocumentSearchConfig) -> str:
    """実モデル検証を再利用できる実行環境と設定を識別する。"""
    condition = {
        "config": inference_config(config),
        "python": sys.version,
        "executable": str(Path(sys.executable).resolve()),
        "platform": platform.platform(),
        "machine": platform.machine(),
        "query_template": EMBEDDING_QUERY_TEMPLATE,
        "reranker_input_format": RERANKER_INPUT_FORMAT,
        "raw_ranking_api": RAW_RANKING_API,
    }
    return hashlib.sha256(json.dumps(condition, sort_keys=True).encode()).hexdigest()


def _verify_vector_dependency() -> None:
    """宣言した sqlite-vec の native extension を実際にロードして使用する。"""
    sqlite_vec = importlib.import_module("sqlite_vec")
    connection = sqlite3.connect(":memory:")
    try:
        connection.enable_load_extension(True)
        sqlite_vec.load(connection)
        connection.enable_load_extension(False)
        version = connection.execute("select vec_version()").fetchone()[0]
        connection.execute("create virtual table probe using vec0(embedding float[2])")
        connection.execute("insert into probe(rowid, embedding) values(1, '[1,0]')")
        connection.execute(
            "select distance from probe where embedding match '[1,0]' and k = 1"
        ).fetchone()
    finally:
        connection.close()
    if version.removeprefix("v") != INITIAL_SEARCH_MATERIALS.sqlite_vec_version:
        raise ValueError("sqlite-vec version mismatch")


def _verify_lock(base: Path) -> None:
    """npm lock の推移的依存と CPU native 配布物が固定されていることを確認する。"""
    lock = json.loads((base / "package-lock.json").read_text(encoding="utf-8"))
    packages = lock["packages"]
    if lock.get("lockfileVersion") != 3 or not isinstance(packages, dict):
        raise ValueError("npm lock is incomplete")
    for name, package in packages.items():
        if not name or package.get("link"):
            continue
        if not package.get("version") or not package.get("integrity"):
            raise ValueError(f"npm dependency is not pinned: {name}")
    native = packages.get("node_modules/@node-llama-cpp/linux-x64", {})
    if (
        native.get("version") != INITIAL_SEARCH_MATERIALS.node_llama_cpp_version
        or not native.get("integrity")
        or not (base / "node_modules/@node-llama-cpp/linux-x64").is_dir()
    ):
        raise ValueError("CPU native runtime is unavailable")


def verify_search_materials(
    installation_root: Path, config: DocumentSearchConfig | None = None
) -> Path:
    """資材 identity と、指定設定で完了済みの実モデル検証を照合する。"""
    base = materials_directory(installation_root)
    if base.is_symlink() or not base.is_dir():
        raise SearchError(
            "NOT_READY", "document search material directory is unavailable"
        )
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
        expected = {
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
                "embedding_tokenizer_sha256": INITIAL_SEARCH_MATERIALS.embedding.tokenizer_metadata_sha256,
                "reranker_tokenizer_sha256": INITIAL_SEARCH_MATERIALS.reranker.tokenizer_metadata_sha256,
                "embedding_pooling": INITIAL_SEARCH_MATERIALS.embedding.pooling,
                "reranker_pooling": INITIAL_SEARCH_MATERIALS.reranker.pooling,
                "embedding_dimensions": INITIAL_SEARCH_MATERIALS.embedding_dimensions,
            },
        }
        if not isinstance(data, dict) or any(
            data.get(key) != value for key, value in expected.items()
        ):
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
        _verify_lock(base)
        _verify_vector_dependency()
        if config is not None:
            verified = data.get("verified_conditions")
            if (
                not isinstance(verified, dict)
                or verified.get(verification_condition(config))
                != "document-query-rerank"
            ):
                raise SearchError(
                    "NOT_READY",
                    "real-model validation is missing for current conditions",
                )
    except SearchError:
        raise
    except (
        OSError,
        ValueError,
        KeyError,
        ImportError,
        sqlite3.Error,
        subprocess.SubprocessError,
    ) as exc:
        raise SearchError(
            "NOT_READY", "document search materials are incomplete"
        ) from exc
    return base


class NodeSearchWorker:
    """モデルを要求単位でロードし、終了まで常駐枠の fd を保持する。"""

    def __init__(
        self,
        installation_root: Path,
        config: DocumentSearchConfig | None,
        *,
        material_base: Path | None = None,
        check: Callable[[], None] | None = None,
        on_failure: Callable[[BaseException], None] | None = None,
    ) -> None:
        """固定資材の配置を記録する。"""
        self.base = material_base or materials_directory(installation_root)
        self.config = config
        self.check = check
        self.on_failure = on_failure

    def _request(self, operation: str, payload: dict[str, object]) -> dict[str, object]:
        """生存監視に使う親 process の identity を付ける。"""
        if operation in ("chunk_embed", "chunk_stream"):
            documents = payload.get("documents")
            if not isinstance(documents, dict) or not all(
                isinstance(path, str) and isinstance(body, str)
                for path, body in documents.items()
            ):
                raise SearchError("MODEL_FAILURE", "invalid document text")
            payload = {
                **payload,
                "sections": {
                    path: _heading_ranges(body) for path, body in documents.items()
                },
            }
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
        return {
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

    def _stop_process(
        self, process: subprocess.Popen[str] | subprocess.Popen[bytes]
    ) -> None:
        """子 process group を有限猶予で止め、fd を解放する。"""
        assert self.config is not None
        try:
            os.killpg(process.pid, signal.SIGTERM)
        except ProcessLookupError:
            pass
        try:
            process.wait(timeout=self.config.shutdown_grace_seconds)
        except subprocess.TimeoutExpired:
            pass
        # 親が先に終了しても同じ process group の descendant を残さない。
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        process.wait()
        for pipe in (process.stdin, process.stdout, process.stderr):
            if pipe is not None:
                pipe.close()

    def run(
        self,
        operation: str,
        payload: dict[str, object],
        *,
        deadline: float | None,
        residency_fd: int,
        cancelled: threading.Event | None = None,
    ) -> object:
        """子 process を同期実行し、期限時も停止・回収してから返す。"""
        if self.config is None:
            raise SearchError("NOT_READY", "document search tuning is not configured")
        request = self._request(operation, payload)
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
                if self.check is not None:
                    self.check()
                if cancelled is not None and cancelled.is_set():
                    raise SearchError("CANCELLED", "document search was cancelled")
                remaining = None if deadline is None else deadline - time.monotonic()
                if remaining is not None and remaining <= 0:
                    raise SearchError(
                        "DEADLINE_EXCEEDED", "inference deadline exceeded"
                    )
                try:
                    stdout, _ = process.communicate(
                        pending_input,
                        timeout=0.2 if remaining is None else min(0.2, remaining),
                    )
                    break
                except subprocess.TimeoutExpired:
                    pending_input = None
        except OSError as exc:
            failure = SearchError("MODEL_FAILURE", "inference worker I/O failed")
            if self.on_failure is not None:
                self.on_failure(failure)
            self._stop_process(process)
            raise failure from exc
        except BaseException as exc:
            interruption = (
                SearchError("CANCELLED", "document search was cancelled")
                if isinstance(exc, KeyboardInterrupt)
                else exc
            )
            if self.on_failure is not None:
                self.on_failure(interruption)
            self._stop_process(process)
            if isinstance(exc, KeyboardInterrupt):
                raise interruption from exc
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

    def stream_chunks(
        self,
        documents: dict[str, str],
        resumes: dict[str, int],
        on_event: Callable[[object], None],
        *,
        reusable_hashes: set[str],
        deadline: float | None,
        residency_fd: int,
        cancelled: threading.Event | None = None,
    ) -> None:
        """worker の chunk 行を到着順に caller へ渡し、失敗時は子を回収する。"""
        if self.config is None:
            raise SearchError("NOT_READY", "document search tuning is not configured")
        request = self._request(
            "chunk_stream",
            {
                "documents": documents,
                "resume": resumes,
                "reusable_hashes": sorted(reusable_hashes),
                "config": asdict(self.config),
            },
        )
        try:
            process = subprocess.Popen(
                ["node", str(self.base / "worker.mjs")],
                cwd=self.base,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL,
                pass_fds=(residency_fd,),
                start_new_session=True,
                env={**os.environ, "NODE_LLAMA_CPP_SKIP_DOWNLOAD": "true"},
            )
        except OSError as exc:
            raise SearchError(
                "MODEL_FAILURE", "inference worker could not start"
            ) from exc
        assert process.stdin is not None and process.stdout is not None
        input_data = json.dumps(request, ensure_ascii=False).encode("utf-8")
        input_offset = 0
        output_buffer = b""
        done = False
        try:
            os.set_blocking(process.stdin.fileno(), False)
            while True:
                if self.check is not None:
                    self.check()
                if cancelled is not None and cancelled.is_set():
                    raise SearchError("CANCELLED", "document search was cancelled")
                remaining = None if deadline is None else deadline - time.monotonic()
                if remaining is not None and remaining <= 0:
                    raise SearchError(
                        "DEADLINE_EXCEEDED", "inference deadline exceeded"
                    )
                if input_offset == len(input_data) and not process.stdin.closed:
                    process.stdin.close()
                readers, writers, _ = select.select(
                    [process.stdout],
                    [process.stdin] if not process.stdin.closed else [],
                    [],
                    0.2 if remaining is None else min(0.2, remaining),
                )
                if writers:
                    try:
                        written = os.write(
                            process.stdin.fileno(), input_data[input_offset:]
                        )
                    except BlockingIOError:
                        written = 0
                    input_offset += written
                if readers:
                    fragment = os.read(process.stdout.fileno(), 65536)
                    if not fragment:
                        break
                    output_buffer += fragment
                    if len(output_buffer) > 2_000_000:
                        raise SearchError(
                            "MODEL_FAILURE", "inference worker output is too large"
                        )
                    while b"\n" in output_buffer:
                        line, output_buffer = output_buffer.split(b"\n", 1)
                        try:
                            event = json.loads(line)
                        except (ValueError, UnicodeError) as exc:
                            raise SearchError(
                                "MODEL_FAILURE", "inference event is invalid"
                            ) from exc
                        if isinstance(event, dict) and event.get("kind") == "done":
                            if done or set(event) != {"kind"}:
                                raise SearchError(
                                    "MODEL_FAILURE", "inference completion is invalid"
                                )
                            done = True
                        elif done:
                            raise SearchError(
                                "MODEL_FAILURE", "inference event after completion"
                            )
                        else:
                            on_event(event)
            if output_buffer or not done:
                raise SearchError(
                    "MODEL_FAILURE", "inference worker output is incomplete"
                )
            while process.poll() is None:
                if self.check is not None:
                    self.check()
                if cancelled is not None and cancelled.is_set():
                    raise SearchError("CANCELLED", "document search was cancelled")
                if deadline is not None and time.monotonic() >= deadline:
                    raise SearchError(
                        "DEADLINE_EXCEEDED", "inference deadline exceeded"
                    )
                time.sleep(0.05)
            if process.returncode != 0:
                raise SearchError("MODEL_FAILURE", "inference worker failed")
        except OSError as exc:
            failure = SearchError("MODEL_FAILURE", "inference worker I/O failed")
            if self.on_failure is not None:
                self.on_failure(failure)
            self._stop_process(process)
            raise failure from exc
        except BaseException as exc:
            interruption = (
                SearchError("CANCELLED", "document search was cancelled")
                if isinstance(exc, KeyboardInterrupt)
                else exc
            )
            if self.on_failure is not None:
                self.on_failure(interruption)
            self._stop_process(process)
            if isinstance(exc, KeyboardInterrupt):
                raise interruption from exc
            raise
        finally:
            for pipe in (process.stdin, process.stdout):
                if pipe is not None and not pipe.closed:
                    pipe.close()
