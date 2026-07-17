import os
import threading
import time
from collections.abc import Callable, Iterator
from contextlib import contextmanager
from contextvars import ContextVar
from datetime import datetime
from pathlib import Path

from basic.path_model import RootPathPlaceHolder, resolve_real_path
from commons.runtime_errors import CmocError

_CWD_LOCK = threading.RLock()
_CWD_OVERRIDE_DEPTH: ContextVar[int] = ContextVar("CWD_OVERRIDE_DEPTH", default=0)


def repo_root(cwd: Path | None = None) -> Path:
    """cmoc の実行前提に合う repository root を runtime error として解決する。"""
    try:
        return _resolve_root(RootPathPlaceHolder.REPO, cwd)
    except ValueError as exc:
        raise CmocError(
            "{{repo-root}} を特定できません。",
            ["git repository 内から cmoc を再実行してください。"],
            str(cwd or Path.cwd()),
        ) from exc


def work_root(cwd: Path | None = None) -> Path:
    """cmoc の実行前提に合う worktree root を runtime error として解決する。"""
    try:
        return _resolve_root(RootPathPlaceHolder.WORK, cwd)
    except ValueError as exc:
        raise CmocError(
            "{{work-root}} を特定できません。",
            ["git worktree 内から cmoc を再実行してください。"],
            str(cwd or Path.cwd()),
        ) from exc


def _resolve_root(placeholder: RootPathPlaceHolder, cwd: Path | None) -> Path:
    """指定された起点から root placeholder を実パスへ解決する。

    Args:
        placeholder: 解決対象の root placeholder。
        cwd: 起点にする file または directory。None は現在の cwd を使う。

    Returns:
        placeholder が示す絶対 root path。
    """
    if cwd is None:
        with _CWD_LOCK:
            return resolve_real_path(placeholder)
    start_dir = cwd.resolve() if cwd.is_dir() else cwd.resolve().parent
    # {{work-root}}/oracle/src/oracle/other/path_model.py
    # root resolver は resolve_real_path 専用の内部実装なので、cwd 起点の
    # runtime 契約は一時的な cwd 切替で公開 API へ寄せる。
    with pushd(start_dir):
        return resolve_real_path(placeholder)


def timestamp() -> str:
    """file name に使う衝突しにくい実行時刻表記を返す。"""
    return datetime.now().strftime("%Y-%m-%d_%H-%M_%S_%f000")


def _reserve_timestamped_path(
    directory: Path, suffix: str, timestamp_factory: Callable[[], str]
) -> tuple[str, Path]:
    """timestamp 付き path を排他的に予約し、timestamp と path を返す。"""
    # {{work-root}}/oracle/doc/app_spec/codex_exec_rule.md
    # {{work-root}}/oracle/doc/app_spec/console_and_file_log.md
    # 壁時計 timestamp が衝突しても、内容を書き始める前に別 path を予約する。
    while True:
        value = timestamp_factory()
        path = directory / f"{value}{suffix}"
        try:
            path.open("x").close()
            return value, path
        except FileExistsError:
            time.sleep(0.000001)


def console_timestamp() -> str:
    """利用者向け console 表示用にミリ秒までの時刻表記を返す。"""
    return datetime.now().strftime("%Y/%m/%d %H:%M:%S.%f")[:-3]


def format_duration(seconds: float) -> str:
    """ログと console の duration 表示を丸めず 0.1 秒単位へそろえる。"""
    # {{work-root}}/oracle/doc/app_spec/console_and_file_log.md は経過時間の正規化表示を
    # 定めるため、負値を剰余計算で別の時刻へ変換せず入力エラーにする。
    if seconds < 0:
        raise ValueError("duration must be non-negative")
    total_tenths = int(seconds * 10)
    hours = total_tenths // 36000
    # {{work-root}}/oracle/doc/app_spec/console_and_file_log.md は hour field を 2 桁に
    # 限るため、表現できない duration は幅を広げずに失敗させる。
    if hours >= 100:
        raise ValueError("duration exceeds the two-digit hour display limit")
    minutes = (total_tenths % 36000) // 600
    sec_tenths = total_tenths % 600
    sec = sec_tenths // 10
    msec = sec_tenths % 10
    return f"{hours:2d}h {minutes:2d}m {sec:2d}.{msec}s"


def sessions_dir(root: Path) -> Path:
    """session state の保存先 directory を返す。"""
    return generated_agent_read_dir(root) / "session"


def reports_dir(root: Path, command: str) -> Path:
    """サブコマンド別 report 保存先 directory を返す。"""
    return generated_agent_read_dir(root) / "report" / command


def logs_dir(root: Path) -> Path:
    """サブコマンド log 保存先 directory を返す。"""
    return generated_agent_read_dir(root) / "log" / "sub_command"


def editor_input_dir(root: Path) -> Path:
    """エディタ入力と、その完全 prompt の保存先 directory を返す。"""
    return generated_agent_read_dir(root) / "log" / "editor_input"


def worktrees_dir(root: Path) -> Path:
    """cmoc 管理 worktree の保存先 directory を返す。"""
    return root / ".cmoc" / "gu" / "worktree"


def codex_log_dir(root: Path) -> Path:
    """Codex call log 保存先 directory を返す。"""
    return generated_agent_read_dir(root) / "log" / "codex"


def schema_store_dir(root: Path) -> Path:
    """Structured Output schema store directory を返す。"""
    return generated_agent_read_dir(root) / "schema"


def config_path(root: Path) -> Path:
    """cmoc config JSON の保存 path を返す。"""
    return tracked_agent_read_dir(root) / "config.json"


def generated_agent_read_dir(root: Path) -> Path:
    """git 非追跡かつ agent 読み取り専用の runtime directory を返す。"""
    # {{work-root}}/oracle/doc/app_spec/run_isolation.md
    return root / ".cmoc" / "gu" / "ar"


def tracked_agent_read_dir(root: Path) -> Path:
    """git 追跡かつ agent 読み取り専用の設定 directory を返す。"""
    # {{work-root}}/oracle/src/oracle/other/cmoc_config.py
    return root / ".cmoc" / "gt" / "ar"


def agent_read_dirs(root: Path) -> tuple[Path, Path]:
    """agent が読み取れる `.cmoc/g*/ar` directory 群を返す。"""
    # {{work-root}}/oracle/src/oracle/prompt_builder/parts/file_access_rule.py
    return generated_agent_read_dir(root), tracked_agent_read_dir(root)


def is_root_memo(root: Path, path: Path) -> bool:
    """`{{work-root}}/memo` 自体またはその配下か判定する。"""
    memo = (root / "memo").resolve()
    resolved = path.resolve()
    return resolved == memo or memo in resolved.parents


def cwd_override_active() -> bool:
    """現在の context が ``pushd`` による cwd 切替区間内かを返す。"""
    return _CWD_OVERRIDE_DEPTH.get() > 0


@contextmanager
def pushd(path: Path) -> Iterator[None]:
    """外部 API が cwd 前提を持つ区間を process-wide に直列化する。"""
    # os.chdir は process-global なので、切替から復元まで lock を保持する。
    with _CWD_LOCK:
        previous = Path.cwd()
        os.chdir(path)
        token = _CWD_OVERRIDE_DEPTH.set(_CWD_OVERRIDE_DEPTH.get() + 1)
        try:
            yield
        finally:
            _CWD_OVERRIDE_DEPTH.reset(token)
            os.chdir(previous)


def cmoc_root() -> Path:
    """cmoc 自身の repository root を runtime error として解決する。"""
    try:
        return resolve_real_path(RootPathPlaceHolder.CMOC)
    except ValueError as exc:
        raise CmocError(
            "{{cmoc-root}} を特定できません。",
            ["cmoc repository 内から実行しているか確認してください。"],
            str(Path(__file__).resolve()),
        ) from exc
