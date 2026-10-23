"""実経路統合テストの PTY 操作 helper を検証する。"""

import json
import os
import signal
import subprocess
import sys
import time
from contextlib import nullcontext
from pathlib import Path
from types import SimpleNamespace

import pytest
import test_production_cli as production_cli
from _command_support import write_python_executable
from test_production_cli import (
    _advance_trust_confirmation,
    _completed_tui_turn,
    _run_refactor_until_confirmed,
)

_SESSION_ID = "019efe07-4886-7423-b252-625febbe31eb"


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
    # 標準ライブラリだけの Fake は共通 command helper と同様に site 初期化を省く。
    # 推論を待たない Fake では監視間隔を短くし、実 SIGINT の配送と終了は待つ。
    result = _run_refactor_until_confirmed(
        [sys.executable, "-S", "-c", script],
        tmp_path,
        dict(os.environ),
        poll_interval=0.001,
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
    """別会話と stream 表示を除外し、exec 由来の固定 UUID の完了を受理する。"""
    sessions = tmp_path / "sessions/2026/10/11"
    sessions.mkdir(parents=True)
    exec_log = sessions / "rollout-exec.jsonl"
    exec_log.write_text(
        json.dumps(
            {
                "type": "session_meta",
                "payload": {"id": "other-session", "originator": "codex_exec"},
            }
        )
        + "\n"
        + json.dumps(
            {
                "type": "event_msg",
                "payload": {
                    "type": "task_complete",
                    "turn_id": "other-turn",
                    "last_agent_message": "resolver",
                },
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
    assert _completed_tui_turn(tmp_path, _SESSION_ID, versions) is None

    # polling 開始後に session が作られる場合も見つける。
    tui_log = sessions / "rollout-tui.jsonl"
    tui_log.write_text(
        json.dumps(
            {
                "type": "session_meta",
                "payload": {"id": _SESSION_ID, "originator": "codex_exec"},
            }
        )
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
        assert _completed_tui_turn(tmp_path, _SESSION_ID, versions) is None
    assert reads.count(exec_log) == reads.count(tui_log) == 1

    completion = (
        json.dumps(
            {
                "type": "event_msg",
                "payload": {
                    "type": "task_complete",
                    "turn_id": "initial-turn",
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
        assert _completed_tui_turn(tmp_path, _SESSION_ID, versions) is None
    assert reads.count(tui_log) == 2

    with tui_log.open("ab") as output:
        output.write(completion[boundary:])
    assert _completed_tui_turn(tmp_path, _SESSION_ID, versions) == (
        "initial-turn",
        "完了しました",
    )
    assert reads.count(tui_log) == 3
    assert reads.count(exec_log) == 1


def test_resumed_tui_completion_requires_a_new_turn(tmp_path) -> None:
    """入力文の保存に依存せず、再開時の最終 turn より後の完了だけを受理する。"""
    log = tmp_path / "sessions/rollout-resumed.jsonl"
    log.parent.mkdir()
    log.write_text(
        json.dumps(
            {
                "type": "session_meta",
                "payload": {"id": _SESSION_ID, "originator": "codex_exec"},
            }
        )
        + "\n"
    )
    versions = {}

    def append(payload):
        with log.open("a") as output:
            output.write(json.dumps({"type": "event_msg", "payload": payload}) + "\n")

    def completed():
        return _completed_tui_turn(
            tmp_path, _SESSION_ID, versions, after_turn_id="previous-turn"
        )

    append(
        {
            "type": "task_complete",
            "turn_id": "initial-turn",
            "last_agent_message": "initial answer",
        }
    )
    assert completed() is None
    append(
        {
            "type": "task_complete",
            "turn_id": "previous-turn",
            "last_agent_message": "previous answer",
        }
    )
    assert completed() is None
    append({"type": "task_started", "turn_id": "new-turn"})
    assert completed() is None
    append(
        {
            "type": "task_complete",
            "turn_id": "new-turn",
            "last_agent_message": "new answer",
        }
    )
    assert completed() == ("new-turn", "new answer")


@pytest.mark.parametrize("input_message", [None, "follow-up"])
def test_tui_driver_waits_for_the_composer_and_the_requested_turn(
    tmp_path, monkeypatch, input_message
) -> None:
    """描画と完了の境界を、process の scheduling や固定待機に依存せず確認する。"""
    # driver が観測する file と描画を poll ごとに進め、早すぎる入力・終了を検出する。
    call = tmp_path / ".cmoc/gu/log/codex/current/tui_call.json"
    call.parent.mkdir(parents=True)
    payload = {
        "argv": ["codex", "resume", _SESSION_ID],
        "fixed_session_id": _SESSION_ID,
        "process_state": "prepared",
    }
    rollout = tmp_path / "sessions/rollout-initial.jsonl"
    rollout.parent.mkdir()
    rollout.write_text(
        json.dumps({"type": "session_meta", "payload": {"id": _SESSION_ID}})
        + "\n"
        + json.dumps(
            {
                "type": "event_msg",
                "payload": {
                    "type": "task_complete",
                    "turn_id": "initial-turn",
                    "last_agent_message": "initial answer",
                },
            }
        )
        + "\n"
    )
    writes = []
    screen = []
    polls = 0
    stopped = []

    def spawn(*_args, **_kwargs):
        # previous_calls の取得後に作り、実際の call log の選別も通す。
        call.write_text(json.dumps(payload))
        return process

    def read_pty(_fd, transcript):
        received = b"".join(screen)
        screen.clear()
        transcript.extend(received)
        return received

    def advance(_seconds):
        nonlocal polls
        polls += 1
        if polls <= 3:
            assert writes == [], "input or shutdown before TUI is ready"
            if polls == 1:
                payload["process_state"] = "started"
                call.write_text(json.dumps(payload))
            elif polls == 2:
                screen.append(b"? for shortcuts")
        elif input_message is not None and polls <= 6:
            if polls == 4:
                assert writes == [b"\x1b[200~" + input_message.encode() + b"\x1b[201~"]
            elif polls == 5:
                assert writes == [b"\r"]
            else:
                assert writes == [], "shutdown based on the previous completion"
                with rollout.open("a") as output:
                    output.write(
                        json.dumps(
                            {
                                "type": "event_msg",
                                "payload": {
                                    "type": "task_complete",
                                    "turn_id": "new-turn",
                                    "last_agent_message": "new answer",
                                },
                            }
                        )
                        + "\n"
                    )
        else:
            assert polls == (4 if input_message is None else 7)
            assert writes == [b"\x03"]
        writes.clear()

    def wait(timeout):
        assert writes == [b"\x03"]
        screen.append(b"Shutting down")
        return 0

    process = SimpleNamespace(poll=lambda: None, wait=wait)
    monkeypatch.setattr(production_cli, "subprocess", SimpleNamespace(Popen=spawn))
    monkeypatch.setattr(
        production_cli, "time", SimpleNamespace(monotonic=lambda: 0, sleep=advance)
    )
    monkeypatch.setattr(
        production_cli,
        "os",
        SimpleNamespace(
            write=lambda _fd, data: writes.append(data),
            close=os.close,
            set_blocking=os.set_blocking,
        ),
    )
    monkeypatch.setattr(production_cli, "_read_pty", read_pty)
    monkeypatch.setattr(production_cli, "_stop_tui_process_group", stopped.append)
    response, transcript = production_cli._run_cmoc_tui(
        tmp_path / "fake-cmoc",
        tmp_path,
        {},
        tmp_path,
        "resume" if input_message is not None else "tui",
        input_message=input_message,
    )
    assert polls == (4 if input_message is None else 7)
    assert response == ("initial answer" if input_message is None else "new answer")
    assert "Shutting down" in transcript
    assert stopped == [process]


def test_tui_driver_exchanges_input_and_shutdown_over_a_real_pty(
    tmp_path, monkeypatch
) -> None:
    """実 process への paste・Enter・終了操作と PTY の回収は一つの結合ケースで保つ。"""
    cmoc = tmp_path / "fake-cmoc"
    write_python_executable(
        cmoc,
        [
            "import json, os, pathlib, select, sys, tty",
            "tty.setraw(sys.stdin.fileno())",
            f"session_id = {_SESSION_ID!r}",
            "rollout = pathlib.Path('sessions/rollout-initial.jsonl')",
            "rollout.parent.mkdir()",
            "def append(event):",
            "    with rollout.open('a') as output:",
            "        output.write(json.dumps(event) + '\\n')",
            "append({'type': 'session_meta', 'payload': {",
            "    'id': session_id, 'originator': 'codex_exec'}})",
            "append({'type': 'event_msg', 'payload': {",
            "    'type': 'task_complete', 'turn_id': 'initial-turn',",
            "    'last_agent_message': 'initial answer'}})",
            "call = pathlib.Path('.cmoc/gu/log/codex/current/tui_call.json')",
            "call.parent.mkdir(parents=True)",
            "payload = {'argv': ['codex', 'resume', session_id],",
            "           'fixed_session_id': session_id, 'process_state': 'started'}",
            "call.write_text(json.dumps(payload))",
            "print('? for shortcuts', flush=True)",
            "def read_until(suffix):",
            "    received = b''",
            "    while not received.endswith(suffix):",
            "        assert select.select([sys.stdin], [], [], 5)[0], 'input timeout'",
            "        received += os.read(sys.stdin.fileno(), 1)",
            "    return received",
            "assert read_until(b'\\r') == b'\\x1b[200~follow-up\\x1b[201~\\r'",
            "append({'type': 'event_msg', 'payload': {",
            "    'type': 'task_complete', 'turn_id': 'new-turn',",
            "    'last_agent_message': 'new answer'}})",
            "assert read_until(b'\\x03\\x03') == b'\\x03\\x03'",
            "print('Shutting down', flush=True)",
        ],
    )
    monkeypatch.setattr(production_cli, "_PRODUCTION_COMMAND_TIMEOUT", 10)
    # Fake は描画・paste burst の待機を要しないので、child へ実行機会だけ譲る。
    # 操作順と poll の境界は上の決定論的 test で検証する。
    monkeypatch.setattr(
        production_cli,
        "time",
        SimpleNamespace(
            monotonic=time.monotonic, sleep=lambda _seconds: time.sleep(0.001)
        ),
    )
    response, transcript = production_cli._run_cmoc_tui(
        cmoc,
        tmp_path,
        dict(os.environ),
        tmp_path,
        "resume",
        input_message="follow-up",
    )
    assert response == "new answer"
    assert "Shutting down" in transcript


def test_trust_confirmation_waits_until_the_poll_after_prompt_detection(
    monkeypatch,
) -> None:
    """描画中ではなく次の poll で trust prompt を確定する。"""
    # poll の境界と送信先・内容を記録し、実 I/O は上の PTY 結合ケースに残す。
    master_fd = 123
    writes = []
    monkeypatch.setattr(
        production_cli,
        "os",
        SimpleNamespace(write=lambda fd, data: writes.append((fd, data))),
    )
    ready, confirmed = _advance_trust_confirmation(master_fd, bytearray(), False)
    assert (ready, confirmed) == (False, False)
    assert writes == []

    ready, confirmed = _advance_trust_confirmation(
        master_fd, bytearray(b"Press enter to continue"), False
    )
    assert (ready, confirmed) == (True, False)
    assert writes == []

    ready, confirmed = _advance_trust_confirmation(
        master_fd, bytearray(b"Press enter to continue"), ready
    )
    assert (ready, confirmed) == (True, True)
    assert writes == [(master_fd, b"\r")]
