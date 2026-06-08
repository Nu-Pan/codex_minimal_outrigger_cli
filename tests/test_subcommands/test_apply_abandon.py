"""サブコマンド横断テストを意味カテゴリ別に分割したファイル。"""

from .helpers import *


def test_apply_abandon_deletes_apply_artifacts_and_resets_state(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """`cmoc apply abandon` は apply 成果物を merge せず破棄する。"""
    repo = _init_repo(tmp_path)
    _checkout_session_branch(repo)
    oracle_snapshot = _add_oracle_snapshot(repo)
    apply_branch, apply_worktree, report_path = _create_completed_apply_run(
        repo,
        oracle_snapshot,
    )
    (apply_worktree / "feature.txt").write_text("implemented\n", encoding="utf-8")
    _git(apply_worktree, "add", "feature.txt")
    _git(apply_worktree, "commit", "-m", "implement feature")

    cmoc_apply_abandon_impl(repo)

    output = capsys.readouterr().out
    state = json.loads(
        (
            repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_000000123.json"
        ).read_text(encoding="utf-8")
    )
    assert state["apply"] == {
        "apply_branch": None,
        "oracle_snapshot_commit": None,
        "state": "ready",
    }
    assert _git(repo, "branch", "--show-current").stdout.strip() == (
        "cmoc/session/2026-05-10_22-21_10_000000123"
    )
    assert _git(repo, "branch", "--list", apply_branch).stdout == ""
    assert not apply_worktree.exists()
    assert report_path.exists()
    assert not (repo / "feature.txt").exists()
    assert f"abandoned apply branch: {apply_branch}" in output
    assert f"abandoned apply worktree: {apply_worktree}" in output
    assert "previous apply.state: completed" in output
    assert "current apply.state: ready" in output


def test_apply_abandon_rejects_cross_session_apply_branch_without_cleanup(
    tmp_path: Path,
) -> None:
    """apply abandon は別 session の apply branch/worktree を削除しない。"""
    repo = _init_repo(tmp_path)
    _checkout_session_branch(repo)
    oracle_snapshot = _add_oracle_snapshot(repo)
    _create_completed_apply_run(repo, oracle_snapshot)
    other_session_id = "2026-05-10_22-21_10_000000999"
    other_apply_run_id = "2026-05-10_22-22_10_000000123"
    other_apply_branch = f"cmoc/apply/{other_session_id}/{other_apply_run_id}"
    other_apply_worktree = (
        repo
        / ".cmoc"
        / "worktrees"
        / other_session_id
        / other_apply_run_id
    )
    _git(repo, "branch", other_apply_branch, oracle_snapshot)
    _git(repo, "worktree", "add", str(other_apply_worktree), other_apply_branch)
    state_path = (
        repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_000000123.json"
    )
    state = json.loads(state_path.read_text(encoding="utf-8"))
    state["apply"]["apply_branch"] = other_apply_branch
    state["apply"]["oracle_snapshot_commit"] = oracle_snapshot
    state_path.write_text(json.dumps(state), encoding="utf-8")

    with pytest.raises(CmocError) as error_info:
        cmoc_apply_abandon_impl(repo)

    assert "同じ session の apply branch" in error_info.value.actions[0]
    assert _git(repo, "branch", "--list", other_apply_branch).stdout.strip()
    assert other_apply_worktree.exists()


def test_apply_abandon_accepts_apply_branch_worktree(
    tmp_path: Path,
) -> None:
    """apply worktree 上から実行しても所有元 repo root の state を更新する。"""
    repo = _init_repo(tmp_path)
    _checkout_session_branch(repo)
    oracle_snapshot = _add_oracle_snapshot(repo)
    apply_branch, apply_worktree, _report_path = _create_completed_apply_run(
        repo,
        oracle_snapshot,
    )

    cmoc_apply_abandon_impl(apply_worktree)

    state = json.loads(
        (
            repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_000000123.json"
        ).read_text(encoding="utf-8")
    )
    assert state["apply"]["state"] == "ready"
    assert _git(repo, "branch", "--list", apply_branch).stdout == ""
    assert not apply_worktree.exists()


def test_apply_abandon_relocates_from_apply_branch_before_cleanup(
    tmp_path: Path,
) -> None:
    """apply branch からの実行時は session branch の worktree へ移動してから消す。"""
    repo = _init_repo(tmp_path)
    home_branch = _git(repo, "branch", "--show-current").stdout.strip()
    _checkout_session_branch(repo)
    session_branch = _git(repo, "branch", "--show-current").stdout.strip()
    oracle_snapshot = _add_oracle_snapshot(repo)
    apply_branch, apply_worktree, _report_path = _create_completed_apply_run(
        repo,
        oracle_snapshot,
    )
    _git(repo, "switch", home_branch)

    cmoc_apply_abandon_impl(apply_worktree)

    assert _git(repo, "branch", "--show-current").stdout.strip() == session_branch
    assert _git(repo, "branch", "--list", apply_branch).stdout == ""
    assert not apply_worktree.exists()


def test_apply_abandon_ignores_worktree_local_log_cmoc(
    tmp_path: Path,
) -> None:
    """ログ用 `.cmoc` がある apply worktree からでも所有元の state を更新する。"""
    repo = _init_repo(tmp_path)
    _checkout_session_branch(repo)
    oracle_snapshot = _add_oracle_snapshot(repo)
    apply_branch, apply_worktree, _report_path = _create_completed_apply_run(
        repo,
        oracle_snapshot,
    )
    (apply_worktree / ".cmoc" / "logs" / "sub_commands").mkdir(parents=True)

    cmoc_apply_abandon_impl(apply_worktree)

    state = json.loads(
        (
            repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_000000123.json"
        ).read_text(encoding="utf-8")
    )
    assert state["apply"]["state"] == "ready"
    assert _git(repo, "branch", "--list", apply_branch).stdout == ""
    assert not apply_worktree.exists()


def test_apply_abandon_rejects_dirty_session_branch_worktree(
    tmp_path: Path,
) -> None:
    """apply branch からの実行でも session branch worktree の差分で停止する。"""
    repo = _init_repo(tmp_path)
    home_branch = _git(repo, "branch", "--show-current").stdout.strip()
    _checkout_session_branch(repo)
    session_branch = _git(repo, "branch", "--show-current").stdout.strip()
    oracle_snapshot = _add_oracle_snapshot(repo)
    apply_branch, apply_worktree, _report_path = _create_completed_apply_run(
        repo,
        oracle_snapshot,
    )
    _git(repo, "switch", home_branch)
    session_worktree = tmp_path / "session-worktree"
    _git(repo, "worktree", "add", str(session_worktree), session_branch)
    (session_worktree / "session-dirty.txt").write_text(
        "dirty\n",
        encoding="utf-8",
    )

    with pytest.raises(CmocError) as error_info:
        cmoc_apply_abandon_impl(apply_worktree)

    assert "未コミットの変更" in error_info.value.message
    assert "session-dirty.txt" in error_info.value.detail
    assert _git(repo, "branch", "--list", apply_branch).stdout.strip()
    assert apply_worktree.exists()


def test_apply_abandon_does_not_check_unrelated_owner_worktree(
    tmp_path: Path,
) -> None:
    """session branch が別 worktree にある場合、所有元 root の差分は見ない。"""
    repo = _init_repo(tmp_path)
    home_branch = _git(repo, "branch", "--show-current").stdout.strip()
    _checkout_session_branch(repo)
    session_branch = _git(repo, "branch", "--show-current").stdout.strip()
    oracle_snapshot = _add_oracle_snapshot(repo)
    apply_branch, apply_worktree, _report_path = _create_completed_apply_run(
        repo,
        oracle_snapshot,
    )
    _git(repo, "switch", home_branch)
    session_worktree = tmp_path / "session-worktree"
    _git(repo, "worktree", "add", str(session_worktree), session_branch)
    (repo / "home-dirty.txt").write_text("dirty\n", encoding="utf-8")

    cmoc_apply_abandon_impl(apply_worktree)

    state = json.loads(
        (
            repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_000000123.json"
        ).read_text(encoding="utf-8")
    )
    assert state["apply"]["state"] == "ready"
    assert _git(repo, "branch", "--list", apply_branch).stdout == ""
    assert not apply_worktree.exists()
    assert (repo / "home-dirty.txt").exists()


def test_apply_abandon_rejects_dirty_owner_before_session_switch(
    tmp_path: Path,
) -> None:
    """session worktree 作成に使う owner root の差分を持ち越さない。"""
    repo = _init_repo(tmp_path)
    home_branch = _git(repo, "branch", "--show-current").stdout.strip()
    _checkout_session_branch(repo)
    oracle_snapshot = _add_oracle_snapshot(repo)
    apply_branch, apply_worktree, _report_path = _create_completed_apply_run(
        repo,
        oracle_snapshot,
    )
    _git(repo, "switch", home_branch)
    (repo / "home-dirty.txt").write_text("dirty\n", encoding="utf-8")

    with pytest.raises(CmocError) as error_info:
        cmoc_apply_abandon_impl(apply_worktree)

    state = json.loads(
        (
            repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_000000123.json"
        ).read_text(encoding="utf-8")
    )
    assert "未コミットの変更" in error_info.value.message
    assert "home-dirty.txt" in error_info.value.detail
    assert state["apply"]["state"] == "completed"
    assert _git(repo, "branch", "--show-current").stdout.strip() == home_branch
    assert _git(repo, "branch", "--list", apply_branch).stdout.strip()
    assert apply_worktree.exists()


def test_apply_abandon_rejects_ready_state_without_cleanup(
    tmp_path: Path,
) -> None:
    """apply.state が ready の場合は破棄対象なしとして停止する。"""
    repo = _init_repo(tmp_path)
    _checkout_session_branch(repo)

    with pytest.raises(CmocError) as error_info:
        cmoc_apply_abandon_impl(repo)

    state = json.loads(
        (
            repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_000000123.json"
        ).read_text(encoding="utf-8")
    )
    assert "破棄対象の apply run" in error_info.value.message
    assert state["apply"]["state"] == "ready"


def test_apply_abandon_accepts_error_state(
    tmp_path: Path,
) -> None:
    """apply.state が error の apply run も成果物を破棄できる。"""
    repo = _init_repo(tmp_path)
    _checkout_session_branch(repo)
    oracle_snapshot = _add_oracle_snapshot(repo)
    apply_branch, apply_worktree, _report_path = _create_completed_apply_run(
        repo,
        oracle_snapshot,
    )
    state_path = repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_000000123.json"
    state = json.loads(state_path.read_text(encoding="utf-8"))
    state["apply"]["state"] = "error"
    state_path.write_text(json.dumps(state), encoding="utf-8")

    cmoc_apply_abandon_impl(repo)

    state = json.loads(state_path.read_text(encoding="utf-8"))
    assert state["apply"]["state"] == "ready"
    assert _git(repo, "branch", "--list", apply_branch).stdout == ""
    assert not apply_worktree.exists()


def test_apply_abandon_stops_running_process_and_resets_state(
    tmp_path: Path,
) -> None:
    """running apply は process を停止してから成果物を破棄する。"""
    repo = _init_repo(tmp_path)
    _checkout_session_branch(repo)
    oracle_snapshot = _add_oracle_snapshot(repo)
    apply_branch, apply_worktree, _report_path = _create_completed_apply_run(
        repo,
        oracle_snapshot,
    )
    process = subprocess.Popen(
        [sys.executable, "-c", "import time; time.sleep(60)"],
    )
    state_path = repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_000000123.json"
    state = json.loads(state_path.read_text(encoding="utf-8"))
    state["apply"]["state"] = "running"
    write_session_state(repo, "2026-05-10_22-21_10_000000123", state)
    write_apply_process_id(
        repo,
        "2026-05-10_22-21_10_000000123",
        process.pid,
        apply_branch,
    )

    try:
        cmoc_apply_abandon_impl(repo)
    finally:
        process.wait(timeout=5)

    state = json.loads(state_path.read_text(encoding="utf-8"))
    assert process.returncode is not None
    assert state["apply"]["state"] == "ready"
    assert "process_id" not in state["apply"]
    assert not (
        repo / ".cmoc" / "runtime" / "apply" / "2026-05-10_22-21_10_000000123.pid"
    ).exists()
    assert _git(repo, "branch", "--list", apply_branch).stdout == ""
    assert not apply_worktree.exists()


def test_apply_abandon_rejects_legacy_pid_without_killing_process(
    tmp_path: Path,
) -> None:
    """PID だけの runtime file では apply process と断定せず停止しない。"""
    repo = _init_repo(tmp_path)
    _checkout_session_branch(repo)
    oracle_snapshot = _add_oracle_snapshot(repo)
    apply_branch, apply_worktree, _report_path = _create_completed_apply_run(
        repo,
        oracle_snapshot,
    )
    process = subprocess.Popen(
        [sys.executable, "-c", "import time; time.sleep(60)"],
    )
    state_path = repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_000000123.json"
    state = json.loads(state_path.read_text(encoding="utf-8"))
    state["apply"]["state"] = "running"
    write_session_state(repo, "2026-05-10_22-21_10_000000123", state)
    process_id_path = (
        repo / ".cmoc" / "runtime" / "apply"
        / "2026-05-10_22-21_10_000000123.pid"
    )
    process_id_path.parent.mkdir(parents=True)
    process_id_path.write_text(f"{process.pid}\n", encoding="utf-8")

    try:
        with pytest.raises(CmocError) as error_info:
            cmoc_apply_abandon_impl(repo)

        assert "安全に特定できませんでした" in error_info.value.message
        assert process.poll() is None
        state = json.loads(state_path.read_text(encoding="utf-8"))
        assert state["apply"]["state"] == "running"
        assert _git(repo, "branch", "--list", apply_branch).stdout.strip()
        assert apply_worktree.exists()
    finally:
        process.terminate()
        process.wait(timeout=5)


def test_apply_abandon_rejects_running_state_without_process_id(
    tmp_path: Path,
) -> None:
    """running state に process id が無い場合は cleanup せず停止する。"""
    repo = _init_repo(tmp_path)
    _checkout_session_branch(repo)
    oracle_snapshot = _add_oracle_snapshot(repo)
    apply_branch, apply_worktree, _report_path = _create_completed_apply_run(
        repo,
        oracle_snapshot,
    )
    state_path = repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_000000123.json"
    state = json.loads(state_path.read_text(encoding="utf-8"))
    state["apply"]["state"] = "running"
    write_session_state(repo, "2026-05-10_22-21_10_000000123", state)

    with pytest.raises(CmocError) as error_info:
        cmoc_apply_abandon_impl(repo)

    state = json.loads(state_path.read_text(encoding="utf-8"))
    assert "process id が記録されていません" in error_info.value.message
    assert "apply.state: running" in error_info.value.detail
    assert state["apply"]["state"] == "running"
    assert _git(repo, "branch", "--list", apply_branch).stdout.strip()
    assert apply_worktree.exists()


def test_apply_abandon_rejects_unknown_state_without_cleanup(
    tmp_path: Path,
) -> None:
    """未知の apply.state は state 破損として扱い cleanup しない。"""
    repo = _init_repo(tmp_path)
    _checkout_session_branch(repo)
    oracle_snapshot = _add_oracle_snapshot(repo)
    apply_branch, apply_worktree, _report_path = _create_completed_apply_run(
        repo,
        oracle_snapshot,
    )
    state_path = repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_000000123.json"
    state = json.loads(state_path.read_text(encoding="utf-8"))
    state["apply"]["state"] = "paused"
    state_path.write_text(json.dumps(state), encoding="utf-8")

    with pytest.raises(CmocError) as error_info:
        cmoc_apply_abandon_impl(repo)

    state = json.loads(state_path.read_text(encoding="utf-8"))
    assert "形式が不正" in error_info.value.message
    assert "apply.state: paused" in error_info.value.detail
    assert state["apply"]["state"] == "paused"
    assert _git(repo, "branch", "--list", apply_branch).stdout.strip()
    assert apply_worktree.exists()
