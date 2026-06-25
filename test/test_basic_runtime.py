import tomllib

from basic.acp import AgentCallParameter
from commons.runtime_codex_profile import build_codex_profile

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


def test_format_duration_truncates_msec_digit_and_space_pads_time_parts() -> None:
    assert format_duration(0.19) == " 0h  0m  0.1s"
    assert format_duration(3.19) == " 0h  0m  3.1s"
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
    next_actions = rendered.split("## Next actions\n", 1)[1].split("## Detail", 1)[0]
    assert sum(line.startswith("- ") for line in next_actions.splitlines()) >= 2
    assert "## Detail\ndetail" in rendered
    assert "## Call stack" in rendered


def test_render_error_fills_empty_next_actions() -> None:
    try:
        raise CmocError("summary", [], "detail")
    except CmocError as exc:
        rendered = render_error(exc)

    next_actions = rendered.split("## Next actions\n", 1)[1].split("## Detail", 1)[0]
    assert sum(line.startswith("- ") for line in next_actions.splitlines()) >= 2
    assert "入力、実行場所、設定、作業ツリー状態に問題がある場合" in next_actions
    assert "原因が実装不具合または仕様不足に見える場合" in next_actions


def test_cli_error_report_is_written_to_stderr(tmp_path: Path, monkeypatch) -> None:
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    run_git(root, "switch", "--detach", "HEAD")

    result = runner.invoke(app, ["session", "fork"])

    assert result.exit_code != 0
    assert "# ERROR" in result.stderr
    assert "detached HEAD 上では実行できません。" in result.stderr
    assert "# ERROR" not in result.stdout
    assert "detached HEAD 上では実行できません。" not in result.stdout


def test_cli_parse_error_report_is_written_to_stderr() -> None:
    result = runner.invoke(app, ["--bad-option"])

    assert result.exit_code != 0
    assert "# ERROR" in result.stderr
    assert "CLI 引数解析に失敗しました。" in result.stderr
    assert "No such option: --bad-option" in result.stderr
    assert "# ERROR" not in result.stdout
    assert "CLI 引数解析に失敗しました。" not in result.stdout
    assert "No such option: --bad-option" not in result.stdout


def test_cli_requires_current_directory_to_be_work_root(
    tmp_path: Path, monkeypatch
) -> None:
    root = make_repo(tmp_path)
    monkeypatch.chdir(root / "oracle")

    result = runner.invoke(app, ["init"])

    assert result.exit_code != 0
    assert "# ERROR" in result.stderr
    assert "cmoc は work root で実行してください。" in result.stderr
    assert f"cwd: {(root / 'oracle').resolve()}" in result.stderr
    assert f"work_root: {root.resolve()}" in result.stderr
    assert "# ERROR" not in result.stdout
    assert "cmoc は work root で実行してください。" not in result.stdout
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


def test_codex_profile_contains_file_access_enforcement(tmp_path: Path) -> None:
    root = tmp_path / "repo"
    root.mkdir()

    def profile(mode: FileAccessMode) -> dict:
        return tomllib.loads(
            build_codex_profile(
                AgentCallParameter(
                    ModelClass.EFFICIENCY,
                    ReasoningEffort.LOW,
                    mode,
                    "prompt",
                    None,
                ),
                CmocConfig(),
                root,
            )
        )

    readonly = profile(FileAccessMode.READONLY)
    assert readonly["sandbox_mode"] == "read-only"
    assert "sandbox_workspace_write" not in readonly

    realization = profile(FileAccessMode.REALIZATION_WRITE)["sandbox_workspace_write"]
    assert realization["writable_roots"] == [str(root)]
    assert realization["read_only_paths"] == [
        str(root / "oracle"),
        str(root / "memo"),
        str(root / ".agents"),
    ]

    oracle = profile(FileAccessMode.ORACLE_WRITE)["sandbox_workspace_write"]
    assert oracle["writable_roots"] == [str(root / "oracle")]
    assert oracle["read_only_paths"] == [str(root / "memo"), str(root / ".agents")]

    repo = profile(FileAccessMode.REPO_WRITE)["sandbox_workspace_write"]
    assert repo["writable_roots"] == [str(root)]
    assert repo["read_only_paths"] == [str(root / "memo"), str(root / ".agents")]
