"""Codex JSONL の異常系と CLI 不在時のログを検証する。

対応する正本:
    {{work-root}}/oracle/doc/app_spec/codex_exec_rule.md
    {{work-root}}/oracle/doc/app_spec/console_and_file_log.md
"""

import json
import subprocess
from pathlib import Path

import cmoc_runtime
import pytest
from cmoc_runtime import CmocError
from config.cmoc_config import CmocConfig
from _codex_support import codex_parameter, setup_codex_home, stub_codex_overrides
from _command_support import write_python_executable
from _git_support import make_repo
from commons.runtime_codex_profile import (
    codex_error_text,
    extract_resume_token,
    is_unexpected_error,
)
from commons.runtime_codex import run_codex_exec
from commons.runtime_logging import (
    SubcommandLogger,
    reset_current_subcommand_logger,
    set_current_subcommand_logger,
)


@pytest.mark.parametrize("line", ["null", "[]", "1"])
def test_codex_jsonl_non_object_events_are_unexpected(line: str) -> None:
    """非 object event を parser 境界で安全に malformed error として扱う。"""
    assert "malformed JSONL event" in codex_error_text(line, "")
    assert extract_resume_token(line) is None
    assert is_unexpected_error(line)


@pytest.mark.parametrize("stdout_text", ["not-json", "{}\n\n"])
def test_codex_jsonl_invalid_lines_are_unexpected(stdout_text: str) -> None:
    """不正 JSON と空行を JSONL protocol failure として分類する。"""
    assert is_unexpected_error(stdout_text)
    assert "malformed JSONL event (invalid JSON):" in codex_error_text(
        stdout_text, ""
    )


def test_codex_runtime_rejects_non_object_jsonl_event(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """非 object JSONL でも AttributeError ではなく CmocError にする。"""
    root = make_repo(tmp_path)
    setup_codex_home(tmp_path, monkeypatch)
    stub_codex_overrides(monkeypatch)
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    fake_codex = bin_dir / "codex"
    write_python_executable(
        fake_codex,
        ["print('null')"],
    )
    monkeypatch.setenv("PATH", f"{bin_dir}:{Path('/usr/bin')}")

    with pytest.raises(CmocError) as exc_info:
        run_codex_exec(
            codex_parameter(),
            root=root,
            capacity_initial_sleep_sec=0,
            config=CmocConfig(),
        )

    assert "malformed JSONL event (expected object): null" not in exc_info.value.detail


def test_codex_runtime_rejects_invalid_jsonl_with_zero_returncode_and_valid_output(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """returncode 0 と valid output があっても不正 stdout は失敗にする。"""
    root = make_repo(tmp_path)
    setup_codex_home(tmp_path, monkeypatch)
    stub_codex_overrides(monkeypatch)
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    write_python_executable(
        bin_dir / "codex",
        [
            "import json, pathlib",
            "import sys",
            "args = sys.argv[1:]",
            "output = pathlib.Path(args[args.index('--output-last-message') + 1])",
            "output.write_text(json.dumps({'ok': True}))",
            "print('not-json')",
        ],
    )
    monkeypatch.setenv("PATH", f"{bin_dir}:{Path('/usr/bin')}")

    with pytest.raises(CmocError) as exc_info:
        run_codex_exec(
            codex_parameter(),
            root=root,
            capacity_initial_sleep_sec=0,
            config=CmocConfig(),
        )

    assert "malformed JSONL event (invalid JSON): not-json" not in exc_info.value.detail


def test_codex_runtime_reports_missing_codex_cli(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Codex CLI 不在時の例外と失敗ログを検証する。"""
    root = make_repo(tmp_path)
    setup_codex_home(tmp_path, monkeypatch)
    stub_codex_overrides(monkeypatch)
    real_run = subprocess.run

    def fake_run(args: list[str], *pos: object, **kwargs: object) -> object:
        """Codex CLI の不在を再現し、それ以外の subprocess 呼び出しを委譲する。"""
        if args[:1] == ["codex"]:
            raise FileNotFoundError("codex")
        return real_run(args, *pos, **kwargs)

    monkeypatch.setattr(cmoc_runtime.subprocess, "run", fake_run)

    logger = SubcommandLogger(root, "test")
    token = set_current_subcommand_logger(logger)
    try:
        with pytest.raises(CmocError, match="Codex CLI が見つかりません"):
            run_codex_exec(
                codex_parameter(),
                root=root,
                capacity_initial_sleep_sec=0,
                config=CmocConfig(),
            )
    finally:
        reset_current_subcommand_logger(token)

    events = [json.loads(line) for line in logger.path.read_text().splitlines()]
    codex_events = [event for event in events if event["event"] == "codex_call"]
    assert len(codex_events) == 1
    assert codex_events[0]["status"] == "failed"
    assert codex_events[0]["returncode"] is None
    assert "Codex CLI が見つかりません" in codex_events[0]["error"]
