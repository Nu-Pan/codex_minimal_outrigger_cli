"""cmoc の基礎 runtime 境界を横断して検証する。

このファイルは 16,000 文字を超えるが、責務境界は個別サブコマンドより下の
共通 runtime 契約に閉じている。root 解決、config、CmocError、CLI error 表示、
subcommand log、FileAccessMode、binary 判定は実行前提として一緒に崩れやすく、
分割すると共通 fixture と root 状態の読み取り文脈が分散する。現状は basic runtime
回帰として一箇所に保つ方が凝集性が高い。
根拠: <work-root>/oracle/src/oracle/prompt_builder/parts/realization_standard.py
"""

import shutil
import subprocess
import sys
import tomllib
from pathlib import Path

import pytest
import main as main_module
import commons.runtime_logging as runtime_logging
from basic.acp import AgentCallParameter, FileAccessMode, ModelClass, ReasoningEffort
from basic.path_model import (
    RootPathPlaceHolder,
    resolve_real_path,
    resolve_ph_path,
)
from cmoc_runtime import (
    CmocError,
    SubcommandLogger,
    config_from_dict,
    create_run_worktree,
    ensure_cmoc_ignored,
    file_access_to_sandbox_mode,
    format_duration,
    remove_worktree,
    render_error,
    repo_root,
    work_root,
)
from commons.runtime_codex_profile import build_codex_profile, file_access_to_codex_cwd
from commons.runtime_content import is_binary
from commons.runtime_state import (
    SessionState,
    apply_branch_session_id,
    branch_session_id,
    load_state_for_branch,
    state_path,
    write_state,
)
from config.cmoc_config import CmocConfig
from main import app

from _support import (
    make_repo,
    run_git,
    runner,
)


def _profile_writable_roots(profile: str) -> set[str]:
    parsed = tomllib.loads(profile)
    return set(parsed.get("sandbox_workspace_write", {}).get("writable_roots", []))


def _assert_writable(profile: str, path: Path) -> None:
    target = path.resolve()
    assert any(
        target.is_relative_to(Path(root)) for root in _profile_writable_roots(profile)
    )


def test_path_model_resolves_token_path_inside_repo() -> None:
    """root placeholder path が repo 内の実 path から復元できる契約を固定する。"""
    cmoc_root = resolve_real_path(RootPathPlaceHolder.CMOC)
    token_path = resolve_ph_path(cmoc_root / "src", RootPathPlaceHolder.CMOC)

    assert token_path == Path("<cmoc-root>") / "src"


def test_format_duration_truncates_msec_digit_and_space_pads_time_parts() -> None:
    """duration 表示は丸めず切り捨て、時分秒の幅を揃える。"""
    assert format_duration(0.19) == " 0h  0m  0.1s"
    assert format_duration(3.19) == " 0h  0m  3.1s"
    assert format_duration(59.99) == " 0h  0m 59.9s"


def test_make_repo_ignores_global_commit_signing_and_hooks(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    hooks = tmp_path / "hooks"
    hooks.mkdir()
    hook = hooks / "pre-commit"
    hook.write_text("#!/bin/sh\nexit 1\n")
    hook.chmod(0o755)
    global_config = tmp_path / "gitconfig"
    global_config.write_text(
        f"[commit]\n\tgpgsign = true\n[core]\n\thooksPath = {hooks}\n"
    )
    monkeypatch.setenv("GIT_CONFIG_GLOBAL", str(global_config))

    root = make_repo(tmp_path)

    assert run_git(root, "config", "--local", "commit.gpgsign").stdout == "false\n"
    assert run_git(root, "config", "--local", "core.hooksPath").stdout == "/dev/null\n"
    assert run_git(root, "rev-parse", "--verify", "HEAD").stdout.strip()


def test_subcommand_logger_keeps_one_file_per_command_on_timestamp_collision(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    timestamps = iter(
        [
            "2026-06-27_10-00_00_000001000",
            "2026-06-27_10-00_00_000001000",
            "2026-06-27_10-00_00_000002000",
        ]
    )
    monkeypatch.setattr(runtime_logging, "timestamp", lambda: next(timestamps))

    first = SubcommandLogger(tmp_path, "first")
    second = SubcommandLogger(tmp_path, "second")
    first.event("marker")
    second.event("marker")

    assert first.path.name == "2026-06-27_10-00_00_000001000.jsonl"
    assert second.path.name == "2026-06-27_10-00_00_000002000.jsonl"
    assert [line for line in first.path.read_text().splitlines() if line]
    assert [line for line in second.path.read_text().splitlines() if line]


def test_runtime_distinguishes_repo_root_from_linked_worktree(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """linked worktree では repo root と run/work root を分けて扱う。"""
    root = make_repo(tmp_path)
    linked = root / ".cmoc" / "local" / "worktree" / "linked"
    run_git(root, "worktree", "add", "-b", "linked-test", str(linked), "HEAD")

    monkeypatch.chdir(linked)
    assert repo_root(linked) == root.resolve()
    assert resolve_real_path(RootPathPlaceHolder.RUN) == linked.resolve()
    assert work_root(linked) == linked.resolve()


def test_run_root_placeholder_rejects_main_worktree(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """main worktree は run root として扱わない。"""
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)

    with pytest.raises(ValueError, match="`<run-root>` was not found"):
        resolve_real_path(RootPathPlaceHolder.RUN)


def test_create_run_worktree_rejects_path_outside_managed_worktrees(
    tmp_path: Path,
) -> None:
    root = make_repo(tmp_path)
    target = tmp_path / "unrelated"
    target.mkdir()
    (target / "keep.txt").write_text("keep\n")

    with pytest.raises(CmocError, match="run worktree path"):
        create_run_worktree(root, "cmoc/apply/session/run", target)

    assert (target / "keep.txt").read_text() == "keep\n"


def test_create_run_worktree_rejects_path_not_matching_branch(
    tmp_path: Path,
) -> None:
    root = make_repo(tmp_path)
    target = root / ".cmoc" / "local" / "worktree" / "session" / "other-run"
    target.mkdir(parents=True)
    (target / "keep.txt").write_text("keep\n")

    with pytest.raises(CmocError, match="run worktree path"):
        create_run_worktree(root, "cmoc/apply/session/run", target)

    assert (target / "keep.txt").read_text() == "keep\n"


def test_remove_worktree_rejects_path_outside_managed_worktrees(
    tmp_path: Path,
) -> None:
    root = make_repo(tmp_path)
    target = tmp_path / "unrelated"
    target.mkdir()
    (target / "keep.txt").write_text("keep\n")

    with pytest.raises(CmocError, match="cmoc 管理外の worktree"):
        remove_worktree(root, target)

    assert (target / "keep.txt").read_text() == "keep\n"


def test_config_defaults_match_logical_model_classes() -> None:
    """既定 config が論理 model class と reasoning effort を埋める。"""
    config = CmocConfig()

    assert config.num_parallel == 8
    assert config.codex.model[ModelClass.MAINSTREAM] == "gpt-5.5"
    assert config.codex.reasoning_effort[ReasoningEffort.HIGH] == "high"
    assert config.codex.num_try_falv_recovery == 1


@pytest.mark.parametrize("value", [False, None, [], {}])
@pytest.mark.parametrize(
    ("field", "key"),
    [
        ("model", "mainstream"),
        ("reasoning_effort", "low"),
    ],
)
def test_config_rejects_non_string_codex_names(
    field: str,
    key: str,
    value: object,
) -> None:
    with pytest.raises(CmocError) as exc_info:
        config_from_dict({"codex": {field: {key: value}}})

    assert exc_info.value.summary == "cmoc config が不正です。"


@pytest.mark.parametrize("field", ["model", "reasoning_effort"])
@pytest.mark.parametrize("value", [None, [], "invalid"])
def test_config_rejects_non_object_codex_name_maps(
    field: str, value: object
) -> None:
    with pytest.raises(CmocError) as exc_info:
        config_from_dict({"codex": {field: value}})

    assert exc_info.value.summary == "cmoc config が不正です。"


@pytest.mark.parametrize("section", ["codex", "apply_fork", "review_oracle"])
@pytest.mark.parametrize("value", [None, [], "invalid"])
def test_config_rejects_non_object_sections(section: str, value: object) -> None:
    with pytest.raises(CmocError) as exc_info:
        config_from_dict({section: value})

    assert exc_info.value.summary == "cmoc config が不正です。"


@pytest.mark.parametrize(
    "data",
    [
        {"num_parallel": True},
        {"num_parallel": "3"},
        {"codex": {"num_try_falv_recovery": False}},
        {"codex": {"num_try_falv_recovery": "1"}},
        {"apply_fork": {"num_apply_files": True}},
        {"apply_fork": {"num_apply_files": "200"}},
        {"review_oracle": {"num_enumerate_findings_loop": False}},
        {"review_oracle": {"num_enumerate_findings_loop": "2"}},
        {"review_oracle": {"num_merge_findings_loop": True}},
        {"review_oracle": {"num_merge_findings_loop": "2"}},
        {"review_oracle": {"num_validate_findings_loop": False}},
        {"review_oracle": {"num_validate_findings_loop": "2"}},
    ],
)
def test_config_rejects_non_integer_count_values(data: dict[str, object]) -> None:
    with pytest.raises(CmocError) as exc_info:
        config_from_dict(data)

    assert exc_info.value.summary == "cmoc config が不正です。"


def test_render_error_uses_structured_markdown() -> None:
    """CmocError は利用者が読む Markdown report として整形される。"""
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
    """next actions 未指定でも回復行動の既定文を出す。"""
    try:
        raise CmocError("summary", [], "detail")
    except CmocError as exc:
        rendered = render_error(exc)

    next_actions = rendered.split("## Next actions\n", 1)[1].split("## Detail", 1)[0]
    assert sum(line.startswith("- ") for line in next_actions.splitlines()) >= 2
    assert "入力、実行場所、設定、作業ツリー状態に問題がある場合" in next_actions
    assert "原因が実装不具合または仕様不足に見える場合" in next_actions


@pytest.mark.parametrize(
    "branch",
    [
        "cmoc/session/",
        "cmoc/session/2026-06-24_20-40_40_571606000/extra",
    ],
)
def test_branch_session_id_rejects_invalid_session_branch_shape(branch: str) -> None:
    """session branch 名の余分な区切りや空 session id を拒否する。"""
    with pytest.raises(CmocError):
        branch_session_id(branch)


@pytest.mark.parametrize(
    "branch",
    [
        "cmoc/apply/",
        "cmoc/apply/session",
        "cmoc/apply/session/run/extra",
    ],
)
def test_apply_branch_session_id_rejects_invalid_apply_branch_shape(branch: str) -> None:
    """apply branch 名は session id と run id の 2 要素だけを受け付ける。"""
    with pytest.raises(CmocError):
        apply_branch_session_id(branch)


def test_load_state_for_branch_rejects_apply_branch_with_extra_parts(tmp_path: Path) -> None:
    """破損した apply branch 名から session state を誤って読まない。"""
    path = state_path(tmp_path, "session")
    write_state(path, SessionState())

    with pytest.raises(CmocError):
        load_state_for_branch(tmp_path, "cmoc/apply/session/run/extra")


def test_cli_error_report_is_written_to_stdout(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """想定済み CLI error は stderr ではなく stdout report として返す。"""
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    run_git(root, "switch", "--detach", "HEAD")

    result = runner.invoke(app, ["session", "fork"])

    assert result.exit_code != 0
    assert "# ERROR" in result.stdout
    assert "detached HEAD 上では実行できません。" in result.stdout
    assert "# ERROR" not in result.stderr
    assert "detached HEAD 上では実行できません。" not in result.stderr


def test_cli_parse_error_report_is_written_to_stdout() -> None:
    """Click の引数解析 error も cmoc 形式の stdout report に変換する。"""
    result = runner.invoke(app, ["--bad-option"])

    assert result.exit_code != 0
    assert "# ERROR" in result.stdout
    assert "CLI 引数解析に失敗しました。" in result.stdout
    assert "No such option: --bad-option" in result.stdout
    assert "# ERROR" not in result.stderr
    assert "CLI 引数解析に失敗しました。" not in result.stderr
    assert "No such option: --bad-option" not in result.stderr


@pytest.mark.parametrize(
    ("argv", "allowed"),
    [
        (["apply", "fork", "--scope", "bad"], ["rolling", "session", "full"]),
        (["review", "oracle", "--scope", "rolling"], ["session", "full"]),
    ],
)
def test_scope_options_are_rejected_by_cli_parser(
    argv: list[str], allowed: list[str]
) -> None:
    """scope の公開値制約はサブコマンド実行前の CLI 解析で拒否する。"""
    result = runner.invoke(app, argv)

    assert result.exit_code != 0
    assert "# ERROR" in result.stdout
    assert "CLI 引数解析に失敗しました。" in result.stdout
    assert "Invalid value for '--scope'" in result.stdout
    assert argv[-1] in result.stdout
    for value in allowed:
        assert value in result.stdout
    assert "# ERROR" not in result.stderr


def test_cli_requires_current_directory_to_be_work_root(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """work root 以外からの CLI 実行では副作用を出す前に拒否する。"""
    root = make_repo(tmp_path)
    monkeypatch.chdir(root / "oracle")

    result = runner.invoke(app, ["init"])

    assert result.exit_code != 0
    assert "# ERROR" in result.stdout
    assert "cmoc は work root で実行してください。" in result.stdout
    assert "# ERROR" not in result.stderr
    assert "cmoc は work root で実行してください。" not in result.stderr
    assert f"cwd: {(root / 'oracle').resolve()}" in result.stdout
    assert f"work_root: {root.resolve()}" in result.stdout
    assert not (root / ".gitignore").exists()


def test_cli_completion_probe_skips_cmoc_preflight_and_side_effects(
    tmp_path: Path,
) -> None:
    """shell completion probe は cmoc preflight と初期化副作用を起こさない。"""
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


def test_pre_log_check_failure_does_not_write_subcommand_log(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert runner.invoke(app, ["init"], catch_exceptions=False).exit_code == 0
    log_paths_before = set((root / ".cmoc" / "local" / "log" / "sub_command").glob("*.jsonl"))
    (root / "README.md").write_text("dirty\n")

    result = runner.invoke(app, ["indexing"])

    assert result.exit_code == 1
    assert set((root / ".cmoc" / "local" / "log" / "sub_command").glob("*.jsonl")) == log_paths_before


def test_bin_cmoc_missing_venv_call_stack_uses_root_token_path(tmp_path: Path) -> None:
    """起動 wrapper の missing venv report は root token path で位置を出す。"""
    fake_cmoc_root = tmp_path / "cmoc"
    fake_bin = fake_cmoc_root / "bin"
    fake_bin.mkdir(parents=True)
    shutil.copy2(Path(__file__).parents[1] / "bin" / "cmoc", fake_bin / "cmoc")

    result = subprocess.run(
        ["./bin/cmoc"],
        cwd=fake_cmoc_root,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 1
    assert "## Call stack" in result.stdout
    assert "(<cmoc-root>/bin/cmoc:" in result.stdout
    assert "(./bin/cmoc:" not in result.stdout
    assert "(bin/cmoc:" not in result.stdout


def test_ensure_cmoc_ignored_updates_gitignore(tmp_path: Path) -> None:
    """`.cmoc` が未 ignore の repo では literal ignore pattern を追加する。"""
    root = make_repo(tmp_path)

    ensure_cmoc_ignored(root)

    assert "/.cmoc/local/" in (root / ".gitignore").read_text()
    ignored = subprocess.run(
        ["git", "check-ignore", "-q", ".cmoc/local/.__cmoc_ignore_probe__"],
        cwd=root,
    )
    assert ignored.returncode == 0


def test_ensure_cmoc_ignored_adds_literal_pattern_after_existing_effective_pattern(
    tmp_path: Path,
) -> None:
    """既存 pattern が有効でも root 固定 pattern を追記して表現を安定させる。"""
    root = make_repo(tmp_path)
    (root / ".gitignore").write_text(".cmoc/\n")
    run_git(root, "add", ".gitignore")
    run_git(root, "commit", "-m", "ignore cmoc")

    ensure_cmoc_ignored(root)

    assert (root / ".gitignore").read_text() == ".cmoc/\n\n/.cmoc/local/\n"
    assert run_git(root, "status", "--short").stdout.strip() == "M .gitignore"


def test_file_access_mode_values_are_json_ready() -> None:
    """FileAccessMode の永続化値は JSON schema 側と共有できる文字列にする。"""
    assert FileAccessMode.READONLY.value == "readonly"
    assert FileAccessMode.PURE_ORACLE_READ.value == "pure_oracle_read"
    assert FileAccessMode.REPO_WRITE.value == "repo_write"
    assert FileAccessMode.PURE_ORACLE_WRITE.value == "pure_oracle_write"
    assert FileAccessMode.REALIZATION_WRITE.value == "realization_write"


def test_file_access_to_sandbox_mode_supports_repo_write() -> None:
    """repo write mode まで Codex sandbox mode へ欠落なく変換する。"""
    assert file_access_to_sandbox_mode(FileAccessMode.READONLY) == "workspace-write"
    assert file_access_to_sandbox_mode(FileAccessMode.PURE_ORACLE_READ) == "workspace-write"
    assert file_access_to_sandbox_mode(FileAccessMode.REALIZATION_WRITE) == "workspace-write"
    assert file_access_to_sandbox_mode(FileAccessMode.PURE_ORACLE_WRITE) == "workspace-write"
    assert file_access_to_sandbox_mode(FileAccessMode.REPO_WRITE) == "workspace-write"


def test_file_access_to_codex_cwd_keeps_work_root_for_compatibility(
    tmp_path: Path,
) -> None:
    """Codex の作業 root は AgentCallParameter.cwd 側で指定する。"""
    root = tmp_path / "repo"
    root.mkdir()

    assert file_access_to_codex_cwd(FileAccessMode.READONLY, root) == root.resolve()
    assert file_access_to_codex_cwd(FileAccessMode.PURE_ORACLE_READ, root) == root.resolve()
    assert file_access_to_codex_cwd(FileAccessMode.PURE_ORACLE_WRITE, root) == root.resolve()


def test_is_binary_reads_only_initial_chunk() -> None:
    """binary 判定は大きい file 全体を読まず先頭 chunk だけを見る。"""
    class Reader:
        def __init__(self) -> None:
            self.size: int | None = None

        def __enter__(self) -> "Reader":
            return self

        def __exit__(self, *args: object) -> None:
            pass

        def read(self, size: int) -> bytes:
            self.size = size
            return b"text"

    class FakePath:
        def __init__(self) -> None:
            self.reader = Reader()

        def open(self, mode: str) -> Reader:
            assert mode == "rb"
            return self.reader

    path = FakePath()

    assert is_binary(path) is False
    assert path.reader.size == 4096


def test_codex_profile_generates_rooted_sandbox(tmp_path: Path) -> None:
    """root 付き通常経路でも FileAccessMode ごとの profile を生成する。"""
    root = tmp_path / "repo"
    root.mkdir()
    (root / ".cmoc").mkdir()
    (root / ".codex").mkdir()
    (root / ".pytest_cache").mkdir()
    (root / "AGENTS.md").write_text("agents\n")
    (root / "INDEX.md").write_text("index\n")
    (root / "src").mkdir()
    (root / "test").mkdir()
    (root / "README.md").write_text("# repo\n")
    (root / "oracle").mkdir()
    (root / "memo").mkdir()
    (root / ".agents").mkdir()
    (root / ".git").mkdir()
    (root / ".gitignore").write_text("memo\n")

    parameter = AgentCallParameter(
        ModelClass.EFFICIENCY,
        ReasoningEffort.LOW,
        FileAccessMode.READONLY,
        "prompt",
        None,
    )
    profiles = {
        mode: build_codex_profile(
            AgentCallParameter(
                parameter.model_class,
                parameter.reasoning_effort,
                mode,
                parameter.prompt,
                parameter.structured_output_schema_path,
            ),
            CmocConfig(),
            root,
        )
        for mode in FileAccessMode
    }

    assert 'sandbox_mode = "workspace-write"' in profiles[FileAccessMode.READONLY]
    assert 'sandbox_mode = "workspace-write"' in profiles[FileAccessMode.PURE_ORACLE_READ]
    for mode in (
        FileAccessMode.READONLY,
        FileAccessMode.PURE_ORACLE_READ,
        FileAccessMode.REALIZATION_WRITE,
        FileAccessMode.PURE_ORACLE_WRITE,
        FileAccessMode.REPO_WRITE,
    ):
        assert 'sandbox_mode = "workspace-write"' in profiles[mode]
        assert "[sandbox_workspace_write]" in profiles[mode]
    assert _profile_writable_roots(profiles[FileAccessMode.REALIZATION_WRITE]) == {
        str(root.resolve()),
    }
    assert _profile_writable_roots(profiles[FileAccessMode.READONLY]) == {
        str(root.resolve()),
    }
    assert _profile_writable_roots(profiles[FileAccessMode.PURE_ORACLE_READ]) == {
        str((root / "oracle").resolve())
    }
    assert _profile_writable_roots(profiles[FileAccessMode.PURE_ORACLE_WRITE]) == {
        str((root / "oracle").resolve())
    }
    assert _profile_writable_roots(profiles[FileAccessMode.REPO_WRITE]) == {
        str(root.resolve()),
    }
    for profile in profiles.values():
        assert all(Path(path).is_dir() for path in _profile_writable_roots(profile))
    _assert_writable(
        profiles[FileAccessMode.REALIZATION_WRITE], root / "src" / "created.py"
    )
    _assert_writable(
        profiles[FileAccessMode.REALIZATION_WRITE], root / "new_top_level.md"
    )
    _assert_writable(profiles[FileAccessMode.REALIZATION_WRITE], root / ".gitignore")
    _assert_writable(
        profiles[FileAccessMode.REPO_WRITE], root / "oracle" / "created.md"
    )
    _assert_writable(
        profiles[FileAccessMode.REPO_WRITE], root / "new_top_level.md"
    )
    _assert_writable(profiles[FileAccessMode.REPO_WRITE], root / ".gitignore")

    extra = root / "src" / "extra"
    profile = build_codex_profile(
        AgentCallParameter(
            parameter.model_class,
            parameter.reasoning_effort,
            FileAccessMode.REALIZATION_WRITE,
            parameter.prompt,
            parameter.structured_output_schema_path,
        ),
        CmocConfig(),
        root,
        extra_writable_paths=[extra],
    )
    assert _profile_writable_roots(profile) == {
        str(root.resolve()),
    }

    repo_extra = root / "new_dir"
    profile = build_codex_profile(
        AgentCallParameter(
            parameter.model_class,
            parameter.reasoning_effort,
            FileAccessMode.REPO_WRITE,
            parameter.prompt,
            parameter.structured_output_schema_path,
        ),
        CmocConfig(),
        root,
        extra_writable_paths=[repo_extra],
    )
    assert _profile_writable_roots(profile) == {
        str(root.resolve()),
    }
    _assert_writable(profile, repo_extra / "created.md")

    with pytest.raises(CmocError, match="許可領域外"):
        build_codex_profile(
            parameter,
            CmocConfig(),
            root,
            [root / "memo" / "blocked.md"],
        )

    with pytest.raises(CmocError, match="許可領域外"):
        build_codex_profile(
            AgentCallParameter(
                parameter.model_class,
                parameter.reasoning_effort,
                FileAccessMode.PURE_ORACLE_READ,
                parameter.prompt,
                parameter.structured_output_schema_path,
            ),
            CmocConfig(),
            root,
            [root / "src" / "blocked.md"],
        )

    build_codex_profile(
        AgentCallParameter(
            parameter.model_class,
            parameter.reasoning_effort,
            FileAccessMode.PURE_ORACLE_READ,
            parameter.prompt,
            parameter.structured_output_schema_path,
        ),
        CmocConfig(),
        root,
        [root / ".cmoc" / "local" / "log" / "tui" / "20260101_cmpl.md"],
    )

    with pytest.raises(CmocError, match="許可領域外"):
        build_codex_profile(
            AgentCallParameter(
                parameter.model_class,
                parameter.reasoning_effort,
                FileAccessMode.PURE_ORACLE_READ,
                parameter.prompt,
                parameter.structured_output_schema_path,
            ),
            CmocConfig(),
            root,
            [root / ".cmoc" / "local" / "log" / "tui" / "20260101_orig.md"],
        )


def test_codex_profile_allows_repo_local_read_from_linked_worktree(
    tmp_path: Path,
) -> None:
    """linked worktree 実行時だけ repo 側 `.cmoc/local` 読み取りを追加許可する。"""
    root = make_repo(tmp_path)
    linked = root / ".cmoc" / "local" / "worktree" / "linked-read"
    linked.parent.mkdir(parents=True)
    run_git(root, "worktree", "add", "-b", "linked-read", str(linked), "HEAD")
    parameter = AgentCallParameter(
        ModelClass.EFFICIENCY,
        ReasoningEffort.LOW,
        FileAccessMode.PURE_ORACLE_READ,
        "prompt",
        None,
    )

    build_codex_profile(
        parameter,
        CmocConfig(),
        linked,
        [root / ".cmoc" / "local" / "report" / "review" / "report.md"],
        extra_read_root=root,
    )

    with pytest.raises(CmocError, match="許可領域外"):
        build_codex_profile(
            parameter,
            CmocConfig(),
            linked,
            [root / "src" / "blocked.md"],
            extra_read_root=root,
        )


def test_codex_profile_allows_root_for_realization_write_and_ignored_extra(
    tmp_path: Path,
) -> None:
    root = make_repo(tmp_path)
    (root / ".gitignore").write_text("/build/\n")
    (root / "src").mkdir()
    (root / "test").mkdir()
    (root / "build").mkdir()
    run_git(root, "add", ".gitignore", "src", "test")
    run_git(root, "commit", "-m", "add realization dirs")

    profile = build_codex_profile(
        AgentCallParameter(
            ModelClass.EFFICIENCY,
            ReasoningEffort.LOW,
            FileAccessMode.REALIZATION_WRITE,
            "prompt",
            None,
        ),
        CmocConfig(),
        root,
    )

    assert _profile_writable_roots(profile) == {str(root.resolve())}
    _assert_writable(profile, root / "src" / "manual.py")
    _assert_writable(profile, root / ".gitignore")

    profile = build_codex_profile(
        AgentCallParameter(
            ModelClass.EFFICIENCY,
            ReasoningEffort.LOW,
            FileAccessMode.REALIZATION_WRITE,
            "prompt",
            None,
        ),
        CmocConfig(),
        root,
        extra_writable_paths=[root / "build"],
    )
    assert _profile_writable_roots(profile) == {str(root.resolve())}


@pytest.mark.parametrize(
    ("mode", "extra"),
    [
        (FileAccessMode.REALIZATION_WRITE, "oracle/blocked.md"),
        (FileAccessMode.REALIZATION_WRITE, "memo/blocked.md"),
        (FileAccessMode.REALIZATION_WRITE, ".agents/blocked.md"),
        (FileAccessMode.REALIZATION_WRITE, ".cmoc/local/state.json"),
        (FileAccessMode.REALIZATION_WRITE, ".codex/config.toml"),
        (FileAccessMode.REALIZATION_WRITE, "AGENTS.md"),
        (FileAccessMode.REALIZATION_WRITE, "INDEX.md"),
        (FileAccessMode.PURE_ORACLE_WRITE, "src/blocked.md"),
        (FileAccessMode.PURE_ORACLE_WRITE, "memo/blocked.md"),
        (FileAccessMode.PURE_ORACLE_WRITE, ".agents/blocked.md"),
        (FileAccessMode.PURE_ORACLE_WRITE, "oracle/INDEX.md"),
        (FileAccessMode.PURE_ORACLE_WRITE, "oracle/AGENTS.md"),
        (FileAccessMode.REPO_WRITE, "memo/blocked.md"),
        (FileAccessMode.REPO_WRITE, ".agents/blocked.md"),
        (FileAccessMode.REPO_WRITE, ".cmoc/local/state.json"),
        (FileAccessMode.REPO_WRITE, ".git/config"),
        (FileAccessMode.REPO_WRITE, "AGENTS.md"),
        (FileAccessMode.REPO_WRITE, "INDEX.md"),
        (FileAccessMode.REPO_WRITE, "../outside.md"),
    ],
)
def test_codex_profile_rejects_disallowed_extra_writable_paths(
    tmp_path: Path, mode: FileAccessMode, extra: str
) -> None:
    root = tmp_path / "repo"
    root.mkdir()
    (root / "src").mkdir()
    (root / "oracle").mkdir()
    (root / "memo").mkdir()
    (root / ".agents").mkdir()
    if extra == ".gitignore":
        (root / extra).write_text("memo\n")

    with pytest.raises(CmocError, match="追加書き込み許可 path"):
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
            extra_writable_paths=[root / extra],
        )


def test_codex_profile_allows_root_ancillary_extra_writable_path(
    tmp_path: Path,
) -> None:
    root = make_repo(tmp_path)
    (root / ".gitignore").write_text("memo\n")
    (root / "README.md").write_text("# repo\n")
    run_git(root, "add", ".gitignore")
    run_git(root, "add", "README.md")
    run_git(root, "commit", "-m", "add gitignore")

    for extra in [root / ".gitignore", root / "README.md"]:
        profile = build_codex_profile(
            AgentCallParameter(
                ModelClass.EFFICIENCY,
                ReasoningEffort.LOW,
                FileAccessMode.REALIZATION_WRITE,
                "prompt",
                None,
            ),
            CmocConfig(),
            root,
            extra_writable_paths=[extra],
        )

        assert _profile_writable_roots(profile) == {str(root.resolve())}
        _assert_writable(profile, extra)


def test_codex_profile_uses_directory_roots_for_session_join_conflict_resolution(
    tmp_path: Path,
) -> None:
    root = tmp_path / "repo"
    root.mkdir()
    (root / "src").mkdir()
    (root / "oracle").mkdir()
    target = root / "oracle" / "spec.md"
    target.write_text("conflict\n")

    profile = build_codex_profile(
        AgentCallParameter(
            ModelClass.EFFICIENCY,
            ReasoningEffort.LOW,
            FileAccessMode.REALIZATION_WRITE,
            "prompt",
            None,
        ),
        CmocConfig(),
        root,
        extra_writable_paths=[target],
        allow_oracle_conflict_writes=True,
    )

    assert _profile_writable_roots(profile) == {str(root.resolve())}
    _assert_writable(profile, target)


def test_codex_profile_allows_session_join_conflict_targets_under_allowed_dirs(
    tmp_path: Path,
) -> None:
    root = tmp_path / "repo"
    root.mkdir()
    (root / "src").mkdir()
    (root / "oracle").mkdir()
    target = root / "oracle" / "spec.md"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("conflict\n")

    profile = build_codex_profile(
        AgentCallParameter(
            ModelClass.EFFICIENCY,
            ReasoningEffort.LOW,
            FileAccessMode.REALIZATION_WRITE,
            "prompt",
            None,
        ),
        CmocConfig(),
        root,
        extra_writable_paths=[target],
        allow_oracle_conflict_writes=True,
    )

    assert all(Path(path).is_dir() for path in _profile_writable_roots(profile))
    _assert_writable(profile, target)


@pytest.mark.parametrize("extra", ["oracle/INDEX.md", "oracle/AGENTS.md"])
def test_codex_profile_rejects_session_join_conflict_targets_with_denied_names(
    tmp_path: Path, extra: str
) -> None:
    root = tmp_path / "repo"
    root.mkdir()
    (root / "src").mkdir()
    target = root / extra
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("conflict\n")

    with pytest.raises(CmocError, match="追加書き込み許可 path"):
        build_codex_profile(
            AgentCallParameter(
                ModelClass.EFFICIENCY,
                ReasoningEffort.LOW,
                FileAccessMode.REALIZATION_WRITE,
                "prompt",
                None,
            ),
            CmocConfig(),
            root,
            extra_writable_paths=[target],
            allow_oracle_conflict_writes=True,
        )


@pytest.mark.parametrize("extra", ["INDEX.md", "AGENTS.md"])
def test_codex_profile_rejects_root_file_session_join_conflict_targets(
    tmp_path: Path, extra: str
) -> None:
    root = tmp_path / "repo"
    root.mkdir()
    (root / "src").mkdir()
    target = root / extra
    target.write_text("conflict\n")

    with pytest.raises(CmocError, match="追加書き込み許可 path"):
        build_codex_profile(
            AgentCallParameter(
                ModelClass.EFFICIENCY,
                ReasoningEffort.LOW,
                FileAccessMode.REALIZATION_WRITE,
                "prompt",
                None,
            ),
            CmocConfig(),
            root,
            extra_writable_paths=[target],
            allow_oracle_conflict_writes=True,
        )


def test_codex_profile_allows_root_readme_session_join_conflict_target(
    tmp_path: Path,
) -> None:
    root = tmp_path / "repo"
    root.mkdir()
    (root / "src").mkdir()
    target = root / "README.md"
    target.write_text("conflict\n")

    profile = build_codex_profile(
        AgentCallParameter(
            ModelClass.EFFICIENCY,
            ReasoningEffort.LOW,
            FileAccessMode.REALIZATION_WRITE,
            "prompt",
            None,
        ),
        CmocConfig(),
        root,
        extra_writable_paths=[target],
        allow_oracle_conflict_writes=True,
    )

    assert _profile_writable_roots(profile) == {str(root.resolve())}
    _assert_writable(profile, target)


@pytest.mark.parametrize(
    "extra",
    [
        ".agents/blocked.md",
        ".cmoc/local/state.json",
        ".codex/config.toml",
        ".git/config",
        "memo/blocked.md",
    ],
)
def test_codex_profile_rejects_runtime_paths_even_for_session_join_conflict(
    tmp_path: Path, extra: str
) -> None:
    root = tmp_path / "repo"
    root.mkdir()
    (root / "src").mkdir()

    with pytest.raises(CmocError, match="追加書き込み許可 path"):
        build_codex_profile(
            AgentCallParameter(
                ModelClass.EFFICIENCY,
                ReasoningEffort.LOW,
                FileAccessMode.REALIZATION_WRITE,
                "prompt",
                None,
            ),
            CmocConfig(),
            root,
            extra_writable_paths=[root / extra],
            allow_oracle_conflict_writes=True,
        )
