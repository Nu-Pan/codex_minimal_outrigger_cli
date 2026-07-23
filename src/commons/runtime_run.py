import os
import signal
from collections.abc import Callable, Iterator
from contextlib import contextmanager
from pathlib import Path
from typing import NamedTuple

from commons.runtime_codex_profile import (
    RUN_PROCESS_TRACKING_ENV,
    open_process_fd,
    process_group_has_running_member,
    process_start_time,
    run_process_id_file_lock,
    send_process_signal,
    set_run_process_tracking_path,
    stop_process_group,
    wait_process_fd_exit,
)
from commons.runtime_errors import CmocError
from commons.runtime_git import main_worktree_root, run_git
from commons.runtime_paths import generated_agent_read_dir, worktrees_dir


class ProcessIdentity(NamedTuple):
    """pid 再利用を避けて process 同一性を確認する識別子。"""

    process_id: int
    start_time: int | None
    process_group_id: int | None = None


class RunProcessIdentity(NamedTuple):
    """editing run 本体と停止対象の Codex child groups を束ねる。"""

    process_id: int
    start_time: int | None
    child_processes: tuple[ProcessIdentity, ...] = ()


def expected_run_worktree(root: Path, run_branch: str) -> Path:
    """run branch 名から managed worktree path を復元する。"""
    parts = run_branch.split("/")
    # {{work-root}}/oracle/doc/branch_model.md
    # dot component は run-root の2階層配置を崩すため、path component として許可しない。
    if (
        len(parts) != 4
        or parts[:2] != ["cmoc", "run"]
        or not parts[2]
        or not parts[3]
        or parts[2] in {".", ".."}
        or parts[3] in {".", ".."}
    ):
        raise CmocError(
            "run worktree を特定できません。",
            ["session state file の run.branch を確認してください。"],
            f"run_branch: {run_branch}",
        )
    return worktrees_dir(main_worktree_root(root)) / parts[2] / parts[3]


def worktree_for_branch(root: Path, branch: str) -> Path:
    """branch が checkout されている worktree を返す。"""
    path = worktree_for_branch_optional(root, branch)
    if path is not None:
        return path
    raise CmocError(
        "branch の worktree を特定できません。",
        ["git worktree list と session state file を確認してください。"],
        f"branch: {branch}",
    )


def worktree_for_branch_optional(root: Path, branch: str) -> Path | None:
    """branch が checkout されている worktree を返し、無ければ None を返す。"""
    output = run_git(["worktree", "list", "--porcelain"], root).stdout
    registered_path: Path | None = None
    resolved_path: Path | None = None
    for line in output.splitlines():
        if line.startswith("worktree "):
            registered_path = Path(line.removeprefix("worktree ")).absolute()
            resolved_path = registered_path.resolve()
        elif line == f"branch refs/heads/{branch}" and resolved_path is not None:
            if branch.startswith("cmoc/run/"):
                # {{work-root}}/oracle/doc/branch_model.md
                expected = expected_run_worktree(root, branch)
                if registered_path != expected or resolved_path != expected.resolve():
                    return None
            return resolved_path
    return None


def run_process_id_path(root: Path, session_id: str) -> Path:
    """session ごとの editing run process tracking path を返す。"""
    return (
        generated_agent_read_dir(root) / "state" / "run_processes" / f"{session_id}.pid"
    )


@contextmanager
def run_lifecycle_lock(root: Path, session_id: str) -> Iterator[None]:
    """run state の公開、join、abandon を session 内で直列化する。"""
    lock_key = run_process_id_path(root, session_id).with_name(f"{session_id}.run")
    with run_process_id_file_lock(lock_key):
        yield


def write_run_process_id(root: Path, session_id: str, process_id: int) -> None:
    """run abandon が同一 process だけを停止できる形で保存する。"""
    path = run_process_id_path(root, session_id)
    with run_process_id_file_lock(path):
        path.parent.mkdir(parents=True, exist_ok=True)
        start_time = process_start_time(process_id)
        text = (
            f"{process_id} {start_time}\n"
            if start_time is not None
            else f"{process_id}\n"
        )
        path.write_text(text, encoding="utf-8")


@contextmanager
def run_process_tracking(root: Path, session_id: str) -> Iterator[None]:
    """Codex subprocess 追跡先を editing run 実行中だけ有効化する。"""
    path = run_process_id_path(root, session_id)
    old_value = os.environ.get(RUN_PROCESS_TRACKING_ENV)
    old_tracking_path = set_run_process_tracking_path(path)
    os.environ[RUN_PROCESS_TRACKING_ENV] = str(path)
    try:
        yield
    finally:
        set_run_process_tracking_path(old_tracking_path)
        if old_value is None:
            os.environ.pop(RUN_PROCESS_TRACKING_ENV, None)
        else:
            os.environ[RUN_PROCESS_TRACKING_ENV] = old_value


def _read_run_process_id_file(path: Path) -> RunProcessIdentity | None:
    """tracking file を検証し、壊れていれば停止対象なしとして返す。"""
    if not path.is_file():
        return None
    try:
        lines = [line.split() for line in path.read_text().splitlines() if line.strip()]
        if not lines or len(lines[0]) not in {1, 2}:
            return None
        process_id = int(lines[0][0])
        if process_id <= 0:
            return None
        start_time = int(lines[0][1]) if len(lines[0]) == 2 else None
        children: list[ProcessIdentity] = []
        for parts in lines[1:]:
            if len(parts) not in {3, 4} or parts[0] != "child":
                return None
            child_id = int(parts[1])
            child_start_time = int(parts[2])
            group_id = int(parts[3]) if len(parts) == 4 else None
            if (
                child_id <= 0
                or child_start_time < 0
                or (group_id is not None and group_id <= 0)
            ):
                return None
            children.append(ProcessIdentity(child_id, child_start_time, group_id))
        return RunProcessIdentity(process_id, start_time, tuple(children))
    except (IndexError, OSError, ValueError):
        return None


def read_run_process_id(root: Path, session_id: str) -> RunProcessIdentity | None:
    """読める場合だけ保存済み run process identity を返す。"""
    path = run_process_id_path(root, session_id)
    with run_process_id_file_lock(path):
        return _read_run_process_id_file(path)


def delete_run_process_id(root: Path, session_id: str) -> None:
    """Codex group が空なら editing run の tracking file を削除する。"""
    path = run_process_id_path(root, session_id)
    with run_process_id_file_lock(path):
        process = _read_run_process_id_file(path)
        if process is None:
            path.unlink(missing_ok=True)
            return
        if any(
            process_group_has_running_member(child.process_group_id or child.process_id)
            for child in process.child_processes
        ):
            return
        path.unlink(missing_ok=True)


def stop_run_process(
    process: RunProcessIdentity,
    read_after_parent_exit: Callable[[], RunProcessIdentity | None] | None = None,
) -> str | None:
    """run process と保存済み Codex child group の停止完了を確認する。"""
    if process.process_id == os.getpid():
        raise CmocError(
            "現在の run abandon process は停止対象にできません。",
            ["別 process から cmoc run abandon を実行してください。"],
            f"pid: {process.process_id}",
        )
    warnings = []
    if warning := _stop_parent_run_process(process):
        warnings.append(warning)
    child_source = read_after_parent_exit() if read_after_parent_exit else process
    children = child_source.child_processes if child_source else process.child_processes
    for child in children:
        if warning := stop_child_process_group(child):
            warnings.append(warning)
    return "; ".join(warnings) if warnings else None


def _stop_parent_run_process(process: RunProcessIdentity) -> str | None:
    """保存済み start time を確認して親 run process を停止する。"""
    process_fd = open_process_fd(process.process_id)
    if process_fd is None:
        return f"run process already stopped: {process.process_id}"
    try:
        current_start_time = process_start_time(process.process_id)
        if current_start_time is None and wait_process_fd_exit(process_fd, 0):
            return f"run process already stopped: {process.process_id}"
        if process.start_time is None or current_start_time is None:
            raise CmocError(
                "実行中 run process の同一性を確認できません。",
                ["run process と tracking file を確認してください。"],
                f"pid: {process.process_id}",
            )
        if current_start_time != process.start_time:
            return f"stale run process id ignored: {process.process_id}"
        send_process_signal(process_fd, process.process_id, signal.SIGTERM)
        if wait_process_fd_exit(process_fd, 5.0):
            return None
        send_process_signal(process_fd, process.process_id, signal.SIGKILL)
        if wait_process_fd_exit(process_fd, 5.0):
            return None
        raise CmocError(
            "実行中 run process を停止できません。",
            ["run process を確認して停止後に再実行してください。"],
            f"pid: {process.process_id}",
        )
    finally:
        os.close(process_fd)


def stop_child_process_group(process: ProcessIdentity) -> str | None:
    """Codex group を保存済み group ID と member pidfd で停止する。"""
    process_group_id = process.process_group_id or process.process_id
    process_fd = open_process_fd(process.process_id, "Codex subprocess")
    if process_fd is not None:
        try:
            current_start_time = process_start_time(process.process_id)
            if current_start_time is not None:
                if process.start_time is None:
                    raise CmocError(
                        "実行中 Codex subprocess の同一性を確認できません。",
                        ["run process を確認し、停止後に再実行してください。"],
                        f"pid: {process.process_id}",
                    )
                if current_start_time != process.start_time:
                    return f"stale run child process id ignored: {process.process_id}"
        finally:
            os.close(process_fd)
    else:
        current_start_time = process_start_time(process.process_id)
        if (
            current_start_time is not None
            and process.start_time is not None
            and current_start_time != process.start_time
        ):
            return f"stale run child process id ignored: {process.process_id}"
        if not process_group_has_running_member(process_group_id):
            return f"run child process already stopped: {process.process_id}"
    stop_process_group(process_group_id)
    return None
