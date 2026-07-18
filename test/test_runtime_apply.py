"""apply runtime の process tracking と停止契約を検証する。

CLI を呼ばず、pid file、advisory lock、pidfd、process group の低レベル契約だけを
直接検証する。apply abandon の CLI 外部挙動は `test_apply_abandon_cli.py` に置く。

根拠: {{work-root}}/oracle/doc/app_spec/sub_command/apply_abandon.md
"""

import threading
import time
from multiprocessing import Pipe, Process
from multiprocessing.connection import Connection
from pathlib import Path

import pytest
from _git_support import make_repo, run_git

import commons.runtime_apply as apply_runtime


def hold_apply_process_id_lock(
    path: Path, ready: Connection, release: Connection
) -> None:
    """別 process で advisory lock を保持するテスト用 helper。"""
    from commons.runtime_codex_profile import apply_process_id_file_lock

    with apply_process_id_file_lock(path):
        ready.send(True)
        release.recv()


def test_stop_apply_process_rereads_child_groups_after_parent_exit(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """親終了後の pid file 再読込で後発 Codex child group も止める。"""
    order: list[str] = []

    def fake_stop_child(process: apply_runtime.ProcessIdentity) -> None:
        """停止対象childのPIDを順序付きで記録する。"""
        order.append(f"child:{process.process_id}")

    def fake_send_signal(process_fd: int, process_id: int, sig: int) -> None:
        """親processへ送るsignalを順序付きで記録する。"""
        order.append(f"parent:{process_id}:{sig}")

    monkeypatch.setattr(apply_runtime, "stop_child_process_group", fake_stop_child)
    monkeypatch.setattr(apply_runtime, "open_process_fd", lambda process_id: 10)
    monkeypatch.setattr(apply_runtime, "process_start_time", lambda process_id: 20)
    monkeypatch.setattr(apply_runtime, "send_process_signal", fake_send_signal)
    monkeypatch.setattr(
        apply_runtime, "wait_process_fd_exit", lambda process_fd, timeout: True
    )
    monkeypatch.setattr(apply_runtime.os, "close", lambda process_fd: None)

    warning = apply_runtime.stop_apply_process(
        apply_runtime.ApplyProcessIdentity(
            12345, 20, (apply_runtime.ProcessIdentity(23456, 30),)
        ),
        lambda: apply_runtime.ApplyProcessIdentity(
            12345, 20, (apply_runtime.ProcessIdentity(34567, 40),)
        ),
    )

    assert warning is None
    assert order == [f"parent:12345:{apply_runtime.signal.SIGTERM}", "child:34567"]


def test_stop_apply_process_keeps_child_warning_when_parent_is_stale(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """親 process 側の warning 後も child 停止 warning を破棄しない。"""
    monkeypatch.setattr(
        apply_runtime,
        "stop_child_process_group",
        lambda process: "apply child process already stopped: 23456",
    )
    monkeypatch.setattr(apply_runtime, "open_process_fd", lambda process_id: 10)
    monkeypatch.setattr(apply_runtime, "process_start_time", lambda process_id: 99)
    monkeypatch.setattr(apply_runtime.os, "close", lambda process_fd: None)

    warning = apply_runtime.stop_apply_process(
        apply_runtime.ApplyProcessIdentity(
            12345, 20, (apply_runtime.ProcessIdentity(23456, 30),)
        )
    )

    assert warning == (
        "stale apply process id ignored: 12345; "
        "apply child process already stopped: 23456"
    )


def test_apply_process_tracking_uses_agent_read_runtime_state(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """PID、child tracking、lock を agent-read runtime state に集約する。"""
    root = tmp_path
    path = apply_runtime.apply_process_id_path(root, "session")
    expected = (
        root / ".cmoc" / "gu" / "ar" / "state" / "apply_processes" / "session.pid"
    )
    legacy_directory = root / ".cmoc" / "gu" / "state" / "apply_processes"
    monkeypatch.setattr(apply_runtime, "process_start_time", lambda _pid: 20)
    monkeypatch.delenv(apply_runtime.APPLY_PROCESS_TRACKING_ENV, raising=False)

    assert path == expected
    apply_runtime.write_apply_process_id(root, "session", 12345)
    assert path.read_text() == "12345 20\n"
    assert path.with_name("session.pid.lock").is_file()

    with apply_runtime.apply_process_tracking(root, "session"):
        assert apply_runtime.os.environ[
            apply_runtime.APPLY_PROCESS_TRACKING_ENV
        ] == str(expected)
    with apply_runtime.apply_run_lock(root, "session"):
        assert path.with_name("session.run.lock").is_file()

    apply_runtime.delete_apply_process_id(root, "session")

    assert not path.exists()
    assert path.with_name("session.pid.lock").is_file()
    assert path.with_name("session.run.lock").is_file()
    assert not legacy_directory.exists()


def test_apply_worktree_lookup_rejects_external_registered_path(
    tmp_path: Path,
) -> None:
    """apply branch が管理領域外で checkout されていても採用しない。"""
    root = make_repo(tmp_path)
    external = tmp_path / "external-apply-worktree"
    branch = "cmoc/apply/session/run"
    run_git(root, "worktree", "add", "-b", branch, str(external), "HEAD")

    assert apply_runtime.expected_apply_worktree(external, branch) == (
        root / ".cmoc" / "gu" / "worktree" / "session" / "run"
    )
    assert apply_runtime.worktree_for_branch_optional(root, branch) is None
    assert external.exists()


def test_apply_process_id_reads_tracked_child_processes(tmp_path: Path) -> None:
    """running abandon が親 PID と同時に記録済み Codex child PID を読める。"""
    root = tmp_path
    path = apply_runtime.apply_process_id_path(root, "session")
    path.parent.mkdir(parents=True)
    path.write_text("12345 20\nchild 23456 30 34567\n")

    process = apply_runtime.read_apply_process_id(root, "session")

    assert process == apply_runtime.ApplyProcessIdentity(
        12345, 20, (apply_runtime.ProcessIdentity(23456, 30, 34567),)
    )


def test_apply_process_id_read_waits_for_tracking_lock(tmp_path: Path) -> None:
    """abandon は child pid file 更新中の中間状態を読まない。"""
    root = tmp_path
    path = apply_runtime.apply_process_id_path(root, "session")
    path.parent.mkdir(parents=True)
    path.write_text("12345 20\nchild 23456 30\n")
    ready_parent, ready_child = Pipe()
    release_parent, release_child = Pipe()
    lock_holder = Process(
        target=hold_apply_process_id_lock,
        args=(path, ready_child, release_child),
    )
    result: list[apply_runtime.ApplyProcessIdentity | None] = []
    reader = threading.Thread(
        target=lambda: result.append(
            apply_runtime.read_apply_process_id(root, "session")
        )
    )

    lock_holder.start()
    assert ready_parent.recv() is True
    reader.start()
    time.sleep(0.1)
    assert result == []
    release_parent.send(True)
    reader.join(2)
    lock_holder.join(2)

    assert not reader.is_alive()
    assert not lock_holder.is_alive()
    assert result == [
        apply_runtime.ApplyProcessIdentity(
            12345, 20, (apply_runtime.ProcessIdentity(23456, 30),)
        )
    ]


def test_stop_child_process_group_uses_stable_group_after_leader_exit(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """leader 終了後も保存済み group ID の descendant を停止対象にする。"""
    stopped: list[int] = []

    monkeypatch.setattr(apply_runtime, "open_process_fd", lambda process_id, name: None)
    monkeypatch.setattr(apply_runtime, "process_start_time", lambda process_id: None)
    monkeypatch.setattr(
        apply_runtime,
        "process_group_has_running_member",
        lambda process_group_id: True,
    )
    monkeypatch.setattr(
        apply_runtime,
        "stop_process_group",
        lambda process_group_id: stopped.append(process_group_id),
    )

    warning = apply_runtime.stop_child_process_group(
        apply_runtime.ProcessIdentity(23456, 30, 34567)
    )

    assert warning is None
    assert stopped == [34567]


def test_stop_apply_process_treats_raced_exit_as_stopped(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """SIGTERM 後に先に終了した process を正常停止として扱う。"""
    sent: list[int] = []

    def fake_send_signal(process_fd: int, process_id: int, sig: int) -> None:
        """送信した signal だけを観測し、process 実体には触れない。"""
        sent.append(sig)

    monkeypatch.setattr(apply_runtime, "open_process_fd", lambda process_id: 10)
    monkeypatch.setattr(apply_runtime, "process_start_time", lambda process_id: 20)
    monkeypatch.setattr(apply_runtime, "send_process_signal", fake_send_signal)
    monkeypatch.setattr(
        apply_runtime, "wait_process_fd_exit", lambda process_fd, timeout: True
    )
    monkeypatch.setattr(apply_runtime.os, "close", lambda process_fd: None)

    warning = apply_runtime.stop_apply_process(
        apply_runtime.ApplyProcessIdentity(12345, 20)
    )

    assert warning is None
    assert sent == [apply_runtime.signal.SIGTERM]


def test_send_process_signal_ignores_already_exited_process(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """pidfd signal 時点で終了済みの process を cleanup 失敗にしない。"""

    def fake_pidfd_send_signal(process_fd: int, sig: int) -> None:
        """Linux pidfd API が返す終了済み process の例外だけを再現する。"""
        raise ProcessLookupError

    monkeypatch.setattr(
        apply_runtime.signal, "pidfd_send_signal", fake_pidfd_send_signal
    )

    apply_runtime.send_process_signal(10, 12345, apply_runtime.signal.SIGTERM)


def test_stop_apply_process_does_not_signal_reused_pid(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """保存時と開始時刻が異なる PID reuse では signal を送らない。"""
    sent: list[int] = []

    monkeypatch.setattr(apply_runtime, "open_process_fd", lambda process_id: 10)
    monkeypatch.setattr(apply_runtime, "process_start_time", lambda process_id: 99)
    monkeypatch.setattr(
        apply_runtime,
        "send_process_signal",
        lambda process_fd, process_id, sig: sent.append(sig),
    )
    monkeypatch.setattr(apply_runtime.os, "close", lambda process_fd: None)

    warning = apply_runtime.stop_apply_process(
        apply_runtime.ApplyProcessIdentity(12345, 20)
    )

    assert warning == "stale apply process id ignored: 12345"
    assert sent == []


def test_stop_child_process_group_opens_pidfd_before_identity_check(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """child PID reuse 確認前に pidfd を握り、別 group への signal を避ける。"""
    order: list[str] = []
    stopped: list[int] = []

    def fake_open_process_fd(process_id: int, name: str) -> int:
        """pidfd取得を記録し、固定fdを返す。"""
        order.append(f"open:{process_id}:{name}")
        return 10

    def fake_process_start_time(process_id: int) -> int:
        """固定start timeを返し、identity確認を記録する。"""
        order.append(f"start:{process_id}")
        return 99

    monkeypatch.setattr(apply_runtime, "open_process_fd", fake_open_process_fd)
    monkeypatch.setattr(apply_runtime, "process_start_time", fake_process_start_time)
    monkeypatch.setattr(
        apply_runtime,
        "stop_process_group",
        lambda process_group_id: stopped.append(process_group_id),
    )
    monkeypatch.setattr(apply_runtime.os, "close", lambda process_fd: None)

    warning = apply_runtime.stop_child_process_group(
        apply_runtime.ProcessIdentity(23456, 30)
    )

    assert warning == "stale apply child process id ignored: 23456"
    assert order == ["open:23456:Codex subprocess", "start:23456"]
    assert stopped == []
