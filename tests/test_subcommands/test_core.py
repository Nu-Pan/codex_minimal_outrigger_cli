"""サブコマンド横断テストを意味カテゴリ別に分割したファイル。"""

from .helpers import *


def test_python_sources_do_not_use_future_annotations() -> None:
    """実装コードは annotations future import を使わない。"""
    src_root = Path(__file__).resolve().parents[2] / "src"
    violating_paths: list[Path] = []

    for path in src_root.rglob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in tree.body:
            if not isinstance(node, ast.ImportFrom):
                continue
            if node.module != "__future__":
                continue
            imported_names = {alias.name for alias in node.names}
            if "annotations" in imported_names:
                violating_paths.append(path.relative_to(src_root.parent))

    assert violating_paths == []


def test_literal_cmoc_error_actions_offer_multiple_choices() -> None:
    """CmocError の静的な actions は oracle 通り複数提示する。"""
    repo_root = Path(__file__).resolve().parents[2]
    violating_locations: list[str] = []

    for source_root in (repo_root / "src", repo_root / "tests"):
        for path in source_root.rglob("*.py"):
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            for node in ast.walk(tree):
                if not isinstance(node, ast.Call):
                    continue
                if getattr(node.func, "id", None) != "CmocError":
                    continue
                actions = None
                if len(node.args) >= 2:
                    actions = node.args[1]
                for keyword in node.keywords:
                    if keyword.arg == "actions":
                        actions = keyword.value
                if not isinstance(actions, ast.List):
                    continue
                if len(actions.elts) < 2:
                    relative_path = path.relative_to(repo_root)
                    violating_locations.append(f"{relative_path}:{node.lineno}")

    assert violating_locations == []


def test_subcommands_do_not_emit_step_timer_report_directly() -> None:
    """ステップ別経過時間は共通の完了サマリー内だけで出す。"""
    repo_root = Path(__file__).resolve().parents[2]
    subcommands_root = repo_root / "src" / "sub_commands"
    violating_locations: list[str] = []

    for path in subcommands_root.rglob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            if not isinstance(node.func, ast.Attribute):
                continue
            if node.func.attr != "report":
                continue
            if not isinstance(node.func.value, ast.Name):
                continue
            if node.func.value.id != "timer":
                continue
            relative_path = path.relative_to(repo_root)
            violating_locations.append(f"{relative_path}:{node.lineno}")

    assert violating_locations == []


def test_run_command_reports_returned_nonzero_exit_code(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """handler が返した非 0 終了コードは共通エラーレポートにする。"""
    repo = _init_repo(tmp_path)
    monkeypatch.chdir(repo)
    monkeypatch.setattr(
        sys,
        "argv",
        ["cmoc", "sample", "--flag", "value"],
    )

    def handler(resolved_repo: Path) -> int:
        """非 0 終了コードを返すサブコマンド本体。"""
        assert resolved_repo == repo
        timer = StepTimer("sample")
        start_step(timer, 1, 1, "first step")
        return 2

    with pytest.raises(typer.Exit) as exit_info:
        run_command(handler, command_path="cmoc sample")

    captured = capsys.readouterr()
    log_files = list((repo / ".cmoc" / "logs" / "sub_commands").glob("*.jsonl"))
    log_events = [
        json.loads(line)
        for line in log_files[0].read_text(encoding="utf-8").splitlines()
    ]
    assert exit_info.value.exit_code == 2
    assert captured.err == ""
    assert len(log_files) == 1
    _assert_markdown_error_report(captured.out)
    assert "サブコマンドがエラー終了しました。" in captured.out
    assert "終了コード 2 を返しました。" in captured.out
    assert "# cmoc subcommand start: cmoc sample" in captured.out
    assert "(1/1) first step" in captured.out
    assert "sample (1/1) first step" not in captured.out
    assert "# Command completion report" in captured.out
    assert f"subcommand log: {log_files[0]}" in captured.out
    assert captured.out.index("# Command completion report") < captured.out.index(
        "sample step timings:"
    )
    assert "sample step timings:" in captured.out
    assert "- 1/1 first step:" in captured.out
    assert "subcommand total elapsed:" in captured.out
    assert "subcommand quota wait elapsed:" in captured.out
    assert "subcommand return code: 2" in captured.out
    assert log_events[0]["event"] == "subcommand_start"
    assert log_events[0]["command_path"] == "cmoc sample"
    assert log_events[0]["argv"] == ["cmoc", "sample", "--flag", "value"]
    assert log_events[0]["cwd"] == str(repo)
    assert log_events[0]["repo_root"] == str(repo)
    assert log_events[0]["subcommand_log"] == str(log_files[0])
    assert any(
        event["event"] == "step_start"
        and event["step"] == "first step"
        and event["step_index"] == "1/1"
        for event in log_events
    )
    assert any(
        event["event"] == "subcommand_end"
        and event["returncode"] == 2
        and event["subcommand_log"] == str(log_files[0])
        for event in log_events
    )
    assert "/.cmoc/logs/" in (repo / ".git" / "info" / "exclude").read_text(
        encoding="utf-8"
    )
    assert _git(repo, "status", "--porcelain").stdout == ""


def test_start_step_logs_hierarchical_step_index(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """階層ステップ番号は console と JSONL の両方に全階層を出す。"""
    repo = _init_repo(tmp_path)
    monkeypatch.chdir(repo)

    def handler(_repo: Path) -> int:
        """階層化されたサブステップ開始を 1 件出す。"""
        timer = StepTimer("sample")
        start_step(
            timer,
            ((5, 6), (2, 3), (1, 4)),
            None,
            "nested step",
        )
        return 0

    run_command(handler)

    captured = capsys.readouterr()
    log_file = next(
        (repo / ".cmoc" / "logs" / "sub_commands").glob("*.jsonl")
    )
    log_content = log_file.read_text(encoding="utf-8")
    log_events = [json.loads(line) for line in log_content.splitlines()]
    assert "(5/6, 2/3, 1/4) nested step" in captured.out
    assert any(
        event["event"] == "step_start"
        and event["step"] == "nested step"
        and event["step_index"] == "5/6, 2/3, 1/4"
        for event in log_events
    )


def test_step_timer_reports_hierarchical_step_timings(
    monkeypatch: MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """完了サマリーは階層 step index ごとに親子の経過時間を出す。"""
    times = iter(float(value) for value in range(12))
    monkeypatch.setattr(timing_module, "perf_counter", lambda: next(times))

    timer = StepTimer("sample")
    start_step(timer, 5, 6, "parent")
    start_step(timer, ((5, 6), (1, 2)), None, "child")
    start_step(timer, ((5, 6), (2, 2)), None, "child")
    start_step(timer, 6, 6, "next")

    timer.report()

    captured = capsys.readouterr()
    assert "- 5/6 parent:  0h  0m  5.0s" in captured.out
    assert "- 5/6, 1/2 child:  0h  0m  1.0s" in captured.out
    assert "- 5/6, 2/2 child:  0h  0m  1.0s" in captured.out
    assert "- 6/6 next:  0h  0m  1.0s" in captured.out


def test_run_command_logs_summary_on_exception(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """例外終了時は stdout へエラーと終了集計を出す。"""
    repo = _init_repo(tmp_path)
    monkeypatch.chdir(repo)

    def handler(_repo: Path) -> None:
        """例外終了するサブコマンド本体として途中進捗を出す。"""
        timer = StepTimer("sample")
        start_step(timer, 1, 1, "failing step")
        raise RuntimeError("boom")

    with pytest.raises(typer.Exit) as exit_info:
        run_command(handler)

    captured = capsys.readouterr()
    log_file = next(
        (repo / ".cmoc" / "logs" / "sub_commands").glob("*.jsonl")
    )
    log_content = log_file.read_text(encoding="utf-8")
    assert exit_info.value.exit_code == 1
    assert captured.err == ""
    _assert_markdown_error_report(captured.out)
    assert "RuntimeError" in captured.out
    assert "boom" in captured.out
    assert "# Command completion report" in captured.out
    assert f"subcommand log: {log_file}" in captured.out
    assert "subcommand return code: 1" in captured.out
    log_events = [json.loads(line) for line in log_content.splitlines()]
    assert any(
        event["event"] == "step_start" and event["step"] == "failing step"
        for event in log_events
    )
    assert any(
        event["event"] == "subcommand_end"
        and event["returncode"] == 1
        and event["subcommand_log"] == str(log_file)
        for event in log_events
    )


def test_run_command_reports_total_elapsed_from_command_entry(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """終了集計の全体経過時間はログ開始ではなく共通入口から測る。"""
    repo = _init_repo(tmp_path)
    monkeypatch.chdir(repo)

    command_times = iter([10.0, 35.0])
    monkeypatch.setattr(
        "commons.command_runner.perf_counter",
        lambda: next(command_times),
    )
    monkeypatch.setattr(
        "commons.subcommand_log.perf_counter",
        lambda: 20.0,
    )

    def handler(_repo: Path) -> None:
        """正常終了する空のサブコマンド本体。"""

    run_command(handler)

    log_content = next(
        (repo / ".cmoc" / "logs" / "sub_commands").glob("*.jsonl")
    ).read_text(encoding="utf-8")
    log_events = [json.loads(line) for line in log_content.splitlines()]
    end_event = next(event for event in log_events if event["event"] == "subcommand_end")
    assert end_event["total_elapsed_seconds"] == 25.0


def test_run_command_reports_nonzero_typer_exit(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """非 0 の typer.Exit も共通エラーレポートとして stdout に出す。"""
    repo = _init_repo(tmp_path)
    monkeypatch.chdir(repo)

    def handler(_repo: Path) -> None:
        """Typer の中断例外でエラー終了するサブコマンド本体。"""
        raise typer.Exit(7)

    with pytest.raises(typer.Exit) as exit_info:
        run_command(handler)

    captured = capsys.readouterr()
    log_content = next(
        (repo / ".cmoc" / "logs" / "sub_commands").glob("*.jsonl")
    ).read_text(encoding="utf-8")
    assert exit_info.value.exit_code == 7
    assert captured.err == ""
    _assert_markdown_error_report(captured.out)
    assert "サブコマンドがエラー終了しました。" in captured.out
    assert "typer.Exit(7)" in captured.out
    assert "raise typer.Exit(7)" in captured.out
    assert "Traceback is not available for this exception." not in captured.out
    assert "# Command completion report" in captured.out
    assert "subcommand return code: 7" in captured.out
    log_events = [json.loads(line) for line in log_content.splitlines()]
    assert any(
        event["event"] == "subcommand_end" and event["returncode"] == 7
        for event in log_events
    )


def test_run_command_treats_apply_unconverged_as_non_error_exit(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """apply fork の未収束区分はエラーレポートなしで終了コードを保持する。"""
    repo = _init_repo(tmp_path)
    monkeypatch.chdir(repo)

    assert APPLY_FORK_EXIT_CODE_CONVERGED == 0
    assert APPLY_FORK_EXIT_CODE_UNCONVERGED not in {
        APPLY_FORK_EXIT_CODE_CONVERGED,
        1,
        2,
    }

    def handler(_repo: Path) -> int:
        """未収束の apply fork 本体と同じ終了コードを返す。"""
        return APPLY_FORK_EXIT_CODE_UNCONVERGED

    with pytest.raises(typer.Exit) as exit_info:
        run_command(
            handler,
            non_error_exit_codes={APPLY_FORK_EXIT_CODE_UNCONVERGED},
        )

    captured = capsys.readouterr()
    log_content = next(
        (repo / ".cmoc" / "logs" / "sub_commands").glob("*.jsonl")
    ).read_text(encoding="utf-8")
    assert exit_info.value.exit_code == APPLY_FORK_EXIT_CODE_UNCONVERGED
    assert captured.err == ""
    assert "ERROR" not in captured.out
    assert "# Command completion report" in captured.out
    assert (
        f"subcommand return code: {APPLY_FORK_EXIT_CODE_UNCONVERGED}"
        in captured.out
    )
    assert f'"returncode": {APPLY_FORK_EXIT_CODE_UNCONVERGED}' in log_content


def test_run_command_reports_repo_root_resolution_error(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """repo root 解決失敗は stdout へエラーと終了集計を出す。"""
    def fail_enter_repo_root() -> Path:
        """repo root 解決に失敗する setup 処理。"""
        raise CmocError(
            "Git リポジトリのルートが見つかりませんでした。",
            [
                "git 管理下のリポジトリへ移動してください。",
                "このディレクトリをリポジトリにする場合は `git init` を実行してください。",
            ],
            f"開始パス: {tmp_path.resolve()}",
        )

    monkeypatch.setattr(
        "commons.command_runner.enter_repo_root",
        fail_enter_repo_root,
    )

    def handler(_repo: Path) -> None:
        """repo root 解決に失敗するため呼ばれない。"""
        raise AssertionError("handler must not be called")

    with pytest.raises(typer.Exit) as exit_info:
        run_command(handler)

    captured = capsys.readouterr()
    assert exit_info.value.exit_code == 1
    assert captured.err == ""
    _assert_markdown_error_report(captured.out)
    assert "Git リポジトリのルートが見つかりませんでした。" in captured.out
    assert f"開始パス: {tmp_path.resolve()}" in captured.out
    assert "# Command completion report" in captured.out
    assert "subcommand log: unavailable" in captured.out
    assert "subcommand total elapsed:" in captured.out
    assert "subcommand quota wait elapsed:" in captured.out
    assert "subcommand return code: 1" in captured.out
    assert not (tmp_path / ".cmoc" / "logs" / "sub_commands").exists()


def test_init_adds_cmoc_ignore_and_commits_it(tmp_path: Path) -> None:
    """`cmoc init` は `.cmoc` ignore ルールを commit する。"""
    repo = _init_repo(tmp_path)

    cmoc_init_impl(repo)

    assert ".cmoc" in (repo / ".gitignore").read_text(encoding="utf-8")
    assert _git(repo, "status", "--porcelain").stdout == ""
    assert (
        _git(repo, "log", "-1", "--pretty=%s").stdout.strip()
        == "Initialize cmoc"
    )


def test_indexing_impl_runs_maintenance_on_clean_repo(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """`cmoc indexing` 本体は clean repo で INDEX メンテナンスへ委譲する。"""
    repo = _init_repo(tmp_path)
    maintained_roots: list[Path] = []

    def fake_maintain_indexes(repo_root: Path) -> bool:
        maintained_roots.append(repo_root)
        return True

    monkeypatch.setattr(
        indexing_module,
        "maintain_indexes",
        fake_maintain_indexes,
    )

    cmoc_indexing_impl(repo)

    captured = capsys.readouterr()
    assert maintained_roots == [repo]
    assert "committed INDEX.md maintenance changes" in captured.out


def test_indexing_impl_rejects_dirty_repo_before_maintenance(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """`cmoc indexing` は実行前の未コミット差分があれば止まる。"""
    repo = _init_repo(tmp_path)
    (repo / "dirty.txt").write_text("dirty\n", encoding="utf-8")
    maintained_roots: list[Path] = []

    def fake_maintain_indexes(repo_root: Path) -> bool:
        maintained_roots.append(repo_root)
        return True

    monkeypatch.setattr(
        indexing_module,
        "maintain_indexes",
        fake_maintain_indexes,
    )

    with pytest.raises(CmocError) as error:
        cmoc_indexing_impl(repo)

    assert maintained_roots == []
    assert "未コミットの変更があります。" in error.value.message
    assert "dirty.txt" in error.value.detail


def test_init_repairs_negated_cmoc_ignore_rule_and_commits_it(
    tmp_path: Path,
) -> None:
    """`cmoc init` は negation で無効な既存 `/.cmoc/` も補修して commit する。"""
    repo = _init_repo(tmp_path)
    (repo / ".gitignore").write_text("/.cmoc/\n!/.cmoc/\n", encoding="utf-8")
    _git(repo, "add", ".gitignore")
    _git(repo, "commit", "-m", "add ineffective cmoc ignore")

    cmoc_init_impl(repo)

    assert (repo / ".gitignore").read_text(encoding="utf-8") == (
        "/.cmoc/\n!/.cmoc/\n/.cmoc/\n"
    )
    assert _git(repo, "ls-files", "--", ".cmoc").stdout == ""
    assert (
        _git(
            repo,
            "check-ignore",
            "-q",
            "--",
            ".cmoc/.__cmoc_ignore_probe__",
        ).returncode
        == 0
    )
    assert _git(repo, "show", "HEAD:.gitignore").stdout == (
        "/.cmoc/\n!/.cmoc/\n/.cmoc/\n"
    )
    assert _git(repo, "status", "--porcelain").stdout == ""
    assert (
        _git(repo, "log", "-1", "--pretty=%s").stdout.strip()
        == "Initialize cmoc"
    )


def test_init_untracks_existing_cmoc_file_and_commits_it(
    tmp_path: Path,
) -> None:
    """`cmoc init` は tracked `.cmoc` ファイルの追跡解除も commit する。"""
    repo = _init_repo(tmp_path)
    cmoc_file = repo / ".cmoc" / "logs" / "tracked.log"
    cmoc_file.parent.mkdir(parents=True)
    cmoc_file.write_text("tracked\n", encoding="utf-8")
    _git(repo, "add", "-f", ".cmoc/logs/tracked.log")
    _git(repo, "commit", "-m", "track cmoc")

    cmoc_init_impl(repo)

    assert _git(repo, "ls-files", "--", ".cmoc").stdout == ""
    assert cmoc_file.exists()
    assert _git(repo, "status", "--porcelain").stdout == ""
    last_commit_paths = _git(
        repo,
        "show",
        "--name-only",
        "--pretty=format:",
        "HEAD",
    ).stdout
    assert ".gitignore" in last_commit_paths
    assert ".cmoc/logs/tracked.log" in last_commit_paths


def test_init_untracks_modified_cmoc_file_and_keeps_worktree_file(
    tmp_path: Path,
) -> None:
    """差分あり tracked `.cmoc` でも init を完了し、実ファイルは残す。"""
    repo = _init_repo(tmp_path)
    cmoc_file = repo / ".cmoc" / "logs" / "tracked.log"
    cmoc_file.parent.mkdir(parents=True)
    cmoc_file.write_text("tracked\n", encoding="utf-8")
    _git(repo, "add", "-f", ".cmoc/logs/tracked.log")
    _git(repo, "commit", "-m", "track cmoc")
    cmoc_file.write_text("staged\n", encoding="utf-8")
    _git(repo, "add", "-f", ".cmoc/logs/tracked.log")
    cmoc_file.write_text("worktree\n", encoding="utf-8")

    cmoc_init_impl(repo)

    assert _git(repo, "ls-files", "--", ".cmoc").stdout == ""
    assert (
        _git(
            repo,
            "check-ignore",
            "-q",
            "--",
            ".cmoc/.__cmoc_ignore_probe__",
        ).returncode
        == 0
    )
    assert cmoc_file.read_text(encoding="utf-8") == "worktree\n"
    assert _git(repo, "status", "--porcelain").stdout == ""
    last_commit_paths = _git(
        repo,
        "show",
        "--name-only",
        "--pretty=format:",
        "HEAD",
    ).stdout
    assert ".gitignore" in last_commit_paths
    assert ".cmoc/logs/tracked.log" in last_commit_paths


def test_init_does_not_commit_existing_gitignore_changes(
    tmp_path: Path,
) -> None:
    """`cmoc init` は既存 `.gitignore` 差分を初期化 commit に混ぜない。"""
    repo = _init_repo(tmp_path)
    (repo / ".gitignore").write_text("user-rule\n", encoding="utf-8")

    cmoc_init_impl(repo)

    gitignore = (repo / ".gitignore").read_text(encoding="utf-8")
    committed_gitignore = _git(repo, "show", "HEAD:.gitignore").stdout
    assert gitignore == "user-rule\n/.cmoc/\n"
    assert committed_gitignore == "/.cmoc/\n"
    assert _git(repo, "log", "-1", "--pretty=%s").stdout.strip() == (
        "Initialize cmoc"
    )
    assert _git(repo, "status", "--porcelain").stdout == " M .gitignore\n"


def test_init_does_not_commit_preexisting_staged_changes(
    tmp_path: Path,
) -> None:
    """`cmoc init` は実行前から stage 済みの別差分を commit に混ぜない。"""
    repo = _init_repo(tmp_path)
    staged_file = repo / "feature.txt"
    staged_file.write_text("user staged\n", encoding="utf-8")
    _git(repo, "add", "feature.txt")

    cmoc_init_impl(repo)

    assert _git(repo, "log", "-1", "--pretty=%s").stdout.strip() == (
        "Initialize cmoc"
    )
    last_commit_paths = _git(
        repo,
        "show",
        "--name-only",
        "--pretty=format:",
        "HEAD",
    ).stdout.splitlines()
    assert last_commit_paths == [".gitignore"]
    assert _git(repo, "diff", "--cached", "--name-only").stdout == (
        "feature.txt\n"
    )


def test_init_keeps_head_when_preexisting_staged_restore_fails(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """既存 staged 差分を戻せない場合、`cmoc init` は HEAD を進めない。"""
    repo = _init_repo(tmp_path)
    base_head = _git(repo, "rev-parse", "HEAD").stdout.strip()
    staged_file = repo / "feature.txt"
    staged_file.write_text("user staged\n", encoding="utf-8")
    _git(repo, "add", "feature.txt")

    def fail_apply_staged_diff(
        repo_root: Path,
        staged_diff: str,
        env: dict[str, str],
    ) -> subprocess.CompletedProcess[str]:
        assert repo_root == repo
        assert staged_diff
        assert env.get("GIT_INDEX_FILE")
        assert _git(repo, "rev-parse", "HEAD").stdout.strip() == base_head
        return subprocess.CompletedProcess(
            ["git", "apply", "--cached", "--3way"],
            1,
            "",
            "forced restore failure",
        )

    monkeypatch.setattr(
        repo_module,
        "_apply_staged_diff_to_index",
        fail_apply_staged_diff,
    )

    with pytest.raises(CmocError):
        cmoc_init_impl(repo)

    assert _git(repo, "rev-parse", "HEAD").stdout.strip() == base_head
    assert _git(repo, "log", "-1", "--pretty=%s").stdout.strip() == "initial"
    assert _git(repo, "diff", "--cached", "--name-only").stdout == (
        "feature.txt\n"
    )


def test_init_does_not_restore_preexisting_staged_cmoc_changes(
    tmp_path: Path,
) -> None:
    """実行前に stage 済みの `.cmoc` 差分も最終的に追跡対象外にする。"""
    repo = _init_repo(tmp_path)
    cmoc_file = repo / ".cmoc" / "logs" / "staged.log"
    cmoc_file.parent.mkdir(parents=True)
    cmoc_file.write_text("user staged\n", encoding="utf-8")
    _git(repo, "add", "-f", ".cmoc/logs/staged.log")

    cmoc_init_impl(repo)

    assert _git(repo, "ls-files", "--", ".cmoc").stdout == ""
    assert _git(
        repo,
        "check-ignore",
        "-q",
        "--",
        ".cmoc/.__cmoc_ignore_probe__",
    ).returncode == 0
    assert ".cmoc" not in _git(
        repo,
        "diff",
        "--cached",
        "--name-only",
    ).stdout
    assert cmoc_file.exists()


def test_init_can_create_first_commit(tmp_path: Path) -> None:
    """`cmoc init` は unborn HEAD のリポジトリでも初期化 commit を作る。"""
    repo = tmp_path / "repo"
    repo.mkdir()
    _git(repo, "init")
    _git(repo, "config", "user.email", "test@example.com")
    _git(repo, "config", "user.name", "Test User")

    cmoc_init_impl(repo)

    assert _git(repo, "log", "-1", "--pretty=%s").stdout.strip() == (
        "Initialize cmoc"
    )
    assert _git(repo, "status", "--porcelain").stdout == ""


def test_init_first_commit_keeps_existing_gitignore_content(
    tmp_path: Path,
) -> None:
    """unborn HEAD の初期 commit は既存 `.gitignore` 内容も保持する。"""
    repo = tmp_path / "repo"
    repo.mkdir()
    _git(repo, "init")
    _git(repo, "config", "user.email", "test@example.com")
    _git(repo, "config", "user.name", "Test User")
    (repo / ".gitignore").write_text("user-rule\n", encoding="utf-8")

    cmoc_init_impl(repo)

    assert (repo / ".gitignore").read_text(encoding="utf-8") == (
        "user-rule\n/.cmoc/\n"
    )
    assert _git(repo, "show", "HEAD:.gitignore").stdout == (
        "user-rule\n/.cmoc/\n"
    )
    assert _git(repo, "status", "--porcelain").stdout == ""


def test_init_can_create_first_commit_with_existing_cmoc_ignore_rule(
    tmp_path: Path,
) -> None:
    """既存 ignore rule 付き unborn HEAD でも初期 commit を作る。"""
    repo = tmp_path / "repo"
    repo.mkdir()
    _git(repo, "init")
    _git(repo, "config", "user.email", "test@example.com")
    _git(repo, "config", "user.name", "Test User")
    (repo / ".gitignore").write_text("user-rule\n/.cmoc/\n", encoding="utf-8")

    cmoc_init_impl(repo)
    init_head = _git(repo, "rev-parse", "HEAD").stdout.strip()

    cmoc_session_fork_impl(repo)

    state_paths = _session_state_paths(repo)
    session_state = json.loads(state_paths[0].read_text(encoding="utf-8"))
    assert _git(repo, "show", "HEAD:.gitignore").stdout == (
        "user-rule\n/.cmoc/\n"
    )
    assert _git(repo, "status", "--porcelain").stdout == ""
    assert session_state["session"]["session_start_commit"] == init_head
