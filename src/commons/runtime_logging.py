import json
import time
from contextvars import ContextVar, Token
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

from commons.runtime_paths import _reserve_timestamped_path, logs_dir, timestamp

_CURRENT_SUBCOMMAND_LOGGER: ContextVar["SubcommandLogger | None"] = ContextVar(
    "CURRENT_SUBCOMMAND_LOGGER",
    default=None,
)


@dataclass
class StepTiming:
    """console summary と log event が共有する step timing の実測単位。"""

    index: str
    description: str
    started_at: float
    elapsed_sec: float | None = None


class SubcommandLogger:
    """サブコマンド単位の JSON Lines event と待機時間を集約する logger。"""

    def __init__(self, root: Path, command: str) -> None:
        """実行中のサブコマンドが追記する log file を初期化する。"""
        self.root = root
        self.command = command
        self.started_at = time.perf_counter()
        self.quota_wait_sec = 0.0
        self.step_timings: list[StepTiming] = []
        log_dir = logs_dir(root)
        log_dir.mkdir(parents=True, exist_ok=True)
        # {{work-root}}/oracle/doc/app_spec/console_and_file_log.md
        _, self.path = _reserve_timestamped_path(log_dir, ".jsonl", timestamp)

    def event(self, kind: str, **payload: Any) -> None:
        """実行時に後から検査したい event を安定した JSON record として残す。"""
        record = {
            "event": kind,
            "command": self.command,
            "timestamp": datetime.now().isoformat(),
            **payload,
        }
        with self.path.open("a") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
            f.flush()

    def start_step(
        self, index: str, description: str, log_description: str | None = None
    ) -> None:
        """完了サマリー用の step 実測値を開始 event と同じ単位で保持する。

        根拠: {{work-root}}/oracle/doc/app_spec/console_and_file_log.md
        `{{work-root}}/oracle/doc/dev_rule/coding_rule.md` が log message を英語に
        限るため、console 表示名と JSON Lines の step 名は分けられる。
        """
        self.finish_current_step()
        self.step_timings.append(StepTiming(index, description, time.perf_counter()))
        self.event(
            "step_started",
            step=log_description or description,
            step_index=index,
        )

    def finish_current_step(self) -> None:
        """進行中 step があれば終了時刻を一度だけ記録する。"""
        if self.step_timings and self.step_timings[-1].elapsed_sec is None:
            step = self.step_timings[-1]
            step.elapsed_sec = time.perf_counter() - step.started_at

    def elapsed(self) -> float:
        """サブコマンド開始からの経過秒を、完了表示と log 集計用に返す。"""
        return time.perf_counter() - self.started_at

    def add_quota_wait(self, seconds: float) -> None:
        """Codex quota 待機をサブコマンド全体の待機時間として合算する。"""
        self.quota_wait_sec += seconds


def set_current_subcommand_logger(
    logger: SubcommandLogger | None,
) -> Token[SubcommandLogger | None]:
    """現在の制御文脈から参照できるサブコマンド logger を差し替える。"""
    return _CURRENT_SUBCOMMAND_LOGGER.set(logger)


def reset_current_subcommand_logger(token: Token[SubcommandLogger | None]) -> None:
    """一時的に差し替えた current logger を元の context 状態へ戻す。"""
    _CURRENT_SUBCOMMAND_LOGGER.reset(token)


def current_subcommand_logger() -> SubcommandLogger | None:
    """深い runtime helper からサブコマンド logger を任意利用できるようにする。"""
    return _CURRENT_SUBCOMMAND_LOGGER.get()
