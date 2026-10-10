"""実経路統合テストの PTY 操作 helper を検証する。"""

import json
import os
import select
import sys
from pathlib import Path

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
