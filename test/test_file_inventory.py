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
from _git_support import make_repo, run_git

import commons.runtime_git as runtime_git
from cmoc_runtime import CmocError, file_sha256
from commons.runtime_git import (
    enumerate_oracle_and_realization_files,
    is_realization_file_path,
)
from commons.runtime_refactor import (
    load_refactor_state,
    sync_refactor_state,
    write_refactor_state,
)

_EXCLUDED_ROOTS = {".git", ".agents", ".codex", ".cmoc", "memo"}
_EXCLUDED_NAMES = {"AGENTS.md", "INDEX.md"}


def _make_nested_repo(path: Path) -> Path:
    """outer repository 内に独立した最小 Git working tree を作る。"""
    path.mkdir(parents=True)
    run_git(path, "init", "--template=/dev/null")
    run_git(path, "config", "user.email", "cmoc@example.invalid")
    run_git(path, "config", "user.name", "cmoc test")
    run_git(path, "config", "commit.gpgsign", "false")
    run_git(path, "config", "core.hooksPath", "/dev/null")
    run_git(path, "config", "core.excludesFile", "/dev/null")
    (path / "nested.txt").write_text("nested\n")
    run_git(path, "add", "nested.txt")
    run_git(path, "commit", "-m", "initial nested")
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
    """fixture 全体を物理 glob し、候補ごとの Git 判定で基準集合を作る。"""
    metadata_roots = tuple(repository / ".git" for repository in nested_repositories)
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
        owning_relative = path.relative_to(owning_repository).as_posix()
        ignored = subprocess.run(
            ["git", "check-ignore", "-q", "--", f"./{owning_relative}"],
            cwd=owning_repository,
            check=False,
        )
        if ignored.returncode == 0:
            continue
        if ignored.returncode != 1:
            raise AssertionError(f"reference check-ignore failed for {path}")
        if stat.S_ISLNK(mode):
            raise AssertionError(f"reference fixture contains a special file: {path}")
        if path.name in _EXCLUDED_NAMES:
            continue

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
    tmp_path: Path,
) -> None:
    """最適化列挙と state entry・SHA 更新を full glob 基準へ一致させる。"""
    root = make_repo(tmp_path)
    (root / ".gitignore").write_text("ignored/\n.venv/\n*.outer\n")
    ignored = root / "ignored"
    ignored.mkdir()
    (ignored / "tracked.txt").write_text("tracked ignored\n")
    (ignored / "untracked.txt").write_text("untracked ignored\n")
    (root / "visible.txt").write_text("visible\n")
    excluded_names = (
        "AGENTS.md",
        "INDEX.md",
        "oracle/AGENTS.md",
        "oracle/INDEX.md",
    )
    for relative in excluded_names:
        (root / relative).write_text("excluded from inventory\n")
    run_git(
        root,
        "add",
        "-f",
        ".gitignore",
        "ignored/tracked.txt",
        *excluded_names,
    )
    run_git(root, "commit", "-m", "add ignored fixture")

    nested = _make_nested_repo(root / "nested")
    (nested / ".gitignore").write_text("*.nested\n")
    (nested / "kept.outer").write_text("nested rule owns this file\n")
    (nested / "dropped.nested").write_text("ignored by nested\n")
    run_git(nested, "add", ".gitignore")
    run_git(nested, "commit", "-m", "add nested ignore")

    expected = _full_glob_reference(root, (nested,))
    actual = _relative_sets(root, enumerate_oracle_and_realization_files(root))

    assert actual == expected
    assert "ignored/tracked.txt" in actual[1]
    assert "ignored/untracked.txt" not in actual[1]
    assert "visible.txt" in actual[1]
    assert "nested/kept.outer" in actual[1]
    assert "nested/dropped.nested" not in actual[1]
    assert set(excluded_names).isdisjoint(actual[0] | actual[1])

    state = sync_refactor_state(root)
    assert set(state) == expected[0] | expected[1]
    for relative, entry in state.items():
        entry.update(
            {
                "investigation_required": False,
                "last_investigation_result": "no_findings",
                "last_investigated_sha256": file_sha256(root / relative),
                "last_investigated_at": "2026-08-08_00-00_00_000000000",
            }
        )
    previous_readme_digest = state["README.md"]["last_investigated_sha256"]
    write_refactor_state(root, state)

    # ignored directory 内の untracked symlink は regular file の state を変えない。
    venv_bin = root / ".venv" / "bin"
    venv_bin.mkdir(parents=True)
    (venv_bin / "python").symlink_to(root / "missing-python")
    expected_with_symlink = _full_glob_reference(root, (nested,))

    assert _relative_sets(root, enumerate_oracle_and_realization_files(root)) == (
        expected_with_symlink
    )
    assert sync_refactor_state(root) == state

    (root / "README.md").write_text("changed\n")
    (root / "visible.txt").unlink()
    (root / "added.txt").write_text("added\n")
    expected_after = _full_glob_reference(root, (nested,))
    synchronized = sync_refactor_state(root)

    assert set(synchronized) == expected_after[0] | expected_after[1]
    assert "visible.txt" not in synchronized
    assert synchronized["added.txt"]["last_investigated_sha256"] is None
    assert synchronized["README.md"]["investigation_required"] is True
    assert (
        synchronized["README.md"]["last_investigated_sha256"] == previous_readme_digest
    )
    assert synchronized["oracle/spec.md"]["investigation_required"] is False


def test_refactor_state_sync_round_trips_non_utf8_filename(tmp_path: Path) -> None:
    """非 UTF-8 filename も列挙結果と state entry を保持する。"""
    root = make_repo(tmp_path)
    invalid_name = os.fsdecode(b"non-utf8-\xff.txt")
    invalid_path = root / invalid_name
    invalid_path.write_bytes(b"non-utf8 filename\n")

    state = sync_refactor_state(root)

    assert invalid_name in state
    assert load_refactor_state(root) == state


def test_inventory_prunes_only_exact_roots_and_verified_nested_git_metadata(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """exact root は走査せず、nested の同名 path と fake `.git` は保持する。"""
    root = make_repo(tmp_path)
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
    root = make_repo(tmp_path)
    path = root / (".agents" if location == "root-boundary" else "special")

    with _special_path(path, kind):
        with pytest.raises(CmocError, match="oracle/realization file"):
            enumerate_oracle_and_realization_files(root)


@pytest.mark.skipif(not hasattr(os, "mkfifo"), reason="named pipes are unavailable")
def test_inventory_rejects_ignored_fifo_in_unpruned_area(tmp_path: Path) -> None:
    """unpruned 領域の FIFO は ignore 対象でも列挙エラーにする。"""
    root = make_repo(tmp_path)
    (root / ".gitignore").write_text("special\n")
    path = root / "special"

    with _special_path(path, "fifo"):
        with pytest.raises(CmocError, match="oracle/realization file"):
            enumerate_oracle_and_realization_files(root)


@pytest.mark.parametrize("status", ["tracked", "unignored"])
def test_inventory_rejects_symlink_not_confirmed_untracked_and_ignored(
    tmp_path: Path, status: str
) -> None:
    """tracked または unignored な symlink を列挙エラーにする。"""
    root = make_repo(tmp_path)
    link = root / "candidate.link"
    if status == "tracked":
        (root / ".gitignore").write_text("*.link\n")
    link.symlink_to(root / "missing-target")
    if status == "tracked":
        run_git(root, "add", "-f", ".gitignore", "candidate.link")
        run_git(root, "commit", "-m", "add tracked symlink")

    with pytest.raises(CmocError, match="oracle/realization file"):
        enumerate_oracle_and_realization_files(root)


def test_inventory_rejects_symlink_when_ignore_status_is_unknown(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Git が ignore 状態を返せない symlink を列挙エラーにする。"""
    root = make_repo(tmp_path)
    (root / ".gitignore").write_text("*.link\n")
    (root / "candidate.link").symlink_to(root / "missing-target")
    original_run = runtime_git.subprocess.run

    def failing_check_ignore(
        *args: object, **kwargs: object
    ) -> subprocess.CompletedProcess:
        """一括 ignore 判定だけを失敗させる。"""
        command = args[0]
        if (
            isinstance(command, list)
            and command
            and command[0] == "git"
            and "check-ignore" in command
        ):
            return subprocess.CompletedProcess(
                command,
                128,
                stdout=b"",
                stderr=b"simulated check-ignore failure",
            )
        return original_run(*args, **kwargs)

    monkeypatch.setattr(runtime_git.subprocess, "run", failing_check_ignore)

    with pytest.raises(CmocError, match="Git ignore"):
        enumerate_oracle_and_realization_files(root)


@pytest.mark.parametrize("target_location", ["inside", "outside"])
def test_inventory_does_not_follow_ignored_symlink_target(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    target_location: str,
) -> None:
    """work-root 内外の symlink 参照先を link 経由で走査しない。"""
    root = make_repo(tmp_path)
    (root / ".gitignore").write_text("*.link\n")
    target = root / "target" if target_location == "inside" else tmp_path / "target"
    target.mkdir()
    (target / "payload.txt").write_text("payload\n")
    link = root / "ignored.link"
    link.symlink_to(target, target_is_directory=True)
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

    assert link.absolute() not in scanned
    assert all(
        not relative.startswith("ignored.link/") for relative in realization_files
    )
    if target_location == "inside":
        assert "target/payload.txt" in realization_files
    else:
        assert target.absolute() not in scanned


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
    root = make_repo(tmp_path)
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


def test_inventory_accepts_linked_worktree_git_file(tmp_path: Path) -> None:
    """linked worktree の regular `.git` metadata file を pruning する。"""
    root = make_repo(tmp_path)
    linked = tmp_path / "linked"
    run_git(root, "worktree", "add", "-b", "linked", str(linked), "HEAD")

    assert (linked / ".git").is_file()
    oracle_files, realization_files = _relative_sets(
        linked, enumerate_oracle_and_realization_files(linked)
    )

    assert oracle_files == {"oracle/spec.md"}
    assert realization_files == {"README.md"}


def test_inventory_uses_all_ignore_sources_in_each_repository(tmp_path: Path) -> None:
    """root・nested の ignore source を owning repository ごとに反映する。"""
    root = make_repo(tmp_path)
    outer_global = tmp_path / "outer-global-ignore"
    outer_global.write_text("outer-global.txt\n")
    run_git(root, "config", "core.excludesFile", str(outer_global))
    (root / ".gitignore").write_text("outer-root.txt\n")
    subdirectory = root / "subdirectory"
    subdirectory.mkdir()
    (subdirectory / ".gitignore").write_text("outer-nested.txt\n")
    outer_exclude = root / Path(
        run_git(root, "rev-parse", "--git-path", "info/exclude").stdout.strip()
    )
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
    (nested / ".gitignore").write_text("nested-root.txt\n")
    nested_subdirectory = nested / "subdirectory"
    nested_subdirectory.mkdir()
    (nested_subdirectory / ".gitignore").write_text("nested-child.txt\n")
    nested_exclude = nested / Path(
        run_git(nested, "rev-parse", "--git-path", "info/exclude").stdout.strip()
    )
    nested_exclude.parent.mkdir(parents=True, exist_ok=True)
    nested_exclude.write_text("nested-local.txt\n")
    for relative in (
        "nested-root.txt",
        "nested-global.txt",
        "nested-local.txt",
        "subdirectory/nested-child.txt",
    ):
        (nested / relative).write_text("ignored\n")
    (nested / "outer-root.txt").write_text("outer rules must not leak\n")

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
    }
    assert ignored_paths.isdisjoint(realization_files)
    assert "nested/outer-root.txt" in realization_files


@pytest.mark.parametrize("duplicate_kind", ["exact", "lexical-alias"])
def test_inventory_validates_duplicate_global_ignore_source_once(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, duplicate_kind: str
) -> None:
    """同一 global ignore source の検証を一度の列挙で重複させない。"""
    root = make_repo(tmp_path)
    global_ignore = tmp_path / "global-ignore"
    global_ignore.write_text("ignored.txt\n")
    duplicate = global_ignore
    if duplicate_kind == "lexical-alias":
        alias_directory = global_ignore.parent / "alias-directory"
        alias_directory.mkdir()
        duplicate = alias_directory / ".." / global_ignore.name
    run_git(root, "config", "--local", "--add", "core.excludesFile", str(global_ignore))
    run_git(root, "config", "--local", "--add", "core.excludesFile", str(duplicate))
    (root / "ignored.txt").write_text("ignored\n")

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

    assert "ignored.txt" not in realization_files
    assert validated.count(global_ignore) == 1


def test_single_path_classifier_uses_nested_repository_context(tmp_path: Path) -> None:
    """単一 path 分類も最内側 repository の ignore と metadata 境界を使う。"""
    root = make_repo(tmp_path)
    (root / ".gitignore").write_text("*.outer\n")
    nested = _make_nested_repo(root / "nested")
    (nested / ".gitignore").write_text("*.nested\n")
    kept = nested / "kept.outer"
    dropped = nested / "dropped.nested"
    kept.write_text("kept\n")
    dropped.write_text("dropped\n")

    assert is_realization_file_path(root, kept)
    assert not is_realization_file_path(root, dropped)
    assert not is_realization_file_path(root, nested / ".git" / "config")


@pytest.mark.parametrize("candidate_kind", ["regular-file", "ignored-symlink"])
def test_inventory_git_work_is_constant_when_only_candidate_count_grows(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    candidate_kind: str,
) -> None:
    """候補 regular file・symlink 数の増加で Git 処理量を増やさない。"""
    root = make_repo(tmp_path)
    source = root / "source"
    source.mkdir()
    (root / ".gitignore").write_text("*.link\n")

    def add_candidate(name: str) -> None:
        """性能 fixture に指定種別の候補を一つ追加する。"""
        if candidate_kind == "regular-file":
            (source / f"{name}.txt").write_text(f"{name}\n")
        else:
            (source / f"{name}.link").symlink_to(root / "missing-target")

    add_candidate("one")

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

    enumerate_oracle_and_realization_files(root)
    first_counts = (git_calls, source_validations, traversals)
    git_calls = 0
    source_validations = 0
    traversals = 0

    for index in range(50):
        add_candidate(f"candidate-{index}")
    enumerate_oracle_and_realization_files(root)

    assert (git_calls, source_validations, traversals) == first_counts
    assert source_validations == 1
