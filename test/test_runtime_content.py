"""runtime content helper の hash・binary 判定と安全な保存を検証する。

根拠:
- {{work-root}}/oracle/doc/app_spec/indexing.md
- {{work-root}}/oracle/doc/app_spec/codex_exec_rule.md
"""

import hashlib
from pathlib import Path

import pytest

from commons.runtime_content import is_binary, write_hashed_file


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


def test_write_hashed_file_replaces_symlink_without_overwriting_target(
    tmp_path: Path,
) -> None:
    """hash path の symlink を辿らず、リンク先の内容を保持して保存する。"""
    content = '{"ok": true}\n'
    external = tmp_path / "external.json"
    external.write_text("keep this file", encoding="utf-8")
    directory = tmp_path / "schema"
    directory.mkdir()
    path = directory / f"{hashlib.sha256(content.encode('utf-8')).hexdigest()}.json"
    path.symlink_to(external)

    result = write_hashed_file(directory, "", ".json", content)

    assert result == path
    assert not path.is_symlink()
    assert path.read_bytes() == content.encode("utf-8")
    assert external.read_text(encoding="utf-8") == "keep this file"
