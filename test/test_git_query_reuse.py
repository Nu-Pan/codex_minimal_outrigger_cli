"""doctor と run 差分検査の Git path 再利用が状態変更を隠さないことを検証する。"""

from collections import Counter
from contextlib import nullcontext

import pytest
from _git_support import make_repo, run_git

import commons.runtime_git as git_module
from commons.runtime_errors import CmocError
from commons.runtime_paths import repo_root, work_root
from commons.runtime_run_lifecycle import (
    EditingRunContext,
    GitChange,
    unexpected_agent_paths,
    unexpected_run_paths,
)


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


def test_git_query_reuse_observes_ignore_content_and_index_changes(cli_repository):
    root = cli_repository
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
def test_git_query_reuse_expires_after_completion_or_failure(
    tmp_path, cli_repository, interrupt
):
    root = cli_repository
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


@pytest.mark.parametrize("inspection", ["agent", "run"])
def test_run_path_inspection_reuses_queries_and_refreshes_after_changes(
    cli_repository, monkeypatch, inspection
):
    """検査内の配置問い合わせを重複させず、次の検査で状態と失敗を再確認する。"""
    root = cli_repository
    paths = ["first.txt", "second.txt"]
    for path in paths:
        (root / path).write_text("content\n")
    context = EditingRunContext(
        repo=root,
        session_worktree=root,
        session_id="session",
        state_path=root / "state.json",
        session_branch="session",
        session_fork_commit="fork",
        kind="realization_apply",
        run_branch="run",
        run_fork_commit="fork",
        run_worktree=root,
    )

    def validate():
        if inspection == "agent":
            return unexpected_agent_paths(context, paths)
        return unexpected_run_paths(
            context, [GitChange("M", (path,)) for path in paths]
        )

    queries = Counter()
    original_run = git_module.subprocess.run

    def record_query(argv, *args, **kwargs):
        if argv[0] == "git" and argv[1] in {"rev-parse", "config"}:
            queries[tuple(argv)] += 1
        return original_run(argv, *args, **kwargs)

    with monkeypatch.context() as probe:
        probe.setattr(git_module.subprocess, "run", record_query)
        assert validate() == []
    assert max(queries.values(), default=0) <= 1

    # 判定結果や index は再利用せず、tracked な ignored file は許可範囲に残す。
    (root / ".gitignore").write_text("first.txt\n")
    assert validate() == ["first.txt"]
    run_git(root, "add", "-f", "first.txt")
    assert validate() == []

    # 設定と ignore source の検証は、成功・失敗いずれの検査後も取り直す。
    global_ignore = root / "global-ignore"
    global_ignore.write_text("second.txt\n")
    run_git(root, "config", "core.excludesFile", str(global_ignore))
    assert validate() == ["second.txt"]
    global_ignore.unlink()
    global_ignore.mkdir()
    with pytest.raises(CmocError, match="global excludes"):
        validate()
    run_git(root, "config", "core.excludesFile", "/dev/null")
    assert validate() == []
