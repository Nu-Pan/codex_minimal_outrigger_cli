"""feedback の判定根拠が依存設定と nested realization を含むことを検証する。"""

from types import SimpleNamespace

import pytest

from sub_commands.feedback import decision


@pytest.mark.parametrize(
    "changed",
    [
        ".cmoc/gc/ar/config.json",
        ".cmoc/gc/ar/realization/refactor/state.json",
        "nested/source.py",
    ],
)
def test_basis_captures_tracked_configuration_and_nested_inputs(
    tmp_path, monkeypatch, changed
):
    paths = [
        "README.md",
        ".cmoc/gc/ar/config.json",
        ".cmoc/gc/ar/realization/refactor/state.json",
        "nested/source.py",
    ]
    for name in paths:
        path = tmp_path / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("old\n")
    monkeypatch.setattr(
        decision,
        "run_git",
        lambda *_args: SimpleNamespace(
            stdout="\0".join([*paths[:-1], "nested/"]) + "\0"
        ),
    )
    monkeypatch.setattr(
        decision,
        "enumerate_oracle_and_realization_files",
        lambda _root: ([], [tmp_path / paths[-1]]),
    )
    before = decision.worktree_inputs(tmp_path)
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
