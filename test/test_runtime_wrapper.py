"""bin/cmoc の仮想環境検査とエラーレポートを検証する。

根拠:
- {{work-root}}/oracle/doc/dev_rule/development_environment.md
- {{work-root}}/oracle/doc/app_spec/error_handling.md
- {{work-root}}/oracle/doc/app_spec/cli_auto_completion.md
- {{work-root}}/oracle/src/oracle/other/path_model.py
"""

import shutil
import subprocess
from pathlib import Path

import pytest


@pytest.fixture(autouse=True)
def _clear_completion_probe_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    """通常 wrapper 経路のテストから補完プローブ環境を分離する。"""
    monkeypatch.delenv("_CMOC_COMPLETE", raising=False)


def _assert_error_report(result: subprocess.CompletedProcess[str]) -> None:
    """wrapper の失敗が簡潔な error terminal result を stderr に含むことを確認する。"""
    # {{work-root}}/oracle/doc/app_spec/error_handling.md
    report = result.stderr
    assert result.returncode == 1
    assert result.stdout == ""
    assert report.startswith("# 失敗: cmoc\n")
    assert "- 理由:" in report
    assert "- 詳細:" in report
    assert report.count("- 次の操作:") == 1
    assert "- 終了コード: `1`" in report
    assert "Call stack" not in report
    assert "Traceback" not in report


def test_bin_cmoc_missing_venv_reports_full_paths(tmp_path: Path) -> None:
    """起動 wrapper の missing venv result は実際のフルパスを出す。"""
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

    _assert_error_report(result)
    assert str(fake_cmoc_root) in result.stderr
    assert str(fake_cmoc_root / ".venv" / "bin" / "python") in result.stderr


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

    _assert_error_report(result)


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

    _assert_error_report(result)
