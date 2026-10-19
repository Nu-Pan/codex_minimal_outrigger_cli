"""realization refactor 永続 state の同期・選択規則を検証する。

正本仕様:
- `{{work-root}}/oracle/doc/app_spec/sub_command/realization_refactor.md`
- `{{work-root}}/oracle/doc/app_spec/oracle_and_realization_file_enumeration.md`
- `{{work-root}}/oracle/doc/app_spec/timestamp.md`
"""

import json
import os
from pathlib import Path
from types import SimpleNamespace
from typing import cast
from unittest.mock import Mock

import pytest
from _git_support import run_git

import commons.runtime_git as git_module
import commons.runtime_refactor as refactor_module
import sub_commands.realization.refactor as refactor_workload
import sub_commands.session.join as session_join_module
from cmoc_runtime import CmocError
from commons.runtime_git import is_oracle_file_path, is_realization_file_path
from commons.runtime_refactor import (
    RefactorState,
    is_normalized_relative_path,
    load_refactor_state,
    merge_refactor_states,
    refactor_cycle_targets,
    sync_refactor_state,
    write_refactor_state,
)
from commons.runtime_results import CommandResult


@pytest.mark.parametrize(
    "initial_state", ["empty", "pending", "investigated", "new_entries"]
)
def test_refactor_cycle_initialization_avoids_redundant_io(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, initial_state: str
) -> None:
    """日時を保持して巡を初期化し、同期が生んだ差分だけを確定する。"""
    root = tmp_path
    targets = [] if initial_state == "empty" else ["README.md", "oracle/spec.md"]
    monkeypatch.setattr(
        refactor_module, "enumerate_refactor_targets", lambda _root: targets
    )
    write_refactor_state(root, {})
    if initial_state in {"pending", "investigated"}:
        state = sync_refactor_state(root)
        if initial_state == "investigated":
            for entry in state.values():
                entry["last_investigated_at"] = "2026-10-18_00-00-00_001"
            write_refactor_state(root, state)
    state_path = refactor_workload.refactor_state_path(root)
    before = state_path.read_bytes()
    save = Mock(wraps=write_refactor_state)
    monkeypatch.setattr(refactor_module, "write_refactor_state", save)
    monkeypatch.setattr(refactor_workload, "write_refactor_state", save)

    # Git 分類・commit/rollback と中断は test_editing_run_cli.py に残す。
    # ここでは保存内容と既存 snapshot の差を Git 境界へ渡し、巡開始の I/O を検査する。
    inspect_changes = Mock(
        side_effect=lambda _root, **_kwargs: (
            [state_path.relative_to(root).as_posix()]
            if state_path.read_bytes() != before
            else []
        )
    )
    commit = Mock()
    monkeypatch.setattr(refactor_workload, "worktree_change_paths", inspect_changes)
    monkeypatch.setattr(refactor_workload, "commit_work_unit", commit)
    progress = refactor_workload._RefactorProgress(
        cycle=1,
        targets={"previous.md"},
        processed={"previous.md"},
        deferred={"previous.md"},
    )

    pending = refactor_workload._initialize_cycle(
        SimpleNamespace(run_worktree=root), progress=progress
    )

    assert pending == targets
    assert set(load_refactor_state(root)) == set(targets)
    assert progress.cycle == 2
    assert progress.targets == set(targets)
    assert not progress.processed
    assert not progress.deferred
    inspect_changes.assert_called_once_with(root, include_rename_sources=True)
    assert save.call_count == (1 if initial_state == "new_entries" else 0)
    if initial_state == "new_entries":
        commit.assert_called_once_with(root, "cmoc realization refactor cycle")
    else:
        commit.assert_not_called()
        assert state_path.read_bytes() == before


@pytest.mark.parametrize(
    "relative", ["nested/../../outside.md", "oracle/../../outside.md"]
)
def test_refactor_target_classifiers_reject_parent_path_escape(
    tmp_path: Path, relative: str
) -> None:
    """oracle/realization file classifier が work-root 外の path を拒否する。"""
    # 根拠: {{work-root}}/oracle/doc/app_spec/oracle_and_realization_file_enumeration.md
    # の「分類結果」
    # 範囲外 path は Git 問い合わせ前に拒否するため、repository は不要。
    root = tmp_path / "repo"
    root.mkdir()
    (root / "nested").mkdir()
    (root / "oracle").mkdir()
    (tmp_path / "outside.md").write_text("outside\n")

    path = root / relative

    assert not is_oracle_file_path(root, path)
    assert not is_realization_file_path(root, path)


def test_refactor_target_classifiers_require_file_entries(
    cli_repository: Path,
) -> None:
    """通常・削除済み file を受理し、directory・欠落 path・Gitlink を拒否する。"""
    # 特殊文字 path の blob と Gitlink を同じ tree に用意し、履歴の準備を共有する。
    root = cli_repository
    (root / "oracle").mkdir()
    realization_directory = root / "src"
    realization_directory.mkdir()
    realization_file = realization_directory / "module[1].py"
    realization_file.write_text("VALUE = 1\n")
    gitlink = root / "module"
    gitlink.mkdir()
    run_git(root, "add", "src/module[1].py")
    # Gitlink の参照先 object は親 repository に不要。分類用の mode と OID だけを
    # 用意し、参照先を作るためだけの空 commit と HEAD 照会を省く。
    run_git(root, "update-index", "--add", "--cacheinfo", f"160000,{'a' * 40},module")
    run_git(root, "commit", "-m", "add classifier entries")

    assert not is_oracle_file_path(root, root / "oracle")
    assert not is_oracle_file_path(root, root / "oracle" / "missing.md")
    assert not is_realization_file_path(root, realization_directory)
    assert not is_realization_file_path(root, realization_directory, branch="HEAD")
    assert is_realization_file_path(root, realization_file, branch="HEAD")
    assert not is_realization_file_path(root, root / "missing.py")
    assert gitlink.is_dir()
    assert not is_realization_file_path(root, gitlink, branch="HEAD")
    gitlink.rmdir()
    assert not is_realization_file_path(root, gitlink, branch="HEAD")

    realization_file.unlink()
    assert not is_realization_file_path(root, realization_file)
    assert is_realization_file_path(root, realization_file, branch="HEAD")


def test_refactor_target_classifiers_reject_symlinked_parent(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """symlink 親を通る path は、Git 問い合わせ前に work-root 外参照を拒否する。"""
    # 実 branch からの file 分類は隣接 test に残し、親 path の拒否に Git を準備しない。
    root = tmp_path / "repo"
    root.mkdir()
    outside = tmp_path / "outside"
    outside.mkdir()
    source = root / "src"
    (outside / "module.py").write_text("outside\n")
    source.symlink_to(outside, target_is_directory=True)
    (root / "oracle").mkdir()
    (root / "oracle" / "linked").symlink_to(outside, target_is_directory=True)

    def unexpected_git(*_args, **_kwargs):
        pytest.fail("symlinked parents must be rejected before querying Git")

    monkeypatch.setattr(git_module, "run_git", unexpected_git)

    assert not is_realization_file_path(root, root / "src" / "module.py", branch="HEAD")
    assert not is_realization_file_path(
        root, root / "src" / "deleted.py", branch="HEAD"
    )
    assert not is_oracle_file_path(root, root / "oracle" / "linked" / "module.py")


@pytest.mark.parametrize(
    "replacement",
    [
        "directory",
        "symlink",
        pytest.param(
            "fifo",
            marks=pytest.mark.skipif(
                not hasattr(os, "mkfifo"), reason="named pipes are unavailable"
            ),
        ),
    ],
)
def test_refactor_target_classifier_rejects_non_file_replacing_branch_file(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, replacement: str
) -> None:
    """branch の blob fallback が既存の非通常 file を file として扱わない。"""
    # 実 branch の blob/tree/Gitlink と特殊文字 path は隣接する分類 test に残す。
    # ここでは同じ branch blob に対する欠落・非通常 file の違いだけを検査する。
    root = tmp_path / "repo"
    root.mkdir()
    path = root / "module.py"

    def branch_blob(args: list[str], *_args, **_kwargs) -> CommandResult:
        assert "unused-invalid-ref" not in args, "non-file paths need no fallback ref"
        return CommandResult(0, f"100644 blob {'a' * 40}\tmodule.py\0", "")

    monkeypatch.setattr(git_module, "run_git", branch_blob)
    # 対照ケースで blob 応答が受理されることも確認し、double の不備を検出する。
    assert is_realization_file_path(root, path, branch="HEAD")

    if replacement == "directory":
        path.mkdir()
    elif replacement == "symlink":
        path.symlink_to(root / "missing")
    else:
        os.mkfifo(path)

    assert not is_realization_file_path(
        root, path, branch="HEAD", fallback_branch="unused-invalid-ref"
    )


def test_refactor_state_sync_initializes_and_preserves_dates_without_reading_contents(
    tmp_path, monkeypatch
):
    """初期 entry の保存と、内容変更後の日時保持を同じ同期処理で検査する。"""
    root = tmp_path
    targets = ["README.md", "oracle/spec.md"]
    for relative in targets:
        path = root / relative
        path.parent.mkdir(exist_ok=True)
        path.write_text("original\n")
    monkeypatch.setattr(
        refactor_module, "enumerate_refactor_targets", lambda _: targets
    )
    state = sync_refactor_state(root)
    assert state == {
        "README.md": {"last_investigated_at": None},
        "oracle/spec.md": {"last_investigated_at": None},
    }
    assert load_refactor_state(root) == state
    state["README.md"]["last_investigated_at"] = "2026-07-19_00-00-00_000"
    write_refactor_state(root, state)
    (root / "README.md").write_text("changed\n")
    open_file = Path.open

    def open_state_only(path, *args, **kwargs):
        assert path not in [root / target for target in targets], (
            "content read during sync"
        )
        return open_file(path, *args, **kwargs)

    monkeypatch.setattr(Path, "open", open_state_only)
    assert sync_refactor_state(root) == state
    assert load_refactor_state(root) == state


@pytest.mark.parametrize(
    "change", ["none", "target_mode", "related_mode", "deleted", "renamed"]
)
def test_refactor_state_update_only_dates_surviving_origin(
    tmp_path, monkeypatch, change
):
    root = tmp_path
    paths = {"README.md", "oracle/spec.md"}
    monkeypatch.setattr(
        refactor_module, "enumerate_refactor_targets", lambda _: sorted(paths)
    )
    state = sync_refactor_state(root)
    for entry in state.values():
        entry["last_investigated_at"] = "2026-10-11_00-00-00_000"
    write_refactor_state(root, state)
    if change in {"target_mode", "related_mode"}:
        relative = "README.md" if change == "target_mode" else "oracle/spec.md"
        path = root / relative
        path.parent.mkdir(exist_ok=True)
        path.write_text("mode probe\n")
        path.chmod(0o755)
    elif change in {"deleted", "renamed"}:
        paths.remove("README.md")
        if change == "renamed":
            paths.add("renamed.md")
    investigated_at = "2026-10-11_00-00-00_001"
    monkeypatch.setattr(refactor_workload, "timestamp", lambda: investigated_at)

    updated = refactor_workload._update_refactor_state(
        SimpleNamespace(run_worktree=root), "README.md"
    )

    assert updated == load_refactor_state(root)
    assert set(updated) == paths
    if "README.md" in paths:
        assert updated["README.md"] == {"last_investigated_at": investigated_at}
    if change == "renamed":
        assert updated["renamed.md"] == {"last_investigated_at": None}
    assert updated["oracle/spec.md"] == state["oracle/spec.md"]


def test_refactor_commit_reuses_verified_head_and_synchronized_state(
    tmp_path, monkeypatch
):
    """検証済み HEAD・同期済み state で進捗を更新し、同じ情報を再取得しない。"""
    state = {"README.md": {"last_investigated_at": "2026-10-11_00-00-00_001"}}
    read = Mock(side_effect=AssertionError("state was already synchronized"))
    monkeypatch.setattr(refactor_workload, "load_refactor_state", read)
    # Git commit と中断の結合は test_editing_run_cli.py に残す。
    query = Mock(side_effect=AssertionError("HEAD was already verified"))
    monkeypatch.setattr(refactor_workload, "run_git", query)
    monkeypatch.setattr(
        refactor_workload, "commit_work_unit", Mock(return_value="after")
    )
    progress = refactor_workload._RefactorProgress(
        cycle=1, targets={"README.md", "removed.md"}, deferred={"removed.md"}
    )
    units = []
    unresolved = {"removed.md": [("old finding", "reason", tmp_path / "call.json")]}

    refactor_workload._commit_refactor_unit(
        SimpleNamespace(run_worktree=tmp_path),
        "README.md",
        0,
        [],
        units,
        unresolved,
        "unit",
        before_head="before",
        state=state,
        progress=progress,
    )

    read.assert_not_called()
    query.assert_not_called()
    assert units == [("README.md", 0)]
    assert progress.targets == progress.processed == {"README.md"}
    assert progress.completed_cycles == 1
    assert not progress.deferred
    assert not unresolved


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("last_investigated_at", []),
        ("last_investigated_at", False),
        ("last_investigated_at", "invalid"),
        ("investigation_required", True),
        ("last_investigation_result", "no_findings"),
        ("last_investigated_sha256", "0" * 64),
    ],
)
@pytest.mark.parametrize("operation", ["write", "sync"])
def test_refactor_state_rejects_invalid_entry_without_discarding_information(
    tmp_path, field, value, operation
):
    state = cast(
        RefactorState, {"README.md": {"last_investigated_at": None, field: value}}
    )
    write_refactor_state(tmp_path, {})
    path = refactor_workload.refactor_state_path(tmp_path)
    if operation == "sync":
        path.write_text(json.dumps(state))
    before = path.read_bytes()
    with pytest.raises(CmocError, match="refactor state"):
        if operation == "write":
            write_refactor_state(tmp_path, state)
        else:
            sync_refactor_state(tmp_path)
    assert path.read_bytes() == before


@pytest.mark.parametrize(
    "link_relative",
    [
        ".cmoc/gt/realization/refactor/state.json",
        ".cmoc/gt/realization/refactor",
        ".cmoc",
        ".",
    ],
)
@pytest.mark.parametrize("target_exists", [True, False])
def test_refactor_state_rejects_symlink_without_accessing_target(
    tmp_path: Path, link_relative: str, target_exists: bool
) -> None:
    """state・親・root の symlink は、参照先の有無にかかわらず読み書きしない。"""
    root = tmp_path / "repo"
    outside = tmp_path / "outside"
    outside_state = outside / ".cmoc" / "gt" / "realization" / "refactor" / "state.json"
    if target_exists:
        outside_state.parent.mkdir(parents=True)
        outside_state.write_text("original\n")
    link = root / link_relative
    target = outside / link_relative
    link.parent.mkdir(parents=True, exist_ok=True)
    link.symlink_to(target, target_is_directory=not link.name.endswith(".json"))

    with pytest.raises(CmocError, match="refactor state") as read_error:
        load_refactor_state(root)
    assert "symlink" in read_error.value.detail
    with pytest.raises(CmocError, match="refactor state") as write_error:
        write_refactor_state(root, {})
    assert "symlink" in write_error.value.detail

    if target_exists:
        assert outside_state.read_text() == "original\n"
    else:
        assert not outside.exists()


@pytest.mark.parametrize(
    "path_kind",
    [
        "directory",
        pytest.param(
            "fifo",
            marks=pytest.mark.skipif(
                not hasattr(os, "mkfifo"), reason="named pipes are unavailable"
            ),
        ),
    ],
)
def test_refactor_state_rejects_non_file_path(tmp_path: Path, path_kind: str) -> None:
    """state path が通常 file でない場合に read/write を block させない。"""
    root = tmp_path
    path = root / ".cmoc" / "gt" / "realization" / "refactor" / "state.json"
    path.parent.mkdir(parents=True)
    if path_kind == "directory":
        path.mkdir()
    else:
        os.mkfifo(path)

    with pytest.raises(CmocError, match="refactor state"):
        load_refactor_state(root)
    with pytest.raises(CmocError, match="refactor state"):
        write_refactor_state(root, {})


@pytest.mark.parametrize(
    "parent_kind",
    [
        "file",
        pytest.param(
            "fifo",
            marks=pytest.mark.skipif(
                not hasattr(os, "mkfifo"), reason="named pipes are unavailable"
            ),
        ),
    ],
)
def test_refactor_state_rejects_non_directory_parent(
    tmp_path: Path, parent_kind: str
) -> None:
    """state の親が通常 directory でない場合に read/write を block させない。"""
    root = tmp_path
    parent = root / ".cmoc" / "gt" / "realization" / "refactor"
    parent.parent.mkdir(parents=True)
    if parent_kind == "file":
        parent.write_text("not a directory\n")
    else:
        os.mkfifo(parent)

    with pytest.raises(CmocError, match="refactor state"):
        load_refactor_state(root)
    with pytest.raises(CmocError, match="refactor state"):
        write_refactor_state(root, {})


def test_refactor_cycle_prioritizes_null_then_milliseconds_then_path():
    state: RefactorState = {
        "README.md": {"last_investigated_at": None},
        "oracle/spec.md": {"last_investigated_at": None},
    }
    assert refactor_cycle_targets(state) == ["README.md", "oracle/spec.md"]
    state["README.md"]["last_investigated_at"] = "2026-01-01_00-00-00_000"
    assert refactor_cycle_targets(state) == ["oracle/spec.md", "README.md"]
    state["oracle/spec.md"]["last_investigated_at"] = "2026-01-01_00-00-00_001"
    assert refactor_cycle_targets(state) == ["README.md", "oracle/spec.md"]
    state["README.md"]["last_investigated_at"] = "2026-01-01_00-00-00_002"
    assert refactor_cycle_targets(state) == ["oracle/spec.md", "README.md"]
    state["oracle/spec.md"]["last_investigated_at"] = "2026-01-01_00-00-00_002"
    assert refactor_cycle_targets(state) == ["README.md", "oracle/spec.md"]
    assert refactor_cycle_targets({}) == []


@pytest.mark.parametrize("has_committed_state", [False, True])
@pytest.mark.parametrize("same_ref", [False, True])
def test_merge_refactor_states_reads_shared_snapshot_once(
    tmp_path, monkeypatch, has_committed_state, same_ref
):
    """同一 ref の照会と同一 snapshot の本文取得を繰り返さず、同期して保存する。"""
    root = tmp_path
    committed = {
        "README.md": {"last_investigated_at": "2026-10-18_00-00-00_001"},
        "removed.md": {"last_investigated_at": "2026-10-18_00-00-00_002"},
    }

    # 実 Git との結合・異なる commit の日時統合は隣接 test に残す。
    # snapshot の有無だけを Git 境界で与え、同期・日時保持・保存は実処理を通す。
    def committed_git(args, queried_root):
        assert queried_root == root
        if args[0] == "ls-tree":
            return CommandResult(
                0,
                "100644 blob abc\t.cmoc/gt/realization/refactor/state.json\0"
                if has_committed_state
                else "",
                "",
            )
        assert args[0] == "show"
        return CommandResult(0, json.dumps(committed), "")

    query = Mock(side_effect=committed_git)
    monkeypatch.setattr(refactor_module, "run_git", query)
    monkeypatch.setattr(
        refactor_module,
        "enumerate_refactor_targets",
        lambda _: ["README.md", "added.md"],
    )
    # 作業中の値は採用せず、確定済み snapshot からだけ日時を引き継ぐ。
    write_refactor_state(root, {"README.md": {"last_investigated_at": None}})

    refs = ("first-commit", "first-commit" if same_ref else "second-commit")
    state = merge_refactor_states(root, refs)

    assert state == {
        "README.md": committed["README.md"]
        if has_committed_state
        else {"last_investigated_at": None},
        "added.md": {"last_investigated_at": None},
    }
    assert load_refactor_state(root) == state
    # 種類・存在は各 ref で検証し、同じ tree entry の本文取得は一度にする。
    assert query.call_count == len(set(refs)) + int(has_committed_state)


def test_merge_refactor_states_uses_committed_dates_and_current_paths(
    tmp_path, monkeypatch
):
    root = tmp_path
    older = "2026-10-18_00-00-00_001"
    newer = "2026-10-18_00-00-00_002"
    left, right = "a" * 40, "b" * 40
    snapshots = {
        left: {
            "README.md": {"last_investigated_at": None},
            "oracle/spec.md": {"last_investigated_at": older},
            "removed.md": {"last_investigated_at": newer},
            "left.py": {"last_investigated_at": older},
        },
        right: {
            "README.md": {"last_investigated_at": newer},
            "oracle/spec.md": {"last_investigated_at": None},
            "right.py": {"last_investigated_at": None},
        },
    }

    # 実 Git の snapshot 取得・日時統合・同期は managed_state_conflict_merges_without_agent
    # と test_editing_run_cli.py の join_merges_committed_timestamps_before_sync に残す。
    # 値の優先順位と入力順序の検査には確定済み snapshot だけを渡し、履歴を作らない。
    def committed_git(args, queried_root):
        assert queried_root == root
        if args[0] == "ls-tree":
            ref = args[2]
            return CommandResult(
                0, f"100644 blob {ref}\t.cmoc/gt/realization/refactor/state.json\0", ""
            )
        assert args[0] == "show"
        ref, _separator, _relative = args[1].partition(":")
        return CommandResult(0, json.dumps(snapshots[ref]), "")

    monkeypatch.setattr(refactor_module, "run_git", committed_git)
    targets = ["README.md", "oracle/spec.md", "left.py", "right.py", "added.py"]
    monkeypatch.setattr(
        refactor_module, "enumerate_refactor_targets", lambda _: targets
    )

    for refs in ((left, right), (right, left)):
        # 各順序で作業中の値を戻し、前回の統合結果からの読み込みも検出する。
        write_refactor_state(root, {"README.md": {"last_investigated_at": None}})
        state = merge_refactor_states(root, refs)

        assert state == {
            "README.md": {"last_investigated_at": newer},
            "oracle/spec.md": {"last_investigated_at": older},
            "left.py": {"last_investigated_at": older},
            "right.py": {"last_investigated_at": None},
            "added.py": {"last_investigated_at": None},
        }, refs
        assert load_refactor_state(root) == state, refs


def test_managed_state_conflict_merges_without_agent(cli_repository, monkeypatch):
    root = cli_repository
    (root / "README.md").write_text("readme\n")
    write_refactor_state(root, {"README.md": {"last_investigated_at": None}})
    run_git(root, "add", "-A")
    run_git(root, "commit", "-m", "initial")
    run_git(root, "branch", "other")
    newer = "2026-10-18_00-00-00_002"
    write_refactor_state(root, {"README.md": {"last_investigated_at": newer}})
    run_git(root, "commit", "-am", "first investigation")
    first = run_git(root, "rev-parse", "HEAD").stdout.strip()
    run_git(root, "switch", "other")
    write_refactor_state(
        root, {"README.md": {"last_investigated_at": "2026-10-18_00-00-00_001"}}
    )
    run_git(root, "commit", "-am", "other investigation")
    other = run_git(root, "rev-parse", "HEAD").stdout.strip()
    merge = git_module.run_git(["merge", "--no-edit", first], root, check=False)
    assert merge.returncode != 0

    # session の入口でも、管理物だけなら完全 prompt の構築を省く。
    build_parameter = Mock(side_effect=AssertionError("unused agent parameter"))
    codex_exec = Mock(side_effect=AssertionError("unused agent call"))
    report_fields = {}
    monkeypatch.setattr(
        session_join_module,
        "build_session_join_conflict_resolution_request",
        build_parameter,
    )
    monkeypatch.setattr(
        session_join_module,
        "update_primary_report_fields",
        lambda **fields: report_fields.update(fields),
    )

    session_join_module.resolve_session_join_conflict(root, first, other, codex_exec)

    build_parameter.assert_not_called()
    codex_exec.assert_not_called()
    assert report_fields["conflict_resolution_status"] == "not_needed"
    assert report_fields["conflict_resolution_result"] == "confirmed"
    assert report_fields["conflict_agent_report"] is None
    assert load_refactor_state(root) == {"README.md": {"last_investigated_at": newer}}
    assert not run_git(root, "status", "--porcelain").stdout


def test_refactor_state_rejects_parent_path_escape(tmp_path: Path) -> None:
    """refactor state の親 path escape を拒否する。"""
    root = tmp_path
    path = root / ".cmoc" / "gt" / "realization" / "refactor" / "state.json"
    path.parent.mkdir(parents=True)
    path.write_text('{"../outside": {"last_investigated_at": null}}\n')

    with pytest.raises(CmocError, match="refactor state"):
        load_refactor_state(root)


@pytest.mark.skipif(os.name != "nt", reason="Windows path semantics are unavailable")
def test_refactor_state_rejects_drive_relative_path() -> None:
    """Windows の drive-relative path を work-root 相対 path として受け入れない。"""
    assert not is_normalized_relative_path("C:outside")


def test_refactor_state_rejects_non_utf8_content(tmp_path: Path) -> None:
    """UTF-8 として読めない state は schema error にする。"""
    root = tmp_path
    path = root / ".cmoc" / "gt" / "realization" / "refactor" / "state.json"
    path.parent.mkdir(parents=True)
    path.write_bytes(b'{"README.md": \xff}\n')

    with pytest.raises(CmocError, match="refactor state"):
        load_refactor_state(root)


def test_refactor_state_rejects_nul_in_path_key(tmp_path: Path) -> None:
    """NUL を含む path key は file path として拒否する。"""
    root = tmp_path
    path = root / ".cmoc" / "gt" / "realization" / "refactor" / "state.json"
    path.parent.mkdir(parents=True)
    path.write_text(
        json.dumps(
            {
                "\x00": {
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
    [
        ("./README.md", "2026-07-19_00-00-00_000"),
        ("README.md", "invalid"),
        ("README.md", "２０２６-０７-１９_００-００_００_０００００００００"),
    ],
)
def test_refactor_state_rejects_noncanonical_path_or_timestamp(
    tmp_path: Path,
    key: str,
    investigated_at: str,
) -> None:
    """正規化されていない path と timestamp を state schema で拒否する。"""
    root = tmp_path
    path = root / ".cmoc" / "gt" / "realization" / "refactor" / "state.json"
    path.parent.mkdir(parents=True)
    path.write_text(
        json.dumps(
            {
                key: {
                    "last_investigated_at": investigated_at,
                }
            }
        )
        + "\n"
    )

    with pytest.raises(CmocError, match="refactor state"):
        load_refactor_state(root)
