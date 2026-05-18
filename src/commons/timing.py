"""サブコマンドのステップ時間計測。"""

from time import perf_counter


class StepTimer:
    """サブコマンド全体と各ステップの経過時間を記録する。"""

    def __init__(self, command_name: str) -> None:
        """空の計測器を作る。"""
        self.command_name = command_name
        self._started = perf_counter()
        self._current_name: str | None = None
        self._current_started: float | None = None
        self._durations: list[tuple[str, float]] = []

    def start(self, step_name: str) -> None:
        """新しいステップを開始し、直前のステップを終了する。"""
        self.finish_current()
        self._current_name = step_name
        self._current_started = perf_counter()

    def finish_current(self) -> None:
        """実行中のステップがあれば経過時間を確定する。"""
        if self._current_name is None or self._current_started is None:
            return
        self._durations.append(
            (self._current_name, perf_counter() - self._current_started)
        )
        self._current_name = None
        self._current_started = None

    def report(self) -> None:
        """ステップ別とサブコマンド全体の経過時間を stdout へ出力する。"""
        self.finish_current()
        print(f"{self.command_name} step timings:")
        for name, duration in self._durations:
            print(f"- {name}: {duration:.3f}s")
        print(
            f"{self.command_name} total elapsed: "
            f"{perf_counter() - self._started:.3f}s"
        )
