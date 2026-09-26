"""許可された oracle 文書の差分同期と検索を行う。"""

import fcntl
import hashlib
import importlib
import json
import math
import os
import shutil
import sqlite3
import stat
import struct
import threading
import time
from collections.abc import Iterator, Mapping
from contextlib import contextmanager
from dataclasses import asdict, dataclass
from importlib import resources
from pathlib import Path
from typing import Protocol

from oracle.acp_builder.basic import DocumentSearchScope
from oracle.other.document_search import (
    EMBEDDING_QUERY_TEMPLATE,
    INITIAL_SEARCH_MATERIALS,
    RAW_RANKING_API,
    RERANKER_INPUT_FORMAT,
    DocumentSearchConfig,
    SearchHit,
    SearchResult,
)

from .runtime_config import _document_search_config
from .runtime_document_search_scope import (
    scope_allows,
    validate_document_search_scope,
)
from .runtime_git import enumerate_oracle_and_realization_files, require_cmoc_ignored
from .runtime_paths import cmoc_root

_INDEX_FORMAT = 1
_CLASSIFICATION_CONTRACT = "oracle-file-inventory-v2"
_LOCK_POLL_SECONDS = 0.05


class SearchError(Exception):
    """検索失敗 code と、原文を含めない説明を保持する。"""

    def __init__(self, code: str, message: str) -> None:
        """公開する failure の分類を固定する。"""
        super().__init__(message)
        self.code = code


@dataclass(frozen=True)
class SourceDocument:
    """現在の許可本文とハッシュ。"""

    text: str
    sha256: str


@dataclass(frozen=True)
class SyncResult:
    """明示同期と検索前同期に共通の機械的結果。"""

    identity: str
    status: str
    document_count: int
    chunk_count: int
    added: int
    changed: int
    deleted: int
    blanked: int
    reused_embeddings: int
    elapsed_seconds: float


class InferenceWorker(Protocol):
    """Python が許可した本文だけを受け取る推論 worker。"""

    def run(
        self,
        operation: str,
        payload: dict[str, object],
        *,
        deadline: float,
        residency_fd: int,
        cancelled: threading.Event | None = None,
    ) -> object:
        """単一操作を収束させて返す。"""


def _deadline_check(deadline: float, cancelled: threading.Event | None = None) -> None:
    if cancelled is not None and cancelled.is_set():
        raise SearchError("CANCELLED", "document search was cancelled")
    if time.monotonic() >= deadline:
        raise SearchError("DEADLINE_EXCEEDED", "document search deadline exceeded")


@contextmanager
def _file_lock(
    path: Path,
    deadline: float,
    cancelled: threading.Event | None = None,
    *,
    shared: bool = False,
) -> Iterator[int]:
    """期限を含めて file lock を保持し、worker へ fd を継承可能にする。"""
    _safe_directory(path.parent)
    try:
        fd = os.open(path, os.O_CREAT | os.O_RDWR | os.O_NOFOLLOW, 0o600)
    except OSError as exc:
        raise SearchError("SYNC_FAILED", "document search lock is unavailable") from exc
    try:
        if not stat.S_ISREG(os.fstat(fd).st_mode):
            raise SearchError("SYNC_FAILED", "document search lock is not regular")
        while True:
            _deadline_check(deadline, cancelled)
            try:
                mode = fcntl.LOCK_SH if shared else fcntl.LOCK_EX
                fcntl.flock(fd, mode | fcntl.LOCK_NB)
                break
            except BlockingIOError:
                time.sleep(min(_LOCK_POLL_SECONDS, max(0, deadline - time.monotonic())))
            except OSError as exc:
                raise SearchError("SYNC_FAILED", "document search lock failed") from exc
        try:
            yield fd
        finally:
            fcntl.flock(fd, fcntl.LOCK_UN)
    finally:
        os.close(fd)


def _safe_directory(path: Path) -> None:
    """管理領域の symlink を通らず directory を準備する。"""
    absolute = path.absolute()
    current = Path(absolute.anchor)
    for part in absolute.parts[1:]:
        current /= part
        try:
            info = current.lstat()
        except FileNotFoundError:
            try:
                current.mkdir()
                info = current.lstat()
            except OSError as exc:
                raise SearchError(
                    "SYNC_FAILED", "document search storage is unavailable"
                ) from exc
        except OSError as exc:
            raise SearchError(
                "SYNC_FAILED", "document search storage is unavailable"
            ) from exc
        if stat.S_ISLNK(info.st_mode):
            raise SearchError("SYNC_FAILED", "document search storage is symlinked")
        if not stat.S_ISDIR(info.st_mode):
            raise SearchError(
                "SYNC_FAILED", "document search storage is not a directory"
            )


def _root_identity(root: Path) -> tuple[int, int]:
    try:
        info = root.lstat()
    except OSError as exc:
        raise SearchError("ROOT_UNAVAILABLE", "work root is unavailable") from exc
    if not stat.S_ISDIR(info.st_mode):
        raise SearchError("ROOT_UNAVAILABLE", "work root is not a directory")
    return info.st_dev, info.st_ino


def _secure_read(root: Path, relative: str) -> bytes:
    """各 component の symlink を拒否し、確認した regular file だけを読む。"""
    parts = relative.split("/")
    descriptors: list[int] = []
    try:
        directory_fd = os.open(root, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
        descriptors.append(directory_fd)
        for part in parts[:-1]:
            directory_fd = os.open(
                part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=directory_fd
            )
            descriptors.append(directory_fd)
        file_fd = os.open(parts[-1], os.O_RDONLY | os.O_NOFOLLOW, dir_fd=directory_fd)
        descriptors.append(file_fd)
        opened = os.fstat(file_fd)
        if not stat.S_ISREG(opened.st_mode):
            raise SearchError("READ_FAILED", "document is not a regular file")
        with os.fdopen(os.dup(file_fd), "rb") as stream:
            content = stream.read()
        for depth, opened_fd in enumerate(descriptors[:-1]):
            current_directory = root.joinpath(*parts[:depth])
            current_info = current_directory.lstat()
            opened_info = os.fstat(opened_fd)
            if not stat.S_ISDIR(current_info.st_mode) or (
                current_info.st_dev,
                current_info.st_ino,
            ) != (opened_info.st_dev, opened_info.st_ino):
                raise SearchError(
                    "SOURCE_CHANGED", "document parent changed during read"
                )
        current = (root / relative).lstat()
        finished = os.fstat(file_fd)
        if (
            (current.st_dev, current.st_ino, current.st_size, current.st_mtime_ns)
            != (
                opened.st_dev,
                opened.st_ino,
                opened.st_size,
                opened.st_mtime_ns,
            )
            or (finished.st_size, finished.st_mtime_ns)
            != (opened.st_size, opened.st_mtime_ns)
            or not stat.S_ISREG(current.st_mode)
        ):
            raise SearchError("SOURCE_CHANGED", "document changed during read")
        return content
    except SearchError:
        raise
    except OSError as exc:
        raise SearchError("READ_FAILED", "document could not be read safely") from exc
    finally:
        for descriptor in reversed(descriptors):
            os.close(descriptor)


def scan_documents(
    root: Path,
    scope: DocumentSearchScope,
    *,
    deadline: float | None = None,
    cancelled: threading.Event | None = None,
) -> dict[str, SourceDocument]:
    """既存分類器を使い、許可された oracle/doc Markdown だけを開く。"""
    scope = validate_document_search_scope(scope)
    root = root.absolute()
    initial_root = _root_identity(root)
    if deadline is not None:
        _deadline_check(deadline, cancelled)
    if not scope.allowed_files and not scope.allowed_subtrees:
        return {}
    try:
        oracle_files, _ = enumerate_oracle_and_realization_files(root)
    except Exception as exc:
        raise SearchError("ENUMERATION_FAILED", "document enumeration failed") from exc
    documents: dict[str, SourceDocument] = {}
    for candidate in oracle_files:
        if deadline is not None:
            _deadline_check(deadline, cancelled)
        relative = candidate.relative_to(root).as_posix()
        if not (
            relative.startswith("oracle/doc/")
            and relative.endswith(".md")
            and scope_allows(scope, relative)
        ):
            continue
        content = _secure_read(root, relative)
        try:
            text = content.decode("utf-8")
        except UnicodeError as exc:
            raise SearchError("READ_FAILED", "document is not UTF-8") from exc
        documents[relative] = SourceDocument(text, hashlib.sha256(content).hexdigest())
    if _root_identity(root) != initial_root:
        raise SearchError("ROOT_UNAVAILABLE", "work root changed during enumeration")
    if deadline is not None:
        _deadline_check(deadline, cancelled)
    return documents


def search_identity(
    root: Path, scope: DocumentSearchScope, config: DocumentSearchConfig
) -> str:
    """worktree 実体、閲覧範囲、分類と推論条件を索引 identity に含める。"""
    device, inode = _root_identity(root)
    worker_files = resources.files("commons.document_search_worker")
    payload = {
        "root": str(root.resolve()),
        "device": device,
        "inode": inode,
        "scope": asdict(validate_document_search_scope(scope)),
        "classification": _CLASSIFICATION_CONTRACT,
        "materials": asdict(INITIAL_SEARCH_MATERIALS),
        "worker_sha256": hashlib.sha256(
            worker_files.joinpath("worker.mjs").read_bytes()
        ).hexdigest(),
        "lock_sha256": hashlib.sha256(
            worker_files.joinpath("package-lock.json").read_bytes()
        ).hexdigest(),
        "query_template": EMBEDDING_QUERY_TEMPLATE,
        "reranker_input_format": RERANKER_INPUT_FORMAT,
        "raw_ranking_api": RAW_RANKING_API,
        "config": asdict(config),
        "format": _INDEX_FORMAT,
    }
    return hashlib.sha256(
        json.dumps(payload, sort_keys=True, ensure_ascii=False).encode("utf-8")
    ).hexdigest()


def _vector_blob(value: object) -> bytes:
    """embedding の次元、有限性、非ゼロ性を保存前に検査する。"""
    dimensions = INITIAL_SEARCH_MATERIALS.embedding_dimensions
    if not isinstance(value, list) or len(value) != dimensions:
        raise SearchError("MODEL_FAILURE", "embedding dimension is invalid")
    if any(
        type(number) not in (int, float) or not math.isfinite(number)
        for number in value
    ):
        raise SearchError("MODEL_FAILURE", "embedding contains non-finite values")
    if not any(number != 0 for number in value):
        raise SearchError("MODEL_FAILURE", "embedding is zero")
    try:
        packed = struct.pack("<" + "f" * dimensions, *value)
    except (OverflowError, struct.error) as exc:
        raise SearchError("MODEL_FAILURE", "embedding exceeds float32") from exc
    if not any(number != 0 for number in struct.unpack("<" + "f" * dimensions, packed)):
        raise SearchError("MODEL_FAILURE", "embedding rounds to zero")
    return packed


def _checked_cached_vector(value: object) -> bytes:
    """破損した query cache を cosine 計算へ渡さない。"""
    dimensions = INITIAL_SEARCH_MATERIALS.embedding_dimensions
    if not isinstance(value, bytes) or len(value) != 4 * dimensions:
        raise SearchError("SYNC_FAILED", "cached query embedding is invalid")
    numbers = struct.unpack("<" + "f" * dimensions, value)
    if not all(math.isfinite(number) for number in numbers) or not any(
        number != 0 for number in numbers
    ):
        raise SearchError("SYNC_FAILED", "cached query embedding is invalid")
    return value


def _open_database(path: Path) -> sqlite3.Connection:
    """sqlite-vec をロードし、整合する索引用 schema を用意する。"""
    if path.is_symlink() or (path.exists() and not path.is_file()):
        raise SearchError("SYNC_FAILED", "document search database is not regular")
    try:
        sqlite_vec = importlib.import_module("sqlite_vec")
    except ImportError as exc:
        raise SearchError("NOT_READY", "sqlite-vec is not installed") from exc
    connection: sqlite3.Connection | None = None
    try:
        connection = sqlite3.connect(path, timeout=0)
        connection.enable_load_extension(True)
        sqlite_vec.load(connection)
        connection.enable_load_extension(False)
        version = connection.execute("select vec_version()").fetchone()[0]
        if version.removeprefix("v") != INITIAL_SEARCH_MATERIALS.sqlite_vec_version:
            raise SearchError("MODEL_IDENTITY_MISMATCH", "sqlite-vec version mismatch")
        connection.execute("pragma foreign_keys = on")
        connection.executescript(
            """
            create table if not exists documents(
                path text primary key, sha256 text not null
            );
            create table if not exists chunks(
                id integer primary key,
                path text not null references documents(path) on delete cascade,
                start_line integer not null,
                end_line integer not null,
                excerpt text not null,
                excerpt_sha256 text not null,
                embedding blob not null
            );
            create table if not exists query_cache(
                query text primary key, embedding blob not null
            );
            create table if not exists score_cache(
                query text not null,
                excerpt_sha256 text not null,
                score real not null,
                primary key(query, excerpt_sha256)
            );
            """
        )
        return connection
    except SearchError:
        if connection is not None:
            connection.close()
        raise
    except (OSError, sqlite3.Error) as exc:
        if connection is not None:
            connection.close()
        raise SearchError("SYNC_FAILED", "document search database failed") from exc


def _reclaim_unused_indexes(
    base: Path,
    identity: str,
    deadline: float,
    cancelled: threading.Event | None,
) -> None:
    """要求中の接続が使わない旧索引だけを lease と調停して回収する。"""
    indexes = base / "indexes"
    _safe_directory(indexes)
    try:
        entries = list(indexes.iterdir())
    except OSError as exc:
        raise SearchError(
            "SYNC_FAILED", "document search indexes are unavailable"
        ) from exc
    for entry in entries:
        _deadline_check(deadline, cancelled)
        if (
            entry.name == identity
            or len(entry.name) != 64
            or any(character not in "0123456789abcdef" for character in entry.name)
        ):
            continue
        lease = base / "leases" / f"{entry.name}.lock"
        _safe_directory(lease.parent)
        try:
            fd = os.open(lease, os.O_CREAT | os.O_RDWR | os.O_NOFOLLOW, 0o600)
        except OSError as exc:
            raise SearchError(
                "SYNC_FAILED", "document search lease is unavailable"
            ) from exc
        try:
            if not stat.S_ISREG(os.fstat(fd).st_mode):
                raise SearchError("SYNC_FAILED", "document search lease is not regular")
            try:
                fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except BlockingIOError:
                continue
            try:
                if not entry.exists() and not entry.is_symlink():
                    continue
                if entry.is_symlink() or not entry.is_dir():
                    raise SearchError(
                        "SYNC_FAILED", "document search index is not a directory"
                    )
                shutil.rmtree(entry)
            finally:
                fcntl.flock(fd, fcntl.LOCK_UN)
        except OSError as exc:
            raise SearchError("SYNC_FAILED", "document search cleanup failed") from exc
        finally:
            os.close(fd)


class DocumentSearch:
    """固定した context の接続で同期と query を実行する。"""

    def __init__(
        self,
        root: Path,
        scope: DocumentSearchScope,
        config: DocumentSearchConfig | None,
        *,
        worker: InferenceWorker | None = None,
        installation_root: Path | None = None,
    ) -> None:
        """閲覧範囲を検証して固定する。"""
        self.root = root.absolute()
        try:
            self.scope = validate_document_search_scope(scope)
        except ValueError as exc:
            raise SearchError("INVALID_SCOPE", str(exc)) from exc
        try:
            self.config = _document_search_config(config)
        except (TypeError, ValueError) as exc:
            raise SearchError("NOT_READY", "document search tuning is invalid") from exc
        self.installation_root = installation_root or cmoc_root()
        self.worker = worker
        self.cancelled: threading.Event | None = None
        self.request_started: float | None = None
        self._lease_fd: int | None = None
        self._lease_lock = threading.Lock()

    def close(self) -> None:
        """接続が保持した索引 lease を解放する。"""
        with self._lease_lock:
            if self._lease_fd is not None:
                os.close(self._lease_fd)
                self._lease_fd = None

    def __del__(self) -> None:
        """明示 close を忘れた非 MCP caller でも lease を残さない。"""
        try:
            self.close()
        except Exception:
            pass

    def _retain_lease(self, path: Path, request_fd: int) -> None:
        """要求間の待機中も旧索引の回収を抑止する。"""
        with self._lease_lock:
            if self._lease_fd is not None:
                try:
                    current = os.fstat(self._lease_fd)
                    request = os.fstat(request_fd)
                except OSError as exc:
                    raise SearchError(
                        "SYNC_FAILED", "document search lease is unavailable"
                    ) from exc
                if (current.st_dev, current.st_ino) != (
                    request.st_dev,
                    request.st_ino,
                ):
                    raise SearchError("SYNC_FAILED", "document search lease changed")
                return
            try:
                fd = os.open(path, os.O_RDWR | os.O_NOFOLLOW)
            except OSError as exc:
                raise SearchError(
                    "SYNC_FAILED", "document search lease is unavailable"
                ) from exc
            try:
                current = os.fstat(fd)
                request = os.fstat(request_fd)
                if not stat.S_ISREG(current.st_mode) or (
                    current.st_dev,
                    current.st_ino,
                ) != (request.st_dev, request.st_ino):
                    raise SearchError("SYNC_FAILED", "document search lease changed")
                fcntl.flock(fd, fcntl.LOCK_SH | fcntl.LOCK_NB)
                self._lease_fd = fd
            except OSError as exc:
                os.close(fd)
                raise SearchError(
                    "SYNC_FAILED", "document search lease is unavailable"
                ) from exc
            except BaseException:
                os.close(fd)
                raise

    def _check(self, deadline: float) -> None:
        _deadline_check(deadline, self.cancelled)

    def _check_sources_current(
        self, documents: Mapping[str, SourceDocument], deadline: float
    ) -> None:
        """結果を返す直前に、同期後の保存済み本文を照合する。"""
        self._check(deadline)
        if (
            scan_documents(
                self.root, self.scope, deadline=deadline, cancelled=self.cancelled
            )
            != documents
        ):
            raise SearchError("SOURCE_CHANGED", "documents changed during search")

    def _paths(self) -> tuple[str, Path, Path, Path]:
        if self.config is None:
            raise SearchError("NOT_READY", "document search tuning is not configured")
        identity = search_identity(self.root, self.scope, self.config)
        base = self.root / ".cmoc/gu/document_search"
        index = base / "indexes" / identity / "index.sqlite3"
        lock = base / "locks" / f"{identity}.lock"
        residency = (
            self.installation_root / ".cmoc/gu/document_search/residency/model.lock"
        )
        return identity, index, lock, residency

    def _inference(
        self,
        operation: str,
        payload: dict[str, object],
        residency: Path,
        deadline: float,
    ) -> object:
        self._check(deadline)
        if self.worker is None:
            from .runtime_document_search_worker import NodeSearchWorker

            self.worker = NodeSearchWorker(self.installation_root, self.config)
        with _file_lock(residency, deadline, self.cancelled) as residency_fd:
            try:
                return self.worker.run(
                    operation,
                    payload,
                    deadline=deadline,
                    residency_fd=residency_fd,
                    cancelled=self.cancelled,
                )
            except SearchError:
                raise
            except Exception as exc:
                raise SearchError(
                    "MODEL_FAILURE", "document search inference failed"
                ) from exc

    def _sync_locked(
        self,
        connection: sqlite3.Connection,
        documents: Mapping[str, SourceDocument],
        residency: Path,
        deadline: float,
        identity: str,
        started: float,
    ) -> SyncResult:
        """全変更を一 transaction に確定し、途中世代を公開しない。"""
        assert self.config is not None
        stored = dict(connection.execute("select path, sha256 from documents"))
        stored_chunks = dict(
            connection.execute("select path, count(*) from chunks group by path")
        )
        deleted_paths = set(stored) - set(documents)
        changed_paths = {
            path
            for path, source in documents.items()
            if stored.get(path) != source.sha256
        }
        added = len(changed_paths - set(stored))
        changed = len(changed_paths & set(stored))
        blanked = sum(1 for path in changed_paths if not documents[path].text.strip())
        fresh = {
            path: documents[path].text
            for path in changed_paths
            if documents[path].text.strip()
        }
        generated: object = {}
        if fresh:
            generated = self._inference(
                "chunk_embed",
                {"documents": fresh, "config": asdict(self.config)},
                residency,
                deadline,
            )
        if not isinstance(generated, dict) or set(generated) != set(fresh):
            raise SearchError("MODEL_FAILURE", "inference chunks are incomplete")
        try:
            connection.execute("begin immediate")
            for path in deleted_paths | changed_paths:
                connection.execute("delete from documents where path = ?", (path,))
            for path in sorted(changed_paths):
                self._check(deadline)
                source = documents[path]
                connection.execute(
                    "insert into documents(path, sha256) values(?, ?)",
                    (path, source.sha256),
                )
                if path not in fresh:
                    continue
                chunks = generated[path]
                if not isinstance(chunks, list) or not chunks:
                    raise SearchError("MODEL_FAILURE", "document chunks are missing")
                for chunk in chunks:
                    if not isinstance(chunk, dict):
                        raise SearchError("MODEL_FAILURE", "document chunk is invalid")
                    start = chunk.get("start")
                    end = chunk.get("end")
                    if (
                        type(start) is not int
                        or type(end) is not int
                        or not 0 <= start < end <= len(source.text)
                    ):
                        raise SearchError(
                            "MODEL_FAILURE", "document chunk offsets are invalid"
                        )
                    excerpt = source.text[start:end]
                    if not excerpt.strip():
                        raise SearchError("MODEL_FAILURE", "document chunk is blank")
                    start_line = source.text.count("\n", 0, start) + 1
                    end_line = source.text.count("\n", 0, end - 1) + 1
                    excerpt_sha = hashlib.sha256(excerpt.encode("utf-8")).hexdigest()
                    connection.execute(
                        "insert into chunks(path, start_line, end_line, excerpt, "
                        "excerpt_sha256, embedding) values(?, ?, ?, ?, ?, ?)",
                        (
                            path,
                            start_line,
                            end_line,
                            excerpt,
                            excerpt_sha,
                            _vector_blob(chunk.get("embedding")),
                        ),
                    )
            connection.execute(
                "delete from score_cache where excerpt_sha256 not in "
                "(select excerpt_sha256 from chunks)"
            )
            connection.execute("commit")
        except BaseException:
            if connection.in_transaction:
                connection.execute("rollback")
            raise
        count = connection.execute("select count(*) from chunks").fetchone()[0]
        reusable = sum(
            chunk_count
            for path, chunk_count in stored_chunks.items()
            if path not in deleted_paths and path not in changed_paths
        )
        return SyncResult(
            identity=identity,
            status="updated" if changed_paths or deleted_paths else "unchanged",
            document_count=len(documents),
            chunk_count=count,
            added=added,
            changed=changed,
            deleted=len(deleted_paths),
            blanked=blanked,
            reused_embeddings=reusable,
            elapsed_seconds=time.monotonic() - started,
        )

    @contextmanager
    def _locked_index(
        self,
    ) -> Iterator[
        tuple[sqlite3.Connection, dict[str, SourceDocument], SyncResult, Path, float]
    ]:
        """索引 lock 内で現在本文を確認し、整合世代を同期する。"""
        started = self.request_started or time.monotonic()
        if self.config is None:
            raise SearchError("NOT_READY", "document search tuning is not configured")
        deadline = started + self.config.request_timeout_seconds
        self._check(deadline)
        identity, index, lock, residency = self._paths()
        try:
            require_cmoc_ignored(self.root)
        except Exception as exc:
            raise SearchError(
                "SYNC_FAILED", "document search storage is not ignored"
            ) from exc
        from .runtime_document_search_worker import (
            NodeSearchWorker,
            verify_search_materials,
        )

        if self.worker is None or isinstance(self.worker, NodeSearchWorker):
            try:
                require_cmoc_ignored(self.installation_root)
            except Exception as exc:
                raise SearchError(
                    "SYNC_FAILED", "shared document search storage is not ignored"
                ) from exc
            verify_search_materials(self.installation_root)
        lease = index.parent.parent.parent / "leases" / f"{identity}.lock"
        with _file_lock(lease, deadline, self.cancelled, shared=True) as lease_fd:
            self._retain_lease(lease, lease_fd)
            _reclaim_unused_indexes(
                index.parent.parent.parent, identity, deadline, self.cancelled
            )
            with _file_lock(lock, deadline, self.cancelled):
                _safe_directory(index.parent)
                documents = scan_documents(
                    self.root, self.scope, deadline=deadline, cancelled=self.cancelled
                )
                self._check(deadline)
                connection = _open_database(index)
                try:
                    result = self._sync_locked(
                        connection, documents, residency, deadline, identity, started
                    )
                    self._check(deadline)
                    yield connection, documents, result, residency, deadline
                except SearchError:
                    raise
                except (OSError, sqlite3.Error) as exc:
                    raise SearchError(
                        "SYNC_FAILED", "document search synchronization failed"
                    ) from exc
                finally:
                    connection.close()

    def synchronize(self) -> SyncResult:
        """query 推論を行わず、通常検索と同じ現在本文の同期を実行する。"""
        with self._locked_index() as (_, documents, result, _, deadline):
            self._check_sources_current(documents, deadline)
            return result

    def search(self, query: str, limit: int | None = None) -> SearchResult:
        """現在本文を同期し、cosine 候補を実モデルで再ランキングする。"""
        if not isinstance(query, str) or not query.strip():
            raise ValueError("query must be non-blank")
        if limit is not None and (type(limit) is not int or limit < 1):
            raise ValueError("limit must be a positive integer")
        with self._locked_index() as (connection, documents, _, residency, deadline):
            assert self.config is not None
            count = min(
                limit or self.config.candidate_count, self.config.candidate_count
            )
            if not connection.execute("select 1 from chunks limit 1").fetchone():
                self._check_sources_current(documents, deadline)
                return {"status": "ok", "hits": []}
            cached = connection.execute(
                "select embedding from query_cache where query = ?", (query,)
            ).fetchone()
            if cached is None:
                embedding = self._inference(
                    "embed_query",
                    {
                        "text": EMBEDDING_QUERY_TEMPLATE.format(query=query),
                        "config": asdict(self.config),
                    },
                    residency,
                    deadline,
                )
                vector = _vector_blob(embedding)
                connection.execute(
                    "insert or replace into query_cache(query, embedding) values(?, ?)",
                    (query, vector),
                )
                connection.commit()
            else:
                vector = _checked_cached_vector(cached[0])
            self._check(deadline)
            candidates = connection.execute(
                "select path, start_line, end_line, excerpt, excerpt_sha256 "
                "from chunks order by vec_distance_cosine(embedding, ?) limit ?",
                (vector, count),
            ).fetchall()
            missing = []
            scores: dict[str, float] = {}
            for _, _, _, excerpt, excerpt_sha in candidates:
                row = connection.execute(
                    "select score from score_cache where query = ? and excerpt_sha256 = ?",
                    (query, excerpt_sha),
                ).fetchone()
                if row is None:
                    missing.append((excerpt_sha, excerpt))
                else:
                    score = row[0]
                    if type(score) not in (int, float) or not math.isfinite(score):
                        raise SearchError(
                            "SYNC_FAILED", "cached reranking score is invalid"
                        )
                    scores[excerpt_sha] = score
            if missing:
                ranking = self._inference(
                    "rerank",
                    {
                        "query": query,
                        "documents": [text for _, text in missing],
                        "config": asdict(self.config),
                        "input_format": RERANKER_INPUT_FORMAT,
                    },
                    residency,
                    deadline,
                )
                if not isinstance(ranking, list) or len(ranking) != len(missing):
                    raise SearchError(
                        "MODEL_FAILURE", "reranking scores are incomplete"
                    )
                for (excerpt_sha, _), score in zip(missing, ranking, strict=True):
                    if type(score) not in (int, float) or not math.isfinite(score):
                        raise SearchError("MODEL_FAILURE", "reranking score is invalid")
                    scores[excerpt_sha] = score
                    connection.execute(
                        "insert or replace into score_cache(query, excerpt_sha256, score) "
                        "values(?, ?, ?)",
                        (query, excerpt_sha, score),
                    )
                connection.commit()
            hits: list[SearchHit] = [
                {"path": path, "start_line": start, "end_line": end, "excerpt": excerpt}
                for path, start, end, excerpt, excerpt_sha in sorted(
                    candidates, key=lambda row: scores[row[4]], reverse=True
                )
            ]
            self._check_sources_current(documents, deadline)
            return {"status": "ok", "hits": hits}
