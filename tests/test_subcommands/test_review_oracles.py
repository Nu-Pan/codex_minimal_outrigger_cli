"""サブコマンド横断テストを意味カテゴリ別に分割したファイル。"""

from .helpers import *


def test_eval_oracles_writes_report_with_fake_codex(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """`cmoc eval-oracles --full` は oracle 評価レポートを保存する。"""
    repo = _init_repo(tmp_path)
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    (oracle_root / "spec.md").write_text("spec\n", encoding="utf-8")
    _prepare_review_oracles_session(repo)

    maintain_calls: list[Path] = []

    def fake_maintain_indexes(repo_root: Path) -> bool:
        """review oracles 冒頭の INDEX.md メンテナンスを記録する。"""
        maintain_calls.append(repo_root)
        return False

    monkeypatch.setattr(
        review_oracles_module,
        "maintain_indexes",
        fake_maintain_indexes,
    )
    codex_kwargs: list[dict[str, object]] = []

    def fake_codex(*args: object, **kwargs: object) -> str:
        """不整合なしの oracle 評価結果を返す Codex 実行を模擬する。"""
        codex_kwargs.append(kwargs)
        return json.dumps(
            {"issues": []},
            ensure_ascii=False,
        )

    monkeypatch.setattr(review_oracles_module, "run_codex_exec", fake_codex)

    cmoc_review_oracles_impl(repo, full=True, repeat_improve_issues_list=0)

    reports = list((repo / ".cmoc" / "reports" / "review_oracles").glob("*.md"))
    assert len(reports) == 1
    report = reports[0].read_text(encoding="utf-8")
    assert len(maintain_calls) == 1
    review_worktree = maintain_calls[0]
    assert review_worktree != repo
    assert review_worktree.is_dir()
    assert review_worktree.is_relative_to(repo / ".cmoc" / "worktrees")
    review_worktree_relative = review_worktree.relative_to(
        repo / ".cmoc" / "worktrees"
    )
    assert len(review_worktree_relative.parts) == 2
    assert review_worktree_relative.parts[1] != "review"
    assert _git(review_worktree, "branch", "--show-current").stdout.startswith(
        "cmoc/review/"
    )
    assert codex_kwargs[0]["expect_json"] is True
    assert codex_kwargs[0]["output_schema"] == (
        review_oracles_module._ENUMERATE_FINDINGS_OUTPUT_SCHEMA
    )
    assert codex_kwargs[0].get("skip_index_maintenance") is not True
    assert "json_validator" in codex_kwargs[0]
    assert 'scope: "full"' in report
    assert 'result: "ok"' in report
    assert "## Fatal findings" in report
    assert "## Minor findings" in report
    assert "## Rejected fatal findings" in report
    assert "## Rejected minor findings" in report
    assert "No findings." in report
    assert "## Specification-only basis" not in report


def test_review_oracles_parallel_evaluation_records_worker_codex_events(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """並列 oracle 評価の worker 内 Codex 呼び出しもサブコマンド JSONL に残す。"""
    repo = _init_repo(tmp_path)
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    for name in ["a.md", "b.md"]:
        (oracle_root / name).write_text(f"{name}\n", encoding="utf-8")
    _prepare_review_oracles_session(repo)

    monkeypatch.setattr(
        review_oracles_module,
        "maintain_indexes",
        lambda repo_root: False,
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
        return json.dumps({"issues": []}, ensure_ascii=False)

    monkeypatch.setattr(review_oracles_module, "run_codex_exec", fake_codex)

    with subcommand_log(repo):
        cmoc_review_oracles_impl(
            repo,
            full=True,
            repeat_improve_issues_list=0,
        )

    log_file = next((repo / ".cmoc" / "logs" / "sub_commands").glob("*.jsonl"))
    events = [
        json.loads(line)
        for line in log_file.read_text(encoding="utf-8").splitlines()
    ]
    codex_events = [
        event for event in events if event["event"] == "codex_exec_call"
    ]
    assert sorted(event["purpose"] for event in codex_events) == [
        "oracle 評価 oracles/a.md",
        "oracle 評価 oracles/b.md",
    ]


def test_review_oracles_runs_codex_in_review_worktree(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """review oracles の Codex 評価は session worktree ではなく review worktree で動く。"""
    repo = _init_repo(tmp_path)
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    (oracle_root / "spec.md").write_text("spec\n", encoding="utf-8")
    _prepare_review_oracles_session(repo)

    monkeypatch.setattr(
        review_oracles_module,
        "maintain_indexes",
        lambda repo_root: False,
    )
    codex_repo_roots: list[Path] = []

    def fake_codex(repo_root: Path, *args: object, **kwargs: object) -> str:
        """Codex 実行 root を記録して問題なしを返す。"""
        codex_repo_roots.append(repo_root)
        return json.dumps({"issues": []}, ensure_ascii=False)

    monkeypatch.setattr(review_oracles_module, "run_codex_exec", fake_codex)

    cmoc_review_oracles_impl(repo, full=True, repeat_improve_issues_list=0)

    assert len(codex_repo_roots) == 1
    assert codex_repo_roots[0] != repo
    assert codex_repo_roots[0].is_relative_to(repo / ".cmoc" / "worktrees")
    review_worktree_relative = codex_repo_roots[0].relative_to(
        repo / ".cmoc" / "worktrees"
    )
    assert len(review_worktree_relative.parts) == 2
    assert review_worktree_relative.parts[1] != "review"
    assert _git(codex_repo_roots[0], "branch", "--show-current").stdout.startswith(
        "cmoc/review/"
    )


def test_review_oracles_backup_snapshot_stays_in_review_worktree(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """review oracles の退避 snapshot は review worktree 内に作る。"""
    repo = _init_repo(tmp_path)
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    (oracle_root / "spec.md").write_text("spec\n", encoding="utf-8")
    _prepare_review_oracles_session(repo)

    original_create_snapshot = review_oracles_module._create_oracle_evaluation_snapshot
    snapshot_roots: list[tuple[Path, Path]] = []

    def fake_create_snapshot(
        repo_root: Path,
        oracle_files: list[Path],
        snapshot_root: Path,
        *,
        display_repo_root: Path | None = None,
    ) -> review_oracles_module._OracleEvaluationSnapshot:
        """退避 snapshot の作成先を記録してから通常処理する。"""
        snapshot_roots.append((repo_root, snapshot_root))
        return original_create_snapshot(
            repo_root,
            oracle_files,
            snapshot_root,
            display_repo_root=display_repo_root,
        )

    monkeypatch.setattr(
        review_oracles_module,
        "_create_oracle_evaluation_snapshot",
        fake_create_snapshot,
    )
    monkeypatch.setattr(
        review_oracles_module,
        "maintain_indexes",
        lambda repo_root: False,
    )
    monkeypatch.setattr(
        review_oracles_module,
        "run_codex_exec",
        lambda *args, **kwargs: json.dumps({"issues": []}, ensure_ascii=False),
    )

    cmoc_review_oracles_impl(repo, full=True, repeat_improve_issues_list=0)

    assert len(snapshot_roots) == 1
    review_worktree, snapshot_root = snapshot_roots[0]
    assert review_worktree != repo
    assert review_worktree.is_relative_to(repo / ".cmoc" / "worktrees")
    assert snapshot_root.is_relative_to(
        review_worktree / review_oracles_module._REVIEW_ORACLES_TMP_DIR
    )


def test_review_oracles_merges_review_branch_to_session(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """review branch の INDEX.md 更新は終了時に session branch へ自動 merge される。"""
    repo = _init_repo(tmp_path)
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    (oracle_root / "spec.md").write_text("spec\n", encoding="utf-8")
    (repo / "docs").mkdir()
    (repo / "docs" / "guide.md").write_text("guide\n", encoding="utf-8")
    _git(repo, "add", "oracles", "docs")
    _git(repo, "commit", "-m", "add docs and oracles")
    _prepare_review_oracles_session(repo)
    session_branch = _git(repo, "branch", "--show-current").stdout.strip()

    def fake_maintain_indexes(repo_root: Path) -> bool:
        """review worktree 側だけで INDEX.md 更新 commit を作る。"""
        (repo_root / "docs" / "INDEX.md").write_text(
            "review maintained docs index\n",
            encoding="utf-8",
        )
        _git(repo_root, "add", "docs/INDEX.md")
        _git(repo_root, "commit", "-m", "fake review index maintenance")
        return True

    monkeypatch.setattr(
        review_oracles_module,
        "maintain_indexes",
        fake_maintain_indexes,
    )
    monkeypatch.setattr(
        review_oracles_module,
        "run_codex_exec",
        lambda *args, **kwargs: json.dumps({"issues": []}, ensure_ascii=False),
    )

    cmoc_review_oracles_impl(repo, full=True, repeat_improve_issues_list=0)

    assert _git(repo, "branch", "--show-current").stdout.strip() == session_branch
    assert (repo / "docs" / "INDEX.md").read_text(encoding="utf-8") == (
        "review maintained docs index\n"
    )
    head_parents = _git(repo, "rev-list", "--parents", "-n", "1", "HEAD").stdout.split()
    assert len(head_parents) == 3
    assert "fake review index maintenance" in _git(repo, "log", "--oneline").stdout


def test_review_oracles_index_conflict_keeps_session_side(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """review branch merge の INDEX.md conflict は session branch 側を採用する。"""
    repo = _init_repo(tmp_path)
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    (oracle_root / "spec.md").write_text("spec\n", encoding="utf-8")
    docs = repo / "docs"
    docs.mkdir()
    (docs / "guide.md").write_text("guide\n", encoding="utf-8")
    (docs / "INDEX.md").write_text("base docs index\n", encoding="utf-8")
    _git(repo, "add", "oracles", "docs")
    _git(repo, "commit", "-m", "add docs index")
    _prepare_review_oracles_session(repo)

    def fake_maintain_indexes(repo_root: Path) -> bool:
        """review worktree 側の INDEX.md 更新 commit を作る。"""
        (repo_root / "docs" / "INDEX.md").write_text(
            "review docs index\n",
            encoding="utf-8",
        )
        _git(repo_root, "add", "docs/INDEX.md")
        _git(repo_root, "commit", "-m", "fake review index maintenance")
        return True

    codex_called = False

    def fake_codex(*args: object, **kwargs: object) -> str:
        """merge 前に session branch 側の同じ INDEX.md を変更済み commit にする。"""
        nonlocal codex_called
        if not codex_called:
            codex_called = True
            (repo / "docs" / "INDEX.md").write_text(
                "session docs index\n",
                encoding="utf-8",
            )
            _git(repo, "add", "docs/INDEX.md")
            _git(repo, "commit", "-m", "session index update during review")
        return json.dumps({"issues": []}, ensure_ascii=False)

    monkeypatch.setattr(
        review_oracles_module,
        "maintain_indexes",
        fake_maintain_indexes,
    )
    monkeypatch.setattr(review_oracles_module, "run_codex_exec", fake_codex)

    cmoc_review_oracles_impl(repo, full=True, repeat_improve_issues_list=0)

    assert (repo / "docs" / "INDEX.md").read_text(encoding="utf-8") == (
        "session docs index\n"
    )
    assert _git(repo, "diff", "--name-only", "--diff-filter=U").stdout == ""
    head_parents = _git(repo, "rev-list", "--parents", "-n", "1", "HEAD").stdout.split()
    assert len(head_parents) == 3


def test_eval_oracles_snapshots_oracles_with_maintained_indexes(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """評価 snapshot は開始時点本文とメンテナンス後 INDEX.md を読む。"""
    repo = _init_repo(tmp_path)
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    original_oracle = oracle_root / "original.md"
    original_oracle.write_text("original\n", encoding="utf-8")
    original_index = oracle_root / "INDEX.md"
    original_index.write_text("initial oracle index\n", encoding="utf-8")
    _git(repo, "add", "oracles")
    _git(repo, "commit", "-m", "add original oracle")
    _prepare_review_oracles_session(repo)
    branch_name = _git(repo, "branch", "--show-current").stdout.strip()
    session_fork_commit = repo_module.read_session_start_commit(repo, branch_name)
    (repo / "session-note.txt").write_text("session change\n", encoding="utf-8")
    _git(repo, "add", "session-note.txt")
    _git(repo, "commit", "-m", "add session change before review")
    review_start_head = _git(repo, "rev-parse", "HEAD").stdout.strip()
    assert session_fork_commit != review_start_head

    maintain_exclusions: list[list[str]] = []

    def fake_maintain_indexes(repo_root: Path) -> bool:
        """メンテナンス中に HEAD と oracle file set が動く状況を模擬する。"""
        maintain_exclusions.append([])
        (repo_root / "oracles" / "generated.md").write_text(
            "generated\n",
            encoding="utf-8",
        )
        (repo_root / "oracles" / "INDEX.md").write_text(
            "maintained oracle index\n",
            encoding="utf-8",
        )
        (repo_root / "INDEX.md").write_text("index\n", encoding="utf-8")
        _git(repo_root, "add", "INDEX.md", "oracles")
        _git(repo_root, "commit", "-m", "fake index maintenance")
        return True

    monkeypatch.setattr(
        review_oracles_module,
        "maintain_indexes",
        fake_maintain_indexes,
    )
    evaluated_purposes: list[str] = []
    snapshot_reads: list[tuple[str, str]] = []

    def fake_codex(*args: object, **kwargs: object) -> str:
        """固定済み oracle だけが開始時点 INDEX snapshot で評価されることを記録する。"""
        execution_repo_root = Path(args[0])
        evaluated_purposes.append(str(kwargs["purpose"]))
        prompt = str(args[1])
        index_match = re.search(
            r"`([^`]+/oracles/INDEX\.md)` から始まる INDEX\.md",
            prompt,
        )
        oracle_match = re.search(
            r"開始時点の内容を固定したコピー `([^`]+/oracles/original\.md)`",
            prompt,
        )
        assert index_match is not None
        assert oracle_match is not None
        Path(index_match.group(1)).relative_to(execution_repo_root)
        Path(oracle_match.group(1)).relative_to(execution_repo_root)
        snapshot_reads.append(
            (
                Path(oracle_match.group(1)).read_text(encoding="utf-8"),
                Path(index_match.group(1)).read_text(encoding="utf-8"),
            )
        )
        return json.dumps({"issues": []}, ensure_ascii=False)

    monkeypatch.setattr(review_oracles_module, "run_codex_exec", fake_codex)

    cmoc_review_oracles_impl(repo, full=True, repeat_improve_issues_list=0)

    report = next(
        (repo / ".cmoc" / "reports" / "review_oracles").glob("*.md")
    ).read_text(encoding="utf-8")
    assert maintain_exclusions == [[]]
    assert evaluated_purposes == ["oracle 評価 oracles/original.md"]
    assert snapshot_reads == [("original\n", "maintained oracle index\n")]
    assert f'session_fork_commit: "{session_fork_commit}"' in report
    assert f'review_fork_commit: "{review_start_head}"' in report
    assert "oracle_count_total: 1" in report
    assert "oracle_count_evaluated: 1" in report
    assert "oracles/generated.md" not in report


def test_eval_oracles_snapshot_gets_missing_oracles_index_after_maintenance(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """元の INDEX.md がなくても評価 prompt の snapshot 側 INDEX.md は存在する。"""
    repo = _init_repo(tmp_path)
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    oracle_file = oracle_root / "spec.md"
    oracle_file.write_text("spec\n", encoding="utf-8")
    _prepare_review_oracles_session(repo)

    def fake_maintain_indexes(repo_root: Path) -> bool:
        """欠落していた oracles/INDEX.md がメンテナンスで作られる状況を模擬する。"""
        (repo_root / "oracles" / "INDEX.md").write_text(
            "created oracle index\n",
            encoding="utf-8",
        )
        _git(repo_root, "add", "oracles/INDEX.md")
        _git(repo_root, "commit", "-m", "fake oracle index maintenance")
        return True

    monkeypatch.setattr(
        review_oracles_module,
        "maintain_indexes",
        fake_maintain_indexes,
    )
    snapshot_index_texts: list[str] = []

    def fake_codex(*args: object, **kwargs: object) -> str:
        """評価 prompt が指す snapshot 側 INDEX.md の実在と内容を記録する。"""
        execution_repo_root = Path(args[0])
        prompt = str(args[1])
        index_match = re.search(
            r"`([^`]+/oracles/INDEX\.md)` から始まる INDEX\.md",
            prompt,
        )
        assert index_match is not None
        Path(index_match.group(1)).relative_to(execution_repo_root)
        snapshot_index_texts.append(
            Path(index_match.group(1)).read_text(encoding="utf-8")
        )
        return json.dumps({"issues": []}, ensure_ascii=False)

    monkeypatch.setattr(review_oracles_module, "run_codex_exec", fake_codex)

    cmoc_review_oracles_impl(repo, full=True, repeat_improve_issues_list=0)

    assert snapshot_index_texts == ["created oracle index\n"]


def test_eval_oracles_reads_fixed_snapshot_after_oracle_tree_changes(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """評価本文と path 検証は評価直前の oracle snapshot に固定する。"""
    repo = _init_repo(tmp_path)
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    oracle_file = oracle_root / "spec.md"
    oracle_file.write_text("original snapshot text\n", encoding="utf-8")
    _prepare_review_oracles_session(repo)

    def fake_maintain_indexes(repo_root: Path) -> bool:
        """INDEX.md メンテナンス自体は oracle 本文を変えない。"""
        (repo_root / "oracles" / "INDEX.md").write_text(
            "maintained index\n",
            encoding="utf-8",
        )
        _git(repo_root, "add", "oracles/INDEX.md")
        _git(repo_root, "commit", "-m", "fake oracle index maintenance")
        return True

    monkeypatch.setattr(
        review_oracles_module,
        "maintain_indexes",
        fake_maintain_indexes,
    )
    snapshot_texts: list[str] = []

    def fake_codex(*args: object, **kwargs: object) -> str:
        """prompt 上の snapshot path を読み、live tree 変更の影響がないことを返す。"""
        execution_repo_root = Path(args[0])
        prompt = str(args[1])
        match = re.search(
            r"開始時点の内容を固定したコピー `([^`]+/oracles/spec\.md)`",
            prompt,
        )
        assert match is not None
        Path(match.group(1)).relative_to(execution_repo_root)
        oracle_file.unlink()
        (repo / "oracles" / "later.md").write_text(
            "later live text\n",
            encoding="utf-8",
        )
        _git(repo, "add", "-A", "oracles")
        _git(repo, "commit", "-m", "change live oracle tree during review")
        snapshot_path = Path(match.group(1))
        snapshot_texts.append(snapshot_path.read_text(encoding="utf-8"))
        issue = _eval_oracle_issue(
            "warning",
            "snapshot warning",
            oracle_file,
            1,
            1,
            [oracle_file],
        )
        return json.dumps({"issues": [issue]}, ensure_ascii=False)

    monkeypatch.setattr(review_oracles_module, "run_codex_exec", fake_codex)

    cmoc_review_oracles_impl(repo, full=True, repeat_improve_issues_list=0)

    report = next(
        (repo / ".cmoc" / "reports" / "review_oracles").glob("*.md")
    ).read_text(encoding="utf-8")
    assert snapshot_texts == ["original snapshot text\n"]
    assert "snapshot warning" in report
    assert f"| 1 | `{oracle_file.resolve()}` | 1 |" in report
    assert str((repo / "oracles" / "later.md").resolve()) not in report


def test_eval_oracles_index_maintenance_updates_oracles_index(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """review 前の INDEX.md メンテナンスは oracles 配下も最新化する。"""
    repo = _init_repo(tmp_path)
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    oracle_file = oracle_root / "spec.md"
    oracle_file.write_text("spec\n", encoding="utf-8")
    stale_index = "stale oracle routing\n"
    (oracle_root / "INDEX.md").write_text(stale_index, encoding="utf-8")
    _git(repo, "add", "oracles")
    _git(repo, "commit", "-m", "add stale oracle index")
    _prepare_review_oracles_session(repo)

    def fake_index_codex(*args: object, **kwargs: object) -> str:
        """repo root INDEX 生成だけを決定論的に返す。"""
        return json.dumps(
            {
                "summary": ["テスト用 entry です。"],
                "read_this_when": ["テストで読むとき。"],
                "do_not_read_this_when": ["テストで読まないとき。"],
            },
            ensure_ascii=False,
        )

    def fake_review_codex(*args: object, **kwargs: object) -> str:
        """oracle 評価では問題なしを返す。"""
        return json.dumps({"issues": []}, ensure_ascii=False)

    monkeypatch.setattr("commons.indexing.run_codex_exec", fake_index_codex)
    monkeypatch.setattr(review_oracles_module, "run_codex_exec", fake_review_codex)

    cmoc_review_oracles_impl(repo, full=True, repeat_improve_issues_list=0)

    assert (oracle_root / "INDEX.md").read_text(encoding="utf-8") != stale_index
    changed_files = _git(
        repo,
        "diff",
        "--name-only",
        "HEAD^1",
        "HEAD",
    ).stdout.splitlines()
    assert "oracles/INDEX.md" in changed_files


def test_eval_oracles_runs_file_evaluations_in_parallel(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """ファイルごとの oracle 評価は並列実行し、report 順は対象順を保つ。"""
    repo = _init_repo(tmp_path)
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    for name in ["a.md", "b.md", "c.md"]:
        (oracle_root / name).write_text(f"{name}\n", encoding="utf-8")
    _prepare_review_oracles_session(repo)

    monkeypatch.setattr(
        review_oracles_module,
        "maintain_indexes",
        lambda repo_root: False,
    )

    barrier = threading.Barrier(3, timeout=2.0)
    lock = threading.Lock()
    active_calls = 0
    max_active_calls = 0
    purposes: list[str] = []

    def fake_codex(*args: object, **kwargs: object) -> str:
        """全評価呼び出しが同時に開始されることを観測する。"""
        nonlocal active_calls, max_active_calls
        with lock:
            active_calls += 1
            max_active_calls = max(max_active_calls, active_calls)
            purposes.append(str(kwargs["purpose"]))
        barrier.wait()
        time.sleep(0.05)
        with lock:
            active_calls -= 1
        return json.dumps({"issues": []}, ensure_ascii=False)

    monkeypatch.setattr(review_oracles_module, "run_codex_exec", fake_codex)

    cmoc_review_oracles_impl(repo, full=True, repeat_improve_issues_list=0)

    report = next(
        (repo / ".cmoc" / "reports" / "review_oracles").glob("*.md")
    ).read_text(encoding="utf-8")
    assert max_active_calls > 1
    assert sorted(purposes) == [
        "oracle 評価 oracles/a.md",
        "oracle 評価 oracles/b.md",
        "oracle 評価 oracles/c.md",
    ]
    row_a = f"| 1 | `{(oracle_root / 'a.md').resolve()}` | 0 |"
    row_b = f"| 2 | `{(oracle_root / 'b.md').resolve()}` | 0 |"
    row_c = f"| 3 | `{(oracle_root / 'c.md').resolve()}` | 0 |"
    assert report.index(row_a) < report.index(row_b)
    assert report.index(row_b) < report.index(row_c)


def test_eval_oracles_writes_error_report_when_evaluation_fails(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """評価処理に失敗した場合も `result: error` レポートを保存する。"""
    repo = _init_repo(tmp_path)
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    (oracle_root / "spec.md").write_text("spec\n", encoding="utf-8")
    _prepare_review_oracles_session(repo)

    monkeypatch.setattr(
        review_oracles_module,
        "maintain_indexes",
        lambda repo_root: False,
    )

    def fake_codex(*args: object, **kwargs: object) -> str:
        """oracle 評価中に失敗する Codex 実行を模擬する。"""
        raise RuntimeError("fake evaluation failure")

    monkeypatch.setattr(review_oracles_module, "run_codex_exec", fake_codex)

    with pytest.raises(RuntimeError, match="fake evaluation failure"):
        cmoc_review_oracles_impl(repo, full=True)

    reports = list((repo / ".cmoc" / "reports" / "review_oracles").glob("*.md"))
    assert len(reports) == 1
    report = reports[0].read_text(encoding="utf-8")
    assert 'result: "error"' in report
    assert "oracle_count_total: 1" in report
    assert "oracle_count_evaluated: 0" in report
    assert "- Failed stage: `oracle ファイル評価`" in report
    assert "- Exception type: `RuntimeError`" in report
    assert "- Exception message: `fake evaluation failure`" in report
    assert "# cmoc review oracles report" in report
    assert "## Verdict" in report
    assert "## Specification-only basis" not in report
    assert "成功評価ではありません" in report
    assert "今回評価した範囲では問題点が検出されませんでした" not in report
    assert "## Evaluated oracle files" in report
    assert "## Fatal findings" in report
    assert "## Minor findings" in report
    assert "## Rejected fatal findings" in report
    assert "## Rejected minor findings" in report
    assert "## Referenced files" in report
    expected_sections = [
        "# cmoc review oracles report",
        "## Verdict",
        "## Evaluated oracle files",
        "## Fatal findings",
        "## Minor findings",
        "## Rejected fatal findings",
        "## Rejected minor findings",
        "## Referenced files",
    ]
    assert [report.index(section) for section in expected_sections] == sorted(
        report.index(section) for section in expected_sections
    )
    evaluated_section = report[
        report.index("## Evaluated oracle files") : report.index(
            "## Fatal findings"
        )
    ]
    assert "Not evaluated oracle files:" not in evaluated_section


def test_eval_oracles_writes_error_report_when_preparation_fails(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """前処理に失敗した場合も、取得済み範囲で error レポートを保存する。"""
    repo = _init_repo(tmp_path)
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    (oracle_root / "spec.md").write_text("spec\n", encoding="utf-8")
    _prepare_review_oracles_session(repo)
    branch_name = _git(repo, "branch", "--show-current").stdout.strip()
    session_fork_commit = repo_module.read_session_start_commit(repo, branch_name)
    (repo / "session-note.txt").write_text("session change\n", encoding="utf-8")
    _git(repo, "add", "session-note.txt")
    _git(repo, "commit", "-m", "add session change before review")
    review_start_head = _git(repo, "rev-parse", "HEAD").stdout.strip()
    assert session_fork_commit != review_start_head

    def fake_maintain_indexes(_repo_root: Path) -> bool:
        """INDEX.md メンテナンス中の失敗を模擬する。"""
        raise RuntimeError("fake preparation failure")

    monkeypatch.setattr(
        review_oracles_module,
        "maintain_indexes",
        fake_maintain_indexes,
    )

    with pytest.raises(RuntimeError, match="fake preparation failure"):
        cmoc_review_oracles_impl(repo, full=True)

    reports = list((repo / ".cmoc" / "reports" / "review_oracles").glob("*.md"))
    assert len(reports) == 1
    report = reports[0].read_text(encoding="utf-8")
    assert 'result: "error"' in report
    assert 'scope: "full"' in report
    assert "session_branch:" in report
    assert f'session_fork_commit: "{session_fork_commit}"' in report
    assert f'review_fork_commit: "{review_start_head}"' in report
    assert "oracle_count_total: 1" in report
    assert "oracle_count_evaluated: 0" in report
    assert "- Failed stage: `INDEX.md メンテナンス`" in report
    spec_row = (
        f"| 1 | `{(oracle_root / 'spec.md').resolve()}` | "
        "not_evaluated | - |"
    )
    assert spec_row in report


def test_eval_oracles_error_report_marks_unevaluated_files_in_table(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """途中失敗時、未評価 file は評価済み行ではなく状態付き行にする。"""
    repo = _init_repo(tmp_path)
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    oracle_a = oracle_root / "a.md"
    oracle_b = oracle_root / "b.md"
    oracle_a.write_text("a\n", encoding="utf-8")
    oracle_b.write_text("b\n", encoding="utf-8")
    _prepare_review_oracles_session(repo)

    monkeypatch.setattr(
        review_oracles_module,
        "maintain_indexes",
        lambda repo_root: False,
    )

    def fake_codex(*args: object, **kwargs: object) -> str:
        """a.md だけ成功し、b.md の評価で失敗する。"""
        purpose = str(kwargs["purpose"])
        if "oracles/b.md" in purpose:
            raise RuntimeError("fake second evaluation failure")
        return json.dumps(
            {"issues": []},
            ensure_ascii=False,
        )

    monkeypatch.setattr(review_oracles_module, "run_codex_exec", fake_codex)

    with pytest.raises(RuntimeError, match="fake second evaluation failure"):
        cmoc_review_oracles_impl(repo, full=True)

    report = next(
        (repo / ".cmoc" / "reports" / "review_oracles").glob("*.md")
    ).read_text(encoding="utf-8")
    assert "oracle_count_total: 2" in report
    assert "oracle_count_evaluated: 1" in report
    assert "## Specification-only basis" not in report
    assert f"| 1 | `{oracle_a.resolve()}` | evaluated | 0 |" in report
    assert f"| 2 | `{oracle_b.resolve()}` | not_evaluated | - |" in report
    assert f"| 2 | `{oracle_b.resolve()}` | evaluated | 0 |" not in report
    assert "Not evaluated oracle files:" not in report
    assert report.index("## Evaluated oracle files") < report.index(
        "## Fatal findings"
    )


def test_eval_oracles_writes_error_report_when_report_generation_fails(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """通常レポート生成失敗も `result: error` レポートとして残す。"""
    repo = _init_repo(tmp_path)
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    oracle_file = oracle_root / "spec.md"
    oracle_file.write_text("spec\n", encoding="utf-8")
    _prepare_review_oracles_session(repo)

    monkeypatch.setattr(
        review_oracles_module,
        "maintain_indexes",
        lambda repo_root: False,
    )

    def fake_codex(*args: object, **kwargs: object) -> str:
        """レポート生成前までは成功する Codex 実行を模擬する。"""
        return json.dumps(
            {"issues": []},
            ensure_ascii=False,
        )

    def fake_write_report(*args: object, **kwargs: object) -> Path:
        """通常レポート書き込みだけが失敗する状態を模擬する。"""
        raise OSError("fake report failure")

    monkeypatch.setattr(review_oracles_module, "run_codex_exec", fake_codex)
    monkeypatch.setattr(
        review_oracles_module,
        "_write_report",
        fake_write_report,
    )

    with pytest.raises(OSError, match="fake report failure"):
        cmoc_review_oracles_impl(repo, full=True)

    reports = list((repo / ".cmoc" / "reports" / "review_oracles").glob("*.md"))
    assert len(reports) == 1
    report = reports[0].read_text(encoding="utf-8")
    assert 'result: "error"' in report
    assert "oracle_count_evaluated: 1" in report
    assert "- Failed stage: `report 書き込み`" in report
    assert "- Exception type: `OSError`" in report
    assert "- Exception message: `fake report failure`" in report
    assert "成功評価ではありません" in report
    assert "今回評価した範囲では問題点が検出されませんでした" not in report
    assert "## Specification-only basis" not in report


def test_eval_oracles_preserves_original_error_when_error_report_fails(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """error report 保存の二次失敗で一次失敗情報を失わない。"""
    repo = _init_repo(tmp_path)
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    (oracle_root / "spec.md").write_text("spec\n", encoding="utf-8")
    _prepare_review_oracles_session(repo)

    monkeypatch.setattr(
        review_oracles_module,
        "maintain_indexes",
        lambda repo_root: False,
    )

    def fake_codex(*args: object, **kwargs: object) -> str:
        """oracle 評価中の一次失敗を模擬する。"""
        raise RuntimeError("primary evaluation failure")

    def fake_write_error_report(*args: object, **kwargs: object) -> Path:
        """error report 書き込み自体の二次失敗を模擬する。"""
        raise OSError("secondary report failure")

    monkeypatch.setattr(review_oracles_module, "run_codex_exec", fake_codex)
    monkeypatch.setattr(
        review_oracles_module,
        "_write_error_report",
        fake_write_error_report,
    )

    with pytest.raises(RuntimeError, match="primary evaluation failure") as exc_info:
        cmoc_review_oracles_impl(repo, full=True)

    assert [
        "review oracles error report generation also failed: "
        "OSError: secondary report failure"
    ] == exc_info.value.__notes__
    captured = capsys.readouterr()
    assert "cmoc review oracles error report generation failed." in captured.err
    assert "- result: error" in captured.err
    assert "- failed_stage: oracle ファイル評価" in captured.err
    assert "- exception: RuntimeError: primary evaluation failure" in captured.err
    assert "- report_exception: OSError: secondary report failure" in captured.err


def test_eval_oracles_report_aggregates_issues_by_severity(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """レポートはファイル単位ではなく issue 単位で severity 順に集約する。"""
    repo = _init_repo(tmp_path)
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    oracle_a = oracle_root / "a.md"
    oracle_b = oracle_root / "b.md"
    oracle_index = oracle_root / "INDEX.md"
    oracle_a.write_text("a\n", encoding="utf-8")
    oracle_b.write_text("b\n", encoding="utf-8")
    oracle_index.write_text("index\n", encoding="utf-8")
    _prepare_review_oracles_session(repo)

    monkeypatch.setattr(
        review_oracles_module,
        "maintain_indexes",
        lambda repo_root: False,
    )

    def fake_codex(*args: object, **kwargs: object) -> str:
        """対象 oracle ごとに異なる severity の評価結果を返す。"""
        purpose = str(kwargs["purpose"])
        if "oracles/a.md" in purpose:
            return json.dumps(
                {
                    "issues": [
                        _eval_oracle_issue(
                            "warning",
                            "A warning",
                            oracle_a,
                            3,
                            4,
                            [oracle_a, oracle_index],
                        ),
                        _eval_oracle_issue(
                            "fatal",
                            "A fatal",
                            oracle_a,
                            5,
                            5,
                            [oracle_a, oracle_index],
                        ),
                    ],
                },
                ensure_ascii=False,
            )
        return json.dumps(
            {
                "issues": [
                    _eval_oracle_issue(
                        "inconclusive",
                        "B inconclusive",
                        oracle_b,
                        None,
                        None,
                        [oracle_b, oracle_index],
                    ),
                    _eval_oracle_issue(
                        "fatal",
                        "B fatal",
                        oracle_b,
                        8,
                        9,
                        [oracle_b, oracle_index],
                    ),
                    _eval_oracle_issue(
                        "warning",
                        "B warning",
                        oracle_b,
                        10,
                        10,
                        [oracle_b, oracle_index],
                    ),
                ],
            },
            ensure_ascii=False,
        )

    monkeypatch.setattr(review_oracles_module, "run_codex_exec", fake_codex)

    cmoc_review_oracles_impl(repo, full=True, repeat_improve_issues_list=0)

    report = next(
        (repo / ".cmoc" / "reports" / "review_oracles").glob("*.md")
    ).read_text(encoding="utf-8")
    for field in [
        'command: "cmoc review oracles"',
        "generated_at:",
        f'repo_root: "{repo.resolve()}"',
        'scope: "full"',
        "session_branch:",
        "session_fork_commit:",
        "review_branch:",
        "review_fork_commit:",
        "review_join_commit:",
        "oracle_count_total: 2",
        "oracle_count_evaluated: 2",
        "fatal_findings_accepted_count: 2",
        "minor_findings_accepted_count: 3",
        "fatal_findings_rejected_count: 0",
        "minor_findings_rejected_count: 0",
        'result: "fatal"',
    ]:
        assert field in report

    expected_sections = [
        "# cmoc review oracles report",
        "## Verdict",
        "## Evaluated oracle files",
        "## Fatal findings",
        "## Minor findings",
        "## Rejected fatal findings",
        "## Rejected minor findings",
        "## Referenced files",
    ]
    assert [report.index(section) for section in expected_sections] == sorted(
        report.index(section) for section in expected_sections
    )
    assert "## Specification-only basis" not in report
    assert report.index("### FATAL-001: A fatal") < report.index(
        "### FATAL-002: B fatal"
    )
    assert report.index("### FATAL-002: B fatal") < report.index(
        "### MINOR-001: A warning"
    )
    assert report.index("### MINOR-001: A warning") < report.index(
        "### MINOR-002: B inconclusive"
    )
    assert report.index("### MINOR-002: B inconclusive") < report.index(
        "### MINOR-003: B warning"
    )
    assert f"| 1 | `{oracle_a.resolve()}` | 2 |" in report
    assert f"| 2 | `{oracle_b.resolve()}` | 3 |" in report
    assert f"- Oracle file: `{oracle_a.resolve()}`" in report
    assert f"- Oracle file: `{oracle_b.resolve()}`" in report
    assert "- Specification-only basis:" in report
    assert "oracles 配下の仕様だけを参照しました。" in report
    assert "- Oracle file: `oracles/a.md`" not in report
    assert "- Oracle file: `oracles/b.md`" not in report
    assert "| No. | Referenced file |" in report
    assert f"| 1 | `{oracle_a.resolve()}` |" in report
    assert f"| 2 | `{(oracle_root / 'INDEX.md').resolve()}` |" in report
    assert f"| 3 | `{oracle_b.resolve()}` |" in report
    assert report.count(f"| 2 | `{(oracle_root / 'INDEX.md').resolve()}` |") == 1


def test_eval_oracles_report_frontmatter_quotes_string_scalars(
    tmp_path: Path,
) -> None:
    """frontmatter の文字列値は YAML 特殊文字を含んでも quote する。"""
    repo = tmp_path / "repo # root: value"
    oracle_root = repo / "oracles"
    oracle_root.mkdir(parents=True)
    oracle_file = oracle_root / "spec.md"
    oracle_file.write_text("spec\n", encoding="utf-8")
    branch_name = "feature: #topic\nquoted \"branch\""
    commit_hash = "abc123: #hash\nnext"

    report_path = review_oracles_module._write_report(
        repo,
        "full",
        True,
        branch_name,
        False,
        None,
        commit_hash,
        False,
        1,
        [oracle_file],
        [],
        "full",
        "cmoc/review/session/run: #branch\nquoted \"review\"",
        "review-fork: #hash\nquoted",
        "review-join: #hash\nquoted",
    )

    frontmatter = report_path.read_text(encoding="utf-8").split("---\n", 2)[1]
    repo_root_value = review_oracles_module._yaml_string(str(repo.resolve()))
    branch_value = review_oracles_module._yaml_string(branch_name)
    commit_value = review_oracles_module._yaml_string(commit_hash)
    review_branch_value = review_oracles_module._yaml_string(
        "cmoc/review/session/run: #branch\nquoted \"review\""
    )
    review_fork_value = review_oracles_module._yaml_string(
        "review-fork: #hash\nquoted"
    )
    review_join_value = review_oracles_module._yaml_string(
        "review-join: #hash\nquoted"
    )
    assert f"repo_root: {repo_root_value}" in frontmatter
    assert f"session_branch: {branch_value}" in frontmatter
    assert f"session_fork_commit: {commit_value}" in frontmatter
    assert f"review_branch: {review_branch_value}" in frontmatter
    assert f"review_fork_commit: {review_fork_value}" in frontmatter
    assert f"review_join_commit: {review_join_value}" in frontmatter


def test_eval_oracles_report_groups_rejected_findings(
    tmp_path: Path,
) -> None:
    """不採用 finding も件数と本文に fatal/minor 別で残す。"""
    repo = tmp_path / "repo"
    oracle_root = repo / "oracles"
    oracle_root.mkdir(parents=True)
    oracle_file = oracle_root / "spec.md"
    oracle_file.write_text("spec\n", encoding="utf-8")
    fatal_issue = _eval_oracle_issue(
        "fatal",
        "Accepted fatal",
        oracle_file,
        None,
        None,
        [oracle_file],
    )
    fatal_issue["finding_severity"] = "fatal"
    fatal_issue["judge_verdict"] = "accept"
    accepted_minor_issue = _eval_oracle_issue(
        "warning",
        "Accepted minor",
        oracle_file,
        None,
        None,
        [oracle_file],
    )
    accepted_minor_issue["finding_severity"] = "minor"
    accepted_minor_issue["judge_verdict"] = "accept"
    rejected_fatal_issue = _eval_oracle_issue(
        "fatal",
        "Rejected fatal",
        oracle_file,
        None,
        None,
        [oracle_file],
    )
    rejected_fatal_issue["finding_severity"] = "fatal"
    rejected_fatal_issue["judge_verdict"] = "reject"
    minor_issue = _eval_oracle_issue(
        "warning",
        "Rejected minor",
        oracle_file,
        None,
        None,
        [oracle_file],
    )
    minor_issue["finding_severity"] = "minor"
    minor_issue["judge_verdict"] = "reject"

    report_path = review_oracles_module._write_report(
        repo,
        "full",
        True,
        "cmoc/session/example",
        True,
        None,
        "session-commit",
        False,
        1,
        [oracle_file],
        [
            {
                "target_oracle_path": str(oracle_file.resolve()),
                "referenced_paths": [str(oracle_file.resolve())],
                "specification_only_basis": "",
                "issues": [
                    fatal_issue,
                    rejected_fatal_issue,
                    accepted_minor_issue,
                    minor_issue,
                ],
            }
        ],
        "full",
        "cmoc/review/example/run",
        "review-fork",
        "review-join",
    )

    report = report_path.read_text(encoding="utf-8")
    assert "fatal_findings_accepted_count: 1" in report
    assert "minor_findings_accepted_count: 1" in report
    assert "fatal_findings_rejected_count: 1" in report
    assert "minor_findings_rejected_count: 1" in report
    assert 'result: "fatal"' in report
    expected_sections = [
        "## Fatal findings",
        "## Minor findings",
        "## Rejected fatal findings",
        "## Rejected minor findings",
    ]
    assert [report.index(section) for section in expected_sections] == sorted(
        report.index(section) for section in expected_sections
    )
    assert "### FATAL-001: Accepted fatal" in report
    assert "### MINOR-001: Accepted minor" in report
    assert "### FATAL-001: Rejected fatal" in report
    assert "### MINOR-001: Rejected minor" in report
    assert report.index("### FATAL-001: Accepted fatal") < report.index(
        "### MINOR-001: Accepted minor"
    )
    assert report.index("### MINOR-001: Accepted minor") < report.index(
        "### FATAL-001: Rejected fatal"
    )
    assert report.index("### FATAL-001: Rejected fatal") < report.index(
        "### MINOR-001: Rejected minor"
    )


@pytest.mark.parametrize(
    ("finding_severity", "issue_severity", "expected_result"),
    [
        ("fatal", "fatal", "fatal"),
        ("minor", "warning", "minor"),
    ],
)
def test_eval_oracles_report_result_counts_rejected_findings(
    tmp_path: Path,
    finding_severity: str,
    issue_severity: str,
    expected_result: str,
) -> None:
    """不採用 finding のみでも result は検出 severity を反映する。"""
    repo = tmp_path / "repo"
    oracle_root = repo / "oracles"
    oracle_root.mkdir(parents=True)
    oracle_file = oracle_root / "spec.md"
    oracle_file.write_text("spec\n", encoding="utf-8")
    issue = _eval_oracle_issue(
        issue_severity,
        f"Rejected {finding_severity}",
        oracle_file,
        None,
        None,
        [oracle_file],
    )
    issue["finding_severity"] = finding_severity
    issue["judge_verdict"] = "reject"

    report_path = review_oracles_module._write_report(
        repo,
        "full",
        True,
        "cmoc/session/example",
        True,
        None,
        "session-commit",
        False,
        1,
        [oracle_file],
        [
            {
                "target_oracle_path": str(oracle_file.resolve()),
                "referenced_paths": [str(oracle_file.resolve())],
                "specification_only_basis": "",
                "issues": [issue],
            }
        ],
        "full",
        "cmoc/review/example/run",
        "review-fork",
        "review-join",
    )

    report = report_path.read_text(encoding="utf-8")
    assert "fatal_findings_accepted_count: 0" in report
    assert "minor_findings_accepted_count: 0" in report
    assert f'result: "{expected_result}"' in report
    if finding_severity == "fatal":
        assert "fatal_findings_rejected_count: 1" in report
        assert "minor_findings_rejected_count: 0" in report
    else:
        assert "fatal_findings_rejected_count: 0" in report
        assert "minor_findings_rejected_count: 1" in report


def test_eval_oracles_error_report_frontmatter_quotes_string_scalars(
    tmp_path: Path,
) -> None:
    """error report の frontmatter も文字列値を安全な scalar にする。"""
    repo = tmp_path / "repo # root: value"
    oracle_root = repo / "oracles"
    oracle_root.mkdir(parents=True)
    branch_name = "feature: #topic\nquoted \"branch\""
    commit_hash = "abc123: #hash\nnext"

    report_path = review_oracles_module._write_error_report(
        repo,
        "partial: #mode",
        False,
        branch_name,
        None,
        None,
        commit_hash,
        None,
        None,
        [],
        [],
        "session",
        "cmoc/review/session/run: #branch\nquoted \"review\"",
        "review-fork: #hash\nquoted",
        None,
        "stage: #failure",
        RuntimeError("boom"),
    )

    frontmatter = report_path.read_text(encoding="utf-8").split("---\n", 2)[1]
    repo_root_value = review_oracles_module._yaml_string(str(repo.resolve()))
    branch_value = review_oracles_module._yaml_string(branch_name)
    commit_value = review_oracles_module._yaml_string(commit_hash)
    review_branch_value = review_oracles_module._yaml_string(
        "cmoc/review/session/run: #branch\nquoted \"review\""
    )
    review_fork_value = review_oracles_module._yaml_string(
        "review-fork: #hash\nquoted"
    )
    assert f"repo_root: {repo_root_value}" in frontmatter
    assert 'scope: "session"' in frontmatter
    assert f"session_branch: {branch_value}" in frontmatter
    assert f"session_fork_commit: {commit_value}" in frontmatter
    assert f"review_branch: {review_branch_value}" in frontmatter
    assert f"review_fork_commit: {review_fork_value}" in frontmatter


def test_review_oracles_improves_combined_issue_list(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """評価後の結合 issue list は指定回数まで改善され、改善後をレポートする。"""
    repo = _init_repo(tmp_path)
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    oracle_file = oracle_root / "spec.md"
    oracle_file.write_text("spec\n", encoding="utf-8")
    _prepare_review_oracles_session(repo)

    monkeypatch.setattr(
        review_oracles_module,
        "maintain_indexes",
        lambda repo_root: False,
    )
    calls: list[str] = []
    codex_kwargs: list[dict[str, object]] = []

    def issue(title: str) -> dict[str, object]:
        result = _eval_oracle_issue("warning", title, oracle_file, 1, 1)
        result["referenced_paths"] = [str(oracle_file.resolve())]
        result["specification_only_basis"] = "oracles 配下の仕様だけを参照しました。"
        return result

    def fake_codex(*args: object, **kwargs: object) -> str:
        """評価結果を改善呼び出しで置き換える Codex 実行を模擬する。"""
        purpose = str(kwargs["purpose"])
        calls.append(purpose)
        codex_kwargs.append(kwargs)
        if "oracle 問題点リスト改善" in purpose:
            return json.dumps(
                {"issues": [issue("Improved warning")]},
                ensure_ascii=False,
            )
        return json.dumps({"issues": [issue("Raw warning")]}, ensure_ascii=False)

    monkeypatch.setattr(review_oracles_module, "run_codex_exec", fake_codex)

    cmoc_review_oracles_impl(repo, full=True, repeat_improve_issues_list=2)

    report = next(
        (repo / ".cmoc" / "reports" / "review_oracles").glob("*.md")
    ).read_text(encoding="utf-8")
    assert calls == [
        "oracle 評価 oracles/spec.md",
        "oracle 問題点リスト改善 1",
        "oracle 問題点リスト改善 2",
    ]
    assert [
        kwargs.get("skip_index_maintenance") for kwargs in codex_kwargs
    ] == [None, None, None]
    improve_kwargs = [
        kwargs
        for kwargs in codex_kwargs
        if "oracle 問題点リスト改善" in kwargs["purpose"]
    ]
    assert all(kwargs["model"] == FRONTIER_MODEL for kwargs in improve_kwargs)
    assert all(
        kwargs["reasoning_effort"] == FRONTIER_HIGH_REASONING_EFFORT
        for kwargs in improve_kwargs
    )
    assert "Improved warning" in report
    assert "Raw warning" not in report


def test_review_oracles_rejects_too_many_refine_findings_loops(
    tmp_path: Path,
) -> None:
    """所見リスト検証ループの反復回数は oracle の最大 3 回を超えられない。"""
    repo = _init_repo(tmp_path)

    with pytest.raises(
        ValueError,
        match="--refine-findings-loop must be between 0 and 3",
    ):
        cmoc_review_oracles_impl(repo, scope="full", refine_findings_loop=4)


def test_review_oracles_finding_pipeline_schemas_are_canonical_files() -> None:
    """review oracles の finding pipeline schema は oracles 配下の正本 JSON を使う。"""
    repo_root = Path(__file__).resolve().parents[2]
    schema_root = (
        repo_root
        / "oracles"
        / "schemas"
        / "structured_output"
        / "review"
        / "oracles"
    )
    expected_schemas = {
        "_ENUMERATE_FINDINGS_OUTPUT_SCHEMA": "enumerate_findings.json",
        "_MERGE_FINDINGS_OUTPUT_SCHEMA": "merge_findings.json",
        "_VALIDATE_FINDINGS_CHALLENGER_OUTPUT_SCHEMA": (
            "validate_findings_challenger.json"
        ),
        "_VALIDATE_FINDINGS_ADVOCATE_OUTPUT_SCHEMA": (
            "validate_findings_advocate.json"
        ),
        "_JUDGE_FINDINGS_OUTPUT_SCHEMA": "judge_findings.json",
    }

    for constant_name, file_name in expected_schemas.items():
        expected_schema = json.loads(
            (schema_root / file_name).read_text(encoding="utf-8")
        )
        assert getattr(review_oracles_module, constant_name) == expected_schema

    source = inspect.getsource(review_oracles_module)
    for constant_name, file_name in expected_schemas.items():
        assert (
            f'{constant_name} = _load_review_oracles_output_schema(\n'
            f'    "{file_name}"\n'
            ")"
        ) in source


def test_review_oracles_validate_finding_prompt_states_reason_principles(
    tmp_path: Path,
) -> None:
    """所見検証 prompt は理由生成の 3 原則と反対側理由を伝える。"""
    repo = _init_repo(tmp_path)
    finding = review_oracles_module._Finding(
        finding_id="FINDING-0001",
        severity="fatal",
        title="Finding",
        oracle_path=str((repo / "oracles" / "spec.md").resolve()),
        reason="指摘理由",
        challenger_reasons=["妥当ではない既存理由"],
        advocate_reasons=["妥当である既存理由"],
    )

    challenger_prompt = review_oracles_module._validate_finding_prompt(
        repo,
        finding,
        "challenger",
    )
    advocate_prompt = review_oracles_module._validate_finding_prompt(
        repo,
        finding,
        "advocate",
    )

    for prompt in [challenger_prompt, advocate_prompt]:
        assert "理由には具体的な根拠を必ず含めてください。" in prompt
        assert "推測だけを根拠にした理由は返さないでください。" in prompt
        assert "対応する反対側理由への反論を含めてください。" in prompt
        assert "反対側の既存理由:" in prompt

    assert '"妥当である既存理由"' in challenger_prompt
    assert '"妥当ではない既存理由"' in advocate_prompt


def test_review_oracles_reasons_payload_rejects_empty_and_speculative_reasons() -> None:
    """所見検証理由 payload は空白理由と禁止された推測表現を拒否する。"""
    review_oracles_module._validate_reasons_payload(
        {"reasons": ["spec.md の記述と実装の条件分岐が一致しないため。"]}
    )

    for reason in ["", "   ", "仕様違反かもしれない。", "不整合の可能性がある。"]:
        with pytest.raises(ValueError, match="reasons\\[0\\]"):
            review_oracles_module._validate_reasons_payload(
                {"reasons": [reason]}
            )


def test_review_oracles_append_new_findings_does_not_reuse_deleted_id(
    tmp_path: Path,
) -> None:
    """delete 後に列挙された新規所見は削除済み ID 番号を再利用しない。"""
    repo = _init_repo(tmp_path)
    oracle_file = repo / "oracles" / "spec.md"
    oracle_file.parent.mkdir()
    oracle_file.write_text("spec\n", encoding="utf-8")
    payload = {
        "severity": "fatal",
        "title": "Finding",
        "oracle_path": str(oracle_file.resolve()),
        "reason": "reason",
    }
    findings = [
        review_oracles_module._finding_from_payload(
            {**payload, "title": f"Finding {index}"},
            index,
        )
        for index in range(1, 4)
    ]
    finding_ids = review_oracles_module._FindingIdAllocator.from_findings(findings)

    findings = review_oracles_module._apply_merge_operations(
        findings,
        [
            {
                "kind": "delete",
                "target_ids": ["FINDING-0002"],
                "finding": None,
            }
        ],
        finding_ids,
    )
    review_oracles_module._append_new_findings(
        findings,
        [{**payload, "title": "Finding 4"}],
        finding_ids,
    )

    assert [finding.finding_id for finding in findings] == [
        "FINDING-0001",
        "FINDING-0003",
        "FINDING-0004",
    ]


def test_review_oracles_merge_operation_allocates_after_max_existing_id(
    tmp_path: Path,
) -> None:
    """gap がある所見 list の merge 生成でも既存 finding_id と衝突しない。"""
    repo = _init_repo(tmp_path)
    oracle_file = repo / "oracles" / "spec.md"
    oracle_file.parent.mkdir()
    oracle_file.write_text("spec\n", encoding="utf-8")
    payload = {
        "severity": "minor",
        "title": "Finding",
        "oracle_path": str(oracle_file.resolve()),
        "reason": "reason",
    }
    findings = [
        review_oracles_module._finding_from_payload(payload, 1),
        review_oracles_module._finding_from_payload(
            {**payload, "title": "Finding 3"},
            3,
        ),
    ]

    merged = review_oracles_module._apply_merge_operations(
        findings,
        [
            {
                "kind": "merge",
                "target_ids": ["FINDING-0001"],
                "finding": {**payload, "title": "Merged finding"},
            }
        ],
    )

    finding_ids = [finding.finding_id for finding in merged]
    assert finding_ids == ["FINDING-0004", "FINDING-0003"]
    assert len(finding_ids) == len(set(finding_ids))


def test_review_oracles_uses_finding_pipeline_schemas(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """review oracles は列挙、マージ、検証、判定の schema で所見を処理する。"""
    repo = _init_repo(tmp_path)
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    oracle_file = oracle_root / "spec.md"
    oracle_file.write_text("spec\n", encoding="utf-8")
    _prepare_review_oracles_session(repo)

    monkeypatch.setattr(
        review_oracles_module,
        "maintain_indexes",
        lambda repo_root: False,
    )
    output_schemas: list[dict[str, object]] = []
    purposes: list[str] = []

    def fake_codex(*args: object, **kwargs: object) -> str:
        """schema ごとに finding pipeline の最小 JSON を返す。"""
        purpose = str(kwargs["purpose"])
        purposes.append(purpose)
        output_schemas.append(kwargs["output_schema"])
        if kwargs["output_schema"] == review_oracles_module._ENUMERATE_FINDINGS_OUTPUT_SCHEMA:
            return json.dumps(
                {
                    "findings": [
                        {
                            "severity": "fatal",
                            "title": "Fatal finding",
                            "oracle_path": str(oracle_file.resolve()),
                            "reason": "fatal reason",
                        }
                    ]
                },
                ensure_ascii=False,
            )
        if kwargs["output_schema"] == review_oracles_module._MERGE_FINDINGS_OUTPUT_SCHEMA:
            return json.dumps({"operations": []}, ensure_ascii=False)
        if kwargs["output_schema"] in [
            review_oracles_module._VALIDATE_FINDINGS_CHALLENGER_OUTPUT_SCHEMA,
            review_oracles_module._VALIDATE_FINDINGS_ADVOCATE_OUTPUT_SCHEMA,
        ]:
            return json.dumps({"reasons": []}, ensure_ascii=False)
        if kwargs["output_schema"] == review_oracles_module._JUDGE_FINDINGS_OUTPUT_SCHEMA:
            return json.dumps(
                {"verdict": "accept", "reason": "show it"},
                ensure_ascii=False,
            )
        raise AssertionError(f"unexpected schema for {purpose}")

    monkeypatch.setattr(review_oracles_module, "run_codex_exec", fake_codex)

    cmoc_review_oracles_impl(
        repo,
        full=True,
        enumerate_findings_loop=1,
        merge_findings_loop=1,
        refine_findings_loop=1,
    )

    report = next(
        (repo / ".cmoc" / "reports" / "review_oracles").glob("*.md")
    ).read_text(encoding="utf-8")
    assert output_schemas[0] == review_oracles_module._ENUMERATE_FINDINGS_OUTPUT_SCHEMA
    assert review_oracles_module._MERGE_FINDINGS_OUTPUT_SCHEMA in output_schemas
    assert (
        review_oracles_module._VALIDATE_FINDINGS_CHALLENGER_OUTPUT_SCHEMA
        in output_schemas
    )
    assert (
        review_oracles_module._VALIDATE_FINDINGS_ADVOCATE_OUTPUT_SCHEMA
        in output_schemas
    )
    assert review_oracles_module._JUDGE_FINDINGS_OUTPUT_SCHEMA in output_schemas
    assert "oracle 評価 oracles/spec.md" in purposes
    assert "oracle 所見リストマージ 1" in purposes
    assert "oracle 所見検証 不採用理由 FINDING-0001" in purposes
    assert "oracle 所見検証 採用理由 FINDING-0001" in purposes
    assert "oracle 所見判定 FINDING-0001" in purposes
    assert "Fatal finding" in report
    assert "FINDING-0001" in report


def test_review_oracles_finding_payload_rejects_non_oracle_files(
    tmp_path: Path,
) -> None:
    """所見本体の oracle_path は oracles ファイル定義に限定する。"""
    repo = _init_repo(tmp_path)
    (repo / ".gitignore").write_text("oracles/ignored.md\n", encoding="utf-8")
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    oracle_file = oracle_root / "spec.md"
    index_file = oracle_root / "INDEX.md"
    ignored_file = oracle_root / "ignored.md"
    oracle_file.write_text("spec\n", encoding="utf-8")
    index_file.write_text("# index\n", encoding="utf-8")
    ignored_file.write_text("ignored\n", encoding="utf-8")

    def payload(oracle_path: Path) -> list[dict[str, object]]:
        return [
            {
                "severity": "fatal",
                "title": "Finding",
                "oracle_path": str(oracle_path.resolve()),
                "reason": "reason",
            }
        ]

    review_oracles_module._validate_finding_payloads(payload(oracle_file), repo)
    for rejected_path in [index_file, ignored_file]:
        with pytest.raises(
            ValueError,
            match="findings\\[0\\].oracle_path must be an oracle file",
        ):
            review_oracles_module._validate_finding_payloads(
                payload(rejected_path),
                repo,
            )


def test_review_oracles_finding_payload_uses_snapshot_oracle_files(
    tmp_path: Path,
) -> None:
    """snapshot 経路でも所見本体の oracle_path は oracle_files と照合する。"""
    repo = _init_repo(tmp_path)
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    oracle_file = oracle_root / "spec.md"
    index_file = oracle_root / "INDEX.md"
    ignored_file = oracle_root / "ignored.md"
    oracle_file.write_text("spec\n", encoding="utf-8")
    index_file.write_text("# index\n", encoding="utf-8")
    ignored_file.write_text("ignored\n", encoding="utf-8")
    snapshot = review_oracles_module._OracleEvaluationSnapshot(
        original_repo_root=repo.resolve(),
        original_oracle_root=oracle_root.resolve(),
        snapshot_root=repo.resolve(),
        snapshot_oracle_root=oracle_root.resolve(),
        oracle_files=frozenset({oracle_file.resolve()}),
        reference_files=frozenset(
            {
                oracle_file.resolve(),
                index_file.resolve(),
                ignored_file.resolve(),
            }
        ),
    )

    def payload(oracle_path: Path) -> list[dict[str, object]]:
        return [
            {
                "severity": "fatal",
                "title": "Finding",
                "oracle_path": str(oracle_path.resolve()),
                "reason": "reason",
            }
        ]

    review_oracles_module._validate_finding_payloads(
        payload(oracle_file),
        repo,
        snapshot,
    )
    for rejected_path in [index_file, ignored_file]:
        with pytest.raises(
            ValueError,
            match="findings\\[0\\].oracle_path must be an oracle file",
        ):
            review_oracles_module._validate_finding_payloads(
                payload(rejected_path),
                repo,
                snapshot,
            )


def test_review_oracles_accepts_improved_issue_for_unevaluated_oracle(
    tmp_path: Path,
) -> None:
    """改善後 issue の oracle_path が評価対象外でも後処理エラーにしない。"""
    repo = _init_repo(tmp_path)
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    evaluated_oracle = oracle_root / "evaluated.md"
    unevaluated_oracle = oracle_root / "unevaluated.md"
    evaluated_oracle.write_text("evaluated\n", encoding="utf-8")
    unevaluated_oracle.write_text("unevaluated\n", encoding="utf-8")

    evaluations = [
        {
            "target_oracle_path": str(evaluated_oracle.resolve()),
            "referenced_paths": [],
            "specification_only_basis": "",
            "issues": [],
        }
    ]
    improved_issue = _eval_oracle_issue(
        "warning",
        "outside target",
        unevaluated_oracle,
        1,
        1,
    )

    review_oracles_module._validate_issues_payload(
        {"issues": [improved_issue]},
        repo,
        {evaluated_oracle.resolve()},
    )

    redistributed = review_oracles_module._redistribute_improved_issues(
        evaluations,
        [improved_issue],
    )

    assert redistributed[0]["issues"] == [improved_issue]


def test_review_oracles_redistribution_uses_only_final_issue_provenance(
    tmp_path: Path,
) -> None:
    """改善後 report の根拠情報は最終 issue list だけから再計算する。"""
    repo = _init_repo(tmp_path)
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    oracle = oracle_root / "spec.md"
    oracle_index = oracle_root / "INDEX.md"
    oracle.write_text("spec\n", encoding="utf-8")
    oracle_index.write_text("index\n", encoding="utf-8")
    basis = "元評価は oracles 配下の仕様断片と INDEX だけを参照しました。"
    evaluations = [
        {
            "target_oracle_path": str(oracle.resolve()),
            "referenced_paths": [
                str(oracle.resolve()),
                str(oracle_index.resolve()),
            ],
            "specification_only_basis": basis,
            "issues": [],
        }
    ]
    improved_issue = _eval_oracle_issue("warning", "warning", oracle, 1, 1)
    improved_issue["referenced_paths"] = []
    improved_issue["specification_only_basis"] = ""

    redistributed = review_oracles_module._redistribute_improved_issues(
        evaluations,
        [improved_issue],
    )

    issue = redistributed[0]["issues"][0]
    assert issue["referenced_paths"] == []
    assert issue["specification_only_basis"] == ""
    assert redistributed[0]["referenced_paths"] == []
    assert redistributed[0]["specification_only_basis"] == ""


def test_review_oracles_redistribution_clears_deleted_issue_provenance(
    tmp_path: Path,
) -> None:
    """改善で issue が消えた評価には改善前の根拠情報を残さない。"""
    repo = _init_repo(tmp_path)
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    oracle = oracle_root / "spec.md"
    oracle_index = oracle_root / "INDEX.md"
    oracle.write_text("spec\n", encoding="utf-8")
    oracle_index.write_text("index\n", encoding="utf-8")
    evaluations = [
        {
            "target_oracle_path": str(oracle.resolve()),
            "referenced_paths": [
                str(oracle.resolve()),
                str(oracle_index.resolve()),
            ],
            "specification_only_basis": (
                "元評価は oracles 配下の仕様断片と INDEX だけを参照しました。"
            ),
            "issues": [_eval_oracle_issue("warning", "warning", oracle, 1, 1)],
        }
    ]

    redistributed = review_oracles_module._redistribute_improved_issues(
        evaluations,
        [],
    )

    assert redistributed == [
        {
            "target_oracle_path": str(oracle.resolve()),
            "referenced_paths": [],
            "specification_only_basis": "",
            "issues": [],
        }
    ]


def test_eval_oracles_result_precedence() -> None:
    """result は評価対象数と severity 件数から機械的に決まる。"""
    assert review_oracles_module._evaluation_result(
        0,
        {"fatal": 0, "inconclusive": 0, "warning": 0},
    ) == "no_targets"
    assert review_oracles_module._evaluation_result(
        1,
        {"fatal": 1, "inconclusive": 1, "warning": 1},
    ) == "fatal"
    assert review_oracles_module._evaluation_result(
        1,
        {"fatal": 0, "inconclusive": 1, "warning": 1},
    ) == "minor"
    assert review_oracles_module._evaluation_result(
        1,
        {"fatal": 0, "inconclusive": 0, "warning": 1},
    ) == "minor"
    assert review_oracles_module._evaluation_result(
        1,
        {"fatal": 0, "inconclusive": 0, "warning": 0},
    ) == "ok"
    assert review_oracles_module._evaluation_result(
        1,
        {"fatal": {"accept": 0, "reject": 1}, "minor": {"accept": 0, "reject": 0}},
    ) == "fatal"
    assert review_oracles_module._evaluation_result(
        1,
        {"fatal": {"accept": 0, "reject": 0}, "minor": {"accept": 0, "reject": 1}},
    ) == "minor"


def test_eval_oracles_payload_accepts_existing_oracle_and_index_paths(
    tmp_path: Path,
) -> None:
    """評価 payload は referenced_paths の実在 oracle / INDEX file 参照を受理する。"""
    repo = _init_repo(tmp_path)
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    oracle = oracle_root / "spec.md"
    oracle_index = oracle_root / "INDEX.md"
    oracle.write_text("spec\n", encoding="utf-8")
    oracle_index.write_text("index\n", encoding="utf-8")

    review_oracles_module._validate_evaluation_payload(
        {
            "issues": [
                _eval_oracle_issue(
                    "warning",
                    "warning",
                    oracle,
                    1,
                    1,
                    [oracle, oracle_index],
                ),
            ],
        },
        repo,
        oracle,
    )


def test_eval_oracles_payload_accepts_index_as_issue_oracle_path(
    tmp_path: Path,
) -> None:
    """issues[].oracle_path が INDEX.md でも後処理エラーにしない。"""
    repo = _init_repo(tmp_path)
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    oracle = oracle_root / "spec.md"
    oracle_index = oracle_root / "INDEX.md"
    oracle.write_text("spec\n", encoding="utf-8")
    oracle_index.write_text("index\n", encoding="utf-8")
    issue = _eval_oracle_issue(
        "fatal",
        "fatal",
        oracle_index,
        1,
        1,
        [oracle, oracle_index],
    )

    review_oracles_module._validate_evaluation_payload(
        {
            "issues": [issue],
        },
        repo,
        oracle,
    )


def test_eval_oracles_payload_accepts_other_oracle_as_issue_oracle_path(
    tmp_path: Path,
) -> None:
    """1 file 評価の issue でも別 oracle への oracle_path をエラーにしない。"""
    repo = _init_repo(tmp_path)
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    oracle = oracle_root / "spec.md"
    other_oracle = oracle_root / "other.md"
    oracle.write_text("spec\n", encoding="utf-8")
    other_oracle.write_text("other\n", encoding="utf-8")
    issue = _eval_oracle_issue(
        "fatal",
        "fatal",
        other_oracle,
        1,
        1,
        [oracle, other_oracle],
    )

    review_oracles_module._validate_evaluation_payload(
        {
            "issues": [issue],
        },
        repo,
        oracle,
    )


def test_eval_oracles_payload_rejects_legacy_top_level_metadata(
    tmp_path: Path,
) -> None:
    """評価 payload は top-level の評価対象メタ情報を受理しない。"""
    repo = _init_repo(tmp_path)
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    oracle = oracle_root / "spec.md"
    oracle.write_text("spec\n", encoding="utf-8")

    with pytest.raises(
        ValueError,
        match="Evaluation payload keys do not match schema",
    ):
        review_oracles_module._validate_evaluation_payload(
            {
                "target_oracle_path": str(oracle.resolve()),
                "referenced_paths": [str(oracle.resolve())],
                "specification_only_basis": "oracles 配下の仕様だけを参照しました。",
                "issues": [],
            },
            repo,
            oracle,
        )


def test_eval_oracles_payload_rejects_legacy_issue_metadata(
    tmp_path: Path,
) -> None:
    """issue item は referenced_paths と specification_only_basis を必須にする。"""
    repo = _init_repo(tmp_path)
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    oracle = oracle_root / "spec.md"
    oracle.write_text("spec\n", encoding="utf-8")
    issue = _eval_oracle_issue("warning", "warning", oracle, 1, 1)
    del issue["referenced_paths"]
    del issue["specification_only_basis"]

    with pytest.raises(
        ValueError,
        match="issues\\[0\\] keys do not match schema",
    ):
        review_oracles_module._validate_evaluation_payload(
            {"issues": [issue]},
            repo,
            oracle,
        )


def test_eval_oracles_payload_accepts_empty_referenced_paths(
    tmp_path: Path,
) -> None:
    """issues[].referenced_paths は oracle schema に合わせて空配列を受理する。"""
    repo = _init_repo(tmp_path)
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    oracle = oracle_root / "spec.md"
    oracle.write_text("spec\n", encoding="utf-8")
    issue = _eval_oracle_issue("warning", "warning", oracle, 1, 1)
    issue["referenced_paths"] = []

    review_oracles_module._validate_evaluation_payload(
        {"issues": [issue]},
        repo,
        oracle,
    )


def test_eval_oracles_payload_accepts_empty_specification_only_basis(
    tmp_path: Path,
) -> None:
    """issues[].specification_only_basis は空文字を受理する。"""
    repo = _init_repo(tmp_path)
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    oracle = oracle_root / "spec.md"
    oracle.write_text("spec\n", encoding="utf-8")
    issue = _eval_oracle_issue("warning", "warning", oracle, 1, 1)
    issue["specification_only_basis"] = ""

    review_oracles_module._validate_evaluation_payload(
        {"issues": [issue]},
        repo,
        oracle,
    )


def test_eval_oracles_payload_rejects_missing_referenced_path(
    tmp_path: Path,
) -> None:
    """issues[].referenced_paths は存在しない oracles 配下 path を受理しない。"""
    repo = _init_repo(tmp_path)
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    oracle = oracle_root / "spec.md"
    oracle.write_text("spec\n", encoding="utf-8")

    with pytest.raises(ValueError, match="referenced_paths\\[1\\] must exist"):
        review_oracles_module._validate_evaluation_payload(
            {
                "issues": [
                    _eval_oracle_issue(
                        "warning",
                        "warning",
                        oracle,
                        1,
                        1,
                        [oracle, oracle_root / "missing.md"],
                    ),
                ],
            },
            repo,
            oracle,
        )


def test_eval_oracles_payload_rejects_directory_referenced_path(
    tmp_path: Path,
) -> None:
    """issues[].referenced_paths は directory を参照済みファイルにしない。"""
    repo = _init_repo(tmp_path)
    oracle_root = repo / "oracles"
    oracle_dir = oracle_root / "nested"
    oracle_dir.mkdir(parents=True)
    oracle = oracle_root / "spec.md"
    oracle.write_text("spec\n", encoding="utf-8")

    with pytest.raises(ValueError, match="referenced_paths\\[1\\] must be a file"):
        review_oracles_module._validate_evaluation_payload(
            {
                "issues": [
                    _eval_oracle_issue(
                        "warning",
                        "warning",
                        oracle,
                        1,
                        1,
                        [oracle, oracle_dir],
                    ),
                ],
            },
            repo,
            oracle,
        )


def test_eval_oracles_payload_rejects_ignored_oracle_path(
    tmp_path: Path,
) -> None:
    """issues[].referenced_paths は .gitignore 対象 oracle file を受理しない。"""
    repo = _init_repo(tmp_path)
    (repo / ".gitignore").write_text("oracles/ignored.md\n", encoding="utf-8")
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    oracle = oracle_root / "spec.md"
    ignored_oracle = oracle_root / "ignored.md"
    oracle.write_text("spec\n", encoding="utf-8")
    ignored_oracle.write_text("ignored\n", encoding="utf-8")

    with pytest.raises(
        ValueError,
        match="referenced_paths\\[1\\] must be an oracle file or INDEX.md",
    ):
        review_oracles_module._validate_evaluation_payload(
            {
                "issues": [
                    _eval_oracle_issue(
                        "warning",
                        "warning",
                        oracle,
                        1,
                        1,
                        [oracle, ignored_oracle],
                    ),
                ],
            },
            repo,
            oracle,
        )


def test_eval_oracles_payload_accepts_missing_issue_oracle_path(
    tmp_path: Path,
) -> None:
    """issues[].oracle_path が存在しない oracle path でも後処理エラーにしない。"""
    repo = _init_repo(tmp_path)
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    oracle = oracle_root / "spec.md"
    missing_oracle = oracle_root / "missing.md"
    oracle.write_text("spec\n", encoding="utf-8")
    issue = _eval_oracle_issue("fatal", "fatal", missing_oracle, 1, 1, [oracle])

    review_oracles_module._validate_evaluation_payload(
        {
            "issues": [issue],
        },
        repo,
        oracle,
    )


def test_eval_oracles_payload_accepts_non_oracles_issue_oracle_path(
    tmp_path: Path,
) -> None:
    """issues[].oracle_path が oracles 外でも後処理エラーにしない。"""
    repo = _init_repo(tmp_path)
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    oracle = oracle_root / "spec.md"
    implementation_path = repo / "src" / "app.py"
    oracle.write_text("spec\n", encoding="utf-8")
    issue = _eval_oracle_issue(
        "fatal",
        "fatal",
        implementation_path,
        1,
        1,
        [oracle],
    )

    review_oracles_module._validate_evaluation_payload(
        {
            "issues": [issue],
        },
        repo,
        oracle,
    )


def test_eval_oracles_verdict_text_distinguishes_error() -> None:
    """error や未知の result を ok 相当の Verdict にしない。"""
    ok_verdict = review_oracles_module._verdict_text("ok")
    error_verdict = review_oracles_module._verdict_text("error")
    unknown_verdict = review_oracles_module._verdict_text("unexpected")

    assert "問題点が検出されませんでした" in ok_verdict
    assert "成功評価ではありません" in error_verdict
    assert "問題点が検出されませんでした" not in error_verdict
    assert "成功として扱えません" in unknown_verdict
    assert "問題点が検出されませんでした" not in unknown_verdict


def test_eval_oracles_stays_partial_when_oracle_was_deleted(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """削除済み oracle があっても `--full` なしの session branch は部分評価する。"""
    repo = _init_repo(tmp_path)
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    changed_oracle = oracle_root / "changed.md"
    unchanged_oracle = oracle_root / "unchanged.md"
    deleted_oracle = oracle_root / "deleted.md"
    changed_oracle.write_text("before\n", encoding="utf-8")
    unchanged_oracle.write_text("unchanged\n", encoding="utf-8")
    deleted_oracle.write_text("deleted\n", encoding="utf-8")
    _git(repo, "add", "oracles")
    _git(repo, "commit", "-m", "add oracles")
    _checkout_session_branch(repo)
    changed_oracle.write_text("after\n", encoding="utf-8")
    deleted_oracle.unlink()
    _git(repo, "add", "-A", "oracles")
    _git(repo, "commit", "-m", "change session oracles")

    evaluated_prompts: list[str] = []
    monkeypatch.setattr(
        review_oracles_module,
        "maintain_indexes",
        lambda repo_root: False,
    )

    def fake_codex(*args: object, **kwargs: object) -> str:
        """部分評価対象の prompt を記録し、不整合なしの結果を返す。"""
        evaluated_prompts.append(str(args[1]))
        return json.dumps(
            {"issues": []},
            ensure_ascii=False,
        )

    monkeypatch.setattr(review_oracles_module, "run_codex_exec", fake_codex)

    cmoc_review_oracles_impl(repo, full=False)

    reports = list((repo / ".cmoc" / "reports" / "review_oracles").glob("*.md"))
    report = reports[0].read_text(encoding="utf-8")
    assert len(evaluated_prompts) == 1
    assert str(changed_oracle) in evaluated_prompts[0]
    assert str(unchanged_oracle) not in evaluated_prompts[0]
    assert 'scope: "session"' in report
    assert "oracle_count_total: 2" in report
    assert "oracle_count_evaluated: 1" in report


def test_eval_oracles_full_mode_requires_valid_session_state(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """session branch 上の full mode でも session state を検証する。"""
    repo = _init_repo(tmp_path)
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    existing_oracle = oracle_root / "existing.md"
    deleted_oracle = oracle_root / "deleted.md"
    existing_oracle.write_text("existing\n", encoding="utf-8")
    deleted_oracle.write_text("deleted\n", encoding="utf-8")
    _git(repo, "add", "oracles")
    _git(repo, "commit", "-m", "add oracles")
    _checkout_session_branch(repo)
    deleted_oracle.unlink()
    session_state = next((repo / ".cmoc" / "sessions").glob("*.json"))
    session_state.write_text("{broken\n", encoding="utf-8")

    monkeypatch.setattr(
        review_oracles_module,
        "maintain_indexes",
        lambda repo_root: False,
    )

    def fake_codex(*args: object, **kwargs: object) -> str:
        """full mode の既存 oracle 評価結果を返す。"""
        return json.dumps(
            {"issues": []},
            ensure_ascii=False,
        )

    monkeypatch.setattr(review_oracles_module, "run_codex_exec", fake_codex)

    with pytest.raises(CmocError) as error:
        cmoc_review_oracles_impl(repo, full=True)

    assert "session state ファイルの JSON が不正です。" in error.value.message


def test_eval_oracles_rejects_non_session_branch(tmp_path: Path) -> None:
    """通常 branch 上の `review oracles` は事前条件違反として拒否する。"""
    repo = _init_repo(tmp_path)
    (repo / ".gitignore").write_text("/.cmoc/\n", encoding="utf-8")
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    (oracle_root / "spec.md").write_text("spec\n", encoding="utf-8")
    _git(repo, "add", ".gitignore", "oracles")
    _git(repo, "commit", "-m", "prepare clean normal branch")

    with pytest.raises(CmocError) as error:
        cmoc_review_oracles_impl(repo, full=True)

    assert "`cmoc review oracles` は session branch 上で実行してください。" in (
        error.value.message
    )
    assert "現在の branch:" in error.value.detail


def test_eval_oracles_rejects_missing_session_state(tmp_path: Path) -> None:
    """session state file がない session branch では実行しない。"""
    repo = _init_repo(tmp_path)
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    (oracle_root / "spec.md").write_text("spec\n", encoding="utf-8")
    _prepare_review_oracles_session(repo)
    next((repo / ".cmoc" / "sessions").glob("*.json")).unlink()

    with pytest.raises(CmocError) as error:
        cmoc_review_oracles_impl(repo, full=True)

    assert "session state ファイルが見つかりませんでした。" in error.value.message


def test_eval_oracles_rejects_inactive_session_state(tmp_path: Path) -> None:
    """session.state が active でない session branch では実行しない。"""
    repo = _init_repo(tmp_path)
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    (oracle_root / "spec.md").write_text("spec\n", encoding="utf-8")
    _prepare_review_oracles_session(repo)
    state_path = next((repo / ".cmoc" / "sessions").glob("*.json"))
    state = json.loads(state_path.read_text(encoding="utf-8"))
    state["session"]["state"] = "joined"
    state_path.write_text(json.dumps(state), encoding="utf-8")

    with pytest.raises(CmocError) as error:
        cmoc_review_oracles_impl(repo, full=True)

    assert "active な session ではありません。" in error.value.message
    assert "session.state: joined" in error.value.detail


def test_eval_oracles_rejects_uncommitted_changes(tmp_path: Path) -> None:
    """git 未コミット差分がある session branch では実行しない。"""
    repo = _init_repo(tmp_path)
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    oracle_file = oracle_root / "spec.md"
    oracle_file.write_text("spec\n", encoding="utf-8")
    _prepare_review_oracles_session(repo)
    oracle_file.write_text("changed\n", encoding="utf-8")

    with pytest.raises(CmocError) as error:
        cmoc_review_oracles_impl(repo, full=True)

    assert "未コミットの変更があります。" in error.value.message
    assert str(oracle_file.resolve()) in error.value.detail


def test_eval_oracles_rejects_apply_branch(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """apply branch 上の `review oracles` は事前条件違反として拒否する。"""
    repo = _init_repo(tmp_path)
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    changed_oracle = oracle_root / "changed.md"
    unchanged_oracle = oracle_root / "unchanged.md"
    changed_oracle.write_text("before\n", encoding="utf-8")
    unchanged_oracle.write_text("unchanged\n", encoding="utf-8")
    _git(repo, "add", "oracles")
    _git(repo, "commit", "-m", "add oracles")
    _git(
        repo,
        "checkout",
        "-b",
        "cmoc/apply/2026-05-10_22-21_10_000000123/2026-05-10_22-22_10_000000123",
    )
    changed_oracle.write_text("after\n", encoding="utf-8")

    monkeypatch.setattr(
        review_oracles_module,
        "maintain_indexes",
        lambda repo_root: False,
    )
    evaluated_targets: list[Path] = []

    def fake_codex(*args: object, **kwargs: object) -> str:
        """評価 prompt 内の対象 oracle に対応した結果を返す。"""
        prompt = str(args[1])
        target = (
            changed_oracle
            if str(changed_oracle.resolve()) in prompt
            else unchanged_oracle
        )
        evaluated_targets.append(target)
        return json.dumps(
            {"issues": []},
            ensure_ascii=False,
        )

    monkeypatch.setattr(review_oracles_module, "run_codex_exec", fake_codex)

    with pytest.raises(CmocError) as error:
        cmoc_review_oracles_impl(repo, full=False)

    assert "`cmoc review oracles` は session branch 上で実行してください。" in (
        error.value.message
    )
    assert evaluated_targets == []


def test_review_oracles_body_uses_command_path_module_name() -> None:
    """`review oracles` の本体はコマンド path 対応のモジュールに置く。"""
    repo_root = Path(__file__).resolve().parents[2]

    body = repo_root / "src" / "sub_commands" / "review" / "oracles.py"
    legacy = repo_root / "src" / "sub_commands" / "eval-oracles.py"
    body_text = body.read_text(encoding="utf-8")
    assert "def cmoc_review_oracles_impl" in body_text
    assert "spec_from_file_location" not in body_text
    assert not legacy.exists()


def test_eval_oracles_validation_helpers_are_ordered_caller_first() -> None:
    """同一ファイル内の validation helper は caller first に並べる。"""
    repo_root = Path(__file__).resolve().parents[2]
    source = (
        repo_root / "src" / "sub_commands" / "review" / "oracles.py"
    ).read_text(encoding="utf-8")

    callee = source.index("def _require_issue_oracle_path_string(")
    assert source.index("def _validate_evaluation_payload(") < callee
    assert source.index("def _validate_referenced_paths(") < callee
    assert source.index("def _validate_evaluation_issues(") < callee


def test_eval_oracles_prompt_forbids_implementation_references() -> None:
    """評価 prompt は仕様だけから致命的問題を判断させる。"""
    prompt = _evaluation_prompt(Path("/repo"), Path("/repo/oracles/spec.md"))

    assert "`/repo/oracles` 外のファイルは一切参照禁止です。" in prompt
    assert "`/repo/oracles/INDEX.md` から始まる INDEX.md" in prompt
    assert "`oracles` 外のファイルは一切参照禁止です。" not in prompt
    assert "`oracles/INDEX.md`" not in prompt
    assert "INDEX.md は自動生成されるため評価対象ではありません。" in prompt
    assert "INDEX.md は関連ファイル選定・参照根拠としてだけ読んでください。" in prompt
    assert "実装ファイル、テストファイル、設定ファイル、ビルド成果物も参照禁止です。" in prompt
    assert "各 issue の referenced_paths には参照した仕様ファイル" in prompt
    assert "Structured Output schema に一致する JSON" in prompt
    assert "仕様だけから判断・実装したとき" in prompt


def test_eval_oracles_improvement_prompt_uses_index_routing() -> None:
    """改善 prompt も INDEX のルーティング情報で関連 oracle を選定させる。"""
    prompt = _improvement_prompt(
        Path("/repo"),
        {
            "issues": [
                {
                    "oracle_path": "/repo/oracles/spec.md",
                    "referenced_paths": ["/repo/oracles/INDEX.md"],
                }
            ]
        },
    )

    assert "`/repo/oracles/INDEX.md` から始まる INDEX.md" in prompt
    assert "Read this when / Do not read this when を根拠に、" in prompt
    assert "関連する仕様ファイルを選定してください。" in prompt
    assert "`/repo/oracles` 外のファイルは一切参照禁止です。" in prompt
    assert "`oracles/INDEX.md`" not in prompt
    assert "実装ファイル、テストファイル、設定ファイル、ビルド成果物も参照禁止です。" in prompt


def test_eval_oracles_prompt_orders_completion_before_details() -> None:
    """評価 prompt はロール、作業、完了条件、詳細指示の順にする。"""
    prompt = _evaluation_prompt(Path("/repo"), Path("/repo/oracles/spec.md"))
    lines = prompt.splitlines()

    assert lines[0] == "あなたはソフトウェア仕様のレビュー担当です。"
    assert lines[1] == (
        "`/repo` 内の仕様ファイル `/repo/oracles/spec.md` を評価してください。"
    )
    assert lines[2] == (
        "完了条件は、指定された Structured Output schema に一致する JSON だけを返すことです。"
    )
    assert lines.index(
        "issues には検出した問題点を入れ、問題がない場合は空配列を返してください。"
    ) > 2


def test_eval_oracles_improvement_prompt_orders_completion_before_snapshot_details() -> None:
    """snapshot 付き改善 prompt も完了条件を詳細指示より前に置く。"""
    snapshot = review_oracles_module._OracleEvaluationSnapshot(
        original_repo_root=Path("/repo"),
        original_oracle_root=Path("/repo/oracles"),
        snapshot_root=Path("/snapshot"),
        snapshot_oracle_root=Path("/snapshot/oracles"),
        oracle_files=frozenset({Path("/repo/oracles/spec.md")}),
        reference_files=frozenset({Path("/repo/oracles/spec.md")}),
    )
    prompt = _improvement_prompt(
        Path("/repo"),
        {
            "issues": [
                {
                    "oracle_path": "/repo/oracles/spec.md",
                    "referenced_paths": ["/repo/oracles/INDEX.md"],
                }
            ]
        },
        snapshot,
    )
    lines = prompt.splitlines()

    assert lines[0] == "あなたはソフトウェア仕様レビュー結果の整理担当です。"
    assert lines[1] == (
        "`/repo` の仕様評価で得られた問題点リストを改善してください。"
    )
    assert lines[2] == (
        "完了条件は、指定された Structured Output schema に一致する JSON だけを返すことです。"
    )
    assert lines.index(
        "必要に応じて読む仕様ファイル群は、開始時点の内容を固定したコピー "
        "`/snapshot/oracles` です。"
    ) > 2
