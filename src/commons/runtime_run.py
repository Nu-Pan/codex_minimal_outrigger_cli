"""editing run の worktree 解決と process cleanup を束ねる共通 runtime 境界。

この module は run state の同一 lock・tracking file・worktree identity を共有する
ため、join/abandon の復旧処理で一緒に読む必要がある。worktree lookup と process
停止を分けると、この不変条件と fail-closed 方針の文脈が分散するため、一つの run
lifecycle 境界として保つ。

根拠:
- {{work-root}}/oracle/doc/app_spec/run_isolation.md
- {{work-root}}/oracle/doc/app_spec/sub_command/editing_run.md
"""

import os
import signal
from collections.abc import Callable, Iterator
from contextlib import contextmanager
from pathlib import Path
from typing import NamedTuple

from .runtime_codex_profile import (
    RUN_PROCESS_TRACKING_ENV,
    _is_valid_process_id,
    open_process_fd,
    process_group_has_running_member,
    process_group_members,
    process_start_time,
    run_process_id_file_lock,
    send_process_signal,
    set_run_process_tracking_path,
    stop_process_group,
    wait_process_fd_exit,
)
from .runtime_errors import CmocError
from .runtime_git import (
    _has_linked_worktree_metadata,
    expected_run_worktree,
    run_git,
)
from .runtime_paths import generated_agent_read_dir


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
                if not registered_path.is_dir() or not _has_linked_worktree_metadata(
                    root, registered_path
                ):
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
    if path.is_symlink() or not path.is_file():
        return None
    try:
        lines = [
            line.split()
            for line in path.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        if not lines or len(lines[0]) not in {1, 2}:
            return None
        process_id = int(lines[0][0])
        if not _is_valid_process_id(process_id):
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
            # {{work-root}}/oracle/doc/app_spec/sub_command/editing_run.md
            # run_tracked_codex_subprocess は start_new_session child の PID を PGID
            # として保存する。別 PGID を受け入れると、leader 消滅後に tracking の
            # stale 値を再利用した別 process group を停止し得る。
            if (
                not _is_valid_process_id(child_id)
                or child_start_time < 0
                or (
                    group_id is not None
                    and (not _is_valid_process_id(group_id) or group_id != child_id)
                )
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
        # {{work-root}}/oracle/doc/app_spec/sub_command/editing_run.md
        # open_process_fd は pidfd_open の EINVAL でも None を返す。live process を
        # already stopped と誤認すると、停止確認前に run worktree を削除してしまうため、
        # kill(pid, 0) と start time の両方で消滅・stale・検証不能を分ける。
        try:
            os.kill(process.process_id, 0)
        except ProcessLookupError:
            return f"run process already stopped: {process.process_id}"
        except OSError as exc:
            raise CmocError(
                "実行中 run process の同一性を確認できません。",
                ["run process と tracking file を確認してください。"],
                f"pid: {process.process_id}\nerror: {exc}",
            ) from exc
        current_start_time = process_start_time(process.process_id)
        if process.start_time is None or current_start_time is None:
            raise CmocError(
                "実行中 run process の同一性を確認できません。",
                ["run process と tracking file を確認してください。"],
                f"pid: {process.process_id}",
            )
        if current_start_time != process.start_time:
            return f"stale run process id ignored: {process.process_id}"
        raise CmocError(
            "実行中 run process を安全に停止できません。",
            ["pidfd を利用できる環境で run process を停止してから再実行してください。"],
            f"pid: {process.process_id}",
        )
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


def _stop_orphaned_child_process_group(
    process: ProcessIdentity,
    process_group_id: int,
    expected_members: tuple[tuple[int, int], ...] | None,
) -> str | None:
    """leader 消滅後も残る group を snapshot 検証付きで停止する。"""
    if expected_members is None:
        raise CmocError(
            "実行中 Codex subprocess の process group を確認できません。",
            ["Codex subprocess を手動で停止してから再実行してください。"],
            f"pid: {process.process_id}\npgid: {process_group_id}",
        )
    members = process_group_members(process_group_id)
    if members is None:
        raise CmocError(
            "実行中 Codex subprocess の process group を確認できません。",
            ["Codex subprocess を手動で停止してから再実行してください。"],
            f"pid: {process.process_id}\npgid: {process_group_id}",
        )
    if not members:
        return f"run child process already stopped: {process.process_id}"
    # {{work-root}}/oracle/doc/app_spec/run_isolation.md
    # leader が消えても member が残る専用 PGID は再利用されない。snapshot の一部を
    # stop_process_group でも確認し、group が一度空になって再利用された race は拒否する。
    stop_process_group(process_group_id, expected_members=expected_members)
    return None


def stop_child_process_group(process: ProcessIdentity) -> str | None:
    """Codex group を保存済み group ID と member pidfd で停止する。"""
    # {{work-root}}/oracle/doc/app_spec/sub_command/editing_run.md
    # tracking が壊れていても cleanup 自身を Codex child として停止しない。
    if process.process_id == os.getpid():
        raise CmocError(
            "現在の process は Codex subprocess の停止対象にできません。",
            ["process tracking と実行中 process を確認してから再実行してください。"],
            f"pid: {process.process_id}",
        )
    process_group_id = process.process_group_id or process.process_id
    # {{work-root}}/oracle/doc/app_spec/sub_command/editing_run.md
    # identity 検証後に leader が終了しても descendant を停止できるよう、停止前の
    # group snapshot を渡す。snapshot と現在 group に重なりがなければ停止側が拒否する。
    expected_members = process_group_members(process_group_id)
    process_fd = open_process_fd(process.process_id, "Codex subprocess")
    if process_fd is not None:
        try:
            current_start_time = process_start_time(process.process_id)
            if current_start_time is None:
                if wait_process_fd_exit(process_fd, 0):
                    return _stop_orphaned_child_process_group(
                        process, process_group_id, expected_members
                    )
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
                # process_group_members は zombie と一時的に読めない process を snapshot
                # から除く。leader が snapshot にいないまま空 group を stop_process_group
                # へ渡すと、live process を停止済みと誤認して cleanup を進め得るため、
                # pidfd で終了を確認できない場合は fail closed にする。
                if (
                    expected_members is None
                    or (process.process_id, process.start_time) not in expected_members
                ):
                    if wait_process_fd_exit(process_fd, 0):
                        return _stop_orphaned_child_process_group(
                            process, process_group_id, expected_members
                        )
                    raise CmocError(
                        "実行中 Codex subprocess の同一性を確認できません。",
                        ["run process を確認し、停止後に再実行してください。"],
                        f"pid: {process.process_id}\npgid: {process_group_id}",
                    )
                stop_process_group(
                    process_group_id,
                    expected_leader=(process.process_id, process.start_time),
                    expected_members=expected_members,
                )
                return None
        finally:
            os.close(process_fd)
    else:
        current_start_time = process_start_time(process.process_id)
        if current_start_time is None:
            return _stop_orphaned_child_process_group(
                process, process_group_id, expected_members
            )
        if process.start_time is None:
            raise CmocError(
                "実行中 Codex subprocess の同一性を確認できません。",
                ["run process を確認し、停止後に再実行してください。"],
                f"pid: {process.process_id}\npgid: {process_group_id}",
            )
        if current_start_time != process.start_time:
            return _stale_child_process_warning(process, process_group_id)
        # pidfd を開けない環境では、leader が snapshot に含まれない理由を終了と
        # 一時的な proc 読み取り欠落から区別できない。停止確認を証明できないまま
        # group cleanup を進めない。
        if (
            expected_members is None
            or (process.process_id, process.start_time) not in expected_members
        ):
            raise CmocError(
                "実行中 Codex subprocess の同一性を確認できません。",
                ["run process を確認し、停止後に再実行してください。"],
                f"pid: {process.process_id}\npgid: {process_group_id}",
            )
    stop_process_group(
        process_group_id,
        expected_leader=(process.process_id, process.start_time),
        expected_members=expected_members,
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
