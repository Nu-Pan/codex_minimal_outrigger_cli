import json
import subprocess
from pathlib import Path

import cmoc_runtime
import pytest
from cmoc_runtime import CmocError
from config.cmoc_config import CmocConfig
from _codex_support import codex_parameter, setup_codex_home, stub_codex_overrides
from _git_support import make_repo
from commons.runtime_codex import run_codex_exec
from commons.runtime_logging import (
    SubcommandLogger,
    reset_current_subcommand_logger,
    set_current_subcommand_logger,
)


def test_codex_runtime_reports_missing_codex_cli(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Codex CLI 不在時の例外と失敗ログを検証する。

    対応する正本:
        <work-root>/oracle/doc/app_spec/codex_exec_rule.md
        <work-root>/oracle/doc/app_spec/console_and_file_log.md
    """
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
