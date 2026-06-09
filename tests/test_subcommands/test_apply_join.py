"""サブコマンド横断テストを意味カテゴリ別に分割したファイル。"""

from .helpers import *


def test_apply_join_merges_completed_apply_branch_and_resets_state(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """`cmoc apply join` は apply branch を session branch へ merge する。"""
    repo = _init_repo(tmp_path)
    home_branch = _git(repo, "branch", "--show-current").stdout.strip()
    _checkout_session_branch(repo)
    oracle_snapshot = _add_oracle_snapshot(repo)
    apply_branch, apply_worktree, report_path = _create_completed_apply_run(
        repo,
        oracle_snapshot,
    )
    (apply_worktree / "feature.txt").write_text("implemented\n", encoding="utf-8")
    _git(apply_worktree, "add", "feature.txt")
    _git(apply_worktree, "commit", "-m", "implement feature")

    cmoc_apply_join_impl(repo)

    output = capsys.readouterr().out
    state = json.loads(
        (
            repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_000000123.json"
        ).read_text(encoding="utf-8")
    )
    assert (repo / "feature.txt").read_text(encoding="utf-8") == "implemented\n"
    assert state["apply"] == {
        "apply_branch": None,
        "oracle_snapshot_commit": None,
        "state": "ready",
    }
    assert state["session"]["session_home_branch"] == home_branch
    assert state["session"]["last_joined_apply_oracle_snapshot_commit"] == (
        oracle_snapshot
    )
    assert "last_joined_apply_join_commit" not in state["session"]
    assert "last_joined_apply_result" not in state["session"]
    assert _git(repo, "branch", "--show-current").stdout.strip() == (
        "cmoc/session/2026-05-10_22-21_10_000000123"
    )
    assert _git(repo, "branch", "--list", apply_branch).stdout == ""
    assert not apply_worktree.exists()
    assert report_path.exists()
    assert "joined apply branch:" in output
    assert "warning: apply cleanup skipped:" not in output


def test_apply_join_rejects_cross_session_apply_branch_without_merge(
    tmp_path: Path,
) -> None:
    """apply join は別 session の apply branch を merge しない。"""
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
    (other_apply_worktree / "foreign.txt").write_text(
        "foreign\n",
        encoding="utf-8",
    )
    _git(other_apply_worktree, "add", "foreign.txt")
    _git(other_apply_worktree, "commit", "-m", "foreign implementation")
    state_path = (
        repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_000000123.json"
    )
    state = json.loads(state_path.read_text(encoding="utf-8"))
    state["apply"]["apply_branch"] = other_apply_branch
    state["apply"]["oracle_snapshot_commit"] = oracle_snapshot
    state_path.write_text(json.dumps(state), encoding="utf-8")

    with pytest.raises(CmocError) as error_info:
        cmoc_apply_join_impl(repo)

    assert "同じ session の apply branch" in error_info.value.actions[0]
    assert not (repo / "foreign.txt").exists()
    assert _git(repo, "branch", "--list", other_apply_branch).stdout.strip()
    assert other_apply_worktree.exists()


def test_apply_join_cleans_worktree_created_under_main_repo_root_from_linked(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """linked worktree で fork した apply run は main repo-root 側で cleanup する。"""
    repo = _init_repo(tmp_path)
    (repo / ".gitignore").write_text("/.cmoc/\n", encoding="utf-8")
    _git(repo, "add", ".gitignore")
    _git(repo, "commit", "-m", "ignore cmoc")
    linked = tmp_path / "linked"
    _git(repo, "worktree", "add", "-b", "feature", str(linked), "HEAD")
    cmoc_session_fork_impl(linked)
    session_branch = _git(linked, "branch", "--show-current").stdout.strip()
    session_id = session_branch.removeprefix("cmoc/session/")
    oracle_root = linked / "oracles"
    oracle_root.mkdir()
    (oracle_root / "spec.md").write_text("spec\n", encoding="utf-8")
    _write_flat_oracles_index(oracle_root, "spec.md")
    _git(linked, "add", "oracles/spec.md", "oracles/INDEX.md")
    _git(linked, "commit", "-m", "add oracle")

    monkeypatch.setattr(
        "sub_commands.apply.fork.maintain_indexes",
        lambda repo_root: False,
    )

    def fake_codex(*args: object, **kwargs: object) -> str:
        """調査を要修正点なしとして完了させる。"""
        if kwargs.get("expect_json") is True:
            return '{"git_head_commit_hash": null, "fixing_points": []}'
        return "No changes"

    monkeypatch.setattr("sub_commands.apply.fork.run_codex_exec", fake_codex)

    exit_code = cmoc_apply_impl(linked)

    state_path = repo / ".cmoc" / "sessions" / f"{session_id}.json"
    state = json.loads(state_path.read_text(encoding="utf-8"))
    apply_branch = state["apply"]["apply_branch"]
    oracle_snapshot = state["apply"]["oracle_snapshot_commit"]
    apply_run_id = apply_branch.rsplit("/", 1)[1]
    apply_worktree = repo / ".cmoc" / "worktrees" / session_id / apply_run_id
    linked_apply_worktree = linked / ".cmoc" / "worktrees" / session_id / apply_run_id
    reports = list(
        (repo / ".cmoc" / "reports" / "apply" / "fork").glob("*.md")
    )
    assert exit_code == 0
    assert apply_worktree.is_dir()
    assert not linked_apply_worktree.exists()
    assert len(reports) == 1
    assert f'apply_worktree_path: "{apply_worktree}"' in reports[0].read_text(
        encoding="utf-8"
    )

    _git(linked, "switch", session_branch)
    original_cwd = Path.cwd()
    cmoc_apply_join_impl(linked)

    state = json.loads(state_path.read_text(encoding="utf-8"))
    assert Path.cwd() == original_cwd
    assert state["apply"] == {
        "apply_branch": None,
        "oracle_snapshot_commit": None,
        "state": "ready",
    }
    assert isinstance(state["session"]["session_home_branch"], str)
    assert state["session"]["session_home_branch"]
    assert state["session"]["last_joined_apply_oracle_snapshot_commit"] == (
        oracle_snapshot
    )
    assert "last_joined_apply_join_commit" not in state["session"]
    assert "last_joined_apply_result" not in state["session"]
    assert _git(repo, "branch", "--list", apply_branch).stdout == ""
    assert not apply_worktree.exists()
    assert state_path.exists()


def test_apply_join_keeps_artifacts_when_report_is_missing(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """report 保存済みを確認できない場合、merge 後も apply artifacts は残す。"""
    repo = _init_repo(tmp_path)
    _checkout_session_branch(repo)
    oracle_snapshot = _add_oracle_snapshot(repo)
    apply_branch, apply_worktree, report_path = _create_completed_apply_run(
        repo,
        oracle_snapshot,
    )
    report_path.unlink()
    (apply_worktree / "feature.txt").write_text("implemented\n", encoding="utf-8")
    _git(apply_worktree, "add", "feature.txt")
    _git(apply_worktree, "commit", "-m", "implement feature")

    cmoc_apply_join_impl(repo)

    output = capsys.readouterr().out
    state = json.loads(
        (
            repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_000000123.json"
        ).read_text(encoding="utf-8")
    )
    assert (repo / "feature.txt").read_text(encoding="utf-8") == "implemented\n"
    assert state["apply"]["state"] == "ready"
    assert "last_joined_apply_result" not in state["session"]
    assert apply_branch in _git(repo, "branch", "--list", apply_branch).stdout
    assert apply_worktree.exists()
    assert not report_path.exists()
    assert (
        "warning: apply cleanup skipped: saved apply report was not found for "
        f"{apply_branch}"
    ) in output


def test_apply_join_keeps_artifacts_without_session_result_field(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """session state に join 結果 snapshot が無い場合は artifacts を削除しない。"""
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

    def mark_ready_without_result(
        repo_root: Path,
        session_id: str,
        state: dict[str, object],
        oracle_snapshot_commit: str,
        session_home_branch: str,
    ) -> None:
        session = state["session"]
        assert isinstance(session, dict)
        session["session_home_branch"] = session_home_branch
        session["last_joined_apply_oracle_snapshot_commit"] = None
        state["apply"] = {
            "state": "ready",
            "apply_branch": None,
            "oracle_snapshot_commit": None,
        }
        write_session_state(repo_root, session_id, state)

    monkeypatch.setattr(
        apply_join_module,
        "_mark_apply_ready",
        mark_ready_without_result,
    )

    cmoc_apply_join_impl(repo)

    output = capsys.readouterr().out
    state = json.loads(
        (
            repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_000000123.json"
        ).read_text(encoding="utf-8")
    )
    assert (repo / "feature.txt").read_text(encoding="utf-8") == "implemented\n"
    assert state["apply"]["state"] == "ready"
    assert state["session"]["last_joined_apply_oracle_snapshot_commit"] is None
    assert "last_joined_apply_result" not in state["session"]
    assert apply_branch in _git(repo, "branch", "--list", apply_branch).stdout
    assert apply_worktree.exists()
    assert report_path.exists()
    assert (
        "warning: apply cleanup skipped: session state does not contain saved apply "
        "result metadata"
    ) in output


def test_apply_join_keeps_branch_when_worktree_remove_fails(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """apply worktree 削除に失敗した場合は branch 削除へ進まない。"""
    repo = _init_repo(tmp_path)
    _checkout_session_branch(repo)
    oracle_snapshot = _add_oracle_snapshot(repo)
    apply_branch, apply_worktree, _report_path = _create_completed_apply_run(
        repo,
        oracle_snapshot,
    )
    (apply_worktree / "feature.txt").write_text("implemented\n", encoding="utf-8")
    _git(apply_worktree, "add", "feature.txt")
    _git(apply_worktree, "commit", "-m", "implement feature")
    original_run_git = apply_join_module.run_git
    branch_delete_attempted = False

    def fail_worktree_remove(
        repo_root: Path,
        args: list[str],
        *,
        check: bool = True,
        text: bool = True,
        input_text: str | None = None,
        env: dict[str, str] | None = None,
    ) -> subprocess.CompletedProcess[str]:
        nonlocal branch_delete_attempted
        if args == ["worktree", "remove", str(apply_worktree)]:
            return subprocess.CompletedProcess(
                ["git", *args],
                1,
                "",
                "simulated worktree remove failure",
            )
        if args == ["branch", "-d", apply_branch]:
            branch_delete_attempted = True
        return original_run_git(
            repo_root,
            args,
            check=check,
            text=text,
            input_text=input_text,
            env=env,
        )

    monkeypatch.setattr(apply_join_module, "run_git", fail_worktree_remove)

    cmoc_apply_join_impl(repo)

    output = capsys.readouterr().out
    state = json.loads(
        (
            repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_000000123.json"
        ).read_text(encoding="utf-8")
    )
    assert (repo / "feature.txt").read_text(encoding="utf-8") == "implemented\n"
    assert state["apply"]["state"] == "ready"
    assert apply_branch in _git(repo, "branch", "--list", apply_branch).stdout
    assert apply_worktree.exists()
    assert not branch_delete_attempted
    assert "warning: apply worktree was not deleted:" in output


def test_apply_join_ignores_worktree_local_log_cmoc(
    tmp_path: Path,
) -> None:
    """apply worktree 内のログ用 `.cmoc` ではなく所有元の state を読む。"""
    repo = _init_repo(tmp_path)
    _checkout_session_branch(repo)
    oracle_snapshot = _add_oracle_snapshot(repo)
    apply_branch, apply_worktree, _report_path = _create_completed_apply_run(
        repo,
        oracle_snapshot,
    )
    (apply_worktree / ".cmoc" / "logs" / "sub_commands").mkdir(parents=True)
    (apply_worktree / "feature.txt").write_text("implemented\n", encoding="utf-8")
    _git(apply_worktree, "add", "feature.txt")
    _git(apply_worktree, "commit", "-m", "implement feature")

    cmoc_apply_join_impl(apply_worktree)

    state = json.loads(
        (
            repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_000000123.json"
        ).read_text(encoding="utf-8")
    )
    assert (repo / "feature.txt").read_text(encoding="utf-8") == "implemented\n"
    assert state["apply"]["state"] == "ready"
    assert _git(repo, "branch", "--list", apply_branch).stdout == ""
    assert not apply_worktree.exists()


def test_apply_join_from_apply_branch_rejects_dirty_session_linked_worktree(
    tmp_path: Path,
) -> None:
    """apply branch からの join も実際の session worktree の dirty を拒否する。"""
    repo = _init_repo(tmp_path)
    home_branch = _git(repo, "branch", "--show-current").stdout.strip()
    _checkout_session_branch(repo)
    oracle_snapshot = _add_oracle_snapshot(repo)
    apply_branch, apply_worktree, _report_path = _create_completed_apply_run(
        repo,
        oracle_snapshot,
    )
    session_branch = _git(repo, "branch", "--show-current").stdout.strip()
    _git(repo, "switch", home_branch)
    session_worktree = tmp_path / "session-linked"
    _git(repo, "worktree", "add", str(session_worktree), session_branch)
    (session_worktree / "dirty.txt").write_text("dirty\n", encoding="utf-8")
    (apply_worktree / "feature.txt").write_text("implemented\n", encoding="utf-8")
    _git(apply_worktree, "add", "feature.txt")
    _git(apply_worktree, "commit", "-m", "implement feature")

    with pytest.raises(CmocError) as error_info:
        cmoc_apply_join_impl(apply_worktree)

    state = json.loads(
        (
            repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_000000123.json"
        ).read_text(encoding="utf-8")
    )
    assert "未コミットの変更" in error_info.value.message
    assert str((session_worktree / "dirty.txt").resolve()) in error_info.value.detail
    assert not (session_worktree / "feature.txt").exists()
    assert state["apply"]["state"] == "completed"
    assert _git(repo, "branch", "--list", apply_branch).stdout.strip()
    assert apply_worktree.exists()


def test_apply_join_stops_on_unexpected_diff_in_normal_mode(
    tmp_path: Path,
) -> None:
    """通常モードの apply join は想定外差分を報告して停止する。"""
    repo = _init_repo(tmp_path)
    _checkout_session_branch(repo)
    oracle_snapshot = _add_oracle_snapshot(repo)
    apply_branch, apply_worktree, _report_path = _create_completed_apply_run(
        repo,
        oracle_snapshot,
    )
    (apply_worktree / "oracles" / "spec.md").write_text(
        "unexpected oracle edit\n",
        encoding="utf-8",
    )
    _git(apply_worktree, "add", "oracles/spec.md")
    _git(apply_worktree, "commit", "-m", "edit oracle unexpectedly")

    with pytest.raises(CmocError) as error_info:
        cmoc_apply_join_impl(repo)

    assert "想定外の差分" in error_info.value.message
    assert (
        f"{apply_branch}: {json.dumps((repo / 'oracles/spec.md').resolve().as_posix())}"
        in error_info.value.detail
    )
    state = json.loads(
        (
            repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_000000123.json"
        ).read_text(encoding="utf-8")
    )
    assert state["apply"]["state"] == "completed"
    assert _git(repo, "branch", "--list", apply_branch).stdout.strip()
    assert apply_worktree.exists()


def test_apply_join_stops_on_apply_branch_forbidden_deletion(
    tmp_path: Path,
) -> None:
    """apply branch 側の禁止 path 削除も想定外差分として停止する。"""
    repo = _init_repo(tmp_path)
    _checkout_session_branch(repo)
    oracle_snapshot = _add_oracle_snapshot(repo)
    apply_branch, apply_worktree, _report_path = _create_completed_apply_run(
        repo,
        oracle_snapshot,
    )
    _git(apply_worktree, "rm", "oracles/spec.md")
    _git(apply_worktree, "commit", "-m", "delete oracle unexpectedly")

    with pytest.raises(CmocError) as error_info:
        cmoc_apply_join_impl(repo)

    assert "想定外の差分" in error_info.value.message
    assert (
        f"{apply_branch}: {json.dumps((repo / 'oracles/spec.md').resolve().as_posix())}"
        in error_info.value.detail
    )
    assert (repo / "oracles" / "spec.md").read_text(encoding="utf-8") == "spec\n"
    assert _git(repo, "branch", "--list", apply_branch).stdout.strip()
    assert apply_worktree.exists()


def test_apply_join_stops_on_apply_branch_non_implementation_diff(
    tmp_path: Path,
) -> None:
    """apply branch 側の非実装ファイル変更は想定外差分として停止する。"""
    repo = _init_repo(tmp_path)
    (repo / ".gitignore").write_text("/ignored.txt\n", encoding="utf-8")
    _git(repo, "add", ".gitignore")
    _git(repo, "commit", "-m", "ignore non implementation file")
    _checkout_session_branch(repo)
    oracle_snapshot = _add_oracle_snapshot(repo)
    apply_branch, apply_worktree, _report_path = _create_completed_apply_run(
        repo,
        oracle_snapshot,
    )
    (apply_worktree / "ignored.txt").write_text("ignored\n", encoding="utf-8")
    _git(apply_worktree, "add", "-f", "ignored.txt")
    _git(apply_worktree, "commit", "-m", "edit non implementation file")

    with pytest.raises(CmocError) as error_info:
        cmoc_apply_join_impl(repo)

    assert "想定外の差分" in error_info.value.message
    assert (
        f"{apply_branch}: {json.dumps((repo / 'ignored.txt').resolve().as_posix())}"
        in error_info.value.detail
    )
    assert not (repo / "ignored.txt").exists()
    assert _git(repo, "branch", "--list", apply_branch).stdout.strip()
    assert apply_worktree.exists()


@pytest.mark.parametrize(
    ("relative_path", "content"),
    [
        (".agents/note.txt", "joined agents note\n"),
        (".cmoc/state.json", "{}\n"),
        ("memo/note.md", "joined memo note\n"),
    ],
)
def test_apply_join_stops_on_apply_branch_forbidden_diff(
    tmp_path: Path,
    relative_path: str,
    content: str,
) -> None:
    """apply fork/Codex CLI の禁止 path は apply branch 成果物にしない。"""
    repo = _init_repo(tmp_path)
    _checkout_session_branch(repo)
    oracle_snapshot = _add_oracle_snapshot(repo)
    apply_branch, apply_worktree, _report_path = _create_completed_apply_run(
        repo,
        oracle_snapshot,
    )
    repo_target = repo / relative_path
    before_exists = repo_target.exists()
    before_content = (
        repo_target.read_text(encoding="utf-8") if before_exists else None
    )
    target = apply_worktree / relative_path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")
    _git(apply_worktree, "add", "-f", relative_path)
    _git(apply_worktree, "commit", "-m", "edit forbidden path")

    with pytest.raises(CmocError) as error_info:
        cmoc_apply_join_impl(repo)

    assert "想定外の差分" in error_info.value.message
    assert (
        f"{apply_branch}: {json.dumps((repo / relative_path).resolve().as_posix())}"
        in error_info.value.detail
    )
    assert repo_target.exists() is before_exists
    if before_content is not None:
        assert repo_target.read_text(encoding="utf-8") == before_content
    assert _git(repo, "branch", "--list", apply_branch).stdout.strip()
    assert apply_worktree.exists()


@pytest.mark.parametrize(
    ("relative_path", "content"),
    [
        ("README.md", "joined readme\n"),
        ("AGENTS.md", "joined agents\n"),
    ],
)
def test_apply_join_rejects_root_doc_implementation_diff(
    tmp_path: Path,
    relative_path: str,
    content: str,
) -> None:
    """root の README/AGENTS は apply join の実装差分として取り込まない。"""
    repo = _init_repo(tmp_path)
    _checkout_session_branch(repo)
    oracle_snapshot = _add_oracle_snapshot(repo)
    apply_branch, apply_worktree, _report_path = _create_completed_apply_run(
        repo,
        oracle_snapshot,
    )
    repo_target = repo / relative_path
    before_exists = repo_target.exists()
    before_content = (
        repo_target.read_text(encoding="utf-8") if before_exists else None
    )
    target = apply_worktree / relative_path
    target.write_text(content, encoding="utf-8")
    _git(apply_worktree, "add", relative_path)
    _git(apply_worktree, "commit", "-m", "edit root doc implementation file")

    with pytest.raises(CmocError) as error_info:
        cmoc_apply_join_impl(repo)

    assert "想定外の差分" in error_info.value.message
    assert (
        f"{apply_branch}: {json.dumps((repo / relative_path).resolve().as_posix())}"
        in error_info.value.detail
    )
    assert repo_target.exists() is before_exists
    if before_content is not None:
        assert repo_target.read_text(encoding="utf-8") == before_content


def test_apply_join_reports_unexpected_diff_with_control_chars(
    tmp_path: Path,
) -> None:
    """apply join の想定外差分検査は改行・tab を含む path を壊さない。"""
    repo = _init_repo(tmp_path)
    (repo / ".gitignore").write_text("ignored*\n", encoding="utf-8")
    _git(repo, "add", ".gitignore")
    _git(repo, "commit", "-m", "ignore non implementation files")
    _checkout_session_branch(repo)
    oracle_snapshot = _add_oracle_snapshot(repo)
    apply_branch, apply_worktree, _report_path = _create_completed_apply_run(
        repo,
        oracle_snapshot,
    )
    relative_path = "ignored\nline\tname.md"
    (apply_worktree / relative_path).write_text("note\n", encoding="utf-8")
    _git(apply_worktree, "add", "-f", relative_path)
    _git(apply_worktree, "commit", "-m", "edit odd ignored path")

    with pytest.raises(CmocError) as error_info:
        cmoc_apply_join_impl(repo)

    assert "想定外の差分" in error_info.value.message
    assert (
        f"{apply_branch}: "
        f"{json.dumps((repo / relative_path).resolve().as_posix())}"
        in error_info.value.detail
    )
    assert "\tignored" not in error_info.value.detail
    assert json.dumps((repo / relative_path).resolve().as_posix()) in (
        error_info.value.detail
    )


def test_apply_join_accepts_apply_branch_index_diff(
    tmp_path: Path,
) -> None:
    """apply branch 側の cmoc 管理 INDEX.md 差分は merge 対象にする。"""
    repo = _init_repo(tmp_path)
    _checkout_session_branch(repo)
    oracle_snapshot = _add_oracle_snapshot(repo)
    _apply_branch, apply_worktree, _report_path = _create_completed_apply_run(
        repo,
        oracle_snapshot,
    )
    (apply_worktree / "INDEX.md").write_text("index\n", encoding="utf-8")
    _git(apply_worktree, "add", "INDEX.md")
    _git(apply_worktree, "commit", "-m", "maintain index")

    cmoc_apply_join_impl(repo)

    assert (repo / "INDEX.md").read_text(encoding="utf-8") == "index\n"


def test_apply_join_stops_on_apply_branch_memo_index_diff(
    tmp_path: Path,
) -> None:
    """apply branch 側の root memo/INDEX.md は想定外差分として停止する。"""
    repo = _init_repo(tmp_path)
    _checkout_session_branch(repo)
    oracle_snapshot = _add_oracle_snapshot(repo)
    apply_branch, apply_worktree, _report_path = _create_completed_apply_run(
        repo,
        oracle_snapshot,
    )
    memo_root = apply_worktree / "memo"
    memo_root.mkdir()
    (memo_root / "INDEX.md").write_text("index\n", encoding="utf-8")
    _git(apply_worktree, "add", "memo/INDEX.md")
    _git(apply_worktree, "commit", "-m", "maintain memo index")

    with pytest.raises(CmocError) as error_info:
        cmoc_apply_join_impl(repo)

    assert "想定外の差分" in error_info.value.message
    assert (
        f"{apply_branch}: {json.dumps((repo / 'memo/INDEX.md').resolve().as_posix())}"
        in error_info.value.detail
    )


@pytest.mark.parametrize(
    "relative_path",
    [".cache/INDEX.md", ".cache/nested/INDEX.md"],
)
def test_apply_join_stops_on_apply_branch_unmaintained_index_diff(
    tmp_path: Path,
    relative_path: str,
) -> None:
    """apply branch 側の配置対象外 INDEX.md 差分は想定外として停止する。"""
    repo = _init_repo(tmp_path)
    _checkout_session_branch(repo)
    oracle_snapshot = _add_oracle_snapshot(repo)
    apply_branch, apply_worktree, _report_path = _create_completed_apply_run(
        repo,
        oracle_snapshot,
    )
    index_path = apply_worktree / relative_path
    index_path.parent.mkdir(parents=True)
    index_path.write_text("index\n", encoding="utf-8")
    _git(apply_worktree, "add", "-f", relative_path)
    _git(apply_worktree, "commit", "-m", "maintain untracked index")

    with pytest.raises(CmocError) as error_info:
        cmoc_apply_join_impl(repo)

    assert "想定外の差分" in error_info.value.message
    assert (
        f"{apply_branch}: {json.dumps((repo / relative_path).resolve().as_posix())}"
        in error_info.value.detail
    )
    assert not (repo / relative_path).exists()


def test_apply_join_accepts_apply_branch_oracles_index_diff(
    tmp_path: Path,
) -> None:
    """apply branch 側の oracles/INDEX.md 差分は merge 対象にする。"""
    repo = _init_repo(tmp_path)
    _checkout_session_branch(repo)
    oracle_snapshot = _add_oracle_snapshot(repo)
    _apply_branch, apply_worktree, _report_path = _create_completed_apply_run(
        repo,
        oracle_snapshot,
    )
    (apply_worktree / "oracles" / "INDEX.md").write_text(
        "index\n",
        encoding="utf-8",
    )
    _git(apply_worktree, "add", "oracles/INDEX.md")
    _git(apply_worktree, "commit", "-m", "maintain oracle index")

    cmoc_apply_join_impl(repo)

    assert (repo / "oracles" / "INDEX.md").read_text(encoding="utf-8") == (
        "index\n"
    )


def test_apply_join_accepts_session_branch_oracles_index_diff(
    tmp_path: Path,
) -> None:
    """session branch 側の oracles/INDEX.md 差分は想定内として扱う。"""
    repo = _init_repo(tmp_path)
    _checkout_session_branch(repo)
    oracle_snapshot = _add_oracle_snapshot(repo)
    _apply_branch, apply_worktree, _report_path = _create_completed_apply_run(
        repo,
        oracle_snapshot,
    )
    (apply_worktree / "feature.txt").write_text("implemented\n", encoding="utf-8")
    _git(apply_worktree, "add", "feature.txt")
    _git(apply_worktree, "commit", "-m", "implement feature")
    (repo / "oracles" / "INDEX.md").write_text("index\n", encoding="utf-8")
    _git(repo, "add", "oracles/INDEX.md")
    _git(repo, "commit", "-m", "maintain oracle index on session")

    cmoc_apply_join_impl(repo)

    state = json.loads(
        (
            repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_000000123.json"
        ).read_text(encoding="utf-8")
    )
    assert (repo / "feature.txt").read_text(encoding="utf-8") == "implemented\n"
    assert (repo / "oracles" / "INDEX.md").read_text(encoding="utf-8") == "index\n"
    assert state["apply"]["state"] == "ready"


def test_apply_join_accepts_session_branch_new_oracle_file(
    tmp_path: Path,
) -> None:
    """session branch 側の新規 oracle ファイル追加は想定内として扱う。"""
    repo = _init_repo(tmp_path)
    _checkout_session_branch(repo)
    oracle_snapshot = _add_oracle_snapshot(repo)
    _apply_branch, apply_worktree, _report_path = _create_completed_apply_run(
        repo,
        oracle_snapshot,
    )
    new_oracle = repo / "oracles" / "new_spec.md"
    new_oracle.write_text("new spec\n", encoding="utf-8")
    _git(repo, "add", "oracles/new_spec.md")
    _git(repo, "commit", "-m", "add oracle on session")
    (apply_worktree / "feature.txt").write_text("implemented\n", encoding="utf-8")
    _git(apply_worktree, "add", "feature.txt")
    _git(apply_worktree, "commit", "-m", "implement feature")

    cmoc_apply_join_impl(repo)

    state = json.loads(
        (
            repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_000000123.json"
        ).read_text(encoding="utf-8")
    )
    assert new_oracle.read_text(encoding="utf-8") == "new spec\n"
    assert (repo / "feature.txt").read_text(encoding="utf-8") == "implemented\n"
    assert state["apply"]["state"] == "ready"


def test_apply_join_accepts_session_branch_memo_diff(
    tmp_path: Path,
) -> None:
    """session branch 側の root memo 差分は想定内として扱う。"""
    repo = _init_repo(tmp_path)
    _checkout_session_branch(repo)
    oracle_snapshot = _add_oracle_snapshot(repo)
    _apply_branch, apply_worktree, _report_path = _create_completed_apply_run(
        repo,
        oracle_snapshot,
    )
    memo_root = repo / "memo"
    memo_root.mkdir()
    (memo_root / "note.md").write_text("note\n", encoding="utf-8")
    _git(repo, "add", "memo/note.md")
    _git(repo, "commit", "-m", "edit memo on session")
    (apply_worktree / "feature.txt").write_text("implemented\n", encoding="utf-8")
    _git(apply_worktree, "add", "feature.txt")
    _git(apply_worktree, "commit", "-m", "implement feature")

    cmoc_apply_join_impl(repo)

    state = json.loads(
        (
            repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_000000123.json"
        ).read_text(encoding="utf-8")
    )
    assert (repo / "memo" / "note.md").read_text(encoding="utf-8") == "note\n"
    assert (repo / "feature.txt").read_text(encoding="utf-8") == "implemented\n"
    assert state["apply"]["state"] == "ready"


def test_apply_join_stops_on_session_branch_ignored_oracle_diff(
    tmp_path: Path,
) -> None:
    """session branch 側でも root .gitignore 対象の oracle 配下差分は停止する。"""
    repo = _init_repo(tmp_path)
    (repo / ".gitignore").write_text("oracles/ignored.md\n", encoding="utf-8")
    _git(repo, "add", ".gitignore")
    _git(repo, "commit", "-m", "ignore oracle path")
    _checkout_session_branch(repo)
    oracle_snapshot = _add_oracle_snapshot(repo)
    _apply_branch, _apply_worktree, _report_path = _create_completed_apply_run(
        repo,
        oracle_snapshot,
    )
    session_branch = _git(repo, "branch", "--show-current").stdout.strip()
    (repo / "oracles" / "ignored.md").write_text("ignored\n", encoding="utf-8")
    _git(repo, "add", "-f", "oracles/ignored.md")
    _git(repo, "commit", "-m", "edit ignored oracle path")

    with pytest.raises(CmocError) as error_info:
        cmoc_apply_join_impl(repo)

    assert "想定外の差分" in error_info.value.message
    assert (
        f"{session_branch}: "
        f"{json.dumps((repo / 'oracles/ignored.md').resolve().as_posix())}"
        in error_info.value.detail
    )


def test_apply_join_stops_on_session_branch_implementation_deletion(
    tmp_path: Path,
) -> None:
    """session branch 側の実装ファイル削除も想定外差分として停止する。"""
    repo = _init_repo(tmp_path)
    (repo / "app.py").write_text("print('base')\n", encoding="utf-8")
    _git(repo, "add", "app.py")
    _git(repo, "commit", "-m", "add implementation file")
    _checkout_session_branch(repo)
    oracle_snapshot = _add_oracle_snapshot(repo)
    _apply_branch, _apply_worktree, _report_path = _create_completed_apply_run(
        repo,
        oracle_snapshot,
    )
    session_branch = _git(repo, "branch", "--show-current").stdout.strip()
    _git(repo, "rm", "app.py")
    _git(repo, "commit", "-m", "delete implementation on session")

    with pytest.raises(CmocError) as error_info:
        cmoc_apply_join_impl(repo)

    assert "想定外の差分" in error_info.value.message
    assert (
        f"{session_branch}: {json.dumps((repo / 'app.py').resolve().as_posix())}"
        in error_info.value.detail
    )
    assert not (repo / "app.py").exists()


def test_apply_join_force_resolve_keeps_expected_apply_index_diff(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """強制モードは想定内差分だけを維持し、禁止 path は戻す。"""
    repo = _init_repo(tmp_path)
    _checkout_session_branch(repo)
    oracle_snapshot = _add_oracle_snapshot(repo)
    apply_branch, apply_worktree, _report_path = _create_completed_apply_run(
        repo,
        oracle_snapshot,
    )
    (apply_worktree / "feature.txt").write_text("implemented\n", encoding="utf-8")
    (apply_worktree / "INDEX.md").write_text("index\n", encoding="utf-8")
    memo_root = apply_worktree / "memo"
    memo_root.mkdir()
    (memo_root / "note.md").write_text("note\n", encoding="utf-8")
    _git(apply_worktree, "add", "feature.txt", "INDEX.md", "memo/note.md")
    _git(apply_worktree, "commit", "-m", "implement with index and memo")

    cmoc_apply_join_impl(repo, force_resolve=True)

    output = capsys.readouterr().out
    state = json.loads(
        (
            repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_000000123.json"
        ).read_text(encoding="utf-8")
    )
    assert (repo / "feature.txt").read_text(encoding="utf-8") == "implemented\n"
    assert (repo / "INDEX.md").read_text(encoding="utf-8") == "index\n"
    assert not (repo / "memo" / "note.md").exists()
    assert state["apply"]["state"] == "ready"
    assert (
        f"- {apply_branch}: {json.dumps((repo / 'memo/note.md').resolve().as_posix())}"
        in output
    )


def test_apply_join_force_resolve_keeps_session_branch_new_oracle_file(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """強制モードも session branch 側の新規 oracle ファイル追加を戻さない。"""
    repo = _init_repo(tmp_path)
    _checkout_session_branch(repo)
    oracle_snapshot = _add_oracle_snapshot(repo)
    apply_branch, apply_worktree, _report_path = _create_completed_apply_run(
        repo,
        oracle_snapshot,
    )
    new_oracle = repo / "oracles" / "new_spec.md"
    new_oracle.write_text("new spec\n", encoding="utf-8")
    (repo / "unexpected.txt").write_text("unexpected\n", encoding="utf-8")
    _git(repo, "add", "oracles/new_spec.md", "unexpected.txt")
    _git(repo, "commit", "-m", "edit session during apply")
    (apply_worktree / "feature.txt").write_text("implemented\n", encoding="utf-8")
    _git(apply_worktree, "add", "feature.txt")
    _git(apply_worktree, "commit", "-m", "implement feature")

    cmoc_apply_join_impl(repo, force_resolve=True)

    output = capsys.readouterr().out
    state = json.loads(
        (
            repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_000000123.json"
        ).read_text(encoding="utf-8")
    )
    assert new_oracle.read_text(encoding="utf-8") == "new spec\n"
    assert (repo / "feature.txt").read_text(encoding="utf-8") == "implemented\n"
    assert not (repo / "unexpected.txt").exists()
    assert state["apply"]["state"] == "ready"
    assert (
        f"- {apply_branch}: "
        f"{json.dumps((repo / 'feature.txt').resolve().as_posix())}"
        not in output
    )
    assert (
        "- cmoc/session/2026-05-10_22-21_10_000000123: "
        f"{json.dumps((repo / 'unexpected.txt').resolve().as_posix())}"
        in output
    )
    assert "oracles/new_spec.md" not in output


def test_apply_join_force_resolves_apply_branch_forbidden_deletion(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """強制モードは apply branch 側の禁止 path 削除を snapshot から復元する。"""
    repo = _init_repo(tmp_path)
    _checkout_session_branch(repo)
    oracle_snapshot = _add_oracle_snapshot(repo)
    apply_branch, apply_worktree, _report_path = _create_completed_apply_run(
        repo,
        oracle_snapshot,
    )
    (apply_worktree / "feature.txt").write_text("implemented\n", encoding="utf-8")
    _git(apply_worktree, "add", "feature.txt")
    _git(apply_worktree, "rm", "oracles/spec.md")
    _git(apply_worktree, "commit", "-m", "implement and delete oracle")

    cmoc_apply_join_impl(repo, force_resolve=True)

    output = capsys.readouterr().out
    state = json.loads(
        (
            repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_000000123.json"
        ).read_text(encoding="utf-8")
    )
    assert (repo / "feature.txt").read_text(encoding="utf-8") == "implemented\n"
    assert (repo / "oracles" / "spec.md").read_text(encoding="utf-8") == "spec\n"
    assert state["apply"]["state"] == "ready"
    assert (
        f"- {apply_branch}: {json.dumps((repo / 'oracles/spec.md').resolve().as_posix())}"
        in output
    )


def test_apply_join_force_resolves_session_branch_implementation_deletion(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """強制モードは session branch 側の実装ファイル削除を snapshot から復元する。"""
    repo = _init_repo(tmp_path)
    (repo / "app.py").write_text("print('base')\n", encoding="utf-8")
    _git(repo, "add", "app.py")
    _git(repo, "commit", "-m", "add implementation file")
    _checkout_session_branch(repo)
    oracle_snapshot = _add_oracle_snapshot(repo)
    _apply_branch, apply_worktree, _report_path = _create_completed_apply_run(
        repo,
        oracle_snapshot,
    )
    session_branch = _git(repo, "branch", "--show-current").stdout.strip()
    _git(repo, "rm", "app.py")
    _git(repo, "commit", "-m", "delete implementation on session")
    (apply_worktree / "feature.txt").write_text("implemented\n", encoding="utf-8")
    _git(apply_worktree, "add", "feature.txt")
    _git(apply_worktree, "commit", "-m", "implement feature")

    cmoc_apply_join_impl(repo, force_resolve=True)

    output = capsys.readouterr().out
    state = json.loads(
        (
            repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_000000123.json"
        ).read_text(encoding="utf-8")
    )
    assert (repo / "app.py").read_text(encoding="utf-8") == "print('base')\n"
    assert (repo / "feature.txt").read_text(encoding="utf-8") == "implemented\n"
    assert state["apply"]["state"] == "ready"
    assert (
        f"- {session_branch}: {json.dumps((repo / 'app.py').resolve().as_posix())}"
        in output
    )


def test_apply_join_force_resolves_session_linked_worktree_from_apply_branch(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """apply branch からの強制 join は session linked worktree で revert する。"""
    repo = _init_repo(tmp_path)
    home_branch = _git(repo, "branch", "--show-current").stdout.strip()
    (repo / "app.py").write_text("print('base')\n", encoding="utf-8")
    _git(repo, "add", "app.py")
    _git(repo, "commit", "-m", "add implementation file")
    _checkout_session_branch(repo)
    oracle_snapshot = _add_oracle_snapshot(repo)
    apply_branch, apply_worktree, _report_path = _create_completed_apply_run(
        repo,
        oracle_snapshot,
    )
    session_branch = _git(repo, "branch", "--show-current").stdout.strip()
    _git(repo, "switch", home_branch)
    session_worktree = tmp_path / "session-linked"
    _git(repo, "worktree", "add", str(session_worktree), session_branch)
    _git(session_worktree, "rm", "app.py")
    _git(session_worktree, "commit", "-m", "delete implementation on session")
    (apply_worktree / "feature.txt").write_text("implemented\n", encoding="utf-8")
    _git(apply_worktree, "add", "feature.txt")
    _git(apply_worktree, "commit", "-m", "implement feature")

    cmoc_apply_join_impl(apply_worktree, force_resolve=True)

    output = capsys.readouterr().out
    state = json.loads(
        (
            repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_000000123.json"
        ).read_text(encoding="utf-8")
    )
    assert (session_worktree / "app.py").read_text(encoding="utf-8") == (
        "print('base')\n"
    )
    assert (session_worktree / "feature.txt").read_text(encoding="utf-8") == (
        "implemented\n"
    )
    assert state["apply"]["state"] == "ready"
    assert _git(repo, "branch", "--list", apply_branch).stdout == ""
    assert not apply_worktree.exists()
    assert (
        f"- {session_branch}: {json.dumps((repo / 'app.py').resolve().as_posix())}"
        in output
    )


def test_apply_join_auto_resolves_index_conflict(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """INDEX.md だけの merge conflict は削除で自動解決する。"""
    repo = _init_repo(tmp_path)
    _checkout_session_branch(repo)
    oracle_snapshot = _add_oracle_snapshot(repo)
    apply_branch, apply_worktree, _report_path = _create_completed_apply_run(
        repo,
        oracle_snapshot,
    )
    (repo / "INDEX.md").write_text("session index\n", encoding="utf-8")
    _git(repo, "add", "INDEX.md")
    _git(repo, "commit", "-m", "maintain session index")
    (apply_worktree / "INDEX.md").write_text("apply index\n", encoding="utf-8")
    _git(apply_worktree, "add", "INDEX.md")
    _git(apply_worktree, "commit", "-m", "maintain apply index")

    cmoc_apply_join_impl(repo)

    output = capsys.readouterr().out
    state = json.loads(
        (
            repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_000000123.json"
        ).read_text(encoding="utf-8")
    )
    assert not (repo / "INDEX.md").exists()
    assert state["apply"]["state"] == "ready"
    assert _git(repo, "branch", "--list", apply_branch).stdout == ""
    assert "auto-resolved INDEX.md conflicts:" in output
    assert f"- {json.dumps((repo / 'INDEX.md').resolve().as_posix())}" in output
    assert "warning: apply cleanup skipped:" not in output


def test_apply_join_unmerged_paths_are_nul_safe(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """unmerged path 取得は改行・tab を含む path を token のまま返す。"""
    repo = _init_repo(tmp_path)
    calls: list[list[str]] = []

    def fake_run_git(
        _repo_root: Path,
        args: list[str],
        *,
        check: bool = True,
        text: bool = True,
        input_text: str | None = None,
        env: dict[str, str] | None = None,
    ) -> subprocess.CompletedProcess[str]:
        del check, text, input_text, env
        calls.append(args)
        return subprocess.CompletedProcess(
            ["git", *args],
            0,
            "dir/a\nb/INDEX.md\0feature\tfile.txt\0",
            "",
        )

    monkeypatch.setattr(apply_join_module, "run_git", fake_run_git)

    assert apply_join_module._unmerged_paths(repo) == [
        "dir/a\nb/INDEX.md",
        "feature\tfile.txt",
    ]
    assert calls == [["diff", "--name-only", "-z", "--diff-filter=U"]]


def test_apply_join_changed_entries_use_destination_paths_and_include_deletes(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """想定外差分判定の path は共通定義に従って正規化する。"""
    repo = _init_repo(tmp_path)
    calls: list[list[str]] = []

    def fake_run_git(
        _repo_root: Path,
        args: list[str],
        *,
        check: bool = True,
        text: bool = True,
        input_text: str | None = None,
        env: dict[str, str] | None = None,
    ) -> subprocess.CompletedProcess[str]:
        del check, text, input_text, env
        calls.append(args)
        return subprocess.CompletedProcess(
            ["git", *args],
            0,
            (
                "R100\0oracles/spec.md\0feature.txt\0"
                "C100\0src/source.py\0src/copied.py\0"
                "D\0deleted.txt\0"
                "M\0modified.txt\0"
            ),
            "",
        )

    monkeypatch.setattr(apply_join_module, "run_git", fake_run_git)

    entries = apply_join_module._changed_path_entries_between(
        repo,
        "base-commit",
        "branch-name",
    )

    assert [entry.paths for entry in entries] == [
        ["feature.txt"],
        ["src/copied.py"],
        ["deleted.txt"],
        ["modified.txt"],
    ]
    assert calls == [
        [
            "diff",
            "--name-status",
            "-z",
            "-M",
            "-C",
            "--find-copies-harder",
            "base-commit..branch-name",
            "--",
        ]
    ]


def test_apply_join_resolves_index_conflict_before_reporting_other_conflict(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """混在 conflict では INDEX.md だけ自動解決し、他 path は報告する。"""
    repo = _init_repo(tmp_path)
    _checkout_session_branch(repo)
    oracle_snapshot = _add_oracle_snapshot(repo)
    apply_branch, apply_worktree, _report_path = _create_completed_apply_run(
        repo,
        oracle_snapshot,
    )
    (apply_worktree / "feature.txt").write_text("implemented\n", encoding="utf-8")
    (apply_worktree / "INDEX.md").write_text("apply index\n", encoding="utf-8")
    _git(apply_worktree, "add", "feature.txt", "INDEX.md")
    _git(apply_worktree, "commit", "-m", "implement feature with index")
    original_run_git = apply_join_module.run_git
    removed_index = False

    def fail_merge_with_mixed_conflicts(
        repo_root: Path,
        args: list[str],
        *,
        check: bool = True,
        text: bool = True,
        input_text: str | None = None,
        env: dict[str, str] | None = None,
    ) -> subprocess.CompletedProcess[str]:
        nonlocal removed_index
        if args == ["merge", "--no-ff", apply_branch]:
            return subprocess.CompletedProcess(
                ["git", *args],
                1,
                "",
                "\n".join(
                    [
                        "CONFLICT (content): Merge conflict in INDEX.md",
                        "CONFLICT (content): Merge conflict in feature.txt",
                    ]
                ),
            )
        if args == ["rm", "--ignore-unmatch", "--", "INDEX.md"]:
            removed_index = True
            return subprocess.CompletedProcess(["git", *args], 0, "", "")
        if args == ["commit", "--no-edit"]:
            pytest.fail("non INDEX.md conflict が残る場合は merge commit しない")
        return original_run_git(
            repo_root,
            args,
            check=check,
            text=text,
            input_text=input_text,
            env=env,
        )

    def mixed_unmerged_paths(_repo: Path) -> list[str]:
        if removed_index:
            return ["feature.txt"]
        return ["INDEX.md", "feature.txt"]

    monkeypatch.setattr(apply_join_module, "run_git", fail_merge_with_mixed_conflicts)
    monkeypatch.setattr(apply_join_module, "_unmerged_paths", mixed_unmerged_paths)

    with pytest.raises(CmocError) as error_info:
        cmoc_apply_join_impl(repo)

    state = json.loads(
        (
            repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_000000123.json"
        ).read_text(encoding="utf-8")
    )
    assert removed_index
    assert json.dumps((repo / "feature.txt").resolve().as_posix()) in (
        error_info.value.detail
    )
    assert json.dumps((repo / "INDEX.md").resolve().as_posix()) not in (
        error_info.value.detail
    )
    assert state["apply"]["state"] == "completed"
    assert _git(repo, "branch", "--list", apply_branch).stdout.strip()
    assert apply_worktree.exists()


def test_apply_join_stops_on_non_index_conflict(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """INDEX.md 以外の conflict は自動解決せず state を維持する。"""
    repo = _init_repo(tmp_path)
    _checkout_session_branch(repo)
    oracle_snapshot = _add_oracle_snapshot(repo)
    apply_branch, apply_worktree, _report_path = _create_completed_apply_run(
        repo,
        oracle_snapshot,
    )
    (apply_worktree / "feature.txt").write_text("implemented\n", encoding="utf-8")
    _git(apply_worktree, "add", "feature.txt")
    _git(apply_worktree, "commit", "-m", "implement feature")
    original_run_git = apply_join_module.run_git

    def fail_merge_with_feature_conflict(
        repo_root: Path,
        args: list[str],
        *,
        check: bool = True,
        text: bool = True,
        input_text: str | None = None,
        env: dict[str, str] | None = None,
    ) -> subprocess.CompletedProcess[str]:
        if args == ["merge", "--no-ff", apply_branch]:
            return subprocess.CompletedProcess(
                ["git", *args],
                1,
                "",
                "CONFLICT (content): Merge conflict in feature.txt",
            )
        return original_run_git(
            repo_root,
            args,
            check=check,
            text=text,
            input_text=input_text,
            env=env,
        )

    monkeypatch.setattr(apply_join_module, "run_git", fail_merge_with_feature_conflict)
    monkeypatch.setattr(
        apply_join_module,
        "_unmerged_paths",
        lambda _repo: ["feature.txt"],
    )

    with pytest.raises(CmocError) as error_info:
        cmoc_apply_join_impl(repo)

    state = json.loads(
        (
            repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_000000123.json"
        ).read_text(encoding="utf-8")
    )
    assert "conflict" in error_info.value.message
    assert json.dumps((repo / "feature.txt").resolve().as_posix()) in (
        error_info.value.detail
    )
    assert state["apply"]["state"] == "completed"
    assert _git(repo, "branch", "--list", apply_branch).stdout.strip()
    assert apply_worktree.exists()


def test_apply_join_allows_apply_branch_rename_from_oracle_to_implementation(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """apply branch 側の rename は rename 後 path 基準で判定する。"""
    repo = _init_repo(tmp_path)
    _checkout_session_branch(repo)
    oracle_snapshot = _add_oracle_snapshot(repo)
    apply_branch, apply_worktree, _report_path = _create_completed_apply_run(
        repo,
        oracle_snapshot,
    )
    _git(apply_worktree, "mv", "oracles/spec.md", "feature.txt")
    _git(apply_worktree, "commit", "-m", "rename oracle to implementation")

    cmoc_apply_join_impl(repo)

    output = capsys.readouterr().out
    state = json.loads(
        (
            repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_000000123.json"
        ).read_text(encoding="utf-8")
    )
    assert (repo / "feature.txt").read_text(encoding="utf-8") == "spec\n"
    assert not (repo / "oracles" / "spec.md").exists()
    assert state["apply"]["state"] == "ready"
    assert "想定外の差分" not in output
    assert "force-resolved unexpected diffs:" not in output
    assert _git(repo, "branch", "--list", apply_branch).stdout == ""


def test_apply_join_force_resolves_apply_branch_non_implementation_diff(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """強制モードは apply branch 側の非実装ファイル変更を revert して merge する。"""
    repo = _init_repo(tmp_path)
    (repo / ".gitignore").write_text("/ignored.txt\n", encoding="utf-8")
    _git(repo, "add", ".gitignore")
    _git(repo, "commit", "-m", "ignore non implementation file")
    _checkout_session_branch(repo)
    oracle_snapshot = _add_oracle_snapshot(repo)
    apply_branch, apply_worktree, _report_path = _create_completed_apply_run(
        repo,
        oracle_snapshot,
    )
    (apply_worktree / "ignored.txt").write_text("ignored\n", encoding="utf-8")
    (apply_worktree / "feature.txt").write_text("implemented\n", encoding="utf-8")
    _git(apply_worktree, "add", "-f", "ignored.txt", "feature.txt")
    _git(apply_worktree, "commit", "-m", "implement with unexpected ignored file")

    cmoc_apply_join_impl(repo, force_resolve=True)

    output = capsys.readouterr().out
    state = json.loads(
        (
            repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_000000123.json"
        ).read_text(encoding="utf-8")
    )
    assert (repo / "feature.txt").read_text(encoding="utf-8") == "implemented\n"
    assert not (repo / "ignored.txt").exists()
    assert state["apply"]["state"] == "ready"
    assert (
        f"- {apply_branch}: {json.dumps((repo / 'ignored.txt').resolve().as_posix())}"
        in output
    )


def test_apply_join_force_resolve_uses_snapshot_gitignore_for_apply_paths(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """session 側の後続 .gitignore 変更で apply 成果物を誤って戻さない。"""
    repo = _init_repo(tmp_path)
    _checkout_session_branch(repo)
    oracle_snapshot = _add_oracle_snapshot(repo)
    apply_branch, apply_worktree, _report_path = _create_completed_apply_run(
        repo,
        oracle_snapshot,
    )
    (apply_worktree / "feature.txt").write_text("implemented\n", encoding="utf-8")
    _git(apply_worktree, "add", "feature.txt")
    _git(apply_worktree, "commit", "-m", "implement feature")
    (repo / ".gitignore").write_text("/feature.txt\n", encoding="utf-8")
    _git(repo, "add", ".gitignore")
    _git(repo, "commit", "-m", "ignore feature on session")

    cmoc_apply_join_impl(repo, force_resolve=True)

    output = capsys.readouterr().out
    state = json.loads(
        (
            repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_000000123.json"
        ).read_text(encoding="utf-8")
    )
    assert (repo / "feature.txt").read_text(encoding="utf-8") == "implemented\n"
    assert not (repo / ".gitignore").exists()
    assert state["apply"]["state"] == "ready"
    assert (
        f"- {apply_branch}: "
        f"{json.dumps((repo / 'feature.txt').resolve().as_posix())}"
        not in output
    )
    assert (
        "- cmoc/session/2026-05-10_22-21_10_000000123: "
        f"{json.dumps((repo / '.gitignore').resolve().as_posix())}"
        in output
    )


def test_apply_join_force_resolve_uses_snapshot_gitignore_for_apply_indexes(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """session 側の後続 .gitignore 変更で apply 側 INDEX.md を誤って戻さない。"""
    repo = _init_repo(tmp_path)
    _checkout_session_branch(repo)
    _add_oracle_snapshot(repo)
    docs = repo / "docs"
    docs.mkdir()
    (docs / "source.txt").write_text("source\n", encoding="utf-8")
    _git(repo, "add", "docs/source.txt")
    _git(repo, "commit", "-m", "add indexed directory")
    oracle_snapshot = _git(repo, "rev-parse", "HEAD").stdout.strip()
    apply_branch, apply_worktree, _report_path = _create_completed_apply_run(
        repo,
        oracle_snapshot,
    )
    apply_docs = apply_worktree / "docs"
    (apply_docs / "INDEX.md").write_text("apply index\n", encoding="utf-8")
    _git(apply_worktree, "add", "docs/INDEX.md")
    _git(apply_worktree, "commit", "-m", "maintain docs index")
    (repo / ".gitignore").write_text("/docs/\n", encoding="utf-8")
    _git(repo, "add", ".gitignore")
    _git(repo, "commit", "-m", "ignore docs on session")

    cmoc_apply_join_impl(repo, force_resolve=True)

    output = capsys.readouterr().out
    state = json.loads(
        (
            repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_000000123.json"
        ).read_text(encoding="utf-8")
    )
    assert (repo / "docs" / "INDEX.md").read_text(encoding="utf-8") == (
        "apply index\n"
    )
    assert not (repo / ".gitignore").exists()
    assert state["apply"]["state"] == "ready"
    assert (
        f"- {apply_branch}: "
        f"{json.dumps((repo / 'docs' / 'INDEX.md').resolve().as_posix())}"
        not in output
    )
    assert (
        "- cmoc/session/2026-05-10_22-21_10_000000123: "
        f"{json.dumps((repo / '.gitignore').resolve().as_posix())}"
        in output
    )


def test_apply_join_force_resolve_uses_snapshot_gitignore_for_session_oracles(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """session 側の後続 .gitignore 変更で oracle ファイル変更を戻さない。"""
    repo = _init_repo(tmp_path)
    _checkout_session_branch(repo)
    oracle_snapshot = _add_oracle_snapshot(repo)
    apply_branch, apply_worktree, _report_path = _create_completed_apply_run(
        repo,
        oracle_snapshot,
    )
    (apply_worktree / "feature.txt").write_text("implemented\n", encoding="utf-8")
    _git(apply_worktree, "add", "feature.txt")
    _git(apply_worktree, "commit", "-m", "implement feature")
    new_oracle = repo / "oracles" / "new_spec.md"
    new_oracle.write_text("new spec\n", encoding="utf-8")
    _git(repo, "add", "oracles/new_spec.md")
    (repo / ".gitignore").write_text("/oracles/new_spec.md\n", encoding="utf-8")
    _git(repo, "add", ".gitignore")
    _git(repo, "commit", "-m", "edit session oracle and gitignore")

    cmoc_apply_join_impl(repo, force_resolve=True)

    output = capsys.readouterr().out
    state = json.loads(
        (
            repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_000000123.json"
        ).read_text(encoding="utf-8")
    )
    assert (repo / "feature.txt").read_text(encoding="utf-8") == "implemented\n"
    assert new_oracle.read_text(encoding="utf-8") == "new spec\n"
    assert not (repo / ".gitignore").exists()
    assert state["apply"]["state"] == "ready"
    assert (
        "- cmoc/session/2026-05-10_22-21_10_000000123: "
        f"{json.dumps((repo / 'oracles' / 'new_spec.md').resolve().as_posix())}"
        not in output
    )
    assert (
        "- cmoc/session/2026-05-10_22-21_10_000000123: "
        f"{json.dumps((repo / '.gitignore').resolve().as_posix())}"
        in output
    )
    assert (
        f"- {apply_branch}: "
        f"{json.dumps((repo / 'feature.txt').resolve().as_posix())}"
        not in output
    )


def test_apply_join_force_resolves_apply_branch_rename_from_oracle(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """強制モードでも rename source は想定外差分として戻さない。"""
    repo = _init_repo(tmp_path)
    _checkout_session_branch(repo)
    oracle_snapshot = _add_oracle_snapshot(repo)
    apply_branch, apply_worktree, _report_path = _create_completed_apply_run(
        repo,
        oracle_snapshot,
    )
    (apply_worktree / "other.txt").write_text("implemented\n", encoding="utf-8")
    _git(apply_worktree, "add", "other.txt")
    _git(apply_worktree, "commit", "-m", "implement other feature")
    _git(apply_worktree, "mv", "oracles/spec.md", "feature.txt")
    _git(apply_worktree, "commit", "-m", "rename oracle to implementation")

    cmoc_apply_join_impl(repo, force_resolve=True)

    output = capsys.readouterr().out
    state = json.loads(
        (
            repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_000000123.json"
        ).read_text(encoding="utf-8")
    )
    assert (repo / "other.txt").read_text(encoding="utf-8") == "implemented\n"
    assert (repo / "feature.txt").read_text(encoding="utf-8") == "spec\n"
    assert not (repo / "oracles" / "spec.md").exists()
    assert state["apply"]["state"] == "ready"
    assert (
        f"- {apply_branch}: "
        f"{json.dumps((repo / 'oracles/spec.md').resolve().as_posix())}"
        not in output
    )
    assert "force-resolved unexpected diffs:" not in output


def test_apply_join_force_resolves_with_missing_apply_worktree(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """強制モードは apply worktree 欠落時も一時 worktree で revert する。"""
    repo = _init_repo(tmp_path)
    (repo / ".gitignore").write_text("/ignored.txt\n", encoding="utf-8")
    _git(repo, "add", ".gitignore")
    _git(repo, "commit", "-m", "ignore non implementation file")
    _checkout_session_branch(repo)
    oracle_snapshot = _add_oracle_snapshot(repo)
    apply_branch, apply_worktree, _report_path = _create_completed_apply_run(
        repo,
        oracle_snapshot,
    )
    (apply_worktree / "ignored.txt").write_text("ignored\n", encoding="utf-8")
    (apply_worktree / "feature.txt").write_text("implemented\n", encoding="utf-8")
    _git(apply_worktree, "add", "-f", "ignored.txt", "feature.txt")
    _git(apply_worktree, "commit", "-m", "implement with unexpected ignored file")
    _git(repo, "worktree", "remove", "--force", str(apply_worktree))

    cmoc_apply_join_impl(repo, force_resolve=True)

    output = capsys.readouterr().out
    state = json.loads(
        (
            repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_000000123.json"
        ).read_text(encoding="utf-8")
    )
    assert (repo / "feature.txt").read_text(encoding="utf-8") == "implemented\n"
    assert not (repo / "ignored.txt").exists()
    assert state["apply"]["state"] == "ready"
    assert _git(repo, "branch", "--list", apply_branch).stdout == ""
    assert not apply_worktree.exists()
    assert list((repo / ".cmoc" / "worktrees" / "tmp").glob("*")) == []
    assert (
        f"- {apply_branch}: {json.dumps((repo / 'ignored.txt').resolve().as_posix())}"
        in output
    )


def test_apply_join_force_resolves_from_apply_branch_without_apply_worktree(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """強制モードは現在の apply branch worktree で想定外差分を revert する。"""
    repo = _init_repo(tmp_path)
    (repo / ".gitignore").write_text("/ignored.txt\n", encoding="utf-8")
    _git(repo, "add", ".gitignore")
    _git(repo, "commit", "-m", "ignore non implementation file")
    _checkout_session_branch(repo)
    oracle_snapshot = _add_oracle_snapshot(repo)
    apply_branch, apply_worktree, _report_path = _create_completed_apply_run(
        repo,
        oracle_snapshot,
    )
    (apply_worktree / "ignored.txt").write_text("ignored\n", encoding="utf-8")
    (apply_worktree / "feature.txt").write_text("implemented\n", encoding="utf-8")
    _git(apply_worktree, "add", "-f", "ignored.txt", "feature.txt")
    _git(apply_worktree, "commit", "-m", "implement with unexpected ignored file")
    _git(repo, "worktree", "remove", "--force", str(apply_worktree))
    _git(repo, "switch", apply_branch)

    cmoc_apply_join_impl(repo, force_resolve=True)

    output = capsys.readouterr().out
    state = json.loads(
        (
            repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_000000123.json"
        ).read_text(encoding="utf-8")
    )
    assert _git(repo, "branch", "--show-current").stdout.strip() == (
        "cmoc/session/2026-05-10_22-21_10_000000123"
    )
    assert (repo / "feature.txt").read_text(encoding="utf-8") == "implemented\n"
    assert not (repo / "ignored.txt").exists()
    assert state["apply"]["state"] == "ready"
    assert _git(repo, "branch", "--list", apply_branch).stdout == ""
    assert not apply_worktree.exists()
    assert not (repo / ".cmoc" / "worktrees" / "tmp").exists()
    assert (
        f"- {apply_branch}: {json.dumps((repo / 'ignored.txt').resolve().as_posix())}"
        in output
    )


def test_apply_join_accepts_apply_branch_copy_to_expected_path(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """apply branch 側の copy は変更後 path を想定外差分検査に使う。"""
    repo = _init_repo(tmp_path)
    _checkout_session_branch(repo)
    oracle_snapshot = _add_oracle_snapshot(repo)
    _apply_branch, apply_worktree, _report_path = _create_completed_apply_run(
        repo,
        oracle_snapshot,
    )
    (apply_worktree / "feature.txt").write_text("spec\n", encoding="utf-8")
    _git(apply_worktree, "add", "feature.txt")
    _git(apply_worktree, "commit", "-m", "copy oracle to implementation")

    cmoc_apply_join_impl(repo, force_resolve=True)

    output = capsys.readouterr().out
    state = json.loads(
        (
            repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_000000123.json"
        ).read_text(encoding="utf-8")
    )
    assert (repo / "feature.txt").read_text(encoding="utf-8") == "spec\n"
    assert (repo / "oracles" / "spec.md").read_text(encoding="utf-8") == "spec\n"
    assert state["apply"]["state"] == "ready"
    assert "force-resolved unexpected diffs:" not in output
