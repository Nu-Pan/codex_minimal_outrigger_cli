"""oracle/realization file の full-tree 列挙契約を検証する。

正本仕様:
- `{{work-root}}/oracle/doc/app_spec/oracle_and_realization_file_enumeration.md`
- `{{work-root}}/oracle/doc/app_spec/sub_command/realization_refactor.md`
"""

import os
import stat
import subprocess
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path

import pytest
from _git_support import RUN_BRANCH, init_repo, run_git

import commons.runtime_git as runtime_git
import commons.runtime_refactor as runtime_refactor
from cmoc_runtime import CmocError
from commons.runtime_git import (
    enumerate_oracle_and_realization_files,
    is_oracle_file_path,
    is_realization_file_path,
)
from commons.runtime_refactor import (
    load_refactor_state,
    sync_refactor_state,
    write_refactor_state,
)

_EXCLUDED_ROOTS = {".git", ".agents", ".codex", ".cmoc", "memo"}
_EXCLUDED_NAMES = {"AGENTS.md"}


# 列挙と ignore 判定には実 index を使い、HEAD と linked worktree の検証だけ commit する。
def _make_nested_repo(path: Path) -> Path:
    """owning repository の判定に必要な nested Git working tree だけを作る。"""
    path.mkdir(parents=True)
    init_repo(path)
    return path


def _relative_sets(
    root: Path, inventory: tuple[list[Path], list[Path]]
) -> tuple[set[str], set[str]]:
    """absolute inventory を assertion 用の work-root 相対集合へ変換する。"""
    oracle_files, realization_files = inventory
    return (
        {path.relative_to(root).as_posix() for path in oracle_files},
        {path.relative_to(root).as_posix() for path in realization_files},
    )


def _full_glob_reference(
    root: Path, nested_repositories: tuple[Path, ...] = ()
) -> tuple[set[str], set[str]]:
    """fixture 全体を物理 glob し、repository ごとの Git 判定で基準集合を作る。"""
    # 製品の pruning・分類処理は使わず、Git への問い合わせだけをまとめる。
    metadata_roots = tuple(repository / ".git" for repository in nested_repositories)
    candidates_by_repository: dict[Path, list[tuple[Path, int]]] = {}
    oracle_files: set[str] = set()
    realization_files: set[str] = set()
    for path in root.rglob("*"):
        relative = path.relative_to(root)
        if relative.parts[0] in _EXCLUDED_ROOTS:
            if len(relative.parts) == 1:
                mode = path.lstat().st_mode
                if not stat.S_ISDIR(mode) and not stat.S_ISREG(mode):
                    raise AssertionError(
                        f"reference pruning boundary is nonregular: {path}"
                    )
            continue
        if path in metadata_roots:
            mode = path.lstat().st_mode
            if not stat.S_ISDIR(mode) and not stat.S_ISREG(mode):
                raise AssertionError(
                    f"reference nested Git metadata is nonregular: {path}"
                )
            continue
        if any(metadata in path.parents for metadata in metadata_roots):
            continue

        mode = path.lstat().st_mode
        if stat.S_ISDIR(mode):
            continue
        if not stat.S_ISREG(mode) and not stat.S_ISLNK(mode):
            raise AssertionError(f"reference fixture contains a special file: {path}")

        owning_repository = max(
            (
                repository
                for repository in (root, *nested_repositories)
                if path == repository or repository in path.parents
            ),
            key=lambda repository: len(repository.parts),
        )
        candidates_by_repository.setdefault(owning_repository, []).append((path, mode))

    for repository, candidates in candidates_by_repository.items():
        payload = b"".join(
            os.fsencode(f"./{path.relative_to(repository).as_posix()}") + b"\0"
            for path, _ in candidates
        )
        ignored = subprocess.run(
            ["git", "check-ignore", "--stdin", "-z"],
            cwd=repository,
            input=payload,
            capture_output=True,
            check=False,
        )
        if ignored.returncode not in {0, 1}:
            raise AssertionError(f"reference check-ignore failed for {repository}")
        ignored_paths = {
            repository / os.fsdecode(relative)
            for relative in ignored.stdout.split(b"\0")
            if relative
        }
        for path, mode in candidates:
            if path in ignored_paths:
                continue
            if stat.S_ISLNK(mode):
                raise AssertionError(
                    f"reference fixture contains a special file: {path}"
                )
            if path.name in _EXCLUDED_NAMES:
                continue

            relative = path.relative_to(root)
            if relative.parts[0] == "oracle":
                oracle_files.add(relative.as_posix())
            else:
                realization_files.add(relative.as_posix())
    return oracle_files, realization_files


@contextmanager
def _special_path(path: Path, kind: str) -> Iterator[None]:
    """symlink または FIFO の検証対象を一時的に保持する。"""
    if kind == "symlink":
        path.symlink_to(path.parent / "missing")
    elif kind == "fifo":
        os.mkfifo(path)
    else:
        raise AssertionError(kind)
    yield


def test_inventory_matches_full_glob_and_refactor_state_hash_updates(
    cli_repository: Path,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """最適化列挙と state entry・SHA 更新を full glob 基準へ一致させる。"""
    root = cli_repository
    (root / "README.md").write_text("# repo\n")
    (root / "oracle").mkdir()
    (root / "oracle" / "spec.md").write_text("# spec\n")
    (root / ".gitignore").write_text("ignored/\n.venv/\n*.outer\n")
    ignored = root / "ignored"
    ignored.mkdir()
    (ignored / "tracked.txt").write_text("tracked ignored\n")
    (ignored / "untracked.txt").write_text("untracked ignored\n")
    (root / "visible.txt").write_text("visible\n")
    classification_names = (
        "AGENTS.md",
        "notes.md",
        "oracle/AGENTS.md",
        "oracle/notes.md",
    )
    for relative in classification_names:
        (root / relative).write_text("name classification fixture\n")
    run_git(
        root,
        "add",
        "-f",
        "README.md",
        "oracle/spec.md",
        ".gitignore",
        "ignored/tracked.txt",
        *classification_names,
    )

    # nested の regular `.git` file も state と full glob の同じ比較で検証する。
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
    assert (nested / ".git").is_file()
    (nested / ".gitignore").write_text("*.nested\n")
    (nested / "kept.outer").write_text("nested rule owns this file\n")
    (nested / "dropped.nested").write_text("ignored by nested\n")
    # nested index でも、ignore pattern に一致する tracked file を保持する。
    (nested / "tracked.nested").write_text("tracked ignored by nested\n")
    run_git(nested, "add", "-f", "tracked.nested")

    state = sync_refactor_state(root)
    for relative, entry in state.items():
        entry.update(
            {
                "last_investigated_at": "2026-08-08_00-00-00_000",
            }
        )
    write_refactor_state(root, state)

    # ignored directory 内の untracked symlink は regular file の state を変えない。
    venv_bin = root / ".venv" / "bin"
    venv_bin.mkdir(parents=True)
    (venv_bin / "python").symlink_to(root / "missing-python")

    # state 同期が実際に消費した列挙結果を記録し、比較のためだけの再列挙を省く。
    inventories: list[tuple[list[Path], list[Path]]] = []

    def recording_inventory(work_root: Path) -> tuple[list[Path], list[Path]]:
        inventory = enumerate_oracle_and_realization_files(work_root)
        inventories.append(inventory)
        return inventory

    monkeypatch.setattr(
        runtime_refactor, "enumerate_oracle_and_realization_files", recording_inventory
    )
    assert sync_refactor_state(root) == state

    # symlink 追加後の分類結果を full glob と照合し、追加前の state の集合も確認する。
    expected = _full_glob_reference(root, (nested,))
    actual = _relative_sets(root, inventories[-1])
    assert actual == expected

    assert "ignored/tracked.txt" in actual[1]
    assert "ignored/untracked.txt" not in actual[1]
    assert "visible.txt" in actual[1]
    assert "nested/kept.outer" in actual[1]
    assert "nested/dropped.nested" not in actual[1]
    assert "nested/tracked.nested" in actual[1]
    assert "nested/.git" not in actual[1]
    assert {"AGENTS.md", "oracle/AGENTS.md"}.isdisjoint(actual[0] | actual[1])
    assert "notes.md" in actual[1]
    assert "oracle/notes.md" in actual[0]
    assert set(state) == actual[0] | actual[1]

    (root / "README.md").write_text("changed\n")
    (root / "visible.txt").unlink()
    (root / "added.txt").write_text("added\n")
    # ignore 規則と index は不変なので、基準集合へ既知の追加・削除だけ反映する。
    expected_after = (expected[0] | expected[1] | {"added.txt"}) - {"visible.txt"}
    synchronized = sync_refactor_state(root)

    assert set(synchronized) == expected_after
    assert "visible.txt" not in synchronized
    assert synchronized["added.txt"] == {"last_investigated_at": None}
    assert synchronized["README.md"] == state["README.md"]
    assert synchronized["oracle/spec.md"] == state["oracle/spec.md"]


def test_realization_classifier_uses_nested_head_for_deleted_file(
    cli_repository: Path,
) -> None:
    """nested repository の削除 path を outer run branch で分類しない。"""
    root = cli_repository
    nested = _make_nested_repo(root / "nested")
    target = nested / "nested.txt"
    target.write_text("nested\n")
    run_git(nested, "add", "nested.txt")
    run_git(nested, "commit", "-m", "initial nested")
    target.unlink()

    assert is_realization_file_path(
        root,
        target,
        branch=RUN_BRANCH,
        fallback_branch="outer-fork",
    )
    assert not is_realization_file_path(
        root,
        nested / "missing.txt",
        branch=RUN_BRANCH,
        fallback_branch="outer-fork",
    )


def test_refactor_state_sync_round_trips_non_utf8_filename(
    cli_repository: Path,
) -> None:
    """非 UTF-8 filename も列挙結果と state entry を保持する。"""
    root = cli_repository
    invalid_name = os.fsdecode(b"non-utf8-\xff.txt")
    invalid_path = root / invalid_name
    invalid_path.write_bytes(b"non-utf8 filename\n")

    state = sync_refactor_state(root)

    assert invalid_name in state
    assert load_refactor_state(root) == state


def test_inventory_does_not_traverse_excluded_roots_or_ignored_symlinks(
    cli_repository: Path,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """除外 root と link へ降りず、nested の同名 path と fake `.git` は保持する。"""
    root = cli_repository
    for name in (".agents", ".codex", ".cmoc", "memo"):
        excluded = root / name
        excluded.mkdir()
        (excluded / "unvisited").symlink_to(excluded / "missing")

    nested = root / "nested"
    for name in (".agents", ".codex", ".cmoc", "memo"):
        included = nested / name
        included.mkdir(parents=True)
        (included / "kept.txt").write_text("kept\n")
    fake_metadata = nested / "fake" / ".git"
    fake_metadata.mkdir(parents=True)
    (fake_metadata / "kept.txt").write_text("not repository metadata\n")
    fake_metadata_file = nested / "fake-file" / ".git"
    fake_metadata_file.parent.mkdir(parents=True)
    fake_metadata_file.write_text("not repository metadata\n")

    # 同じ走査で work-root 内外の link も検査し、repository と列挙の準備を共有する。
    (root / ".gitignore").write_text("*.link\n")
    links: list[Path] = []
    for location, target in (
        ("inside", root / "target"),
        ("outside", tmp_path / "target"),
    ):
        target.mkdir()
        (target / "payload.txt").write_text("payload\n")
        link = root / f"ignored-{location}.link"
        link.symlink_to(target, target_is_directory=True)
        links.append(link)

    scanned: list[Path] = []
    original_scandir = runtime_git.os.scandir

    def recording_scandir(path: Path) -> Iterator[os.DirEntry[str]]:
        """走査された directory を記録して実処理へ委譲する。"""
        scanned.append(Path(path).absolute())
        return original_scandir(path)

    monkeypatch.setattr(runtime_git.os, "scandir", recording_scandir)

    _, realization_files = _relative_sets(
        root, enumerate_oracle_and_realization_files(root)
    )

    expected_nested = {
        f"nested/{name}/kept.txt" for name in (".agents", ".codex", ".cmoc", "memo")
    }
    assert expected_nested <= realization_files
    assert "nested/fake/.git/kept.txt" in realization_files
    assert "nested/fake-file/.git" in realization_files
    assert all(root / name not in scanned for name in _EXCLUDED_ROOTS)

    for link in links:
        assert link.absolute() not in scanned
        assert all(
            not relative.startswith(f"{link.name}/") for relative in realization_files
        )
    assert "target/payload.txt" in realization_files
    assert (tmp_path / "target").absolute() not in scanned


@pytest.mark.parametrize(
    ("kind", "location"),
    [
        ("symlink", "root-boundary"),
        pytest.param(
            "fifo",
            "root-boundary",
            marks=pytest.mark.skipif(
                not hasattr(os, "mkfifo"), reason="named pipes are unavailable"
            ),
        ),
        pytest.param(
            "fifo",
            "unpruned",
            marks=pytest.mark.skipif(
                not hasattr(os, "mkfifo"), reason="named pipes are unavailable"
            ),
        ),
    ],
)
def test_inventory_rejects_nonregular_paths(
    tmp_path: Path, kind: str, location: str
) -> None:
    """pruning 境界と通常走査領域の非通常 file を列挙エラーにする。"""
    # 種類の拒否は Git 判定より前なので、repository と index は用意しない。
    root = tmp_path
    path = root / (".agents" if location == "root-boundary" else "special")

    with _special_path(path, kind):
        with pytest.raises(CmocError, match="oracle/realization file"):
            enumerate_oracle_and_realization_files(root)


@pytest.mark.skipif(not hasattr(os, "mkfifo"), reason="named pipes are unavailable")
def test_inventory_rejects_ignored_fifo_in_unpruned_area(tmp_path: Path) -> None:
    """unpruned 領域の FIFO は ignore 対象でも列挙エラーにする。"""
    # FIFO は ignore 判定より先に拒否するため、Git repository は不要。
    root = tmp_path
    (root / ".gitignore").write_text("special\n")
    path = root / "special"

    with _special_path(path, "fifo"):
        with pytest.raises(CmocError, match="oracle/realization file"):
            enumerate_oracle_and_realization_files(root)


@pytest.mark.parametrize("status", ["tracked", "unignored"])
def test_inventory_and_state_sync_reject_unignored_or_tracked_symlink(
    cli_repository: Path, status: str
) -> None:
    """tracked または unignored な oracle symlink を分類・state 同期で拒否する。"""
    root = cli_repository
    (root / "oracle").mkdir()
    link = root / "oracle" / "candidate.link"
    if status == "tracked":
        (root / ".gitignore").write_text("*.link\n")
    link.symlink_to(root / "missing-target")
    if status == "tracked":
        run_git(root, "add", "-f", ".gitignore", "oracle/candidate.link")

    # 列挙の拒否が state 同期まで伝わることも、同じ実 index と link で検査する。
    assert not is_oracle_file_path(root, link)
    with pytest.raises(CmocError, match="oracle/realization file"):
        sync_refactor_state(root)


def test_inventory_rejects_symlink_when_ignore_status_is_unknown(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Git が ignore 状態を返せない symlink を列挙エラーにする。"""
    # 実 Git と ignore source の結合は隣接ケースと test_runtime_git_ignore.py に残す。
    # ここでは source 検証後の故障応答だけを渡し、repository の準備を省く。
    root = tmp_path
    (root / "candidate.link").symlink_to(root / "missing-target")
    monkeypatch.setattr(
        runtime_git, "_validate_git_ignore_sources", lambda *_args: None
    )

    def failing_check_ignore(
        command: list[str], **_kwargs: object
    ) -> subprocess.CompletedProcess:
        """一括 ignore 判定だけを失敗させる。"""
        return subprocess.CompletedProcess(
            command,
            128,
            stdout=b"",
            stderr=b"simulated check-ignore failure",
        )

    monkeypatch.setattr(runtime_git.subprocess, "run", failing_check_ignore)

    with pytest.raises(CmocError, match="Git ignore"):
        enumerate_oracle_and_realization_files(root)


@pytest.mark.parametrize(
    "mode",
    [stat.S_IFSOCK | 0o600, stat.S_IFCHR | 0o600, stat.S_IFBLK | 0o600],
)
@pytest.mark.parametrize("location", ["root-boundary", "unpruned"])
def test_inventory_rejects_simulated_socket_and_device_modes(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    mode: int,
    location: str,
) -> None:
    """socket・device 相当 mode を pruning 境界と通常領域の両方で拒否する。"""
    # 実在する通常 file の mode だけを置き換え、Git を使わず種類の拒否を検証する。
    root = tmp_path
    path = root / (".agents" if location == "root-boundary" else "special")
    path.write_text("mode probe\n")
    original_lstat = runtime_git._lstat_directory_entries

    def simulated_lstat(directory: Path) -> list[tuple[Path, int]]:
        """対象 entry だけを非通常 mode として traversal へ渡す。"""
        return [
            (entry_path, mode if entry_path == path else entry_mode)
            for entry_path, entry_mode in original_lstat(directory)
        ]

    monkeypatch.setattr(runtime_git, "_lstat_directory_entries", simulated_lstat)

    with pytest.raises(CmocError, match="oracle/realization file"):
        enumerate_oracle_and_realization_files(root)


def test_inventory_accepts_linked_worktree_git_file(
    committed_repository: Path, tmp_path: Path
) -> None:
    """linked worktree の regular `.git` metadata file を pruning する。"""
    # HEAD は worktree 作成だけに使い、列挙対象は linked 側へ直接用意する。
    root = committed_repository
    linked = tmp_path / "linked"
    run_git(root, "worktree", "add", "-b", "linked", str(linked), "HEAD")
    (linked / "README.md").write_text("# repo\n")
    (linked / "oracle").mkdir()
    (linked / "oracle" / "spec.md").write_text("# spec\n")

    assert (linked / ".git").is_file()
    oracle_files, realization_files = _relative_sets(
        linked, enumerate_oracle_and_realization_files(linked)
    )

    assert oracle_files == {"oracle/spec.md"}
    assert realization_files == {"README.md"}


def test_inventory_and_classifier_use_owning_repository_ignore_sources(
    tmp_path: Path,
    cli_repository: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """owning repository の ignore source を反映し、重複 source は一度だけ検証する。"""
    root = cli_repository
    outer_global = tmp_path / "outer-global-ignore"
    outer_global.write_text("outer-global.txt\n")
    run_git(root, "config", "core.excludesFile", str(outer_global))
    # 同じ source の同一表記・別表記も、この repository の列挙で検証する。
    alias_directory = tmp_path / "alias-directory"
    alias_directory.mkdir()
    alias = alias_directory / ".." / outer_global.name
    for source in (outer_global, alias):
        run_git(root, "config", "--local", "--add", "core.excludesFile", str(source))
    (root / ".gitignore").write_text("outer-root.txt\n*.outer\n")
    subdirectory = root / "subdirectory"
    subdirectory.mkdir()
    (subdirectory / ".gitignore").write_text("outer-nested.txt\n")
    # 両 repository は init_repo が通常の .git directory を作るため、配置の問い合わせは不要。
    outer_exclude = root / ".git" / "info" / "exclude"
    outer_exclude.parent.mkdir(parents=True, exist_ok=True)
    outer_exclude.write_text("outer-local.txt\n")
    for relative in (
        "outer-root.txt",
        "outer-global.txt",
        "outer-local.txt",
        "subdirectory/outer-nested.txt",
    ):
        (root / relative).write_text("ignored\n")

    nested = _make_nested_repo(root / "nested")
    nested_global = tmp_path / "nested-global-ignore"
    nested_global.write_text("nested-global.txt\n")
    run_git(nested, "config", "core.excludesFile", str(nested_global))
    (nested / ".gitignore").write_text("nested-root.txt\n*.nested\n")
    nested_subdirectory = nested / "subdirectory"
    nested_subdirectory.mkdir()
    (nested_subdirectory / ".gitignore").write_text("nested-child.txt\n")
    nested_exclude = nested / ".git" / "info" / "exclude"
    nested_exclude.parent.mkdir(parents=True, exist_ok=True)
    nested_exclude.write_text("nested-local.txt\n")
    for relative in (
        "nested-root.txt",
        "nested-global.txt",
        "nested-local.txt",
        "subdirectory/nested-child.txt",
        "dropped.nested",
    ):
        (nested / relative).write_text("ignored\n")
    (nested / "outer-root.txt").write_text("outer rules must not leak\n")
    (nested / "kept.outer").write_text("kept\n")

    validated: list[Path] = []
    original_validate = runtime_git._validate_global_git_ignore_path

    def counting_validate(path: Path) -> None:
        """検証された global ignore source を記録する。"""
        validated.append(path)
        original_validate(path)

    monkeypatch.setattr(
        runtime_git, "_validate_global_git_ignore_path", counting_validate
    )

    _, realization_files = _relative_sets(
        root, enumerate_oracle_and_realization_files(root)
    )

    ignored_paths = {
        "outer-root.txt",
        "outer-global.txt",
        "outer-local.txt",
        "subdirectory/outer-nested.txt",
        "nested/nested-root.txt",
        "nested/nested-global.txt",
        "nested/nested-local.txt",
        "nested/subdirectory/nested-child.txt",
        "nested/dropped.nested",
    }
    assert ignored_paths.isdisjoint(realization_files)
    assert "nested/outer-root.txt" in realization_files
    assert "nested/kept.outer" in realization_files
    validated_sources = [path.resolve() for path in validated]
    assert validated_sources.count(outer_global.resolve()) == 1
    assert validated_sources.count(nested_global.resolve()) == 1

    # 同じ nested index と ignore source で、単一 path 分類の境界も検証する。
    assert is_realization_file_path(root, nested / "kept.outer")
    assert not is_realization_file_path(root, nested / "dropped.nested")
    assert not is_realization_file_path(root, nested / ".git" / "config")


def test_inventory_git_work_is_constant_when_only_candidate_count_grows(
    cli_repository: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """候補 regular file・symlink 数の増加で Git 処理量を増やさない。"""
    root = cli_repository
    source = root / "source"
    source.mkdir()
    (root / ".gitignore").write_text("*.link\n")

    def add_candidate(kind: str, name: str) -> None:
        """性能 fixture に指定種別の候補を一つ追加する。"""
        if kind == "regular-file":
            (source / f"{name}.txt").write_text(f"{name}\n")
        else:
            (source / f"{name}.link").symlink_to(root / "missing-target")

    git_calls = 0
    source_validations = 0
    traversals = 0
    original_run = runtime_git.subprocess.run
    original_validate = runtime_git._validate_git_ignore_sources
    original_scandir = runtime_git.os.scandir

    def counting_run(*args: object, **kwargs: object) -> subprocess.CompletedProcess:
        """Git subprocess の起動回数を記録する。"""
        nonlocal git_calls
        command = args[0]
        if isinstance(command, list) and command[:1] == ["git"]:
            git_calls += 1
        return original_run(*args, **kwargs)

    def counting_validate(*args: object, **kwargs: object) -> None:
        """repository 単位の ignore source 検証回数を記録する。"""
        nonlocal source_validations
        source_validations += 1
        original_validate(*args, **kwargs)

    def counting_scandir(path: Path) -> Iterator[os.DirEntry[str]]:
        """pruning 後に traversal した directory 数を記録する。"""
        nonlocal traversals
        traversals += 1
        return original_scandir(path)

    monkeypatch.setattr(runtime_git.subprocess, "run", counting_run)
    monkeypatch.setattr(runtime_git, "_validate_git_ignore_sources", counting_validate)
    monkeypatch.setattr(runtime_git.os, "scandir", counting_scandir)

    # 混在する候補集合を基準に、一度に一方の種別だけ増やして比較する。
    add_candidate("regular-file", "one")
    add_candidate("ignored-symlink", "one")
    enumerate_oracle_and_realization_files(root)
    first_counts = (git_calls, source_validations, traversals)
    assert source_validations == 1

    for kind in ("regular-file", "ignored-symlink"):
        for index in range(50):
            add_candidate(kind, f"candidate-{index}")
        git_calls = 0
        source_validations = 0
        traversals = 0

        enumerate_oracle_and_realization_files(root)

        assert (git_calls, source_validations, traversals) == first_counts, kind
        assert source_validations == 1, kind
