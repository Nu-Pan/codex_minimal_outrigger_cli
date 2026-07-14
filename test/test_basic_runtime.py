"""Root/worktree と path model の runtime 契約を検証する。

根拠:
- <work-root>/oracle/src/oracle/other/path_model.py
- <work-root>/oracle/doc/app_spec/run_isolation.md
"""

import threading
from pathlib import Path

import pytest

from basic.path_model import RootPathPlaceHolder, resolve_ph_path, resolve_real_path
from cmoc_runtime import (
    CmocError,
    create_run_worktree,
    remove_worktree,
    pushd,
    repo_root,
    work_root,
)
from _git_support import make_repo, run_git


def test_path_model_resolves_token_path_inside_repo() -> None:
    """root placeholder path が repo 内の実 path から復元できる。"""
    cmoc_root = resolve_real_path(RootPathPlaceHolder.CMOC)
    token_path = resolve_ph_path(cmoc_root / "src", RootPathPlaceHolder.CMOC)

    assert token_path == Path("<cmoc-root>") / "src"


def test_make_repo_ignores_global_commit_signing_and_hooks(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    hooks = tmp_path / "hooks"
    hooks.mkdir()
    hook = hooks / "pre-commit"
    hook.write_text("#!/bin/sh\nexit 1\n")
    hook.chmod(0o755)
    global_config = tmp_path / "gitconfig"
    global_config.write_text(
        f"[commit]\n\tgpgsign = true\n[core]\n\thooksPath = {hooks}\n"
    )
    monkeypatch.setenv("GIT_CONFIG_GLOBAL", str(global_config))

    root = make_repo(tmp_path)

    assert run_git(root, "config", "--local", "commit.gpgsign").stdout == "false\n"
    assert run_git(root, "config", "--local", "core.hooksPath").stdout == "/dev/null\n"
    assert run_git(root, "rev-parse", "--verify", "HEAD").stdout.strip()


def test_runtime_distinguishes_repo_root_from_linked_worktree(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """linked worktree では repo root と run/work root を分けて扱う。"""
    root = make_repo(tmp_path)
    linked = root / ".cmoc" / "local" / "worktree" / "linked"
    run_git(root, "worktree", "add", "-b", "linked-test", str(linked), "HEAD")

    monkeypatch.chdir(linked)
    assert repo_root(linked) == root.resolve()
    assert resolve_real_path(RootPathPlaceHolder.RUN) == linked.resolve()
    assert work_root(linked) == linked.resolve()


def test_pushd_serializes_process_global_cwd_changes(tmp_path: Path) -> None:
    """並列する pushd が process-global な cwd を混線させない。"""
    first = tmp_path / "first"
    second = tmp_path / "second"
    first.mkdir()
    second.mkdir()
    original = Path.cwd()
    first_ready = threading.Event()
    second_started = threading.Event()
    second_entered = threading.Event()
    release_first = threading.Event()

    def hold_first_directory() -> None:
        with pushd(first):
            first_ready.set()
            release_first.wait(5)

    def enter_second_directory() -> None:
        first_ready.wait(5)
        second_started.set()
        with pushd(second):
            second_entered.set()

    first_thread = threading.Thread(target=hold_first_directory)
    second_thread = threading.Thread(target=enter_second_directory)
    first_thread.start()
    second_thread.start()
    try:
        assert first_ready.wait(5)
        assert second_started.wait(5)
        assert not second_entered.wait(0.1)
    finally:
        release_first.set()
        first_thread.join(5)
        second_thread.join(5)

    assert second_entered.is_set()
    assert not first_thread.is_alive()
    assert not second_thread.is_alive()
    assert Path.cwd() == original


def test_run_root_placeholder_rejects_main_worktree(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """main worktree は run root として扱わない。"""
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)

    with pytest.raises(ValueError, match="`<run-root>` was not found"):
        resolve_real_path(RootPathPlaceHolder.RUN)


def test_create_run_worktree_rejects_path_outside_managed_worktrees(
    tmp_path: Path,
) -> None:
    root = make_repo(tmp_path)
    target = tmp_path / "unrelated"
    target.mkdir()
    (target / "keep.txt").write_text("keep\n")

    with pytest.raises(CmocError, match="run worktree path"):
        create_run_worktree(root, "cmoc/apply/session/run", target)

    assert (target / "keep.txt").read_text() == "keep\n"


def test_create_run_worktree_rejects_path_not_matching_branch(
    tmp_path: Path,
) -> None:
    root = make_repo(tmp_path)
    target = root / ".cmoc" / "local" / "worktree" / "session" / "other-run"
    target.mkdir(parents=True)
    (target / "keep.txt").write_text("keep\n")

    with pytest.raises(CmocError, match="run worktree path"):
        create_run_worktree(root, "cmoc/apply/session/run", target)

    assert (target / "keep.txt").read_text() == "keep\n"


@pytest.mark.parametrize("symlink_component", ["base", "session", "target"])
def test_create_run_worktree_rejects_symlink_components(
    tmp_path: Path, symlink_component: str
) -> None:
    root = make_repo(tmp_path)
    managed = root / ".cmoc" / "local" / "worktree"
    external = tmp_path / "external"
    external.mkdir()

    if symlink_component == "base":
        managed.parent.mkdir(parents=True)
        managed.symlink_to(external, target_is_directory=True)
    else:
        managed.mkdir(parents=True)
        session = managed / "session"
        if symlink_component == "session":
            session.symlink_to(external / "session", target_is_directory=True)
        else:
            session.mkdir()
            (session / "run").symlink_to(
                external / "session" / "run", target_is_directory=True
            )

    target = managed / "session" / "run"
    with pytest.raises(CmocError, match="run worktree path"):
        create_run_worktree(root, "cmoc/apply/session/run", target)

    assert not (external / "session" / "run").exists()


def test_create_run_worktree_rejects_unregistered_managed_path(
    tmp_path: Path,
) -> None:
    root = make_repo(tmp_path)
    target = root / ".cmoc" / "local" / "worktree" / "session" / "run"
    target.mkdir(parents=True)
    (target / "keep.txt").write_text("keep\n")

    with pytest.raises(CmocError, match="run worktree path"):
        create_run_worktree(root, "cmoc/apply/session/run", target)

    assert (target / "keep.txt").read_text() == "keep\n"


def test_remove_worktree_rejects_path_outside_managed_worktrees(
    tmp_path: Path,
) -> None:
    root = make_repo(tmp_path)
    target = tmp_path / "unrelated"
    target.mkdir()
    (target / "keep.txt").write_text("keep\n")

    with pytest.raises(CmocError, match="cmoc 管理外の worktree"):
        remove_worktree(root, target)

    assert (target / "keep.txt").read_text() == "keep\n"


@pytest.mark.parametrize("symlink_component", ["base", "session", "target"])
def test_remove_worktree_rejects_symlink_components(
    tmp_path: Path, symlink_component: str
) -> None:
    root = make_repo(tmp_path)
    managed = root / ".cmoc" / "local" / "worktree"
    external = tmp_path / "external"
    actual = external / "session" / "run"
    actual.parent.mkdir(parents=True)
    run_git(
        root,
        "worktree",
        "add",
        "-b",
        "cmoc/apply/session/run",
        str(actual),
        "HEAD",
    )

    if symlink_component == "base":
        managed.parent.mkdir(parents=True)
        managed.symlink_to(external, target_is_directory=True)
    else:
        managed.mkdir(parents=True)
        session = managed / "session"
        if symlink_component == "session":
            session.symlink_to(external / "session", target_is_directory=True)
        else:
            session.mkdir(parents=True)
            (session / "run").symlink_to(actual, target_is_directory=True)

    target = managed / "session" / "run"
    with pytest.raises(CmocError, match="cmoc 管理外の worktree"):
        remove_worktree(root, target)

    assert actual.exists()


def test_remove_worktree_rejects_unregistered_managed_path(
    tmp_path: Path,
) -> None:
    root = make_repo(tmp_path)
    target = root / ".cmoc" / "local" / "worktree" / "session" / "run"
    target.mkdir(parents=True)
    (target / "keep.txt").write_text("keep\n")

    with pytest.raises(CmocError, match="cmoc 管理外の worktree"):
        remove_worktree(root, target)

    assert (target / "keep.txt").read_text() == "keep\n"
