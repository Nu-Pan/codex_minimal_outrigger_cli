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

_WRAPPER_SOURCE = Path(__file__).parents[1] / "bin" / "cmoc"


@pytest.fixture(autouse=True)
def _clear_completion_probe_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    """通常 wrapper 経路のテストから補完プローブ環境を分離する。"""
    monkeypatch.delenv("_CMOC_COMPLETE", raising=False)


def _copy_wrapper(fake_cmoc_root: Path) -> None:
    """テスト用 cmoc root に起動 wrapper を配置する。"""
    fake_bin = fake_cmoc_root / "bin"
    fake_bin.mkdir(parents=True)
    shutil.copy2(_WRAPPER_SOURCE, fake_bin / "cmoc")


def _write_probe_python(fake_cmoc_root: Path) -> None:
    """probe と本番転送を観測できる fake interpreter を作成する。"""
    venv_python = fake_cmoc_root / ".venv" / "bin" / "python"
    venv_python.parent.mkdir(parents=True)
    venv_python.write_text(
        """#!/bin/sh
if [ "$1" = "-c" ]; then
    printf '%s' 'cmoc-python-probe'
    exit 0
fi
printf 'main=%s\n' "$1"
printf 'completion=%s\n' "${_CMOC_COMPLETE-absent}"
shift
printf 'args=%s\n' "$*"
""",
        encoding="utf-8",
    )
    venv_python.chmod(0o755)


def _run_wrapper(fake_cmoc_root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    """テスト用 root の wrapper を指定引数で実行する。"""
    return subprocess.run(
        ["./bin/cmoc", *args],
        cwd=fake_cmoc_root,
        text=True,
        capture_output=True,
        check=False,
    )


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
    _copy_wrapper(fake_cmoc_root)

    result = _run_wrapper(fake_cmoc_root)

    _assert_error_report(result)
    assert str(fake_cmoc_root) in result.stderr
    assert str(fake_cmoc_root / ".venv" / "bin" / "python") in result.stderr


def test_bin_cmoc_non_file_venv_path_uses_error_report(tmp_path: Path) -> None:
    """通常ファイルでない venv path も wrapper の error report で通知する。"""
    fake_cmoc_root = tmp_path / "cmoc"
    (fake_cmoc_root / ".venv" / "bin" / "python").mkdir(parents=True)
    _copy_wrapper(fake_cmoc_root)

    result = _run_wrapper(fake_cmoc_root)

    _assert_error_report(result)


@pytest.mark.parametrize("fake_exit_code", [0, 42])
def test_bin_cmoc_non_python_executable_uses_error_report(
    tmp_path: Path, fake_exit_code: int
) -> None:
    """Python として起動できない executable も wrapper の error report で通知する。"""
    fake_cmoc_root = tmp_path / "cmoc"
    venv_python = fake_cmoc_root / ".venv" / "bin" / "python"
    venv_python.parent.mkdir(parents=True)
    venv_python.write_text(f"#!/bin/sh\nexit {fake_exit_code}\n")
    venv_python.chmod(0o755)
    _copy_wrapper(fake_cmoc_root)

    result = _run_wrapper(fake_cmoc_root)

    _assert_error_report(result)


def test_bin_cmoc_usable_venv_forwards_to_main(tmp_path: Path) -> None:
    """通常経路が probe 後に main.py と引数を interpreter へ渡す。"""
    fake_cmoc_root = tmp_path / "cmoc"
    _write_probe_python(fake_cmoc_root)
    _copy_wrapper(fake_cmoc_root)

    result = _run_wrapper(fake_cmoc_root, "--status")

    assert result.returncode == 0
    assert result.stderr == ""
    assert result.stdout == (
        f"main={fake_cmoc_root / 'src' / 'main.py'}\ncompletion=absent\nargs=--status\n"
    )


def test_bin_cmoc_completion_probe_forwards_without_wrapper_output(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """補完プローブが通常経路の error report を出さずに転送する。"""
    fake_cmoc_root = tmp_path / "cmoc"
    _write_probe_python(fake_cmoc_root)
    _copy_wrapper(fake_cmoc_root)
    monkeypatch.setenv("_CMOC_COMPLETE", "bash_complete")

    result = _run_wrapper(fake_cmoc_root, "--completion-arg")

    assert result.returncode == 0
    assert result.stderr == ""
    assert result.stdout == (
        f"main={fake_cmoc_root / 'src' / 'main.py'}\n"
        "completion=bash_complete\n"
        "args=--completion-arg\n"
    )


def test_bin_cmoc_completion_probe_suppresses_missing_venv_error(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """補完プローブは venv 欠損時も cmoc 形式の報告を出さない。"""
    fake_cmoc_root = tmp_path / "cmoc"
    _copy_wrapper(fake_cmoc_root)
    monkeypatch.setenv("_CMOC_COMPLETE", "bash_complete")

    result = _run_wrapper(fake_cmoc_root)

    assert result.returncode == 1
    assert result.stdout == ""
    assert result.stderr == ""
