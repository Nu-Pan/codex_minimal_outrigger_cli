import json
import time
from contextvars import ContextVar, Token
from datetime import datetime
from pathlib import Path
from typing import Any

from commons.runtime_paths import logs_dir, timestamp


_CURRENT_SUBCOMMAND_LOGGER: ContextVar["SubcommandLogger | None"] = ContextVar(
    "CURRENT_SUBCOMMAND_LOGGER",
    default=None,
)


class SubcommandLogger:
    """サブコマンド単位の JSON Lines event と待機時間を集約する logger。"""

    def __init__(self, root: Path, command: str) -> None:
        """実行中のサブコマンドが追記する log file を初期化する。"""
        self.root = root
        self.command = command
        self.started_at = time.perf_counter()
        self.quota_wait_sec = 0.0
        log_dir = logs_dir(root)
        log_dir.mkdir(parents=True, exist_ok=True)
        while True:
            self.path = log_dir / f"{timestamp()}.jsonl"
            try:
                # <work-root>/oracle/doc/app_spec/console_and_file_log.md requires
                # one <time-stamp>.jsonl per subcommand; reserve it atomically.
                self.path.open("x").close()
                break
            except FileExistsError:
                time.sleep(0.000001)

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
