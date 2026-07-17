import signal
from pathlib import Path

import pytest
from _command_support import write_python_executable

import cmoc_runtime
import commons.runtime_codex_profile as runtime_codex_profile
from commons.runtime_codex_profile import (
    run_codex_subprocess,
    run_tracked_codex_subprocess,
)


def test_tracked_codex_subprocess_records_dedicated_process_group(
    tmp_path: Path,
) -> None:
    """apply cleanup に必要な専用 process group を記録する。

    Oracle: {{work-root}}/oracle/doc/app_spec/sub_command/apply_abandon.md
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


def test_tracked_codex_subprocess_defers_sigterm_until_tracking_is_written(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Popen 後の SIGTERM は child 行の記録後にだけ配信する。"""
    tracking_path = tmp_path / "apply.pid"
    tracking_path.write_text("111 222\n")
    received: list[int] = []
    previous_handler = signal.getsignal(signal.SIGTERM)

    def handler(signum: int, _frame: object) -> None:
        """受信したSIGTERMを記録する。"""
        received.append(signum)

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

    Oracle: {{work-root}}/oracle/doc/app_spec/sub_command/apply_abandon.md
    """
    tracking_path = tmp_path / "apply.pid"
    tracking_path.write_text("111 222\n")

    class InterruptedProcess:
        """communicate 中断後も生存する fake process。

        Oracle: {{work-root}}/oracle/doc/app_spec/sub_command/apply_abandon.md
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


def test_run_codex_subprocess_ignores_inherited_apply_tracking_env(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Codex 起動時に継承した apply tracking を無視する。

    Oracle: {{work-root}}/oracle/doc/app_spec/sub_command/apply_abandon.md
    """
    tracking_path = tmp_path / "external" / "apply.pid"
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    write_python_executable(bin_dir / "codex", ["print('ok')"])
    monkeypatch.setenv("PATH", f"{bin_dir}:{Path('/usr/bin')}")
    monkeypatch.setenv(cmoc_runtime.APPLY_PROCESS_TRACKING_ENV, str(tracking_path))

    result = run_codex_subprocess(["codex"], text=True, capture_output=True)

    assert result.stdout == "ok\n"
    assert not tracking_path.exists()
