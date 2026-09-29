"""回復条件が等しい Codex call の待機と probe を共有する。"""

import signal
import sys
import threading
import time
from collections.abc import Callable
from contextvars import ContextVar, Token
from dataclasses import dataclass, field
from types import FrameType
from typing import Literal

from .runtime_errors import CmocError
from .runtime_feedback_store import uuid7_prefixed
from .runtime_logging import SubcommandLogger
from .runtime_paths import console_timestamp

RecoveryReason = Literal["quota", "transient"]
CodexOutcome = Literal["succeeded", "quota", "transient", "failed"]
_CANCELLATION: ContextVar[threading.Event | None] = ContextVar(
    "codex_recovery_cancellation", default=None
)
_CONDITION = threading.Condition()


@dataclass
class _RecoveryGroup:
    recovery_id: str = field(default_factory=lambda: uuid7_prefixed("rcv_"))
    done: bool = False
    error: BaseException | None = None
    outcome: CodexOutcome = "failed"


_GROUPS: dict[tuple[object, ...], _RecoveryGroup] = {}


def install_recovery_interruption() -> Callable[[], None]:
    """中断可能 invocation の要求を worker にも伝え、既存 handler へ渡す。"""
    # 不可分な finalization の遅延 handler は、この handler を保存・復元する。
    cancellation = threading.Event()
    token: Token[threading.Event | None] = _CANCELLATION.set(cancellation)
    previous = signal.getsignal(signal.SIGINT)

    def interrupt(signum: int, frame: FrameType | None) -> None:
        # probe 成功と競合しても、以後の呼び出し開始を禁止する。
        cancellation.set()
        if callable(previous):
            previous(signum, frame)
        else:
            raise KeyboardInterrupt

    signal.signal(signal.SIGINT, interrupt)

    def restore() -> None:
        # サブコマンドの終了後へ cancellation を持ち越さない。
        signal.signal(signal.SIGINT, previous)
        _CANCELLATION.reset(token)

    return restore


def current_recovery_cancellation() -> threading.Event | None:
    """同じ invocation の worker へ継承される中断状態を返す。"""
    # ContextVar の値は copy_context 経由でも同じ Event を参照する。
    return _CANCELLATION.get()


def check_recovery_interruption() -> None:
    """中断受理後の probe・resume・新規 call を開始させない。"""
    # KeyboardInterrupt は workload 固有の commit/rollback 処理へ返す。
    cancellation = current_recovery_cancellation()
    if cancellation is not None and cancellation.is_set():
        raise KeyboardInterrupt


def _emit_progress(reason: RecoveryReason, message: str) -> None:
    # 個別 probe の詳細は console に列挙しない。
    label = "quota" if reason == "quota" else "一時障害"
    print(
        f"# {console_timestamp()} Codex CLI の {label} 回復待ち: {message}",
        file=sys.stderr,
        flush=True,
    )


def wait_for_recovery(
    *,
    key: tuple[object, ...],
    reason: RecoveryReason,
    probe: Callable[[RecoveryReason, bool, str], CodexOutcome],
    quota_interval: float,
    transient_interval: float,
    logger: SubcommandLogger | None,
    agent_call_id: str,
    stopped_codex_call_id: str,
    call_log_path: str,
) -> dict[RecoveryReason, float]:
    """同等条件の代表 probe が成功するまで待ち、理由別の実待機時間を返す。"""
    # 各確認ごとに同じ理由・設定継承条件の call を集約する。
    waited: dict[RecoveryReason, float] = {"quota": 0.0, "transient": 0.0}
    inherited = reason == "transient"
    while True:
        check_recovery_interruption()
        joined_at = time.perf_counter()
        group_key = (*key, reason, inherited)
        with _CONDITION:
            group = _GROUPS.get(group_key)
            leader = group is None
            if group is None:
                group = _RecoveryGroup()
                _GROUPS[group_key] = group

        def event(status: str, **fields: object) -> None:
            # 全 waiter の停止 call と代表 probe を recovery_id で対応付ける。
            if logger is not None:
                logger.event(
                    "codex_recovery",
                    status=status,
                    recovery_id=group.recovery_id,
                    agent_call_id=agent_call_id,
                    stopped_codex_call_id=stopped_codex_call_id,
                    call_log_path=call_log_path,
                    reason=reason,
                    inherited_config=inherited,
                    **fields,
                )

        try:
            event("started" if leader else "joined", representative=leader)
            if leader:
                interval = quota_interval if reason == "quota" else transient_interval
                _emit_progress(reason, f"待機を継続。次回確認は約 {interval:g} 秒後")
                event("waiting", next_probe_sec=interval)
                cancellation = current_recovery_cancellation()
                if cancellation is None:
                    time.sleep(interval)
                else:
                    cancellation.wait(interval)
                check_recovery_interruption()
                group.outcome = probe(reason, inherited, group.recovery_id)
            else:
                with _CONDITION:
                    while not group.done:
                        check_recovery_interruption()
                        _CONDITION.wait(timeout=0.1)
                if group.error is not None:
                    raise group.error
            check_recovery_interruption()
            event("probe_result", outcome=group.outcome)
            if group.outcome == "failed":
                raise CmocError(
                    "Codex CLI 回復確認 probe が失敗しました。",
                    ["診断用サブコマンドログを確認して原因を解消してください。"],
                    f"recovery_id: {group.recovery_id}",
                )
        except BaseException as exc:
            if leader:
                group.error = exc
            _emit_progress(
                reason,
                "中断により待機終了"
                if isinstance(exc, KeyboardInterrupt)
                else "失敗により待機終了",
            )
            event("stopped", error=type(exc).__name__)
            raise
        finally:
            if leader:
                with _CONDITION:
                    group.done = True
                    del _GROUPS[group_key]
                    _CONDITION.notify_all()
            # probe の時間も含め、各理由で実際に保留された時間だけを集計する。
            seconds = time.perf_counter() - joined_at
            waited[reason] += seconds
            if logger is not None:
                logger.add_recovery_wait(reason, seconds)
            event("finished", elapsed_sec=seconds)
        check_recovery_interruption()
        if group.outcome == "succeeded":
            _emit_progress(reason, "復旧を確認。処理を再開")
            event("resuming")
            return waited
        if group.outcome != reason:
            event("reason_changed", next_reason=group.outcome)
            reason = group.outcome
            inherited = inherited or reason == "transient"
            _emit_progress(reason, "待機理由を変更")
