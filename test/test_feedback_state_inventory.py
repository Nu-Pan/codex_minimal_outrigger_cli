"""feedback artifact の列挙境界を Git・publication の準備なしで検証する。"""

import os
from pathlib import Path

import pytest

from commons.runtime_errors import CmocError
from commons.runtime_feedback_state import _require_only_expected_files


def test_inventory_checks_nested_and_hidden_files_and_refreshes(tmp_path, monkeypatch):
    root = tmp_path / "state"
    _require_only_expected_files(root, set(), "state")
    (root / "nested" / "empty").mkdir(parents=True)
    paths = [root / "manifest.json", root / "nested" / ".checkpoint.json"]
    for path in paths:
        path.write_bytes(b"{}\n")
    expected = set(paths)

    # root の表記によらず、解決済みの参照集合と照合する。
    monkeypatch.chdir(tmp_path)
    alias = tmp_path / "alias"
    alias.symlink_to(tmp_path, target_is_directory=True)
    for directory in (root, Path("state"), alias / "state"):
        _require_only_expected_files(directory, expected, "state")

    # cleanup 済みの欠落は許し、次の呼出しで増えた file は再検査する。
    paths[0].unlink()
    _require_only_expected_files(root, expected, "state")
    extra = root / "nested" / ".unexpected.json"
    extra.write_bytes(b"{}\n")
    with pytest.raises(CmocError, match="未定義 artifact") as error:
        _require_only_expected_files(root, expected, "state")
    assert error.value.detail == str(extra)
    extra.unlink()
    _require_only_expected_files(root, expected, "state")


@pytest.mark.parametrize("kind", ["file", "directory_link", "dangling_link"])
def test_inventory_rejects_invalid_root(tmp_path, kind):
    root = tmp_path / "state"
    if kind == "file":
        root.touch()
    else:
        target = tmp_path if kind == "directory_link" else tmp_path / "missing"
        root.symlink_to(target, target_is_directory=True)

    with pytest.raises(CmocError, match="root が通常 directory"):
        _require_only_expected_files(root, set(), "state")


@pytest.mark.parametrize("kind", ["file_link", "directory_link", "dangling", "fifo"])
def test_inventory_rejects_nonregular_artifacts_even_if_listed(tmp_path, kind):
    root = tmp_path / "state"
    nested = root / "nested"
    nested.mkdir(parents=True)
    artifact = nested / "artifact"
    if kind == "fifo":
        os.mkfifo(artifact)
    else:
        target = tmp_path / "target"
        if kind == "file_link":
            target.touch()
        elif kind == "directory_link":
            target.mkdir()
        artifact.symlink_to(target, target_is_directory=kind == "directory_link")

    with pytest.raises(CmocError, match="未定義 artifact") as error:
        _require_only_expected_files(root, {artifact.resolve()}, "state")
    assert error.value.detail == str(artifact)


def test_inventory_does_not_skip_unreadable_subtree(tmp_path, monkeypatch):
    nested = tmp_path / "nested"
    nested.mkdir()
    scan = os.scandir

    def unreadable(directory):
        if Path(directory) == nested:
            raise PermissionError("unreadable subtree")
        return scan(directory)

    monkeypatch.setattr(os, "scandir", unreadable)
    with pytest.raises(CmocError, match="artifact 一覧を読めません") as error:
        _require_only_expected_files(tmp_path, set(), "state")
    assert error.value.detail == str(nested)
    assert isinstance(error.value.__cause__, PermissionError)
