"""サブコマンド呼び出し単位の tee ログ管理。"""

import subprocess
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
        """コンソール出力先とログファイル出力先を保持して初期化する。"""
        self._console = console
        self._log_file = log_file

    def write(self, text: str) -> int:
        """同じ文字列を両方の出力先へ書き込む。"""
        error: Exception | None = None
        try:
            self._log_file.write(text)
        except Exception as write_error:
            error = write_error
        try:
            self._console.write(text)
        except Exception as write_error:
            if error is None:
                error = write_error
        if error is not None:
            raise error
        return len(text)

    def flush(self) -> None:
        """両方の出力先を flush する。"""
        error: Exception | None = None
        try:
            self._log_file.flush()
        except Exception as flush_error:
            error = flush_error
        try:
            self._console.flush()
        except Exception as flush_error:
            if error is None:
                error = flush_error
        if error is not None:
            raise error

    def isatty(self) -> bool:
        """コンソール側の TTY 判定を引き継ぐ。"""
        return self._console.isatty()


@contextmanager
def subcommand_log(repo_root: Path) -> Iterator[SubcommandLogContext]:
    """stdout/stderr を `<repo-root>/.cmoc/logs/sub_commands` へ tee する。"""
    _ensure_logs_excluded(repo_root)
    log_dir = repo_root / ".cmoc" / "logs" / "sub_commands"
    log_dir.mkdir(parents=True, exist_ok=True)
    log_path, log_file = _create_unique_log_file(log_dir)
    with log_file:
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


def add_quota_wait(duration_seconds: float) -> None:
    """現在のサブコマンドに quota 回復待ち時間を加算する。"""
    context = current_subcommand_log()
    if context is None:
        return
    context.quota_wait_seconds += max(0.0, duration_seconds)


def current_subcommand_log() -> SubcommandLogContext | None:
    """現在のサブコマンドログ状態を返す。"""
    return _CURRENT_LOG.get()


def _create_unique_log_file(log_dir: Path) -> tuple[Path, IO[str]]:
    """未使用の `<time-stamp>.log` を排他的に新規作成する。"""
    while True:
        log_path = log_dir / f"{make_timestamp()}.log"
        try:
            return log_path, log_path.open("x", encoding="utf-8")
        except FileExistsError:
            continue


def _ensure_logs_excluded(repo_root: Path) -> None:
    """`.cmoc/logs/` がサブコマンド自身の未コミット差分にならないようにする。"""
    exclude_path = _git_exclude_path(repo_root)
    if exclude_path is None:
        return

    exclude_path.parent.mkdir(parents=True, exist_ok=True)
    if exclude_path.exists():
        content = exclude_path.read_text(encoding="utf-8")
    else:
        content = ""
    lines = [line.strip() for line in content.splitlines()]
    if "/.cmoc/logs/" in lines:
        return

    prefix = content
    if prefix and not prefix.endswith("\n"):
        prefix += "\n"
    exclude_path.write_text(f"{prefix}/.cmoc/logs/\n", encoding="utf-8")


def _git_exclude_path(repo_root: Path) -> Path | None:
    """repo の実際の gitdir にある info/exclude path を返す。"""
    git_entry = repo_root / ".git"
    if not git_entry.exists():
        return None

    result = subprocess.run(
        [
            "git",
            "rev-parse",
            "--path-format=absolute",
            "--git-path",
            "info/exclude",
        ],
        cwd=repo_root,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if result.returncode != 0:
        if git_entry.is_dir():
            return git_entry / "info" / "exclude"
        return None

    output = result.stdout.strip()
    if not output:
        return None
    path = Path(output)
    if path.is_absolute():
        return path
    return repo_root / path
