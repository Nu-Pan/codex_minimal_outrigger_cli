"""runtime content helper の hash と安全な保存を検証する。

根拠:
- {{work-root}}/spec/app_spec/codex_exec_rule.md
"""

import hashlib
import os
from pathlib import Path

import pytest

import commons.runtime_content as runtime_content
from commons.runtime_content import write_hashed_file


@pytest.mark.parametrize("target_content", ["keep this file", '{"ok": true}\n', None])
def test_write_hashed_file_replaces_symlink_without_overwriting_target(
    tmp_path: Path,
    target_content: str | None,
) -> None:
    """同内容や dangling の symlink も置換し、リンク先を保持する。"""
    content = '{"ok": true}\n'
    external = tmp_path / "external.json"
    if target_content is not None:
        external.write_text(target_content, encoding="utf-8")
    directory = tmp_path / "schema"
    directory.mkdir()
    path = directory / f"{hashlib.sha256(content.encode('utf-8')).hexdigest()}.json"
    path.symlink_to(external)

    result = write_hashed_file(directory, "", ".json", content)

    assert result == path
    assert not path.is_symlink()
    assert path.read_bytes() == content.encode("utf-8")
    if target_content is None:
        assert not external.exists()
    else:
        assert external.read_text(encoding="utf-8") == target_content


@pytest.mark.parametrize("existing_content", [None, "stale", '{"ok": true}\n'])
def test_write_hashed_file_creates_repairs_or_reuses_regular_file(
    tmp_path: Path,
    existing_content: str | None,
) -> None:
    """未作成なら親から作成し、破損を修復し、同内容の保存物は書き換えない。"""
    content = '{"ok": true}\n'
    directory = tmp_path / "nested" / "schema"
    path = directory / f"{hashlib.sha256(content.encode('utf-8')).hexdigest()}.json"
    if existing_content is not None:
        directory.mkdir(parents=True)
        path.write_text(existing_content, encoding="utf-8")
        os.utime(path, ns=(1_000_000_000, 1_000_000_000))
        original_mtime = path.stat().st_mtime_ns

    result = write_hashed_file(directory, "", ".json", content)

    assert result == path
    assert path.read_bytes() == content.encode("utf-8")
    assert list(directory.iterdir()) == [path]
    if existing_content == content:
        assert path.stat().st_mtime_ns == original_mtime


def test_write_hashed_file_rejects_directory_at_hash_path(tmp_path: Path) -> None:
    """保存先が directory の場合はそのまま残して失敗する。"""
    content = '{"ok": true}\n'
    path = tmp_path / f"{hashlib.sha256(content.encode('utf-8')).hexdigest()}.json"
    path.mkdir()

    with pytest.raises(IsADirectoryError):
        write_hashed_file(tmp_path, "", ".json", content)

    assert path.is_dir()
    assert list(tmp_path.iterdir()) == [path]


def test_write_hashed_file_cleans_up_after_replace_failure(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """置換できない場合は元の保存物を保持し、一時 file を残さない。"""
    content = '{"ok": true}\n'
    path = tmp_path / f"{hashlib.sha256(content.encode('utf-8')).hexdigest()}.json"
    path.write_text("stale", encoding="utf-8")

    def fail_replace(source: Path, destination: Path) -> None:
        raise PermissionError("replace denied")

    monkeypatch.setattr(runtime_content.os, "replace", fail_replace)

    with pytest.raises(PermissionError, match="replace denied"):
        write_hashed_file(tmp_path, "", ".json", content)

    assert path.read_text(encoding="utf-8") == "stale"
    assert list(tmp_path.iterdir()) == [path]
