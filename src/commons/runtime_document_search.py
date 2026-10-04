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
from dataclasses import asdict, dataclass, replace
from heapq import nlargest
from importlib import resources
from pathlib import Path
from typing import Callable, Protocol

from oracle.other.cmoc_config import DocumentSearchConfig
from oracle.other.document_search import (
    EMBEDDING_QUERY_TEMPLATE,
    SEARCH_CANDIDATE_COUNT_MAX,
    SEARCH_CANDIDATE_COUNT_MIN,
)

from .runtime_config import _document_search_config, load_config
from .runtime_document_search_observation import (
    SearchError,
    SearchEventSink,
    SearchObservation,
    inference_config,
    mcp_tool_timeout_seconds,
)
from .runtime_document_search_types import (
    SEARCH_MATERIALS,
    SearchHit,
    SearchRange,
    SearchResult,
)
from .runtime_errors import CmocError
from .runtime_git import enumerate_oracle_and_realization_files, require_cmoc_ignored
from .runtime_logging import current_subcommand_logger
from .runtime_paths import cmoc_root, repo_root

_INDEX_FORMAT = 5
_CLASSIFICATION_CONTRACT = "oracle-file-inventory-v2"
_LOCK_POLL_SECONDS = 0.05


@dataclass(frozen=True)
class SourceDocument:
    """現在の許可本文とハッシュ。"""

    text: str
    sha256: str


@dataclass(frozen=True)
class SyncResult:
    """doctor と検索前同期に共通の機械的結果。"""

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
        deadline: float | None,
        residency_fd: int,
        cancelled: threading.Event | None = None,
    ) -> object:
        """単一操作を収束させて返す。"""

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
        """文書の chunk を計算順に渡す。"""


def _deadline_check(
    deadline: float | None, cancelled: threading.Event | None = None
) -> None:
    if cancelled is not None and cancelled.is_set():
        raise SearchError("CANCELLED", "document search was cancelled")
    if deadline is not None and time.monotonic() >= deadline:
        raise SearchError("DEADLINE_EXCEEDED", "document search deadline exceeded")


@contextmanager
def _file_lock(
    path: Path,
    deadline: float | None,
    cancelled: threading.Event | None = None,
    *,
    shared: bool = False,
    on_wait: Callable[[float], None] | None = None,
    observation: SearchObservation | None = None,
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
        wait_started: float | None = None
        try:
            while True:
                if observation is not None:
                    observation.check(cancelled is not None and cancelled.is_set())
                _deadline_check(deadline, cancelled)
                try:
                    mode = fcntl.LOCK_SH if shared else fcntl.LOCK_EX
                    fcntl.flock(fd, mode | fcntl.LOCK_NB)
                    break
                except BlockingIOError:
                    if wait_started is None:
                        wait_started = time.monotonic()
                        if observation is not None:
                            observation.start_wait()
                    wait = (
                        _LOCK_POLL_SECONDS
                        if deadline is None
                        else min(
                            _LOCK_POLL_SECONDS, max(0, deadline - time.monotonic())
                        )
                    )
                    time.sleep(wait)
                except OSError as exc:
                    raise SearchError(
                        "SYNC_FAILED", "document search lock failed"
                    ) from exc
        finally:
            if wait_started is not None and observation is not None:
                observation.end_wait()
            if wait_started is not None and on_wait is not None:
                on_wait(time.monotonic() - wait_started)
        try:
            yield fd
        except BaseException as exc:
            if observation is not None:
                observation.fail(exc)
            raise
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
                current.mkdir(exist_ok=True)
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
    *,
    deadline: float | None = None,
    cancelled: threading.Event | None = None,
    check: Callable[[], None] | None = None,
) -> dict[str, SourceDocument]:
    """既存分類器を使い、oracle/doc の Markdown だけを開く。"""
    root = root.absolute()
    initial_root = _root_identity(root)
    if check is not None:
        check()
    if deadline is not None:
        _deadline_check(deadline, cancelled)
    try:
        oracle_files, _ = enumerate_oracle_and_realization_files(root)
    except Exception as exc:
        raise SearchError("ENUMERATION_FAILED", "document enumeration failed") from exc
    documents: dict[str, SourceDocument] = {}
    for candidate in oracle_files:
        if check is not None:
            check()
        if deadline is not None:
            _deadline_check(deadline, cancelled)
        relative = candidate.relative_to(root).as_posix()
        if not (relative.startswith("oracle/doc/") and relative.endswith(".md")):
            continue
        content = _secure_read(root, relative)
        try:
            text = content.decode("utf-8")
        except UnicodeError as exc:
            raise SearchError("READ_FAILED", "document is not UTF-8") from exc
        documents[relative] = SourceDocument(text, hashlib.sha256(content).hexdigest())
    if _root_identity(root) != initial_root:
        raise SearchError("ROOT_UNAVAILABLE", "work root changed during enumeration")
    if check is not None:
        check()
    if deadline is not None:
        _deadline_check(deadline, cancelled)
    return documents


def search_identity(
    root: Path, config: DocumentSearchConfig, *, index_format: int | None = None
) -> str:
    """worktree 実体、分類と推論条件を索引 identity に含める。"""
    device, inode = _root_identity(root)
    worker_files = resources.files("commons.document_search_worker")
    payload = {
        "root": str(root.resolve()),
        "device": device,
        "inode": inode,
        "classification": _CLASSIFICATION_CONTRACT,
        "materials": asdict(SEARCH_MATERIALS),
        "worker_sha256": hashlib.sha256(
            worker_files.joinpath("worker.mjs").read_bytes()
        ).hexdigest(),
        "lock_sha256": hashlib.sha256(
            worker_files.joinpath("package-lock.json").read_bytes()
        ).hexdigest(),
        "query_template": EMBEDDING_QUERY_TEMPLATE,
        "config": inference_config(config),
        "format": _INDEX_FORMAT if index_format is None else index_format,
    }
    return hashlib.sha256(
        json.dumps(payload, sort_keys=True, ensure_ascii=False).encode("utf-8")
    ).hexdigest()


def _vector_blob(value: object) -> bytes:
    """embedding の次元、有限性、非ゼロ性を保存前に検査する。"""
    dimensions = SEARCH_MATERIALS.embedding_dimensions
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
    """破損した保存済み embedding を cosine 計算へ渡さない。"""
    dimensions = SEARCH_MATERIALS.embedding_dimensions
    if not isinstance(value, bytes) or len(value) != 4 * dimensions:
        raise SearchError("SYNC_FAILED", "cached embedding is invalid")
    numbers = struct.unpack("<" + "f" * dimensions, value)
    if not all(math.isfinite(number) for number in numbers) or not any(
        number != 0 for number in numbers
    ):
        raise SearchError("SYNC_FAILED", "cached embedding is invalid")
    return value


def _worktree_identity(root: Path) -> str:
    # 同じ path を再作成した worktree も生成元と区別する。
    device, inode = _root_identity(root)
    return hashlib.sha256(f"{root.resolve()}:{device}:{inode}".encode()).hexdigest()


def _embedding_identity(config: DocumentSearchConfig) -> str:
    # 分割・索引形式・query・期限は文書入力片の推論条件ではない。
    materials = asdict(SEARCH_MATERIALS)
    materials.pop("sqlite_vec_version")
    payload = {
        "materials": materials,
        # 文書入力の整形や pooling を変える場合はこの契約も更新する。
        "input_contract": "raw-document-text-last-v1",
        "context_tokens": config.embedding_context_tokens,
        "batch_tokens": config.batch_tokens,
        "threads": config.threads,
    }
    return hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()


class _EmbeddingCache:
    """repository の互換な入力片と生成元を、索引の寿命から分離して保持する。"""

    def __init__(self, path: Path) -> None:
        # caller の cache lock 内だけで開き、保存を入力片ごとに確定する。
        _safe_directory(path.parent)
        if path.is_symlink() or (path.exists() and not path.is_file()):
            raise SearchError("SYNC_FAILED", "embedding cache is not regular")
        self.connection = sqlite3.connect(path, timeout=0)
        try:
            self.connection.execute(
                "create table if not exists embeddings("
                "excerpt_sha256 text primary key, embedding blob not null, "
                "producer_worktree text not null)"
            )
            self.connection.commit()
        except BaseException:
            self.connection.close()
            raise

    def close(self) -> None:
        # 索引 connection とは独立に lock の解放前に閉じる。
        self.connection.close()

    def get(self, digest: str) -> tuple[bytes, str] | None:
        # 不正な保存結果は公開・再利用せず、不足分として再生成する。
        row = self.connection.execute(
            "select embedding, producer_worktree from embeddings where excerpt_sha256 = ?",
            (digest,),
        ).fetchone()
        if row is None:
            return None
        try:
            vector = _checked_cached_vector(row[0])
            if not isinstance(row[1], str) or len(row[1]) != 64:
                raise SearchError("SYNC_FAILED", "embedding producer is invalid")
        except SearchError:
            with self.connection:
                self.connection.execute(
                    "delete from embeddings where excerpt_sha256 = ?", (digest,)
                )
            return None
        return vector, row[1]

    def save(self, digest: str, vector: bytes, producer: str) -> bool:
        # 先行処理の生成元は後続 worktree での保存・再利用によって置き換えない。
        with self.connection:
            saved = self.connection.execute(
                "insert or ignore into embeddings values(?, ?, ?)",
                (digest, vector, producer),
            )
        return saved.rowcount == 1

    def hashes(self, check: Callable[[], None]) -> set[str]:
        # ロック取得後の保存結果を確認し、待機前の不足判定を使わない。
        hashes = set()
        for (digest,) in self.connection.execute(
            "select excerpt_sha256 from embeddings"
        ):
            check()
            if self.get(digest) is not None:
                hashes.add(digest)
        return hashes

    def import_legacy_index(
        self, index: Path, producer: str, check: Callable[[], None]
    ) -> None:
        # 旧版の互換 identity が示す保存結果だけを読み、元の索引を同期しない。
        if not index.exists() and not index.is_symlink():
            return
        _safe_directory(index.parent)
        if index.is_symlink() or not index.is_file():
            raise SearchError("SYNC_FAILED", "reuse source index is not regular")
        connection = sqlite3.connect(index.as_uri() + "?mode=ro", uri=True, timeout=0)
        try:
            for digest, embedding in connection.execute(
                "select excerpt_sha256, embedding from embedding_cache"
            ):
                check()
                try:
                    vector = _checked_cached_vector(embedding)
                except SearchError:
                    continue
                self.save(digest, vector, producer)
        finally:
            connection.close()


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
        if version.removeprefix("v") != SEARCH_MATERIALS.sqlite_vec_version:
            raise SearchError("MODEL_IDENTITY_MISMATCH", "sqlite-vec version mismatch")
        connection.execute("pragma foreign_keys = on")
        connection.executescript(
            """
            create table if not exists documents(
                path text primary key, sha256 text not null,
                complete integer not null check(complete in (0, 1))
            );
            create table if not exists chunks(
                id integer primary key,
                path text not null references documents(path) on delete cascade,
                ordinal integer not null,
                start_offset integer not null,
                end_offset integer not null,
                start_line integer not null,
                end_line integer not null,
                excerpt text not null,
                excerpt_sha256 text not null,
                embedding blob not null,
                producer_worktree text not null,
                unique(path, ordinal)
            );
            create table if not exists query_cache(
                query text primary key, embedding blob not null
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
    deadline: float | None,
    cancelled: threading.Event | None,
    *,
    check: Callable[[], None] | None = None,
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
        if check is not None:
            check()
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
        config: DocumentSearchConfig | None,
        *,
        worker: InferenceWorker | None = None,
        installation_root: Path | None = None,
        use_saved_config: bool = False,
        event_sink: SearchEventSink | None = None,
        tool_timeout_seconds: float | None = None,
    ) -> None:
        """work-root と検索設定を接続に結び付ける。"""
        self.root = root.absolute()
        try:
            self.config = _document_search_config(config)
        except (TypeError, ValueError) as exc:
            raise SearchError("NOT_READY", "document search tuning is invalid") from exc
        self.installation_root = installation_root or cmoc_root()
        self.worker = worker
        self.use_saved_config = use_saved_config
        self.tool_timeout_seconds = tool_timeout_seconds
        logger = current_subcommand_logger()
        self.event_sink = event_sink
        if event_sink is None and logger is not None:
            self.event_sink = lambda kind, payload: logger.event(kind, **payload)
        self._observation: SearchObservation | None = None
        self.cancelled: threading.Event | None = None
        self._lease_fd: int | None = None
        self._lease_lock = threading.Lock()
        self.sync_progress: dict[str, object] | None = None

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

    def _check(self, deadline: float | None) -> None:
        if self._observation is not None:
            self._observation.check(
                self.cancelled is not None and self.cancelled.is_set()
            )
        _deadline_check(deadline, self.cancelled)

    def _refresh_saved_config(self) -> None:
        """要求時の保存済み設定を検証し、変更時は旧索引と worker を離す。"""
        if not self.use_saved_config:
            return
        try:
            current = load_config(self.root).document_search
        except CmocError as exc:
            self.close()
            raise SearchError(
                "NOT_READY",
                f"{exc.summary}\n{exc.detail}\n{' '.join(exc.next_actions)}",
            ) from exc
        if (
            self.tool_timeout_seconds is not None
            and current is not None
            and mcp_tool_timeout_seconds(current) > self.tool_timeout_seconds
        ):
            raise SearchError(
                "NOT_READY",
                "increased document search request or shutdown timeout requires a new Codex call; "
                "restart the command to refresh the MCP tool timeout",
            )
        if current != self.config:
            self.close()
            from .runtime_document_search_worker import NodeSearchWorker

            if isinstance(self.worker, NodeSearchWorker):
                self.worker = None
            self.config = current

    def _check_sources_current(
        self, documents: Mapping[str, SourceDocument], deadline: float | None
    ) -> None:
        """結果を返す直前に、同期後の保存済み本文を照合する。"""
        self._check(deadline)
        if (
            scan_documents(
                self.root,
                deadline=deadline,
                cancelled=self.cancelled,
                check=lambda: self._check(deadline),
            )
            != documents
        ):
            raise SearchError("SOURCE_CHANGED", "documents changed during search")

    def _paths(self) -> tuple[str, Path, Path, Path]:
        if self.config is None:
            raise SearchError("NOT_READY", "document search tuning is not configured")
        identity = search_identity(self.root, self.config)
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
        deadline: float | None,
    ) -> object:
        from .runtime_document_search_worker import NodeSearchWorker

        self._check(deadline)
        if self.worker is None:
            self.worker = NodeSearchWorker(
                self.installation_root,
                self.config,
                check=lambda: self._check(None),
                on_failure=self._inference_failure,
            )
        if isinstance(self.worker, NodeSearchWorker):
            self.worker.check = lambda: self._check(None)
            self.worker.on_failure = self._inference_failure
        with _file_lock(
            residency,
            deadline,
            self.cancelled,
            observation=self._observation,
        ) as residency_fd:
            try:
                if self._observation is not None and operation == "embed_query":
                    self._observation.query_inference_calls += 1
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

    def _stream_inference(
        self,
        documents: dict[str, str],
        resumes: dict[str, int],
        reusable_hashes: set[str],
        residency: Path,
        deadline: float | None,
        on_event: Callable[[object], None],
    ) -> None:
        """chunk の到着時に Python の検証・保存 callback を実行する。"""
        from .runtime_document_search_worker import NodeSearchWorker

        self._check(deadline)
        if self.worker is None:
            self.worker = NodeSearchWorker(
                self.installation_root,
                self.config,
                check=lambda: self._check(None),
                on_failure=self._inference_failure,
            )
        if isinstance(self.worker, NodeSearchWorker):
            self.worker.check = lambda: self._check(None)
            self.worker.on_failure = self._inference_failure
        assert self.config is not None
        with _file_lock(
            residency,
            deadline,
            self.cancelled,
            observation=self._observation,
        ) as residency_fd:
            self.worker.stream_chunks(
                documents,
                resumes,
                on_event,
                reusable_hashes=reusable_hashes,
                deadline=deadline,
                residency_fd=residency_fd,
                cancelled=self.cancelled,
            )

    def _inference_failure(self, failure: BaseException) -> None:
        # worker の停止・回収より前に、打切り時点を固定する。
        if self._observation is not None:
            self._observation.fail(failure)

    def _sync_locked(
        self,
        connection: sqlite3.Connection,
        cache: _EmbeddingCache,
        documents: Mapping[str, SourceDocument],
        residency: Path,
        deadline: float | None,
        identity: str,
        started: float,
        index_created: bool,
    ) -> SyncResult:
        """有効な chunk を個別確定し、完了文書だけを検索に使える状態にする。"""
        stored = {
            path: (sha, bool(complete))
            for path, sha, complete in connection.execute(
                "select path, sha256, complete from documents"
            )
        }
        deleted_paths = set(stored) - set(documents)
        changed_paths = {
            path
            for path, source in documents.items()
            if path not in stored or stored[path][0] != source.sha256
        }
        pending_paths = {
            path
            for path, (_, complete) in stored.items()
            if path in documents and path not in changed_paths and not complete
        }
        blanked = sum(1 for path in changed_paths if not documents[path].text.strip())
        fresh = {
            path: documents[path].text
            for path in sorted(changed_paths | pending_paths)
            if documents[path].text.strip()
        }
        assert self.sync_progress is not None
        self.sync_progress.update(
            identity=identity,
            document_count=len(documents),
            checked_document_count=0,
            changed_document_count=len(deleted_paths | changed_paths | pending_paths),
            persisted_chunks=0,
            reused_embeddings=0,
            generated_embeddings=0,
            persisted_embeddings=0,
            reused_same_worktree=0,
            reused_other_worktree=0,
            document_states={path: "unprocessed" for path in documents},
        )
        producer = _worktree_identity(self.root)

        def increment(field: str, count: int = 1) -> None:
            assert self.sync_progress is not None
            before = self.sync_progress[field]
            assert isinstance(before, int)
            self.sync_progress[field] = before + count

        def reused(origin: str) -> None:
            increment("reused_embeddings")
            increment(
                "reused_same_worktree"
                if origin == producer
                else "reused_other_worktree"
            )

        def checked_document(path: str) -> None:
            # 必要な分割まで確認済みの文書を、embedding 完了とは別に数える。
            assert self.sync_progress is not None
            states = self.sync_progress["document_states"]
            assert isinstance(states, dict)
            if states[path] == "checked":
                return
            states[path] = "checked"
            count = self.sync_progress["checked_document_count"]
            assert isinstance(count, int)
            self.sync_progress["checked_document_count"] = count + 1
            assert self._observation is not None
            self._observation.progress("document_checked", path)

        # 出現位置だけを外し、repository の cache は保持する。
        with connection:
            for path in deleted_paths | changed_paths:
                connection.execute("delete from documents where path = ?", (path,))
            for path in changed_paths:
                source = documents[path]
                connection.execute(
                    "insert into documents(path, sha256, complete) values(?, ?, ?)",
                    (path, source.sha256, int(not source.text.strip())),
                )

        resumes: dict[str, int] = {}
        repaired_paths: set[str] = set()
        for path in sorted(documents):
            self._check(deadline)
            states = self.sync_progress["document_states"]
            assert isinstance(states, dict)
            states[path] = "processing"
            source = documents[path]
            rows = connection.execute(
                "select ordinal, start_offset, end_offset, start_line, end_line, "
                "excerpt, excerpt_sha256, embedding, producer_worktree "
                "from chunks where path = ? order by ordinal",
                (path,),
            ).fetchall()
            valid = True
            for ordinal, row in enumerate(rows):
                self._check(deadline)
                (
                    saved_ordinal,
                    start,
                    end,
                    start_line,
                    end_line,
                    excerpt,
                    excerpt_sha,
                    embedding,
                    origin,
                ) = row
                if (
                    saved_ordinal != ordinal
                    or type(start) is not int
                    or type(end) is not int
                    or not 0 <= start < end <= len(source.text)
                    or start_line != source.text.count("\n", 0, start) + 1
                    or end_line != source.text.count("\n", 0, end - 1) + 1
                    or excerpt != source.text[start:end]
                    or not excerpt.strip()
                    or excerpt_sha
                    != hashlib.sha256(excerpt.encode("utf-8")).hexdigest()
                    or not isinstance(origin, str)
                    or len(origin) != 64
                ):
                    valid = False
                    break
                try:
                    _checked_cached_vector(embedding)
                except SearchError:
                    valid = False
                    break
                assert self._observation is not None
                self._observation.progress("cached_chunk_checked", f"{path}:{ordinal}")
            if (
                path in stored
                and stored[path][1]
                and (
                    (source.text.strip() and not rows)
                    or (not source.text.strip() and rows)
                )
            ):
                valid = False
            if not valid:
                with connection:
                    connection.execute("delete from chunks where path = ?", (path,))
                    connection.execute(
                        "update documents set complete = ? where path = ?",
                        (int(not source.text.strip()), path),
                    )
                rows = []
                repaired_paths.add(path)
                self.sync_progress["changed_document_count"] = len(
                    deleted_paths | changed_paths | pending_paths | repaired_paths
                )
                if source.text.strip():
                    fresh[path] = source.text
            if path in pending_paths and not source.text.strip():
                with connection:
                    connection.execute(
                        "update documents set complete = 1 where path = ?", (path,)
                    )
            for row in rows:
                reused(row[-1])
                cache.save(row[-3], row[-2], row[-1])
            if path in fresh:
                resumes[path] = len(rows)
            else:
                checked_document(path)
            if rows:
                assert self._observation is not None
                self._observation.progress("embedding_reused", path)
        reusable_hashes = (
            cache.hashes(lambda: self._check(deadline)) if fresh else set()
        )
        next_ordinal = dict(resumes)
        completed: set[str] = set()

        def current_source(path: str) -> SourceDocument:
            """確定直前に権限分類と本文が元の入力に一致するか確認する。"""
            self._check(deadline)
            current = scan_documents(
                self.root,
                deadline=deadline,
                cancelled=self.cancelled,
                check=lambda: self._check(deadline),
            ).get(path)
            if current != documents[path]:
                raise SearchError(
                    "SOURCE_CHANGED", "documents changed during synchronization"
                )
            return documents[path]

        def on_event(event: object) -> None:
            """worker 出力を検証し、各 chunk または文書完了を個別確定する。"""
            # 届いた生成実績は、直後の期限・編集競合・保存失敗でも残す。
            if isinstance(event, dict) and event.get("kind") == "chunk":
                increment("generated_embeddings")
            self._check(deadline)
            if not isinstance(event, dict):
                raise SearchError("MODEL_FAILURE", "inference event is invalid")
            kind = event.get("kind")
            path = event.get("path")
            if not isinstance(path, str) or path not in fresh or path in completed:
                raise SearchError("MODEL_FAILURE", "inference path is invalid")
            if kind == "document_prepared":
                if type(event.get("chunk_count")) is not int or event[
                    "chunk_count"
                ] < max(1, resumes[path]):
                    raise SearchError("MODEL_FAILURE", "document partition is invalid")
                current_source(path)
                checked_document(path)
                return
            if kind == "document_complete":
                if (
                    type(event.get("chunk_count")) is not int
                    or event["chunk_count"] != next_ordinal[path]
                    or next_ordinal[path] == 0
                ):
                    raise SearchError("MODEL_FAILURE", "document chunks are incomplete")
                current_source(path)
                with connection:
                    connection.execute(
                        "update documents set complete = 1 where path = ?", (path,)
                    )
                completed.add(path)
                checked_document(path)
                return
            if (
                kind not in ("chunk", "reuse")
                or event.get("ordinal") != next_ordinal[path]
            ):
                raise SearchError("MODEL_FAILURE", "inference chunk order is invalid")
            source = current_source(path)
            start, end = event.get("start"), event.get("end")
            if (
                type(start) is not int
                or type(end) is not int
                or not 0 <= start < end <= len(source.text)
            ):
                raise SearchError("MODEL_FAILURE", "document chunk offsets are invalid")
            excerpt = source.text[start:end]
            if not excerpt.strip():
                raise SearchError("MODEL_FAILURE", "document chunk is blank")
            excerpt_sha = hashlib.sha256(excerpt.encode("utf-8")).hexdigest()
            if kind == "reuse":
                cached = cache.get(excerpt_sha)
                if cached is None:
                    raise SearchError(
                        "MODEL_FAILURE", "reused embedding is unavailable"
                    )
                vector, origin = cached
            else:
                vector = _vector_blob(event.get("embedding"))
                origin = producer
                if cache.save(excerpt_sha, vector, origin):
                    increment("persisted_embeddings")
            with connection:
                connection.execute(
                    "insert into chunks(path, ordinal, start_offset, end_offset, "
                    "start_line, end_line, excerpt, excerpt_sha256, embedding, producer_worktree) "
                    "values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (
                        path,
                        next_ordinal[path],
                        start,
                        end,
                        source.text.count("\n", 0, start) + 1,
                        source.text.count("\n", 0, end - 1) + 1,
                        excerpt,
                        excerpt_sha,
                        vector,
                        origin,
                    ),
                )
            next_ordinal[path] += 1
            assert self.sync_progress is not None
            if kind == "chunk":
                increment("persisted_chunks")
            else:
                reused(origin)
            assert self._observation is not None
            self._observation.progress(
                "embedding_saved" if kind == "chunk" else "embedding_reused",
                f"{path}:{next_ordinal[path] - 1}",
            )

        if fresh:
            self._stream_inference(
                fresh, resumes, reusable_hashes, residency, deadline, on_event
            )
        if (
            completed != set(fresh)
            or connection.execute(
                "select 1 from documents where complete = 0 limit 1"
            ).fetchone()
        ):
            raise SearchError("MODEL_FAILURE", "inference chunks are incomplete")
        final_reused = self.sync_progress["reused_embeddings"]
        assert isinstance(final_reused, int)
        count = connection.execute("select count(*) from chunks").fetchone()[0]
        return SyncResult(
            identity=identity,
            status="updated"
            if index_created
            or changed_paths
            or deleted_paths
            or pending_paths
            or repaired_paths
            else "unchanged",
            document_count=len(documents),
            chunk_count=count,
            added=len(changed_paths - set(stored)),
            changed=len(changed_paths & set(stored)),
            deleted=len(deleted_paths),
            blanked=blanked,
            reused_embeddings=final_reused,
            elapsed_seconds=time.monotonic() - started,
        )

    @contextmanager
    def _locked_index(
        self,
        *,
        synchronizing_only: bool = False,
    ) -> Iterator[
        tuple[
            sqlite3.Connection,
            dict[str, SourceDocument],
            SyncResult,
            Path,
            float | None,
        ]
    ]:
        """資材の切替を防いだまま索引・推論の全要求を完了する。"""
        from .runtime_document_search_setup import _material_lock
        from .runtime_document_search_worker import NodeSearchWorker

        assert self._observation is not None
        if self.sync_progress is None:
            self.sync_progress = self._observation.begin_sync()
        try:
            if self.worker is not None and not isinstance(
                self.worker, NodeSearchWorker
            ):
                with self._locked_index_inner(
                    synchronizing_only=synchronizing_only
                ) as state:
                    yield state
                return
            try:
                require_cmoc_ignored(self.installation_root)
            except Exception as exc:
                raise SearchError(
                    "NOT_READY",
                    "shared document search storage is not ignored; run cmoc doctor",
                ) from exc
            with _file_lock(
                _material_lock(self.installation_root),
                None,
                self.cancelled,
                shared=True,
                observation=self._observation,
            ):
                with self._locked_index_inner(
                    synchronizing_only=synchronizing_only
                ) as state:
                    yield state
        except BaseException as exc:
            self._observation.fail(exc)
            raise
        finally:
            if not synchronizing_only:
                self._observation.finish_sync()

    @contextmanager
    def _locked_index_inner(
        self,
        *,
        synchronizing_only: bool = False,
    ) -> Iterator[
        tuple[
            sqlite3.Connection,
            dict[str, SourceDocument],
            SyncResult,
            Path,
            float | None,
        ]
    ]:
        """索引 lock 内で現在本文を確認し、整合世代を同期する。"""
        assert self._observation is not None and self.sync_progress is not None
        started = time.monotonic()
        if self.config is None:
            raise SearchError("NOT_READY", "document search tuning is not configured")
        # 四種類の期限は observation が判定する。doctor は同じ経路を期限なしで使う。
        deadline = None
        self._check(deadline)
        identity, index, lock, residency = self._paths()
        self.sync_progress["identity"] = identity
        try:
            require_cmoc_ignored(self.root)
            repository = repo_root(self.root)
            if repository != self.root:
                require_cmoc_ignored(repository)
        except Exception as exc:
            raise SearchError(
                "SYNC_FAILED", "document search storage is not ignored"
            ) from exc
        cache_base = repository / ".cmoc/gu/document_search/cache"
        condition = _embedding_identity(self.config)
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
            try:
                verify_search_materials(self.installation_root, self.config)
            except SearchError as exc:
                raise SearchError(exc.code, f"{exc}; run cmoc doctor") from exc
        lease = index.parent.parent.parent / "leases" / f"{identity}.lock"
        with _file_lock(
            lease,
            deadline,
            self.cancelled,
            shared=True,
            observation=self._observation,
        ) as lease_fd:
            self._retain_lease(lease, lease_fd)
            with _file_lock(
                lock,
                deadline,
                self.cancelled,
                observation=self._observation,
            ):
                _safe_directory(index.parent)
                documents = scan_documents(
                    self.root,
                    deadline=deadline,
                    cancelled=self.cancelled,
                    check=lambda: self._check(deadline),
                )
                self.sync_progress["document_count"] = len(documents)
                self._check(deadline)
                index_created = not index.exists()
                connection: sqlite3.Connection | None = None
                try:
                    # 同じ互換条件の不足判定・生成・保存を repository 内で直列化する。
                    # 元の索引 lock は取らず、旧版 DB の確定済み snapshot だけを読む。
                    with _file_lock(
                        cache_base / f"{condition}.lock",
                        deadline,
                        self.cancelled,
                        observation=self._observation,
                    ):
                        cache = _EmbeddingCache(cache_base / f"{condition}.sqlite3")
                        try:
                            for source_root in dict.fromkeys((self.root, repository)):
                                legacy_identity = search_identity(
                                    source_root, self.config, index_format=4
                                )
                                cache.import_legacy_index(
                                    source_root
                                    / ".cmoc/gu/document_search/indexes"
                                    / legacy_identity
                                    / "index.sqlite3",
                                    _worktree_identity(source_root),
                                    lambda: self._check(deadline),
                                )
                            _reclaim_unused_indexes(
                                index.parent.parent.parent,
                                identity,
                                deadline,
                                self.cancelled,
                                check=lambda: self._check(deadline),
                            )
                            connection = _open_database(index)
                            result = self._sync_locked(
                                connection,
                                cache,
                                documents,
                                residency,
                                deadline,
                                identity,
                                started,
                                index_created,
                            )
                        finally:
                            cache.close()
                    self._check(deadline)
                    self._check_sources_current(documents, deadline)
                    self.sync_progress["status"] = result.status
                    if not synchronizing_only:
                        self._observation.finish_sync(result.status)
                        self._observation.start_post_sync()
                    yield connection, documents, result, residency, deadline
                except (OSError, sqlite3.Error) as exc:
                    failure = SearchError(
                        "SYNC_FAILED", "document search synchronization failed"
                    )
                    self._observation.fail(failure)
                    raise failure from exc
                except BaseException as exc:
                    self._observation.fail(exc)
                    raise
                finally:
                    if connection is not None:
                        connection.close()

    def synchronize(
        self, *, unbounded: bool = False, sync_id: str | None = None
    ) -> SyncResult:
        """query 推論を行わず、通常検索と同じ現在本文の同期を実行する。"""
        observation = SearchObservation(self.root, self.event_sink, request=False)
        self._observation = observation
        self.sync_progress = None
        result: SyncResult | None = None
        try:
            self._refresh_saved_config()
            observation.configure(self.config, bounded=not unbounded)
            self.sync_progress = observation.begin_sync(sync_id)
            with self._locked_index(synchronizing_only=True) as (
                _,
                _,
                result,
                _,
                deadline,
            ):
                self._check(deadline)
                observation.decide_sync(result.status)
        except BaseException as exc:
            observation.fail(exc)
            raise
        finally:
            try:
                if unbounded:
                    self.close()
            except BaseException as exc:
                observation.fail(exc)
                raise
            finally:
                observation.finish_sync(result.status if result is not None else None)
                self._observation = None
        assert result is not None and observation.last_sync is not None
        return replace(
            result, elapsed_seconds=time.monotonic() - observation.last_sync.started
        )

    def begin_request(
        self, *, started: float | None = None, request_id: str | int | None = None
    ) -> SearchObservation:
        """MCP の受付時に、queue の待機より前の開始記録を作る。"""
        # 各受付に独立した時計を持たせ、並行要求の識別を保つ。
        return SearchObservation(
            self.root,
            self.event_sink,
            request=True,
            started=started,
            request_id=request_id,
        )

    def search(
        self,
        query: str,
        limit: int | None = None,
        *,
        observation: SearchObservation | None = None,
    ) -> SearchResult:
        """現在本文を同期し、候補位置と cosine 類似度をファイルごとに集約する。"""
        # MCP と直接呼出しで同じ候補数の境界を維持する。
        if not isinstance(query, str) or not query.strip():
            raise ValueError("query must be non-blank")
        if limit is not None and (
            type(limit) is not int
            or not SEARCH_CANDIDATE_COUNT_MIN <= limit <= SEARCH_CANDIDATE_COUNT_MAX
        ):
            raise ValueError(
                f"limit must be an integer from {SEARCH_CANDIDATE_COUNT_MIN} "
                f"to {SEARCH_CANDIDATE_COUNT_MAX}"
            )
        observation = observation or self.begin_request()
        self._observation = observation
        self.sync_progress = None
        try:
            self._refresh_saved_config()
            observation.configure(self.config, bounded=True)
            self._check(None)
            with self._locked_index() as (
                connection,
                documents,
                _,
                residency,
                deadline,
            ):
                found = self._search_locked(
                    query, limit, connection, documents, residency, deadline
                )
                observation.decide_success()
            return found
        except BaseException as exc:
            observation.fail(exc)
            raise
        finally:
            observation.finish_request()
            self._observation = None

    def _search_locked(
        self,
        query: str,
        limit: int | None,
        connection: sqlite3.Connection,
        documents: Mapping[str, SourceDocument],
        residency: Path,
        deadline: float | None,
    ) -> SearchResult:
        # 集約前の候補箇所数に設定と引数の上限を適用する。
        assert self.config is not None
        count = min(limit or self.config.candidate_count, self.config.candidate_count)
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
            assert self._observation is not None
            self._observation.query_generated_embeddings += 1
            connection.execute(
                "insert or replace into query_cache(query, embedding) values(?, ?)",
                (query, vector),
            )
            connection.commit()
        else:
            vector = _checked_cached_vector(cached[0])
        self._check(deadline)

        def scored_candidates() -> Iterator[tuple[str, int, int, float]]:
            # 全候補を検査し、不正な値が採用上限の外へ隠れることを防ぐ。
            try:
                for path, start, end, distance in connection.execute(
                    "select path, start_line, end_line, "
                    "vec_distance_cosine(embedding, ?) from chunks",
                    (vector,),
                ):
                    self._check(deadline)
                    if (
                        type(distance) not in (int, float)
                        or not math.isfinite(distance)
                        or not 0 <= distance <= 2
                    ):
                        raise SearchError(
                            "MODEL_FAILURE", "cosine similarity is invalid"
                        )
                    yield path, start, end, 1.0 - distance
            except sqlite3.Error as exc:
                raise SearchError(
                    "MODEL_FAILURE", "cosine similarity calculation failed"
                ) from exc

        candidates = nlargest(
            count, scored_candidates(), key=lambda candidate: candidate[3]
        )
        # 重複・重なりを位置順に統合し、採用候補の最大類似度を保持する。
        by_path: dict[str, list[SearchRange]] = {}
        for path, start, end, similarity in candidates:
            by_path.setdefault(path, []).append(
                {"start_line": start, "end_line": end, "max_similarity": similarity}
            )
        hits: list[SearchHit] = []
        for path, ranges in by_path.items():
            merged: list[SearchRange] = []
            for candidate in sorted(
                ranges, key=lambda item: (item["start_line"], item["end_line"])
            ):
                if merged and candidate["start_line"] <= merged[-1]["end_line"]:
                    merged[-1]["end_line"] = max(
                        merged[-1]["end_line"], candidate["end_line"]
                    )
                    merged[-1]["max_similarity"] = max(
                        merged[-1]["max_similarity"], candidate["max_similarity"]
                    )
                else:
                    merged.append(candidate)
            merged.sort(key=lambda item: item["max_similarity"], reverse=True)
            hits.append({"path": path, "ranges": merged})
        hits.sort(key=lambda hit: hit["ranges"][0]["max_similarity"], reverse=True)
        self._check_sources_current(documents, deadline)
        return {"status": "ok", "hits": hits}
