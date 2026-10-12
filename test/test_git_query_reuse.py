"""Git path の重複照会を避け、状態変更後の安全性検査を保つことを検証する。"""

import shutil
from collections import Counter
from contextlib import nullcontext

import pytest
from _git_support import RUN_BRANCH, RUN_ID, SESSION_ID, init_repo, run_git

import commons.runtime_git as git_module
from commons.prompt_editor_input import ensure_prompt_editor_roots_ignored
from commons.runtime_errors import CmocError
from commons.runtime_paths import repo_root, work_root
from commons.runtime_results import CommandResult
from commons.runtime_run_lifecycle import (
    EditingRunContext,
    GitChange,
    unexpected_agent_paths,
    unexpected_run_paths,
)


@pytest.mark.parametrize("anchor", ["main", "linked"])
def test_worktree_mutations_avoid_repeated_root_discovery(
    committed_repository, tmp_path, monkeypatch, anchor
):
    """作成・削除ごとの root 探索を一度に保ち、linked 起点でも同じ管理先を使う。"""
    root = committed_repository
    repository = root
    if anchor == "linked":
        repository = tmp_path / "linked"
        run_git(root, "worktree", "add", "-b", "linked-query", str(repository), "HEAD")
    target = root / ".cmoc/gu/worktree" / SESSION_ID / RUN_ID
    root_queries = 0
    prune_calls = 0
    original_run = git_module.subprocess.run

    def record_query(argv, *args, **kwargs):
        nonlocal root_queries, prune_calls
        if argv[0] == "git" and "--show-toplevel" in argv:
            root_queries += 1
        if argv[:3] == ["git", "worktree", "prune"]:
            prune_calls += 1
        return original_run(argv, *args, **kwargs)

    monkeypatch.setattr(git_module.subprocess, "run", record_query)
    assert git_module.create_run_worktree(repository, RUN_BRANCH, target) == target
    assert root_queries <= 1
    assert target.is_dir()
    assert run_git(target, "branch", "--show-current").stdout.strip() == RUN_BRANCH

    root_queries = 0
    assert git_module.remove_worktree(repository, target).returncode == 0
    assert root_queries <= 1
    assert prune_calls == 0
    assert not target.exists()
    assert str(target) not in run_git(root, "worktree", "list", "--porcelain").stdout


@pytest.mark.parametrize("state_after_failure", ["registered", "missing", "detached"])
def test_remove_worktree_preserves_fallback_cleanup_and_rechecks_registration(
    committed_repository, monkeypatch, state_after_failure
):
    """削除失敗時は残存登録を回収し、branch の登録が変わった実体は保護する。"""
    root = committed_repository
    target = root / ".cmoc/gu/worktree" / SESSION_ID / RUN_ID
    git_module.create_run_worktree(root, RUN_BRANCH, target)
    (target / "keep.txt").write_text("keep\n")
    original_run = git_module.run_git
    prune_calls = 0

    def fail_removal(args, git_cwd, check=True):
        nonlocal prune_calls
        if args[:2] == ["worktree", "remove"]:
            if state_after_failure == "detached":
                run_git(target, "switch", "--detach")
            elif state_after_failure == "missing":
                shutil.rmtree(target)
            return CommandResult(1, "", "simulated removal failure")
        if args[:2] == ["worktree", "prune"]:
            prune_calls += 1
        return original_run(args, git_cwd, check=check)

    monkeypatch.setattr(git_module, "run_git", fail_removal)
    if state_after_failure == "detached":
        with pytest.raises(CmocError, match="cmoc 管理外の worktree"):
            git_module.remove_worktree(root, target)
        assert prune_calls == 0
        assert (target / "keep.txt").read_text() == "keep\n"
        assert (target / ".git").is_file()
    else:
        result = git_module.remove_worktree(root, target)
        assert result.returncode == 1
        assert result.stderr == "simulated removal failure"
        assert prune_calls == 1
        assert not target.exists()
        assert (
            str(target) not in run_git(root, "worktree", "list", "--porcelain").stdout
        )


def test_git_query_reuse_keeps_worktrees_and_environment_separate(
    committed_repository, tmp_path, monkeypatch
):
    """両 root の導出を共有し、異なる起点・環境では取り直す。"""
    # linked worktree に必要な HEAD だけを用意し、追跡 file と staging を準備しない。
    root = committed_repository
    linked = tmp_path / "linked"
    run_git(root, "worktree", "add", "-b", "linked-query", str(linked), "HEAD")
    index_query = ["rev-parse", "--git-path", "index"]
    git_calls = 0
    original_run = git_module.subprocess.run

    def record_query(argv, *args, **kwargs):
        nonlocal git_calls
        if argv[0] == "git":
            git_calls += 1
        return original_run(argv, *args, **kwargs)

    monkeypatch.setattr(git_module.subprocess, "run", record_query)

    with git_module.reuse_git_path_queries():
        for anchor in (root, linked, root, linked):
            monkeypatch.chdir(anchor)
            assert repo_root() == root
            calls_after_repo_root = git_calls
            assert work_root() == anchor
            assert repo_root() == root
            assert git_calls == calls_after_repo_root
            assert git_module.git_common_dir(anchor) == root / ".git"
        assert git_module.run_git(index_query, root).stdout.strip() == ".git/index"
        assert git_module.run_git(index_query, linked).stdout.strip() != ".git/index"
        with monkeypatch.context() as environment:
            alternate_index = tmp_path / "alternate-index"
            environment.setenv("GIT_INDEX_FILE", str(alternate_index))
            assert git_module.run_git(index_query, root).stdout.strip() == str(
                alternate_index
            )
            calls_before_root = git_calls
            assert repo_root(root) == root
            assert git_calls > calls_before_root
            calls_after_repo_root = git_calls
            assert work_root(root) == root
            assert git_calls == calls_after_repo_root
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


def test_prompt_editor_ignore_reuses_queries_and_refreshes_after_repair(
    cli_repository, monkeypatch
):
    """入力前処理は配置を再利用し、修復した index と次回の設定変更を検査する。"""
    root = cli_repository
    monkeypatch.chdir(root)
    tracked = root / ".cmoc/gu/input.txt"
    tracked.parent.mkdir(parents=True)
    tracked.write_text("preserve input\n")
    run_git(root, "add", "-f", str(tracked.relative_to(root)))
    queries = Counter()
    original_run = git_module.subprocess.run

    def record_query(argv, *args, **kwargs):
        if argv[0] == "git":
            queries[tuple(argv[1:])] += 1
        return original_run(argv, *args, **kwargs)

    monkeypatch.setattr(git_module.subprocess, "run", record_query)

    ensure_prompt_editor_roots_ignored(root)

    assert queries[("rev-parse", "--git-path", "info/exclude")] == 1
    assert queries[("config", "--path", "--get-all", "core.excludesFile")] == 1
    assert queries[("ls-files", "--", ".cmoc/gu")] == 2
    assert queries[("check-ignore", "-q", git_module.CMOC_IGNORE_PROBE)] == 2
    assert tracked.read_text() == "preserve input\n"
    assert run_git(root, "ls-files", "--", ".cmoc/gu").stdout == ""
    assert "/.cmoc/gu/" in (root / ".gitignore").read_text()

    # 起動間や失敗後へ配置・安全性の判定を持ち越さない。
    global_ignore = root / "new-ignore"
    global_ignore.mkdir()
    run_git(root, "config", "core.excludesFile", str(global_ignore))
    with pytest.raises(CmocError, match="global excludes"):
        ensure_prompt_editor_roots_ignored(root)
    global_ignore.rmdir()
    global_ignore.write_text("*.unused\n")
    ensure_prompt_editor_roots_ignored(root)


def test_exclude_initialization_reuses_path_and_rechecks_state(
    cli_repository, monkeypatch
):
    """exclude の保存先だけを再利用し、次回の内容変更と index 変更を検査する。"""
    root = cli_repository
    queries = Counter()
    original_run = git_module.subprocess.run

    def record_query(argv, *args, **kwargs):
        if argv[0] == "git":
            queries[tuple(argv[1:])] += 1
        return original_run(argv, *args, **kwargs)

    monkeypatch.setattr(git_module.subprocess, "run", record_query)
    exclude = root / ".git/info/exclude"
    for content in (None, "existing.txt\n"):
        if content is not None:
            exclude.write_text(content)
        queries.clear()

        git_module.ensure_cmoc_ignored_in_exclude(root)

        assert queries[("rev-parse", "--git-path", "info/exclude")] == 1
        assert queries[("ls-files", "--", ".cmoc/gu")] == 1
        assert queries[("check-ignore", "-q", git_module.CMOC_IGNORE_PROBE)] == 1
        assert "/.cmoc/gu/" in exclude.read_text()
        if content is not None:
            assert exclude.read_text().startswith(content)
        assert not (root / ".gitignore").exists()

    # 同じ保存先でも、前回の非追跡判定は使い回さない。
    tracked = root / ".cmoc/gu/input.txt"
    tracked.parent.mkdir(parents=True)
    tracked.write_text("preserve input\n")
    run_git(root, "add", "-f", str(tracked.relative_to(root)))
    with pytest.raises(CmocError, match="追跡対象外"):
        git_module.ensure_cmoc_ignored_in_exclude(root)
    assert tracked.read_text() == "preserve input\n"


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
            assert work_root(nested) == root
            if interrupt:
                raise RuntimeError("interrupted")

    ignore_path = tmp_path / "new-ignore"
    ignore_path.write_text("candidate.txt\n")
    run_git(root, "config", "core.excludesFile", str(ignore_path))
    run_git(nested, "init", "--template=/dev/null")
    assert git_module.run_git(query, root).stdout.strip() == str(ignore_path)
    assert repo_root(nested) == nested
    assert work_root(nested) == nested
    with git_module.reuse_git_path_queries():
        assert git_module.run_git(query, root).stdout.strip() == str(ignore_path)
        assert repo_root(nested) == nested
        assert work_root(nested) == nested


def test_root_query_reuse_retries_failed_discovery(tmp_path):
    """root を発見できない失敗を保存せず、同じ区間でも再試行する。"""
    root = tmp_path / "not-yet-a-repository"
    root.mkdir()

    with git_module.reuse_git_path_queries():
        # 両 resolver の失敗を確かめ、共有する root 探索の再試行は一度だけ準備する。
        for resolver, placeholder in (
            (repo_root, "repo-root"),
            (work_root, "work-root"),
        ):
            with pytest.raises(CmocError, match=placeholder):
                resolver(root)
        init_repo(root)
        assert repo_root(root) == root
        assert work_root(root) == root


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

    queries = Counter()
    original_run = git_module.subprocess.run

    def record_query(argv, *args, **kwargs):
        if argv[0] == "git":
            queries[tuple(argv)] += 1
        return original_run(argv, *args, **kwargs)

    monkeypatch.setattr(git_module.subprocess, "run", record_query)

    def validate():
        queries.clear()
        if inspection == "agent":
            unexpected = unexpected_agent_paths(context, paths)
        else:
            unexpected = unexpected_run_paths(
                context, [GitChange("M", (path,)) for path in paths]
            )
        placement_queries = [
            count
            for argv, count in queries.items()
            if argv[1] in {"rev-parse", "config"}
        ]
        assert max(placement_queries, default=0) <= 1
        # 存在する ignored file も、branch/fork ごとに同じ判定を繰り返さない。
        assert sum(
            count for argv, count in queries.items() if argv[1] == "check-ignore"
        ) <= len(paths)
        return unexpected

    assert validate() == []

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
