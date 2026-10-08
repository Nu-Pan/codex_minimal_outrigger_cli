"""実経路統合テストの PTY 操作 helper を検証する。"""

import os
import select
import sys

from test_production_cli import (
    _advance_trust_confirmation,
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
