"""Windows toast の内容、transport、Codex callback 境界を検証する。

根拠: {{work-root}}/oracle/doc/app_spec/windows_toast_notification.md
"""

import base64
import json
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import pytest

import commons.runtime_windows_toast as runtime_windows_toast

_REAL_WINDOWS_TOAST_TRANSPORT = runtime_windows_toast._run_windows_toast_transport


@pytest.mark.parametrize(
    ("state", "state_text"),
    [
        ("completed", "完了"),
        ("failed", "エラー終了"),
        ("interrupted", "ユーザー中断完了"),
    ],
)
def test_terminal_result_uses_only_short_required_fields(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    state: str,
    state_text: str,
) -> None:
    """toast が command、repository、状態だけを一行の短い内容にする。"""
    calls: list[tuple[str, str]] = []
    monkeypatch.setattr(
        runtime_windows_toast,
        "_run_windows_toast_transport",
        lambda title, message: calls.append((title, message)) or True,
    )
    repository = tmp_path / "secret-parent" / "repository\nname"

    runtime_windows_toast.notify_terminal_result(
        "oracle\treview",
        repository,
        state,
    )

    assert calls == [("cmoc oracle review", f"repository name — {state_text}")]
    rendered = "\n".join(calls[0])
    assert str(repository) not in rendered
    assert "secret-parent" not in rendered


def test_transport_passes_notification_as_json_stdin(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """通知文字列を shell/PowerShell code へ連結せず JSON data として渡す。"""
    calls: list[tuple[list[str], dict[str, object]]] = []
    monkeypatch.setattr(
        runtime_windows_toast,
        "_powershell_executable",
        lambda: Path("/windows/powershell.exe"),
    )

    def fake_run(
        args: list[str], **kwargs: object
    ) -> subprocess.CompletedProcess[bytes]:
        """PowerShell process の argv と stdin を記録する。"""
        calls.append((args, kwargs))
        return subprocess.CompletedProcess(args, 0)

    monkeypatch.setattr(runtime_windows_toast.subprocess, "run", fake_run)
    title = "cmoc '; Write-Error injected"
    message = 'repo </text><text id="2">secret'

    # suite 全体の toast 隔離 fixture を越えて、実 transport の組み立てを検証する。
    assert _REAL_WINDOWS_TOAST_TRANSPORT(title, message) is True

    [(args, kwargs)] = calls
    assert args[:5] == [
        "/windows/powershell.exe",
        "-NoLogo",
        "-NoProfile",
        "-NonInteractive",
        "-EncodedCommand",
    ]
    assert title not in "\n".join(args)
    assert message not in "\n".join(args)
    encoded_script = args[5]
    script = base64.b64decode(encoded_script).decode("utf-16-le")
    assert title not in script
    assert message not in script
    assert "[Console]::In.ReadToEnd()" in script
    payload = kwargs["input"]
    assert isinstance(payload, bytes)
    assert json.loads(payload) == {"title": title, "message": message}
    assert kwargs["timeout"] == runtime_windows_toast._POWERSHELL_TIMEOUT_SEC
    assert kwargs["check"] is False
    assert "shell" not in kwargs


def test_notification_failure_does_not_escape(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """transport の timeout を terminal result の失敗へ変換しない。"""
    calls: list[tuple[str, str]] = []

    def fail_transport(title: str, message: str) -> bool:
        """有限時間超過した transport を再現する。"""
        calls.append((title, message))
        raise subprocess.TimeoutExpired(["powershell.exe"], 5)

    monkeypatch.setattr(
        runtime_windows_toast,
        "_run_windows_toast_transport",
        fail_transport,
    )

    runtime_windows_toast.notify_terminal_result("doctor", tmp_path, "failed")
    assert calls == [("cmoc doctor", f"{tmp_path.name} — エラー終了")]


def test_codex_callback_deduplicates_each_turn_and_ignores_message_text(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """同じ turn は一度だけ通知し、callback 本文を通知へ渡さない。"""
    state_root = tmp_path / "callback-state"
    state_root.mkdir()
    calls: list[tuple[str, str, str]] = []
    monkeypatch.setattr(
        runtime_windows_toast,
        "_notify_fields",
        lambda command, repository, state: calls.append((command, repository, state)),
    )
    payload = json.dumps(
        {
            "type": "agent-turn-complete",
            "thread-id": "thread-1",
            "turn-id": "turn-1",
            "input-messages": ["prompt secret"],
            "last-assistant-message": "assistant secret",
        }
    )
    arguments = [
        "codex-tui-callback",
        str(state_root),
        "oracle edit",
        "repository",
        payload,
    ]

    with ThreadPoolExecutor(max_workers=8) as executor:
        results = list(executor.map(runtime_windows_toast.main, [arguments] * 8))

    assert results == [0] * 8
    assert calls == [("oracle edit", "repository", "waiting")]
    assert "prompt secret" not in repr(calls)
    assert "assistant secret" not in repr(calls)

    next_payload = json.loads(payload)
    next_payload["turn-id"] = "turn-2"
    arguments[-1] = json.dumps(next_payload)
    assert runtime_windows_toast.main(arguments) == 0
    assert calls[-1] == ("oracle edit", "repository", "waiting")
    assert len(calls) == 2


def test_tui_callback_state_is_invocation_local(tmp_path: Path) -> None:
    """callback state を TUI invocation 終了時に永続化せず破棄する。"""
    callback = runtime_windows_toast.create_tui_notification_callback(
        "tui",
        tmp_path / "repository",
    )

    assert callback is not None
    assert callback.command[0] == sys.executable
    assert Path(callback.command[1]) == Path(runtime_windows_toast.__file__).resolve()
    assert callback.command[2] == "codex-tui-callback"
    state_root = Path(callback.command[3])
    assert state_root.is_dir()
    assert callback.command[4:] == ["tui", "repository"]

    callback.close()

    assert not state_root.exists()


def test_tui_callback_command_runs_as_standalone_script(tmp_path: Path) -> None:
    """Codex が起動する実 argv で callback を実行し、一時 state だけを残す。"""
    callback = runtime_windows_toast.create_tui_notification_callback(
        "oracle investigation",
        tmp_path / "repository",
    )
    assert callback is not None
    payload = json.dumps(
        {
            "type": "agent-turn-complete",
            "thread-id": "thread-1",
            "turn-id": "turn-1",
        }
    )
    state_root = Path(callback.command[3])

    try:
        for _ in range(2):
            result = subprocess.run(
                [*callback.command, payload],
                env=os.environ,
                text=True,
                capture_output=True,
                timeout=10,
                check=False,
            )
            assert result.returncode == 0
            assert result.stdout == ""
            assert result.stderr == ""
        assert len(list(state_root.glob("*.seen"))) == 1
    finally:
        callback.close()
