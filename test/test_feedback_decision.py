"""feedback の判定根拠が依存設定と nested realization を含むことを検証する。"""

from pathlib import Path
from types import SimpleNamespace

import pytest

from sub_commands.feedback import decision


@pytest.mark.parametrize(
    "changed",
    [
        ".cmoc/gt/config.json",
        ".cmoc/gt/realization/refactor/state.json",
        "nested/source.py",
    ],
)
def test_basis_captures_tracked_configuration_and_nested_inputs(
    tmp_path, monkeypatch, changed
):
    paths = [
        "README.md",
        ".cmoc/gt/config.json",
        ".cmoc/gt/realization/refactor/state.json",
        "nested/source.py",
    ]
    runtime_paths = [
        ".cmoc/gu/log/codex/call.json",
        ".cmoc/gu/editor_input/input.md",
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
    assert set(before) == set(paths)
    (tmp_path / changed).write_text("new\n")
    after = decision.worktree_inputs(tmp_path)
    assert before["README.md"] == after["README.md"]
    assert before[changed] != after[changed]


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


def test_basis_includes_nonmetadata_nested_git_named_inputs(tmp_path, monkeypatch):
    path = tmp_path / "nested" / "fake" / ".git" / "kept.txt"
    path.parent.mkdir(parents=True)
    path.write_text("old\n")

    def fake_run_git(args, *_args, **_kwargs):
        if args[0] == "ls-files":
            return SimpleNamespace(stdout="nested/fake/.git/kept.txt\0", returncode=0)
        return SimpleNamespace(stdout="", returncode=1)

    monkeypatch.setattr(decision, "run_git", fake_run_git)
    monkeypatch.setattr(
        decision,
        "enumerate_oracle_and_realization_files",
        lambda _root: ([], [path]),
    )

    before = decision.worktree_inputs(tmp_path)
    path.write_text("new\n")
    after = decision.worktree_inputs(tmp_path)

    assert set(before) == {"nested/fake/.git/kept.txt"}
    assert before != after


def test_basis_excludes_verified_nested_git_metadata(tmp_path, monkeypatch):
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

    assert set(decision.worktree_inputs(tmp_path)) == {"nested/fake/.git/kept.txt"}


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
