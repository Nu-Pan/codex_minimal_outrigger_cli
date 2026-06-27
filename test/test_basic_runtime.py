import shutil
import subprocess
import sys
from pathlib import Path
import tomllib

import pytest
import main as main_module
from basic.acp import AgentCallParameter, FileAccessMode, ModelClass, ReasoningEffort
from basic.path_model import (
    RootToken,
    resolve_real_path,
    resolve_run_root,
    resolve_token_path,
)
from cmoc_runtime import (
    CmocError,
    ensure_cmoc_ignored,
    file_access_to_sandbox_mode,
    format_duration,
    render_error,
    repo_root,
    work_root,
)
from commons.runtime_codex_profile import build_codex_profile
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


def test_path_model_resolves_token_path_inside_repo() -> None:
    """root token path が repo 内の実 path から復元できる契約を固定する。"""
    cmoc_root = resolve_real_path(RootToken.CMOC)
    token_path = resolve_token_path(cmoc_root / "src", RootToken.CMOC)

    assert token_path == Path("<cmoc-root>") / "src"


def test_format_duration_truncates_msec_digit_and_space_pads_time_parts() -> None:
    """duration 表示は丸めず切り捨て、時分秒の幅を揃える。"""
    assert format_duration(0.19) == " 0h  0m  0.1s"
    assert format_duration(3.19) == " 0h  0m  3.1s"
    assert format_duration(59.99) == " 0h  0m 59.9s"


def test_runtime_distinguishes_repo_root_from_linked_worktree(
    tmp_path: Path,
) -> None:
    """linked worktree では repo root と run/work root を分けて扱う。"""
    root = make_repo(tmp_path)
    linked = root / ".cmoc" / "worktrees" / "linked"
    run_git(root, "worktree", "add", "-b", "linked-test", str(linked), "HEAD")

    assert repo_root(linked) == root.resolve()
    assert resolve_run_root(linked) == linked.resolve()
    assert work_root(linked) == linked.resolve()


def test_resolve_run_root_rejects_main_worktree(tmp_path: Path) -> None:
    """main worktree は run root として扱わない。"""
    root = make_repo(tmp_path)

    with pytest.raises(ValueError, match="`<run-root>` was not found"):
        resolve_run_root(root)


def test_config_defaults_match_logical_model_classes() -> None:
    """既定 config が論理 model class と reasoning effort を埋める。"""
    config = CmocConfig()

    assert config.num_parallel == 8
    assert config.codex.model[ModelClass.MAINSTREAM] == "GPT-5.5"
    assert config.codex.reasoning_effort[ReasoningEffort.HIGH] == "high"


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

    assert "/.cmoc/" in (root / ".gitignore").read_text()
    ignored = subprocess.run(
        ["git", "check-ignore", "-q", ".cmoc/.__cmoc_ignore_probe__"],
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

    assert (root / ".gitignore").read_text() == ".cmoc/\n\n/.cmoc/\n"
    assert run_git(root, "status", "--short").stdout.strip() == "M .gitignore"


def test_file_access_mode_values_are_json_ready() -> None:
    """FileAccessMode の永続化値は JSON schema 側と共有できる文字列にする。"""
    assert FileAccessMode.READONLY.value == "readonly"
    assert FileAccessMode.REALIZATION_WRITE.value == "realization_write"
    assert FileAccessMode.REPO_WRITE.value == "repo_write"


def test_file_access_to_sandbox_mode_supports_repo_write() -> None:
    """repo write mode まで Codex sandbox mode へ欠落なく変換する。"""
    assert file_access_to_sandbox_mode(FileAccessMode.READONLY) == "read-only"
    assert file_access_to_sandbox_mode(FileAccessMode.PURE_ORACLE_READ) == "read-only"
    assert file_access_to_sandbox_mode(FileAccessMode.REALIZATION_WRITE) == "workspace-write"
    assert file_access_to_sandbox_mode(FileAccessMode.ORACLE_WRITE) == "workspace-write"
    assert file_access_to_sandbox_mode(FileAccessMode.REPO_WRITE) == "workspace-write"


def test_is_binary_reads_only_initial_chunk() -> None:
    """binary 判定は大きい file 全体を読まず先頭 chunk だけを見る。"""
    class Reader:
        """読み取り size を記録する fake binary reader。"""

        def __init__(self) -> None:
            """未読み取り状態で fake reader を初期化する。"""
            self.size: int | None = None

        def __enter__(self) -> "Reader":
            """context manager として fake reader 自身を返す。"""
            return self

        def __exit__(self, *args: object) -> None:
            """fake reader では close 副作用を観測しない。"""
            pass

        def read(self, size: int) -> bytes:
            """binary 判定が要求した read size を記録する。"""
            self.size = size
            return b"text"

    class FakePath:
        """open 呼び出しを fake reader へ接続する path 代替。"""

        def __init__(self) -> None:
            """assertion から参照する fake reader を保持する。"""
            self.reader = Reader()

        def open(self, mode: str) -> Reader:
            """binary 判定が binary mode で開くことを確認する。"""
            assert mode == "rb"
            return self.reader

    path = FakePath()

    assert is_binary(path) is False
    assert path.reader.size == 4096


def test_codex_profile_contains_supported_sandbox_settings(tmp_path: Path) -> None:
    """Codex profile は現在の Codex CLI が受け付ける sandbox key だけを持つ。"""
    root = tmp_path / "repo"
    root.mkdir()

    def profile(mode: FileAccessMode) -> dict:
        """file access mode ごとの profile TOML を dict として読む。"""
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
    assert "permissions" not in readonly
    assert "sandbox_workspace_write" not in readonly

    assert profile(FileAccessMode.PURE_ORACLE_READ)["sandbox_mode"] == "read-only"

    prompt_file = root / ".cmoc" / "log" / "tui" / "prompt_cmpl.md"
    pure_oracle_tui = tomllib.loads(
        build_codex_profile(
            AgentCallParameter(
                ModelClass.EFFICIENCY,
                ReasoningEffort.LOW,
                FileAccessMode.PURE_ORACLE_READ,
                "prompt",
                None,
            ),
            CmocConfig(),
            root,
            [prompt_file],
        )
    )
    assert pure_oracle_tui["sandbox_mode"] == "read-only"
    assert "sandbox_workspace_write" not in pure_oracle_tui

    realization_profile = profile(FileAccessMode.REALIZATION_WRITE)
    assert realization_profile["sandbox_mode"] == "workspace-write"
    realization_workspace = realization_profile["sandbox_workspace_write"]
    assert realization_workspace["writable_roots"] == [str(root)]
    assert "read_only_paths" not in realization_workspace

    (root / "oracle").mkdir()
    oracle_conflict = root / "oracle" / "spec.md"
    oracle_conflict.write_text("# spec\n")
    other_oracle_file = root / "oracle" / "other.md"
    other_oracle_file.write_text("# other\n")
    conflict_profile = tomllib.loads(
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
            extra_writable_paths=[
                oracle_conflict,
                root / "memo" / "blocked.md",
                root / ".agents" / "blocked.md",
            ],
        )
    )
    conflict_workspace = conflict_profile["sandbox_workspace_write"]
    assert conflict_workspace["writable_roots"] == sorted(
        [str(root), str(oracle_conflict)]
    )
    assert "read_only_paths" not in conflict_workspace
    assert "permissions" not in conflict_profile

    oracle_workspace = profile(FileAccessMode.ORACLE_WRITE)["sandbox_workspace_write"]
    assert oracle_workspace["writable_roots"] == [str(root / "oracle")]

    repo_workspace = profile(FileAccessMode.REPO_WRITE)["sandbox_workspace_write"]
    assert repo_workspace["writable_roots"] == [str(root)]
