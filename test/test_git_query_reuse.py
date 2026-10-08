"""doctor 内の Git path 再利用が変更可能な状態や次の呼び出しを隠さないことを検証する。"""

from contextlib import nullcontext

import pytest
from _git_support import make_repo, run_git

import commons.runtime_git as git_module
from commons.runtime_paths import repo_root, work_root


def test_git_query_reuse_keeps_worktrees_and_environment_separate(
    tmp_path, monkeypatch
):
    root = make_repo(tmp_path)
    linked = tmp_path / "linked"
    run_git(root, "worktree", "add", "-b", "linked-query", str(linked), "HEAD")
    index_query = ["rev-parse", "--git-path", "index"]

    with git_module.reuse_git_path_queries():
        for anchor in (root, linked, root, linked):
            monkeypatch.chdir(anchor)
            assert repo_root() == root
            assert work_root() == anchor
            assert git_module.git_common_dir(anchor) == root / ".git"
        assert git_module.run_git(index_query, root).stdout.strip() == ".git/index"
        assert git_module.run_git(index_query, linked).stdout.strip() != ".git/index"
        with monkeypatch.context() as environment:
            alternate_index = tmp_path / "alternate-index"
            environment.setenv("GIT_INDEX_FILE", str(alternate_index))
            assert git_module.run_git(index_query, root).stdout.strip() == str(
                alternate_index
            )
        assert git_module.run_git(index_query, root).stdout.strip() == ".git/index"


def test_git_query_reuse_observes_ignore_content_and_index_changes(tmp_path):
    root = make_repo(tmp_path)
    candidate = root / "candidate.txt"
    candidate.write_text("content\n")
    gitignore = root / ".gitignore"
    gitignore.write_text("")

    with git_module.reuse_git_path_queries():
        assert not git_module.is_git_ignored(root, candidate)
        gitignore.write_text("candidate.txt\n")
        assert git_module.is_git_ignored(root, candidate)
        assert git_module.is_untracked_git_ignored(root, candidate)
        run_git(root, "add", "-f", candidate.name)
        assert git_module.is_git_ignored(root, candidate)
        assert not git_module.is_untracked_git_ignored(root, candidate)


@pytest.mark.parametrize("interrupt", [False, True])
def test_git_query_reuse_expires_after_completion_or_failure(tmp_path, interrupt):
    root = make_repo(tmp_path)
    nested = root / "nested"
    nested.mkdir()
    query = ["config", "--path", "--get-all", "core.excludesFile"]
    expected_error = (
        pytest.raises(RuntimeError, match="interrupted") if interrupt else nullcontext()
    )

    with expected_error:
        with git_module.reuse_git_path_queries():
            assert git_module.run_git(query, root).stdout.strip() == "/dev/null"
            assert repo_root(nested) == root
            if interrupt:
                raise RuntimeError("interrupted")

    ignore_path = tmp_path / "new-ignore"
    ignore_path.write_text("candidate.txt\n")
    run_git(root, "config", "core.excludesFile", str(ignore_path))
    run_git(nested, "init", "--template=/dev/null")
    assert git_module.run_git(query, root).stdout.strip() == str(ignore_path)
    assert repo_root(nested) == nested
    with git_module.reuse_git_path_queries():
        assert git_module.run_git(query, root).stdout.strip() == str(ignore_path)
        assert repo_root(nested) == nested
