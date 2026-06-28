import os
import select
import signal
import time
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path
from typing import NamedTuple

from cmoc_runtime import (
    APPLY_PROCESS_TRACKING_ENV,
    CmocError,
    process_start_time,
    run_git,
    worktrees_dir,
)


class ProcessIdentity(NamedTuple):
    """pid 再利用を避けて process 同一性を確認するための識別子。"""

    process_id: int
    start_time: int | None


class ApplyProcessIdentity(NamedTuple):
    """apply 本体 process と停止対象の Codex child groups を束ねる識別子。"""

    process_id: int
    start_time: int | None
    child_processes: tuple[ProcessIdentity, ...] = ()


def worktree_for_branch(root: Path, branch: str) -> Path:
    """branch が checkout されている linked worktree を返す。"""
    path = worktree_for_branch_optional(root, branch)
    if path is not None:
        return path
    raise CmocError(
        "session branch の worktree を特定できません。",
        ["git worktree list を確認し、session branch の worktree から再実行してください。"],
        f"branch: {branch}",
    )


def expected_apply_worktree(root: Path, apply_branch: str) -> Path:
    """apply branch 命名から対応する managed worktree path を復元する。"""
    parts = apply_branch.split("/")
    if (
        len(parts) != 4
        or parts[:2] != ["cmoc", "apply"]
        or not parts[2]
        or not parts[3]
    ):
        raise CmocError(
            "apply worktree を特定できません。",
            ["session state file の apply.apply_branch を確認してください。"],
            f"apply_branch: {apply_branch}",
        )
    return worktrees_dir(root) / parts[2] / parts[3]


def worktree_for_branch_optional(root: Path, branch: str) -> Path | None:
    """branch が checkout されている linked worktree を返し、無ければ None を返す。"""
    output = run_git(["worktree", "list", "--porcelain"], root).stdout
    current_path: Path | None = None
    for line in output.splitlines():
        if line.startswith("worktree "):
            current_path = Path(line.removeprefix("worktree ")).resolve()
        elif line == f"branch refs/heads/{branch}" and current_path is not None:
            return current_path
    return None


def apply_process_id_path(root: Path, session_id: str) -> Path:
    """session ごとの apply process pid file path を一箇所で決める。"""
    return root / ".cmoc" / "state" / "apply_processes" / f"{session_id}.pid"


def write_apply_process_id(root: Path, session_id: str, process_id: int) -> None:
    """apply abandon が同一 process だけを止められる形で pid file を保存する。"""
    path = apply_process_id_path(root, session_id)
    path.parent.mkdir(parents=True, exist_ok=True)
    start_time = process_start_time(process_id)
    text = (
        f"{process_id} {start_time}\n"
        if start_time is not None
        else f"{process_id}\n"
    )
    path.write_text(text)


@contextmanager
def apply_process_tracking(root: Path, session_id: str) -> Iterator[None]:
    """Codex subprocess 追跡先を apply 実行中だけ環境変数で渡す。"""
    path = apply_process_id_path(root, session_id)
    old_value = os.environ.get(APPLY_PROCESS_TRACKING_ENV)
    os.environ[APPLY_PROCESS_TRACKING_ENV] = str(path)
    try:
        yield
    finally:
        if old_value is None:
            os.environ.pop(APPLY_PROCESS_TRACKING_ENV, None)
        else:
            os.environ[APPLY_PROCESS_TRACKING_ENV] = old_value


def read_apply_process_id(root: Path, session_id: str) -> ApplyProcessIdentity | None:
    """壊れた pid file を停止対象にせず、読める場合だけ識別子を返す。"""
    path = apply_process_id_path(root, session_id)
    if not path.is_file():
        return None
    try:
        lines = [line.split() for line in path.read_text().splitlines() if line.strip()]
        if not lines:
            return None
        parts = lines[0]
        if len(parts) not in {1, 2}:
            return None
        process_id = int(parts[0])
        if process_id <= 0:
            return None
        start_time = int(parts[1]) if len(parts) == 2 else None
        children: list[ProcessIdentity] = []
        for child_parts in lines[1:]:
            if len(child_parts) != 3 or child_parts[0] != "child":
                return None
            child_id = int(child_parts[1])
            if child_id <= 0:
                return None
            children.append(ProcessIdentity(child_id, int(child_parts[2])))
        return ApplyProcessIdentity(process_id, start_time, tuple(children))
    except (IndexError, ValueError):
        return None


def delete_apply_process_id(root: Path, session_id: str) -> None:
    """apply cleanup 後に stale な停止対象を残さないよう pid file を消す。"""
    apply_process_id_path(root, session_id).unlink(missing_ok=True)


def stop_apply_process(process: ApplyProcessIdentity) -> str | None:
    """running abandon では cleanup 前に apply process が消えたことを確認する。"""
    warnings: list[str] = []
    for child in process.child_processes:
        warning = stop_child_process_group(child)
        if warning:
            warnings.append(warning)
    process_id = process.process_id
    if process_id == os.getpid():
        raise CmocError(
            "現在の apply abandon process は停止対象にできません。",
            ["別 process から cmoc apply abandon を実行してください。"],
            f"pid: {process_id}",
        )
    process_fd = open_process_fd(process_id)
    if process_fd is None:
        return f"apply process already stopped: {process_id}"
    try:
        current_start_time = process_start_time(process_id)
        if current_start_time is None and wait_process_fd_exit(process_fd, 0):
            return f"apply process already stopped: {process_id}"
        if process.start_time is None or current_start_time is None:
            raise CmocError(
                "実行中 apply process の同一性を確認できません。",
                ["apply process と pid file を確認し、停止後に再実行してください。"],
                f"pid: {process_id}",
            )
        if current_start_time != process.start_time:
            return f"stale apply process id ignored: {process_id}"
        send_process_signal(process_fd, process_id, signal.SIGTERM)
        if wait_process_fd_exit(process_fd, 5.0):
            return "; ".join(warnings) if warnings else None
        send_process_signal(process_fd, process_id, signal.SIGKILL)
        if wait_process_fd_exit(process_fd, 5.0):
            return "; ".join(warnings) if warnings else None
        raise CmocError(
            "実行中 apply process を停止できません。",
            ["apply process を確認して停止後に再実行してください。"],
            f"pid: {process_id}",
        )
    finally:
        os.close(process_fd)


def stop_child_process_group(process: ProcessIdentity) -> str | None:
    """Codex subprocess を専用 process group 単位で停止する。"""
    process_id = process.process_id
    current_start_time = process_start_time(process_id)
    if current_start_time is None:
        return f"apply child process already stopped: {process_id}"
    if process.start_time is None:
        raise CmocError(
            "実行中 Codex subprocess の同一性を確認できません。",
            ["apply process と pid file を確認し、停止後に再実行してください。"],
            f"pid: {process_id}",
        )
    if current_start_time != process.start_time:
        return f"stale apply child process id ignored: {process_id}"
    try:
        process_group_id = os.getpgid(process_id)
    except ProcessLookupError:
        return f"apply child process already stopped: {process_id}"
    if process_group_id != process_id:
        raise CmocError(
            "実行中 Codex subprocess の process group を確認できません。",
            ["Codex subprocess を手動で停止してから再実行してください。"],
            f"pid: {process_id}\npgid: {process_group_id}",
        )
    # <work-root>/oracle/doc/app_spec/sub_command/apply_abandon.md
    # Codex CLI は apply の実作業なので、親 cmoc process より先に専用 group ごと止める。
    send_process_group_signal(process_group_id, signal.SIGTERM)
    if wait_process_group_exit(process_group_id, 5.0):
        return None
    send_process_group_signal(process_group_id, signal.SIGKILL)
    if wait_process_group_exit(process_group_id, 5.0):
        return None
    raise CmocError(
        "実行中 Codex subprocess を停止できません。",
        ["Codex subprocess を確認して停止後に再実行してください。"],
        f"pid: {process_id}\npgid: {process_group_id}",
    )


def open_process_fd(process_id: int) -> int | None:
    """pidfd 対応環境でだけ race を避けた process 参照を開く。"""
    if not (hasattr(os, "pidfd_open") and hasattr(signal, "pidfd_send_signal")):
        raise CmocError(
            "apply process の同一性を安全に確認できません。",
            ["apply process を手動で停止してから再実行してください。"],
            f"pid: {process_id}",
        )
    try:
        return os.pidfd_open(process_id)
    except ProcessLookupError:
        return None
    except PermissionError as exc:
        raise CmocError(
            "実行中 apply process の確認権限がありません。",
            ["apply process を手動で確認し、停止後に再実行してください。"],
            f"pid: {process_id}",
        ) from exc


def send_process_signal(process_fd: int, process_id: int, sig: signal.Signals) -> None:
    """pidfd 経由で apply process へ signal を送り、権限失敗を cmoc 化する。"""
    try:
        signal.pidfd_send_signal(process_fd, sig)
    except ProcessLookupError:
        return
    except PermissionError as exc:
        raise CmocError(
            "実行中 apply process を停止する権限がありません。",
            ["apply process を手動で停止してから再実行してください。"],
            f"pid: {process_id}",
        ) from exc


def wait_process_fd_exit(process_fd: int, timeout_sec: float) -> bool:
    """pidfd の readable 化を process 終了として待つ。"""
    readable, _, _ = select.select([process_fd], [], [], timeout_sec)
    return bool(readable)


def send_process_group_signal(process_group_id: int, sig: signal.Signals) -> None:
    """Codex subprocess group へ signal を送り、権限失敗を cmoc 化する。"""
    try:
        os.killpg(process_group_id, sig)
    except ProcessLookupError:
        return
    except PermissionError as exc:
        raise CmocError(
            "実行中 Codex subprocess を停止する権限がありません。",
            ["Codex subprocess を手動で停止してから再実行してください。"],
            f"pgid: {process_group_id}",
        ) from exc


def wait_process_group_exit(process_group_id: int, timeout_sec: float) -> bool:
    """process group が消えるまで短い polling で待つ。"""
    deadline = time.monotonic() + timeout_sec
    while True:
        try:
            os.killpg(process_group_id, 0)
        except ProcessLookupError:
            return True
        except PermissionError as exc:
            raise CmocError(
                "実行中 Codex subprocess の確認権限がありません。",
                ["Codex subprocess を手動で確認し、停止後に再実行してください。"],
                f"pgid: {process_group_id}",
            ) from exc
        if time.monotonic() >= deadline:
            return False
        time.sleep(0.05)
