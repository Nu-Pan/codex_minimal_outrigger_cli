"""サブコマンド呼び出し単位の tee ログ管理。"""

from __future__ import annotations

import sys
from contextlib import contextmanager, redirect_stderr, redirect_stdout
from contextvars import ContextVar
from dataclasses import dataclass
from pathlib import Path
from time import perf_counter
from typing import IO, Iterator

from .timestamps import make_timestamp


@dataclass
class SubcommandLogContext:
    """現在実行中のサブコマンドログ状態。"""

    repo_root: Path
    path: Path
    started: float
    quota_wait_seconds: float = 0.0


_CURRENT_LOG: ContextVar[SubcommandLogContext | None] = ContextVar(
    "cmoc_subcommand_log",
    default=None,
)


class _TeeTextIO:
    """write/flush をコンソールとログファイルへ複製する。"""

    def __init__(self, console: IO[str], log_file: IO[str]) -> None:
        self._console = console
        self._log_file = log_file

    def write(self, text: str) -> int:
        """同じ文字列を両方の出力先へ書き込む。"""
        self._console.write(text)
        self._log_file.write(text)
        return len(text)

    def flush(self) -> None:
        """両方の出力先を flush する。"""
        self._console.flush()
        self._log_file.flush()

    def isatty(self) -> bool:
        """コンソール側の TTY 判定を引き継ぐ。"""
        return self._console.isatty()


@contextmanager
def subcommand_log(repo_root: Path) -> Iterator[SubcommandLogContext]:
    """stdout/stderr を `<repo-root>/logs/sub_commands` へ tee する。"""
    _ensure_logs_excluded(repo_root)
    log_dir = repo_root / "logs" / "sub_commands"
    log_dir.mkdir(parents=True, exist_ok=True)
    log_path = log_dir / f"{make_timestamp()}.log"
    with log_path.open("a", encoding="utf-8") as log_file:
        context = SubcommandLogContext(
            repo_root=repo_root,
            path=log_path,
            started=perf_counter(),
        )
        token = _CURRENT_LOG.set(context)
        stdout_tee = _TeeTextIO(sys.stdout, log_file)
        stderr_tee = _TeeTextIO(sys.stderr, log_file)
        try:
            with redirect_stdout(stdout_tee), redirect_stderr(stderr_tee):
                print(f"subcommand log: {log_path.relative_to(repo_root)}")
                yield context
        finally:
            _CURRENT_LOG.reset(token)


def current_subcommand_log() -> SubcommandLogContext | None:
    """現在のサブコマンドログ状態を返す。"""
    return _CURRENT_LOG.get()


def add_quota_wait(duration_seconds: float) -> None:
    """現在のサブコマンドに quota 回復待ち時間を加算する。"""
    context = current_subcommand_log()
    if context is None:
        return
    context.quota_wait_seconds += max(0.0, duration_seconds)


def _ensure_logs_excluded(repo_root: Path) -> None:
    """`logs/` がサブコマンド自身の未コミット差分にならないようにする。"""
    exclude_path = repo_root / ".git" / "info" / "exclude"
    if not exclude_path.exists():
        return

    content = exclude_path.read_text(encoding="utf-8")
    lines = [line.strip() for line in content.splitlines()]
    if "/logs/" in lines:
        return

    prefix = content
    if prefix and not prefix.endswith("\n"):
        prefix += "\n"
    exclude_path.write_text(f"{prefix}/logs/\n", encoding="utf-8")
