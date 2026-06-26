import os
import select
import signal
from pathlib import Path
from typing import NamedTuple

from cmoc_runtime import CmocError, run_git, worktrees_dir


class ApplyProcessIdentity(NamedTuple):
    process_id: int
    start_time: int | None


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
    return root / ".cmoc" / "state" / "apply_processes" / f"{session_id}.pid"


def write_apply_process_id(root: Path, session_id: str, process_id: int) -> None:
    path = apply_process_id_path(root, session_id)
    path.parent.mkdir(parents=True, exist_ok=True)
    start_time = process_start_time(process_id)
    text = (
        f"{process_id} {start_time}\n"
        if start_time is not None
        else f"{process_id}\n"
    )
    path.write_text(text)


def read_apply_process_id(root: Path, session_id: str) -> ApplyProcessIdentity | None:
    path = apply_process_id_path(root, session_id)
    if not path.is_file():
        return None
    try:
        parts = path.read_text().split()
        if len(parts) not in {1, 2}:
            return None
        process_id = int(parts[0])
        if process_id <= 0:
            return None
        start_time = int(parts[1]) if len(parts) == 2 else None
        return ApplyProcessIdentity(process_id, start_time)
    except (IndexError, ValueError):
        return None


def delete_apply_process_id(root: Path, session_id: str) -> None:
    apply_process_id_path(root, session_id).unlink(missing_ok=True)


def stop_apply_process(process: ApplyProcessIdentity) -> str | None:
    """running abandon では cleanup 前に apply process が消えたことを確認する。"""
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
            return None
        send_process_signal(process_fd, process_id, signal.SIGKILL)
        if wait_process_fd_exit(process_fd, 5.0):
            return None
        raise CmocError(
            "実行中 apply process を停止できません。",
            ["apply process を確認して停止後に再実行してください。"],
            f"pid: {process_id}",
        )
    finally:
        os.close(process_fd)


def process_start_time(process_id: int) -> int | None:
    try:
        stat = Path(f"/proc/{process_id}/stat").read_text()
    except OSError:
        return None
    try:
        return int(stat.rsplit(") ", 1)[1].split()[19])
    except (IndexError, ValueError):
        return None


def open_process_fd(process_id: int) -> int | None:
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
    readable, _, _ = select.select([process_fd], [], [], timeout_sec)
    return bool(readable)
