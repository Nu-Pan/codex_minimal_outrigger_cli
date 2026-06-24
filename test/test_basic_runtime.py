from _support import (
    CmocConfig,
    CmocError,
    FileAccessMode,
    ModelClass,
    Path,
    ReasoningEffort,
    RootToken,
    app,
    ensure_cmoc_ignored,
    file_access_to_sandbox_mode,
    format_duration,
    main_module,
    make_repo,
    render_error,
    repo_root,
    resolve_real_path,
    resolve_token_path,
    run_git,
    runner,
    subprocess,
    sys,
    work_root,
)

def test_path_model_resolves_token_path_inside_repo() -> None:
    cmoc_root = resolve_real_path(RootToken.CMOC)
    token_path = resolve_token_path(cmoc_root / "src", RootToken.CMOC)

    assert token_path == Path("<cmoc-root>") / "src"


def test_format_duration_truncates_msec_digit() -> None:
    assert format_duration(0.19) == " 0h  0m 00.1s"
    assert format_duration(59.99) == " 0h  0m 59.9s"


def test_runtime_distinguishes_repo_root_from_linked_worktree(
    tmp_path: Path,
) -> None:
    root = make_repo(tmp_path)
    linked = root / ".cmoc" / "worktrees" / "linked"
    run_git(root, "worktree", "add", "-b", "linked-test", str(linked), "HEAD")

    assert repo_root(linked) == root.resolve()
    assert work_root(linked) == linked.resolve()


def test_config_defaults_match_logical_model_classes() -> None:
    config = CmocConfig()

    assert config.num_parallel == 8
    assert config.codex.model[ModelClass.MAINSTREAM] == "GPT-5.5"
    assert config.codex.reasoning_effort[ReasoningEffort.HIGH] == "high"


def test_render_error_uses_structured_markdown() -> None:
    try:
        raise CmocError("summary", ["next"], "detail")
    except CmocError as exc:
        rendered = render_error(exc)

    assert "# ERROR" in rendered
    assert "## Summary\nsummary" in rendered
    assert "- next" in rendered
    assert "## Detail\ndetail" in rendered
    assert "## Call stack" in rendered


def test_render_error_fills_empty_next_actions() -> None:
    try:
        raise CmocError("summary", [], "detail")
    except CmocError as exc:
        rendered = render_error(exc)

    assert "## Next actions\n- エラー内容を確認し" in rendered


def test_cli_error_report_is_written_to_stdout(tmp_path: Path, monkeypatch) -> None:
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    run_git(root, "switch", "--detach", "HEAD")

    result = runner.invoke(app, ["session", "fork"])

    assert result.exit_code != 0
    assert "# ERROR" in result.output
    assert "detached HEAD 上では実行できません。" in result.output
    assert result.stderr == ""


def test_cli_requires_current_directory_to_be_work_root(
    tmp_path: Path, monkeypatch
) -> None:
    root = make_repo(tmp_path)
    monkeypatch.chdir(root / "oracle")

    result = runner.invoke(app, ["init"])

    assert result.exit_code != 0
    assert "# ERROR" in result.output
    assert "cmoc は work root で実行してください。" in result.output
    assert f"cwd: {(root / 'oracle').resolve()}" in result.output
    assert f"work_root: {root.resolve()}" in result.output
    assert not (root / ".gitignore").exists()


def test_cli_completion_probe_skips_cmoc_preflight_and_side_effects(
    tmp_path: Path,
) -> None:
    root = make_repo(tmp_path)
    main_path = Path(main_module.__file__).resolve()
    result = subprocess.run(
        [sys.executable, str(main_path), "init"],
        cwd=root,
        env={"PYTHONPATH": str(main_path.parent), "_CMOC_COMPLETE": "bash_complete"},
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode != 0
    assert "# ERROR" not in result.stdout + result.stderr
    assert "sub_command_log" not in result.stdout + result.stderr
    assert not (root / ".gitignore").exists()
    assert not (root / ".cmoc").exists()


def test_ensure_cmoc_ignored_updates_gitignore(tmp_path: Path) -> None:
    root = make_repo(tmp_path)

    ensure_cmoc_ignored(root)

    assert "/.cmoc/" in (root / ".gitignore").read_text()
    ignored = subprocess.run(
        ["git", "check-ignore", "-q", ".cmoc/.__cmoc_ignore_probe__"],
        cwd=root,
    )
    assert ignored.returncode == 0

def test_file_access_mode_values_are_json_ready() -> None:
    assert FileAccessMode.READONLY.value == "readonly"
    assert FileAccessMode.REPO_WRITE.value == "repo_write"


def test_file_access_to_sandbox_mode_supports_repo_write() -> None:
    assert file_access_to_sandbox_mode(FileAccessMode.READONLY) == "read-only"
    assert file_access_to_sandbox_mode(FileAccessMode.PURE_ORACLE_READ) == "read-only"
    assert file_access_to_sandbox_mode(FileAccessMode.REALIZATION_WRITE) == "workspace-write"
    assert file_access_to_sandbox_mode(FileAccessMode.ORACLE_WRITE) == "workspace-write"
    assert file_access_to_sandbox_mode(FileAccessMode.REPO_WRITE) == "workspace-write"
