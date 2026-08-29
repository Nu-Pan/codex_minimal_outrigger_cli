"""実経路統合テストの PTY 操作 helper を検証する。"""

import os
import select

from test_production_cli import _advance_trust_confirmation


def test_trust_confirmation_waits_until_the_poll_after_prompt_detection() -> None:
    """描画中ではなく次の poll で trust prompt を確定する。"""
    read_fd, write_fd = os.pipe()
    try:
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
