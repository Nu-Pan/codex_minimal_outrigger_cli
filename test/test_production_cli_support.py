"""実経路統合テストの PTY 操作 helper を検証する。"""

import json
import os
import select
import signal
import subprocess
import sys
from contextlib import nullcontext
from pathlib import Path
from types import SimpleNamespace

import test_production_cli as production_cli
from test_production_cli import (
    _advance_trust_confirmation,
    _completed_tui_message,
    _run_refactor_until_confirmed,
)


def test_refactor_driver_interrupts_after_a_confirmed_unit(tmp_path) -> None:
    """Real CLI 用 driver の停止条件を Fake process で検証する。"""
    script = (
        "import json, pathlib, signal, sys, time; "
        "signal.signal(signal.SIGINT, lambda *_: sys.exit(0)); "
        "path = pathlib.Path('.cmoc/gu/log/sub_command/fake.jsonl'); "
        "path.parent.mkdir(parents=True); "
        "path.write_text(json.dumps({'event':'refactor_progress','confirmed':1})); "
        "print('confirmed', flush=True); time.sleep(30)"
    )
    result = _run_refactor_until_confirmed(
        [sys.executable, "-c", script], tmp_path, dict(os.environ)
    )
    assert result.returncode == 0
    assert result.stdout == "confirmed\n"


def test_refactor_driver_rechecks_only_changed_logs(tmp_path, monkeypatch) -> None:
    """履歴を除外し、追記と同サイズの更新を検出して SIGINT を一度だけ送る。"""
    directory = tmp_path / ".cmoc/gu/log/sub_command"
    directory.mkdir(parents=True)
    previous = directory / "previous.jsonl"
    previous.write_text('{"event":"refactor_progress","confirmed":1}\n')
    log = directory / "current.jsonl"
    reads = []
    read_text = Path.read_text

    def record_read(path, *args, **kwargs):
        reads.append(path)
        return read_text(path, *args, **kwargs)

    monkeypatch.setattr(Path, "read_text", record_read)
    signals = []
    polls = 0

    def communicate(timeout):
        nonlocal polls
        polls += 1
        if polls <= 4:
            assert not signals
        else:
            assert signals == [signal.SIGINT]
        if polls == 1:
            log.write_text('{"event":"refactor_progress","confirmed":')
            os.utime(log, ns=(1_000_000_000, 1_000_000_000))
        elif polls == 3:
            # mtime が同じでも、partial JSON への追記は再確認する。
            with log.open("a") as output:
                output.write("0}\n")
            os.utime(log, ns=(1_000_000_000, 1_000_000_000))
        elif polls == 4:
            # 同サイズの書き換えは mtime の変更から検出する。
            log.write_text('{"event":"refactor_progress","confirmed":1}\n')
            os.utime(log, ns=(2_000_000_000, 2_000_000_000))
        elif polls == 6:
            return "confirmed\n", "diagnostics\n"
        raise subprocess.TimeoutExpired(["fake-refactor"], timeout)

    process = SimpleNamespace(
        communicate=communicate, send_signal=signals.append, returncode=0
    )
    # polling は決定論的に進め、実 SIGINT の配送は上の Fake process test に残す。
    monkeypatch.setattr(
        production_cli.subprocess,
        "Popen",
        lambda *_args, **_kwargs: nullcontext(process),
    )
    result = _run_refactor_until_confirmed(["fake-refactor"], tmp_path, {})
    assert result.returncode == 0
    assert (result.stdout, result.stderr) == ("confirmed\n", "diagnostics\n")
    assert reads == [log, log, log]
    assert polls == 6


def test_tui_completion_skips_unchanged_logs_and_rechecks_partial_utf8(
    tmp_path, monkeypatch
) -> None:
    """完了済み exec と stream 表示を除外し、TUI の追記完了だけを受理する。"""
    sessions = tmp_path / "sessions/2026/10/11"
    sessions.mkdir(parents=True)
    exec_log = sessions / "rollout-exec.jsonl"
    exec_log.write_text(
        json.dumps({"type": "session_meta", "payload": {"originator": "codex-exec"}})
        + "\n"
        + json.dumps(
            {
                "type": "event_msg",
                "payload": {"type": "task_complete", "last_agent_message": "resolver"},
            }
        )
        + "\n",
        encoding="utf-8",
    )
    reads = []
    read_bytes = Path.read_bytes

    def record_read(path):
        reads.append(path)
        return read_bytes(path)

    monkeypatch.setattr(Path, "read_bytes", record_read)
    versions = {}
    assert _completed_tui_message(tmp_path, versions) is None

    # polling 開始後に session が作られる場合も見つける。
    tui_log = sessions / "rollout-tui.jsonl"
    tui_log.write_text(
        json.dumps({"type": "session_meta", "payload": {"originator": "codex-tui"}})
        + "\n"
        + json.dumps(
            {
                "type": "event_msg",
                "payload": {"type": "agent_message", "message": "streaming"},
            }
        )
        + "\n",
        encoding="utf-8",
    )
    for _ in range(3):
        assert _completed_tui_message(tmp_path, versions) is None
    assert reads.count(exec_log) == reads.count(tui_log) == 1

    completion = (
        json.dumps(
            {
                "type": "event_msg",
                "payload": {
                    "type": "task_complete",
                    "last_agent_message": "完了しました",
                },
            },
            ensure_ascii=False,
        ).encode("utf-8")
        + b"\n"
    )
    boundary = completion.index("完".encode("utf-8")) + 1
    with tui_log.open("ab") as output:
        output.write(completion[:boundary])
    for _ in range(3):
        assert _completed_tui_message(tmp_path, versions) is None
    assert reads.count(tui_log) == 2

    with tui_log.open("ab") as output:
        output.write(completion[boundary:])
    assert _completed_tui_message(tmp_path, versions) == "完了しました"
    assert reads.count(tui_log) == 3
    assert reads.count(exec_log) == 1


def test_trust_confirmation_waits_until_the_poll_after_prompt_detection() -> None:
    """描画中ではなく次の poll で trust prompt を確定する。"""
    read_fd, write_fd = os.pipe()
    try:
        ready, confirmed = _advance_trust_confirmation(
            write_fd,
            bytearray(),
            False,
        )

        assert (ready, confirmed) == (False, False)
        assert not select.select([read_fd], [], [], 0)[0]

        ready, confirmed = _advance_trust_confirmation(
            write_fd,
            bytearray(b"Press enter to continue"),
            False,
        )

        assert (ready, confirmed) == (True, False)
        assert not select.select([read_fd], [], [], 0)[0]

        ready, confirmed = _advance_trust_confirmation(
            write_fd,
            bytearray(b"Press enter to continue"),
            ready,
        )

        assert (ready, confirmed) == (True, True)
        assert os.read(read_fd, 1) == b"\r"
    finally:
        os.close(read_fd)
        os.close(write_fd)
