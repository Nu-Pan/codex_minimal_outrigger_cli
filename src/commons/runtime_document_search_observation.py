"""検索要求と同期の時計、進捗、即時保存する診断を管理する。"""

import math
import time
import uuid
from collections.abc import Callable
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path

from oracle.other.document_search import DocumentSearchConfig

from .runtime_logging import append_log_record

type SearchEventSink = Callable[[str, dict[str, object]], None]

# 返送と polling の余裕。性能保証ではなく、live 接続でも検証する暫定値。
MCP_RESPONSE_MARGIN_SECONDS = 10.0


def mcp_tool_timeout_seconds(config: DocumentSearchConfig) -> float:
    """内側の全体上限に、停止と返送の余裕を加える。"""
    # 起動時と保存設定の再検証で同じ外側期限の関係を使う。
    # CLI の Duration 符号化による小数丸めで、外側の余裕を削らない。
    return math.ceil(
        config.search_request_timeout_seconds
        + config.shutdown_grace_seconds
        + MCP_RESPONSE_MARGIN_SECONDS
    )


def inference_config(config: DocumentSearchConfig) -> dict[str, object]:
    """要求の時計だけの変更では、推論資材や保存結果を無効化しない。"""
    # 入力と実モデル検証の条件を変えない要求期限は identity から分離する。
    request_fields = {
        "resource_wait_timeout_seconds",
        "sync_no_progress_timeout_seconds",
        "post_sync_search_timeout_seconds",
        "search_request_timeout_seconds",
    }
    return {
        name: value
        for name, value in asdict(config).items()
        if name not in request_fields
    }


class SearchError(Exception):
    """検索失敗 code と、原文を含めない説明を保持する。"""

    def __init__(self, code: str, message: str) -> None:
        """公開する failure の分類を固定する。"""
        # MCP の失敗表現と診断記録で同じ code を使う。
        super().__init__(message)
        self.code = code


@dataclass(frozen=True)
class SearchLogContext:
    """起動管理側が供給する、呼出し元ログと Codex call の対応。"""

    path: Path
    command: str
    execution_id: str
    codex_call_id: str

    def event(self, kind: str, payload: dict[str, object]) -> None:
        """MCP stdout を使わず、呼出し元の既存ログへ即時追記する。"""
        # 相関情報は tool 入力から受け取らず、各記録へ同じ固定値を付ける。
        append_log_record(
            self.path,
            {
                **payload,
                "event": kind,
                "timestamp": datetime.now().isoformat(),
                "command": self.command,
                "execution_id": self.execution_id,
                "codex_call_id": self.codex_call_id,
            },
        )


@dataclass
class _SyncTiming:
    sync_id: str
    sequence: int
    started: float
    wait_at_start: float
    progress: dict[str, object]
    completed_steps: set[tuple[str, str]] = field(default_factory=set)
    last_progress_active: float = 0.0
    last_progress: dict[str, object] | None = None
    longest_no_progress: float = 0.0
    decision_at: float | None = None
    decision_times: dict[str, object] | None = None
    status: str = "started"
    failure: BaseException | None = None
    cleanup_failure: BaseException | None = None


def _failure_status(failure: BaseException) -> str:
    # 元の打切り理由は、終了処理の失敗が起きても保持する。
    if isinstance(failure, KeyboardInterrupt):
        return "cancelled"
    if isinstance(failure, SearchError):
        if failure.code == "CANCELLED":
            return "cancelled"
        if failure.code == "DEADLINE_EXCEEDED":
            return "deadline_exceeded"
    return "failed"


def _failure_fields(failure: BaseException | None) -> dict[str, object]:
    # 失敗の公開 code と診断理由を同じ終端へ残す。
    return {
        "failure_code": (
            failure.code
            if isinstance(failure, SearchError)
            else "CANCELLED"
            if isinstance(failure, KeyboardInterrupt)
            else "SYNC_FAILED"
            if failure is not None
            else None
        ),
        "failure_reason": str(failure) if failure is not None else None,
        "failure_type": type(failure).__name__ if failure is not None else None,
    }


class SearchObservation:
    """一つの要求内で、期限と同期の実測区間を対応付ける。"""

    def __init__(
        self,
        work_root: Path,
        scope_identity: str,
        sink: SearchEventSink | None,
        *,
        request: bool,
        started: float | None = None,
        request_id: str | int | None = None,
    ) -> None:
        """identity の確定や最初の待機より前に開始を保存する。"""
        # 受付側で作成すれば、queue の待機も要求全体の時間に含まれる。
        self.started = time.monotonic() if started is None else started
        self.request = request
        self.request_id = uuid.uuid4().hex if request else None
        self.sink = sink
        self.context: dict[str, object] = {
            "work_root": str(work_root),
            "scope_identity": scope_identity,
            "request_id": self.request_id,
            "mcp_request_id": request_id,
        }
        self.limits: dict[str, float] | None = None
        self.sync: _SyncTiming | None = None
        self.last_sync: _SyncTiming | None = None
        self.sync_ids: list[str] = []
        self._wait_depth = 0
        self._wait_started: float | None = None
        self._wait_seconds = 0.0
        self._post_sync_started: float | None = None
        self._decision_at: float | None = None
        self._decision_times: dict[str, object] | None = None
        self._failure: BaseException | None = None
        self._cleanup_failure: BaseException | None = None
        self._last_progress: dict[str, object] | None = None
        self._finished = False
        if request:
            self._event("document_search_request_started", index_identity=None)

    def _event(self, kind: str, **payload: object) -> None:
        # sink は保存だけを行い、console や MCP の stdout へ通知しない。
        if self.sink is not None:
            self.sink(kind, {**self.context, **payload})

    def configure(self, config: DocumentSearchConfig | None, *, bounded: bool) -> None:
        """検証済みの設定から、その要求に適用する期限を記録する。"""
        # doctor の索引同期には、検索用の四種類の期限を適用しない。
        if config is not None and bounded:
            self.limits = {
                "resource_wait": config.resource_wait_timeout_seconds,
                "sync_no_progress": config.sync_no_progress_timeout_seconds,
                "post_sync_search": config.post_sync_search_timeout_seconds,
                "search_request": config.search_request_timeout_seconds,
            }
        if self.request:
            self._event(
                "document_search_request_configured", deadline_limits=self.limits
            )

    def begin_sync(self, sync_id: str | None = None) -> dict[str, object]:
        """同期の最初の待機・処理より前に、独立した識別子で開始する。"""
        # 再同期も独立した区間とし、親の累積時計をリセットしない。
        now = time.monotonic()
        identifier = sync_id or f"dsi_{uuid.uuid4().hex}"
        self.sync_ids.append(identifier)
        progress: dict[str, object] = {
            "identity": None,
            "status": "started",
            "document_count": None,
            "checked_document_count": None,
            "changed_document_count": None,
            "persisted_chunks": None,
            "reused_embeddings": None,
            "document_states": None,
        }
        self.sync = _SyncTiming(
            identifier, len(self.sync_ids), now, self.resource_wait(now), progress
        )
        self._event(
            "document_search_sync_started",
            sync_id=identifier,
            sync_sequence=self.sync.sequence,
            index_identity=None,
        )
        return progress

    def resource_wait(self, now: float | None = None) -> float:
        """重なる取得待ちを一度だけ含めた累積秒数を返す。"""
        # 保有時間や停止・回収の時間は取得待ちへ加算しない。
        current = time.monotonic() if now is None else now
        return self._wait_seconds + (
            current - self._wait_started if self._wait_started is not None else 0.0
        )

    def start_wait(self) -> None:
        """取得待ちに入り、無進捗の時計をその値で止める。"""
        # 入れ子の待機でも同じ単調時計上の区間を重複加算しない。
        if self._wait_depth == 0:
            self._wait_started = time.monotonic()
        self._wait_depth += 1

    def end_wait(self) -> None:
        """取得・失敗・取消のいずれでも、待機前の時計を継続する。"""
        # 取得に至らなかった待機も累積に残す。
        self._wait_depth -= 1
        if self._wait_depth == 0:
            assert self._wait_started is not None
            self._wait_seconds += time.monotonic() - self._wait_started
            self._wait_started = None

    def measurements(self, now: float | None = None) -> dict[str, object]:
        """判定時点の四種類の実測値を、未開始と区別して返す。"""
        # 終了処理へ入った時計は、判定時の値で固定する。
        current = time.monotonic() if now is None else now
        sync = self.sync
        no_progress: float | None = None
        if sync is not None and (self.request or self.limits is not None):
            if sync.decision_times is not None:
                previous = sync.decision_times["sync_no_progress"]
                assert isinstance(previous, float)
                no_progress = previous
            else:
                active = (
                    current
                    - sync.started
                    - (self.resource_wait(current) - sync.wait_at_start)
                )
                no_progress = max(0.0, active - sync.last_progress_active)
            sync.longest_no_progress = max(sync.longest_no_progress, no_progress)
        return {
            "search_request": current - self.started,
            "resource_wait": self.resource_wait(current),
            "sync_no_progress": no_progress,
            "post_sync_search": (
                current - self._post_sync_started
                if self._post_sync_started is not None
                else None
            ),
        }

    def check(self, cancelled: bool = False) -> None:
        """適用中の全期限を同時判定し、回収より前に診断を保存する。"""
        # 終了処理中には新しい期限判定を行わない。
        if self._decision_at is not None:
            if self._failure is not None:
                raise self._failure
            return
        if cancelled:
            failure = SearchError("CANCELLED", "document search was cancelled")
            self.fail(failure)
            raise failure
        now = time.monotonic()
        measured = self.measurements(now)
        reached = []
        if self.limits is not None:
            for name, limit in self.limits.items():
                value = measured[name]
                if isinstance(value, (int, float)) and value >= limit:
                    reached.append(name)
        if reached:
            failure = SearchError(
                "DEADLINE_EXCEEDED",
                "document search deadline exceeded: " + ", ".join(reached),
            )
            timing = self.sync or self.last_sync
            self._event(
                "document_search_deadline_exceeded",
                deadline_kinds=reached,
                deadline_limits=self.limits,
                measured_seconds=measured,
                sync_id=self.sync.sync_id if self.sync is not None else None,
                index_identity=timing.progress["identity"] if timing else None,
                progress=timing.progress if timing else None,
                progress_sync_id=timing.sync_id if timing else None,
                longest_no_progress_seconds=self.sync.longest_no_progress
                if self.sync
                else None,
                last_progress=self.last_progress,
            )
            self.fail(failure, now=now)
            raise failure

    @property
    def last_progress(self) -> dict[str, object] | None:
        """最後の進捗を、その同期 ID とともに返す。"""
        # 進捗がなければ None とし、測定済みゼロとは区別する。
        return self._last_progress

    def progress(self, operation: str, target: str) -> None:
        """未処理の対象で必要な処理を完了した場合だけ時計を更新する。"""
        # heartbeat や同じ対象の再通知では延命しない。
        self.check()
        sync = self.sync
        assert sync is not None
        key = (operation, target)
        if key in sync.completed_steps:
            return
        sync.completed_steps.add(key)
        now = time.monotonic()
        self.measurements(now)
        sync.last_progress_active = (
            now - sync.started - (self.resource_wait(now) - sync.wait_at_start)
        )
        sync.last_progress = {
            "sync_id": sync.sync_id,
            "operation": operation,
            "target": target,
            "timestamp": datetime.now().isoformat(),
            "sync_elapsed_seconds": now - sync.started,
        }
        self._last_progress = sync.last_progress

    def fail(self, failure: BaseException, *, now: float | None = None) -> None:
        """元の打切り理由と判定時の測定値を、終了処理前に固定する。"""
        # worker 停止 callback からも同じ判定区間を確定できる。
        current = time.monotonic() if now is None else now
        if self._decision_at is None:
            self._decision_times = self.measurements(current)
            self._decision_at = current
            self._failure = failure
        elif failure is not self._failure:
            self._cleanup_failure = failure
        if self.sync is not None and self.sync.decision_at is None:
            self.sync.decision_times = self.measurements(current)
            self.sync.decision_at = current
            self.sync.failure = failure
            self.sync.status = _failure_status(failure)
        elif self.sync is not None and failure is not self.sync.failure:
            self.sync.cleanup_failure = failure

    def decide_sync(self, status: str) -> None:
        """同期処理の完了を、残る接続・lock の解放より前に確定する。"""
        # 無進捗の実測値へ終了処理の時間を含めない。
        sync = self.sync
        assert sync is not None
        self.check()
        sync.decision_times = self.measurements()
        sync.decision_at = time.monotonic()
        sync.status = status

    def finish_sync(self, status: str | None = None) -> None:
        """同期に属する終了処理を終えた時点で実績と終端を保存する。"""
        # 同期の成功から親検索の成功を推定しない。
        sync = self.sync
        if sync is None:
            return
        now = time.monotonic()
        if sync.decision_at is None:
            sync.decision_times = self.measurements(now)
            sync.decision_at = now
            sync.status = status or "failed"
        measured = sync.decision_times
        assert measured is not None
        progress = sync.progress
        status = "failed" if sync.cleanup_failure is not None else sync.status
        progress["status"] = status
        self._event(
            "document_search_sync_finished",
            sync_id=sync.sync_id,
            sync_sequence=sync.sequence,
            index_identity=progress["identity"],
            status=status,
            elapsed_seconds=now - sync.started,
            lock_wait_seconds=self.resource_wait(now) - sync.wait_at_start,
            cleanup_seconds=now - sync.decision_at,
            decision_seconds=measured,
            no_progress_seconds=measured["sync_no_progress"],
            longest_no_progress_seconds=sync.longest_no_progress
            if self.request
            else None,
            last_progress=sync.last_progress if self.request else None,
            document_count=progress["document_count"],
            checked_document_count=progress["checked_document_count"],
            changed_document_count=progress["changed_document_count"],
            persisted_chunk_count=progress["persisted_chunks"],
            reused_chunk_count=progress["reused_embeddings"],
            document_states=progress["document_states"],
            counts_complete=status in {"updated", "unchanged"},
            cleanup_failure=str(sync.cleanup_failure)
            if sync.cleanup_failure is not None
            else None,
            **_failure_fields(sync.failure or sync.cleanup_failure),
        )
        self.last_sync = sync
        self.sync = None

    def start_post_sync(self) -> None:
        """初回同期完了からの時計を、一度だけ起動する。"""
        # 再同期でも query・候補・照合の親時計をリセットしない。
        if self._post_sync_started is None:
            self._post_sync_started = time.monotonic()

    def decide_success(self) -> None:
        """正常返却の決定を、資源解放より前に記録する。"""
        # 到達済みの期限を成功へ置き換えない。
        self.check()
        self._decision_times = self.measurements()
        self._decision_at = time.monotonic()

    def finish_request(self, cleanup_failure: BaseException | None = None) -> None:
        """回収・資源解放後の総時間と、元の決定時点を区別して保存する。"""
        # 同じ終了処理を要求と同期で測る場合があり、単純加算しない。
        if not self.request or self._finished:
            return
        now = time.monotonic()
        cleanup_failure = cleanup_failure or self._cleanup_failure
        self._finished = True
        self._event(
            "document_search_request_finished",
            status=(
                "failed"
                if cleanup_failure is not None
                else _failure_status(self._failure)
                if self._failure is not None
                else "succeeded"
            ),
            elapsed_seconds=now - self.started,
            resource_wait_seconds=self.resource_wait(now),
            cleanup_seconds=(
                now - self._decision_at if self._decision_at is not None else None
            ),
            decision_seconds=self._decision_times,
            deadline_limits=self.limits,
            last_progress=self.last_progress,
            sync_ids=self.sync_ids,
            progress=self.last_sync.progress if self.last_sync else None,
            progress_sync_id=self.last_sync.sync_id if self.last_sync else None,
            index_identity=(
                self.last_sync.progress["identity"] if self.last_sync else None
            ),
            cleanup_failure=str(cleanup_failure)
            if cleanup_failure is not None
            else None,
            **_failure_fields(self._failure or cleanup_failure),
        )
