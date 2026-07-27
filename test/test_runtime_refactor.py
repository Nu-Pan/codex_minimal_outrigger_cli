"""realization refactor 永続 state の同期・選択規則を検証する。

正本仕様: `{{work-root}}/oracle/doc/app_spec/sub_command/realization_refactor.md`,
`{{work-root}}/oracle/doc/app_spec/misc_spec.md`。
"""

import hashlib
import json
from pathlib import Path
from typing import cast

import pytest
from _git_support import make_repo, run_git

from cmoc_runtime import CmocError, file_sha256
from commons.runtime_git import is_oracle_file_path, is_realization_file_path
from commons.runtime_refactor import (
    RefactorState,
    load_refactor_state,
    select_refactor_target,
    sync_refactor_state,
    write_refactor_state,
)


def test_refactor_state_sync_tracks_exact_oracle_and_realization_set(
    tmp_path: Path,
) -> None:
    """refactor state が oracle と realization の正確な file 集合を追跡する。"""
    root = make_repo(tmp_path)

    state = sync_refactor_state(root)

    assert set(state) == {"README.md", "oracle/spec.md"}
    assert all(entry["investigation_required"] for entry in state.values())
    assert all(
        entry["last_investigation_result"] == "not_investigated"
        for entry in state.values()
    )
    assert all(
        entry["last_investigated_sha256"] is None
        and entry["last_investigated_at"] is None
        for entry in state.values()
    )
    assert load_refactor_state(root) == state


@pytest.mark.parametrize(
    "relative", ["nested/../../outside.md", "oracle/../../outside.md"]
)
def test_refactor_target_classifiers_reject_parent_path_escape(
    tmp_path: Path, relative: str
) -> None:
    """oracle/realization file classifier が work-root 外の path を拒否する。"""
    # 根拠: {{work-root}}/oracle/src/oracle/prompt_builder/parts/oracle_and_realization_basic.py
    root = make_repo(tmp_path)
    (tmp_path / "outside.md").write_text("outside\n")

    path = root / relative

    assert not is_oracle_file_path(root, path)
    assert not is_realization_file_path(root, path)


def test_refactor_target_classifiers_require_file_entries(
    tmp_path: Path,
) -> None:
    """oracle/realization file classifier が directory と欠落 path を拒否する。"""
    root = make_repo(tmp_path)
    realization_directory = root / "src"
    realization_directory.mkdir()
    realization_file = realization_directory / "module.py"
    realization_file.write_text("VALUE = 1\n")
    run_git(root, "add", "src/module.py")
    run_git(root, "commit", "-m", "add realization directory")

    assert not is_oracle_file_path(root, root / "oracle")
    assert not is_oracle_file_path(root, root / "oracle" / "missing.md")
    assert not is_realization_file_path(root, realization_directory)
    assert not is_realization_file_path(root, realization_directory, branch="HEAD")
    assert is_realization_file_path(root, realization_file, branch="HEAD")
    assert not is_realization_file_path(root, root / "missing.py")


def test_refactor_target_classifier_rejects_gitlink_directory(
    tmp_path: Path,
) -> None:
    """realization file classifier が Gitlink の directory entry を拒否する。"""
    root = make_repo(tmp_path)
    gitlink = root / "module"
    gitlink.mkdir()
    commit = run_git(root, "rev-parse", "HEAD").stdout.strip()
    run_git(root, "update-index", "--add", "--cacheinfo", f"160000,{commit},module")
    run_git(root, "commit", "-m", "add gitlink entry")

    assert gitlink.is_dir()
    assert not is_realization_file_path(root, gitlink, branch="HEAD")


def test_refactor_state_sync_hashes_dangling_oracle_symlink(
    tmp_path: Path,
) -> None:
    """定義上の oracle file である dangling symlink を state 同期できる。"""
    root = make_repo(tmp_path)
    link = root / "oracle" / "dangling.md"
    link.symlink_to("../missing.md")
    run_git(root, "add", "oracle/dangling.md")
    run_git(root, "commit", "-m", "add dangling oracle symlink")

    state = sync_refactor_state(root)
    expected_digest = hashlib.sha256(b"../missing.md").hexdigest()

    assert "oracle/dangling.md" in state
    state["oracle/dangling.md"].update(
        {
            "investigation_required": False,
            "last_investigation_result": "no_findings",
            "last_investigated_sha256": expected_digest,
            "last_investigated_at": "2026-07-19_00-00_00_000000000",
        }
    )
    write_refactor_state(root, state)
    link.unlink()
    link.symlink_to("../different-missing.md")

    synchronized = sync_refactor_state(root)

    changed = synchronized["oracle/dangling.md"]
    assert changed["investigation_required"] is True
    assert changed["last_investigated_sha256"] == expected_digest


def test_refactor_state_sync_preserves_history_and_requeues_changed_file(
    tmp_path: Path,
) -> None:
    """state 同期が調査履歴を保持し、変更 file を再調査対象へ戻す。"""
    root = make_repo(tmp_path)
    state = sync_refactor_state(root)
    entry = state["README.md"]
    previous_digest = file_sha256(root / "README.md")
    entry.update(
        {
            "investigation_required": False,
            "last_investigation_result": "no_findings",
            "last_investigated_sha256": previous_digest,
            "last_investigated_at": "2026-07-19_00-00_00_000000000",
        }
    )
    write_refactor_state(root, state)
    (root / "README.md").write_text("changed\n")

    synchronized = sync_refactor_state(root)

    changed = synchronized["README.md"]
    assert changed["investigation_required"] is True
    assert changed["last_investigation_result"] == "no_findings"
    assert changed["last_investigated_at"] == "2026-07-19_00-00_00_000000000"
    assert changed["last_investigated_sha256"] == previous_digest


def test_refactor_state_writer_rejects_invalid_entry(tmp_path: Path) -> None:
    """state writer が schema 不正値を保存しない。"""
    root = make_repo(tmp_path)
    state = cast(
        RefactorState,
        {
            "README.md": {
                "investigation_required": True,
                "last_investigation_result": [],
                "last_investigated_sha256": None,
                "last_investigated_at": None,
            }
        },
    )

    with pytest.raises(CmocError, match="refactor state"):
        write_refactor_state(root, state)


def test_refactor_target_selection_prioritizes_uninvestigated_then_oldest(
    tmp_path: Path,
) -> None:
    """target 選択が未調査 entry と古い調査時刻を優先する。"""
    root = make_repo(tmp_path)
    state = sync_refactor_state(root)
    state["README.md"].update(
        {
            "last_investigation_result": "findings",
            "last_investigated_sha256": file_sha256(root / "README.md"),
            "last_investigated_at": "2026-01-01_00-00_00_000000000",
        }
    )

    assert select_refactor_target(state) == "oracle/spec.md"

    state["oracle/spec.md"].update(
        {
            "last_investigation_result": "no_findings",
            "last_investigated_sha256": file_sha256(root / "oracle" / "spec.md"),
            "last_investigated_at": "2026-02-01_00-00_00_000000000",
        }
    )
    assert select_refactor_target(state) == "README.md"
    assert select_refactor_target(state, {"README.md"}) == "oracle/spec.md"
    assert select_refactor_target(state, set(state)) is None


def test_refactor_state_rejects_parent_path_escape(tmp_path: Path) -> None:
    """refactor state の親 path escape を拒否する。"""
    root = make_repo(tmp_path)
    path = root / ".cmoc" / "gt" / "ar" / "realization" / "refactor" / "state.json"
    path.parent.mkdir(parents=True)
    path.write_text(
        '{"../outside": {'
        '"investigation_required": true, '
        '"last_investigation_result": "not_investigated", '
        '"last_investigated_sha256": null, '
        '"last_investigated_at": null}}\n'
    )

    with pytest.raises(CmocError, match="refactor state"):
        load_refactor_state(root)


@pytest.mark.parametrize("result", [[], {}])
def test_refactor_state_rejects_non_string_result(
    tmp_path: Path,
    result: object,
) -> None:
    """entry の調査結果が JSON string 以外なら schema error にする。"""
    root = make_repo(tmp_path)
    path = root / ".cmoc" / "gt" / "ar" / "realization" / "refactor" / "state.json"
    path.parent.mkdir(parents=True)
    path.write_text(
        json.dumps(
            {
                "README.md": {
                    "investigation_required": False,
                    "last_investigation_result": result,
                    "last_investigated_sha256": "0" * 64,
                    "last_investigated_at": "2026-07-19_00-00_00_000000000",
                }
            }
        )
        + "\n"
    )

    with pytest.raises(CmocError, match="refactor state"):
        load_refactor_state(root)


def test_refactor_state_rejects_non_utf8_content(tmp_path: Path) -> None:
    """UTF-8 として読めない state は schema error にする。"""
    root = make_repo(tmp_path)
    path = root / ".cmoc" / "gt" / "ar" / "realization" / "refactor" / "state.json"
    path.parent.mkdir(parents=True)
    path.write_bytes(b'{"README.md": \xff}\n')

    with pytest.raises(CmocError, match="refactor state"):
        load_refactor_state(root)


def test_refactor_state_rejects_nul_in_path_key(tmp_path: Path) -> None:
    """NUL を含む path key は file path として拒否する。"""
    root = make_repo(tmp_path)
    path = root / ".cmoc" / "gt" / "ar" / "realization" / "refactor" / "state.json"
    path.parent.mkdir(parents=True)
    path.write_text(
        json.dumps(
            {
                "\x00": {
                    "investigation_required": True,
                    "last_investigation_result": "not_investigated",
                    "last_investigated_sha256": None,
                    "last_investigated_at": None,
                }
            }
        )
        + "\n"
    )

    with pytest.raises(CmocError, match="refactor state"):
        load_refactor_state(root)


@pytest.mark.parametrize(
    ("key", "investigated_at"),
    [("./README.md", "2026-07-19_00-00_00_000000000"), ("README.md", "invalid")],
)
def test_refactor_state_rejects_noncanonical_path_or_timestamp(
    tmp_path: Path,
    key: str,
    investigated_at: str,
) -> None:
    """正規化されていない path と timestamp を state schema で拒否する。"""
    root = make_repo(tmp_path)
    path = root / ".cmoc" / "gt" / "ar" / "realization" / "refactor" / "state.json"
    path.parent.mkdir(parents=True)
    path.write_text(
        json.dumps(
            {
                key: {
                    "investigation_required": False,
                    "last_investigation_result": "no_findings",
                    "last_investigated_sha256": "0" * 64,
                    "last_investigated_at": investigated_at,
                }
            }
        )
        + "\n"
    )

    with pytest.raises(CmocError, match="refactor state"):
        load_refactor_state(root)
