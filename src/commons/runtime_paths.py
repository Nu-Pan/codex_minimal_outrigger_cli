import os
from collections.abc import Iterator
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path

from basic.path_model import RootPathPlaceHolder, resolve_real_path

from commons.runtime_errors import CmocError


def repo_root(cwd: Path | None = None) -> Path:
    """cmoc の実行前提に合う repository root を runtime error として解決する。"""
    try:
        return _resolve_root(RootPathPlaceHolder.REPO, cwd)
    except ValueError as exc:
        raise CmocError(
            "<repo-root> を特定できません。",
            ["git repository 内から cmoc を再実行してください。"],
            str(cwd or Path.cwd()),
        ) from exc


def work_root(cwd: Path | None = None) -> Path:
    """cmoc の実行前提に合う worktree root を runtime error として解決する。"""
    try:
        return _resolve_root(RootPathPlaceHolder.WORK, cwd)
    except ValueError as exc:
        raise CmocError(
            "<work-root> を特定できません。",
            ["git worktree 内から cmoc を再実行してください。"],
            str(cwd or Path.cwd()),
        ) from exc


def _resolve_root(placeholder: RootPathPlaceHolder, cwd: Path | None) -> Path:
    if cwd is None:
        return resolve_real_path(placeholder)
    start_dir = cwd.resolve() if cwd.is_dir() else cwd.resolve().parent
    # <work-root>/oracle/src/oracle/other/path_model.py
    # root resolver は resolve_real_path 専用の内部実装なので、cwd 起点の
    # runtime 契約は一時的な cwd 切替で公開 API へ寄せる。
    with pushd(start_dir):
        return resolve_real_path(placeholder)


def timestamp() -> str:
    """file name に使う衝突しにくい実行時刻表記を返す。"""
    return datetime.now().strftime("%Y-%m-%d_%H-%M_%S_%f000")


def console_timestamp() -> str:
    """利用者向け console 表示用にミリ秒までの時刻表記を返す。"""
    return datetime.now().strftime("%Y/%m/%d %H:%M:%S.%f")[:-3]


def format_duration(seconds: float) -> str:
    """ログと console の duration 表示を丸めず 0.1 秒単位へそろえる。"""
    total_tenths = int(seconds * 10)
    hours = total_tenths // 36000
    minutes = (total_tenths % 36000) // 600
    sec_tenths = total_tenths % 600
    sec = sec_tenths // 10
    msec = sec_tenths % 10
    return f"{hours:2d}h {minutes:2d}m {sec:2d}.{msec}s"


def sessions_dir(root: Path) -> Path:
    """session state の保存先 directory を返す。"""
    return root / ".cmoc" / "local" / "session"


def reports_dir(root: Path, command: str) -> Path:
    """サブコマンド別 report 保存先 directory を返す。"""
    return root / ".cmoc" / "local" / "report" / command


def logs_dir(root: Path) -> Path:
    """サブコマンド log 保存先 directory を返す。"""
    return root / ".cmoc" / "local" / "log" / "sub_command"


def worktrees_dir(root: Path) -> Path:
    """cmoc 管理 worktree の保存先 directory を返す。"""
    return root / ".cmoc" / "local" / "worktree"


def codex_log_dir(root: Path) -> Path:
    """Codex call log 保存先 directory を返す。"""
    return root / ".cmoc" / "local" / "log" / "codex"


def schema_store_dir(root: Path) -> Path:
    """Structured Output schema store directory を返す。"""
    return root / ".cmoc" / "local" / "schema"


def config_path(root: Path) -> Path:
    """cmoc config JSON の保存 path を返す。"""
    return root / ".cmoc" / "config.json"


def is_root_memo(root: Path, path: Path) -> bool:
    """`<work-root>/memo` 自体またはその配下か判定する。"""
    memo = (root / "memo").resolve()
    resolved = path.resolve()
    return resolved == memo or memo in resolved.parents


@contextmanager
def pushd(path: Path) -> Iterator[None]:
    """外部 API が cwd 前提を持つ短い区間だけ作業 directory を差し替える。"""
    previous = Path.cwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(previous)


def cmoc_root() -> Path:
    """cmoc 自身の repository root を runtime error として解決する。"""
    try:
        return resolve_real_path(RootPathPlaceHolder.CMOC)
    except ValueError as exc:
        raise CmocError(
            "<cmoc-root> を特定できません。",
            ["cmoc repository 内から実行しているか確認してください。"],
            str(Path(__file__).resolve()),
        ) from exc
