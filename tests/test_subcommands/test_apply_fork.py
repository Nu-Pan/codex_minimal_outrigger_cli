"""サブコマンド横断テストを意味カテゴリ別に分割したファイル。"""

from .helpers import *


def test_apply_returns_complete_when_no_discrepancies(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """`cmoc apply` は不整合なし JSON で完了扱いのレポートを保存する。"""
    repo = _init_repo(tmp_path)
    _checkout_session_branch(repo)
    (repo / ".gitignore").write_text("/.cmoc/\n", encoding="utf-8")
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    (oracle_root / "spec.md").write_text("spec\n", encoding="utf-8")
    _write_flat_oracles_index(oracle_root, "spec.md")
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "oracle")
    session_head = _git(repo, "rev-parse", "HEAD").stdout.strip()

    monkeypatch.setattr(
        "sub_commands.apply.fork.maintain_indexes",
        lambda repo_root: False,
    )
    codex_kwargs: list[dict[str, object]] = []
    codex_prompts: list[str] = []
    event_order: list[str] = []
    original_mark_apply_completed = apply_module._mark_apply_completed
    original_write_apply_report = apply_module._write_apply_report

    def record_mark_apply_completed(*args: object, **kwargs: object) -> None:
        event_order.append("apply 完了記録")
        original_mark_apply_completed(*args, **kwargs)

    def record_write_apply_report(*args: object, **kwargs: object) -> Path:
        event_order.append("report 書き込み")
        return original_write_apply_report(*args, **kwargs)

    monkeypatch.setattr(
        apply_module,
        "_mark_apply_completed",
        record_mark_apply_completed,
    )
    monkeypatch.setattr(
        apply_module,
        "_write_apply_report",
        record_write_apply_report,
    )

    def fake_codex(*args: object, **kwargs: object) -> str:
        """調査なら不整合なし JSON、変更要約なら summary JSON を返す。"""
        codex_kwargs.append(kwargs)
        codex_prompts.append(str(args[1]))
        if kwargs.get("purpose") == "apply 変更要約":
            return _change_summary_json()
        if kwargs.get("expect_json") is True:
            return '{"git_head_commit_hash": null, "fixing_points": []}'
        return _apply_report(str(args[1]), "収束", [0])

    monkeypatch.setattr("sub_commands.apply.fork.run_codex_exec", fake_codex)

    exit_code = cmoc_apply_impl(repo)

    reports = list(
        (repo / ".cmoc" / "reports" / "apply" / "fork").glob("*.md")
    )
    state = json.loads(
        (
            repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_000000123.json"
        ).read_text(encoding="utf-8")
    )
    assert exit_code == 0
    assert len(reports) == 1
    assert state["apply"]["state"] == "completed"
    assert event_order == ["apply 完了記録", "report 書き込み"]
    assert state["apply"]["apply_branch"].startswith(
        "cmoc/apply/2026-05-10_22-21_10_000000123/"
    )
    assert state["apply"]["oracle_snapshot_commit"] == _git(
        repo,
        "rev-parse",
        "HEAD",
    ).stdout.strip()
    apply_run_id = state["apply"]["apply_branch"].rsplit("/", 1)[1]
    apply_worktree = (
        repo
        / ".cmoc"
        / "worktrees"
        / "2026-05-10_22-21_10_000000123"
        / apply_run_id
    )
    assert apply_worktree.is_dir()
    assert set(state["apply"]) == {
        "state",
        "apply_branch",
        "oracle_snapshot_commit",
    }
    assert _git(repo, "branch", "--show-current").stdout.strip() == (
        "cmoc/session/2026-05-10_22-21_10_000000123"
    )
    report_text = reports[0].read_text(encoding="utf-8")
    assert report_text.startswith("---\n")
    session_fork_commit = state["session"]["session_start_commit"]
    assert "cmoc_session_id: \"2026-05-10_22-21_10_000000123\"" in report_text
    assert "cmoc_apply_run_id: " in report_text
    assert (
        "cmoc_session_branch: \"cmoc/session/2026-05-10_22-21_10_000000123\""
        in report_text
    )
    assert (
        f"cmoc_session_fork_commit: \"{session_fork_commit}\""
        in report_text
    )
    assert (
        "cmoc_apply_branch: \"cmoc/apply/2026-05-10_22-21_10_000000123/"
        in report_text
    )
    apply_fork_commit = state["apply"]["oracle_snapshot_commit"]
    assert f"cmoc_apply_fork_commit: \"{apply_fork_commit}\"" in report_text
    assert "apply_worktree_path: " in report_text
    assert "oracle_snapshot_commit: " in report_text
    assert "session_head_at_apply_start: " in report_text
    assert "session_head_at_apply_finish: " in report_text
    assert f"session_head_at_apply_start: \"{session_head}\"" in report_text
    assert f"session_head_at_apply_finish: \"{session_head}\"" in report_text
    assert "## 作業結果" in report_text
    assert "## 要修正点件数の推移" in report_text
    assert "全変更内容" in report_text
    assert codex_kwargs[0]["output_schema"] == _DISCREPANCY_OUTPUT_SCHEMA
    assert "fixing_points" in codex_prompts[0]
    assert "実装だけから見た成果物品質上の致命的な問題" in codex_prompts[0]
    assert "realization files の肥大化抑制" in codex_prompts[0]
    assert "同じ責務の実装・テスト・fixture・定数・コメント" in (
        codex_prompts[0]
    )
    assert "現行仕様に不要な旧実装、互換分岐" in codex_prompts[0]
    assert "oracle_requirement" in codex_prompts[0]
    investigation_kwargs = [
        kwargs
        for kwargs in codex_kwargs
        if str(kwargs.get("purpose", "")).startswith("oracle 調査 ")
        or str(kwargs.get("purpose", "")).startswith("実装調査 ")
    ]
    investigation_purposes = [
        str(kwargs.get("purpose", "")) for kwargs in investigation_kwargs
    ]
    assert investigation_kwargs
    assert any(
        purpose.startswith("oracle 調査 ")
        for purpose in investigation_purposes
    )
    assert any(
        purpose.startswith("実装調査 ")
        for purpose in investigation_purposes
    )
    assert all(
        kwargs["model"] == FRONTIER_MODEL
        for kwargs in investigation_kwargs
    )
    assert all(
        kwargs["reasoning_effort"] == FRONTIER_REASONING_EFFORT
        for kwargs in investigation_kwargs
    )
    assert all(
        kwargs.get("skip_index_maintenance") is not True
        for kwargs in investigation_kwargs
    )
    assert all(
        kwargs["index_excluded_roots"] == []
        for kwargs in investigation_kwargs
    )
    report_kwargs = [
        kwargs
        for kwargs in codex_kwargs
        if kwargs.get("purpose") == "apply 変更要約"
    ]
    assert report_kwargs == []
    assert "カテゴリ: 変更なし" in report_text
    assert (
        "今回の自動適用処理以前の作業も含めてください"
        not in "\n".join(codex_prompts)
    )


def test_apply_investigates_file_origin_targets_in_parallel(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """apply fork の file 起点調査は事前列挙対象を N+M 並列で実行する。"""
    repo = _init_repo(tmp_path)
    base_commit = _git(repo, "rev-parse", "HEAD").stdout.strip()
    (repo / ".gitignore").write_text("/.cmoc/\n", encoding="utf-8")
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    (oracle_root / "spec.md").write_text("spec\n", encoding="utf-8")
    _write_flat_oracles_index(oracle_root, "spec.md")
    (repo / "app.py").write_text("print('hello')\n", encoding="utf-8")
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "targets")
    oracle_snapshot_commit = _git(repo, "rev-parse", "HEAD").stdout.strip()

    active = 0
    max_active = 0
    lock = threading.Lock()
    codex_kwargs: list[dict[str, object]] = []

    def fake_codex(*args: object, **kwargs: object) -> str:
        """調査呼び出しが重なっているかを記録する。"""
        nonlocal active
        nonlocal max_active
        with lock:
            active += 1
            max_active = max(max_active, active)
            codex_kwargs.append(kwargs)
        try:
            time.sleep(0.05)
            return '{"git_head_commit_hash": null, "fixing_points": []}'
        finally:
            with lock:
                active -= 1

    monkeypatch.setattr("sub_commands.apply.fork.run_codex_exec", fake_codex)

    discrepancies = apply_module._investigate_discrepancies(
        repo,
        base_commit,
        oracle_snapshot_commit,
        timer=StepTimer("test"),
        step_path=((1, 1),),
        repeat_improove_fixing_list=0,
        scope="session",
    )

    purposes = [str(kwargs.get("purpose", "")) for kwargs in codex_kwargs]
    assert discrepancies == []
    assert len(codex_kwargs) >= 2
    assert max_active >= 2
    assert any(purpose.startswith("oracle 調査 ") for purpose in purposes)
    assert any(
        purpose.startswith("実装調査 ")
        for purpose in purposes
    )
    assert all(kwargs["model"] == FRONTIER_MODEL for kwargs in codex_kwargs)
    assert all(
        kwargs["reasoning_effort"] == FRONTIER_REASONING_EFFORT
        for kwargs in codex_kwargs
    )


def test_apply_scope_rolling_derives_last_joined_apply_join_commit(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """rolling scope は履歴上の最後に join された apply merge 以降だけを調査する。"""
    repo = _init_repo(tmp_path)
    _checkout_session_branch(repo)
    (repo / ".gitignore").write_text("/.cmoc/\n", encoding="utf-8")
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    (oracle_root / "old.md").write_text("old spec\n", encoding="utf-8")
    _write_flat_oracles_index(oracle_root, "old.md")
    (repo / "old.py").write_text("print('old')\n", encoding="utf-8")
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "old targets")
    last_joined_snapshot = _git(repo, "rev-parse", "HEAD").stdout.strip()
    apply_branch = "cmoc/apply/2026-05-10_22-21_10_000000123/2026-05-10_22-22_10_000000123"
    _git(repo, "switch", "-c", apply_branch, last_joined_snapshot)
    (repo / "joined.py").write_text("print('joined')\n", encoding="utf-8")
    _git(repo, "add", "joined.py")
    _git(repo, "commit", "-m", "joined implementation")
    _git(repo, "switch", "cmoc/session/2026-05-10_22-21_10_000000123")
    _git(repo, "merge", "--no-ff", apply_branch)

    state_path = (
        repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_000000123.json"
    )
    state = json.loads(state_path.read_text(encoding="utf-8"))
    state["session"]["last_joined_apply_oracle_snapshot_commit"] = (
        last_joined_snapshot
    )
    write_session_state(repo, "2026-05-10_22-21_10_000000123", state)

    (oracle_root / "new.md").write_text("new spec\n", encoding="utf-8")
    _write_flat_oracles_index(oracle_root, "new.md", "old.md")
    (repo / "new.py").write_text("print('new')\n", encoding="utf-8")
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "new targets")

    monkeypatch.setattr(
        "sub_commands.apply.fork.maintain_indexes",
        lambda repo_root: False,
    )
    purposes: list[str] = []

    def fake_codex(*args: object, **kwargs: object) -> str:
        purpose = str(kwargs.get("purpose"))
        purposes.append(purpose)
        if purpose == "apply 変更要約":
            return _change_summary_json()
        return '{"git_head_commit_hash": null, "fixing_points": []}'

    monkeypatch.setattr("sub_commands.apply.fork.run_codex_exec", fake_codex)

    assert cmoc_apply_impl(
        repo,
        repeat_investigate_and_fix=1,
        repeat_improove_fixing_list=0,
    ) == 0

    assert any(purpose.endswith("oracles/new.md") for purpose in purposes)
    assert any(purpose.endswith("new.py") for purpose in purposes)
    assert not any(purpose.endswith("oracles/old.md") for purpose in purposes)
    assert not any(purpose.endswith("old.py") for purpose in purposes)
    assert not any(purpose.endswith("joined.py") for purpose in purposes)


def test_apply_scope_rolling_rejects_joined_snapshot_without_merge(
    tmp_path: Path,
) -> None:
    """rolling scope は join 済み snapshot に対応する merge commit を必要とする。"""
    repo = _init_repo(tmp_path)
    snapshot_commit = _git(repo, "rev-parse", "HEAD").stdout.strip()
    state = {
        "session": {
            "last_joined_apply_oracle_snapshot_commit": snapshot_commit,
        }
    }

    with pytest.raises(CmocError) as error:
        apply_module._scope_base_commit(repo, state, "start123", "rolling")

    assert "merge commit" in error.value.actions[0]
    assert f"last_joined_apply_oracle_snapshot_commit: {snapshot_commit}" in (
        error.value.detail
    )


def test_apply_scope_target_selection_supports_session_and_full(
    tmp_path: Path,
) -> None:
    """session scope と full scope は仕様通り差分対象・全件対象を選べる。"""
    repo = _init_repo(tmp_path)
    base_commit = _git(repo, "rev-parse", "HEAD").stdout.strip()
    (repo / ".gitignore").write_text("/.cmoc/\n", encoding="utf-8")
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    (oracle_root / "old.md").write_text("old spec\n", encoding="utf-8")
    _write_flat_oracles_index(oracle_root, "old.md")
    (repo / "old.py").write_text("print('old')\n", encoding="utf-8")
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "old targets")
    last_joined_snapshot = _git(repo, "rev-parse", "HEAD").stdout.strip()

    (oracle_root / "new.md").write_text("new spec\n", encoding="utf-8")
    _write_flat_oracles_index(oracle_root, "new.md", "old.md")
    (repo / "new.py").write_text("print('new')\n", encoding="utf-8")
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "new targets")
    oracle_snapshot_commit = _git(repo, "rev-parse", "HEAD").stdout.strip()

    session_oracles = apply_module._target_oracle_files(
        repo,
        base_commit,
        oracle_snapshot_commit,
        partial=True,
    )
    session_impls = apply_module._target_implementation_files(
        repo,
        base_commit,
        oracle_snapshot_commit,
        partial=True,
    )
    rolling_oracles = apply_module._target_oracle_files(
        repo,
        last_joined_snapshot,
        oracle_snapshot_commit,
        partial=True,
    )
    rolling_impls = apply_module._target_implementation_files(
        repo,
        last_joined_snapshot,
        oracle_snapshot_commit,
        partial=True,
    )
    full_oracles = apply_module._target_oracle_files(
        repo,
        oracle_snapshot_commit,
        oracle_snapshot_commit,
        partial=False,
    )
    full_impls = apply_module._target_implementation_files(
        repo,
        oracle_snapshot_commit,
        oracle_snapshot_commit,
        partial=False,
    )

    assert {target.path.name for target in session_oracles} == {
        "old.md",
        "new.md",
    }
    assert {"old.py", "new.py"} <= {
        target.path.name for target in session_impls
    }
    assert {target.path.name for target in rolling_oracles} == {"new.md"}
    assert {"new.py"} <= {target.path.name for target in rolling_impls}
    assert {"old.md", "new.md"} <= {target.path.name for target in full_oracles}
    assert {"old.py", "new.py"} <= {target.path.name for target in full_impls}


def test_apply_commits_index_changes_when_no_discrepancies(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """不整合 0 件でも apply worktree の INDEX 差分を commit して完了する。"""
    repo = _init_repo(tmp_path)
    _checkout_session_branch(repo)
    (repo / ".gitignore").write_text("/.cmoc/\n", encoding="utf-8")
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    (oracle_root / "spec.md").write_text("spec\n", encoding="utf-8")
    _write_flat_oracles_index(oracle_root, "spec.md")
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "oracle")
    session_head = _git(repo, "rev-parse", "HEAD").stdout.strip()

    maintained_roots: list[Path] = []

    def fake_maintain_indexes(repo_root: Path) -> bool:
        """apply worktree の初回 INDEX メンテナンスだけ差分を作る。"""
        maintained_roots.append(repo_root)
        if not (repo_root / ".git").is_file():
            return False
        index_path = repo_root / "docs" / "INDEX.md"
        if index_path.exists():
            return False
        index_path.parent.mkdir()
        index_path.write_text("# `docs`\n", encoding="utf-8")
        return True

    monkeypatch.setattr(
        "sub_commands.apply.fork.maintain_indexes",
        fake_maintain_indexes,
    )
    codex_kwargs: list[dict[str, object]] = []

    def fake_codex(*args: object, **kwargs: object) -> str:
        """調査、commit message、変更要約生成を目的別に返す。"""
        codex_kwargs.append(kwargs)
        if kwargs.get("purpose") == "commit message 生成":
            return "Maintain apply indexes"
        if kwargs.get("purpose") == "apply 変更要約":
            return _change_summary_json()
        if kwargs.get("expect_json") is True:
            return '{"git_head_commit_hash": null, "fixing_points": []}'
        return _apply_report(str(args[1]), "収束", [0])

    monkeypatch.setattr("sub_commands.apply.fork.run_codex_exec", fake_codex)

    exit_code = cmoc_apply_impl(repo)

    state = json.loads(
        (
            repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_000000123.json"
        ).read_text(encoding="utf-8")
    )
    apply_run_id = state["apply"]["apply_branch"].rsplit("/", 1)[1]
    apply_worktree = (
        repo
        / ".cmoc"
        / "worktrees"
        / "2026-05-10_22-21_10_000000123"
        / apply_run_id
    )
    report_kwargs = [
        kwargs
        for kwargs in codex_kwargs
        if kwargs.get("purpose") == "apply 変更要約"
    ]
    reports = list(
        (repo / ".cmoc" / "reports" / "apply" / "fork").glob("*.md")
    )
    assert len(reports) == 1
    report_text = reports[0].read_text(encoding="utf-8")
    apply_head = _git(
        repo,
        "rev-parse",
        state["apply"]["apply_branch"],
    ).stdout.strip()

    assert exit_code == 0
    assert state["apply"]["state"] == "completed"
    assert _git(apply_worktree, "status", "--porcelain").stdout == ""
    assert _git(apply_worktree, "log", "-1", "--pretty=%s").stdout.strip() == (
        "Maintain apply indexes"
    )
    assert _git(apply_worktree, "show", "HEAD:docs/INDEX.md").stdout == (
        "# `docs`\n"
    )
    assert len(report_kwargs) == 1
    assert report_kwargs[0].get("skip_index_maintenance") is not True
    assert report_kwargs[0]["index_excluded_roots"] == []
    assert maintained_roots.count(apply_worktree) == 2
    assert f"session_head_at_apply_start: \"{session_head}\"" in report_text
    assert f"session_head_at_apply_finish: \"{session_head}\"" in report_text
    assert session_head != apply_head
    assert f"session_head_at_apply_finish: \"{apply_head}\"" not in report_text


def test_apply_report_records_session_head_at_finish_when_session_advances(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """apply fork は終了時点の session branch HEAD を report に記録する。"""
    repo = _init_repo(tmp_path)
    _checkout_session_branch(repo)
    (repo / ".gitignore").write_text("/.cmoc/\n", encoding="utf-8")
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    (oracle_root / "spec.md").write_text("spec\n", encoding="utf-8")
    _write_flat_oracles_index(oracle_root, "spec.md")
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "oracle")
    session_head_at_start = _git(repo, "rev-parse", "HEAD").stdout.strip()

    monkeypatch.setattr(
        "sub_commands.apply.fork.maintain_indexes",
        lambda repo_root: False,
    )
    advanced_session = False
    advance_lock = threading.Lock()

    def fake_codex(*args: object, **kwargs: object) -> str:
        """調査中に session branch を進め、調査自体は収束させる。"""
        nonlocal advanced_session
        if kwargs.get("expect_json") is True:
            with advance_lock:
                if not advanced_session:
                    (repo / "session-progress.txt").write_text(
                        "session advanced\n",
                        encoding="utf-8",
                    )
                    _git(repo, "add", "session-progress.txt")
                    _git(repo, "commit", "-m", "advance session during apply")
                    advanced_session = True
            return '{"git_head_commit_hash": null, "fixing_points": []}'
        if kwargs.get("purpose") == "apply 変更要約":
            return _change_summary_json()
        return "No changes"

    monkeypatch.setattr("sub_commands.apply.fork.run_codex_exec", fake_codex)

    exit_code = cmoc_apply_impl(repo)

    state = json.loads(
        (
            repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_000000123.json"
        ).read_text(encoding="utf-8")
    )
    reports = list(
        (repo / ".cmoc" / "reports" / "apply" / "fork").glob("*.md")
    )
    report_text = reports[0].read_text(encoding="utf-8")
    session_head_at_finish = _git(repo, "rev-parse", "HEAD").stdout.strip()
    apply_head = _git(
        repo,
        "rev-parse",
        state["apply"]["apply_branch"],
    ).stdout.strip()

    assert exit_code == 0
    assert len(reports) == 1
    assert session_head_at_start != session_head_at_finish
    assert session_head_at_finish != apply_head
    assert (
        f"session_head_at_apply_start: \"{session_head_at_start}\""
        in report_text
    )
    assert (
        f"session_head_at_apply_finish: \"{session_head_at_finish}\""
        in report_text
    )
    assert f"session_head_at_apply_finish: \"{apply_head}\"" not in report_text
def test_apply_uses_investigate_repeat_option_for_loop_limit(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """`cmoc apply` は指定された調査・修正ループ回数を上限に使う。"""
    repo = _init_repo(tmp_path)
    _checkout_session_branch(repo)
    (repo / ".gitignore").write_text("/.cmoc/\n", encoding="utf-8")
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    (oracle_root / "spec.md").write_text("spec\n", encoding="utf-8")
    _write_flat_oracles_index(oracle_root, "spec.md")
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "oracle")

    monkeypatch.setattr(
        "sub_commands.apply.fork.maintain_indexes",
        lambda repo_root: False,
    )
    codex_prompts: list[str] = []

    def fake_codex(*args: object, **kwargs: object) -> str:
        """常に不整合を返し、指定回数で incomplete になることを見やすくする。"""
        codex_prompts.append(str(args[1]))
        if str(kwargs.get("purpose")).startswith("要修正点適用"):
            (Path(args[0]) / "app.py").write_text(
                "fixed but still needs review\n",
                encoding="utf-8",
            )
            return ""
        if kwargs.get("purpose") == "apply 変更要約":
            return _change_summary_json()
        if kwargs.get("expect_json") is True:
            return _discrepancy_json("f")
        return _apply_report(str(args[1]), "未収束", [1, 1])

    monkeypatch.setattr("sub_commands.apply.fork.run_codex_exec", fake_codex)

    exit_code = cmoc_apply_impl(repo, repeat_investigate_and_fix=2)

    assert exit_code == APPLY_FORK_EXIT_CODE_UNCONVERGED
    assert (
        "実装反復 (2/2) 要修正点: 1"
        in capsys.readouterr().out
    )
    reports = list(
        (repo / ".cmoc" / "reports" / "apply" / "fork").glob("*.md")
    )
    report_text = reports[0].read_text(encoding="utf-8")
    assert codex_prompts
    assert "## 作業結果\n未収束" in report_text
    assert "まだ要修正点が残っている可能性" in report_text


def test_apply_reinvestigates_files_changed_by_previous_fix(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """Codex 修正で増えた実装差分は次の partial 調査対象に戻す。"""
    repo = _init_repo(tmp_path)
    (repo / ".gitignore").write_text("/.cmoc/\n", encoding="utf-8")
    _git(repo, "add", ".gitignore")
    _git(repo, "commit", "-m", "ignore cmoc state")
    _checkout_session_branch(repo)
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    (oracle_root / "spec.md").write_text("spec\n", encoding="utf-8")
    _write_flat_oracles_index(oracle_root, "spec.md")
    _git(repo, "add", "oracles/spec.md", "oracles/INDEX.md")
    _git(repo, "commit", "-m", "oracle")

    monkeypatch.setattr(
        "sub_commands.apply.fork.maintain_indexes",
        lambda repo_root: False,
    )
    apply_ran = False
    implementation_investigation_purposes: list[str] = []

    def first_discrepancy() -> str:
        payload = json.loads(_discrepancy_json("create app"))
        payload["fixing_points"][0]["evidences"][0]["path"] = str(
            repo / "oracles" / "spec.md"
        )
        return json.dumps(payload)

    def fake_codex(*args: object, **kwargs: object) -> str:
        """初回だけ要修正点を返し、修正後の実装調査対象を記録する。"""
        nonlocal apply_ran
        purpose = str(kwargs.get("purpose"))
        if purpose.startswith("oracle 調査"):
            if apply_ran:
                return '{"git_head_commit_hash": null, "fixing_points": []}'
            return first_discrepancy()
        if purpose.startswith("実装調査"):
            implementation_investigation_purposes.append(purpose)
            return '{"git_head_commit_hash": null, "fixing_points": []}'
        if purpose.startswith("要修正点適用"):
            apply_ran = True
            (Path(args[0]) / "app.py").write_text("fixed\n", encoding="utf-8")
            return ""
        if purpose == "commit message 生成":
            return "Apply fix"
        if purpose == "apply 変更要約":
            return _change_summary_json()
        return ""

    monkeypatch.setattr("sub_commands.apply.fork.run_codex_exec", fake_codex)

    assert cmoc_apply_impl(
        repo,
        repeat_investigate_and_fix=2,
        repeat_improove_fixing_list=0,
    ) == 0

    assert any(
        purpose.endswith("app.py")
        for purpose in implementation_investigation_purposes
    )


def test_apply_keeps_empty_oracle_dirty_set_when_only_implementation_evidence(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """実装 evidence だけの次ループで oracle dirty 空集合を再スコープ化しない。"""
    repo = _init_repo(tmp_path)
    _checkout_session_branch(repo)
    (repo / ".gitignore").write_text("/.cmoc/\n", encoding="utf-8")
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    (oracle_root / "spec.md").write_text("spec\n", encoding="utf-8")
    _write_flat_oracles_index(oracle_root, "spec.md")
    (repo / "app.py").write_text("base\n", encoding="utf-8")
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "targets")

    monkeypatch.setattr(
        "sub_commands.apply.fork.maintain_indexes",
        lambda repo_root: False,
    )
    discrepancy_returned = False
    oracle_investigation_purposes: list[str] = []
    implementation_investigation_purposes: list[str] = []

    def implementation_only_discrepancy() -> str:
        payload = json.loads(_discrepancy_json("fix app"))
        payload["fixing_points"][0]["evidences"][0]["path"] = "app.py"
        return json.dumps(payload)

    def fake_codex(*args: object, **kwargs: object) -> str:
        """初回 oracle 調査だけ実装 evidence の要修正点を返す。"""
        nonlocal discrepancy_returned
        purpose = str(kwargs.get("purpose"))
        if purpose.startswith("oracle 調査"):
            oracle_investigation_purposes.append(purpose)
            if not discrepancy_returned:
                discrepancy_returned = True
                return implementation_only_discrepancy()
            return '{"git_head_commit_hash": null, "fixing_points": []}'
        if purpose.startswith("実装調査"):
            implementation_investigation_purposes.append(purpose)
            return '{"git_head_commit_hash": null, "fixing_points": []}'
        if purpose.startswith("要修正点適用"):
            return ""
        if purpose == "apply 変更要約":
            return _change_summary_json()
        return ""

    monkeypatch.setattr("sub_commands.apply.fork.run_codex_exec", fake_codex)

    assert cmoc_apply_impl(
        repo,
        repeat_investigate_and_fix=2,
        repeat_improove_fixing_list=0,
    ) == 0

    assert len(oracle_investigation_purposes) == 1
    assert sum(
        purpose.endswith("app.py")
        for purpose in implementation_investigation_purposes
    ) == 2


def test_apply_improoves_fixing_list_until_same_result_or_limit(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """要修正点リスト改善ループは上限内で同一結果まで繰り返す。"""
    repo = _init_repo(tmp_path)
    _checkout_session_branch(repo)
    (repo / ".gitignore").write_text("/.cmoc/\n", encoding="utf-8")
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    (oracle_root / "spec.md").write_text("spec\n", encoding="utf-8")
    _write_flat_oracles_index(oracle_root, "spec.md")
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "oracle")

    monkeypatch.setattr(
        "sub_commands.apply.fork.maintain_indexes",
        lambda repo_root: False,
    )
    organize_prompts: list[str] = []
    organize_kwargs: list[dict[str, object]] = []
    apply_prompts: list[str] = []
    organize_results = [
        _discrepancy_json("first improvement"),
        _discrepancy_json("second improvement"),
        _discrepancy_json("second improvement"),
    ]

    def fake_codex(*args: object, **kwargs: object) -> str:
        """調査、改善、修正、レポートの呼び出しを purpose で分岐する。"""
        purpose = str(kwargs.get("purpose"))
        if purpose.startswith("oracle 調査") or purpose.startswith(
            "実装調査"
        ):
            return _discrepancy_json("initial")
        if purpose == "要修正点整理":
            organize_prompts.append(str(args[1]))
            organize_kwargs.append(kwargs)
            return organize_results.pop(0)
        if purpose.startswith("要修正点適用"):
            apply_prompts.append(str(args[1]))
            return ""
        if purpose == "apply 変更要約":
            return _change_summary_json()
        return ""

    monkeypatch.setattr("sub_commands.apply.fork.run_codex_exec", fake_codex)

    exit_code = cmoc_apply_impl(
        repo,
        repeat_investigate_and_fix=1,
        repeat_improove_fixing_list=3,
    )

    output = capsys.readouterr().out
    assert exit_code == APPLY_FORK_EXIT_CODE_UNCONVERGED
    assert len(organize_prompts) == 3
    assert all(kwargs["model"] == FRONTIER_MODEL for kwargs in organize_kwargs)
    assert all(
        kwargs["reasoning_effort"] == FRONTIER_HIGH_REASONING_EFFORT
        for kwargs in organize_kwargs
    )
    assert "(5/6, 1/1, 4/5, 3/3) 要修正点リスト改善" in output
    assert "(5/6, 1/1, 5/5, 1/1) 要修正点適用" in output
    assert "要修正点リスト改善ループ (3/3) 要修正点: 1" in output
    assert "second improvement" in apply_prompts[0]
    assert "initial" in organize_prompts[0]
    assert "first improvement" in organize_prompts[1]


def test_apply_improove_fixing_list_uses_oracle_snapshot_base(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """要修正点整理の過去修正範囲は apply snapshot 起点に限定する。"""
    repo = _init_repo(tmp_path)
    _checkout_session_branch(repo)
    (repo / ".gitignore").write_text("/.cmoc/\n", encoding="utf-8")
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    (oracle_root / "old.md").write_text("old spec\n", encoding="utf-8")
    _write_flat_oracles_index(oracle_root, "old.md")
    (repo / "old.py").write_text("print('old')\n", encoding="utf-8")
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "old targets")
    last_joined_snapshot = _git(repo, "rev-parse", "HEAD").stdout.strip()
    apply_branch = "cmoc/apply/2026-05-10_22-21_10_000000123/2026-05-10_22-22_10_000000123"
    _git(repo, "switch", "-c", apply_branch, last_joined_snapshot)
    (repo / "joined.py").write_text("print('joined')\n", encoding="utf-8")
    _git(repo, "add", "joined.py")
    _git(repo, "commit", "-m", "joined implementation")
    _git(repo, "switch", "cmoc/session/2026-05-10_22-21_10_000000123")
    _git(repo, "merge", "--no-ff", apply_branch)

    state_path = (
        repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_000000123.json"
    )
    state = json.loads(state_path.read_text(encoding="utf-8"))
    state["session"]["last_joined_apply_oracle_snapshot_commit"] = (
        last_joined_snapshot
    )
    write_session_state(repo, "2026-05-10_22-21_10_000000123", state)

    (oracle_root / "new.md").write_text("new spec\n", encoding="utf-8")
    _write_flat_oracles_index(oracle_root, "new.md", "old.md")
    (repo / "new.py").write_text("print('new')\n", encoding="utf-8")
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "new targets")
    oracle_snapshot_commit = _git(repo, "rev-parse", "HEAD").stdout.strip()

    monkeypatch.setattr(
        "sub_commands.apply.fork.maintain_indexes",
        lambda repo_root: False,
    )
    purposes: list[str] = []
    organize_prompts: list[str] = []

    def fake_codex(*args: object, **kwargs: object) -> str:
        """rolling の調査範囲と整理 prompt の base を記録する。"""
        purpose = str(kwargs.get("purpose"))
        purposes.append(purpose)
        if purpose.startswith("oracle 調査") or purpose.startswith(
            "実装調査"
        ):
            return _discrepancy_json("initial")
        if purpose == "要修正点整理":
            organize_prompts.append(str(args[1]))
            return '{"git_head_commit_hash": null, "fixing_points": []}'
        if purpose == "apply 変更要約":
            return _change_summary_json()
        return ""

    monkeypatch.setattr("sub_commands.apply.fork.run_codex_exec", fake_codex)

    assert cmoc_apply_impl(
        repo,
        repeat_investigate_and_fix=1,
        repeat_improove_fixing_list=1,
        scope="rolling",
    ) == 0

    assert any(purpose.endswith("oracles/new.md") for purpose in purposes)
    assert any(purpose.endswith("new.py") for purpose in purposes)
    assert not any(purpose.endswith("oracles/old.md") for purpose in purposes)
    assert not any(purpose.endswith("old.py") for purpose in purposes)
    assert not any(purpose.endswith("joined.py") for purpose in purposes)
    assert organize_prompts
    assert (
        f"`{oracle_snapshot_commit}..{oracle_snapshot_commit}`"
        in organize_prompts[0]
    )
    assert (
        f"`{last_joined_snapshot}..{oracle_snapshot_commit}`"
        not in organize_prompts[0]
    )


def test_apply_stops_improoving_fixing_list_when_it_becomes_empty(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """要修正点リスト改善ループは空リストになった時点で収束する。"""
    repo = _init_repo(tmp_path)
    _checkout_session_branch(repo)
    (repo / ".gitignore").write_text("/.cmoc/\n", encoding="utf-8")
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    (oracle_root / "spec.md").write_text("spec\n", encoding="utf-8")
    _write_flat_oracles_index(oracle_root, "spec.md")
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "oracle")

    monkeypatch.setattr(
        "sub_commands.apply.fork.maintain_indexes",
        lambda repo_root: False,
    )
    organize_prompts: list[str] = []
    apply_prompts: list[str] = []

    def fake_codex(*args: object, **kwargs: object) -> str:
        """調査後の整理で空リストを返し、以後の改善を不要にする。"""
        purpose = str(kwargs.get("purpose"))
        if purpose.startswith("oracle 調査") or purpose.startswith(
            "実装調査"
        ):
            return _discrepancy_json("initial")
        if purpose == "要修正点整理":
            organize_prompts.append(str(args[1]))
            return '{"git_head_commit_hash": null, "fixing_points": []}'
        if purpose.startswith("要修正点適用"):
            apply_prompts.append(str(args[1]))
            return ""
        if purpose == "apply 変更要約":
            return _change_summary_json()
        return ""

    monkeypatch.setattr("sub_commands.apply.fork.run_codex_exec", fake_codex)

    exit_code = cmoc_apply_impl(
        repo,
        repeat_investigate_and_fix=1,
        repeat_improove_fixing_list=3,
    )

    output = capsys.readouterr().out
    reports = list(
        (repo / ".cmoc" / "reports" / "apply" / "fork").glob("*.md")
    )
    report_text = reports[0].read_text(encoding="utf-8")
    assert exit_code == 0
    assert len(organize_prompts) == 1
    assert apply_prompts == []
    assert "要修正点リスト改善ループ (1/3) 要修正点: 0" in output
    assert "要修正点リスト改善ループ (2/3)" not in output
    assert "実装反復 (1/1) 要修正点: 0" in output
    assert "## 作業結果\n収束" in report_text


def test_apply_fills_discrepancy_head_commit_hash(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """AI が null を返しても要修正点には cmoc 側で発見時 HEAD を付与する。"""
    repo = _init_repo(tmp_path)
    _checkout_session_branch(repo)
    (repo / ".gitignore").write_text("/.cmoc/\n", encoding="utf-8")
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    (oracle_root / "spec.md").write_text("spec\n", encoding="utf-8")
    _write_flat_oracles_index(oracle_root, "spec.md")
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "oracle")
    expected_head = _git(repo, "rev-parse", "HEAD").stdout.strip()

    monkeypatch.setattr(
        "sub_commands.apply.fork.maintain_indexes",
        lambda repo_root: False,
    )
    apply_prompts: list[str] = []

    def fake_codex(*args: object, **kwargs: object) -> str:
        """調査は null の hash を返し、修正依頼 prompt を記録する。"""
        purpose = str(kwargs.get("purpose"))
        if purpose.startswith("oracle 調査") or purpose.startswith(
            "実装調査"
        ):
            return _discrepancy_json("fill hash")
        if purpose.startswith("要修正点適用"):
            apply_prompts.append(str(args[1]))
            return ""
        if purpose == "apply 変更要約":
            return _change_summary_json()
        return ""

    monkeypatch.setattr("sub_commands.apply.fork.run_codex_exec", fake_codex)

    assert cmoc_apply_impl(
        repo,
        repeat_investigate_and_fix=1,
        repeat_improove_fixing_list=0,
    ) == APPLY_FORK_EXIT_CODE_UNCONVERGED

    assert apply_prompts
    assert all(
        f'"git_head_commit_hash": "{expected_head}"' in prompt
        for prompt in apply_prompts
    )
    assert all(
        '"git_head_commit_hash": null' not in prompt
        for prompt in apply_prompts
    )


def test_apply_commits_each_discrepancy_before_next_codex_call(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """修正作業ループは要修正点 1 件ごとに検査と commit を完了する。"""
    repo = _init_repo(tmp_path)
    _checkout_session_branch(repo)
    (repo / ".gitignore").write_text("/.cmoc/\n", encoding="utf-8")
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    (oracle_root / "spec.md").write_text("spec\n", encoding="utf-8")
    _write_flat_oracles_index(oracle_root, "spec.md")
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "oracle")

    monkeypatch.setattr(
        "sub_commands.apply.fork.maintain_indexes",
        lambda repo_root: False,
    )
    first_payload = json.loads(_discrepancy_json("first fix"))
    second_item = json.loads(_discrepancy_json("second fix"))[
        "fixing_points"
    ][0]
    first_payload["fixing_points"].append(second_item)
    two_discrepancies_json = json.dumps(first_payload)
    apply_count = 0
    commit_message_count = 0
    status_before_second_apply: list[str] = []
    head_before_second_apply: list[str] = []
    apply_repos: list[Path] = []
    commit_message_options: list[tuple[object, object]] = []

    def fake_codex(*args: object, **kwargs: object) -> str:
        """2 件の修正依頼の間で作業ツリーと HEAD を記録する。"""
        nonlocal apply_count
        nonlocal commit_message_count
        purpose = str(kwargs.get("purpose"))
        if purpose.startswith("oracle 調査") or purpose.startswith(
            "実装調査"
        ):
            return two_discrepancies_json
        if purpose == "要修正点整理":
            return two_discrepancies_json
        if purpose.startswith("要修正点適用"):
            apply_count += 1
            apply_repos.append(Path(args[0]))
            if apply_count == 2:
                apply_repo = Path(args[0])
                status_before_second_apply.append(
                    _git(apply_repo, "status", "--porcelain").stdout
                )
                head_before_second_apply.append(
                    _git(apply_repo, "log", "-1", "--pretty=%s").stdout.strip()
                )
            (Path(args[0]) / "app.py").write_text(
                f"fix {apply_count}\n",
                encoding="utf-8",
            )
            return ""
        if purpose == "commit message 生成":
            commit_message_count += 1
            commit_message_options.append(
                (
                    kwargs.get("model"),
                    kwargs.get("reasoning_effort"),
                )
            )
            return f"Apply fix {commit_message_count}"
        if purpose == "apply 変更要約":
            return _change_summary_json()
        return ""

    monkeypatch.setattr("sub_commands.apply.fork.run_codex_exec", fake_codex)

    assert (
        cmoc_apply_impl(repo, repeat_investigate_and_fix=1)
        == APPLY_FORK_EXIT_CODE_UNCONVERGED
    )

    assert apply_repos
    commit_subjects = _git(
        apply_repos[-1],
        "log",
        "--pretty=%s",
        "-3",
    ).stdout.splitlines()
    assert apply_count == 2
    assert commit_message_count == 2
    assert commit_message_options == [
        (COMMIT_MESSAGE_MODEL, COMMIT_MESSAGE_REASONING_EFFORT),
        (COMMIT_MESSAGE_MODEL, COMMIT_MESSAGE_REASONING_EFFORT),
    ]
    assert status_before_second_apply == [""]
    assert head_before_second_apply == ["Apply fix 1"]
    assert commit_subjects[:2] == ["Apply fix 2", "Apply fix 1"]
    assert _git(repo, "status", "--porcelain").stdout == ""
    assert _git(repo, "branch", "--show-current").stdout.strip() == (
        "cmoc/session/2026-05-10_22-21_10_000000123"
    )


def test_organize_prompt_includes_fixing_list_quality_requirements(
    tmp_path: Path,
) -> None:
    """要修正点リスト改善 prompt は成果物品質の観点を明示する。"""
    prompt = _organize_prompt(
        tmp_path,
        json.loads(_discrepancy_json("fix"))["fixing_points"],
        "cmoc/session/2026-05-10_22-21_10_000000123",
        "1111111111111111111111111111111111111111",
        "2222222222222222222222222222222222222222",
    )

    assert "内容の品質に明確な問題がない" in prompt
    assert "realization files の肥大化抑制" in prompt
    assert "新しい抽象化、CLI 引数、設定項目、状態、外部依存" in prompt
    assert "同じ観点のテストは統合可能か確認" in prompt
    assert "重複する要修正点は 1 件にマージ" in prompt
    assert "矛盾する修正方針は矛盾しない内容に調整" in prompt
    assert "git ブランチ `cmoc/session/2026-05-10_22-21_10_000000123`" in prompt
    assert (
        "`1111111111111111111111111111111111111111"
        "..2222222222222222222222222222222222222222`"
    ) in prompt
    assert "に含まれる過去の修正内容を確認" in prompt
    assert "False-Positive と判断できる要修正点は除外" in prompt
    assert "作業順序として適切になるよう並べ替えてください" in prompt
    assert "改善過程で発見した漏れがあれば" in prompt


def test_apply_prompt_treats_discrepancy_as_optional_hint(
    tmp_path: Path,
) -> None:
    """修正作業 prompt は要修正点情報を無視可能なヒントとして扱う。"""
    prompt = _apply_prompt(
        tmp_path,
        {
            "title": "sample",
            "oracle_requirement": "oracle requirement",
            "observed_implementation": "observed implementation",
            "reason": "reason",
            "suggested_fix": "suggested fix",
            "evidences": [],
        },
    )

    assert "作業のためのヒント" in prompt
    assert "絶対に従わなければならない指示書としては扱わない" in prompt
    assert "realization files の肥大化抑制" in prompt
    assert "追加した realization files の削除・統合・短縮余地" in prompt
    assert "無視してかまいません" in prompt
    assert "ベストエフォート" in prompt
    assert "目的を達成した保証は不要" in prompt
    assert f"`{tmp_path / 'oracles'}` は編集禁止です。" in prompt
    assert "配下の `INDEX.md` 以外は編集禁止" not in prompt
    assert f"`{tmp_path / 'README.md'}` は編集禁止です。" in prompt
    assert f"`{tmp_path / 'AGENTS.md'}` は編集禁止です。" in prompt
    assert f"`{tmp_path / '.cmoc'}` は編集禁止です。" in prompt


def test_apply_prompt_orders_completion_before_details() -> None:
    """修正作業 prompt はロール、作業、完了条件、詳細指示の順にする。"""
    prompt = _apply_prompt(
        Path("/repo"),
        {
            "title": "sample",
            "oracle_requirement": "oracle requirement",
            "observed_implementation": "observed implementation",
            "reason": "reason",
            "suggested_fix": "suggested fix",
            "evidences": [],
        },
    )
    lines = prompt.splitlines()

    assert lines[0] == "あなたはソフトウェア実装担当です。"
    assert lines[1] == (
        "`/repo` の実装を、要修正点情報に記載された仕様要求に"
        "追従するようベストエフォートで更新してください。"
    )
    assert lines[2] == (
        "完了条件は、必要と判断した実装修正とテスト更新を終え、変更内容と残課題を報告することです。"
    )
    assert lines.index("以下の要修正点情報は作業のためのヒントです。") > 2


def test_apply_report_validation_requires_markdown_sections() -> None:
    """apply report 検証は本文全体の substring だけでは通さない。"""
    body = "\n".join(
        [
            "作業結果 収束",
            "要修正点件数の推移 1 回目: 0 件",
            "cmoc/apply/session/run 全変更内容 カテゴリ: 実装修正",
            "本文に必要語はあるが Markdown 見出しではない。",
        ]
    )

    with pytest.raises(ValueError) as error:
        apply_module._validate_apply_report(
            body,
            "cmoc/apply/session/run",
            "収束",
            True,
            [0],
        )

    assert "作業結果の区分" in str(error.value)
    assert "要修正点件数の推移" in str(error.value)
    assert "ブランチ上の全変更内容" in str(error.value)


def test_apply_report_validation_matches_loop_counts_by_line() -> None:
    """件数推移は loop 番号と件数が同じ行に対応している必要がある。"""
    body = "\n".join(
        [
            "## 作業結果",
            "未収束",
            "",
            "## 要修正点件数の推移",
            "- 1 回目: 9 件",
            "- 2 回目: 1 件",
            "まだ要修正点が残っている可能性があります。",
            "",
            "## ブランチ cmoc/apply/session/run 上の全変更内容",
            "- カテゴリ: 実装修正",
            "  - 要約を記録しました。",
        ]
    )

    with pytest.raises(ValueError) as error:
        apply_module._validate_apply_report(
            body,
            "cmoc/apply/session/run",
            "未収束",
            False,
            [1, 9],
        )

    assert "要修正点件数の推移 loop 1" in str(error.value)
    assert "要修正点件数の推移 loop 2" in str(error.value)


def test_apply_report_validation_requires_change_summary_item() -> None:
    """全変更内容 section はカテゴリ名だけでなく要約項目も必要とする。"""
    body = "\n".join(
        [
            "## 作業結果",
            "収束",
            "",
            "## 要修正点件数の推移",
            "- 1 回目: 0 件",
            "",
            "## ブランチ cmoc/apply/session/run 上の全変更内容",
            "- カテゴリ: 実装修正",
        ]
    )

    with pytest.raises(ValueError) as error:
        apply_module._validate_apply_report(
            body,
            "cmoc/apply/session/run",
            "収束",
            True,
            [0],
        )

    assert "ブランチ上の全変更内容" in str(error.value)


def test_apply_report_validation_requires_fork_commit_metadata() -> None:
    """Front Matter は session/apply それぞれの分岐元 commit を必須にする。"""
    report = "\n".join(
        [
            "---",
            "generated_at: \"2026-05-10T22:21:10\"",
            "cmoc_session_id: \"session\"",
            "cmoc_apply_run_id: \"run\"",
            "cmoc_session_branch: \"cmoc/session/session\"",
            "cmoc_apply_branch: \"cmoc/apply/session/run\"",
            "apply_worktree_path: \"/tmp/worktree\"",
            "oracle_snapshot_commit: \"apply-fork\"",
            "session_head_at_apply_start: \"apply-fork\"",
            "session_head_at_apply_finish: \"apply-finish\"",
            "result: \"収束\"",
            "---",
            "",
            "## 作業結果",
            "収束",
            "",
            "## 要修正点件数の推移",
            "- 1 回目: 0 件",
            "",
            "## ブランチ cmoc/apply/session/run 上の全変更内容",
            "- カテゴリ: 実装修正",
            "  - 要約を記録しました。",
        ]
    )

    with pytest.raises(ValueError) as error:
        apply_module._validate_apply_report(
            report,
            "cmoc/apply/session/run",
            "収束",
            True,
            [0],
            require_front_matter=True,
        )

    assert "YAML Front Matter cmoc_session_fork_commit" in str(error.value)
    assert "YAML Front Matter cmoc_apply_fork_commit" in str(error.value)


def test_apply_marks_error_when_success_report_generation_fails(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """成功 report 生成失敗は completed ではなく error として記録する。"""
    repo = _init_repo(tmp_path)
    _checkout_session_branch(repo)
    (repo / ".gitignore").write_text("/.cmoc/\n", encoding="utf-8")
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    (oracle_root / "spec.md").write_text("spec\n", encoding="utf-8")
    _write_flat_oracles_index(oracle_root, "spec.md")
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "oracle")
    session_head = _git(repo, "rev-parse", "HEAD").stdout.strip()

    def fake_maintain_indexes(repo_root: Path) -> bool:
        """apply worktree 側だけ report 対象差分を作る。"""
        if not (repo_root / ".git").is_file():
            return False
        index_path = repo_root / "docs" / "INDEX.md"
        if index_path.exists():
            return False
        index_path.parent.mkdir()
        index_path.write_text("# `docs`\n", encoding="utf-8")
        return True

    monkeypatch.setattr(
        "sub_commands.apply.fork.maintain_indexes",
        fake_maintain_indexes,
    )
    advanced_session = False

    def fake_codex(*args: object, **kwargs: object) -> str:
        """調査は収束、変更要約は必須項目不足にする。"""
        nonlocal advanced_session
        if kwargs.get("purpose") == "apply 変更要約":
            if not advanced_session:
                (repo / "session-progress.txt").write_text(
                    "session advanced\n",
                    encoding="utf-8",
                )
                _git(repo, "add", "session-progress.txt")
                _git(repo, "commit", "-m", "advance session during apply")
                advanced_session = True
            return '{"changes": []}'
        if kwargs.get("expect_json") is True:
            return '{"git_head_commit_hash": null, "fixing_points": []}'
        return "Maintain indexes"

    monkeypatch.setattr("sub_commands.apply.fork.run_codex_exec", fake_codex)

    with pytest.raises(CmocError):
        cmoc_apply_impl(repo)

    state = json.loads(
        (
            repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_000000123.json"
        ).read_text(encoding="utf-8")
    )
    report_dir = repo / ".cmoc" / "reports" / "apply" / "fork"
    assert state["apply"]["state"] == "error"
    assert state["apply"]["apply_branch"].startswith(
        "cmoc/apply/2026-05-10_22-21_10_000000123/"
    )
    reports = list(report_dir.glob("*.md"))
    apply_head = _git(
        repo,
        "rev-parse",
        state["apply"]["apply_branch"],
    ).stdout.strip()
    session_head_at_finish = _git(repo, "rev-parse", "HEAD").stdout.strip()
    assert len(reports) == 1
    assert 'result: "エラー"' in reports[0].read_text(encoding="utf-8")
    assert session_head != session_head_at_finish
    assert session_head != apply_head
    assert not (
        repo
        / ".cmoc"
        / "sessions"
        / "2026-05-10_22-21_10_000000123.apply_process.json"
    ).exists()


def test_apply_marks_error_before_success_report_when_completion_record_fails(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """完了 state 更新失敗時は成功 report を保存せず error として記録する。"""
    repo = _init_repo(tmp_path)
    _checkout_session_branch(repo)
    (repo / ".gitignore").write_text("/.cmoc/\n", encoding="utf-8")
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    (oracle_root / "spec.md").write_text("spec\n", encoding="utf-8")
    _write_flat_oracles_index(oracle_root, "spec.md")
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "oracle")

    monkeypatch.setattr(
        "sub_commands.apply.fork.maintain_indexes",
        lambda repo_root: False,
    )

    def fake_codex(*args: object, **kwargs: object) -> str:
        """調査は収束させ、error report の変更要約も返す。"""
        if kwargs.get("purpose") == "apply 変更要約":
            return _change_summary_json()
        if kwargs.get("expect_json") is True:
            return '{"git_head_commit_hash": null, "fixing_points": []}'
        return "No changes"

    success_report_called = False

    def fake_write_apply_report(*args: object, **kwargs: object) -> Path:
        """完了記録後の成功 report へ進んでいないことを検証する。"""
        nonlocal success_report_called
        success_report_called = True
        raise AssertionError("success report must not be written")

    def fake_mark_apply_completed(*args: object, **kwargs: object) -> None:
        """session state の completed 永続化失敗を模擬する。"""
        raise RuntimeError("fake completion record failure")

    monkeypatch.setattr("sub_commands.apply.fork.run_codex_exec", fake_codex)
    monkeypatch.setattr(
        apply_module,
        "_write_apply_report",
        fake_write_apply_report,
    )
    monkeypatch.setattr(
        apply_module,
        "_mark_apply_completed",
        fake_mark_apply_completed,
    )

    with pytest.raises(RuntimeError, match="fake completion record failure"):
        cmoc_apply_impl(repo)

    state = json.loads(
        (
            repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_000000123.json"
        ).read_text(encoding="utf-8")
    )
    reports = list(
        (repo / ".cmoc" / "reports" / "apply" / "fork").glob("*.md")
    )
    report_texts = [report.read_text(encoding="utf-8") for report in reports]

    assert not success_report_called
    assert state["apply"]["state"] == "error"
    assert len(reports) == 1
    assert any('result: "エラー"' in text for text in report_texts)
    assert any(
        "- Failed stage: `apply 完了記録`" in text for text in report_texts
    )
    assert not (
        repo
        / ".cmoc"
        / "sessions"
        / "2026-05-10_22-21_10_000000123.apply_process.json"
    ).exists()


def test_apply_marks_error_when_final_output_fails(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """最終出力失敗は completed ではなく error として記録する。"""
    repo = _init_repo(tmp_path)
    _checkout_session_branch(repo)
    (repo / ".gitignore").write_text("/.cmoc/\n", encoding="utf-8")
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    (oracle_root / "spec.md").write_text("spec\n", encoding="utf-8")
    _write_flat_oracles_index(oracle_root, "spec.md")
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "oracle")

    monkeypatch.setattr(
        "sub_commands.apply.fork.maintain_indexes",
        lambda repo_root: False,
    )

    def fake_codex(*args: object, **kwargs: object) -> str:
        """調査は収束させ、必要なら変更要約を返す。"""
        if kwargs.get("purpose") == "apply 変更要約":
            return _change_summary_json()
        if kwargs.get("expect_json") is True:
            return '{"git_head_commit_hash": null, "fixing_points": []}'
        return "No changes"

    monkeypatch.setattr("sub_commands.apply.fork.run_codex_exec", fake_codex)
    failed_once = False

    def fake_print(*args: object, **kwargs: object) -> None:
        """収束 report path の最初の出力だけ失敗させる。"""
        nonlocal failed_once
        if (
            not failed_once
            and len(args) == 1
            and str(args[0]).endswith(".md")
        ):
            failed_once = True
            raise RuntimeError("fake final output failure")
        builtins.print(*args, **kwargs)

    monkeypatch.setattr(apply_module, "print", fake_print, raising=False)

    with pytest.raises(RuntimeError, match="fake final output failure"):
        cmoc_apply_impl(repo)

    state = json.loads(
        (
            repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_000000123.json"
        ).read_text(encoding="utf-8")
    )
    reports = list(
        (repo / ".cmoc" / "reports" / "apply" / "fork").glob("*.md")
    )
    report_texts = [report.read_text(encoding="utf-8") for report in reports]

    assert state["apply"]["state"] == "error"
    assert state["apply"]["apply_branch"].startswith(
        "cmoc/apply/2026-05-10_22-21_10_000000123/"
    )
    assert len(reports) == 1
    assert any('result: "エラー"' in text for text in report_texts)
    assert not (
        repo
        / ".cmoc"
        / "sessions"
        / "2026-05-10_22-21_10_000000123.apply_process.json"
    ).exists()


def test_apply_fallback_change_summary_preserves_special_path_tokens(
    tmp_path: Path,
) -> None:
    """fallback report の changed_paths は newline や前後空白を削らない。"""
    repo = _init_repo(tmp_path)
    snapshot_commit = _git(repo, "rev-parse", "HEAD").stdout.strip()
    special_path = repo / " changed\nfile.py "
    special_path.write_text("changed\n", encoding="utf-8")
    _git(repo, "add", special_path.relative_to(repo).as_posix())
    _git(repo, "commit", "-m", "special path")
    branch_name = _git(repo, "branch", "--show-current").stdout.strip()

    summary = apply_module._fallback_change_summary_from_git(
        repo,
        branch_name,
        snapshot_commit,
        RuntimeError("summary failed"),
    )

    assert summary[0]["changed_paths"] == [" changed\nfile.py "]


def test_apply_fallback_change_summary_includes_uncommitted_paths(
    tmp_path: Path,
) -> None:
    """fallback report は staged/working tree/untracked の変更も列挙する。"""
    repo = _init_repo(tmp_path)
    snapshot_commit = _git(repo, "rev-parse", "HEAD").stdout.strip()
    branch_name = _git(repo, "branch", "--show-current").stdout.strip()

    (repo / "working.py").write_text("working\n", encoding="utf-8")
    _git(repo, "add", "working.py")
    _git(repo, "commit", "-m", "add working")
    (repo / "staged.py").write_text("staged\n", encoding="utf-8")
    _git(repo, "add", "staged.py")
    (repo / "working.py").write_text("working changed\n", encoding="utf-8")
    (repo / "untracked.py").write_text("untracked\n", encoding="utf-8")

    summary = apply_module._fallback_change_summary_from_git(
        repo,
        branch_name,
        snapshot_commit,
        RuntimeError("summary failed"),
    )

    assert summary[0]["category"] == "変更ファイル一覧"
    assert summary[0]["changed_paths"] == [
        "staged.py",
        "untracked.py",
        "working.py",
    ]


def test_apply_fallback_change_summary_includes_deleted_paths(
    tmp_path: Path,
) -> None:
    """fallback report は commit 済み/staged/working tree の削除も列挙する。"""
    repo = _init_repo(tmp_path)
    (repo / "committed_delete.py").write_text("committed\n", encoding="utf-8")
    (repo / "staged_delete.py").write_text("staged\n", encoding="utf-8")
    (repo / "working_delete.py").write_text("working\n", encoding="utf-8")
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "add delete targets")
    snapshot_commit = _git(repo, "rev-parse", "HEAD").stdout.strip()
    branch_name = _git(repo, "branch", "--show-current").stdout.strip()

    (repo / "committed_delete.py").unlink()
    _git(repo, "add", "committed_delete.py")
    _git(repo, "commit", "-m", "delete committed")
    (repo / "staged_delete.py").unlink()
    _git(repo, "add", "staged_delete.py")
    (repo / "working_delete.py").unlink()

    summary = apply_module._fallback_change_summary_from_git(
        repo,
        branch_name,
        snapshot_commit,
        RuntimeError("summary failed"),
    )

    assert summary[0]["category"] == "変更ファイル一覧"
    assert summary[0]["changed_paths"] == [
        "committed_delete.py",
        "staged_delete.py",
        "working_delete.py",
    ]


def test_apply_change_summary_treats_uncommitted_paths_as_changes(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """変更要約は commit 間差分が空でも未コミット差分があれば Codex に依頼する。"""
    repo = _init_repo(tmp_path)
    snapshot_commit = _git(repo, "rev-parse", "HEAD").stdout.strip()
    branch_name = _git(repo, "branch", "--show-current").stdout.strip()
    (repo / "working.py").write_text("working\n", encoding="utf-8")

    prompts: list[str] = []

    def fake_codex(repo_root: Path, prompt: str, **kwargs: object) -> str:
        prompts.append(prompt)
        return _change_summary_json()

    monkeypatch.setattr("sub_commands.apply.fork.run_codex_exec", fake_codex)

    summary = apply_module._generate_change_summary(
        repo,
        branch_name,
        snapshot_commit,
    )

    assert prompts
    assert "working tree / staging area" in prompts[0]
    assert 'top-level JSON object として {"changes": [...]} を返す' in prompts[0]
    assert "changes 配列だけを返す" not in prompts[0]
    assert summary[0]["category"] == "実装修正"


def test_apply_change_summary_treats_deleted_paths_as_changes(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """変更要約は削除のみの差分でも Codex に依頼する。"""
    repo = _init_repo(tmp_path)
    (repo / "deleted.py").write_text("deleted\n", encoding="utf-8")
    _git(repo, "add", "deleted.py")
    _git(repo, "commit", "-m", "add deleted target")
    snapshot_commit = _git(repo, "rev-parse", "HEAD").stdout.strip()
    branch_name = _git(repo, "branch", "--show-current").stdout.strip()
    (repo / "deleted.py").unlink()
    _git(repo, "add", "deleted.py")

    prompts: list[str] = []

    def fake_codex(repo_root: Path, prompt: str, **kwargs: object) -> str:
        prompts.append(prompt)
        return json.dumps(
            {
                "changes": [
                    {
                        "category": "削除",
                        "summary": "不要なファイルを削除しました。",
                        "changed_paths": ["deleted.py"],
                    }
                ]
            }
        )

    monkeypatch.setattr("sub_commands.apply.fork.run_codex_exec", fake_codex)

    summary = apply_module._generate_change_summary(
        repo,
        branch_name,
        snapshot_commit,
    )

    assert prompts
    assert '["deleted.py"]' in prompts[0]
    assert summary[0]["changed_paths"] == ["deleted.py"]


def test_apply_writes_error_report_when_midway_stage_fails(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """apply fork は途中エラーでも保存済みレポートのパスを出力する。"""
    repo = _init_repo(tmp_path)
    _checkout_session_branch(repo)
    (repo / ".gitignore").write_text("/.cmoc/\n", encoding="utf-8")
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    (oracle_root / "spec.md").write_text("spec\n", encoding="utf-8")
    _write_flat_oracles_index(oracle_root, "spec.md")
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "oracle")

    def fail_maintain_indexes(repo_root: Path) -> bool:
        raise RuntimeError(f"fake maintain failure at {repo_root.name}")

    monkeypatch.setattr(
        "sub_commands.apply.fork.maintain_indexes",
        fail_maintain_indexes,
    )

    with pytest.raises(RuntimeError, match="fake maintain failure"):
        cmoc_apply_impl(repo)

    state = json.loads(
        (
            repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_000000123.json"
        ).read_text(encoding="utf-8")
    )
    reports = list(
        (repo / ".cmoc" / "reports" / "apply" / "fork").glob("*.md")
    )
    captured = capsys.readouterr()

    assert state["apply"]["state"] == "error"
    assert state["apply"]["apply_branch"].startswith(
        "cmoc/apply/2026-05-10_22-21_10_000000123/"
    )
    assert len(reports) == 1
    assert str(reports[0]) in captured.out
    report_text = reports[0].read_text(encoding="utf-8")
    session_fork_commit = state["session"]["session_start_commit"]
    assert "result: \"エラー\"" in report_text
    assert "cmoc_apply_run_id: " in report_text
    assert (
        f"cmoc_session_fork_commit: \"{session_fork_commit}\""
        in report_text
    )
    assert (
        "cmoc_apply_branch: \"cmoc/apply/2026-05-10_22-21_10_000000123/"
        in report_text
    )
    apply_fork_commit = state["apply"]["oracle_snapshot_commit"]
    assert f"cmoc_apply_fork_commit: \"{apply_fork_commit}\"" in report_text
    assert "apply_worktree_path: " in report_text
    assert "- Failed stage: `INDEX.md メンテナンス`" in report_text
    assert "- Exception type: `RuntimeError`" in report_text
    assert "- Exception message: `fake maintain failure at " in report_text
    assert "エラー発生前に記録済みの要修正点件数はありません。" in report_text
    assert "カテゴリ: 変更なし" in report_text


def test_apply_error_report_includes_codex_change_summary(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """error report でも apply branch の変更要約を Codex Structured Output から描画する。"""
    repo = _init_repo(tmp_path)
    (repo / "oracles").mkdir()
    (repo / "oracles" / "spec.md").write_text("spec\n", encoding="utf-8")
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "base")
    oracle_snapshot_commit = _git(repo, "rev-parse", "HEAD").stdout.strip()
    apply_branch = "cmoc/apply/session/run"
    _git(repo, "checkout", "-b", apply_branch)
    (repo / "app.py").write_text("print('changed')\n", encoding="utf-8")
    _git(repo, "add", "app.py")
    _git(repo, "commit", "-m", "change app")

    codex_purposes: list[str] = []

    def fake_codex(*args: object, **kwargs: object) -> str:
        codex_purposes.append(str(kwargs.get("purpose")))
        return _change_summary_json()

    monkeypatch.setattr("sub_commands.apply.fork.run_codex_exec", fake_codex)

    report_path = apply_module._write_apply_error_report(
        repo,
        "session",
        "run",
        "cmoc/session/session",
        apply_branch,
        repo,
        oracle_snapshot_commit,
        oracle_snapshot_commit,
        oracle_snapshot_commit,
        oracle_snapshot_commit,
        "要修正点適用",
        RuntimeError("fake apply failure"),
        [1],
    )

    report_text = report_path.read_text(encoding="utf-8")
    assert codex_purposes == ["apply 変更要約"]
    assert "result: \"エラー\"" in report_text
    assert "## エラー詳細" in report_text
    assert "- Failed stage: `要修正点適用`" in report_text
    assert "カテゴリ: 実装修正" in report_text
    assert "テスト用の変更内容を整理しました。" in report_text
    assert "- `app.py`" in report_text
    assert "カテゴリ: エラー終了" not in report_text


def test_apply_rejects_non_cmoc_branch(tmp_path: Path) -> None:
    """`cmoc apply` は cmoc ブランチ外では仕様通り CmocError にする。"""
    repo = _init_repo(tmp_path)

    with pytest.raises(CmocError) as error:
        cmoc_apply_impl(repo)

    assert "`cmoc apply` は session branch 上で実行してください。" in error.value.message


def test_apply_rejects_non_oracle_changes_after_cmoc_guarantee(
    tmp_path: Path,
) -> None:
    """開始前の未コミット実装差分は ignore 保証前に拒否する。"""
    repo = _init_repo(tmp_path)
    _checkout_session_branch(repo)
    (repo / "app.py").write_text("changed\n", encoding="utf-8")

    with pytest.raises(CmocError) as error:
        cmoc_apply_impl(repo)

    assert "未コミットの変更" in error.value.message
    assert "app.py" in error.value.detail
    assert not (repo / ".gitignore").exists()
    assert _git(repo, "log", "-1", "--pretty=%s").stdout.strip() == "initial"


def test_apply_does_not_commit_preexisting_gitignore_changes(
    tmp_path: Path,
) -> None:
    """開始前からある `.gitignore` 差分も precondition failure にする。"""
    repo = _init_repo(tmp_path)
    _checkout_session_branch(repo)
    (repo / ".gitignore").write_text("user-rule\n", encoding="utf-8")

    with pytest.raises(CmocError) as error:
        cmoc_apply_impl(repo)

    assert "未コミットの変更" in error.value.message
    assert _git(repo, "status", "--porcelain", "--", ".gitignore").stdout == (
        "?? .gitignore\n"
    )


def test_apply_untracks_existing_cmoc_before_worktree_creation(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """apply fork は state 検証後に tracked `.cmoc` を初期化 commit で外す。"""
    repo = _init_repo(tmp_path)
    _checkout_session_branch(repo)
    state_path = ".cmoc/sessions/2026-05-10_22-21_10_000000123.json"
    _git(repo, "add", "-f", state_path)
    _git(repo, "commit", "-m", "track session state")

    monkeypatch.setattr(
        "sub_commands.apply.fork.maintain_indexes",
        lambda repo_root: False,
    )

    exit_code = cmoc_apply_impl(repo, repeat_investigate_and_fix=0)

    assert exit_code == APPLY_FORK_EXIT_CODE_UNCONVERGED
    assert _git(repo, "show", "HEAD:.gitignore").stdout == "/.cmoc/\n"
    assert _git(repo, "log", "-1", "--pretty=%s").stdout.strip() == (
        "Initialize cmoc"
    )
    assert (repo / ".cmoc" / "worktrees").exists()
    assert _git(repo, "ls-files", "--", ".cmoc").stdout == ""
    branches = _git(repo, "branch", "--format=%(refname:short)").stdout
    assert "cmoc/apply/" in branches
    assert _git(repo, "status", "--porcelain").stdout == ""


def test_apply_rejects_broken_session_state_before_cmoc_ignore(
    tmp_path: Path,
) -> None:
    """壊れた session state は `.gitignore` を作らずに拒否する。"""
    repo = _init_repo(tmp_path)
    _git(repo, "checkout", "-b", "cmoc/session/2026-05-10_22-21_10_000000123")
    broken_path = repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_000000123.json"
    broken_path.parent.mkdir(parents=True)
    broken_path.write_text("{not json", encoding="utf-8")

    with pytest.raises(CmocError) as error:
        cmoc_apply_impl(repo)

    assert "JSON が不正" in error.value.message
    assert not (repo / ".gitignore").exists()
    assert not (repo / ".cmoc" / "worktrees").exists()
    branches = _git(repo, "branch", "--format=%(refname:short)").stdout
    assert "cmoc/apply/" not in branches


def test_apply_rejects_not_ready_state_before_cmoc_ignore(
    tmp_path: Path,
) -> None:
    """apply.state の事前条件違反では `.gitignore` を変更しない。"""
    repo = _init_repo(tmp_path)
    _checkout_session_branch(repo)
    session_id = "2026-05-10_22-21_10_000000123"
    state_path = repo / ".cmoc" / "sessions" / f"{session_id}.json"
    state = json.loads(state_path.read_text(encoding="utf-8"))
    state["apply"]["state"] = "running"
    state["apply"]["apply_branch"] = (
        f"cmoc/apply/{session_id}/2026-05-10_22-22_10_000000123"
    )
    state["apply"]["oracle_snapshot_commit"] = _git(
        repo,
        "rev-parse",
        "HEAD",
    ).stdout.strip()
    state_path.write_text(
        json.dumps(state, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    with pytest.raises(CmocError) as error:
        cmoc_apply_impl(repo)

    assert "apply run を開始できる状態ではありません。" in error.value.message
    assert "apply.state: running" in error.value.detail
    assert not (repo / ".gitignore").exists()
    assert not (repo / ".cmoc" / "worktrees").exists()
    branches = _git(repo, "branch", "--format=%(refname:short)").stdout
    assert "cmoc/apply/" not in branches


def test_apply_rejects_negative_repeat_before_worktree_creation(
    tmp_path: Path,
) -> None:
    """repeat 系オプションの負値は apply 開始副作用の前に拒否する。"""
    repo = _init_repo(tmp_path)
    _checkout_session_branch(repo)

    with pytest.raises(CmocError) as error:
        cmoc_apply_impl(repo, repeat_investigate_and_fix=-1)

    state = json.loads(
        (
            repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_000000123.json"
        ).read_text(encoding="utf-8")
    )
    branches = _git(repo, "branch", "--format=%(refname:short)").stdout
    assert "調査・修正ループ回数に負の値" in error.value.message
    assert state["apply"] == {
        "apply_branch": None,
        "oracle_snapshot_commit": None,
        "state": "ready",
    }
    assert not (repo / ".cmoc" / "worktrees").exists()
    assert "cmoc/apply/" not in branches


def test_apply_marks_error_when_running_state_write_fails(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """apply 開始中の state 書き込み失敗も error state として残す。"""
    repo = _init_repo(tmp_path)
    _checkout_session_branch(repo)
    (repo / ".gitignore").write_text("/.cmoc/\n", encoding="utf-8")
    _git(repo, "add", ".gitignore")
    _git(repo, "commit", "-m", "ignore cmoc")
    real_write_session_state = apply_module.write_session_state
    calls = 0

    def flaky_write_session_state(
        repo_root: Path,
        session_id: str,
        state: dict[str, object],
    ) -> Path:
        """running 遷移の保存だけ失敗させる。"""
        nonlocal calls
        calls += 1
        if calls == 1:
            raise OSError("fake running write failure")
        return real_write_session_state(repo_root, session_id, state)

    monkeypatch.setattr(
        apply_module,
        "write_session_state",
        flaky_write_session_state,
    )

    with pytest.raises(OSError) as error:
        cmoc_apply_impl(repo)

    state = json.loads(
        (
            repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_000000123.json"
        ).read_text(encoding="utf-8")
    )
    apply_branch = state["apply"]["apply_branch"]
    assert "fake running write failure" in str(error.value)
    assert state["apply"]["state"] == "error"
    assert isinstance(apply_branch, str)
    assert apply_branch.startswith("cmoc/apply/2026-05-10_22-21_10_000000123/")
    assert _git(repo, "branch", "--list", apply_branch).stdout.strip()
    assert calls == 2


def test_apply_revalidates_ready_state_under_start_lock(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """apply fork は lock 獲得後に state を読み直して二重開始を拒否する。"""
    repo = _init_repo(tmp_path)
    _checkout_session_branch(repo)
    (repo / ".gitignore").write_text("/.cmoc/\n", encoding="utf-8")
    _git(repo, "add", ".gitignore")
    _git(repo, "commit", "-m", "ignore cmoc")
    session_id = "2026-05-10_22-21_10_000000123"
    state_path = repo / ".cmoc" / "sessions" / f"{session_id}.json"
    running_branch = (
        f"cmoc/apply/{session_id}/2026-05-10_22-22_10_000000123"
    )
    snapshot_commit = _git(repo, "rev-parse", "HEAD").stdout.strip()
    real_read_session_state = apply_module.read_session_state
    read_calls = 0

    def read_state_with_concurrent_start(
        repo_root: Path,
        requested_session_id: str,
    ) -> dict[str, object]:
        """初回検証後に別 apply が running を保存した状態を模擬する。"""
        nonlocal read_calls
        read_calls += 1
        state = real_read_session_state(repo_root, requested_session_id)
        if read_calls == 1:
            concurrent_state = json.loads(
                json.dumps(state, ensure_ascii=False),
            )
            concurrent_state["apply"] = {
                "state": "running",
                "apply_branch": running_branch,
                "oracle_snapshot_commit": snapshot_commit,
            }
            write_session_state(repo_root, requested_session_id, concurrent_state)
        return state

    monkeypatch.setattr(
        apply_module,
        "read_session_state",
        read_state_with_concurrent_start,
    )

    with pytest.raises(CmocError) as error:
        cmoc_apply_impl(repo)

    state = json.loads(state_path.read_text(encoding="utf-8"))
    branches = _git(repo, "branch", "--format=%(refname:short)").stdout
    reports = list(
        (repo / ".cmoc" / "reports" / "apply" / "fork").glob("*.md")
    )
    assert "apply run を開始できる状態ではありません" in error.value.message
    assert state["apply"] == {
        "state": "running",
        "apply_branch": running_branch,
        "oracle_snapshot_commit": snapshot_commit,
    }
    assert read_calls == 2
    assert "cmoc/apply/" not in branches
    assert not (repo / ".cmoc" / "worktrees").exists()
    assert reports == []


def test_apply_marks_error_when_worktree_creation_fails(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """apply 開始後の worktree 作成失敗は error state として残す。"""
    repo = _init_repo(tmp_path)
    _checkout_session_branch(repo)
    (repo / ".gitignore").write_text("/.cmoc/\n", encoding="utf-8")
    _git(repo, "add", ".gitignore")
    _git(repo, "commit", "-m", "ignore cmoc")

    def fail_create_apply_worktree(
        _repo_root: Path,
        _session_id: str,
        _oracle_snapshot_commit: str,
        _initial_plan: apply_module._ApplyWorktreePlan,
    ) -> apply_module._ApplyWorktreePlan:
        """worktree 作成失敗を模擬する。"""
        raise RuntimeError("fake worktree creation failure")

    monkeypatch.setattr(
        apply_module,
        "_create_apply_worktree",
        fail_create_apply_worktree,
    )

    with pytest.raises(RuntimeError) as error:
        cmoc_apply_impl(repo)

    state = json.loads(
        (
            repo / ".cmoc" / "sessions" / "2026-05-10_22-21_10_000000123.json"
        ).read_text(encoding="utf-8")
    )
    branches = _git(repo, "branch", "--format=%(refname:short)").stdout
    reports = list(
        (repo / ".cmoc" / "reports" / "apply" / "fork").glob("*.md")
    )
    captured = capsys.readouterr()
    assert "fake worktree creation failure" in str(error.value)
    assert state["apply"]["state"] == "error"
    assert state["apply"]["apply_branch"].startswith(
        "cmoc/apply/2026-05-10_22-21_10_000000123/"
    )
    assert state["apply"]["oracle_snapshot_commit"] == _git(
        repo,
        "rev-parse",
        "HEAD",
    ).stdout.strip()
    assert not (repo / ".cmoc" / "worktrees").exists()
    assert "cmoc/apply/" not in branches
    assert len(reports) == 1
    assert str(reports[0]) in captured.out
    report_text = reports[0].read_text(encoding="utf-8")
    apply_run_id_match = re.search(
        r'^cmoc_apply_run_id: "([^"]+)"$',
        report_text,
        re.MULTILINE,
    )
    assert apply_run_id_match is not None
    apply_run_id = apply_run_id_match.group(1)
    planned_apply_worktree = (
        repo
        / ".cmoc"
        / "worktrees"
        / "2026-05-10_22-21_10_000000123"
        / apply_run_id
    )
    assert f"apply_worktree_path: \"{planned_apply_worktree}\"" in report_text
    assert f"apply_worktree_path: \"{repo}\"" not in report_text

    cmoc_apply_abandon_impl(repo)

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


def test_create_apply_worktree_failure_reports_last_attempted_plan(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """worktree 作成リトライ失敗は最後に実試行した候補を例外に載せる。"""
    repo = tmp_path / "repo"
    repo.mkdir()
    session_id = "session"
    oracle_snapshot_commit = "abc123"
    initial_plan = apply_module._ApplyWorktreePlan(
        "run0",
        f"cmoc/apply/{session_id}/run0",
        repo / ".cmoc" / "worktrees" / session_id / "run0",
    )
    timestamps = iter(f"run{index}" for index in range(1, 10))
    attempted_branches: list[str] = []

    def fake_make_timestamp() -> str:
        return next(timestamps)

    def fake_run_git(
        _repo_root: Path,
        args: list[str],
        *,
        check: bool = True,
    ) -> subprocess.CompletedProcess[str]:
        del check
        if args[:1] == ["branch"]:
            attempted_branches.append(args[1])
        return subprocess.CompletedProcess(args, 1, "", "fake collision")

    monkeypatch.setattr(apply_module, "make_timestamp", fake_make_timestamp)
    monkeypatch.setattr(apply_module, "run_git", fake_run_git)
    monkeypatch.setattr(apply_module, "sleep", lambda _seconds: None)

    with pytest.raises(apply_module._ApplyWorktreeCreationError) as error:
        apply_module._create_apply_worktree(
            repo,
            session_id,
            oracle_snapshot_commit,
            initial_plan,
        )

    assert attempted_branches[0] == initial_plan.apply_branch
    assert attempted_branches[-1] == f"cmoc/apply/{session_id}/run9"
    assert error.value.last_plan.apply_run_id == "run9"
    assert error.value.last_plan.apply_branch == attempted_branches[-1]
    assert error.value.last_plan.apply_worktree == (
        repo / ".cmoc" / "worktrees" / session_id / "run9"
    )


def test_create_apply_worktree_reports_branch_cleanup_failure(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """worktree 作成後始末の branch 削除失敗は診断付きで即時失敗する。"""
    repo = tmp_path / "repo"
    repo.mkdir()
    session_id = "session"
    oracle_snapshot_commit = "abc123"
    initial_plan = apply_module._ApplyWorktreePlan(
        "run0",
        f"cmoc/apply/{session_id}/run0",
        repo / ".cmoc" / "worktrees" / session_id / "run0",
    )
    git_calls: list[list[str]] = []

    def fake_run_git(
        _repo_root: Path,
        args: list[str],
        *,
        check: bool = True,
    ) -> subprocess.CompletedProcess[str]:
        del check
        git_calls.append(args)
        if args[:1] == ["branch"] and args[1] != "-D":
            return subprocess.CompletedProcess(args, 0, "", "")
        if args[:2] == ["worktree", "add"]:
            return subprocess.CompletedProcess(
                args,
                1,
                "worktree stdout",
                "worktree failed",
            )
        if args[:2] == ["branch", "-D"]:
            return subprocess.CompletedProcess(
                args,
                1,
                "cleanup stdout",
                "cleanup failed",
            )
        raise AssertionError(f"unexpected git args: {args}")

    monkeypatch.setattr(apply_module, "run_git", fake_run_git)
    monkeypatch.setattr(apply_module, "sleep", lambda _seconds: None)

    with pytest.raises(apply_module._ApplyWorktreeCreationError) as error:
        apply_module._create_apply_worktree(
            repo,
            session_id,
            oracle_snapshot_commit,
            initial_plan,
        )

    assert git_calls == [
        ["branch", initial_plan.apply_branch, oracle_snapshot_commit],
        [
            "worktree",
            "add",
            str(initial_plan.apply_worktree),
            initial_plan.apply_branch,
        ],
        ["branch", "-D", initial_plan.apply_branch],
    ]
    assert error.value.last_plan == initial_plan
    message = str(error.value)
    assert "branch cleanup に失敗しました" in message
    assert f"apply_branch: {initial_plan.apply_branch}" in message
    assert f"apply_worktree: {initial_plan.apply_worktree}" in message
    assert "worktree failed" in message
    assert "cleanup failed" in message


def test_apply_commits_untracked_oracle_changes_after_cmoc_guarantee(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """未追跡 oracle 差分は自動 commit せず precondition failure にする。"""
    repo = _init_repo(tmp_path)
    _checkout_session_branch(repo)
    cmoc_log = repo / ".cmoc" / "logs" / "poll.log"
    cmoc_log.parent.mkdir(parents=True)
    cmoc_log.write_text("local log\n", encoding="utf-8")
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    (oracle_root / "spec.md").write_text("spec\n", encoding="utf-8")

    monkeypatch.setattr(
        "sub_commands.apply.fork.maintain_indexes",
        lambda repo_root: False,
    )

    def fake_codex(*args: object, **kwargs: object) -> str:
        """調査なら不整合なし JSON、レポートなら Markdown を返す。"""
        if kwargs.get("expect_json") is True:
            return '{"git_head_commit_hash": null, "fixing_points": []}'
        return "\n".join(
            [
                "## 作業結果",
                "収束",
                "## 不整合件数の推移",
                "1 回目: 0 件",
                "## ブランチ cmoc/session/2026-05-10_22-21_10_000000123 上の全変更内容",
                "カテゴリ: oracle 整備",
            ]
        )

    monkeypatch.setattr("sub_commands.apply.fork.run_codex_exec", fake_codex)

    with pytest.raises(CmocError) as error:
        cmoc_apply_impl(repo)

    assert "未コミットの変更" in error.value.message
    assert str(oracle_root.resolve()) in error.value.detail
    assert _git(repo, "log", "-1", "--pretty=%s").stdout.strip() == "initial"
    assert _git(repo, "status", "--porcelain", "--", "oracles").stdout == (
        "?? oracles/\n"
    )
    assert _git(repo, "status", "--porcelain", "--", ".cmoc").stdout == ""


def test_apply_commits_preexisting_staged_oracles_after_cmoc_guarantee(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """事前 stage 済み oracle 差分も自動 commit せず拒否する。"""
    repo = _init_repo(tmp_path)
    _checkout_session_branch(repo)
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    (oracle_root / "spec.md").write_text("spec\n", encoding="utf-8")
    _git(repo, "add", "oracles/spec.md")

    monkeypatch.setattr(
        "sub_commands.apply.fork.maintain_indexes",
        lambda repo_root: False,
    )

    def fake_codex(*args: object, **kwargs: object) -> str:
        """調査なら不整合なし JSON、レポートなら Markdown を返す。"""
        if kwargs.get("expect_json") is True:
            return '{"git_head_commit_hash": null, "fixing_points": []}'
        return "\n".join(
            [
                "## 作業結果",
                "収束",
                "## 不整合件数の推移",
                "1 回目: 0 件",
                "## ブランチ cmoc/session/2026-05-10_22-21_10_000000123 上の全変更内容",
                "カテゴリ: oracle 整備",
            ]
        )

    monkeypatch.setattr("sub_commands.apply.fork.run_codex_exec", fake_codex)

    with pytest.raises(CmocError) as error:
        cmoc_apply_impl(repo)

    assert "未コミットの変更" in error.value.message
    assert "oracles/spec.md" in error.value.detail
    assert _git(repo, "log", "-1", "--pretty=%s").stdout.strip() == "initial"
    assert _git(repo, "status", "--porcelain", "--", "oracles").stdout == (
        "A  oracles/spec.md\n"
    )


def test_commit_all_changes_allows_oracles_index_after_index_update(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """INDEX メンテナンス後の oracles/INDEX.md 差分は commit できる。"""
    repo = _init_repo(tmp_path)
    (repo / "app.py").write_text("changed\n", encoding="utf-8")

    def fake_maintain_indexes(repo_root: Path) -> bool:
        """INDEX メンテナンス時に oracle INDEX 差分を作る fake。"""
        oracle_index = repo_root / "oracles" / "INDEX.md"
        oracle_index.parent.mkdir()
        oracle_index.write_text("index\n", encoding="utf-8")
        return True

    monkeypatch.setattr(
        "sub_commands.apply.fork.maintain_indexes",
        fake_maintain_indexes,
    )
    monkeypatch.setattr(
        "sub_commands.apply.fork.run_codex_exec",
        lambda *args, **kwargs: "maintain indexes",
    )

    _commit_all_changes(repo)

    assert (repo / "oracles" / "INDEX.md").read_text(encoding="utf-8") == (
        "index\n"
    )
    assert _git(repo, "log", "-1", "--pretty=%s").stdout.strip() == (
        "maintain indexes"
    )
    assert _git(repo, "status", "--porcelain").stdout == ""
    committed_paths = _git(repo, "show", "--name-only", "--pretty=").stdout
    assert "app.py" in committed_paths
    assert "oracles/INDEX.md" in committed_paths


def test_commit_all_changes_allows_committed_maintained_oracles_index(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """INDEX メンテナンス自身の oracles/INDEX.md commit は許可する。"""
    repo = _init_repo(tmp_path)
    (repo / "app.py").write_text("changed\n", encoding="utf-8")

    def fake_maintain_indexes(repo_root: Path) -> bool:
        """INDEX メンテナンスが oracle INDEX を自動 commit する状況を模擬する。"""
        oracle_index = repo_root / "oracles" / "INDEX.md"
        oracle_index.parent.mkdir()
        oracle_index.write_text("index\n", encoding="utf-8")
        _git(repo_root, "add", "oracles/INDEX.md")
        _git(repo_root, "commit", "-m", "Maintain INDEX.md files")
        return True

    monkeypatch.setattr(
        "sub_commands.apply.fork.maintain_indexes",
        fake_maintain_indexes,
    )
    monkeypatch.setattr(
        "sub_commands.apply.fork.run_codex_exec",
        lambda *args, **kwargs: "apply changes",
    )

    _commit_all_changes(repo)

    assert _git(repo, "log", "-1", "--pretty=%s").stdout.strip() == (
        "apply changes"
    )
    assert _git(repo, "log", "-2", "--pretty=%s").stdout.splitlines() == [
        "apply changes",
        "Maintain INDEX.md files",
    ]
    assert _git(repo, "status", "--porcelain").stdout == ""


def test_forbidden_path_check_rejects_reverted_oracles_change_in_commit_range(
    tmp_path: Path,
) -> None:
    """最終差分が空でも、範囲内の oracle 変更 commit は拒否する。"""
    repo = _init_repo(tmp_path)
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    (oracle_root / "spec.md").write_text("spec\n", encoding="utf-8")
    _git(repo, "add", "oracles/spec.md")
    _git(repo, "commit", "-m", "add oracle")
    before_commit = _git(repo, "rev-parse", "HEAD").stdout.strip()

    (oracle_root / "spec.md").write_text("changed\n", encoding="utf-8")
    _git(repo, "add", "oracles/spec.md")
    _git(repo, "commit", "-m", "change oracle")
    (oracle_root / "spec.md").write_text("spec\n", encoding="utf-8")
    _git(repo, "add", "oracles/spec.md")
    _git(repo, "commit", "-m", "revert oracle")

    assert (
        _git(repo, "diff", "--name-only", f"{before_commit}..HEAD").stdout == ""
    )
    assert apply_module._changed_paths_since_for_forbidden_check(
        repo,
        before_commit,
    ) == ["oracles/spec.md", "oracles/spec.md"]
    with pytest.raises(CmocError) as error:
        apply_module._assert_forbidden_paths_unchanged_since(repo, before_commit)

    assert "編集禁止パス" in error.value.message
    assert "oracles/spec.md" in error.value.detail


def test_apply_index_maintenance_does_not_exclude_oracles_root(
    tmp_path: Path,
) -> None:
    """apply worktree の INDEX メンテナンスは oracles 配下も対象にする。"""
    repo = _init_repo(tmp_path)

    assert _apply_index_excluded_roots(repo) == []


def test_maintain_apply_indexes_updates_stale_oracles_index(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """apply 用 INDEX メンテナンスは既存 oracles/INDEX.md も更新する。"""
    repo = _init_repo(tmp_path)
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    (oracle_root / "spec.md").write_text("spec\n", encoding="utf-8")
    (oracle_root / "INDEX.md").write_text("manual oracle index\n", encoding="utf-8")

    def fake_codex(*args: object, **kwargs: object) -> str:
        """INDEX 生成用の最小 Structured Output を返す。"""
        return json.dumps(
            {
                "summary": ["summary"],
                "read_this_when": ["read"],
                "do_not_read_this_when": ["skip"],
            }
        )

    monkeypatch.setattr("commons.indexing.run_codex_exec", fake_codex)

    changed = apply_module._maintain_apply_indexes(repo)

    assert changed is True
    assert (oracle_root / "INDEX.md").read_text(encoding="utf-8") != (
        "manual oracle index\n"
    )
    assert "# `spec.md`" in (oracle_root / "INDEX.md").read_text(
        encoding="utf-8"
    )
    assert "oracles/INDEX.md" in _git(
        repo,
        "show",
        "--name-only",
        "--pretty=",
    ).stdout


def test_maintain_apply_indexes_creates_missing_oracles_index(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """apply は欠落した oracles/INDEX.md を作成する。"""
    repo = _init_repo(tmp_path)
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    (oracle_root / "spec.md").write_text("spec\n", encoding="utf-8")

    def fake_codex(*args: object, **kwargs: object) -> str:
        """INDEX 生成用の最小 Structured Output を返す。"""
        return json.dumps(
            {
                "summary": ["summary"],
                "read_this_when": ["read"],
                "do_not_read_this_when": ["skip"],
            }
        )

    monkeypatch.setattr("commons.indexing.run_codex_exec", fake_codex)

    changed = apply_module._maintain_apply_indexes(repo)

    assert changed is True
    assert (oracle_root / "INDEX.md").exists()
    assert "# `spec.md`" in (oracle_root / "INDEX.md").read_text(
        encoding="utf-8"
    )
    assert "oracles/INDEX.md" in _git(
        repo,
        "show",
        "--name-only",
        "--pretty=",
    ).stdout


def test_maintain_apply_indexes_updates_stale_nested_oracles_index(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """apply は stale な oracles 配下サブディレクトリの INDEX.md も更新する。"""
    repo = _init_repo(tmp_path)
    oracle_root = repo / "oracles"
    nested_root = oracle_root / "docs"
    nested_root.mkdir(parents=True)
    (nested_root / "spec.md").write_text("spec\n", encoding="utf-8")
    (nested_root / "INDEX.md").write_text(
        "manual oracle index\n",
        encoding="utf-8",
    )

    def fake_codex(*args: object, **kwargs: object) -> str:
        """INDEX 生成用の最小 Structured Output を返す。"""
        return json.dumps(
            {
                "summary": ["summary"],
                "read_this_when": ["read"],
                "do_not_read_this_when": ["skip"],
            }
        )

    monkeypatch.setattr("commons.indexing.run_codex_exec", fake_codex)

    changed = apply_module._maintain_apply_indexes(repo)

    assert changed is True
    assert (nested_root / "INDEX.md").read_text(encoding="utf-8") != (
        "manual oracle index\n"
    )
    assert "# `spec.md`" in (nested_root / "INDEX.md").read_text(
        encoding="utf-8"
    )


def test_commit_all_changes_rejects_oracle_file_after_index_update(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """INDEX メンテナンス後も oracle ファイル差分は commit 前に止める。"""
    repo = _init_repo(tmp_path)
    (repo / "app.py").write_text("changed\n", encoding="utf-8")

    def fake_maintain_indexes(repo_root: Path) -> bool:
        """INDEX メンテナンス時に oracle ファイル差分を作る fake。"""
        oracle_file = repo_root / "oracles" / "spec.md"
        oracle_file.parent.mkdir()
        oracle_file.write_text("forbidden\n", encoding="utf-8")
        return True

    monkeypatch.setattr(
        "sub_commands.apply.fork.maintain_indexes",
        fake_maintain_indexes,
    )

    with pytest.raises(CmocError) as error:
        _commit_all_changes(repo)

    assert "編集禁止パス" in error.value.message
    assert "oracles/spec.md" in error.value.detail
    assert _git(repo, "status", "--porcelain").stdout


def test_apply_implementation_files_at_commit_matches_implementation_files(
    tmp_path: Path,
) -> None:
    """apply の snapshot 調査対象は root memo を含めない。"""
    repo = _init_repo(tmp_path)
    (repo / ".gitignore").write_text("/.cmoc/\n", encoding="utf-8")
    memo_root = repo / "memo"
    memo_root.mkdir()
    (memo_root / "note.md").write_text("memo\n", encoding="utf-8")
    (repo / "AGENTS.md").write_text("agents\n", encoding="utf-8")
    agents_root = repo / ".agents"
    agents_root.mkdir()
    (agents_root / "skill.md").write_text("skill\n", encoding="utf-8")
    nested_memo = repo / "docs" / "memo"
    nested_memo.mkdir(parents=True)
    (nested_memo / "note.md").write_text("note\n", encoding="utf-8")
    (repo / "app.py").write_text("app\n", encoding="utf-8")
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "implementation targets")
    commit_hash = _git(repo, "rev-parse", "HEAD").stdout.strip()

    relative_paths = [
        path.relative_to(repo).as_posix()
        for path in apply_module._implementation_files_at_commit(
            repo,
            commit_hash,
        )
    ]

    assert relative_paths == [
        ".agents/skill.md",
        ".gitignore",
        "AGENTS.md",
        "README.md",
        "app.py",
        "docs/memo/note.md",
    ]


def test_apply_files_at_commit_exclude_tracked_root_gitignored_files(
    tmp_path: Path,
) -> None:
    """apply の snapshot 調査対象は tracked でも root .gitignore 対象を含めない。"""
    repo = _init_repo(tmp_path)
    (repo / ".gitignore").write_text(
        "oracles/ignored.md\nignored.py\n",
        encoding="utf-8",
    )
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    (oracle_root / "kept.md").write_text("kept\n", encoding="utf-8")
    (oracle_root / "ignored.md").write_text("ignored\n", encoding="utf-8")
    (repo / "kept.py").write_text("kept\n", encoding="utf-8")
    (repo / "ignored.py").write_text("ignored\n", encoding="utf-8")
    _git(repo, "add", ".gitignore", "oracles/kept.md", "kept.py")
    _git(repo, "add", "-f", "oracles/ignored.md", "ignored.py")
    _git(repo, "commit", "-m", "snapshot targets")
    commit_hash = _git(repo, "rev-parse", "HEAD").stdout.strip()

    oracle_paths = [
        path.relative_to(repo).as_posix()
        for path in apply_module._oracle_files_at_commit(repo, commit_hash)
    ]
    implementation_paths = [
        path.relative_to(repo).as_posix()
        for path in apply_module._implementation_files_at_commit(
            repo,
            commit_hash,
        )
    ]

    assert oracle_paths == ["oracles/kept.md"]
    assert implementation_paths == [".gitignore", "README.md", "kept.py"]


def test_apply_files_at_commit_use_snapshot_root_gitignore(
    tmp_path: Path,
) -> None:
    """snapshot 調査対象は現在の worktree ではなく snapshot の .gitignore で絞る。"""
    repo = _init_repo(tmp_path)
    base_commit = _git(repo, "rev-parse", "HEAD").stdout.strip()
    (repo / ".gitignore").write_text(
        "oracles/snapshot_ignored.md\nsnapshot_ignored.py\n",
        encoding="utf-8",
    )
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    (oracle_root / "kept.md").write_text("kept\n", encoding="utf-8")
    (oracle_root / "snapshot_ignored.md").write_text(
        "snapshot ignored\n",
        encoding="utf-8",
    )
    (oracle_root / "worktree_ignored.md").write_text(
        "worktree ignored\n",
        encoding="utf-8",
    )
    (repo / "kept.py").write_text("kept\n", encoding="utf-8")
    (repo / "snapshot_ignored.py").write_text(
        "snapshot ignored\n",
        encoding="utf-8",
    )
    (repo / "worktree_ignored.py").write_text(
        "worktree ignored\n",
        encoding="utf-8",
    )
    _git(
        repo,
        "add",
        ".gitignore",
        "oracles/kept.md",
        "oracles/worktree_ignored.md",
        "kept.py",
        "worktree_ignored.py",
    )
    _git(
        repo,
        "add",
        "-f",
        "oracles/snapshot_ignored.md",
        "snapshot_ignored.py",
    )
    _git(repo, "commit", "-m", "snapshot targets")
    snapshot_commit = _git(repo, "rev-parse", "HEAD").stdout.strip()
    (repo / ".gitignore").write_text(
        "oracles/worktree_ignored.md\nworktree_ignored.py\n",
        encoding="utf-8",
    )

    oracle_paths = [
        path.relative_to(repo).as_posix()
        for path in apply_module._oracle_files_at_commit(
            repo,
            snapshot_commit,
        )
    ]
    implementation_paths = [
        path.relative_to(repo).as_posix()
        for path in apply_module._implementation_files_at_commit(
            repo,
            snapshot_commit,
        )
    ]
    changed_oracle_paths = [
        path.relative_to(repo).as_posix()
        for path in apply_module._changed_oracle_files_at_commit(
            repo,
            base_commit,
            snapshot_commit,
        )
    ]
    changed_implementation_paths = [
        path.relative_to(repo).as_posix()
        for path in apply_module._changed_implementation_files_at_commit(
            repo,
            base_commit,
            snapshot_commit,
        )
    ]

    assert oracle_paths == [
        "oracles/kept.md",
        "oracles/worktree_ignored.md",
    ]
    assert implementation_paths == [
        ".gitignore",
        "README.md",
        "kept.py",
        "worktree_ignored.py",
    ]
    assert changed_oracle_paths == [
        "oracles/kept.md",
        "oracles/worktree_ignored.md",
    ]
    assert changed_implementation_paths == [
        ".gitignore",
        "kept.py",
        "worktree_ignored.py",
    ]


def test_apply_partial_targets_exclude_tracked_root_gitignored_files(
    tmp_path: Path,
) -> None:
    """部分 apply の変更調査対象は tracked でも root .gitignore 対象を含めない。"""
    repo = _init_repo(tmp_path)
    (repo / ".gitignore").write_text(
        "oracles/ignored.md\nignored.py\n",
        encoding="utf-8",
    )
    _git(repo, "add", ".gitignore")
    _git(repo, "commit", "-m", "base ignore rules")
    _checkout_session_branch(repo)
    base_commit = _git(repo, "rev-parse", "HEAD").stdout.strip()

    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    (oracle_root / "kept.md").write_text("kept\n", encoding="utf-8")
    (oracle_root / "ignored.md").write_text("ignored\n", encoding="utf-8")
    (repo / "kept.py").write_text("kept\n", encoding="utf-8")
    (repo / "ignored.py").write_text("ignored\n", encoding="utf-8")
    _git(repo, "add", "oracles/kept.md", "kept.py")
    _git(repo, "add", "-f", "oracles/ignored.md", "ignored.py")
    _git(repo, "commit", "-m", "change targets")
    snapshot_commit = _git(repo, "rev-parse", "HEAD").stdout.strip()

    oracle_targets = [
        target.path.relative_to(repo).as_posix()
        for target in apply_module._target_oracle_files(
            repo,
            base_commit,
            snapshot_commit,
            partial=True,
        )
    ]
    implementation_targets = [
        target.path.relative_to(repo).as_posix()
        for target in apply_module._target_implementation_files(
            repo,
            base_commit,
            snapshot_commit,
            partial=True,
        )
    ]

    assert oracle_targets == ["oracles/kept.md"]
    assert implementation_targets == ["kept.py"]


def test_apply_partial_targets_exclude_deleted_and_keep_reverted_paths(
    tmp_path: Path,
) -> None:
    """部分 apply は削除済みを除外し、存在する履歴変更 path は対象にする。"""
    repo = _init_repo(tmp_path)
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    (oracle_root / "spec.md").write_text("spec\n", encoding="utf-8")
    (oracle_root / "obsolete.md").write_text("obsolete\n", encoding="utf-8")
    (repo / "app.py").write_text("app\n", encoding="utf-8")
    (repo / "obsolete.py").write_text("obsolete\n", encoding="utf-8")
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "base targets")
    _checkout_session_branch(repo)
    base_commit = _git(repo, "rev-parse", "HEAD").stdout.strip()

    (repo / "app.py").write_text("changed\n", encoding="utf-8")
    (oracle_root / "spec.md").write_text("changed\n", encoding="utf-8")
    _git(repo, "add", "app.py", "oracles/spec.md")
    _git(repo, "commit", "-m", "change then revert targets")

    (repo / "app.py").write_text("app\n", encoding="utf-8")
    (oracle_root / "spec.md").write_text("spec\n", encoding="utf-8")
    _git(repo, "add", "app.py", "oracles/spec.md")
    _git(repo, "commit", "-m", "revert targets")

    (repo / "obsolete.py").unlink()
    (oracle_root / "obsolete.md").unlink()
    _git(repo, "rm", "obsolete.py", "oracles/obsolete.md")
    _git(repo, "commit", "-m", "delete targets")
    snapshot_commit = _git(repo, "rev-parse", "HEAD").stdout.strip()

    oracle_targets = {
        target.path.relative_to(repo).as_posix(): target.deleted_at_snapshot
        for target in apply_module._target_oracle_files(
            repo,
            base_commit,
            snapshot_commit,
            partial=True,
        )
    }
    implementation_targets = {
        target.path.relative_to(repo).as_posix(): target.deleted_at_snapshot
        for target in apply_module._target_implementation_files(
            repo,
            base_commit,
            snapshot_commit,
            partial=True,
        )
    }

    assert oracle_targets == {"oracles/spec.md": False}
    assert implementation_targets == {"app.py": False}


def test_apply_dirty_targets_record_snapshot_and_worktree_existence(
    tmp_path: Path,
) -> None:
    """dirty path は snapshot/worktree の存在状態を分けて対象化する。"""
    repo = _init_repo(tmp_path)
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    (oracle_root / "spec.md").write_text("spec\n", encoding="utf-8")
    (repo / "app.py").write_text("app\n", encoding="utf-8")
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "base targets")
    snapshot_commit = _git(repo, "rev-parse", "HEAD").stdout.strip()
    (oracle_root / "created.md").write_text("created\n", encoding="utf-8")
    (repo / "created.py").write_text("created\n", encoding="utf-8")
    (oracle_root / "spec.md").unlink()
    (repo / "app.py").unlink()

    oracle_targets = {
        target.path.relative_to(repo).as_posix(): (
            target.exists_at_snapshot,
            target.exists_in_worktree,
            target.deleted_at_snapshot,
        )
        for target in apply_module._target_oracle_files(
            repo,
            snapshot_commit,
            snapshot_commit,
            partial=True,
            dirty_paths={
                oracle_root / "created.md",
                oracle_root / "deleted.md",
                oracle_root / "spec.md",
            },
        )
    }
    implementation_targets = {
        target.path.relative_to(repo).as_posix(): (
            target.exists_at_snapshot,
            target.exists_in_worktree,
            target.deleted_at_snapshot,
        )
        for target in apply_module._target_implementation_files(
            repo,
            snapshot_commit,
            snapshot_commit,
            partial=True,
            dirty_paths={
                repo / "app.py",
                repo / "created.py",
                repo / "deleted.py",
            },
        )
    }

    assert oracle_targets == {
        "oracles/created.md": (False, True, False),
        "oracles/deleted.md": (False, False, True),
        "oracles/spec.md": (True, False, False),
    }
    assert implementation_targets == {
        "app.py": (True, False, False),
        "created.py": (False, True, False),
        "deleted.py": (False, False, True),
    }


def test_apply_dirty_changed_implementation_files_include_deleted_paths(
    tmp_path: Path,
) -> None:
    """修正後 dirty 更新用の変更実装 path は削除側 path も含める。"""
    repo = _init_repo(tmp_path)
    (repo / "app.py").write_text("app\n", encoding="utf-8")
    (repo / "obsolete.py").write_text("obsolete\n", encoding="utf-8")
    (repo / "old.py").write_text("old\n", encoding="utf-8")
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "base implementation files")
    base_commit = _git(repo, "rev-parse", "HEAD").stdout.strip()

    (repo / "app.py").write_text("changed\n", encoding="utf-8")
    _git(repo, "rm", "obsolete.py")
    _git(repo, "mv", "old.py", "new.py")
    _git(repo, "add", "app.py")
    _git(repo, "commit", "-m", "change delete and rename implementation files")
    head_commit = _git(repo, "rev-parse", "HEAD").stdout.strip()

    dirty_paths = sorted(
        path.relative_to(repo).as_posix()
        for path in apply_module._changed_implementation_files_since(
            repo,
            base_commit,
            head_commit,
        )
    )

    assert dirty_paths == [
        "app.py",
        "new.py",
        "obsolete.py",
        "old.py",
    ]


def test_apply_partial_targets_use_renamed_new_paths(
    tmp_path: Path,
) -> None:
    """部分 apply の rename 調査対象は rename 後 path だけにする。"""
    repo = _init_repo(tmp_path)
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    (oracle_root / "old.md").write_text("oracle\n", encoding="utf-8")
    (repo / "old.py").write_text("app\n", encoding="utf-8")
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "base targets")
    _checkout_session_branch(repo)
    base_commit = _git(repo, "rev-parse", "HEAD").stdout.strip()

    _git(repo, "mv", "oracles/old.md", "oracles/new.md")
    _git(repo, "mv", "old.py", "new.py")
    _git(repo, "commit", "-m", "rename targets")
    snapshot_commit = _git(repo, "rev-parse", "HEAD").stdout.strip()

    oracle_targets = [
        target.path.relative_to(repo).as_posix()
        for target in apply_module._target_oracle_files(
            repo,
            base_commit,
            snapshot_commit,
            partial=True,
        )
    ]
    implementation_targets = [
        target.path.relative_to(repo).as_posix()
        for target in apply_module._target_implementation_files(
            repo,
            base_commit,
            snapshot_commit,
            partial=True,
        )
    ]

    assert oracle_targets == ["oracles/new.md"]
    assert implementation_targets == ["new.py"]


def test_apply_partial_targets_preserve_special_path_tokens(
    tmp_path: Path,
) -> None:
    """部分 apply の調査対象 path は newline や前後空白を保持する。"""
    repo = _init_repo(tmp_path)
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    old_oracle = oracle_root / "old\nspec.md"
    old_impl = repo / "old\nimpl.py"
    old_oracle.write_text("oracle\n", encoding="utf-8")
    old_impl.write_text("app\n", encoding="utf-8")
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "base targets")
    _checkout_session_branch(repo)
    base_commit = _git(repo, "rev-parse", "HEAD").stdout.strip()

    _git(repo, "mv", "oracles/old\nspec.md", "oracles/ new\nspec.md ")
    _git(repo, "mv", "old\nimpl.py", " new\nimpl.py ")
    _git(repo, "commit", "-m", "rename special targets")
    snapshot_commit = _git(repo, "rev-parse", "HEAD").stdout.strip()

    oracle_targets = [
        target.path.relative_to(repo).as_posix()
        for target in apply_module._target_oracle_files(
            repo,
            base_commit,
            snapshot_commit,
            partial=True,
        )
    ]
    implementation_targets = [
        target.path.relative_to(repo).as_posix()
        for target in apply_module._target_implementation_files(
            repo,
            base_commit,
            snapshot_commit,
            partial=True,
        )
    ]

    assert oracle_targets == ["oracles/ new\nspec.md "]
    assert implementation_targets == [" new\nimpl.py "]


def test_apply_deleted_investigation_target_prompt_mentions_history(
    tmp_path: Path,
) -> None:
    """削除済み調査起点は存在しない path として履歴確認を促す。"""
    repo = _init_repo(tmp_path)
    target = apply_module._InvestigationTarget(
        repo / "deleted.py",
        exists_at_snapshot=False,
        exists_in_worktree=False,
    )

    prompt = apply_module._implementation_investigation_prompt(repo, target)

    assert "`" + str(repo / "deleted.py") + "` を起点" in prompt
    assert "調査対象として固定された commit 時点では存在しません" in prompt
    assert "削除差分や履歴上の変更内容" in prompt


def test_apply_oracle_investigation_prompt_orders_completion_before_details() -> None:
    """oracle 起点調査 prompt はロール、作業、完了条件、詳細指示の順にする。"""
    repo = Path("/repo")
    target = apply_module._InvestigationTarget(
        repo / "oracles/spec.md",
        exists_at_snapshot=True,
        exists_in_worktree=True,
    )

    prompt = apply_module._investigation_prompt(repo, target)
    lines = prompt.splitlines()

    assert lines[0] == "あなたはソフトウェア実装の監査担当です。"
    assert lines[1] == "`/repo/oracles/spec.md` を起点に `/repo` の要修正点を調査してください。"
    assert lines[2] == (
        "完了条件は、指定された Structured Output schema に一致する JSON だけを返すことです。"
    )
    assert (
        lines.index(
            "この起点 path は調査対象として固定された commit 時点に存在するファイルです。"
        )
        > 2
    )


def test_apply_implementation_investigation_prompt_orders_completion_before_details() -> None:
    """実装起点調査 prompt はロール、作業、完了条件、詳細指示の順にする。"""
    repo = Path("/repo")
    target = apply_module._InvestigationTarget(
        repo / "src/app.py",
        exists_at_snapshot=False,
        exists_in_worktree=False,
    )

    prompt = apply_module._implementation_investigation_prompt(repo, target)
    lines = prompt.splitlines()

    assert lines[0] == "あなたはソフトウェア実装の監査担当です。"
    assert lines[1] == "`/repo/src/app.py` を起点に、"
    assert lines[2] == "`/repo` の要修正点を調査してください。"
    assert lines[3] == (
        "完了条件は、指定された Structured Output schema に一致する JSON だけを返すことです。"
    )
    assert lines.index(
        "この起点 path は調査対象として固定された commit 時点では存在しません。"
        "削除差分や履歴上の変更内容を確認して調査してください。"
    ) > 3


def test_apply_created_dirty_investigation_target_prompt_mentions_worktree_content(
    tmp_path: Path,
) -> None:
    """新規作成 dirty 起点は現在 worktree の内容確認を促す。"""
    repo = _init_repo(tmp_path)
    target = apply_module._InvestigationTarget(
        repo / "created.py",
        exists_at_snapshot=False,
        exists_in_worktree=True,
    )

    prompt = apply_module._implementation_investigation_prompt(repo, target)

    assert "`" + str(repo / "created.py") + "` を起点" in prompt
    assert "調査対象として固定された commit 時点では存在せず" in prompt
    assert "現在の worktree には存在します" in prompt
    assert "前回までの修正で新規作成されたファイル" in prompt
    assert "現在の worktree の内容を確認" in prompt
    assert "削除差分や履歴上の変更内容" not in prompt


def test_apply_removed_dirty_investigation_target_prompt_mentions_deletion_diff(
    tmp_path: Path,
) -> None:
    """削除された dirty 起点は snapshot 上の存在と削除差分確認を伝える。"""
    repo = _init_repo(tmp_path)
    target = apply_module._InvestigationTarget(
        repo / "removed.py",
        exists_at_snapshot=True,
        exists_in_worktree=False,
    )

    prompt = apply_module._implementation_investigation_prompt(repo, target)

    assert "`" + str(repo / "removed.py") + "` を起点" in prompt
    assert "調査対象として固定された commit 時点には存在し" in prompt
    assert "現在の worktree には存在しません" in prompt
    assert "前回までの修正で削除されたファイル" in prompt
    assert "削除差分や履歴上の変更内容" in prompt


def test_commit_all_changes_rejects_memo_changes(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """workspace-write prompt の読み書き禁止領域 memo は commit 前に検出する。"""
    repo = _init_repo(tmp_path)
    memo_root = repo / "memo"
    memo_root.mkdir()
    (memo_root / "note.md").write_text("memo\n", encoding="utf-8")
    (repo / "app.py").write_text("changed\n", encoding="utf-8")
    monkeypatch.setattr(
        "sub_commands.apply.fork.maintain_indexes",
        lambda repo_root: False,
    )

    with pytest.raises(CmocError) as error:
        _commit_all_changes(repo)

    assert "編集禁止パス" in error.value.message
    assert "memo/" in error.value.detail
    assert _git(repo, "log", "-1", "--pretty=%s").stdout.strip() == "initial"


@pytest.mark.parametrize(
    "forbidden_file",
    [".cmoc/state.json", "README.md", "AGENTS.md"],
)
def test_commit_all_changes_rejects_root_forbidden_changes(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
    forbidden_file: str,
) -> None:
    """root の workspace-write 編集禁止 path 変更は commit 前に検出する。"""
    repo = _init_repo(tmp_path)
    target = repo / forbidden_file
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("tampered\n", encoding="utf-8")
    (repo / "app.py").write_text("changed\n", encoding="utf-8")
    monkeypatch.setattr(
        "sub_commands.apply.fork.maintain_indexes",
        lambda repo_root: False,
    )

    with pytest.raises(CmocError) as error:
        _commit_all_changes(repo)

    assert "編集禁止パス" in error.value.message
    if forbidden_file.startswith(".cmoc/"):
        assert ".cmoc/" in error.value.detail
    else:
        assert forbidden_file in error.value.detail
    assert _git(repo, "log", "-1", "--pretty=%s").stdout.strip() == "initial"


@pytest.mark.parametrize(
    ("relative_path", "content"),
    [
        ("README.md", "changed readme\n"),
        ("AGENTS.md", "changed agents\n"),
    ],
)
def test_commit_all_changes_rejects_root_doc_implementation_changes(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
    relative_path: str,
    content: str,
) -> None:
    """root の README/AGENTS 変更は apply 実装差分として commit しない。"""
    repo = _init_repo(tmp_path)
    target = repo / relative_path
    target.write_text(content, encoding="utf-8")
    monkeypatch.setattr(
        "sub_commands.apply.fork.maintain_indexes",
        lambda repo_root: False,
    )
    monkeypatch.setattr(
        "sub_commands.apply.fork.run_codex_exec",
        lambda *args, **kwargs: "Apply root doc implementation change",
    )

    with pytest.raises(CmocError) as error:
        _commit_all_changes(repo)

    assert "編集禁止パス" in error.value.message
    assert relative_path in error.value.detail
    assert _git(repo, "log", "-1", "--pretty=%s").stdout.strip() == "initial"
    assert target.read_text(encoding="utf-8") == content


def test_apply_discrepancies_rejects_committed_forbidden_change(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """Codex CLI が commit 済みにした禁止 path 差分も検出する。"""
    repo = _init_repo(tmp_path)
    (repo / "app.py").write_text("base\n", encoding="utf-8")
    _git(repo, "add", "app.py")
    _git(repo, "commit", "-m", "add app")
    monkeypatch.setattr(
        "sub_commands.apply.fork.maintain_indexes",
        lambda repo_root: False,
    )

    def fake_codex(repo_root: Path, *args: object, **kwargs: object) -> str:
        """workspace-write Codex 実行中の禁止 path commit を模擬する。"""
        target = repo_root / ".agents" / "skill.md"
        target.parent.mkdir()
        target.write_text("forbidden\n", encoding="utf-8")
        _git(repo_root, "add", ".agents/skill.md")
        _git(repo_root, "commit", "-m", "commit forbidden path")
        return ""

    monkeypatch.setattr(
        "sub_commands.apply.fork.run_codex_exec",
        fake_codex,
    )

    with pytest.raises(CmocError) as error:
        apply_module._apply_discrepancies(
            repo,
            [
                {
                    "title": "fix",
                    "evidences": [],
                    "oracle_requirement": "requirement",
                    "observed_implementation": "observed",
                    "reason": "reason",
                    "suggested_fix": "suggested",
                }
            ],
            timer=StepTimer("test"),
            step_path=((1, 1),),
        )

    assert "編集禁止パス" in error.value.message
    assert ".agents/skill.md" in error.value.detail
    assert _git(repo, "log", "-1", "--pretty=%s").stdout.strip() == (
        "commit forbidden path"
    )


def test_apply_parallel_investigation_records_worker_codex_events(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """並列 file 起点調査の worker 内 Codex 呼び出しもサブコマンド JSONL に残す。"""
    repo = _init_repo(tmp_path)
    oracle_path = repo / "oracles" / "docs" / "spec.md"
    implementation_path = repo / "src" / "app.py"
    oracle_path.parent.mkdir(parents=True)
    implementation_path.parent.mkdir(parents=True)
    oracle_path.write_text("# spec\n", encoding="utf-8")
    implementation_path.write_text("print('app')\n", encoding="utf-8")
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "add investigation targets")
    head = _git(repo, "rev-parse", "HEAD").stdout.strip()
    monkeypatch.setattr(
        apply_module,
        "_target_oracle_files",
        lambda *args, **kwargs: [
            apply_module._InvestigationTarget(oracle_path),
        ],
    )
    monkeypatch.setattr(
        apply_module,
        "_target_implementation_files",
        lambda *args, **kwargs: [
            apply_module._InvestigationTarget(implementation_path),
        ],
    )

    def fake_codex(
        repo_root: Path,
        prompt: str,
        *,
        purpose: str,
        **kwargs: object,
    ) -> str:
        """run_codex_exec の完了通知と同じイベントだけを worker thread で記録する。"""
        log_event(
            "codex_exec_call",
            {
                "purpose": purpose,
                "log_path": str(
                    repo_root / ".cmoc" / "logs" / "codex_exec" / "fake.log"
                ),
                "elapsed_seconds": 0.1,
                "returncode": 0,
            },
        )
        return json.dumps({"git_head_commit_hash": None, "fixing_points": []})

    monkeypatch.setattr(apply_module, "run_codex_exec", fake_codex)

    with subcommand_log(repo):
        result = apply_module._investigate_discrepancies(
            repo,
            head,
            head,
            timer=StepTimer("test"),
            step_path=((1, 1),),
            repeat_improove_fixing_list=0,
            scope="full",
        )

    log_file = next((repo / ".cmoc" / "logs" / "sub_commands").glob("*.jsonl"))
    events = [
        json.loads(line)
        for line in log_file.read_text(encoding="utf-8").splitlines()
    ]
    codex_events = [
        event for event in events if event["event"] == "codex_exec_call"
    ]
    assert result == []
    assert sorted(event["purpose"] for event in codex_events) == [
        "oracle 調査 oracles/docs/spec.md",
        "実装調査 src/app.py",
    ]


def test_apply_discrepancy_schema_rejects_incomplete_items() -> None:
    """不整合調査 JSON は仕様 schema の必須項目不足を意味的失敗として扱う。"""
    with pytest.raises(ValueError):
        _validate_discrepancy_payload(
            {
                "git_head_commit_hash": None,
                "fixing_points": [
                    {
                        "title": "missing fields",
                    }
                ]
            }
        )


def test_apply_discrepancy_schema_requires_git_head_commit_hash() -> None:
    """不整合調査 JSON は top-level の HEAD hash key 欠落を拒否する。"""
    assert set(_DISCREPANCY_OUTPUT_SCHEMA["required"]) == {
        "git_head_commit_hash",
        "fixing_points",
    }

    with pytest.raises(ValueError, match="git_head_commit_hash"):
        _validate_discrepancy_payload({"fixing_points": []})


def test_apply_discrepancy_schema_accepts_fixing_points() -> None:
    """要修正点 JSON は fixing_points と evidences 形式を受け付ける。"""
    _validate_discrepancy_payload(json.loads(_discrepancy_json("fix")))


def test_apply_discrepancy_schema_rejects_relative_evidence_path() -> None:
    """要修正点 JSON の evidence path は絶対パスでなければ拒否する。"""
    payload = json.loads(_discrepancy_json("fix"))
    payload["fixing_points"][0]["evidences"][0]["path"] = "oracles/spec.md"

    with pytest.raises(ValueError, match="must be an absolute path"):
        _validate_discrepancy_payload(payload)


def test_apply_discrepancy_schema_rejects_near_miss_keys() -> None:
    """似た名前のキーでも不整合調査 schema と一致しなければ拒否する。"""
    with pytest.raises(ValueError):
        _validate_discrepancy_payload(
            {
                "git_head_commit_hash": None,
                "fixing_points": [
                    {
                        "title": "near miss",
                        "evidence": [
                            {
                                "path": "/repo/src/app.py",
                                "line_start": 10,
                                "line_end": 12,
                                "summary": "summary",
                            }
                        ],
                        "expected_by_oracle": "requirement",
                        "observed_implementation": "observed",
                        "reason": "reason",
                        "suggested_fix": "fix",
                    }
                ]
            }
        )
