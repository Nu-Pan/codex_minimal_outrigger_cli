"""Root/worktree と path model の runtime 契約を検証する。

根拠:
- {{work-root}}/oracle/src/oracle/other/path_model.py
- {{work-root}}/oracle/doc/branch_model.md
- {{work-root}}/oracle/doc/app_spec/run_isolation.md
"""

import threading
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import pytest
from _git_support import make_repo, run_git

from basic.path_model import (
    AgentCallPathContext,
    RootPathPlaceHolder,
    resolve_ph_path,
    resolve_real_path,
)
from cmoc_runtime import (
    CmocError,
    create_run_worktree,
    is_root_memo,
    pushd,
    remove_worktree,
    repo_root,
    work_root,
)
from commons.runtime_run import expected_run_worktree, worktree_for_branch_optional


def test_path_model_resolves_token_path_inside_repo() -> None:
    """root placeholder path が repo 内の実 path から復元できる。"""
    cmoc_root = resolve_real_path(RootPathPlaceHolder.CMOC)
    token_path = resolve_ph_path(cmoc_root / "src", RootPathPlaceHolder.CMOC)

    assert token_path == Path("{{cmoc-root}}") / "src"


def test_make_repo_ignores_global_git_config(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """test repository が global Git 設定に依存しないことを検証する。"""
    hooks = tmp_path / "hooks"
    hooks.mkdir()
    hook = hooks / "pre-commit"
    hook.write_text("#!/bin/sh\nexit 1\n")
    hook.chmod(0o755)
    template = tmp_path / "git-template"
    template.mkdir()
    (template / ".gitignore").write_text("README.md\noracle/spec.md\n")
    global_ignore = tmp_path / "gitignore"
    global_ignore.write_text("README.md\noracle/spec.md\n")
    global_config = tmp_path / "gitconfig"
    global_config.write_text(
        f"[commit]\n\tgpgsign = true\n[core]\n\thooksPath = {hooks}\n"
        f"\texcludesFile = {global_ignore}\n[init]\n\ttemplateDir = {template}\n"
    )
    monkeypatch.setenv("GIT_CONFIG_GLOBAL", str(global_config))

    root = make_repo(tmp_path)

    assert run_git(root, "config", "--local", "commit.gpgsign").stdout == "false\n"
    assert run_git(root, "config", "--local", "core.hooksPath").stdout == "/dev/null\n"
    assert (
        run_git(root, "config", "--local", "core.excludesFile").stdout == "/dev/null\n"
    )
    assert run_git(root, "rev-parse", "--verify", "HEAD").stdout.strip()


def test_runtime_distinguishes_repo_root_from_linked_worktree(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """linked worktree では repo root と run/work root を分けて扱う。"""
    root = make_repo(tmp_path)
    linked = root / ".cmoc" / "gu" / "worktree" / "linked"
    run_git(root, "worktree", "add", "-b", "linked-test", str(linked), "HEAD")

    monkeypatch.chdir(linked)
    assert repo_root(linked) == root.resolve()
    assert resolve_real_path(RootPathPlaceHolder.RUN) == linked.resolve()
    assert work_root(linked) == linked.resolve()


def test_agent_call_path_contexts_are_parallel_and_call_scoped(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """並列 call が process cwd を変えず、互いに異なる work root を保持する。"""
    root = make_repo(tmp_path)
    worktrees = [root / "first-worktree", root / "second-worktree"]
    for index, worktree in enumerate(worktrees):
        run_git(
            root,
            "worktree",
            "add",
            "-b",
            f"parallel-context-{index}",
            str(worktree),
            "HEAD",
        )
    monkeypatch.chdir(root)

    with ThreadPoolExecutor(max_workers=2) as executor:
        contexts = list(executor.map(AgentCallPathContext, worktrees))

    assert Path.cwd() == root
    for context, worktree in zip(contexts, worktrees, strict=True):
        assert context.agent_call_cwd == worktree.resolve()
        assert context.work_root == worktree.resolve()
        assert context.repo_root == root.resolve()
        assert context.root_placeholder_definitions() == {
            "repo-root": root.resolve(),
            "work-root": worktree.resolve(),
        }


def test_root_resolution_serializes_relative_cwd_and_accepts_missing_anchor(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """relativeな起点の解決をcwd切替と直列化し、未作成の祖先も受理する。"""
    (tmp_path / "first").mkdir()
    (tmp_path / "second").mkdir()
    first = make_repo(tmp_path / "first")
    second = make_repo(tmp_path / "second")
    original = first.resolve()
    monkeypatch.chdir(original)
    first_ready = threading.Event()
    release_first = threading.Event()
    worker_started = threading.Event()
    worker_finished = threading.Event()
    observed: list[Path] = []

    def hold_other_directory() -> None:
        """別threadのpushdがprocess-global cwdを保持する。"""
        with pushd(second):
            first_ready.set()
            release_first.wait(5)

    def resolve_relative_cwd() -> None:
        """相対cwdを解決し、呼び出し結果を記録する。"""
        first_ready.wait(5)
        worker_started.set()
        observed.append(repo_root(Path(".")))
        worker_finished.set()

    holder = threading.Thread(target=hold_other_directory)
    worker = threading.Thread(target=resolve_relative_cwd)
    holder.start()
    assert first_ready.wait(5)
    worker.start()
    try:
        assert worker_started.wait(5)
        assert not worker_finished.wait(0.1)
    finally:
        release_first.set()
        holder.join(5)
        worker.join(5)

    assert observed == [original]
    assert not holder.is_alive()
    assert not worker.is_alive()

    missing_anchor = original / "not-created" / "file.py"
    assert repo_root(missing_anchor) == original
    assert work_root(missing_anchor) == original


def test_root_memo_classification_uses_repository_path_for_symlinks(
    tmp_path: Path,
) -> None:
    """memo 判定は symlink の link 先ではなく repository path で行う。"""
    root = make_repo(tmp_path)
    memo = root / "memo"
    memo.mkdir()
    (memo / "target.md").write_text("memo\n")
    outside = tmp_path / "outside.md"
    outside.write_text("outside\n")
    memo_link = memo / "outside-link.md"
    memo_link.symlink_to(outside)
    outside_link = root / "outside-link.md"
    outside_link.symlink_to(memo / "target.md")

    assert is_root_memo(root, memo_link)
    assert not is_root_memo(root, outside_link)
    assert not is_root_memo(root, memo / ".." / outside_link.name)


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
        """最初のpushdを保持して次のthreadを待たせる。"""
        with pushd(first):
            first_ready.set()
            release_first.wait(5)

    def enter_second_directory() -> None:
        """二つ目のpushdへ入り、lock解放後に進めることを記録する。"""
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

    with pytest.raises(ValueError, match="`{{run-root}}` was not found"):
        resolve_real_path(RootPathPlaceHolder.RUN)


def test_create_run_worktree_rejects_path_outside_managed_worktrees(
    tmp_path: Path,
) -> None:
    """管理領域外のpathでrun worktreeを作成しないことを検証する。"""
    root = make_repo(tmp_path)
    target = tmp_path / "unrelated"
    target.mkdir()
    (target / "keep.txt").write_text("keep\n")

    with pytest.raises(CmocError, match="run worktree path"):
        create_run_worktree(root, "cmoc/run/session/run", target)

    assert (target / "keep.txt").read_text() == "keep\n"


def test_create_run_worktree_rejects_path_not_matching_branch(
    tmp_path: Path,
) -> None:
    """branchと一致しないmanaged pathをrun worktreeとして作成しないことを検証する。"""
    root = make_repo(tmp_path)
    target = root / ".cmoc" / "gu" / "worktree" / "session" / "other-run"
    target.mkdir(parents=True)
    (target / "keep.txt").write_text("keep\n")

    with pytest.raises(CmocError, match="run worktree path"):
        create_run_worktree(root, "cmoc/run/session/run", target)

    assert (target / "keep.txt").read_text() == "keep\n"


@pytest.mark.parametrize("branch", ["cmoc/run/../run", "cmoc/run/session/.."])
def test_run_worktree_rejects_dot_path_components(tmp_path: Path, branch: str) -> None:
    """run branch の dot component が managed path の外へ解決されないことを検証する。"""
    root = make_repo(tmp_path)

    with pytest.raises(CmocError, match="run worktree"):
        expected_run_worktree(root, branch)
    with pytest.raises(CmocError, match="run worktree"):
        create_run_worktree(
            root, branch, root / ".cmoc" / "gu" / "worktree" / "session" / "run"
        )


@pytest.mark.parametrize("symlink_component", ["base", "session", "target"])
def test_run_worktree_lookup_rejects_symlink_components(
    tmp_path: Path, symlink_component: str
) -> None:
    """登録後に symlink 化された run worktree を作業 root として扱わない。"""
    root = make_repo(tmp_path)
    managed = root / ".cmoc" / "gu" / "worktree"
    expected = managed / "session" / "run"
    run_git(
        root, "worktree", "add", "-b", "cmoc/run/session/run", str(expected), "HEAD"
    )

    external = tmp_path / "external"
    moved = external / "worktree"
    moved.parent.mkdir(parents=True)
    if symlink_component == "base":
        managed.rename(moved)
        managed.symlink_to(moved, target_is_directory=True)
    elif symlink_component == "session":
        moved = external / "session"
        (managed / "session").rename(moved)
        (managed / "session").symlink_to(moved, target_is_directory=True)
    else:
        moved = external / "run"
        expected.rename(moved)
        expected.symlink_to(moved, target_is_directory=True)

    assert worktree_for_branch_optional(root, "cmoc/run/session/run") is None


def test_run_worktree_lookup_rejects_replaced_registered_path(
    tmp_path: Path,
) -> None:
    """Git 登録が残っていても linked worktree でない置換先を扱わない。"""
    root = make_repo(tmp_path)
    target = root / ".cmoc" / "gu" / "worktree" / "session" / "run"
    run_git(
        root,
        "worktree",
        "add",
        "-b",
        "cmoc/run/session/run",
        str(target),
        "HEAD",
    )
    target.rename(tmp_path / "moved-worktree")
    assert worktree_for_branch_optional(root, "cmoc/run/session/run") is None
    target.mkdir(parents=True)

    assert worktree_for_branch_optional(root, "cmoc/run/session/run") is None


@pytest.mark.parametrize("symlink_component", ["base", "session", "target"])
def test_create_run_worktree_rejects_symlink_components(
    tmp_path: Path, symlink_component: str
) -> None:
    """symlink componentを経由したrun worktree作成を拒否することを検証する。"""
    root = make_repo(tmp_path)
    managed = root / ".cmoc" / "gu" / "worktree"
    external = tmp_path / "external"
    external.mkdir()

    if symlink_component == "base":
        managed.parent.mkdir(parents=True)
        managed.symlink_to(external, target_is_directory=True)
        symlink_path = managed
    else:
        managed.mkdir(parents=True)
        session = managed / "session"
        if symlink_component == "session":
            session.symlink_to(external / "session", target_is_directory=True)
            symlink_path = session
        else:
            session.mkdir()
            symlink_path = session / "run"
            symlink_path.symlink_to(
                external / "session" / "run", target_is_directory=True
            )

    target = managed / "session" / "run"
    with pytest.raises(CmocError, match="run worktree path"):
        create_run_worktree(root, "cmoc/run/session/run", target)

    assert symlink_path.is_symlink()
    assert not (external / "session" / "run").exists()


def test_create_run_worktree_rejects_unregistered_managed_path(
    tmp_path: Path,
) -> None:
    """Git未登録のmanaged pathをrun worktreeとして扱わないことを検証する。"""
    root = make_repo(tmp_path)
    target = root / ".cmoc" / "gu" / "worktree" / "session" / "run"
    target.mkdir(parents=True)
    (target / "keep.txt").write_text("keep\n")

    with pytest.raises(CmocError, match="run worktree path"):
        create_run_worktree(root, "cmoc/run/session/run", target)

    assert (target / "keep.txt").read_text() == "keep\n"


def test_remove_worktree_rejects_path_outside_managed_worktrees(
    tmp_path: Path,
) -> None:
    """管理領域外のpathをworktree削除対象にしないことを検証する。"""
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
    """symlink componentを経由したworktree削除を拒否することを検証する。"""
    root = make_repo(tmp_path)
    managed = root / ".cmoc" / "gu" / "worktree"
    external = tmp_path / "external"
    actual = external / "session" / "run"
    actual.parent.mkdir(parents=True)
    run_git(
        root,
        "worktree",
        "add",
        "-b",
        "cmoc/run/session/run",
        str(actual),
        "HEAD",
    )

    if symlink_component == "base":
        managed.parent.mkdir(parents=True)
        managed.symlink_to(external, target_is_directory=True)
        symlink_path = managed
    else:
        managed.mkdir(parents=True)
        session = managed / "session"
        if symlink_component == "session":
            session.symlink_to(external / "session", target_is_directory=True)
            symlink_path = session
        else:
            session.mkdir(parents=True)
            symlink_path = session / "run"
            symlink_path.symlink_to(actual, target_is_directory=True)

    target = managed / "session" / "run"
    with pytest.raises(CmocError, match="cmoc 管理外の worktree"):
        remove_worktree(root, target)

    assert symlink_path.is_symlink()
    assert actual.exists()


def test_remove_worktree_rejects_unregistered_managed_path(
    tmp_path: Path,
) -> None:
    """Git未登録のmanaged pathをworktree削除対象にしないことを検証する。"""
    root = make_repo(tmp_path)
    target = root / ".cmoc" / "gu" / "worktree" / "session" / "run"
    target.mkdir(parents=True)
    (target / "keep.txt").write_text("keep\n")

    with pytest.raises(CmocError, match="cmoc 管理外の worktree"):
        remove_worktree(root, target)

    assert (target / "keep.txt").read_text() == "keep\n"


def test_remove_worktree_rejects_non_run_branch_at_managed_path(
    tmp_path: Path,
) -> None:
    """管理領域内でもrun branchと対応しないworktreeを削除しない。"""
    root = make_repo(tmp_path)
    target = root / ".cmoc" / "gu" / "worktree" / "session" / "run"
    run_git(root, "worktree", "add", "-b", "ordinary", str(target), "HEAD")

    try:
        with pytest.raises(CmocError, match="cmoc 管理外の worktree"):
            remove_worktree(root, target)
        assert target.exists()
    finally:
        run_git(root, "worktree", "remove", "--force", str(target))


def test_remove_worktree_rejects_replaced_registered_path(
    tmp_path: Path,
) -> None:
    """staleなGit登録だけを根拠に通常directoryを削除しないことを検証する。"""
    root = make_repo(tmp_path)
    target = root / ".cmoc" / "gu" / "worktree" / "session" / "run"
    run_git(
        root,
        "worktree",
        "add",
        "-b",
        "cmoc/run/session/run",
        str(target),
        "HEAD",
    )
    moved = tmp_path / "moved-worktree"
    target.rename(moved)
    target.mkdir(parents=True)
    (target / "keep.txt").write_text("keep\n")

    with pytest.raises(CmocError, match="cmoc 管理外の worktree"):
        remove_worktree(root, target)

    assert (target / "keep.txt").read_text() == "keep\n"
