"""サブコマンドのステップ時間計測。"""

from contextvars import ContextVar
from math import floor
from time import perf_counter

_CURRENT_TIMER: ContextVar["StepTimer | None"] = ContextVar(
    "cmoc_step_timer",
    default=None,
)


class StepTimer:
    """サブコマンド全体と各ステップの経過時間を記録する。"""

    def __init__(self, command_name: str) -> None:
        """空の計測器を作る。"""
        # サブコマンド全体の開始時刻と現在ステップ状態を初期化する。
        self.command_name = command_name
        self._started = perf_counter()
        self._current_name: str | None = None
        self._current_started: float | None = None
        self._durations: list[tuple[str, float]] = []
        self._reported = False
        _CURRENT_TIMER.set(self)

    def start(self, step_name: str) -> None:
        """新しいステップを開始し、直前のステップを終了する。"""
        # 直前ステップを確定してから新しいステップ名と開始時刻を保持する。
        self.finish_current()
        self._current_name = step_name
        self._current_started = perf_counter()

    def report(self) -> None:
        """ステップ別とサブコマンド全体の経過時間を stdout へ出力する。"""
        if self._reported:
            return
        # 未確定の最後のステップを含めてから stdout に集計を出す。
        self.finish_current()
        print(f"{self.command_name} step timings:")
        for name, duration in self._durations:
            print(f"- {name}: {format_duration(duration)}")
        print(
            f"{self.command_name} total elapsed: "
            f"{format_duration(perf_counter() - self._started)}"
        )
        self._reported = True

    def finish_current(self) -> None:
        """実行中のステップがあれば経過時間を確定する。"""
        # 計測中ステップが無ければ idempotent に何もしない。
        if self._current_name is None or self._current_started is None:
            return

        # 現在ステップの経過時間を保存して、計測中状態をクリアする。
        self._durations.append(
            (self._current_name, perf_counter() - self._current_started)
        )
        self._current_name = None
        self._current_started = None


def start_step(
    timer: StepTimer,
    step_number: int,
    total_steps: int,
    description: str,
) -> None:
    """ステップ開始を計測し、oracle 指定フォーマットで通知する。"""
    timer.start(description)
    print(f"({step_number}/{total_steps}) {description}")


def current_timer() -> StepTimer | None:
    """現在のサブコマンド用 StepTimer を返す。"""
    return _CURRENT_TIMER.get()


def report_current_timer() -> None:
    """現在の StepTimer があれば未出力の経過時間を出力する。"""
    timer = current_timer()
    if timer is None:
        return
    timer.report()


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
