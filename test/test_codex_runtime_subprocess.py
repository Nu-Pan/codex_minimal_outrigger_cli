import cmoc_runtime
import pytest
from pathlib import Path

from _support import write_python_executable
from commons.runtime_codex_profile import (
    run_codex_subprocess,
    run_tracked_codex_subprocess,
)


def test_tracked_codex_subprocess_records_dedicated_process_group(
    tmp_path: Path,
) -> None:
    tracking_path = tmp_path / "apply.pid"
    tracking_path.write_text("111 222\n")
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    script = bin_dir / "codex"
    write_python_executable(
        script,
        [
            "import os, pathlib, sys, time",
            "time.sleep(0.2)",
            "print(os.getpid())",
            "print(os.getpgrp())",
            "print(pathlib.Path(sys.argv[1]).read_text(), end='')",
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


def test_run_codex_subprocess_ignores_inherited_apply_tracking_env(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    tracking_path = tmp_path / "external" / "apply.pid"
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    write_python_executable(bin_dir / "codex", ["print('ok')"])
    monkeypatch.setenv("PATH", f"{bin_dir}:{Path('/usr/bin')}")
    monkeypatch.setenv(cmoc_runtime.APPLY_PROCESS_TRACKING_ENV, str(tracking_path))

    result = run_codex_subprocess(["codex"], text=True, capture_output=True)

    assert result.stdout == "ok\n"
    assert not tracking_path.exists()


