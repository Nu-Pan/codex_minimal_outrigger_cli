"""サブコマンド横断テストを意味カテゴリ別に分割したファイル。"""

from .helpers import *


def test_session_abandon_marks_state_and_force_deletes_branch(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """`cmoc session abandon` は session branch を merge せず破棄する。"""
    repo = _init_repo(tmp_path)
    (repo / ".gitignore").write_text("/.cmoc/\n", encoding="utf-8")
    _git(repo, "add", ".gitignore")
    _git(repo, "commit", "-m", "ignore cmoc")
    home_branch = _git(repo, "branch", "--show-current").stdout.strip()
    _checkout_session_branch(repo)
    (repo / "feature.txt").write_text("feature\n", encoding="utf-8")
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "session-only feature")

    cmoc_session_abandon_impl(repo)

    captured = capsys.readouterr()
    branches = _git(
        repo,
        "branch",
        "--format=%(refname:short)",
    ).stdout.splitlines()
    state = json.loads(
        (
            repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_000000123.json"
        ).read_text(encoding="utf-8")
    )
    assert _git(repo, "branch", "--show-current").stdout.strip() == home_branch
    assert state["session"]["state"] == "abandoned"
    assert state["session"].get("joined_at") is None
    assert "cmoc/session/2026-05-10_22-21_10_000000123" not in branches
    assert (repo / "feature.txt").exists() is False
    assert (
        "abandoned session branch: cmoc/session/2026-05-10_22-21_10_000000123"
        in captured.out
    )


def test_session_abandon_rejects_null_session_home_branch(
    tmp_path: Path,
) -> None:
    """null home branch の session state では session abandon しない。"""
    repo = _init_repo(tmp_path)
    (repo / ".gitignore").write_text("/.cmoc/\n", encoding="utf-8")
    _git(repo, "add", ".gitignore")
    _git(repo, "commit", "-m", "ignore cmoc")
    home_branch = _git(repo, "branch", "--show-current").stdout.strip()
    _checkout_session_branch(repo)
    state_path = repo / ".cmoc" / "sessions" / (
        "2026-05-10_22-21_10_000000123.json"
    )
    state = json.loads(state_path.read_text(encoding="utf-8"))
    state["session"]["session_home_branch"] = None
    state_path.write_text(json.dumps(state), encoding="utf-8")
    (repo / "feature.txt").write_text("session only\n", encoding="utf-8")
    _git(repo, "add", "feature.txt")
    _git(repo, "commit", "-m", "session only")

    with pytest.raises(CmocError) as error:
        cmoc_session_abandon_impl(repo)

    branches = _git(repo, "branch", "--format=%(refname:short)").stdout
    state_after = json.loads(state_path.read_text(encoding="utf-8"))
    assert "session state ファイルの形式が不正です。" in error.value.message
    assert "session.session_home_branch: None" in error.value.detail
    assert _git(repo, "branch", "--show-current").stdout.strip() == (
        "cmoc/session/2026-05-10_22-21_10_000000123"
    )
    assert state_after["session"]["state"] == "active"
    assert state_after["session"]["session_home_branch"] is None
    assert "cmoc/session/2026-05-10_22-21_10_000000123" in branches


def test_session_abandon_dirty_worktree_rejects_null_session_home_branch_first(
    tmp_path: Path,
) -> None:
    """dirty 判定前に null home branch state を schema 検証で拒否する。"""
    repo = _init_repo(tmp_path)
    (repo / ".gitignore").write_text("/.cmoc/\n", encoding="utf-8")
    _git(repo, "add", ".gitignore")
    _git(repo, "commit", "-m", "ignore cmoc")
    _checkout_session_branch(repo)
    state_path = repo / ".cmoc" / "sessions" / (
        "2026-05-10_22-21_10_000000123.json"
    )
    state = json.loads(state_path.read_text(encoding="utf-8"))
    state["session"]["session_home_branch"] = None
    state_path.write_text(json.dumps(state), encoding="utf-8")
    state_before = json.loads(state_path.read_text(encoding="utf-8"))
    (repo / "dirty.txt").write_text("dirty\n", encoding="utf-8")

    with pytest.raises(CmocError) as error:
        cmoc_session_abandon_impl(repo)

    state_after = json.loads(state_path.read_text(encoding="utf-8"))
    branches = _git(repo, "branch", "--format=%(refname:short)").stdout
    assert "session state ファイルの形式が不正です。" in error.value.message
    assert "session.session_home_branch: None" in error.value.detail
    assert _git(repo, "branch", "--show-current").stdout.strip() == (
        "cmoc/session/2026-05-10_22-21_10_000000123"
    )
    assert state_after == state_before
    assert state_after["session"]["session_home_branch"] is None
    assert "cmoc/session/2026-05-10_22-21_10_000000123" in branches


def test_session_abandon_ensures_cmoc_ignored_before_cleanup(
    tmp_path: Path,
) -> None:
    """tracked `.cmoc` state を補修し、home branch 側も ignore 保証する。"""
    repo = _init_repo(tmp_path)
    home_branch = _git(repo, "branch", "--show-current").stdout.strip()
    _checkout_session_branch(repo)
    session_branch = _git(repo, "branch", "--show-current").stdout.strip()
    state_path = ".cmoc/sessions/2026-05-10_22-21_10_000000123.json"
    _git(repo, "add", "-f", state_path)
    _git(repo, "commit", "-m", "track session state")

    cmoc_session_abandon_impl(repo)

    state = json.loads((repo / state_path).read_text(encoding="utf-8"))
    branches = _git(repo, "branch", "--format=%(refname:short)").stdout
    assert _git(repo, "branch", "--show-current").stdout.strip() == home_branch
    assert state["session"]["state"] == "abandoned"
    assert session_branch not in branches
    assert "/.cmoc/" in (repo / ".gitignore").read_text(encoding="utf-8")
    assert _git(repo, "ls-files", "--", ".cmoc").stdout == ""
    assert _git(repo, "status", "--porcelain").stdout == ""


def test_session_abandon_rejects_apply_run_before_cleanup(
    tmp_path: Path,
) -> None:
    """apply run が ready でなければ branch/state を変更しない。"""
    repo = _init_repo(tmp_path)
    (repo / ".gitignore").write_text("/.cmoc/\n", encoding="utf-8")
    _git(repo, "add", ".gitignore")
    _git(repo, "commit", "-m", "ignore cmoc")
    _checkout_session_branch(repo)
    state_path = repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_000000123.json"
    state = json.loads(state_path.read_text(encoding="utf-8"))
    state["apply"]["state"] = "running"
    state["apply"]["apply_branch"] = (
        "cmoc/apply/2026-05-10_22-21_10_000000123/2026-05-10_22-22_10_000000123"
    )
    state["apply"]["oracle_snapshot_commit"] = _git(
        repo,
        "rev-parse",
        "HEAD",
    ).stdout.strip()
    state_path.write_text(json.dumps(state), encoding="utf-8")

    with pytest.raises(CmocError) as error:
        cmoc_session_abandon_impl(repo)

    state_after = json.loads(state_path.read_text(encoding="utf-8"))
    branches = _git(
        repo,
        "branch",
        "--format=%(refname:short)",
    ).stdout.splitlines()
    assert "apply run" in error.value.message
    assert _git(repo, "branch", "--show-current").stdout.strip() == (
        "cmoc/session/2026-05-10_22-21_10_000000123"
    )
    assert state_after["session"]["state"] == "active"
    assert "cmoc/session/2026-05-10_22-21_10_000000123" in branches


def test_session_abandon_rejects_uncommitted_changes_before_switch(
    tmp_path: Path,
) -> None:
    """未コミット差分がある場合は home branch へ戻らず停止する。"""
    repo = _init_repo(tmp_path)
    (repo / ".gitignore").write_text("/.cmoc/\n", encoding="utf-8")
    _git(repo, "add", ".gitignore")
    _git(repo, "commit", "-m", "ignore cmoc")
    _checkout_session_branch(repo)
    (repo / "dirty.txt").write_text("dirty\n", encoding="utf-8")

    with pytest.raises(CmocError) as error:
        cmoc_session_abandon_impl(repo)

    state = json.loads(
        (
            repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_000000123.json"
        ).read_text(encoding="utf-8")
    )
    assert "未コミットの変更" in error.value.message
    assert _git(repo, "branch", "--show-current").stdout.strip() == (
        "cmoc/session/2026-05-10_22-21_10_000000123"
    )
    assert state["session"]["state"] == "active"


def test_session_abandon_reports_home_switch_cleanup_failure(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """home branch への switch 失敗も cleanup 失敗として再実行を促す。"""
    repo = _init_repo(tmp_path)
    (repo / ".gitignore").write_text("/.cmoc/\n", encoding="utf-8")
    _git(repo, "add", ".gitignore")
    _git(repo, "commit", "-m", "ignore cmoc")
    home_branch = _git(repo, "branch", "--show-current").stdout.strip()
    session_branch = "cmoc/session/2026-05-10_22-21_10_000000123"
    _checkout_session_branch(repo)
    original_run_git = session_abandon_module.run_git

    def fail_home_switch(
        repo_root: Path,
        args: list[str],
        *,
        check: bool = True,
        text: bool = True,
        input_text: str | None = None,
        env: dict[str, str] | None = None,
    ) -> subprocess.CompletedProcess[str]:
        """cleanup 最初の home branch switch 失敗を模擬する。"""
        if args == ["switch", home_branch]:
            raise subprocess.CalledProcessError(
                1,
                ["git", *args],
                stderr="fake home switch failure",
            )
        return original_run_git(
            repo_root,
            args,
            check=check,
            text=text,
            input_text=input_text,
            env=env,
        )

    monkeypatch.setattr(session_abandon_module, "run_git", fail_home_switch)

    with pytest.raises(CmocError) as error:
        cmoc_session_abandon_impl(repo)

    state = json.loads(
        (
            repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_000000123.json"
        ).read_text(encoding="utf-8")
    )
    branches = _git(repo, "branch", "--format=%(refname:short)").stdout
    assert error.value.message == "session abandon のクリーンアップに失敗しました。"
    assert "cleanup failure" in error.value.detail
    assert "fake home switch failure" in error.value.detail
    assert "rollback failure" not in error.value.detail
    assert "`cmoc session abandon` を再実行" in error.value.actions[0]
    assert _git(repo, "branch", "--show-current").stdout.strip() == session_branch
    assert state["session"]["state"] == "active"
    assert session_branch in branches


def test_session_abandon_rolls_back_cmoc_repair_commit_on_cleanup_failure(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """`.cmoc` 補修後の失敗では、session branch HEAD も元へ戻す。"""
    repo = _init_repo(tmp_path)
    home_branch = _git(repo, "branch", "--show-current").stdout.strip()
    session_branch = "cmoc/session/2026-05-10_22-21_10_000000123"
    _checkout_session_branch(repo)
    original_session_head = _git(repo, "rev-parse", "HEAD").stdout.strip()
    original_run_git = session_abandon_module.run_git

    def fail_home_switch_after_repair(
        repo_root: Path,
        args: list[str],
        *,
        check: bool = True,
        text: bool = True,
        input_text: str | None = None,
        env: dict[str, str] | None = None,
    ) -> subprocess.CompletedProcess[str]:
        """`.cmoc` 補修 commit の直後に home branch switch 失敗を模擬する。"""
        if args == ["switch", home_branch]:
            raise subprocess.CalledProcessError(
                1,
                ["git", *args],
                stderr="fake home switch failure",
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
        session_abandon_module,
        "run_git",
        fail_home_switch_after_repair,
    )

    with pytest.raises(CmocError) as error:
        cmoc_session_abandon_impl(repo)

    state = json.loads(
        (
            repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_000000123.json"
        ).read_text(encoding="utf-8")
    )
    assert error.value.message == "session abandon のクリーンアップに失敗しました。"
    assert "rollback failure" not in error.value.detail
    assert _git(repo, "branch", "--show-current").stdout.strip() == session_branch
    assert _git(repo, "rev-parse", "HEAD").stdout.strip() == original_session_head
    assert (repo / ".gitignore").exists() is False
    assert _git(repo, "status", "--porcelain").stdout == ""
    assert state["session"]["state"] == "active"


def test_session_abandon_rolls_back_home_repair_commit_on_cleanup_failure(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """home branch 側の `.cmoc` 補修 commit も cleanup 失敗時に戻す。"""
    repo = _init_repo(tmp_path)
    home_branch = _git(repo, "branch", "--show-current").stdout.strip()
    original_home_head = _git(repo, "rev-parse", "HEAD").stdout.strip()
    session_branch = "cmoc/session/2026-05-10_22-21_10_000000123"
    _checkout_session_branch(repo)
    original_session_head = _git(repo, "rev-parse", "HEAD").stdout.strip()
    original_run_git = session_abandon_module.run_git

    def fail_branch_delete_after_home_repair(
        repo_root: Path,
        args: list[str],
        *,
        check: bool = True,
        text: bool = True,
        input_text: str | None = None,
        env: dict[str, str] | None = None,
    ) -> subprocess.CompletedProcess[str]:
        """home branch の `.cmoc` 補修 commit 後に branch 削除失敗を模擬する。"""
        if args == ["branch", "-D", session_branch]:
            raise subprocess.CalledProcessError(
                1,
                ["git", *args],
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
        session_abandon_module,
        "run_git",
        fail_branch_delete_after_home_repair,
    )

    with pytest.raises(CmocError) as error:
        cmoc_session_abandon_impl(repo)

    state = json.loads(
        (
            repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_000000123.json"
        ).read_text(encoding="utf-8")
    )
    assert error.value.message == "session abandon のクリーンアップに失敗しました。"
    assert "rollback failure" not in error.value.detail
    assert _git(repo, "branch", "--show-current").stdout.strip() == session_branch
    assert _git(repo, "rev-parse", "HEAD").stdout.strip() == original_session_head
    assert _git(repo, "rev-parse", home_branch).stdout.strip() == original_home_head
    assert (repo / ".gitignore").exists() is False
    assert _git(repo, "status", "--porcelain").stdout == ""
    assert state["session"]["state"] == "active"


def test_session_abandon_reports_rollback_switch_failure(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """checkout 復旧失敗も active state に戻し、再実行を促す。"""
    repo = _init_repo(tmp_path)
    (repo / ".gitignore").write_text("/.cmoc/\n", encoding="utf-8")
    _git(repo, "add", ".gitignore")
    _git(repo, "commit", "-m", "ignore cmoc")
    home_branch = _git(repo, "branch", "--show-current").stdout.strip()
    session_branch = "cmoc/session/2026-05-10_22-21_10_000000123"
    _checkout_session_branch(repo)
    original_run_git = session_abandon_module.run_git

    def fail_cleanup_and_restore_switch(
        repo_root: Path,
        args: list[str],
        *,
        check: bool = True,
        text: bool = True,
        input_text: str | None = None,
        env: dict[str, str] | None = None,
    ) -> subprocess.CompletedProcess[str]:
        """branch 削除失敗と session branch への復旧失敗を模擬する。"""
        if args == ["branch", "-D", session_branch]:
            raise subprocess.CalledProcessError(
                1,
                ["git", *args],
                stderr="fake branch delete failure",
            )
        if args == ["switch", session_branch]:
            return subprocess.CompletedProcess(
                ["git", *args],
                1,
                stdout="",
                stderr="fake switch failure",
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
        session_abandon_module,
        "run_git",
        fail_cleanup_and_restore_switch,
    )

    with pytest.raises(CmocError) as error:
        cmoc_session_abandon_impl(repo)

    state = json.loads(
        (
            repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_000000123.json"
        ).read_text(encoding="utf-8")
    )
    branches = _git(repo, "branch", "--format=%(refname:short)").stdout
    assert error.value.message == "session abandon のクリーンアップに失敗しました。"
    assert "cleanup failure" in error.value.detail
    assert "fake branch delete failure" in error.value.detail
    assert "rollback failure" in error.value.detail
    assert "fake switch failure" in error.value.detail
    assert "`cmoc session abandon` を再実行" in error.value.actions[0]
    assert _git(repo, "branch", "--show-current").stdout.strip() == home_branch
    assert state["session"]["state"] == "active"
    assert session_branch in branches


def test_session_abandon_reports_state_restore_failure_after_branch_delete_fails(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """branch 削除失敗後の active rollback 保存失敗を detail に含める。"""
    repo = _init_repo(tmp_path)
    (repo / ".gitignore").write_text("/.cmoc/\n", encoding="utf-8")
    _git(repo, "add", ".gitignore")
    _git(repo, "commit", "-m", "ignore cmoc")
    home_branch = _git(repo, "branch", "--show-current").stdout.strip()
    session_branch = "cmoc/session/2026-05-10_22-21_10_000000123"
    _checkout_session_branch(repo)
    original_run_git = session_abandon_module.run_git
    original_write_session_state = session_abandon_module.write_session_state
    restore_switches: list[list[str]] = []

    def fail_branch_delete(
        repo_root: Path,
        args: list[str],
        *,
        check: bool = True,
        text: bool = True,
        input_text: str | None = None,
        env: dict[str, str] | None = None,
    ) -> subprocess.CompletedProcess[str]:
        """cleanup の branch 削除失敗と rollback switch 呼び出しを観測する。"""
        if args == ["branch", "-D", session_branch]:
            raise subprocess.CalledProcessError(
                1,
                ["git", *args],
                stderr="fake branch delete failure",
            )
        if args == ["switch", session_branch]:
            restore_switches.append(args)
        return original_run_git(
            repo_root,
            args,
            check=check,
            text=text,
            input_text=input_text,
            env=env,
        )

    def fail_active_state_restore(
        repo_root: Path,
        session_id: str,
        state: dict[str, object],
    ) -> Path:
        """active への rollback 保存失敗を模擬する。"""
        session = state.get("session")
        if isinstance(session, dict) and session.get("state") == "active":
            raise OSError("fake state restore failure")
        return original_write_session_state(repo_root, session_id, state)

    monkeypatch.setattr(session_abandon_module, "run_git", fail_branch_delete)
    monkeypatch.setattr(
        session_abandon_module,
        "write_session_state",
        fail_active_state_restore,
    )

    with pytest.raises(CmocError) as error:
        cmoc_session_abandon_impl(repo)

    state = json.loads(
        (
            repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_000000123.json"
        ).read_text(encoding="utf-8")
    )
    branches = _git(repo, "branch", "--format=%(refname:short)").stdout
    assert error.value.message == "session abandon のクリーンアップに失敗しました。"
    assert "cleanup failure" in error.value.detail
    assert "fake branch delete failure" in error.value.detail
    assert "rollback failure" in error.value.detail
    assert "fake state restore failure" in error.value.detail
    assert "`cmoc session abandon` を再実行" in error.value.actions[0]
    assert restore_switches == [["switch", session_branch]]
    assert _git(repo, "branch", "--show-current").stdout.strip() == session_branch
    assert state["session"]["state"] == "abandoned"
    assert session_branch in branches


def test_session_abandon_does_not_delete_branch_when_abandoned_save_fails(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """abandoned 保存失敗時は branch 削除前に停止し、再実行可能に戻す。"""
    repo = _init_repo(tmp_path)
    (repo / ".gitignore").write_text("/.cmoc/\n", encoding="utf-8")
    _git(repo, "add", ".gitignore")
    _git(repo, "commit", "-m", "ignore cmoc")
    session_branch = "cmoc/session/2026-05-10_22-21_10_000000123"
    _checkout_session_branch(repo)
    original_session_head = _git(repo, "rev-parse", "HEAD").stdout.strip()
    delete_calls: list[list[str]] = []
    original_run_git = session_abandon_module.run_git
    original_write_session_state = session_abandon_module.write_session_state

    def observe_branch_delete(
        repo_root: Path,
        args: list[str],
        *,
        check: bool = True,
        text: bool = True,
        input_text: str | None = None,
        env: dict[str, str] | None = None,
    ) -> subprocess.CompletedProcess[str]:
        """state 保存失敗時に branch 削除へ進まないことを観測する。"""
        if args == ["branch", "-D", session_branch]:
            delete_calls.append(args)
        return original_run_git(
            repo_root,
            args,
            check=check,
            text=text,
            input_text=input_text,
            env=env,
        )

    def fail_abandoned_state_save(
        repo_root: Path,
        session_id: str,
        state: dict[str, object],
    ) -> Path:
        """cleanup 終盤の abandoned 保存失敗を模擬する。"""
        session = state.get("session")
        if isinstance(session, dict) and session.get("state") == "abandoned":
            raise OSError("fake abandoned save failure")
        return original_write_session_state(repo_root, session_id, state)

    monkeypatch.setattr(session_abandon_module, "run_git", observe_branch_delete)
    monkeypatch.setattr(
        session_abandon_module,
        "write_session_state",
        fail_abandoned_state_save,
    )

    with pytest.raises(CmocError) as error:
        cmoc_session_abandon_impl(repo)

    state = json.loads(
        (
            repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_000000123.json"
        ).read_text(encoding="utf-8")
    )
    branches = _git(repo, "branch", "--format=%(refname:short)").stdout
    assert error.value.message == "session abandon のクリーンアップに失敗しました。"
    assert "fake abandoned save failure" in error.value.detail
    assert "rollback failure" not in error.value.detail
    assert "`cmoc session abandon` を再実行" in error.value.actions[0]
    assert delete_calls == []
    assert _git(repo, "branch", "--show-current").stdout.strip() == session_branch
    assert _git(repo, "rev-parse", "HEAD").stdout.strip() == original_session_head
    assert state["session"]["state"] == "active"
    assert session_branch in branches
