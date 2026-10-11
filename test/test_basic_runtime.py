"""Root/worktree と path model の runtime 契約を検証する。

この file は 16,000 文字を超えるが、root placeholder の解決と managed worktree の
操作は同じ Git repository／worktree 境界を共有する。分割すると、Git fixture と
root 不変条件の検証文脈が複数 file に分散するため、一つの runtime 回帰として保つ。

根拠:
- {{work-root}}/oracle/src/oracle/other/path_model.py
- {{work-root}}/oracle/doc/branch_model.md
- {{work-root}}/oracle/doc/app_spec/run_isolation.md
"""

import threading
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import pytest
from _git_support import (
    RUN_BRANCH,
    RUN_ID,
    SESSION_BRANCH,
    SESSION_ID,
    init_repo,
    make_repo,
    run_git,
)

import commons.runtime_paths as runtime_paths
from basic.path_model import (
    AgentCallPathContext,
    RootPathPlaceHolder,
    resolve_ph_path,
    resolve_real_path,
)
from cmoc_runtime import (
    CmocError,
    create_run_worktree,
    pushd,
    remove_worktree,
    repo_root,
    work_root,
)
from commons.runtime_run import expected_run_worktree, worktree_for_branch_optional


@pytest.fixture
def _cwd_lock_contention(monkeypatch: pytest.MonkeyPatch) -> threading.Event:
    """実 RLock の競合を通知し、固定時間の待機なしで排他を検証する。"""
    # 既存の lock をそのまま使い、待つ理由だけを観測する。
    lock = runtime_paths._CMOC_PROCESS_CWD_LOCK
    contended = threading.Event()

    class _ObservedLock:
        def __enter__(self) -> None:
            # 再入は許し、別 thread との競合だけを通知する。
            if not lock.acquire(blocking=False):
                contended.set()
                lock.acquire()

        def __exit__(self, *_args: object) -> None:
            # 次の呼び出しも同じ実 lock を使えるよう、取得と解放を対応させる。
            lock.release()

    monkeypatch.setattr(runtime_paths, "_CMOC_PROCESS_CWD_LOCK", _ObservedLock())
    return contended


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

    # commit 成功で署名・失敗する hook の隔離を、tree で global ignore の隔離を確認する。
    assert run_git(
        root, "ls-tree", "-r", "--name-only", "HEAD"
    ).stdout.splitlines() == [
        "README.md",
        "oracle/spec.md",
    ]


def test_runtime_roots_distinguish_linked_worktree_from_nested_main(
    committed_repository: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """linked worktree の両 root を区別し、nested main は run root から除く。"""
    # 成功と拒否に同じ linked metadata を使い、外側の履歴・worktree 準備を共用する。
    root = committed_repository
    linked = tmp_path / "linked"
    run_git(root, "worktree", "add", "-b", "linked-test", str(linked), "HEAD")

    monkeypatch.chdir(linked)
    assert repo_root(linked) == root.resolve()
    assert resolve_real_path(RootPathPlaceHolder.RUN) == linked.resolve()
    assert work_root(linked) == linked.resolve()

    # 内側の main repository に履歴は不要。外側の linked root を誤採用しない。
    nested_main = linked / "repo"
    nested_main.mkdir()
    init_repo(nested_main)
    monkeypatch.chdir(nested_main)

    with pytest.raises(ValueError, match="`{{run-root}}` was not found"):
        resolve_real_path(RootPathPlaceHolder.RUN)


@pytest.mark.parametrize("marker_kind", ["file", "directory"])
def test_root_resolution_ignores_dot_git_names_without_repository_metadata(
    cli_repository: Path,
    marker_kind: str,
) -> None:
    """通常の `.git` 名を内側の worktree metadata として扱わない。"""
    # root の導出に履歴は不要だが、偽 marker の外側には実 Git metadata を残す。
    root = cli_repository
    nested = root / "nested"
    nested.mkdir()
    marker = nested / ".git"
    if marker_kind == "file":
        marker.write_text("not git metadata\n")
    else:
        marker.mkdir()

    context = AgentCallPathContext(nested)

    assert context.work_root == root.resolve()
    assert context.repo_root == root.resolve()


def test_agent_call_path_context_resolves_submodule_repository(
    committed_repository: Path,
    tmp_path: Path,
) -> None:
    """submodule の Git metadata から submodule 自身の両 root を解決する。"""
    # clone 元は空 commit の HEAD だけを使い、追跡 file は準備しない。
    source = committed_repository
    # submodule を登録する親には履歴・追跡 file が不要。
    parent = tmp_path / "parent"
    parent.mkdir()
    init_repo(parent)
    submodule = parent / "nested"
    run_git(
        parent,
        "-c",
        "protocol.file.allow=always",
        "submodule",
        "add",
        str(source),
        submodule.name,
    )

    context = AgentCallPathContext(submodule)

    assert context.work_root == submodule.resolve()
    assert context.repo_root == submodule.resolve()


def test_agent_call_path_context_resolves_separate_git_directory(
    tmp_path: Path,
) -> None:
    """separate git directory でも worktree path を両 root として解決する。"""
    worktree = tmp_path / "separate-worktree"
    git_directory = tmp_path / "separate-metadata"
    worktree.mkdir()
    run_git(
        worktree,
        "init",
        "--template=/dev/null",
        f"--separate-git-dir={git_directory}",
    )

    context = AgentCallPathContext(worktree)

    assert context.work_root == worktree.resolve()
    assert context.repo_root == worktree.resolve()
    assert expected_run_worktree(worktree, RUN_BRANCH) == (
        worktree / ".cmoc" / "gu" / "worktree" / SESSION_ID / RUN_ID
    )


def test_agent_call_path_context_ignores_repository_selection_environment(
    cli_repository: Path,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Git の repository 選択環境変数で agent call の cwd 起点を上書きしない。"""
    # 両方を実 repository にする。環境変数による誤選択の検出に履歴は不要。
    target = cli_repository
    override = tmp_path / "override"
    override.mkdir()
    init_repo(override)
    monkeypatch.setenv("GIT_DIR", str(override / ".git"))
    monkeypatch.setenv("GIT_WORK_TREE", str(override))
    monkeypatch.setenv("GIT_COMMON_DIR", str(override / ".git"))

    context = AgentCallPathContext(target)

    assert context.work_root == target.resolve()
    assert context.repo_root == target.resolve()


def test_agent_call_path_contexts_are_parallel_and_call_scoped(
    committed_repository: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """並列 call が process cwd を変えず、互いに異なる work root を保持する。"""
    root = committed_repository
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
    cli_repository: Path,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    _cwd_lock_contention: threading.Event,
) -> None:
    """relativeな起点の解決をcwd切替と直列化し、未作成の祖先も受理する。"""
    # cwd の混線を検出するための二つの Git root だけを準備する。
    first = cli_repository
    second = tmp_path / "second"
    second.mkdir()
    init_repo(second)
    original = first.resolve()
    monkeypatch.chdir(original)
    first_ready = threading.Event()
    release_first = threading.Event()
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
        observed.append(repo_root(Path(".")))
        worker_finished.set()

    holder = threading.Thread(target=hold_other_directory)
    worker = threading.Thread(target=resolve_relative_cwd)
    holder.start()
    assert first_ready.wait(5)
    worker.start()
    try:
        assert _cwd_lock_contention.wait(5)
        assert not worker_finished.is_set()
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


def test_pushd_serializes_process_global_cwd_changes(
    tmp_path: Path, _cwd_lock_contention: threading.Event
) -> None:
    """並列する pushd が process-global な cwd を混線させない。"""
    first = tmp_path / "first"
    second = tmp_path / "second"
    first.mkdir()
    second.mkdir()
    original = Path.cwd()
    first_ready = threading.Event()
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
        with pushd(second):
            assert Path.cwd() == second
            second_entered.set()

    first_thread = threading.Thread(target=hold_first_directory)
    second_thread = threading.Thread(target=enter_second_directory)
    first_thread.start()
    second_thread.start()
    try:
        assert first_ready.wait(5)
        assert _cwd_lock_contention.wait(5)
        assert not second_entered.is_set()
        assert Path.cwd() == first
    finally:
        release_first.set()
        first_thread.join(5)
        second_thread.join(5)

    assert second_entered.is_set()
    assert not first_thread.is_alive()
    assert not second_thread.is_alive()
    assert Path.cwd() == original


def test_run_worktree_operations_reject_path_outside_managed_worktrees(
    cli_repository: Path,
    tmp_path: Path,
) -> None:
    """管理領域外の同じ path を、作成でも削除でも保護する。"""
    # path の拒否に履歴は不要だが、root 解決には実 Git repository を使う。
    root = cli_repository
    target = tmp_path / "unrelated"
    target.mkdir()
    (target / "keep.txt").write_text("keep\n")

    with pytest.raises(CmocError, match="run worktree path"):
        create_run_worktree(root, RUN_BRANCH, target)

    assert (target / "keep.txt").read_text() == "keep\n"

    with pytest.raises(CmocError, match="cmoc 管理外の worktree"):
        remove_worktree(root, target)

    assert (target / "keep.txt").read_text() == "keep\n"


def test_create_run_worktree_rejects_path_not_matching_branch(
    cli_repository: Path,
) -> None:
    """branchと一致しないmanaged pathをrun worktreeとして作成しないことを検証する。"""
    root = cli_repository
    target = root / ".cmoc" / "gu" / "worktree" / SESSION_ID / "other-run"
    target.mkdir(parents=True)
    (target / "keep.txt").write_text("keep\n")

    with pytest.raises(CmocError, match="run worktree path"):
        create_run_worktree(root, RUN_BRANCH, target)

    assert (target / "keep.txt").read_text() == "keep\n"


def test_run_worktree_rejects_noncanonical_branch(
    cli_repository: Path,
) -> None:
    """現行 ID を持たない branch を worktree の保存先へ解決しない。"""
    root = cli_repository

    # 拒否で repository は変わらないため、全 branch 境界に同じ実 Git root を使う。
    for branch in (
        f"cmoc/run/../{RUN_ID}",
        f"cmoc/run/{SESSION_ID}/..",
        f"cmoc/run/2026-09-29_15-04_07_123456789/{RUN_ID}",
        f"cmoc/run/{SESSION_ID}/2026-09-29_15-04_07_123456789",
    ):
        with pytest.raises(CmocError, match="run worktree"):
            expected_run_worktree(root, branch)
        with pytest.raises(CmocError, match="run worktree"):
            create_run_worktree(
                root, branch, root / ".cmoc" / "gu" / "worktree" / SESSION_ID / RUN_ID
            )


@pytest.mark.parametrize("symlink_component", ["base", "session", "target"])
def test_run_worktree_lookup_rejects_symlink_components(
    committed_repository: Path, tmp_path: Path, symlink_component: str
) -> None:
    """登録後に symlink 化された run worktree を作業 root として扱わない。"""
    root = committed_repository
    managed = root / ".cmoc" / "gu" / "worktree"
    expected = managed / SESSION_ID / RUN_ID
    run_git(root, "worktree", "add", "-b", RUN_BRANCH, str(expected), "HEAD")

    external = tmp_path / "external"
    moved = external / "worktree"
    moved.parent.mkdir(parents=True)
    if symlink_component == "base":
        managed.rename(moved)
        managed.symlink_to(moved, target_is_directory=True)
    elif symlink_component == "session":
        moved = external / SESSION_ID
        (managed / SESSION_ID).rename(moved)
        (managed / SESSION_ID).symlink_to(moved, target_is_directory=True)
    else:
        moved = external / RUN_ID
        expected.rename(moved)
        expected.symlink_to(moved, target_is_directory=True)

    assert worktree_for_branch_optional(root, RUN_BRANCH) is None


def test_run_worktree_lookup_and_removal_reject_replaced_registered_path(
    committed_repository: Path, tmp_path: Path
) -> None:
    """stale な Git 登録先を作業 root として使わず、置換した内容も削除しない。"""
    root = committed_repository
    target = root / ".cmoc" / "gu" / "worktree" / SESSION_ID / RUN_ID
    run_git(
        root,
        "worktree",
        "add",
        "-b",
        RUN_BRANCH,
        str(target),
        "HEAD",
    )
    target.rename(tmp_path / "moved-worktree")
    assert worktree_for_branch_optional(root, RUN_BRANCH) is None
    target.mkdir(parents=True)

    assert worktree_for_branch_optional(root, RUN_BRANCH) is None

    (target / "keep.txt").write_text("keep\n")
    with pytest.raises(CmocError, match="cmoc 管理外の worktree"):
        remove_worktree(root, target)

    assert (target / "keep.txt").read_text() == "keep\n"


def test_session_worktree_lookup_rejects_invalid_registered_path(
    committed_repository: Path, tmp_path: Path
) -> None:
    """session branch も stale な Git 登録先を worktree として扱わない。"""
    root = committed_repository
    target = tmp_path / "session-worktree"
    run_git(
        root,
        "worktree",
        "add",
        "-b",
        SESSION_BRANCH,
        str(target),
        "HEAD",
    )
    target.rename(tmp_path / "moved-session-worktree")

    # Git 登録は不変なので、欠損・file・directory 置換に同じ準備を使う。
    assert worktree_for_branch_optional(root, SESSION_BRANCH) is None

    target.write_text("not a worktree\n")
    assert worktree_for_branch_optional(root, SESSION_BRANCH) is None

    target.unlink()
    target.mkdir()

    assert worktree_for_branch_optional(root, SESSION_BRANCH) is None


@pytest.mark.parametrize("symlink_component", ["base", "session", "target"])
def test_create_run_worktree_rejects_symlink_components(
    cli_repository: Path, tmp_path: Path, symlink_component: str
) -> None:
    """symlink componentを経由したrun worktree作成を拒否することを検証する。"""
    root = cli_repository
    managed = root / ".cmoc" / "gu" / "worktree"
    external = tmp_path / "external"
    external.mkdir()

    if symlink_component == "base":
        managed.parent.mkdir(parents=True)
        managed.symlink_to(external, target_is_directory=True)
        symlink_path = managed
    else:
        managed.mkdir(parents=True)
        session = managed / SESSION_ID
        if symlink_component == "session":
            session.symlink_to(external / SESSION_ID, target_is_directory=True)
            symlink_path = session
        else:
            session.mkdir()
            symlink_path = session / RUN_ID
            symlink_path.symlink_to(
                external / SESSION_ID / RUN_ID, target_is_directory=True
            )

    target = managed / SESSION_ID / RUN_ID
    with pytest.raises(CmocError, match="run worktree path"):
        create_run_worktree(root, RUN_BRANCH, target)

    assert symlink_path.is_symlink()
    assert not (external / SESSION_ID / RUN_ID).exists()


def test_run_worktree_operations_reject_unregistered_managed_path(
    cli_repository: Path,
) -> None:
    """Git 未登録の同じ managed path を、作成でも削除でも保護する。"""
    root = cli_repository
    target = root / ".cmoc" / "gu" / "worktree" / SESSION_ID / RUN_ID
    target.mkdir(parents=True)
    (target / "keep.txt").write_text("keep\n")

    with pytest.raises(CmocError, match="run worktree path"):
        create_run_worktree(root, RUN_BRANCH, target)

    assert (target / "keep.txt").read_text() == "keep\n"

    with pytest.raises(CmocError, match="cmoc 管理外の worktree"):
        remove_worktree(root, target)

    assert (target / "keep.txt").read_text() == "keep\n"


def test_remove_worktree_rejects_symlink_components(
    committed_repository: Path, tmp_path: Path
) -> None:
    """symlink componentを経由したworktree削除を拒否することを検証する。"""
    root = committed_repository
    managed = root / ".cmoc" / "gu" / "worktree"
    external = tmp_path / "external"
    actual = external / SESSION_ID / RUN_ID
    actual.parent.mkdir(parents=True)
    run_git(
        root,
        "worktree",
        "add",
        "-b",
        RUN_BRANCH,
        str(actual),
        "HEAD",
    )

    target = managed / SESSION_ID / RUN_ID
    target.parent.mkdir(parents=True)
    # 外側の実 worktree と登録は不変。内側から親へ link を掛け替えて準備を共用する。
    for symlink_path, destination in (
        (target, actual),
        (target.parent, actual.parent),
        (managed, external),
    ):
        if symlink_path.exists():
            symlink_path.rmdir()
        symlink_path.symlink_to(destination, target_is_directory=True)
        with pytest.raises(CmocError, match="cmoc 管理外の worktree"):
            remove_worktree(root, target)

        assert symlink_path.is_symlink(), symlink_path
        assert actual.exists(), symlink_path
        symlink_path.unlink()


def test_remove_worktree_rejects_non_run_branch_at_managed_path(
    committed_repository: Path,
) -> None:
    """管理領域内でもrun branchと対応しないworktreeを削除しない。"""
    root = committed_repository
    target = root / ".cmoc" / "gu" / "worktree" / SESSION_ID / RUN_ID
    run_git(root, "worktree", "add", "-b", "ordinary", str(target), "HEAD")

    # repository と linked metadata は tmp_path 内で完結し、Git による後処理は不要。
    with pytest.raises(CmocError, match="cmoc 管理外の worktree"):
        remove_worktree(root, target)
    assert target.exists()


def test_remove_worktree_rejects_noncanonical_run_ids(
    committed_repository: Path,
) -> None:
    """旧 ID の branch と登録先が一致しても削除対象にしない。"""
    root = committed_repository
    old_id = "2026-09-29_15-04_07_123456789"
    target = root / ".cmoc/gu/worktree" / old_id / old_id
    run_git(root, "worktree", "add", "-b", f"cmoc/run/{old_id}/{old_id}", str(target))

    with pytest.raises(CmocError, match="cmoc 管理外の worktree"):
        remove_worktree(root, target)
    assert target.is_dir()
