"""realization refactor 永続 state の同期・選択規則を検証する。"""

from pathlib import Path

import pytest
from _git_support import make_repo

from cmoc_runtime import CmocError, file_sha256
from commons.runtime_refactor import (
    load_refactor_state,
    select_refactor_target,
    sync_refactor_state,
    write_refactor_state,
)


def test_refactor_state_sync_tracks_exact_oracle_and_realization_set(
    tmp_path: Path,
) -> None:
    root = make_repo(tmp_path)

    state = sync_refactor_state(root)

    assert set(state) == {"README.md", "oracle/spec.md"}
    assert all(entry["investigation_required"] for entry in state.values())
    assert all(
        entry["last_investigation_result"] == "not_investigated"
        for entry in state.values()
    )
    assert load_refactor_state(root) == state


def test_refactor_state_sync_preserves_history_and_requeues_changed_file(
    tmp_path: Path,
) -> None:
    root = make_repo(tmp_path)
    state = sync_refactor_state(root)
    entry = state["README.md"]
    entry.update(
        {
            "investigation_required": False,
            "last_investigation_result": "no_findings",
            "last_investigated_sha256": file_sha256(root / "README.md"),
            "last_investigated_at": "2026-07-19_00-00-00_000000000",
        }
    )
    write_refactor_state(root, state)
    (root / "README.md").write_text("changed\n")

    synchronized = sync_refactor_state(root)

    changed = synchronized["README.md"]
    assert changed["investigation_required"] is True
    assert changed["last_investigation_result"] == "no_findings"
    assert changed["last_investigated_at"] == "2026-07-19_00-00-00_000000000"
    assert changed["last_investigated_sha256"] != file_sha256(root / "README.md")


def test_refactor_target_selection_prioritizes_uninvestigated_then_oldest(
    tmp_path: Path,
) -> None:
    root = make_repo(tmp_path)
    state = sync_refactor_state(root)
    state["README.md"].update(
        {
            "last_investigation_result": "findings",
            "last_investigated_sha256": file_sha256(root / "README.md"),
            "last_investigated_at": "2026-01-01_00-00-00_000000000",
        }
    )

    assert select_refactor_target(state) == "oracle/spec.md"

    state["oracle/spec.md"].update(
        {
            "last_investigation_result": "no_findings",
            "last_investigated_sha256": file_sha256(root / "oracle" / "spec.md"),
            "last_investigated_at": "2026-02-01_00-00-00_000000000",
        }
    )
    assert select_refactor_target(state) == "README.md"
    assert select_refactor_target(state, {"README.md"}) == "oracle/spec.md"
    assert select_refactor_target(state, set(state)) is None


def test_refactor_state_rejects_parent_path_escape(tmp_path: Path) -> None:
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
