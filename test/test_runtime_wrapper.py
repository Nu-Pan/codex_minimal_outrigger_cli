"""bin/cmoc の仮想環境検査とエラーレポートを検証する。

根拠:
- {{work-root}}/oracle/doc/dev_rule/development_environment.md
- {{work-root}}/oracle/doc/app_spec/error_handling.md
- {{work-root}}/oracle/src/oracle/other/path_model.py
"""

import shutil
import subprocess
from pathlib import Path

import pytest


def test_bin_cmoc_missing_venv_call_stack_uses_root_token_path(tmp_path: Path) -> None:
    """起動 wrapper の missing venv report は root token path で位置を出す。"""
    fake_cmoc_root = tmp_path / "cmoc"
    fake_bin = fake_cmoc_root / "bin"
    fake_bin.mkdir(parents=True)
    shutil.copy2(Path(__file__).parents[1] / "bin" / "cmoc", fake_bin / "cmoc")

    result = subprocess.run(
        ["./bin/cmoc"],
        cwd=fake_cmoc_root,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 1
    assert "## Call stack" in result.stdout
    assert "({{cmoc-root}}/bin/cmoc:" in result.stdout
    assert "(./bin/cmoc:" not in result.stdout
    assert "(bin/cmoc:" not in result.stdout


def test_bin_cmoc_non_file_venv_path_uses_error_report(tmp_path: Path) -> None:
    """通常ファイルでない venv path も wrapper の error report で通知する。"""
    fake_cmoc_root = tmp_path / "cmoc"
    fake_bin = fake_cmoc_root / "bin"
    fake_bin.mkdir(parents=True)
    (fake_cmoc_root / ".venv" / "bin" / "python").mkdir(parents=True)
    shutil.copy2(Path(__file__).parents[1] / "bin" / "cmoc", fake_bin / "cmoc")

    result = subprocess.run(
        ["./bin/cmoc"],
        cwd=fake_cmoc_root,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 1
    assert "# ERROR" in result.stdout
    assert "## Call stack" in result.stdout
    assert result.stderr == ""


@pytest.mark.parametrize("fake_exit_code", [0, 42])
def test_bin_cmoc_non_python_executable_uses_error_report(
    tmp_path: Path, fake_exit_code: int
) -> None:
    """Python として起動できない executable も wrapper の error report で通知する。"""
    fake_cmoc_root = tmp_path / "cmoc"
    fake_bin = fake_cmoc_root / "bin"
    fake_bin.mkdir(parents=True)
    venv_python = fake_cmoc_root / ".venv" / "bin" / "python"
    venv_python.parent.mkdir(parents=True)
    venv_python.write_text(f"#!/bin/sh\nexit {fake_exit_code}\n")
    venv_python.chmod(0o755)
    shutil.copy2(Path(__file__).parents[1] / "bin" / "cmoc", fake_bin / "cmoc")

    result = subprocess.run(
        ["./bin/cmoc"],
        cwd=fake_cmoc_root,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 1
    assert "# ERROR" in result.stdout
    assert "## Call stack" in result.stdout
    assert result.stderr == ""
