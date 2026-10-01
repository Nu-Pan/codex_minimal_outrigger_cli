"""cmoc の root・保存先解決、配置先補完、時刻整形、cwd 切替を提供する。"""

import os
import stat
import threading
from collections.abc import Iterator
from contextlib import contextmanager
from contextvars import ContextVar
from datetime import datetime
from pathlib import Path

from basic.path_model import RootPathPlaceHolder, resolve_real_path

from .runtime_errors import CmocError

_CMOC_PROCESS_CWD_LOCK = threading.RLock()
_RootQueryKey = tuple[RootPathPlaceHolder, Path, tuple[tuple[str, str], ...]]
_ROOT_QUERIES: ContextVar[dict[_RootQueryKey, Path] | None] = ContextVar(
    "cmoc_root_queries", default=None
)


@contextmanager
def reuse_root_queries() -> Iterator[None]:
    """repository 構成を変えない処理内で、成功した root 解決を再利用する。"""
    # 呼び出し間や並行する別 context に root の探索結果を持ち越さない。
    token = _ROOT_QUERIES.set({})
    try:
        yield
    finally:
        _ROOT_QUERIES.reset(token)


def repo_root(root_anchor: Path | None = None) -> Path:
    """cmoc の実行前提に合う repository root を runtime error として解決する。"""
    try:
        return _resolve_root(RootPathPlaceHolder.REPO, root_anchor)
    except ValueError as exc:
        raise CmocError(
            "{{repo-root}} を特定できません。",
            ["git repository 内から cmoc を再実行してください。"],
            str(root_anchor or Path.cwd()),
        ) from exc


def work_root(root_anchor: Path | None = None) -> Path:
    """cmoc の実行前提に合う worktree root を runtime error として解決する。"""
    try:
        return _resolve_root(RootPathPlaceHolder.WORK, root_anchor)
    except ValueError as exc:
        raise CmocError(
            "{{work-root}} を特定できません。",
            ["git worktree 内から cmoc を再実行してください。"],
            str(root_anchor or Path.cwd()),
        ) from exc


def _resolve_root(placeholder: RootPathPlaceHolder, root_anchor: Path | None) -> Path:
    """指定された起点から root placeholder を実パスへ解決する。

    Args:
        placeholder: 解決対象の root placeholder。
        root_anchor: 起点にする file または directory。None は process の cwd を使う。

    Returns:
        placeholder が示す絶対 root path。
    """
    with _CMOC_PROCESS_CWD_LOCK:
        # {{work-root}}/oracle/doc/dev_rule/coding_rule.md
        # root 探索の起点は file または directory なので、process の cwd と区別する。
        # relative path の解決から root resolver の完了まで process-global cwd を
        # 固定し、別 thread の pushd と起点 path が混線しないようにする。
        resolved_root_anchor = (root_anchor or Path.cwd()).resolve()
        start_dir = (
            resolved_root_anchor
            if resolved_root_anchor.is_dir()
            else resolved_root_anchor.parent
        )
        # 存在しない file/directory を起点にしても、既存の祖先から root を探索できる。
        while not start_dir.is_dir():
            parent = start_dir.parent
            if parent == start_dir:
                break
            start_dir = parent
        # doctor 内でも起点や環境の異なる探索は共有せず、失敗は記憶しない。
        queries = _ROOT_QUERIES.get()
        key = (placeholder, start_dir, tuple(sorted(os.environ.items())))
        if queries is not None and key in queries:
            return queries[key]
        # {{work-root}}/oracle/src/oracle/other/path_model.py
        # root resolver は resolve_real_path 専用の内部実装なので、cwd 起点の
        # runtime 契約は一時的な cwd 切替で公開 API へ寄せる。
        with pushd(start_dir):
            resolved = resolve_real_path(placeholder)
        if queries is not None:
            queries[key] = resolved
        return resolved


def timestamp() -> str:
    """ローカル日時をミリ秒精度の共通 timestamp として返す。"""
    now = datetime.now()
    return (
        f"{now.year:04d}-{now.month:02d}-{now.day:02d}_"
        f"{now.hour:02d}-{now.minute:02d}-{now.second:02d}_"
        f"{now.microsecond // 1000:03d}"
    )


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

    # 経過時間には暦上の起点がないため、month は固定 30 day として分解する。
    tenths_per_day = 24 * 60 * 60 * 10
    months, remainder = divmod(total_tenths, 30 * tenths_per_day)
    days, remainder = divmod(remainder, tenths_per_day)
    hours, remainder = divmod(remainder, 36000)
    minutes, sec_tenths = divmod(remainder, 600)
    sec, msec = divmod(sec_tenths, 10)

    # {{work-root}}/oracle/doc/app_spec/console_and_file_log.md は各 field を 2 桁に
    # 限るため、表現できない duration は幅を広げずに失敗させる。
    if months >= 100:
        raise ValueError("duration exceeds the two-digit month display limit")

    # 最初の非 0 単位より上位だけを省略し、seconds は常に残す。
    values = (months, days, hours, minutes)
    parts = (
        f"{months:2d} Mo",
        f"{days:2d} Day",
        f"{hours:2d} Hr",
        f"{minutes:2d} Min",
        f"{sec:2d}.{msec} Sec",
    )
    first_visible = next(
        (index for index, value in enumerate(values) if value), len(values)
    )
    return " ".join(parts[first_visible:])


def sessions_dir(root: Path) -> Path:
    """session state の保存先 directory を返す。"""
    return untracked_data_dir(root) / "session"


def reports_dir(root: Path, command: str) -> Path:
    """サブコマンド別 report 保存先 directory を返す。"""
    return untracked_data_dir(root) / "report" / command


def logs_dir(root: Path) -> Path:
    """サブコマンド log 保存先 directory を返す。"""
    return untracked_data_dir(root) / "log" / "sub_command"


def editor_input_log_dir(root: Path) -> Path:
    """編集から確定保存まで使う editor input file の directory を返す。"""
    # {{work-root}}/oracle/doc/app_spec/prompt_editor_input.md
    return untracked_data_dir(root) / "log" / "editor_input"


def worktrees_dir(root: Path) -> Path:
    """cmoc 管理 worktree の保存先 directory を返す。"""
    return untracked_data_dir(root) / "worktree"


def codex_log_dir(root: Path) -> Path:
    """Codex call log 保存先 directory を返す。"""
    return untracked_data_dir(root) / "log" / "codex"


def schema_store_dir(root: Path) -> Path:
    """Structured Output schema store directory を返す。"""
    return untracked_data_dir(root) / "schema"


def config_path(root: Path) -> Path:
    """cmoc config JSON の保存 path を返す。"""
    return _tracked_data_dir(root) / "config.json"


def refactor_state_path(root: Path) -> Path:
    """realization refactor の追跡 state 保存 path を返す。"""
    # {{work-root}}/oracle/doc/app_spec/sub_command/realization_refactor.md
    return _tracked_data_dir(root) / "realization" / "refactor" / "state.json"


def untracked_data_dir(root: Path) -> Path:
    """git 非追跡の cmoc 管理 directory を返す。"""
    # {{work-root}}/oracle/doc/app_spec/run_isolation.md
    return root / ".cmoc" / "gu"


def _tracked_data_dir(root: Path) -> Path:
    """git 追跡する cmoc 管理 directory を返す。"""
    # {{work-root}}/oracle/src/oracle/other/cmoc_config.py
    return root / ".cmoc" / "gt"


def ensure_work_directories(root: Path, *, create_missing: bool = True) -> None:
    """処理対象 work-root の固定配置先を補完・検証する。

    Args:
        root: 配置先を使用する worktree の root。
        create_missing: 不足を補完するか。False は修復後の状態の検証に使う。
    """
    # {{cmoc-root}}/oracle/doc/app_spec/doctor_preprocess.md の
    # 「作業用配置先の存在保証」
    for relative in ("oracle/doc", "oracle/src", "oracle/test", "src", "test"):
        path = root / relative
        try:
            if create_missing:
                path.mkdir(parents=True, exist_ok=True)
            if not stat.S_ISDIR(path.stat().st_mode):
                raise NotADirectoryError(f"not a directory: {path}")
        except OSError as exc:
            raise CmocError(
                "作業用配置先を準備・検証できません。",
                [
                    f"配置先 ({path}) と親ディレクトリを確認し、衝突するファイルの退避"
                    "またはディレクトリの作成・参照権限の修正後に再実行してください。"
                ],
                f"work-root: {root}\npath: {path}\nreason: {exc}",
            ) from exc


@contextmanager
def pushd(path: Path) -> Iterator[None]:
    """外部 API が cwd 前提を持つ区間を process-wide に直列化する。"""
    # os.chdir は process-global なので、切替から復元まで lock を保持する。
    with _CMOC_PROCESS_CWD_LOCK:
        previous_cmoc_process_cwd = Path.cwd()
        os.chdir(path)
        try:
            yield
        finally:
            os.chdir(previous_cmoc_process_cwd)


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
