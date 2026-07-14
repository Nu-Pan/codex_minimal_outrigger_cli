import os
import signal
from collections.abc import Callable, Iterator
from contextlib import contextmanager
from pathlib import Path
from typing import NamedTuple

from cmoc_runtime import (
    APPLY_PROCESS_TRACKING_ENV,
    CmocError,
    apply_process_id_file_lock,
    open_process_fd,
    process_group_has_running_member,
    process_start_time,
    run_git,
    send_process_signal,
    set_apply_process_tracking_path,
    stop_process_group,
    wait_process_fd_exit,
    worktrees_dir,
)


class ProcessIdentity(NamedTuple):
    """pid 再利用を避けて process 同一性を確認するための識別子。"""

    process_id: int
    start_time: int | None
    process_group_id: int | None = None


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
    return root / ".cmoc" / "local" / "state" / "apply_processes" / f"{session_id}.pid"


@contextmanager
def apply_run_lock(root: Path, session_id: str) -> Iterator[None]:
    """apply state の公開と abandon cleanup を同じ run 単位で直列化する。"""
    # <work-root>/oracle/doc/app_spec/sub_command/apply_abandon.md
    # PID tracking は Codex child 起動中にも取得するため、lifecycle lock は別鍵にする。
    lock_key = apply_process_id_path(root, session_id).with_name(f"{session_id}.run")
    with apply_process_id_file_lock(lock_key):
        yield


def write_apply_process_id(root: Path, session_id: str, process_id: int) -> None:
    """apply abandon が同一 process だけを止められる形で pid file を保存する。"""
    path = apply_process_id_path(root, session_id)
    with apply_process_id_file_lock(path):
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
    """Codex subprocess 追跡先を apply 実行中だけ有効化する。"""
    path = apply_process_id_path(root, session_id)
    old_value = os.environ.get(APPLY_PROCESS_TRACKING_ENV)
    # <work-root>/oracle/doc/app_spec/sub_command/apply_abandon.md
    # Env is restored for compatibility, but the active tracking decision stays
    # process-local so a parent shell cannot force unrelated Codex calls into it.
    old_tracking_path = set_apply_process_tracking_path(path)
    os.environ[APPLY_PROCESS_TRACKING_ENV] = str(path)
    try:
        yield
    finally:
        set_apply_process_tracking_path(old_tracking_path)
        if old_value is None:
            os.environ.pop(APPLY_PROCESS_TRACKING_ENV, None)
        else:
            os.environ[APPLY_PROCESS_TRACKING_ENV] = old_value


def _read_apply_process_id_file(path: Path) -> ApplyProcessIdentity | None:
    if not path.is_file():
        return None
    try:
        lines = [
            line.split() for line in path.read_text().splitlines() if line.strip()
        ]
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
            if len(child_parts) not in {3, 4} or child_parts[0] != "child":
                return None
            child_id = int(child_parts[1])
            child_start_time = int(child_parts[2])
            if child_id <= 0 or child_start_time < 0:
                return None
            group_id = int(child_parts[3]) if len(child_parts) == 4 else None
            if group_id is not None and group_id <= 0:
                return None
            children.append(ProcessIdentity(child_id, child_start_time, group_id))
        return ApplyProcessIdentity(process_id, start_time, tuple(children))
    except (IndexError, OSError, ValueError):
        return None


def read_apply_process_id(root: Path, session_id: str) -> ApplyProcessIdentity | None:
    """壊れた pid file を停止対象にせず、読める場合だけ識別子を返す。"""
    path = apply_process_id_path(root, session_id)
    with apply_process_id_file_lock(path):
        return _read_apply_process_id_file(path)


def delete_apply_process_id(root: Path, session_id: str) -> None:
    """Codex group が空になるまで stale tracking を残して cleanup 競合を防ぐ。"""
    path = apply_process_id_path(root, session_id)
    with apply_process_id_file_lock(path):
        process = _read_apply_process_id_file(path)
        if process is None:
            return
        if any(
            process_group_has_running_member(
                child.process_group_id or child.process_id
            )
            for child in process.child_processes
        ):
            return
        path.unlink(missing_ok=True)


def stop_apply_process(
    process: ApplyProcessIdentity,
    read_after_parent_exit: Callable[[], ApplyProcessIdentity | None] | None = None,
) -> str | None:
    """abandon では cleanup 前に apply process が消えたことを確認する。"""
    warnings: list[str] = []

    def joined_warnings(*extra: str) -> str | None:
        combined = [*warnings, *extra]
        return "; ".join(combined) if combined else None

    process_id = process.process_id
    if process_id == os.getpid():
        raise CmocError(
            "現在の apply abandon process は停止対象にできません。",
            ["別 process から cmoc apply abandon を実行してください。"],
            f"pid: {process_id}",
        )
    parent_warning = _stop_parent_apply_process(process)
    if parent_warning:
        warnings.append(parent_warning)

    # <work-root>/oracle/doc/app_spec/sub_command/apply_abandon.md
    # 親 apply process の終了後に pid file を読み直す。親が snapshot 取得後に
    # start_new_session=True の Codex child を増やしても cleanup 前に止めるため。
    child_source = read_after_parent_exit() if read_after_parent_exit else process
    child_processes = (
        child_source.child_processes if child_source else process.child_processes
    )
    for child in child_processes:
        warning = stop_child_process_group(child)
        if warning:
            warnings.append(warning)
    return joined_warnings()


def _stop_parent_apply_process(process: ApplyProcessIdentity) -> str | None:
    process_id = process.process_id
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


def stop_child_process_group(process: ProcessIdentity) -> str | None:
    """Codex group を安定した group ID と個別 pidfd で停止する。"""
    # <work-root>/oracle/doc/app_spec/sub_command/apply_abandon.md
    # leader 終了後も数値 PID/PGID の再取得をせず、保存済み group を member pidfd で止める。
    process_id = process.process_id
    process_group_id = process.process_group_id or process_id
    process_fd = open_process_fd(process_id, "Codex subprocess")
    if process_fd is not None:
        try:
            current_start_time = process_start_time(process_id)
            if current_start_time is not None:
                if process.start_time is None:
                    raise CmocError(
                        "実行中 Codex subprocess の同一性を確認できません。",
                        ["apply process を確認し、停止後に再実行してください。"],
                        f"pid: {process_id}",
                    )
                if current_start_time != process.start_time:
                    return f"stale apply child process id ignored: {process_id}"
        finally:
            os.close(process_fd)
    else:
        # leader が消えても、保存済み group ID の descendant を cleanup 前に止める。
        current_start_time = process_start_time(process_id)
        if current_start_time is not None and process.start_time is not None:
            if current_start_time != process.start_time:
                return f"stale apply child process id ignored: {process_id}"
        if not process_group_has_running_member(process_group_id):
            return f"apply child process already stopped: {process_id}"
    stop_process_group(process_group_id)
    return None
