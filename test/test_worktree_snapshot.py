"""取得済み状態を共用する復元処理と、復元後の再確認を検証する。"""

import pytest

import commons.runtime_git as runtime_git
from commons.runtime_errors import CmocError


def test_restore_snapshot_reuses_current_state_and_preserves_unselected_files(tmp_path):
    """所有 path を取得済み状態から復元し、対象外の人間の差分を保持する。"""
    owned = tmp_path / "owned.txt"
    other = tmp_path / "other.txt"
    owned.write_text("initial")
    snapshot = runtime_git.capture_worktree_snapshot(tmp_path, paths=[owned.name])
    owned.write_text("changed")
    other.write_text("human change")
    current = runtime_git.capture_worktree_snapshot(tmp_path, paths=snapshot.paths)

    runtime_git.restore_worktree_snapshot(snapshot, current=current)
    assert owned.read_text() == "initial"
    assert other.read_text() == "human change"
    runtime_git.restore_worktree_snapshot(snapshot)
    assert owned.read_text() == "initial"


def test_restore_snapshot_rejects_incomplete_restoration(tmp_path, monkeypatch):
    """復元書き込みが状態を戻せなければ、成功を返さず再確認で停止する。"""
    owned = tmp_path / "owned.txt"
    owned.write_text("initial")
    snapshot = runtime_git.capture_worktree_snapshot(tmp_path, paths=[owned.name])
    owned.write_text("changed")
    current = runtime_git.capture_worktree_snapshot(tmp_path, paths=snapshot.paths)
    monkeypatch.setattr(runtime_git, "_write_worktree_artifact", lambda *_args: None)

    with pytest.raises(CmocError, match="復元できませんでした") as error:
        runtime_git.restore_worktree_snapshot(snapshot, current=current)

    assert owned.name in error.value.detail
