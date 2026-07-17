"""indexing が binary file を除外するための content 判定を検証する。

根拠:
- {{work-root}}/oracle/doc/app_spec/indexing.md
"""

from pathlib import Path

import pytest

from commons.runtime_content import is_binary


@pytest.mark.parametrize(
    ("content", "expected"),
    [(b"plain text\n", False), (b"text\0bytes", True)],
    ids=("text", "nul-byte"),
)
def test_is_binary_distinguishes_text_and_nul_bytes(
    tmp_path: Path, content: bytes, expected: bool
) -> None:
    """NUL byteを含む内容だけをbinaryとして判定することを検証する。"""
    path = tmp_path / "content"
    path.write_bytes(content)

    assert is_binary(path) is expected
