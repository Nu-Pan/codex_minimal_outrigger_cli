"""サブコマンド横断テストを意味カテゴリ別に分割したファイル。"""

from .helpers import *


def test_session_fork_creates_session_branch_and_records_state(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """`cmoc session fork` は session branch 作成と state 記録を行う。"""
    repo = _init_repo(tmp_path)
    cmoc_init_impl(repo)
    home_branch = _git(repo, "branch", "--show-current").stdout.strip()
    base_commit = _git(repo, "rev-parse", "HEAD").stdout.strip()

    cmoc_session_fork_impl(repo)

    branch_name = _git(repo, "branch", "--show-current").stdout.strip()
    session_id = branch_name.removeprefix("cmoc/session/")
    record_path = repo / ".cmoc" / "sessions" / f"{session_id}.json"
    state = json.loads(record_path.read_text(encoding="utf-8"))
    assert branch_name.startswith("cmoc/session/")
    assert is_timestamp(session_id)
    assert state["session"]["state"] == "active"
    assert state["session"]["session_home_branch"] == home_branch
    assert state["session"]["session_start_commit"] == base_commit
    assert state["session"]["last_joined_apply_oracle_snapshot_commit"] is None
    assert "last_joined_apply_join_commit" not in state["session"]
    assert state["apply"] == {
        "state": "ready",
        "apply_branch": None,
        "oracle_snapshot_commit": None,
    }
    output = capsys.readouterr().out
    assert "(1/4) repository 状態検証" in output
    assert "session fork (1/4) repository 状態検証" not in output
    assert "session branch 作成試行 (1/10)" in output


def test_session_fork_repairs_missing_cmoc_ignore_before_clean_check(
    tmp_path: Path,
) -> None:
    """`.cmoc` ignore 不足は内部初期化 commit として補修して続行する。"""
    repo = _init_repo(tmp_path)
    home_branch = _git(repo, "branch", "--show-current").stdout.strip()
    initial_head = _git(repo, "rev-parse", "HEAD").stdout.strip()

    cmoc_session_fork_impl(repo)

    branch_name = _git(repo, "branch", "--show-current").stdout.strip()
    session_id = branch_name.removeprefix("cmoc/session/")
    state = json.loads(
        (repo / ".cmoc" / "sessions" / f"{session_id}.json").read_text(
            encoding="utf-8",
        )
    )
    assert branch_name.startswith("cmoc/session/")
    assert state["session"]["session_start_commit"] == initial_head
    assert _git(repo, "merge-base", home_branch, branch_name).stdout.strip() == (
        initial_head
    )
    assert _git(repo, "show", "HEAD:.gitignore").stdout == "/.cmoc/\n"
    assert _git(repo, "log", "-1", "--pretty=%s").stdout.strip() == (
        "Initialize cmoc session branch"
    )
    assert _git(repo, "status", "--porcelain").stdout == ""


def test_session_fork_ensures_cmoc_ignore_before_active_state_scan(
    tmp_path: Path,
) -> None:
    """ignore 保証が済む前に `.cmoc/sessions` の壊れた state を読まない。"""
    repo = _init_repo(tmp_path)
    home_branch = _git(repo, "branch", "--show-current").stdout.strip()
    broken_path = repo / ".cmoc" / "sessions" / "broken.json"
    broken_path.parent.mkdir(parents=True)
    broken_path.write_text("{not json", encoding="utf-8")

    with pytest.raises(CmocError) as error:
        cmoc_session_fork_impl(repo)

    assert "未コミットの変更" in error.value.message
    assert str((repo / ".cmoc").resolve()) in error.value.detail
    assert "JSON が不正" not in error.value.message
    assert _git(repo, "branch", "--show-current").stdout.strip() == home_branch
    assert _session_state_paths(repo) == [broken_path]


@pytest.mark.parametrize(
    ("target_kind", "expected_message"),
    [
        ("commit_hash", "detached HEAD"),
        ("remote_tracking_branch", "detached HEAD"),
    ],
)
def test_session_fork_rejects_non_local_branch_start_points(
    tmp_path: Path,
    target_kind: str,
    expected_message: str,
) -> None:
    """`cmoc session fork` は local branch 以外から開始しない。"""
    repo = _init_repo(tmp_path)
    start_branch = _git(repo, "branch", "--show-current").stdout.strip()
    start_commit = _git(repo, "rev-parse", "HEAD").stdout.strip()
    _git(repo, "update-ref", "refs/remotes/origin/main", start_commit)
    checkout_target = start_commit
    if target_kind == "remote_tracking_branch":
        checkout_target = "origin/main"
    _git(repo, "checkout", checkout_target)

    with pytest.raises(CmocError) as error:
        cmoc_session_fork_impl(repo)

    assert expected_message in error.value.message
    assert _git(repo, "rev-parse", "HEAD").stdout.strip() == start_commit
    assert start_branch in _git(repo, "branch", "--format=%(refname:short)").stdout
    assert _session_state_paths(repo) == []


def test_session_fork_rejects_cmoc_managed_branch_before_creating_state(
    tmp_path: Path,
) -> None:
    """cmoc 管理 branch 上では session branch を二重作成しない。"""
    repo = _init_repo(tmp_path)
    _git(repo, "checkout", "-b", "cmoc/session/2026-05-10_22-21_10_000000123")

    with pytest.raises(CmocError) as error:
        cmoc_session_fork_impl(repo)

    assert "cmoc 管理 branch" in error.value.message
    branches = _git(repo, "branch", "--format=%(refname:short)").stdout
    assert branches.count("cmoc/session/") == 1
    assert _session_state_paths(repo) == []


@pytest.mark.parametrize(
    "branch_name",
    [
        "cmoc/session/not-a-timestamp",
        "cmoc/session/2026-05-10_22-21_10_000000123/extra",
        "cmoc/apply/foo/bar",
        "cmoc/apply/2026-05-10_22-21_10_000000123/run-1",
    ],
)
def test_session_fork_rejects_cmoc_reserved_branch_namespace(
    tmp_path: Path,
    branch_name: str,
) -> None:
    """不正形式でも cmoc 予約 namespace 上では session を開始しない。"""
    repo = _init_repo(tmp_path)
    _git(repo, "checkout", "-b", branch_name)

    with pytest.raises(CmocError) as error:
        cmoc_session_fork_impl(repo)

    assert "cmoc 管理 branch" in error.value.message
    branches = _git(repo, "branch", "--format=%(refname:short)").stdout.splitlines()
    assert branch_name in branches
    assert [
        branch
        for branch in branches
        if branch.startswith("cmoc/session/") and branch != branch_name
    ] == []
    assert _session_state_paths(repo) == []


def test_session_fork_rejects_uncommitted_changes_before_branch_creation(
    tmp_path: Path,
) -> None:
    """未コミット差分がある場合は branch 作成前に止める。"""
    repo = _init_repo(tmp_path)
    start_branch = _git(repo, "branch", "--show-current").stdout.strip()
    (repo / "README.md").write_text("changed\n", encoding="utf-8")

    with pytest.raises(CmocError) as error:
        cmoc_session_fork_impl(repo)

    assert "未コミットの変更" in error.value.message
    assert _git(repo, "branch", "--show-current").stdout.strip() == start_branch
    assert _session_state_paths(repo) == []


def test_session_fork_rejects_existing_active_session_for_home_branch(
    tmp_path: Path,
) -> None:
    """同じ home branch の active session がある場合は新規作成しない。"""
    repo = _init_repo(tmp_path)
    home_branch = _git(repo, "branch", "--show-current").stdout.strip()
    start_commit = _git(repo, "rev-parse", "HEAD").stdout.strip()
    (repo / ".gitignore").write_text("/.cmoc/\n", encoding="utf-8")
    _git(repo, "add", ".gitignore")
    _git(repo, "commit", "-m", "ignore cmoc")
    session_id = "2026-05-10_22-21_10_000000123"
    _git(repo, "branch", f"cmoc/session/{session_id}")
    write_session_state(
        repo,
        session_id,
        {
            "session": {
                "state": "active",
                "session_home_branch": home_branch,
                "session_start_commit": start_commit,
                "last_joined_apply_oracle_snapshot_commit": None,
            },
            "apply": {
                "state": "ready",
                "apply_branch": None,
                "oracle_snapshot_commit": None,
            },
        },
    )

    with pytest.raises(CmocError) as error:
        cmoc_session_fork_impl(repo)

    assert "active session" in error.value.message
    assert error.value.detail == session_id
    assert _git(repo, "branch", "--show-current").stdout.strip() == home_branch
    assert _session_state_paths(repo) == [
        repo / ".cmoc" / "sessions" / f"{session_id}.json",
    ]


def test_session_fork_rejects_null_active_session_home_branch(
    tmp_path: Path,
) -> None:
    """null home branch の active session state は schema 検証で止める。"""
    repo = _init_repo(tmp_path)
    cmoc_init_impl(repo)
    start_commit = _git(repo, "rev-parse", "HEAD").stdout.strip()
    _git(repo, "branch", "feature", start_commit)

    cmoc_session_fork_impl(repo)
    first_session_branch = _git(repo, "branch", "--show-current").stdout.strip()
    first_session_id = first_session_branch.removeprefix("cmoc/session/")
    first_state_path = repo / ".cmoc" / "sessions" / f"{first_session_id}.json"
    first_state = json.loads(first_state_path.read_text(encoding="utf-8"))
    first_state["session"]["session_home_branch"] = None
    first_state_path.write_text(json.dumps(first_state), encoding="utf-8")
    _git(repo, "checkout", "feature")

    with pytest.raises(CmocError) as error:
        cmoc_session_fork_impl(repo)

    first_state = json.loads(first_state_path.read_text(encoding="utf-8"))
    assert "session state ファイルの形式が不正です。" in error.value.message
    assert "session.session_home_branch: None" in error.value.detail
    assert first_state["session"]["session_home_branch"] is None
    assert _git(repo, "branch", "--show-current").stdout.strip() == "feature"
    assert _session_state_paths(repo) == [
        repo / ".cmoc" / "sessions" / f"{first_session_id}.json",
    ]


def test_session_fork_rechecks_active_session_before_branch_creation(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """作成直前に active session が見えた場合も新規 session を作らない。"""
    repo = _init_repo(tmp_path)
    cmoc_init_impl(repo)
    home_branch = _git(repo, "branch", "--show-current").stdout.strip()
    calls = 0

    def racing_active_session_ids(
        _repo_root: Path,
        _session_home_branch: str,
    ) -> list[str]:
        """事前確認後に別 session が作られた競合を模擬する。"""
        nonlocal calls
        calls += 1
        if calls == 1:
            return []
        return ["existing"]

    monkeypatch.setattr(
        session_fork_module,
        "active_session_ids_for_home_branch",
        racing_active_session_ids,
    )

    with pytest.raises(CmocError) as error:
        cmoc_session_fork_impl(repo)

    branches = _git(repo, "branch", "--format=%(refname:short)").stdout
    assert "active session" in error.value.message
    assert error.value.detail == "existing"
    assert calls == 2
    assert _git(repo, "branch", "--show-current").stdout.strip() == home_branch
    assert "cmoc/session/" not in branches
    assert _session_state_paths(repo) == []


def test_session_fork_from_linked_worktree_records_state_in_main_repo_root(
    tmp_path: Path,
) -> None:
    """linked worktree で作った session state は main repo-root 側へ保存する。"""
    repo = _init_repo(tmp_path)
    (repo / ".gitignore").write_text("/.cmoc/\n", encoding="utf-8")
    _git(repo, "add", ".gitignore")
    _git(repo, "commit", "-m", "ignore cmoc")
    linked = tmp_path / "linked"
    _git(repo, "worktree", "add", "-b", "feature", str(linked), "HEAD")

    cmoc_session_fork_impl(linked)

    branch_name = _git(linked, "branch", "--show-current").stdout.strip()
    session_id = branch_name.removeprefix("cmoc/session/")
    assert (repo / ".cmoc" / "sessions" / f"{session_id}.json").exists()
    assert not (linked / ".cmoc" / "sessions" / f"{session_id}.json").exists()


def test_session_fork_from_linked_worktree_rejects_main_active_session(
    tmp_path: Path,
) -> None:
    """active session 判定は main repo-root 側の state を見る。"""
    repo = _init_repo(tmp_path)
    (repo / ".gitignore").write_text("/.cmoc/\n", encoding="utf-8")
    _git(repo, "add", ".gitignore")
    _git(repo, "commit", "-m", "ignore cmoc")
    linked = tmp_path / "linked"
    _git(repo, "worktree", "add", "-b", "feature", str(linked), "HEAD")
    start_commit = _git(linked, "rev-parse", "HEAD").stdout.strip()
    session_id = "2026-05-10_22-21_10_000000123"
    _git(linked, "branch", f"cmoc/session/{session_id}")
    write_session_state(
        repo,
        session_id,
        {
            "session": {
                "state": "active",
                "session_home_branch": "feature",
                "session_start_commit": start_commit,
                "last_joined_apply_oracle_snapshot_commit": None,
            },
            "apply": {
                "state": "ready",
                "apply_branch": None,
                "oracle_snapshot_commit": None,
            },
        },
    )

    with pytest.raises(CmocError) as error:
        cmoc_session_fork_impl(linked)

    assert "active session" in error.value.message
    assert error.value.detail == session_id
    assert _git(linked, "branch", "--show-current").stdout.strip() == "feature"
    assert _session_state_paths(repo) == [
        repo / ".cmoc" / "sessions" / f"{session_id}.json",
    ]
    assert _session_state_paths(linked) == []


def test_session_fork_rejects_malformed_session_state_before_branch_creation(
    tmp_path: Path,
) -> None:
    """壊れた session state がある場合は active guard を fail closed にする。"""
    repo = _init_repo(tmp_path)
    home_branch = _git(repo, "branch", "--show-current").stdout.strip()
    (repo / ".gitignore").write_text("/.cmoc/\n", encoding="utf-8")
    _git(repo, "add", ".gitignore")
    _git(repo, "commit", "-m", "ignore cmoc")
    broken_path = repo / ".cmoc" / "sessions" / "broken.json"
    broken_path.parent.mkdir(parents=True)
    broken_path.write_text("{not json", encoding="utf-8")

    with pytest.raises(CmocError) as error:
        cmoc_session_fork_impl(repo)

    branches = _git(repo, "branch", "--format=%(refname:short)").stdout
    assert "JSON が不正" in error.value.message
    assert str(broken_path) in error.value.detail
    assert _git(repo, "branch", "--show-current").stdout.strip() == home_branch
    assert "cmoc/session/" not in branches
    assert _session_state_paths(repo) == [broken_path]


def test_session_fork_rejects_orphan_session_branch_before_creation(
    tmp_path: Path,
) -> None:
    """対応 state がない session branch が残る場合は新規 session を作らない。"""
    repo = _init_repo(tmp_path)
    cmoc_init_impl(repo)
    home_branch = _git(repo, "branch", "--show-current").stdout.strip()
    orphan_branch = "cmoc/session/2026-05-10_22-21_10_000000123"
    _git(repo, "branch", orphan_branch)

    with pytest.raises(CmocError) as error:
        cmoc_session_fork_impl(repo)

    branches = _git(repo, "branch", "--format=%(refname:short)").stdout
    assert "session state がない session branch" in error.value.message
    assert orphan_branch in error.value.detail
    assert _git(repo, "branch", "--show-current").stdout.strip() == home_branch
    assert branches.count("cmoc/session/") == 1
    assert _session_state_paths(repo) == []


def test_session_fork_rolls_back_branch_when_state_write_fails(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """state 保存に失敗した session branch は残さない。"""
    repo = _init_repo(tmp_path)
    cmoc_init_impl(repo)
    home_branch = _git(repo, "branch", "--show-current").stdout.strip()

    def fail_write_session_state(
        _repo_root: Path,
        _session_id: str,
        _state: dict[str, object],
    ) -> Path:
        """session state 保存失敗を模擬する。"""
        raise OSError("fake state write failure")

    monkeypatch.setattr(
        session_fork_module,
        "write_session_state",
        fail_write_session_state,
    )

    with pytest.raises(CmocError) as error:
        cmoc_session_fork_impl(repo)

    branches = _git(repo, "branch", "--format=%(refname:short)").stdout
    assert "session state の保存に失敗" in error.value.message
    assert "fake state write failure" in error.value.detail
    assert _git(repo, "branch", "--show-current").stdout.strip() == home_branch
    assert "cmoc/session/" not in branches
    assert _session_state_paths(repo) == []
    assert _git(repo, "status", "--porcelain").stdout == ""


def test_session_fork_keeps_state_when_rollback_branch_delete_fails(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """rollback が branch を消せない場合は対応する state を残す。"""
    repo = _init_repo(tmp_path)
    cmoc_init_impl(repo)
    home_branch = _git(repo, "branch", "--show-current").stdout.strip()
    session_id = "2026-05-10_22-21_10_000000123"
    session_branch = f"cmoc/session/{session_id}"
    original_run_git = session_fork_module.run_git

    monkeypatch.setattr(
        session_fork_module,
        "make_timestamp",
        lambda: session_id,
    )

    def fail_after_writing_session_state(
        repo_root: Path,
        state_session_id: str,
        state: dict[str, object],
    ) -> Path:
        """state 作成後の保存失敗を模擬する。"""
        path = write_session_state(repo_root, state_session_id, state)
        raise OSError(f"fake state write failure after {path.name}")

    def fail_branch_delete(
        repo_root: Path,
        args: list[str],
        *,
        check: bool = True,
        text: bool = True,
        input_text: str | None = None,
        env: dict[str, str] | None = None,
    ) -> subprocess.CompletedProcess[str]:
        """rollback 中の session branch 削除失敗を模擬する。"""
        if args == ["branch", "-D", session_branch]:
            return subprocess.CompletedProcess(
                ["git", *args],
                1,
                stdout="",
                stderr="fake branch delete failure",
            )
        return original_run_git(
            repo_root,
            args,
            check=check,
            text=text,
            input_text=input_text,
            env=env,
        )

    monkeypatch.setattr(
        session_fork_module,
        "write_session_state",
        fail_after_writing_session_state,
    )
    monkeypatch.setattr(session_fork_module, "run_git", fail_branch_delete)

    with pytest.raises(CmocError) as error:
        cmoc_session_fork_impl(repo)

    branches = _git(repo, "branch", "--format=%(refname:short)").stdout
    state_path = repo / ".cmoc" / "sessions" / f"{session_id}.json"
    state = json.loads(state_path.read_text(encoding="utf-8"))
    assert "session state の保存に失敗" in error.value.message
    assert "完全には取り消せません" in error.value.message
    assert "fake branch delete failure" in error.value.detail
    assert _git(repo, "branch", "--show-current").stdout.strip() == home_branch
    assert session_branch in branches
    assert state["session"]["state"] == "active"
    assert state["session"]["session_home_branch"] == home_branch
    assert state["apply"]["state"] == "ready"
