"""pytest process と子 process の Windows toast 外部副作用を隔離する。"""

import json
import os
from pathlib import Path

import pytest
from oracle.editor_input_handoff.body import EditorInputHandoffSource

import commons.runtime_windows_toast as runtime_windows_toast
from commons.runtime_editor_input_handoff_protocol import EDITOR_INPUT_SOURCE_ENV


@pytest.fixture(autouse=True)
def _isolate_windows_toast_transport(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """test が利用者の Windows 通知履歴へ toast を残さないようにする。"""
    # {{work-root}}/oracle/doc/app_spec/windows_toast_notification.md
    # subprocess callback も同じ隔離先を使えるよう、PATH に fake transport を置く。
    executable = tmp_path / "toast-bin" / "powershell.exe"
    executable.parent.mkdir()
    executable.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
    executable.chmod(0o755)
    monkeypatch.setenv("PATH", f"{executable.parent}:{os.environ.get('PATH', '')}")
    monkeypatch.setattr(runtime_windows_toast, "_WINDOWS_POWERSHELL", executable)
    monkeypatch.setattr(
        runtime_windows_toast,
        "_run_windows_toast_transport",
        lambda _title, _message: True,
    )


@pytest.fixture
def handoff_source(tmp_path, monkeypatch):
    """実行中の送信側 TUI に結び付いた MCP context を用意する。"""
    source = EditorInputHandoffSource(
        "oracle investigation", "sci_sender", "cdc_sender", tmp_path / "sender.jsonl"
    )
    monkeypatch.setenv(
        EDITOR_INPUT_SOURCE_ENV,
        json.dumps(
            {
                "subcommand": source.subcommand,
                "execution_id": source.execution_id,
                "codex_call_id": source.codex_call_id,
                "sub_command_log_path": str(source.sub_command_log_path),
            }
        ),
    )
    return source
