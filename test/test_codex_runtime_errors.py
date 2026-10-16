"""Codex JSONL の異常系と CLI 不在時のログを検証する。

対応する正本:
    {{work-root}}/oracle/doc/app_spec/codex_exec_rule.md
    {{work-root}}/oracle/doc/app_spec/console_and_file_log.md
"""

import json
import subprocess
from itertools import count
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock

import pytest
from _codex_support import codex_parameter, setup_codex_home, stub_codex_overrides

import cmoc_runtime
import commons.runtime_codex_exec as exec_module
import commons.runtime_logging as logging_module
from cmoc_runtime import CmocError
from commons.runtime_codex import run_codex_exec
from commons.runtime_codex_profile import (
    classify_codex_call,
    codex_error_text,
    extract_resume_token,
)
from commons.runtime_logging import (
    SubcommandLogger,
    reset_current_subcommand_logger,
    set_current_subcommand_logger,
)
from config.cmoc_config import CmocConfig


@pytest.fixture
def codex_error_directory(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """応答と起動失敗に不要な Git 探索と永続採番を省く。"""
    # 実 Git の cwd・worktree 境界は test_codex_runtime_paths.py に残す。
    root = tmp_path / "repo"
    root.mkdir()
    setup_codex_home(tmp_path, monkeypatch)
    stub_codex_overrides(monkeypatch)
    monkeypatch.setattr(
        exec_module,
        "AgentCallPathContext",
        lambda agent_call_cwd: SimpleNamespace(
            agent_call_cwd=agent_call_cwd, work_root=root, repo_root=root
        ),
    )
    # 採番の永続性は test_runtime_ids.py、実 logger との結合は
    # test_runtime_cli.py と test_codex_runtime_paths.py で検証する。
    ids = count()

    def next_id(_root: Path, prefix: str) -> str:
        """エラー検査に必要な異なる識別子を、DB 書き込みなしで供給する。"""
        return f"{prefix}_{next(ids):06d}_2000-01-01_00-00"

    monkeypatch.setattr(exec_module, "new_id", next_id)
    monkeypatch.setattr(logging_module, "new_id", next_id)
    return root


@pytest.mark.parametrize("line", ["null", "[]", "1"])
def test_codex_jsonl_non_object_events_are_unexpected(line: str) -> None:
    """非 object event を parser 境界で安全に malformed error として扱う。"""
    assert f"malformed JSONL event (expected object): {line}" in codex_error_text(
        line, ""
    )
    assert extract_resume_token(line) is None
    assert classify_codex_call(line, 0) == "failed"


@pytest.mark.parametrize("stdout_text", ["not-json", "{}\n\n"])
def test_codex_jsonl_invalid_lines_are_unexpected(stdout_text: str) -> None:
    """不正 JSON と空行を JSONL protocol failure として分類する。"""
    assert classify_codex_call(stdout_text, 0) == "failed"
    assert "malformed JSONL event (invalid JSON):" in codex_error_text(stdout_text, "")


def test_codex_runtime_rejects_malformed_jsonl(
    codex_error_directory: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """不正 stdout は正常な最終出力があっても失敗させ、本文を log だけに残す。"""
    # JSONL の境界値は上の parser test に集約し、共通の失敗・保存経路を一度検査する。
    # 実 process の argv・stdin・出力取得は test_codex_runtime_exec.py に残す。
    root = codex_error_directory
    stdout_text = "not-json\n"
    output_text = '{"ok": true}'
    expected_error = "malformed JSONL event (invalid JSON): not-json"
    stderr_text = "private stderr\n"

    def fake_codex(
        args: list[str], **_kwargs: object
    ) -> subprocess.CompletedProcess[str]:
        """正常な出力 file を残し、malformed な stdout を返す。"""
        output = Path(args[args.index("--output-last-message") + 1])
        output.write_text(output_text, encoding="utf-8")
        return subprocess.CompletedProcess(args, 0, stdout_text, stderr_text)

    codex_call = Mock(side_effect=fake_codex)
    monkeypatch.setattr(exec_module, "run_codex_subprocess", codex_call)
    logger = SubcommandLogger(root, "test")

    with pytest.raises(CmocError, match="Codex CLI 呼び出しが失敗しました") as exc_info:
        run_codex_exec(
            codex_parameter(agent_call_cwd=root),
            root=root,
            transient_poll_interval_sec=0,
            config=CmocConfig(),
            subcommand_logger=logger,
        )

    codex_call.assert_called_once()
    events = [json.loads(line) for line in logger.path.read_text().splitlines()]
    (event,) = [event for event in events if event["event"] == "codex_call"]
    assert event["status"] == "failed"
    assert event["returncode"] == 0
    assert expected_error in event["error"]
    assert Path(event["stdout_log_path"]).read_text() == stdout_text
    assert Path(event["stderr_log_path"]).read_text() == stderr_text
    assert Path(event["output_path"]).read_text() == output_text
    assert expected_error not in exc_info.value.detail
    assert stderr_text not in exc_info.value.detail
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == ""


def test_codex_runtime_reports_missing_codex_cli(
    codex_error_directory: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Codex CLI 不在時の例外と失敗ログを検証する。"""
    # 不在の変換は実 run_codex_subprocess を通し、OS の起動失敗だけを代替する。
    root = codex_error_directory
    codex_call = Mock(
        side_effect=FileNotFoundError(2, "No such file or directory", "codex")
    )
    monkeypatch.setattr(cmoc_runtime.subprocess, "run", codex_call)

    logger = SubcommandLogger(root, "test")
    token = set_current_subcommand_logger(logger)
    try:
        with pytest.raises(CmocError, match="Codex CLI が見つかりません"):
            run_codex_exec(
                codex_parameter(agent_call_cwd=root),
                root=root,
                transient_poll_interval_sec=0,
                config=CmocConfig(),
            )
    finally:
        reset_current_subcommand_logger(token)

    codex_call.assert_called_once()
    events = [json.loads(line) for line in logger.path.read_text().splitlines()]
    codex_events = [event for event in events if event["event"] == "codex_call"]
    assert len(codex_events) == 1
    assert codex_events[0]["status"] == "failed"
    assert codex_events[0]["returncode"] is None
    assert "Codex CLI が見つかりません" in codex_events[0]["error"]
