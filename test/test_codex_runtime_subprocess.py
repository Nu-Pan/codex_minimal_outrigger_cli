from pathlib import Path

import pytest

import cmoc_runtime
from _command_support import write_python_executable
import commons.runtime_codex_profile as runtime_codex_profile
from commons.runtime_codex_profile import (
    run_codex_subprocess,
    run_tracked_codex_subprocess,
)


def test_tracked_codex_subprocess_records_dedicated_process_group(
    tmp_path: Path,
) -> None:
    """Records the dedicated process group needed for apply cleanup.

    Oracle: <work-root>/oracle/doc/app_spec/sub_command/apply_abandon.md
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


def test_tracked_codex_subprocess_keeps_live_child_after_interrupt(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Keeps child tracking when communicate is interrupted.

    Oracle: <work-root>/oracle/doc/app_spec/sub_command/apply_abandon.md
    """
    tracking_path = tmp_path / "apply.pid"
    tracking_path.write_text("111 222\n")

    class InterruptedProcess:
        """Fake process that remains alive after communicate is interrupted.

        Oracle: <work-root>/oracle/doc/app_spec/sub_command/apply_abandon.md
        """

        pid = 4321

        def communicate(self, _input: object) -> object:
            """Raise KeyboardInterrupt to model an interrupted communicate."""
            raise KeyboardInterrupt

        def poll(self) -> None:
            """Report that the fake process is still running."""
            return None

    process = InterruptedProcess()
    monkeypatch.setattr(
        runtime_codex_profile.subprocess,
        "Popen",
        lambda *_args, **_kwargs: process,
    )
    monkeypatch.setattr(
        runtime_codex_profile, "process_start_time", lambda _pid: 333
    )

    with pytest.raises(KeyboardInterrupt):
        run_tracked_codex_subprocess(
            ["codex"], tracking_path, text=True, capture_output=True
        )

    assert tracking_path.read_text() == "111 222\nchild 4321 333\n"


def test_run_codex_subprocess_ignores_inherited_apply_tracking_env(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Ignores inherited apply tracking while launching Codex.

    Oracle: <work-root>/oracle/doc/app_spec/sub_command/apply_abandon.md
    """
    tracking_path = tmp_path / "external" / "apply.pid"
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    write_python_executable(bin_dir / "codex", ["print('ok')"])
    monkeypatch.setenv("PATH", f"{bin_dir}:{Path('/usr/bin')}")
    monkeypatch.setenv(
        cmoc_runtime.APPLY_PROCESS_TRACKING_ENV, str(tracking_path)
    )

    result = run_codex_subprocess(["codex"], text=True, capture_output=True)

    assert result.stdout == "ok\n"
    assert not tracking_path.exists()
