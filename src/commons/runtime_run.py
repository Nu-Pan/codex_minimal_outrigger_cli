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
from commons.runtime_git import expected_run_worktree, run_git
from commons.runtime_paths import generated_agent_read_dir


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
                # run worktree は managed path そのものに限定し、symlink 経由で
                # run-root 外へ解決される登録を受け入れない。
                if registered_path != expected or resolved_path != expected:
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
        if start_time is not None and start_time < 0:
            return None
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
    except (IndexError, OSError, UnicodeError, ValueError):
        return None


def read_run_process_id(root: Path, session_id: str) -> RunProcessIdentity | None:
    """読める場合だけ保存済み run process identity を返す。"""
    path = run_process_id_path(root, session_id)
    with run_process_id_file_lock(path):
        return _read_run_process_id_file(path)


def _run_process_tracking_present(root: Path, session_id: str) -> bool:
    """tracking path に読み取れない file entry が残っているか返す。"""
    path = run_process_id_path(root, session_id)
    return path.exists() or path.is_symlink()


def _invalid_run_process_tracking_error(root: Path, session_id: str) -> CmocError:
    """破損した tracking を停止対象なしとして扱わないための error を作る。"""
    # {{work-root}}/oracle/doc/app_spec/sub_command/editing_run.md
    return CmocError(
        "run process tracking を検証できません。",
        ["tracking file を確認してから再実行してください。"],
        str(run_process_id_path(root, session_id)),
    )


def delete_run_process_id(root: Path, session_id: str) -> None:
    """Codex group が空なら editing run の tracking file を削除する。"""
    path = run_process_id_path(root, session_id)
    with run_process_id_file_lock(path):
        process = _read_run_process_id_file(path)
        if process is None:
            # {{work-root}}/oracle/doc/app_spec/sub_command/editing_run.md
            # unreadable tracking は停止対象を検証できない状態なので、error cleanup
            # が証跡を消して live process を見失わないよう fail closed に保つ。
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


def stop_error_run_process(root: Path, session_id: str) -> tuple[bool, str | None]:
    """error state の残存 process を停止し、tracking を整理する。

    根拠: {{work-root}}/oracle/doc/app_spec/sub_command/editing_run.md
    """
    process = read_run_process_id(root, session_id)
    if process is None:
        if _run_process_tracking_present(root, session_id):
            raise _invalid_run_process_tracking_error(root, session_id)
        delete_run_process_id(root, session_id)
        return False, "run process tracking was absent or stale"
    warning = stop_run_process(
        process,
        lambda: read_run_process_id(root, session_id),
    )
    delete_run_process_id(root, session_id)
    return True, warning


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
            if current_start_time is None:
                # {{work-root}}/oracle/doc/app_spec/sub_command/editing_run.md
                # pidfd が開けても leader の stat を読めない場合は、終了済みでも
                # 数値 PGID だけで停止すると別 process group を巻き込むため fail closed にする。
                if wait_process_fd_exit(
                    process_fd, 0
                ) and not process_group_has_running_member(process_group_id):
                    return f"run child process already stopped: {process.process_id}"
                raise CmocError(
                    "実行中 Codex subprocess の同一性を確認できません。",
                    ["run process を確認し、停止後に再実行してください。"],
                    f"pid: {process.process_id}\npgid: {process_group_id}",
                )
            else:
                if process.start_time is None:
                    raise CmocError(
                        "実行中 Codex subprocess の同一性を確認できません。",
                        ["run process を確認し、停止後に再実行してください。"],
                        f"pid: {process.process_id}",
                    )
                if current_start_time != process.start_time:
                    return _stale_child_process_warning(process, process_group_id)
            # {{work-root}}/oracle/doc/app_spec/sub_command/editing_run.md
            # run_tracked_codex_subprocess は start_new_session child の PID を PGID として
            # 保存するため、停止完了まで pidfd を保持して leader/PGID の再利用による
            # 別 process group への signal を防ぐ。
            if current_start_time == process.start_time:
                stop_process_group(
                    process_group_id,
                    expected_leader=(process.process_id, process.start_time),
                )
                return None
        finally:
            os.close(process_fd)
    else:
        current_start_time = process_start_time(process.process_id)
        if current_start_time is None:
            if not process_group_has_running_member(process_group_id):
                return f"run child process already stopped: {process.process_id}"
            # {{work-root}}/oracle/doc/app_spec/sub_command/editing_run.md
            # leader が消えた後に PGID だけで停止すると、再利用された PGID の別 group
            # へ signal を送るため、対応関係を確認できない場合は fail closed にする。
            raise CmocError(
                "実行中 Codex subprocess の同一性を確認できません。",
                ["run process を確認し、停止後に再実行してください。"],
                f"pid: {process.process_id}\npgid: {process_group_id}",
            )
        if process.start_time is None:
            raise CmocError(
                "実行中 Codex subprocess の同一性を確認できません。",
                ["run process を確認し、停止後に再実行してください。"],
                f"pid: {process.process_id}\npgid: {process_group_id}",
            )
        if current_start_time != process.start_time:
            return _stale_child_process_warning(process, process_group_id)
    stop_process_group(
        process_group_id,
        expected_leader=(process.process_id, process.start_time),
    )
    return None


def _stale_child_process_warning(
    process: ProcessIdentity, process_group_id: int
) -> str:
    """stale leader 後も process group が残る場合は cleanup を止める。"""
    if process_group_has_running_member(process_group_id):
        # {{work-root}}/oracle/doc/app_spec/sub_command/editing_run.md
        # leader の PID 再利用後に group の対応を確認できないまま cleanup すると、
        # run の descendant または別 process group を残したまま worktree を破棄する。
        raise CmocError(
            "実行中 Codex subprocess の同一性を確認できません。",
            ["run process を確認し、停止後に再実行してください。"],
            f"pid: {process.process_id}\npgid: {process_group_id}",
        )
    return f"stale run child process id ignored: {process.process_id}"


def stop_tracked_codex_children(root: Path, session_id: str) -> list[str]:
    """追跡中の Codex child group を停止する。"""
    # {{work-root}}/oracle/doc/app_spec/sub_command/editing_run.md
    # run の cleanup 前に tracking された child を停止し、error 後も実行中 process が
    # worktree を変更し続ける状態を残さない。
    tracked = read_run_process_id(root, session_id)
    if tracked is None:
        if _run_process_tracking_present(root, session_id):
            raise _invalid_run_process_tracking_error(root, session_id)
        return []
    warnings: list[str] = []
    for child in tracked.child_processes:
        if warning := stop_child_process_group(child):
            warnings.append(warning)
    return warnings
