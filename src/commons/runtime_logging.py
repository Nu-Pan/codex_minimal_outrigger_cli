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
    def __init__(self, root: Path, command: str) -> None:
        self.root = root
        self.command = command
        self.started_at = time.perf_counter()
        self.quota_wait_sec = 0.0
        self.path = logs_dir(root) / f"{timestamp()}.jsonl"
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def event(self, kind: str, **payload: Any) -> None:
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
        return time.perf_counter() - self.started_at

    def add_quota_wait(self, seconds: float) -> None:
        self.quota_wait_sec += seconds


def set_current_subcommand_logger(
    logger: SubcommandLogger | None,
) -> Token[SubcommandLogger | None]:
    return _CURRENT_SUBCOMMAND_LOGGER.set(logger)


def reset_current_subcommand_logger(token: Token[SubcommandLogger | None]) -> None:
    _CURRENT_SUBCOMMAND_LOGGER.reset(token)


def current_subcommand_logger() -> SubcommandLogger | None:
    return _CURRENT_SUBCOMMAND_LOGGER.get()
