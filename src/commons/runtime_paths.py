import os
import threading
import time
from collections.abc import Callable, Iterator
from contextlib import contextmanager
from contextvars import ContextVar
from datetime import datetime
from pathlib import Path

from basic.path_model import RootPathPlaceHolder, resolve_real_path

from .runtime_errors import CmocError

_CWD_LOCK = threading.RLock()
_CWD_OVERRIDE_DEPTH: ContextVar[int] = ContextVar("CWD_OVERRIDE_DEPTH", default=0)


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
    with _CWD_LOCK:
        if root_anchor is None:
            return resolve_real_path(placeholder)
        # {{work-root}}/oracle/doc/dev_rule/coding_rule.md
        # root 探索の起点は file または directory なので、process の cwd と区別する。
        # relative path の解決から root resolver の完了まで process-global cwd を
        # 固定し、別 thread の pushd と起点 path が混線しないようにする。
        resolved_root_anchor = root_anchor.resolve()
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
    return generated_agent_read_dir(root) / "session"


def reports_dir(root: Path, command: str) -> Path:
    """サブコマンド別 report 保存先 directory を返す。"""
    return generated_agent_read_dir(root) / "report" / command


def logs_dir(root: Path) -> Path:
    """サブコマンド log 保存先 directory を返す。"""
    return generated_agent_read_dir(root) / "log" / "sub_command"


def editor_work_dir(root: Path) -> Path:
    """未信頼かつ可変な editor work file の directory を返す。"""
    # {{work-root}}/oracle/doc/app_spec/prompt_editor_input.md
    return root / ".cmoc" / "gu" / "aw" / "editor_input"


def editor_input_log_dir(root: Path) -> Path:
    """入力結果の保存コピーと完全 prompt の directory を返す。"""
    # {{work-root}}/oracle/doc/app_spec/prompt_editor_input.md
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
    return _tracked_agent_read_dir(root) / "config.json"


def refactor_state_path(root: Path) -> Path:
    """realization refactor の追跡 state 保存 path を返す。"""
    # {{work-root}}/oracle/doc/app_spec/sub_command/realization_refactor.md
    return _tracked_agent_read_dir(root) / "realization" / "refactor" / "state.json"


def generated_agent_read_dir(root: Path) -> Path:
    """git 非追跡かつ agent 読み取り専用の runtime directory を返す。"""
    # {{work-root}}/oracle/doc/app_spec/run_isolation.md
    return root / ".cmoc" / "gu" / "ar"


def _tracked_agent_read_dir(root: Path) -> Path:
    """git 追跡かつ agent 読み取り専用の設定 directory を返す。"""
    # {{work-root}}/oracle/src/oracle/other/cmoc_config.py
    return root / ".cmoc" / "gt" / "ar"


def is_root_memo(root: Path, path: Path) -> bool:
    """`{{work-root}}/memo` 自体またはその配下か判定する。"""
    # {{work-root}}/oracle/doc/app_spec/indexing.md
    # memo の判定は repository 上の path 境界で行い、symlink の実体へ追跡しない。
    # abspath は symlink を解決せずに `.`/`..` だけを正規化するため、memo/../path
    # を memo 配下と誤認しない。
    memo = Path(os.path.abspath(root / "memo"))
    candidate = Path(os.path.abspath(path))
    return candidate == memo or memo in candidate.parents


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
