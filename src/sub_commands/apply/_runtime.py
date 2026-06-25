import os
import signal
import time
from pathlib import Path

from cmoc_runtime import CmocError, run_git, worktrees_dir


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
    path.write_text(f"{process_id}\n")


def read_apply_process_id(root: Path, session_id: str) -> int | None:
    path = apply_process_id_path(root, session_id)
    if not path.is_file():
        return None
    try:
        return int(path.read_text().strip())
    except ValueError:
        return None


def delete_apply_process_id(root: Path, session_id: str) -> None:
    apply_process_id_path(root, session_id).unlink(missing_ok=True)


def stop_apply_process(process_id: int) -> str | None:
    """running abandon では cleanup 前に apply process が消えたことを確認する。"""
    if process_id == os.getpid():
        raise CmocError(
            "現在の apply abandon process は停止対象にできません。",
            ["別 process から cmoc apply abandon を実行してください。"],
            f"pid: {process_id}",
        )
    if not process_exists(process_id):
        return f"apply process already stopped: {process_id}"
    os.kill(process_id, signal.SIGTERM)
    if wait_process_exit(process_id, 5.0):
        return None
    os.kill(process_id, signal.SIGKILL)
    if wait_process_exit(process_id, 5.0):
        return None
    raise CmocError(
        "実行中 apply process を停止できません。",
        ["apply process を確認して停止後に再実行してください。"],
        f"pid: {process_id}",
    )


def wait_process_exit(process_id: int, timeout_sec: float) -> bool:
    deadline = time.monotonic() + timeout_sec
    while time.monotonic() < deadline:
        if not process_exists(process_id):
            return True
        time.sleep(0.1)
    return not process_exists(process_id)


def process_exists(process_id: int) -> bool:
    if process_id <= 0:
        return False
    try:
        os.kill(process_id, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    return True
