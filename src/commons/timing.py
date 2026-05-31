"""サブコマンドのステップ時間計測。"""

from collections.abc import Sequence
from contextvars import ContextVar
from dataclasses import dataclass
from math import floor
from time import perf_counter

from .subcommand_log import log_event
from .timestamps import console_timestamp

_CURRENT_TIMER: ContextVar["StepTimer | None"] = ContextVar(
    "cmoc_step_timer",
    default=None,
)

StepIndexPath = Sequence[tuple[int, int]]


@dataclass
class _StepRecord:
    """開始済みステップの表示名と開始・終了時刻。"""

    name: str
    started: float
    step_index: str | None
    step_path: tuple[tuple[int, int], ...] | None
    ended: float | None = None

    def label(self) -> str:
        """完了サマリー用に step index と説明を結合する。"""
        if self.step_index is None:
            return self.name
        return f"{self.step_index} {self.name}"

    def duration(self) -> float:
        """確定済みステップの経過秒数を返す。"""
        if self.ended is None:
            return perf_counter() - self.started
        return self.ended - self.started


class StepTimer:
    """サブコマンド全体と各ステップの経過時間を記録する。"""

    def __init__(self, command_name: str) -> None:
        """空の計測器を作る。"""
        # サブコマンド全体の開始時刻と現在ステップ状態を初期化する。
        self.command_name = command_name
        self._started = perf_counter()
        self._active_records: list[_StepRecord] = []
        self._records: list[_StepRecord] = []
        self._reported = False
        _CURRENT_TIMER.set(self)

    def start(
        self,
        step_name: str,
        *,
        step_index: str | None = None,
        step_path: StepIndexPath | None = None,
    ) -> None:
        """新しいステップを開始し、階層上不要になったステップを終了する。"""
        normalized_path = (
            tuple(step_path)
            if step_path is not None
            else None
        )
        self._finish_steps_not_containing(normalized_path)
        record = _StepRecord(
            name=step_name,
            started=perf_counter(),
            step_index=step_index,
            step_path=normalized_path,
        )
        self._active_records.append(record)
        self._records.append(record)

    def report(self) -> None:
        """ステップ別とサブコマンド全体の経過時間を stdout へ出力する。"""
        if self._reported:
            return
        # 未確定の最後のステップを含めてから stdout に集計を出す。
        self.finish_current()
        print(f"{self.command_name} step timings:")
        for record in self._records:
            print(f"- {record.label()}: {format_duration(record.duration())}")
        print(
            f"{self.command_name} total elapsed: "
            f"{format_duration(perf_counter() - self._started)}"
        )
        self._reported = True

    def finish_current(self) -> None:
        """実行中のステップがあれば経過時間を確定する。"""
        self._finish_active_steps()

    def _finish_steps_not_containing(
        self,
        step_path: tuple[tuple[int, int], ...] | None,
    ) -> None:
        """新ステップの親ではない active step を終了する。"""
        if step_path is None:
            self._finish_active_steps()
            return

        now = perf_counter()
        while self._active_records:
            active = self._active_records[-1]
            if (
                active.step_path is not None
                and _is_strict_prefix(active.step_path, step_path)
            ):
                return
            active.ended = now
            self._active_records.pop()

    def _finish_active_steps(self) -> None:
        """active stack 上の全ステップを終了する。"""
        now = perf_counter()
        while self._active_records:
            record = self._active_records.pop()
            record.ended = now


def start_step(
    timer: StepTimer,
    step_number: int | StepIndexPath,
    total_steps: int | None,
    description: str,
) -> None:
    """ステップ開始を計測し、oracle 指定フォーマットで通知する。"""
    step_index = _format_step_index(step_number, total_steps)
    step_path = _normalize_step_path(step_number, total_steps)
    timer.start(description, step_index=step_index, step_path=step_path)
    timestamp = console_timestamp()
    log_event(
        "step_start",
        {
            "command": timer.command_name,
            "step": description,
            "step_index": step_index,
        },
    )
    print(f"# {timestamp} ({step_index}) {description}")


def _normalize_step_path(
    step_number: int | StepIndexPath,
    total_steps: int | None,
) -> tuple[tuple[int, int], ...]:
    """単一階層または階層化ステップ番号を内部 path へ正規化する。"""
    if isinstance(step_number, int):
        if total_steps is None:
            raise ValueError("total_steps is required for flat step index.")
        return ((step_number, total_steps),)

    if total_steps is not None:
        raise ValueError("total_steps must be None for hierarchical step index.")
    if not step_number:
        raise ValueError("hierarchical step index must not be empty.")
    return tuple(step_number)


def _format_step_index(
    step_number: int | StepIndexPath,
    total_steps: int | None,
) -> str:
    """単一階層または階層化ステップ番号を表示用文字列へ変換する。"""
    # 既存の単一階層 API 呼び出しはそのまま `i/N` として扱う。
    if isinstance(step_number, int):
        if total_steps is None:
            raise ValueError("total_steps is required for flat step index.")
        return f"{step_number}/{total_steps}"

    # 階層化 API では全階層を `i/N, j/M, ...` として並べる。
    if total_steps is not None:
        raise ValueError("total_steps must be None for hierarchical step index.")
    if not step_number:
        raise ValueError("hierarchical step index must not be empty.")
    parts: list[str] = []
    for current_step, current_total in step_number:
        parts.append(f"{current_step}/{current_total}")
    return ", ".join(parts)


def _is_strict_prefix(
    candidate: tuple[tuple[int, int], ...],
    value: tuple[tuple[int, int], ...],
) -> bool:
    """candidate が value の真の親階層なら True を返す。"""
    return len(candidate) < len(value) and value[: len(candidate)] == candidate


def report_current_timer() -> None:
    """現在の StepTimer があれば未出力の経過時間を出力する。"""
    timer = current_timer()
    if timer is None:
        return
    timer.report()


def current_timer() -> StepTimer | None:
    """現在のサブコマンド用 StepTimer を返す。"""
    return _CURRENT_TIMER.get()


def clear_current_timer() -> None:
    """現在の StepTimer 参照を消す。"""
    _CURRENT_TIMER.set(None)


def format_duration(duration_seconds: float) -> str:
    """oracle 指定の経過時間表示へ変換する。"""
    # 秒数を 0.1 秒単位に切り捨て、負値は 0 として扱う。
    total_tenths = max(0, floor(duration_seconds * 10))
    total_seconds, msec = divmod(total_tenths, 10)
    total_minutes, sec = divmod(total_seconds, 60)
    hour, minute = divmod(total_minutes, 60)
    return f"{hour:2d}h {minute:2d}m {sec:2d}.{msec}s"
