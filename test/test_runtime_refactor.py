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

import pytest
from _git_support import run_git

import commons.runtime_refactor as refactor_module
import sub_commands.realization.refactor.fork as refactor_workload
from cmoc_runtime import CmocError, file_sha256
from commons.runtime_git import is_oracle_file_path, is_realization_file_path
from commons.runtime_refactor import (
    RefactorState,
    is_normalized_relative_path,
    load_refactor_state,
    refactor_cycle_targets,
    sync_refactor_state,
    write_refactor_state,
)


@pytest.fixture
def refactor_files(tmp_path: Path) -> Path:
    """state 同期で実際に読み書きする file を、Git 準備から分ける。"""
    root = tmp_path / "repo"
    root.mkdir()
    (root / "README.md").write_text("# repo\n")
    (root / "oracle").mkdir()
    (root / "oracle" / "spec.md").write_text("# spec\n")
    return root


def test_refactor_state_sync_tracks_enumerated_files(
    refactor_files: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """列挙された新規・未調査 file を、不要な内容読み取りなしで同期する。"""
    root = refactor_files
    # 実列挙との結合は test_file_inventory.py に残し、state 更新だけを分離する。
    monkeypatch.setattr(
        refactor_module,
        "enumerate_refactor_targets",
        lambda _root: ["README.md", "oracle/spec.md"],
    )

    def unexpected_hash(_path: Path) -> str:
        pytest.fail("uninvestigated files do not need a content hash comparison")

    monkeypatch.setattr(refactor_module, "file_sha256", unexpected_hash)

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

    # 比較先が null の既存 entry も、内容にかかわらず再調査へ戻す。
    for entry in state.values():
        entry["investigation_required"] = False
    write_refactor_state(root, state)
    synchronized = sync_refactor_state(root)
    assert synchronized == {
        relative: {**entry, "investigation_required": True}
        for relative, entry in state.items()
    }


def test_refactor_state_sync_globs_nested_repository_files(
    cli_repository: Path, tmp_path: Path
) -> None:
    """work-root 配下の nested repository 内 file も対象へ含める。"""
    root = cli_repository
    nested = root / "nested"
    nested.mkdir()
    run_git(
        root,
        "init",
        "--template=/dev/null",
        "--separate-git-dir",
        str(tmp_path / "nested-git"),
        str(nested),
    )
    run_git(nested, "config", "core.excludesFile", "/dev/null")
    (nested / "module.py").write_text("VALUE = 1\n")

    state = sync_refactor_state(root)

    assert "nested/module.py" in state


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
    committed_repository: Path,
) -> None:
    """通常 file を受理し、directory・欠落 path・Gitlink を拒否する。"""
    # blob と Gitlink を同じ tree に用意し、種類の検査で repository 準備を共有する。
    root = committed_repository
    (root / "oracle").mkdir()
    realization_directory = root / "src"
    realization_directory.mkdir()
    realization_file = realization_directory / "module.py"
    realization_file.write_text("VALUE = 1\n")
    gitlink = root / "module"
    gitlink.mkdir()
    commit = run_git(root, "rev-parse", "HEAD").stdout.strip()
    run_git(root, "add", "src/module.py")
    run_git(root, "update-index", "--add", "--cacheinfo", f"160000,{commit},module")
    run_git(root, "commit", "-m", "add classifier entries")

    assert not is_oracle_file_path(root, root / "oracle")
    assert not is_oracle_file_path(root, root / "oracle" / "missing.md")
    assert not is_realization_file_path(root, realization_directory)
    assert not is_realization_file_path(root, realization_directory, branch="HEAD")
    assert is_realization_file_path(root, realization_file, branch="HEAD")
    assert not is_realization_file_path(root, root / "missing.py")
    assert gitlink.is_dir()
    assert not is_realization_file_path(root, gitlink, branch="HEAD")


def test_refactor_target_classifiers_reject_symlinked_parent(
    cli_repository: Path, tmp_path: Path
) -> None:
    """classifier が symlink 親を通じて work-root 外の file を扱わない。"""
    root = cli_repository
    outside = tmp_path / "outside"
    outside.mkdir()
    source = root / "src"
    source.mkdir()
    (source / "module.py").write_text("inside\n")
    (source / "deleted.py").write_text("deleted\n")
    run_git(root, "add", "src/module.py", "src/deleted.py")
    run_git(root, "commit", "-m", "add realization module")
    (outside / "module.py").write_text("outside\n")
    (source / "module.py").unlink()
    (source / "deleted.py").unlink()
    source.rmdir()
    source.symlink_to(outside, target_is_directory=True)
    (root / "oracle").mkdir()
    (root / "oracle" / "linked").symlink_to(outside, target_is_directory=True)

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
    cli_repository: Path, replacement: str
) -> None:
    """branch の blob fallback が既存の非通常 file を file として扱わない。"""
    root = cli_repository
    path = root / "module.py"
    path.write_text("VALUE = 1\n")
    run_git(root, "add", "module.py")
    run_git(root, "commit", "-m", "add module")
    path.unlink()
    if replacement == "directory":
        path.mkdir()
    elif replacement == "symlink":
        path.symlink_to(root / "missing")
    else:
        os.mkfifo(path)

    assert not is_realization_file_path(
        root, path, branch="HEAD", fallback_branch="unused-invalid-ref"
    )


def test_refactor_target_classifier_accepts_special_path_from_branch(
    cli_repository: Path,
) -> None:
    """削除された特殊文字 path も branch tree の realization と判定する。"""
    root = cli_repository
    realization_file = root / "module[1].py"
    realization_file.write_text("VALUE = 1\n")
    run_git(root, "add", "module[1].py")
    run_git(root, "commit", "-m", "add special realization")
    realization_file.unlink()

    assert is_realization_file_path(root, realization_file, branch="HEAD")


def test_refactor_state_sync_rejects_oracle_symlink(
    cli_repository: Path,
) -> None:
    """state 同期が regular file ではない oracle symlink を拒否する。"""
    root = cli_repository
    (root / "oracle").mkdir()
    link = root / "oracle" / "dangling.md"
    link.symlink_to("../missing.md")
    run_git(root, "add", "oracle/dangling.md")

    assert not is_oracle_file_path(root, link)
    with pytest.raises(CmocError, match="oracle/realization file"):
        sync_refactor_state(root)


def test_refactor_state_sync_preserves_history_and_requeues_changed_file(
    refactor_files: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """変更検出と要求済み file の履歴保持を、必要な内容比較だけで行う。"""
    root = refactor_files
    requested_path = root / "requested.py"
    requested_path.write_text("before\n")
    monkeypatch.setattr(
        refactor_module,
        "enumerate_refactor_targets",
        lambda _root: ["README.md", "oracle/spec.md", "requested.py"],
    )
    state = sync_refactor_state(root)
    entry = state["README.md"]
    previous_digest = file_sha256(root / "README.md")
    entry.update(
        {
            "investigation_required": False,
            "last_investigation_result": "no_findings",
            "last_investigated_sha256": previous_digest,
            "last_investigated_at": "2026-07-19_00-00-00_000",
        }
    )
    requested_entry = {
        **entry,
        "investigation_required": True,
        "last_investigation_result": "findings",
        "last_investigated_sha256": file_sha256(requested_path),
    }
    state[requested_path.name].update(requested_entry)
    write_refactor_state(root, state)
    (root / "README.md").write_text("changed\n")
    requested_path.write_text("changed too\n")
    hashed_paths: list[Path] = []

    def record_hash(path: Path) -> str:
        hashed_paths.append(path)
        return file_sha256(path)

    monkeypatch.setattr(refactor_module, "file_sha256", record_hash)

    synchronized = sync_refactor_state(root)

    assert hashed_paths == [root / "README.md"]
    assert synchronized[requested_path.name] == requested_entry
    assert synchronized["oracle/spec.md"] == state["oracle/spec.md"]
    changed = synchronized["README.md"]
    assert changed["investigation_required"] is True
    assert changed["last_investigation_result"] == "no_findings"
    assert changed["last_investigated_at"] == "2026-07-19_00-00-00_000"
    assert changed["last_investigated_sha256"] == previous_digest


@pytest.mark.parametrize("change", ["none", "target_mode", "related_mode"])
def test_refactor_state_update_requeues_changes_without_redundant_io(
    refactor_files: Path, monkeypatch: pytest.MonkeyPatch, change: str
) -> None:
    """調査履歴と再調査要求を保ち、重複保存と要求済み file の hash 比較を省く。"""
    root = refactor_files
    related = root / "related.py"
    related.write_text("VALUE = 1\n")
    paths = {"README.md", "oracle/spec.md", related.name}
    # 実列挙・追加削除・rename・commit/rollback は既存の結合 test に残す。
    monkeypatch.setattr(
        refactor_module, "enumerate_refactor_targets", lambda _root: sorted(paths)
    )
    state = sync_refactor_state(root)
    for relative, entry in state.items():
        entry.update(
            investigation_required=False,
            last_investigation_result="no_findings",
            last_investigated_sha256=file_sha256(root / relative),
            last_investigated_at="2026-10-11_00-00-00_000",
        )
    state["README.md"].update(
        investigation_required=True, last_investigation_result="findings"
    )
    write_refactor_state(root, state)

    changed = []
    if change in {"target_mode", "related_mode"}:
        relative = "README.md" if change == "target_mode" else related.name
        (root / relative).chmod(0o755)
        changed = [relative]

    def save_changed_state(root: Path, updated: RefactorState) -> None:
        assert updated != load_refactor_state(root), "state is already persisted"
        write_refactor_state(root, updated)

    hashed_paths = []

    def record_hash(path: Path) -> str:
        hashed_paths.append(path)
        return file_sha256(path)

    monkeypatch.setattr(refactor_module, "write_refactor_state", save_changed_state)
    monkeypatch.setattr(refactor_workload, "write_refactor_state", save_changed_state)
    monkeypatch.setattr(refactor_module, "file_sha256", record_hash)
    investigated_at = "2026-10-11_00-00-00_001"
    monkeypatch.setattr(refactor_workload, "timestamp", lambda: investigated_at)
    has_findings = change != "none"

    refactor_workload._update_refactor_state(
        SimpleNamespace(run_worktree=root),
        "README.md",
        state["README.md"]["last_investigated_sha256"],
        has_findings,
        changed,
    )

    updated = load_refactor_state(root)
    assert set(updated) == paths
    assert updated["README.md"] == {
        **state["README.md"],
        "investigation_required": has_findings,
        "last_investigation_result": "findings" if has_findings else "no_findings",
        "last_investigated_at": investigated_at,
    }
    assert updated["oracle/spec.md"] == state["oracle/spec.md"]
    assert updated[related.name] == {
        **state[related.name],
        "investigation_required": change == "related_mode",
    }
    assert set(hashed_paths).isdisjoint(root / relative for relative in changed)


def test_refactor_state_writer_rejects_invalid_entry(tmp_path: Path) -> None:
    """state writer が schema 不正値を保存しない。"""
    root = tmp_path
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


def test_refactor_cycle_preserves_request_and_millisecond_priority() -> None:
    """引継ぎ要求を優先し、各群で未調査・保存されたミリ秒・path の順に並べる。"""
    state: RefactorState = {
        path: {
            "investigation_required": True,
            "last_investigation_result": "not_investigated",
            "last_investigated_sha256": None,
            "last_investigated_at": None,
        }
        for path in ("README.md", "oracle/spec.md")
    }
    state["README.md"].update(
        {
            "last_investigation_result": "findings",
            "last_investigated_sha256": "0" * 64,
            "last_investigated_at": "2026-01-01_00-00-00_000",
        }
    )

    assert refactor_cycle_targets(state) == ["oracle/spec.md", "README.md"]

    state["oracle/spec.md"].update(
        {
            "last_investigation_result": "no_findings",
            "last_investigated_sha256": "0" * 64,
            "last_investigated_at": "2026-01-01_00-00-00_001",
        }
    )
    assert refactor_cycle_targets(state) == ["README.md", "oracle/spec.md"]
    state["README.md"]["last_investigated_at"] = "2026-01-01_00-00-00_002"
    assert refactor_cycle_targets(state) == ["oracle/spec.md", "README.md"]
    state["oracle/spec.md"]["last_investigated_at"] = "2026-01-01_00-00-00_002"
    assert refactor_cycle_targets(state) == ["README.md", "oracle/spec.md"]
    state["README.md"]["investigation_required"] = False
    assert refactor_cycle_targets(state) == ["oracle/spec.md", "README.md"]
    assert refactor_cycle_targets({}) == []


def test_refactor_state_rejects_parent_path_escape(tmp_path: Path) -> None:
    """refactor state の親 path escape を拒否する。"""
    root = tmp_path
    path = root / ".cmoc" / "gt" / "realization" / "refactor" / "state.json"
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


@pytest.mark.skipif(os.name != "nt", reason="Windows path semantics are unavailable")
def test_refactor_state_rejects_drive_relative_path() -> None:
    """Windows の drive-relative path を work-root 相対 path として受け入れない。"""
    assert not is_normalized_relative_path("C:outside")


@pytest.mark.parametrize("result", [[], {}])
def test_refactor_state_rejects_non_string_result(
    tmp_path: Path,
    result: object,
) -> None:
    """entry の調査結果が JSON string 以外なら schema error にする。"""
    root = tmp_path
    path = root / ".cmoc" / "gt" / "realization" / "refactor" / "state.json"
    path.parent.mkdir(parents=True)
    path.write_text(
        json.dumps(
            {
                "README.md": {
                    "investigation_required": False,
                    "last_investigation_result": result,
                    "last_investigated_sha256": "0" * 64,
                    "last_investigated_at": "2026-07-19_00-00-00_000",
                }
            }
        )
        + "\n"
    )

    with pytest.raises(CmocError, match="refactor state"):
        load_refactor_state(root)


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


def test_refactor_state_sync_treats_uppercase_digest_as_same_content(
    refactor_files: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """大文字 hex の既存履歴を同じ SHA256 として同期する。"""
    root = refactor_files
    monkeypatch.setattr(
        refactor_module,
        "enumerate_refactor_targets",
        lambda _root: ["README.md", "oracle/spec.md"],
    )
    state = sync_refactor_state(root)
    digest = file_sha256(root / "README.md")
    state["README.md"].update(
        {
            "investigation_required": False,
            "last_investigation_result": "no_findings",
            "last_investigated_sha256": digest.upper(),
            "last_investigated_at": "2026-07-19_00-00-00_000",
        }
    )
    state_path = root / ".cmoc" / "gt" / "realization" / "refactor" / "state.json"
    state_path.write_text(json.dumps(state) + "\n")

    synchronized = sync_refactor_state(root)

    assert synchronized["README.md"]["investigation_required"] is False
    assert synchronized["README.md"]["last_investigated_sha256"] == digest
