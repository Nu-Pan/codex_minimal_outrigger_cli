import errno
import os
import signal
from pathlib import Path

import pytest
from _command_support import write_python_executable

import cmoc_runtime
import commons.runtime_codex_profile as runtime_codex_profile
import commons.runtime_run as runtime_run
from commons.runtime_codex_profile import (
    run_codex_subprocess,
    run_tracked_codex_subprocess,
)
from commons.runtime_errors import CmocError


def test_open_process_fd_treats_invalid_pidfd_as_unavailable(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """OS が pidfd を開けない child を停止経路の再検証へ渡す。"""

    def invalid_pidfd(_process_id: int) -> int:
        """production cleanup で観測した pidfd_open の失敗を再現する。"""
        raise OSError(errno.EINVAL, "Invalid argument")

    monkeypatch.setattr(runtime_codex_profile.os, "pidfd_open", invalid_pidfd)

    assert runtime_codex_profile.open_process_fd(123, "Codex subprocess") is None


def test_stop_run_process_does_not_treat_live_process_as_stopped(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """pidfd が使えない live run process を停止済みとして cleanup しない。

    Oracle: {{work-root}}/oracle/doc/app_spec/sub_command/editing_run.md
    """
    process = runtime_run.RunProcessIdentity(123, 456)
    monkeypatch.setattr(runtime_run.os, "getpid", lambda: 999)
    monkeypatch.setattr(runtime_run, "open_process_fd", lambda *_args: None)
    monkeypatch.setattr(runtime_run.os, "kill", lambda _pid, _signal: None)
    monkeypatch.setattr(runtime_run, "process_start_time", lambda _pid: 456)

    with pytest.raises(CmocError, match="安全に停止できません"):
        runtime_run.stop_run_process(process)


def test_tracked_codex_subprocess_records_dedicated_process_group(
    tmp_path: Path,
) -> None:
    """apply cleanup に必要な専用 process group を記録する。

    Oracle: {{work-root}}/oracle/doc/app_spec/sub_command/editing_run.md
    """
    tracking_path = tmp_path / "apply.pid"
    tracking_path.write_text("111 222\n")
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    script = bin_dir / "codex"
    write_python_executable(
        script,
        [
            "import os, pathlib, sys, time",
            "path = pathlib.Path(sys.argv[1])",
            "process_id = os.getpid()",
            "child_prefix = f'child {process_id} '",
            "deadline = time.monotonic() + 3",
            "while True:",
            "    tracking_text = path.read_text()",
            "    lines = tracking_text.splitlines()",
            "    if any(line.startswith(child_prefix) for line in lines):",
            "        break",
            "    if time.monotonic() >= deadline:",
            "        break",
            "    time.sleep(0.01)",
            "print(os.getpid())",
            "print(os.getpgrp())",
            "print(tracking_text, end='')",
        ],
    )

    result = run_tracked_codex_subprocess(
        [str(script), str(tracking_path)],
        tracking_path,
        text=True,
        capture_output=True,
    )

    stdout_lines = result.stdout.splitlines()
    process_id = stdout_lines[0]
    assert stdout_lines[1] == process_id
    assert stdout_lines[2] == "111 222"
    assert stdout_lines[3].startswith(f"child {process_id} ")
    assert tracking_path.read_text() == "111 222\n"


def test_signal_process_group_members_uses_each_member_pidfd(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """group stop は数値 PGID signal ではなく member pidfd を使う。"""
    sent: list[tuple[int, int, signal.Signals, str]] = []
    closed: list[int] = []
    members = ((111, 10), (222, 20))

    monkeypatch.setattr(
        runtime_codex_profile, "process_group_members", lambda _group: members
    )
    monkeypatch.setattr(
        runtime_codex_profile,
        "open_process_fd",
        lambda process_id, _name: process_id + 1000,
    )
    monkeypatch.setattr(
        runtime_codex_profile,
        "process_start_time",
        lambda process_id: {111: 10, 222: 20}[process_id],
    )
    monkeypatch.setattr(
        runtime_codex_profile,
        "send_process_signal",
        lambda fd, process_id, sig, name: sent.append((fd, process_id, sig, name)),
    )
    monkeypatch.setattr(
        runtime_codex_profile.os, "close", lambda process_fd: closed.append(process_fd)
    )

    runtime_codex_profile.signal_process_group_members(333, signal.SIGTERM)

    assert sent == [
        (1111, 111, signal.SIGTERM, "Codex subprocess"),
        (1222, 222, signal.SIGTERM, "Codex subprocess"),
    ]
    assert closed == [1111, 1222]


def test_stop_process_group_rejects_reused_group_before_signal(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """保存済み group member と異なる PGID へ signal を送らない。"""
    sent: list[signal.Signals] = []
    monkeypatch.setattr(
        runtime_codex_profile,
        "process_group_members",
        lambda _group: ((222, 20),),
    )
    monkeypatch.setattr(
        runtime_codex_profile,
        "_signal_process_members",
        lambda _members, sig: sent.append(sig),
    )

    with pytest.raises(CmocError, match="同一性を確認できません"):
        runtime_codex_profile.stop_process_group(111, expected_members=((111, 10),))

    assert sent == []


def test_stop_process_group_rejects_snapshot_without_expected_leader(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """生存中 leader と異なる group snapshot を停止対象にしない。

    Oracle: {{work-root}}/oracle/doc/app_spec/sub_command/editing_run.md
    """
    sent: list[signal.Signals] = []
    monkeypatch.setattr(
        runtime_codex_profile,
        "process_group_members",
        lambda _group: ((222, 20),),
    )
    monkeypatch.setattr(
        runtime_codex_profile,
        "_signal_process_members",
        lambda _members, sig: sent.append(sig),
    )
    monkeypatch.setattr(
        runtime_codex_profile,
        "_wait_tracked_process_group_exit",
        lambda *_args: False,
    )

    with pytest.raises(CmocError, match="同一性を確認できません"):
        runtime_codex_profile.stop_process_group(
            111,
            expected_leader=(111, 10),
            expected_members=((222, 20),),
        )

    assert sent == []


def test_stop_process_group_rejects_empty_snapshot_without_expected_leader(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """leader の証跡がない空 snapshot を停止済みとして扱わない。"""
    sent: list[signal.Signals] = []
    monkeypatch.setattr(
        runtime_codex_profile,
        "process_group_members",
        lambda _group: (),
    )
    monkeypatch.setattr(
        runtime_codex_profile,
        "_signal_process_members",
        lambda _members, sig: sent.append(sig),
    )

    with pytest.raises(CmocError, match="同一性を確認できません"):
        runtime_codex_profile.stop_process_group(
            111,
            expected_leader=(111, 10),
            expected_members=((222, 20),),
        )

    assert sent == []


def test_stop_process_group_accepts_descendant_after_leader_exit(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """検証済み leader が終了しても同じ snapshot の descendant を停止する。"""
    snapshots = iter([((222, 20),), ()])
    sent: list[signal.Signals] = []
    monkeypatch.setattr(
        runtime_codex_profile,
        "process_group_members",
        lambda _group: next(snapshots),
    )
    monkeypatch.setattr(
        runtime_codex_profile,
        "_signal_process_members",
        lambda _members, sig: sent.append(sig),
    )

    runtime_codex_profile.stop_process_group(
        111,
        expected_leader=(111, 10),
        expected_members=((111, 10), (222, 20)),
    )

    assert sent == [signal.SIGTERM]


def test_stop_process_group_rejects_unknown_group_after_signal(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """停止中に未知の member だけが残った group を成功扱いしない。"""
    snapshots = iter([((111, 10),), ((222, 20),)])
    sent: list[signal.Signals] = []
    monkeypatch.setattr(
        runtime_codex_profile,
        "process_group_members",
        lambda _group: next(snapshots),
    )
    monkeypatch.setattr(
        runtime_codex_profile,
        "_signal_process_members",
        lambda _members, sig: sent.append(sig),
    )

    with pytest.raises(CmocError, match="同一性を確認できません"):
        runtime_codex_profile.stop_process_group(111, expected_members=((111, 10),))

    assert sent == [signal.SIGTERM]


def test_stop_process_group_rejects_unknown_group_after_timeout(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """timeout 後に未知の member だけが残った group を成功扱いしない。"""
    snapshots = iter([((111, 10),), ((222, 20),)])
    sent: list[signal.Signals] = []
    monkeypatch.setattr(
        runtime_codex_profile,
        "process_group_members",
        lambda _group: next(snapshots),
    )
    monkeypatch.setattr(
        runtime_codex_profile,
        "_signal_process_members",
        lambda _members, sig: sent.append(sig),
    )
    monkeypatch.setattr(
        runtime_codex_profile,
        "_wait_tracked_process_group_exit",
        lambda *_args: False,
    )

    with pytest.raises(CmocError, match="同一性を確認できません"):
        runtime_codex_profile.stop_process_group(111)

    assert sent == [signal.SIGTERM]


def test_tracked_codex_subprocess_defers_sigterm_until_tracking_is_written(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Popen 後の SIGTERM は child 行の記録後にだけ配信する。"""
    tracking_path = tmp_path / "apply.pid"
    tracking_path.write_text("111 222\n")
    received: list[int] = []
    tracking_at_signal: list[str] = []
    previous_handler = signal.getsignal(signal.SIGTERM)

    def handler(signum: int, _frame: object) -> None:
        """受信時点の tracking を記録する。"""
        received.append(signum)
        tracking_at_signal.append(tracking_path.read_text())

    class ExitedProcess:
        """すでに終了したsubprocessの最小double。"""

        pid = 4321
        returncode = 0

        def communicate(self, _input: object) -> tuple[str, str]:
            """固定stdoutとstderrを返す。"""
            return "ok", ""

        def poll(self) -> int:
            """終了済みreturncodeを返す。"""
            return 0

    process = ExitedProcess()
    signal.signal(signal.SIGTERM, handler)
    try:

        def popen(*_args: object, **_kwargs: object) -> ExitedProcess:
            """SIGTERMを受信した後に終了済みprocessを返す。"""
            signal.raise_signal(signal.SIGTERM)
            return process

        monkeypatch.setattr(runtime_codex_profile.subprocess, "Popen", popen)
        monkeypatch.setattr(
            runtime_codex_profile, "process_start_time", lambda _pid: 333
        )
        monkeypatch.setattr(
            runtime_codex_profile,
            "process_group_has_running_member",
            lambda _group: False,
        )
        result = run_tracked_codex_subprocess(
            ["codex"], tracking_path, text=True, capture_output=True
        )
    finally:
        signal.signal(signal.SIGTERM, previous_handler)

    assert result.stdout == "ok"
    assert received == [signal.SIGTERM]
    assert tracking_at_signal == ["111 222\nchild 4321 333 4321\n"]


def test_tracked_codex_subprocess_redelivers_sigterm_when_startup_fails(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Popen 前の失敗でも保留した SIGTERM を握りつぶさない。"""
    tracking_path = tmp_path / "apply.pid"
    tracking_path.write_text("111 222\n")
    received: list[int] = []
    previous_handler = signal.getsignal(signal.SIGTERM)

    def handler(signum: int, _frame: object) -> None:
        """復元後の handler が保留 signal を受け取ったことを記録する。"""
        received.append(signum)

    def popen(*_args: object, **_kwargs: object) -> object:
        """Popen 前の失敗と同時に SIGTERM を受けた状態を再現する。"""
        signal.raise_signal(signal.SIGTERM)
        raise OSError("startup failed")

    signal.signal(signal.SIGTERM, handler)
    try:
        monkeypatch.setattr(runtime_codex_profile.subprocess, "Popen", popen)
        with pytest.raises(OSError, match="startup failed"):
            run_tracked_codex_subprocess(
                ["codex"], tracking_path, text=True, capture_output=True
            )
    finally:
        signal.signal(signal.SIGTERM, previous_handler)

    assert received == [signal.SIGTERM]


def test_tracked_codex_subprocess_keeps_group_tracking_after_leader_exit(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """leader 終了後に descendant が残る間は child tracking を消さない。"""
    tracking_path = tmp_path / "apply.pid"
    tracking_path.write_text("111 222\n")

    class ExitedProcess:
        """leader終了後もgroup memberが残るsubprocessの最小double。"""

        pid = 4321
        returncode = 0

        def communicate(self, _input: object) -> tuple[str, str]:
            """固定stdoutとstderrを返す。"""
            return "ok", ""

        def poll(self) -> int:
            """leader終了を示すreturncodeを返す。"""
            return 0

    monkeypatch.setattr(
        runtime_codex_profile.subprocess,
        "Popen",
        lambda *_args, **_kwargs: ExitedProcess(),
    )
    monkeypatch.setattr(runtime_codex_profile, "process_start_time", lambda _pid: 333)
    monkeypatch.setattr(
        runtime_codex_profile, "process_group_has_running_member", lambda _group: True
    )

    run_tracked_codex_subprocess(
        ["codex"], tracking_path, text=True, capture_output=True
    )

    assert tracking_path.read_text() == "111 222\nchild 4321 333 4321\n"


def test_tracked_codex_subprocess_keeps_live_child_after_interrupt(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """communicate が中断されても child tracking を保持する。

    Oracle: {{work-root}}/oracle/doc/app_spec/sub_command/editing_run.md
    """
    tracking_path = tmp_path / "apply.pid"
    tracking_path.write_text("111 222\n")

    class InterruptedProcess:
        """communicate 中断後も生存する fake process。

        Oracle: {{work-root}}/oracle/doc/app_spec/sub_command/editing_run.md
        """

        pid = 4321

        def communicate(self, _input: object) -> object:
            """中断された communicate を表すため KeyboardInterrupt を送出する。"""
            raise KeyboardInterrupt

        def poll(self) -> None:
            """fake process が実行中であることを返す。"""
            return None

    process = InterruptedProcess()
    monkeypatch.setattr(
        runtime_codex_profile.subprocess,
        "Popen",
        lambda *_args, **_kwargs: process,
    )
    monkeypatch.setattr(runtime_codex_profile, "process_start_time", lambda _pid: 333)

    with pytest.raises(KeyboardInterrupt):
        run_tracked_codex_subprocess(
            ["codex"], tracking_path, text=True, capture_output=True
        )

    assert tracking_path.read_text() == "111 222\nchild 4321 333 4321\n"


@pytest.mark.parametrize(
    ("tracking_bytes", "expected_error"),
    [
        (b"\xff", UnicodeDecodeError),
        (b"111 222\ninvalid line\n", OSError),
        (b"2147483648\n", OSError),
        (b"111 222\nchild 2147483648 789 2147483648\n", OSError),
        (b"111 222\nchild 789 1011 123\n", OSError),
    ],
)
def test_tracked_codex_subprocess_rejects_invalid_tracking_before_start(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    tracking_bytes: bytes,
    expected_error: type[Exception],
) -> None:
    """壊れた tracking file では child を起動しない。

    Oracle: {{work-root}}/oracle/doc/app_spec/sub_command/editing_run.md
    """
    tracking_path = tmp_path / "apply.pid"
    tracking_path.write_bytes(tracking_bytes)
    started: list[bool] = []

    def popen(*_args: object, **_kwargs: object) -> object:
        """不正 state では subprocess を作成しないことを検証する。"""
        started.append(True)
        raise AssertionError("invalid tracking file must fail before Popen")

    monkeypatch.setattr(
        runtime_codex_profile.subprocess,
        "Popen",
        popen,
    )

    with pytest.raises(expected_error):
        run_tracked_codex_subprocess(
            ["codex"], tracking_path, text=True, capture_output=True
        )

    assert started == []


def test_tracked_codex_subprocess_stops_and_reaps_child_when_tracking_fails(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """child 起動後の tracking 更新失敗でも child を残さない。"""
    tracking_path = tmp_path / "apply.pid"
    tracking_path.write_text("111 222\n")
    stopped: list[
        tuple[
            int,
            tuple[int, int] | None,
            tuple[tuple[int, int], ...] | None,
        ]
    ] = []

    class RunningProcess:
        """tracking 更新失敗後も生存している fake process。"""

        pid = 4321
        returncode: int | None = None

        def poll(self) -> int | None:
            """fake process がまだ動作中であることを返す。"""
            return self.returncode

        def wait(self) -> int:
            """cleanup 後に process を reap したことを記録する。"""
            self.returncode = 0
            return 0

    process = RunningProcess()

    def fail_record(*_args: object, **_kwargs: object) -> None:
        """child 起動後の tracking 更新失敗を再現する。"""
        raise UnicodeDecodeError("utf-8", b"\xff", 0, 1, "invalid")

    monkeypatch.setattr(
        runtime_codex_profile.subprocess,
        "Popen",
        lambda *_args, **_kwargs: process,
    )
    monkeypatch.setattr(
        runtime_codex_profile,
        "_record_tracked_child_process",
        fail_record,
    )
    monkeypatch.setattr(runtime_codex_profile, "process_start_time", lambda _pid: 333)
    monkeypatch.setattr(
        runtime_codex_profile,
        "process_group_members",
        lambda _group: (),
    )
    monkeypatch.setattr(
        runtime_codex_profile,
        "stop_process_group",
        lambda process_group_id, expected_leader=None, expected_members=None: (
            stopped.append((process_group_id, expected_leader, expected_members))
        ),
    )

    with pytest.raises(UnicodeDecodeError):
        run_tracked_codex_subprocess(
            ["codex"], tracking_path, text=True, capture_output=True
        )

    assert stopped == [(4321, (4321, 333), ())]
    assert process.returncode == 0


def test_run_codex_subprocess_ignores_inherited_run_tracking_env(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Codex 起動時に継承した apply tracking を無視する。

    Oracle: {{work-root}}/oracle/doc/app_spec/sub_command/editing_run.md
    """
    tracking_path = tmp_path / "external" / "apply.pid"
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    write_python_executable(bin_dir / "codex", ["print('ok')"])
    monkeypatch.setenv("PATH", f"{bin_dir}:{Path('/usr/bin')}")
    monkeypatch.setenv(cmoc_runtime.RUN_PROCESS_TRACKING_ENV, str(tracking_path))

    monkeypatch.setattr(
        runtime_codex_profile,
        "run_tracked_codex_subprocess",
        lambda *_args, **_kwargs: pytest.fail(
            "inherited tracking env must not activate child tracking"
        ),
    )

    result = run_codex_subprocess(["codex"], text=True, capture_output=True)

    assert result.stdout == "ok\n"
    assert not tracking_path.exists()


def test_run_codex_subprocess_preserves_missing_cwd_error(
    tmp_path: Path,
) -> None:
    """missing cwd を Codex CLI 不在のエラーへ誤変換しない。"""
    missing_cwd = tmp_path / "missing-cwd"

    with pytest.raises(FileNotFoundError) as exc_info:
        run_codex_subprocess(["codex"], cwd=missing_cwd)

    assert Path(exc_info.value.filename) == missing_cwd


def test_stop_child_process_group_stops_group_after_leader_is_gone(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """leader 消滅後も残る専用 group を snapshot 検証付きで停止する。

    Oracle: {{work-root}}/oracle/doc/app_spec/sub_command/editing_run.md
    """
    child = runtime_run.ProcessIdentity(123, 456, 789)
    members = ((222, 20),)
    stopped: list[tuple[int, tuple[tuple[int, int], ...] | None]] = []
    monkeypatch.setattr(runtime_run, "open_process_fd", lambda *_args: None)
    monkeypatch.setattr(runtime_run, "process_start_time", lambda _pid: None)

    monkeypatch.setattr(runtime_run, "process_group_members", lambda _pgid: members)

    def stop_group(
        process_group_id: int,
        *,
        expected_members: tuple[tuple[int, int], ...] | None = None,
    ) -> None:
        """同じ snapshot を確認した停止だけを許可する。"""
        stopped.append((process_group_id, expected_members))

    monkeypatch.setattr(runtime_run, "stop_process_group", stop_group)

    assert runtime_run.stop_child_process_group(child) is None
    assert stopped == [(789, members)]


def test_stop_child_process_group_rejects_current_process(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """壊れた child tracking で cleanup 自身を停止対象にしない。"""
    child = runtime_run.ProcessIdentity(123, 456, 123)
    monkeypatch.setattr(runtime_run.os, "getpid", lambda: 123)

    with pytest.raises(CmocError, match="現在の process は Codex subprocess"):
        runtime_run.stop_child_process_group(child)


@pytest.mark.parametrize("process_fd", [None, 99])
def test_stop_child_process_group_rejects_reused_group_after_leader_exit(
    monkeypatch: pytest.MonkeyPatch,
    process_fd: int | None,
) -> None:
    """leader 消滅後の PGID 再利用を停止前 snapshot で拒否する。"""
    child = runtime_run.ProcessIdentity(123, 456, 789)
    target_snapshots = iter([(), ((222, 20),)])
    reused_members = ((222, 20),)
    signals: list[signal.Signals] = []

    monkeypatch.setattr(
        runtime_run,
        "process_group_members",
        lambda _group: next(target_snapshots),
    )
    monkeypatch.setattr(runtime_run, "open_process_fd", lambda *_args: process_fd)
    monkeypatch.setattr(runtime_run, "process_start_time", lambda _pid: None)
    monkeypatch.setattr(runtime_run, "wait_process_fd_exit", lambda *_args: True)
    monkeypatch.setattr(runtime_run.os, "close", lambda _fd: None)
    monkeypatch.setattr(
        runtime_codex_profile,
        "process_group_members",
        lambda _group: reused_members,
    )
    monkeypatch.setattr(
        runtime_codex_profile,
        "_signal_process_members",
        lambda _members, sig: signals.append(sig),
    )
    monkeypatch.setattr(
        runtime_codex_profile,
        "_wait_tracked_process_group_exit",
        lambda *_args: True,
    )

    with pytest.raises(CmocError, match="同一性を確認できません"):
        runtime_run.stop_child_process_group(child)

    assert signals == []


def test_stop_child_process_group_stops_group_after_pidfd_leader_exit(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """pidfd 経路でも leader 消滅後の専用 group を停止する。"""
    child = runtime_run.ProcessIdentity(123, 456, 789)
    members = ((222, 20),)
    stopped: list[tuple[int, tuple[tuple[int, int], ...] | None]] = []
    closed: list[int] = []
    monkeypatch.setattr(runtime_run, "open_process_fd", lambda *_args: 99)
    monkeypatch.setattr(runtime_run, "process_start_time", lambda _pid: None)
    monkeypatch.setattr(runtime_run, "wait_process_fd_exit", lambda *_args: True)
    monkeypatch.setattr(runtime_run, "process_group_members", lambda _pgid: members)

    def stop_group(
        process_group_id: int,
        *,
        expected_members: tuple[tuple[int, int], ...] | None = None,
    ) -> None:
        """同じ snapshot を確認した停止だけを許可する。"""
        stopped.append((process_group_id, expected_members))

    monkeypatch.setattr(runtime_run, "stop_process_group", stop_group)
    monkeypatch.setattr(runtime_run.os, "close", lambda fd: closed.append(fd))

    assert runtime_run.stop_child_process_group(child) is None
    assert stopped == [(789, members)]
    assert closed == [99]


def test_stop_child_process_group_keeps_leader_pidfd_until_group_stop(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """leader の pidfd を閉じる前に process group を停止する。

    Oracle: {{work-root}}/oracle/doc/app_spec/sub_command/editing_run.md
    """
    child = runtime_run.ProcessIdentity(123, 456, 123)
    events: list[str] = []
    leader_fd_open = False

    def open_fd(*_args: object) -> int:
        """leader の pidfd を開いた状態を記録する。"""
        nonlocal leader_fd_open
        leader_fd_open = True
        events.append("open")
        return 99

    def stop_group(
        process_group_id: int,
        *,
        expected_leader: tuple[int, int] | None = None,
        expected_members: tuple[tuple[int, int], ...] | None = None,
    ) -> None:
        """pidfd 保持中の process group 停止だけを許可する。"""
        assert leader_fd_open
        assert expected_leader == (123, 456)
        assert expected_members == ((123, 456), (222, 20))
        current_members = ((222, 20),)
        assert expected_leader not in current_members
        assert any(member in expected_members for member in current_members)
        events.append(f"stop:{process_group_id}")

    def close_fd(_process_fd: int) -> None:
        """leader の pidfd が閉じたことを記録する。"""
        nonlocal leader_fd_open
        leader_fd_open = False
        events.append("close")

    monkeypatch.setattr(runtime_run, "open_process_fd", open_fd)
    monkeypatch.setattr(runtime_run, "process_start_time", lambda _pid: 456)
    monkeypatch.setattr(
        runtime_run,
        "process_group_members",
        lambda _group: ((123, 456), (222, 20)),
    )
    monkeypatch.setattr(runtime_run, "stop_process_group", stop_group)
    monkeypatch.setattr(runtime_run.os, "close", close_fd)

    assert runtime_run.stop_child_process_group(child) is None
    assert events == ["open", "stop:123", "close"]


@pytest.mark.parametrize("process_fd", [None, 99])
def test_stop_child_process_group_fails_closed_when_live_leader_is_missing(
    monkeypatch: pytest.MonkeyPatch,
    process_fd: int | None,
) -> None:
    """snapshot 欠落時に live leader を停止済みとして扱わない。"""
    child = runtime_run.ProcessIdentity(123, 456, 123)
    stopped: list[int] = []
    monkeypatch.setattr(runtime_run, "process_group_members", lambda _pgid: ())
    monkeypatch.setattr(runtime_run, "open_process_fd", lambda *_args: process_fd)
    monkeypatch.setattr(runtime_run, "process_start_time", lambda _pid: 456)
    monkeypatch.setattr(
        runtime_run,
        "wait_process_fd_exit",
        lambda *_args: False,
    )
    monkeypatch.setattr(
        runtime_run,
        "stop_process_group",
        lambda pgid, **_kwargs: stopped.append(pgid),
    )
    if process_fd is not None:
        monkeypatch.setattr(runtime_run.os, "close", lambda _fd: None)

    with pytest.raises(CmocError, match="同一性を確認できません"):
        runtime_run.stop_child_process_group(child)

    assert stopped == []


def test_read_run_process_id_treats_invalid_encoding_as_stale(
    tmp_path: Path,
) -> None:
    """壊れた encoding の tracking file を停止対象なしとして扱う。"""
    tracking_path = runtime_run.run_process_id_path(tmp_path, "session")
    tracking_path.parent.mkdir(parents=True)
    tracking_path.write_bytes(b"\xff")

    assert runtime_run.read_run_process_id(tmp_path, "session") is None


def test_read_run_process_id_rejects_negative_parent_start_time(
    tmp_path: Path,
) -> None:
    """不正な親 process の start time を停止対象として受け入れない。"""
    tracking_path = runtime_run.run_process_id_path(tmp_path, "session")
    tracking_path.parent.mkdir(parents=True)
    tracking_path.write_text("123 -1\n")

    assert runtime_run.read_run_process_id(tmp_path, "session") is None


@pytest.mark.parametrize(
    "tracking_text",
    [
        f"{2**31}\n",
        f"123 456\nchild {2**31} 789 {2**31}\n",
        "123 456\nchild 789 1011 123\n",
    ],
)
def test_read_run_process_id_rejects_unusable_child_identity(
    tmp_path: Path, tracking_text: str
) -> None:
    """停止対象として扱えない pid と group の組を受け入れない。"""
    tracking_path = runtime_run.run_process_id_path(tmp_path, "session")
    tracking_path.parent.mkdir(parents=True)
    tracking_path.write_text(tracking_text)

    assert runtime_run.read_run_process_id(tmp_path, "session") is None


@pytest.mark.parametrize("path_kind", ["symlink", "fifo"])
def test_run_process_tracking_rejects_external_or_special_path(
    tmp_path: Path, path_kind: str
) -> None:
    """tracking file は管理領域外 symlink と blocking な特殊 file を拒否する。"""
    tracking_path = runtime_run.run_process_id_path(tmp_path, "session")
    tracking_path.parent.mkdir(parents=True)
    outside: Path | None = None
    if path_kind == "symlink":
        outside = tmp_path / "outside.pid"
        outside.write_text("123 456\n", encoding="utf-8")
        tracking_path.symlink_to(outside)
    else:
        if not hasattr(os, "mkfifo"):
            pytest.skip("named pipes are unavailable")
        os.mkfifo(tracking_path)

    with pytest.raises(CmocError, match="run process tracking path"):
        runtime_run.read_run_process_id(tmp_path, "session")
    with pytest.raises(CmocError, match="run process tracking path"):
        runtime_run.write_run_process_id(tmp_path, "session", 123)

    if outside is not None:
        assert outside.read_text(encoding="utf-8") == "123 456\n"


def test_stop_child_process_group_fails_closed_when_stale_leader_group_is_running(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """stale leader の group が残る場合は cleanup を続行しない。"""
    child = runtime_run.ProcessIdentity(123, 456, 789)
    stopped: list[int] = []
    monkeypatch.setattr(runtime_run, "open_process_fd", lambda *_args: None)
    monkeypatch.setattr(runtime_run, "process_start_time", lambda _pid: 999)
    monkeypatch.setattr(
        runtime_run, "process_group_has_running_member", lambda _pgid: True
    )
    monkeypatch.setattr(
        runtime_run, "stop_process_group", lambda pgid: stopped.append(pgid)
    )

    with pytest.raises(CmocError, match="同一性を確認できません"):
        runtime_run.stop_child_process_group(child)

    assert stopped == []
