"""Git path の重複照会を避け、状態変更後の安全性検査を保つことを検証する。"""

import shutil
from collections import Counter
from contextlib import nullcontext

import pytest
from _git_support import RUN_BRANCH, RUN_ID, SESSION_ID, init_repo, run_git

import commons.runtime_git as git_module
import commons.runtime_run_join as run_join_module
from commons.prompt_editor_input import ensure_prompt_editor_roots_ignored
from commons.runtime_errors import CmocError
from commons.runtime_paths import repo_root, reuse_root_queries, work_root
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
            calls_before_nested = git_calls
            with reuse_root_queries(), git_module.reuse_git_path_queries():
                assert repo_root() == root
                assert work_root() == anchor
                assert git_module.git_common_dir(anchor) == root / ".git"
            assert git_calls == calls_before_nested
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


def test_join_doctor_reuses_roots_only_before_preprocessing(
    committed_repository, tmp_path, monkeypatch
):
    """join 前の両 root は探索を共有し、doctor と次回呼び出しは取り直す。"""
    root = committed_repository
    linked = tmp_path / "linked"
    run_git(root, "worktree", "add", "-b", "join-doctor-query", str(linked), "HEAD")
    root_queries = 0
    original_run = git_module.subprocess.run

    def record_query(argv, *args, **kwargs):
        nonlocal root_queries
        if argv[0] == "git" and "--show-toplevel" in argv:
            root_queries += 1
        return original_run(argv, *args, **kwargs)

    monkeypatch.setattr(git_module.subprocess, "run", record_query)

    # 修復・復旧・同期の判断は test_editing_run_cli.py に残し、探索の境界だけを検査する。
    def preprocess(work, main, *, rollback_on_interruption):
        assert work == anchor
        assert main == root
        assert rollback_on_interruption is (anchor == linked)
        assert root_queries == 1
        # doctor が行う検証へ成功結果を持ち越さない。
        assert work_root(work) == work
        assert root_queries == 2

    monkeypatch.setattr(run_join_module, "_run_join_doctor", preprocess)
    for anchor in (linked, root, linked):
        monkeypatch.chdir(anchor)
        root_queries = 0
        run_join_module.doctor_preprocess_for_join(
            rollback_on_interruption=anchor == linked
        )
        assert root_queries == 2


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
    assert queries[("check-ignore", "-q", git_module.CMOC_IGNORE_PROBE)] == 1
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


def test_run_path_inspection_reuses_queries_and_refreshes_after_changes(
    cli_repository, monkeypatch
):
    """検査内の配置問い合わせを重複させず、次の検査で状態と失敗を再確認する。"""
    root = cli_repository
    paths = ["first.txt", "second.txt", "space tab\tline\n.txt", ":(literal)file.txt"]
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
    # 読み取り専用の両入口へ同じ状態を渡し、Git の準備と状態変更だけを共有する。
    inspections = (
        (unexpected_agent_paths, paths),
        (unexpected_run_paths, [GitChange("M", (path,)) for path in paths]),
    )

    queries = Counter()
    original_run = git_module.subprocess.run

    def record_query(argv, *args, **kwargs):
        if argv[0] == "git":
            queries[tuple(argv)] += 1
        return original_run(argv, *args, **kwargs)

    monkeypatch.setattr(git_module.subprocess, "run", record_query)

    def validate(expected):
        for inspect, changes in inspections:
            queries.clear()
            assert inspect(context, changes) == expected, inspect.__name__
            placement_queries = [
                count
                for argv, count in queries.items()
                if argv[1] in {"rev-parse", "config"}
            ]
            assert max(placement_queries, default=0) <= 1, inspect.__name__
            # file 数と特殊文字にかかわらず、同じ repository の判定を一括で行う。
            ignore_queries = sum(
                count for argv, count in queries.items() if argv[1] == "check-ignore"
            )
            assert ignore_queries == 1, inspect.__name__

    validate([])

    # ignored な特殊名も、空白・改行・pathspec magic を区切りや構文として解釈しない。
    (root / ".gitignore").write_text("*.txt\n")
    validate(sorted(paths))

    # 判定結果や index は再利用せず、tracked な ignored file は許可範囲に残す。
    (root / ".gitignore").write_text("first.txt\n")
    validate(["first.txt"])
    run_git(root, "add", "-f", "first.txt")
    validate([])

    # 設定と ignore source の検証は、成功・失敗いずれの検査後も取り直す。
    global_ignore = root / "global-ignore"
    global_ignore.write_text("second.txt\n")
    run_git(root, "config", "core.excludesFile", str(global_ignore))
    validate(["second.txt"])
    global_ignore.unlink()
    global_ignore.mkdir()
    for inspect, changes in inspections:
        with pytest.raises(CmocError, match="global excludes"):
            inspect(context, changes)
    run_git(root, "config", "core.excludesFile", "/dev/null")
    validate([])


def test_run_path_inspection_batches_each_owning_repository(
    cli_repository, monkeypatch
):
    """一括化しても nested の index・ignore と agent/run の許可範囲を区別する。"""
    root = cli_repository
    (root / ".gitignore").write_text("*.outer\n")
    (root / "dropped.outer").write_text("outer ignored\n")
    (root / "visible.txt").write_text("visible\n")
    nested = root / "nested"
    nested.mkdir()
    init_repo(nested)
    (nested / ".gitignore").write_text("*.nested\n")
    for name in ("kept.outer", "dropped.nested", "tracked.nested"):
        (nested / name).write_text("nested content\n")
    run_git(nested, "add", "-f", "tracked.nested")
    (nested / "alias").symlink_to(nested / "kept.outer")
    (root / "oracle").mkdir()
    (root / "oracle/spec.md").write_text("oracle\n")
    managed_state = ".cmoc/gt/realization/refactor/state.json"
    context = EditingRunContext(
        repo=root,
        session_worktree=root,
        session_id="session",
        state_path=root / "state.json",
        session_branch="session",
        session_fork_commit="fork",
        kind="realization_refactor",
        run_branch="run",
        run_fork_commit="fork",
        run_worktree=root,
    )
    rejected = [
        "dropped.outer",
        "nested/.git/config",
        "nested/alias",
        "nested/dropped.nested",
        "oracle/spec.md",
    ]
    paths = [*rejected, "visible.txt", "nested/kept.outer", "nested/tracked.nested"]
    # 重複と rename の両端も渡し、return 値と実 Git の問い合わせ数を検査する。
    paths += ["visible.txt", managed_state]
    changes = [GitChange("M", (path,)) for path in paths]
    changes.append(GitChange("R100", ("dropped.outer", "nested/kept.outer")))
    queries = Counter()
    original_run = git_module.subprocess.run

    def record_query(argv, *args, **kwargs):
        if argv[:2] == ["git", "check-ignore"]:
            queries[kwargs["cwd"]] += 1
        return original_run(argv, *args, **kwargs)

    monkeypatch.setattr(git_module.subprocess, "run", record_query)
    for inspect, inputs, expected in (
        (unexpected_agent_paths, paths, sorted([*rejected, managed_state])),
        (unexpected_run_paths, changes, rejected),
    ):
        queries.clear()
        assert inspect(context, inputs) == expected
        assert queries == {root: 1, nested: 1}

    # 明示対象外は run 検査だけに適用し、他の想定外 path は維持する。
    assert (
        unexpected_run_paths(context, changes, ignored_paths=["oracle/spec.md"])
        == (rejected[:-1])
    )

    # 一括判定の前にも nested の ignore source を検証し、特殊 file を読み込まない。
    (nested / ".gitignore").unlink()
    (nested / ".gitignore").mkdir()
    for inspect, inputs in (
        (unexpected_agent_paths, paths),
        (unexpected_run_paths, changes),
    ):
        with pytest.raises(CmocError, match=".gitignore"):
            inspect(context, inputs)
