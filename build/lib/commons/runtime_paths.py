import os
from collections.abc import Iterator
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path

from basic.path_model import RootPathPlaceHolder, resolve_real_path

from commons.runtime_errors import CmocError

# `<work-root>/oracle/src/oracle/other/path_model.py` keeps root resolver
# functions internal to path resolution. Runtime needs `start_path` for cwd-like
# checks, so this module wraps those internals without re-exporting them through
# `basic.path_model`.
from oracle.other.path_model import (
    resolve_repo_root as _resolve_repo_root,
    resolve_work_root as _resolve_work_root,
)


def repo_root(cwd: Path | None = None) -> Path:
    try:
        return _resolve_repo_root(cwd)
    except ValueError as exc:
        raise CmocError(
            "<repo-root> を特定できません。",
            ["git repository 内から cmoc を再実行してください。"],
            str(cwd or Path.cwd()),
        ) from exc


def work_root(cwd: Path | None = None) -> Path:
    try:
        return _resolve_work_root(cwd)
    except ValueError as exc:
        raise CmocError(
            "<work-root> を特定できません。",
            ["git worktree 内から cmoc を再実行してください。"],
            str(cwd or Path.cwd()),
        ) from exc


def timestamp() -> str:
    return datetime.now().strftime("%Y-%m-%d_%H-%M_%S_%f000")


def console_timestamp() -> str:
    return datetime.now().strftime("%Y/%m/%d %H:%M:%S.%f")[:-3]


def format_duration(seconds: float) -> str:
    total_tenths = int(seconds * 10)
    hours = total_tenths // 36000
    minutes = (total_tenths % 36000) // 600
    sec_tenths = total_tenths % 600
    sec = sec_tenths // 10
    msec = sec_tenths % 10
    return f"{hours:2d}h {minutes:2d}m {sec:2d}.{msec}s"


def sessions_dir(root: Path) -> Path:
    return root / ".cmoc" / "sessions"


def reports_dir(root: Path, command: str) -> Path:
    return root / ".cmoc" / "reports" / command


def logs_dir(root: Path) -> Path:
    return root / ".cmoc" / "log" / "sub_command"


def worktrees_dir(root: Path) -> Path:
    return root / ".cmoc" / "worktrees"


def codex_log_dir(root: Path) -> Path:
    return root / ".cmoc" / "log" / "codex"


def schema_store_dir(root: Path) -> Path:
    return root / ".cmoc" / "state" / "schema"


def config_path(root: Path) -> Path:
    return root / ".cmoc" / "config.json"


def is_root_memo(root: Path, path: Path) -> bool:
    """`<work-root>/memo` 自体またはその配下か判定する。"""
    memo = (root / "memo").resolve()
    resolved = path.resolve()
    return resolved == memo or memo in resolved.parents


@contextmanager
def pushd(path: Path) -> Iterator[None]:
    previous = Path.cwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(previous)


def cmoc_root() -> Path:
    try:
        return resolve_real_path(RootPathPlaceHolder.CMOC)
    except ValueError as exc:
        raise CmocError(
            "<cmoc-root> を特定できません。",
            ["cmoc repository 内から実行しているか確認してください。"],
            str(Path(__file__).resolve()),
        ) from exc
