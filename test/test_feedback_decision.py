"""feedback の判定根拠に依存設定を含め、機械生成物を除くことを検証する。"""

from collections import Counter
from pathlib import Path
from types import SimpleNamespace

import pytest

from sub_commands.feedback import decision


def test_basis_captures_tracked_configuration_and_nested_inputs(tmp_path, monkeypatch):
    paths = [
        "README.md",
        ".cmoc/gt/config.json",
        ".cmoc/gt/realization/refactor/state.json",
        "nested/source.py",
    ]
    runtime_paths = [
        ".cmoc/gu/log/codex/exec_000000_2026-09-29_15-04/cc_000000_2026-09-29_15-04_call.json",
        ".cmoc/gu/log/editor_input/exec_000000_2026-09-29_15-04_orig.md",
        ".cmoc/gu/feedback/active/current.json",
        ".cmoc/gu/state/run_processes/session.pid",
    ]
    for name in [*paths, *runtime_paths]:
        path = tmp_path / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("old\n")
    monkeypatch.setattr(
        decision,
        "run_git",
        lambda *_args: SimpleNamespace(
            stdout="\0".join([*paths[:-1], *runtime_paths, "nested/"]) + "\0"
        ),
    )
    monkeypatch.setattr(
        decision,
        "enumerate_oracle_and_realization_files",
        lambda _root: ([], [tmp_path / paths[-1]]),
    )
    before = decision.worktree_inputs(tmp_path)
    assert set(before) == set(paths) - {".cmoc/gt/realization/refactor/state.json"}
    # 準備と初回収集を共有し、各入力の変更は一つずつ検出する。
    for changed in (".cmoc/gt/config.json", "nested/source.py"):
        (tmp_path / changed).write_text("new\n")
        after = decision.worktree_inputs(tmp_path)
        assert set(after) == set(before)
        assert {name for name in before if before[name] != after[name]} == {changed}
        before = after


def test_basis_uses_git_modes_across_atomic_write_and_checkout(tmp_path, monkeypatch):
    path = tmp_path / "source.py"
    path.write_text("pass\n")
    monkeypatch.setattr(
        decision, "run_git", lambda *_args: SimpleNamespace(stdout="source.py\0")
    )
    monkeypatch.setattr(
        decision, "enumerate_oracle_and_realization_files", lambda _root: ([], [path])
    )
    path.chmod(0o600)
    before = decision.worktree_inputs(tmp_path)
    path.chmod(0o644)
    assert decision.worktree_inputs(tmp_path) == before
    path.chmod(0o755)
    assert decision.worktree_inputs(tmp_path) != before


def test_basis_excludes_only_verified_nested_git_metadata(tmp_path, monkeypatch):
    metadata = tmp_path / "nested" / ".git" / "config"
    kept = tmp_path / "nested" / "fake" / ".git" / "kept.txt"
    metadata.parent.mkdir(parents=True)
    kept.parent.mkdir(parents=True)
    metadata.write_text("metadata\n")
    kept.write_text("kept\n")

    def fake_run_git(args, cwd, *_args, **_kwargs):
        if args[0] == "ls-files":
            return SimpleNamespace(
                stdout="nested/.git/config\0nested/fake/.git/kept.txt\0",
                returncode=0,
            )
        if Path(cwd) == tmp_path / "nested":
            return SimpleNamespace(stdout=f"{cwd}\n", returncode=0)
        return SimpleNamespace(stdout="", returncode=1)

    monkeypatch.setattr(decision, "run_git", fake_run_git)
    monkeypatch.setattr(
        decision,
        "enumerate_oracle_and_realization_files",
        lambda _root: ([], [kept]),
    )

    before = decision.worktree_inputs(tmp_path)
    assert set(before) == {"nested/fake/.git/kept.txt"}
    kept.write_text("changed\n")
    after = decision.worktree_inputs(tmp_path)
    assert set(after) == set(before)
    assert before != after


def test_basis_ignores_deleted_tracked_nested_git_named_input(tmp_path, monkeypatch):
    def fake_run_git(args, *_args, **_kwargs):
        if args[0] == "ls-files":
            return SimpleNamespace(
                stdout="nested/fake/.git/deleted.txt\0", returncode=0
            )
        raise AssertionError("deleted paths must not trigger nested Git probing")

    monkeypatch.setattr(decision, "run_git", fake_run_git)
    monkeypatch.setattr(
        decision,
        "enumerate_oracle_and_realization_files",
        lambda _root: ([], []),
    )

    assert decision.worktree_inputs(tmp_path) == {}


def test_basis_rejects_git_output_path_outside_worktree(tmp_path, monkeypatch):
    outside = tmp_path / "outside.txt"
    outside.write_text("must not be read\n")
    monkeypatch.setattr(
        decision,
        "run_git",
        lambda *_args, **_kwargs: SimpleNamespace(
            stdout="../outside.txt\0", returncode=0
        ),
    )
    monkeypatch.setattr(
        decision,
        "enumerate_oracle_and_realization_files",
        lambda _root: ([], []),
    )

    with pytest.raises(ValueError, match="invalid path"):
        decision.worktree_inputs(tmp_path / "worktree")

    assert outside.read_text() == "must not be read\n"


def test_basis_checks_shared_parents_once_without_reusing_file_contents(
    tmp_path, monkeypatch
):
    paths = [
        "inputs/package/first.py",
        "inputs/package/second.py",
        "inputs/other/third.py",
    ]
    for name in paths:
        path = tmp_path / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(name)
    monkeypatch.setattr(
        decision,
        "run_git",
        lambda *_args, **_kwargs: SimpleNamespace(stdout="\0".join(paths) + "\0"),
    )
    monkeypatch.setattr(
        decision, "enumerate_oracle_and_realization_files", lambda _root: ([], [])
    )
    checks = Counter()
    original = Path.is_symlink

    def check_parent(path):
        checks[path] += 1
        return original(path)

    monkeypatch.setattr(Path, "is_symlink", check_parent)
    before = decision.worktree_inputs(tmp_path)
    assert set(before) == set(paths)
    expected = Counter(
        {tmp_path / name: 1 for name in ("inputs", "inputs/package", "inputs/other")}
    )
    assert checks == expected

    (tmp_path / paths[1]).write_text("changed\n")
    checks.clear()
    after = decision.worktree_inputs(tmp_path)
    assert checks == expected
    assert {name for name in paths if before[name] != after[name]} == {paths[1]}


@pytest.mark.parametrize("link_parent", ["inputs", "inputs/package"])
def test_basis_rejects_symlinked_parent_without_reading_target(
    tmp_path, monkeypatch, link_parent
):
    worktree = tmp_path / "worktree"
    relative = Path("inputs/package/source.py")
    outside = tmp_path / "outside"
    target = outside / relative.relative_to(link_parent)
    target.parent.mkdir(parents=True)
    target.write_text("must not be read\n")
    link = worktree / link_parent
    source = worktree / relative
    source.parent.mkdir(parents=True)
    source.write_text("source\n")
    monkeypatch.setattr(
        decision,
        "run_git",
        lambda *_args, **_kwargs: SimpleNamespace(stdout=f"{relative}\0"),
    )
    monkeypatch.setattr(
        decision, "enumerate_oracle_and_realization_files", lambda _root: ([], [])
    )

    assert set(decision.worktree_inputs(worktree)) == {relative.as_posix()}
    # 前回確認した親を symlink へ置換し、収集間で検証結果を持ち越さない。
    link.rename(tmp_path / "previous-inputs")
    link.symlink_to(outside, target_is_directory=True)

    def fail_read(_path):
        pytest.fail("symlink targets must not be read")

    monkeypatch.setattr(Path, "read_bytes", fail_read)

    with pytest.raises(ValueError, match="symlinked parent"):
        decision.worktree_inputs(worktree)


def test_basis_normalizes_relative_worktree_path(tmp_path, monkeypatch):
    worktree = tmp_path / "worktree"
    path = worktree / "source.py"
    path.parent.mkdir()
    path.write_text("source\n")
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(
        decision,
        "run_git",
        lambda *_args, **_kwargs: SimpleNamespace(stdout="source.py\0"),
    )
    monkeypatch.setattr(
        decision,
        "enumerate_oracle_and_realization_files",
        lambda root: ([], [root / "source.py"]),
    )

    assert set(decision.worktree_inputs(Path("worktree"))) == {"source.py"}
