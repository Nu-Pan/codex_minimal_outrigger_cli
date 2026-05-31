"""サブコマンド呼び出し単位の JSON Lines ログ管理。"""

import json
import subprocess
from contextlib import contextmanager
from contextvars import ContextVar
from dataclasses import dataclass
from dataclasses import field
from datetime import datetime
from pathlib import Path
from threading import Lock
from time import perf_counter
from typing import IO, Iterator
from typing import Any

from .timestamps import make_timestamp


@dataclass
class SubcommandLogContext:
    """現在実行中のサブコマンドログ状態。"""

    repo_root: Path
    path: Path
    started: float
    quota_wait_seconds: float = 0.0
    lock: Any = field(default_factory=Lock)


_CURRENT_LOG: ContextVar[SubcommandLogContext | None] = ContextVar(
    "cmoc_subcommand_log",
    default=None,
)


@contextmanager
def subcommand_log(repo_root: Path) -> Iterator[SubcommandLogContext]:
    """サブコマンドイベントを `<repo-root>/.cmoc/logs/sub_commands` へ記録する。"""
    log_root = _subcommand_log_repo_root(repo_root)
    _ensure_logs_excluded(log_root)
    log_dir = log_root / ".cmoc" / "logs" / "sub_commands"
    log_dir.mkdir(parents=True, exist_ok=True)
    log_path, log_file = _create_unique_log_file(log_dir)
    with log_file:
        context = SubcommandLogContext(
            repo_root=log_root,
            path=log_path,
            started=perf_counter(),
        )
        token = _CURRENT_LOG.set(context)
        try:
            log_event("subcommand_start", {"repo_root": str(log_root)})
            print(f"# cmoc subcommand start")
            print(f"- subcommand log: {log_path}")
            yield context
        finally:
            _CURRENT_LOG.reset(token)


def log_event(event: str, payload: dict[str, object]) -> None:
    """現在のサブコマンドログへ 1 イベントを JSON Lines で追記する。"""
    context = current_subcommand_log()
    if context is None:
        return
    record = {
        "event": event,
        "time": _console_timestamp(),
        "elapsed_seconds": perf_counter() - context.started,
        **payload,
    }
    line = json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n"
    with context.lock:
        with context.path.open("a", encoding="utf-8") as log_file:
            log_file.write(line)
            log_file.flush()


def add_quota_wait(duration_seconds: float) -> None:
    """現在のサブコマンドに quota 回復待ち時間を加算する。"""
    context = current_subcommand_log()
    if context is None:
        return
    duration = max(0.0, duration_seconds)
    with context.lock:
        context.quota_wait_seconds += duration
    log_event("quota_wait_added", {"duration_seconds": duration})


def current_subcommand_log() -> SubcommandLogContext | None:
    """現在のサブコマンドログ状態を返す。"""
    return _CURRENT_LOG.get()


def _create_unique_log_file(log_dir: Path) -> tuple[Path, IO[str]]:
    """未使用の `<time-stamp>.jsonl` を排他的に新規作成する。"""
    while True:
        log_path = log_dir / f"{make_timestamp()}.jsonl"
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


def _subcommand_log_repo_root(repo_root: Path) -> Path:
    """サブコマンドログを書き込む repo root を返す。"""
    owner_root = _owning_repo_root_from_apply_worktree_path(repo_root)
    if owner_root is not None:
        return owner_root

    if not (repo_root / ".git").exists():
        return repo_root
    result = subprocess.run(
        [
            "git",
            "rev-parse",
            "--path-format=absolute",
            "--git-common-dir",
        ],
        cwd=repo_root,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if result.returncode != 0:
        return repo_root
    common_dir = result.stdout.strip()
    if not common_dir:
        return repo_root
    common_root = Path(common_dir).parent
    if _is_cmoc_managed_worktree_root(repo_root, common_root):
        return common_root
    return repo_root


def _owning_repo_root_from_apply_worktree_path(repo_root: Path) -> Path | None:
    """cmoc apply worktree path から所有元 repo root を復元する。"""
    parts = repo_root.resolve().parts
    marker = (".cmoc", "worktrees", "apply")
    for index in range(0, len(parts) - len(marker)):
        if parts[index : index + len(marker)] != marker:
            continue
        if len(parts) == index + len(marker) + 2:
            return Path(*parts[:index])
    return None


def _is_cmoc_managed_worktree_root(repo_root: Path, common_root: Path) -> bool:
    """repo_root が common_root 配下の cmoc 管理 worktree なら真を返す。"""
    try:
        repo_root.resolve().relative_to(
            (common_root / ".cmoc" / "worktrees").resolve()
        )
    except ValueError:
        return False
    return True


def _console_timestamp() -> str:
    """コンソールログ用のミリ秒付き日時を返す。"""
    now = datetime.now().astimezone()
    return (
        f"{now.year:04d}/{now.month:02d}/{now.day:02d} "
        f"{now.hour:02d}:{now.minute:02d}:{now.second:02d}."
        f"{now.microsecond // 1000:03d}"
    )
