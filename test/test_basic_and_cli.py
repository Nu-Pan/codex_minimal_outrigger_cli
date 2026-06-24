import json
import subprocess
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from typer.testing import CliRunner

import cmoc_runtime
import main as main_module
from basic.acp import AgentCallParameter, FileAccessMode, ModelClass, ReasoningEffort
from basic.path_model import RootToken, resolve_real_path, resolve_token_path
from config.cmoc_config import CmocConfig
from cmoc_runtime import (
    CmocError,
    SubcommandLogger,
    ensure_cmoc_ignored,
    file_access_to_sandbox_mode,
    render_error,
    repo_root,
    run_codex_exec,
    run_codex_tui,
    work_root,
)
from main import app
from sub_commands.tui import parse_markdown_prompt

runner = CliRunner()


def run_git(root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args], cwd=root, text=True, capture_output=True, check=True
    )


def make_repo(tmp_path: Path) -> Path:
    root = tmp_path / "repo"
    root.mkdir()
    run_git(root, "init")
    run_git(root, "config", "user.email", "cmoc@example.invalid")
    run_git(root, "config", "user.name", "cmoc test")
    (root / "README.md").write_text("# repo\n")
    (root / "oracle").mkdir()
    (root / "oracle" / "spec.md").write_text("# spec\n")
    run_git(root, "add", ".")
    run_git(root, "commit", "-m", "initial")
    return root


def setup_codex_home(tmp_path: Path, monkeypatch) -> Path:
    codex_home = tmp_path / "codex_home"
    codex_home.mkdir()
    (codex_home / "auth.json").write_text("{}\n")
    monkeypatch.setenv("CODEX_HOME", str(codex_home))
    return codex_home


def apply_worktree_from_state(root: Path, state: dict) -> Path:
    return main_module.worktree_for_branch(root, state["apply"]["apply_branch"])


def test_path_model_resolves_token_path_inside_repo() -> None:
    cmoc_root = resolve_real_path(RootToken.CMOC)
    token_path = resolve_token_path(cmoc_root / "src", RootToken.CMOC)

    assert token_path == Path("<cmoc-root>") / "src"


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


def test_init_untracks_existing_cmoc_files_and_commits_cleanup(
    tmp_path: Path, monkeypatch
) -> None:
    root = make_repo(tmp_path)
    tracked_cmoc_file = root / ".cmoc" / "tracked.txt"
    tracked_cmoc_file.parent.mkdir()
    tracked_cmoc_file.write_text("tracked before init\n")
    run_git(root, "add", ".cmoc/tracked.txt")
    run_git(root, "commit", "-m", "track cmoc file")
    monkeypatch.chdir(root)

    result = runner.invoke(app, ["init"], catch_exceptions=False)

    assert result.exit_code == 0
    assert tracked_cmoc_file.exists()
    assert run_git(root, "ls-files", "--", ".cmoc").stdout.strip() == ""
    ignored = subprocess.run(
        ["git", "check-ignore", "-q", ".cmoc/.__cmoc_ignore_probe__"],
        cwd=root,
    )
    assert ignored.returncode == 0
    assert run_git(root, "status", "--short", "--", ".gitignore").stdout.strip() == ""
    assert "cmoc init" in run_git(root, "log", "--oneline", "-1").stdout


def test_init_writes_default_config_json(tmp_path: Path, monkeypatch) -> None:
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)

    result = runner.invoke(app, ["init"], catch_exceptions=False)

    assert result.exit_code == 0
    config_path = root / ".cmoc" / "config.json"
    assert config_path.is_file()
    data = json.loads(config_path.read_text())
    assert data["num_parallel"] == 8
    assert data["codex"]["model"]["mainstream"] == "GPT-5.5"
    assert data["codex"]["model"]["efficiency"] == "GPT-5.4-mini"
    assert data["codex"]["reasoning_effort"]["high"] == "high"
    assert (
        subprocess.run(
            ["git", "check-ignore", "-q", ".cmoc/config.json"], cwd=root
        ).returncode
        == 0
    )
    assert (
        run_git(root, "status", "--short", "--", ".cmoc/config.json").stdout.strip()
        == ""
    )


def test_init_syncs_config_defaults_without_overwriting_human_values(
    tmp_path: Path,
    monkeypatch,
) -> None:
    root = make_repo(tmp_path)
    config_path = root / ".cmoc" / "config.json"
    config_path.parent.mkdir()
    config_path.write_text(
        json.dumps(
            {
                "num_parallel": 3,
                "codex": {"model": {"mainstream": "CUSTOM-MAIN"}},
            }
        )
        + "\n"
    )
    monkeypatch.chdir(root)

    result = runner.invoke(app, ["init"], catch_exceptions=False)

    assert result.exit_code == 0
    data = json.loads(config_path.read_text())
    assert data["num_parallel"] == 3
    assert data["codex"]["model"]["mainstream"] == "CUSTOM-MAIN"
    assert data["codex"]["model"]["efficiency"] == "GPT-5.4-mini"
    assert data["codex"]["reasoning_effort"]["low"] == "low"
    assert data["apply_fork"]["num_apply_loop"] == 5
    assert data["review_oracle"]["num_validate_findings_loop"] == 3


def test_tui_runs_editor_resolves_parameters_and_launches_codex(
    tmp_path: Path,
    monkeypatch,
) -> None:
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert runner.invoke(app, ["init"], catch_exceptions=False).exit_code == 0
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    fake_code = bin_dir / "code"
    fake_code.write_text(
        "\n".join(
            [
                "#!/usr/bin/env python3",
                "import pathlib, sys",
                "path = pathlib.Path(sys.argv[-1])",
                "text = path.read_text()",
                "path.write_text(text + '\\n<!-- remove me -->\\n# 依頼\\n\\nsrc を確認して必要なら直す\\n')",
            ]
        )
        + "\n"
    )
    fake_code.chmod(0o755)
    monkeypatch.setenv("PATH", f"{bin_dir}:{Path('/usr/bin')}")
    exec_calls = []
    tui_calls = []

    class FakeResolveResult:
        output_json = {
            "file_access_mode": {"value": "repo_write", "reason": "repo wide task"},
            "oracle_and_realization_basic": {"value": True, "reason": "needed"},
            "oracle_standard": {"value": False, "reason": "not needed"},
            "realization_standard": {"value": True, "reason": "needed"},
            "review_oracle_standard": {"value": False, "reason": "not needed"},
            "apply_review_standard": {"value": False, "reason": "not needed"},
            "index_entry_standard": {"value": False, "reason": "not needed"},
        }

    def fake_run_codex_exec(parameter, **kwargs):
        exec_calls.append((parameter, kwargs))
        assert kwargs["purpose"] == "tui resolve parameter"
        assert parameter.structured_output_schema_path.name == "resolve_parameter.json"
        assert "remove me" not in parameter.prompt
        assert "src を確認して必要なら直す" in parameter.prompt
        return FakeResolveResult()

    def fake_run_codex_tui(parameter, **kwargs):
        tui_calls.append((parameter, kwargs))
        assert kwargs["purpose"] == "tui codex"
        assert parameter.model_class == ModelClass.MAINSTREAM
        assert parameter.reasoning_effort == ReasoningEffort.MEDIUM
        assert parameter.file_access_mode == FileAccessMode.REPO_WRITE
        assert parameter.structured_output_schema_path is None
        assert parameter.prompt.endswith("_cmpl.md` の指示に従って下さい。")

    monkeypatch.setattr(main_module, "run_codex_exec", fake_run_codex_exec)
    monkeypatch.setattr(main_module, "run_codex_tui", fake_run_codex_tui)

    result = runner.invoke(app, ["tui"], catch_exceptions=False)

    assert result.exit_code == 0
    assert len(exec_calls) == 1
    assert len(tui_calls) == 1
    orig_files = list((root / ".cmoc" / "log" / "tui").glob("*_orig.md"))
    assert len(orig_files) == 1
    assert "TODO ここから書き始める" in orig_files[0].read_text()
    complete_files = list((root / ".cmoc" / "log" / "tui").glob("*_cmpl.md"))
    assert len(complete_files) == 1
    complete_prompt = complete_files[0].read_text()
    assert "# file read write rule - repo_write" in complete_prompt
    assert "# 詳細指示" in complete_prompt
    assert "src を確認して必要なら直す" in complete_prompt
    assert "remove me" not in complete_prompt
    assert str(complete_files[0]) in tui_calls[0][0].prompt
    assert "/.cmoc/" in (root / ".gitignore").read_text()
    assert (root / ".cmoc" / "log" / "sub_command").is_dir()
    assert not (root / ".cmoc" / "logs" / "sub_commands").exists()


def test_parse_markdown_prompt_ignores_headings_inside_fenced_code_blocks() -> None:
    parsed = parse_markdown_prompt(
        "\n".join(
            [
                "# 依頼",
                "",
                "```python",
                "# 見出しではない",
                "print('ok')",
                "```",
                "",
                "## 補足",
                "本文",
            ]
        )
    )

    assert [doc.title for doc in parsed] == ["依頼", "補足"]
    assert isinstance(parsed[0].children, str)
    assert "# 見出しではない" in parsed[0].children


def test_session_fork_creates_session_branch_and_state(
    tmp_path: Path, monkeypatch
) -> None:
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    init_result = runner.invoke(app, ["init"], catch_exceptions=False)
    assert init_result.exit_code == 0

    result = runner.invoke(app, ["session", "fork"], catch_exceptions=False)

    assert result.exit_code == 0
    branch = run_git(root, "branch", "--show-current").stdout.strip()
    assert branch.startswith("cmoc/session/")
    session_id = branch.removeprefix("cmoc/session/")
    state = json.loads((root / ".cmoc" / "sessions" / f"{session_id}.json").read_text())
    assert state["session"]["state"] == "active"
    assert state["session"]["session_home_branch"] in {"master", "main"}
    assert state["apply"]["state"] == "ready"


def test_session_abandon_switches_home_and_marks_state(
    tmp_path: Path, monkeypatch
) -> None:
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert runner.invoke(app, ["init"], catch_exceptions=False).exit_code == 0
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )
    session_branch = run_git(root, "branch", "--show-current").stdout.strip()
    session_id = session_branch.removeprefix("cmoc/session/")
    state_path = root / ".cmoc" / "sessions" / f"{session_id}.json"

    result = runner.invoke(app, ["session", "abandon"], catch_exceptions=False)

    assert result.exit_code == 0
    assert run_git(root, "branch", "--show-current").stdout.strip() == "master"
    assert (
        subprocess.run(
            ["git", "rev-parse", "--verify", session_branch], cwd=root
        ).returncode
        != 0
    )
    state = json.loads(state_path.read_text())
    assert state["session"]["state"] == "abandoned"
    assert state["session"]["joined_at"] is None
    assert f"- abandoned_branch: `{session_branch}`" in result.output
    assert "- session_state: `abandoned`" in result.output
    assert "- joined_at: `None`" in result.output


def test_session_abandon_requires_existing_home_branch(
    tmp_path: Path, monkeypatch
) -> None:
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert runner.invoke(app, ["init"], catch_exceptions=False).exit_code == 0
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )
    session_branch = run_git(root, "branch", "--show-current").stdout.strip()
    run_git(root, "branch", "-D", "master")

    result = runner.invoke(app, ["session", "abandon"])

    assert result.exit_code != 0
    assert run_git(root, "branch", "--show-current").stdout.strip() == session_branch
    assert "session home branch が存在しません。" in result.output
    assert result.stderr == ""
    assert (
        subprocess.run(
            ["git", "rev-parse", "--verify", session_branch], cwd=root
        ).returncode
        == 0
    )


def test_review_oracle_writes_report(tmp_path: Path, monkeypatch) -> None:
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    init_result = runner.invoke(app, ["init"], catch_exceptions=False)
    assert init_result.exit_code == 0
    fork_result = runner.invoke(app, ["session", "fork"], catch_exceptions=False)
    assert fork_result.exit_code == 0
    calls: list[str] = []

    class FakeCodexResult:
        def __init__(self, output_json):
            self.output_json = output_json

    def fake_run_codex_exec(parameter, **kwargs):
        calls.append(kwargs["purpose"])
        schema_name = parameter.structured_output_schema_path.name
        if schema_name == "enumerate_finding.json":
            return FakeCodexResult({"findings": []})
        if schema_name == "merge_finding.json":
            return FakeCodexResult({"operations": []})
        if schema_name in {
            "validate_finding_challenger.json",
            "validate_finding_advocate.json",
        }:
            return FakeCodexResult({"reasons": []})
        if schema_name == "judge_finding.json":
            return FakeCodexResult({"verdict": "reject", "reason": "no finding"})
        raise AssertionError(schema_name)

    monkeypatch.setattr(main_module, "run_codex_exec", fake_run_codex_exec)

    result = runner.invoke(
        app, ["review", "oracle", "--scope", "full"], catch_exceptions=False
    )

    assert result.exit_code == 0
    report_path = Path(
        [line for line in result.output.splitlines() if line.startswith("/")][-1]
    )
    assert report_path.is_file()
    rendered = report_path.read_text()
    assert "# cmoc review oracle report" in rendered
    assert "## Verdict" in rendered
    assert "## Evaluated oracle file" in rendered
    assert "`oracle/spec.md`" in rendered
    assert any(call.startswith("review oracle enumerate findings") for call in calls)


def test_review_oracle_accepts_short_scope_option(tmp_path: Path, monkeypatch) -> None:
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert runner.invoke(app, ["init"], catch_exceptions=False).exit_code == 0
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )

    class FakeCodexResult:
        def __init__(self, output_json):
            self.output_json = output_json

    def fake_run_codex_exec(parameter, **kwargs):
        schema_name = parameter.structured_output_schema_path.name
        if schema_name == "enumerate_finding.json":
            return FakeCodexResult({"findings": []})
        if schema_name == "merge_finding.json":
            return FakeCodexResult({"operations": []})
        if schema_name in {
            "validate_finding_challenger.json",
            "validate_finding_advocate.json",
        }:
            return FakeCodexResult({"reasons": []})
        if schema_name == "judge_finding.json":
            return FakeCodexResult({"verdict": "reject", "reason": "no finding"})
        raise AssertionError(schema_name)

    monkeypatch.setattr(main_module, "run_codex_exec", fake_run_codex_exec)

    result = runner.invoke(
        app, ["review", "oracle", "-s", "full"], catch_exceptions=False
    )

    assert result.exit_code == 0
    report_path = Path(
        [line for line in result.output.splitlines() if line.startswith("/")][-1]
    )
    rendered = report_path.read_text()
    assert "scope: full" in rendered


def test_review_oracle_session_scope_reports_total_and_no_targets(
    tmp_path: Path,
    monkeypatch,
) -> None:
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert runner.invoke(app, ["init"], catch_exceptions=False).exit_code == 0
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )
    calls: list[str] = []

    def fail_run_codex_exec(parameter, **kwargs):
        calls.append(kwargs["purpose"])
        raise AssertionError(
            "no session-scope oracle targets should skip review Codex calls"
        )

    monkeypatch.setattr(main_module, "run_codex_exec", fail_run_codex_exec)

    result = runner.invoke(app, ["review", "oracle"], catch_exceptions=False)

    assert result.exit_code == 0
    assert calls == []
    report_path = Path(
        [line for line in result.output.splitlines() if line.startswith("/")][-1]
    )
    rendered = report_path.read_text()
    assert "scope: session" in rendered
    assert "oracle_count_total: 1" in rendered
    assert "oracle_count_evaluated: 0" in rendered
    assert "result: no_targets" in rendered
    assert "レビュー対象 oracle が 0 件でした。" in rendered


def test_review_oracle_merges_review_index_changes(tmp_path: Path, monkeypatch) -> None:
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert runner.invoke(app, ["init"], catch_exceptions=False).exit_code == 0
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )

    class FakeCodexResult:
        def __init__(self, output_json):
            self.output_json = output_json

    def fake_run_codex_exec(parameter, **kwargs):
        schema_name = parameter.structured_output_schema_path.name
        if schema_name == "enumerate_finding.json":
            (Path.cwd() / "INDEX.md").write_text("# generated review index\n")
            return FakeCodexResult({"findings": []})
        if schema_name == "merge_finding.json":
            return FakeCodexResult({"operations": []})
        if schema_name in {
            "validate_finding_challenger.json",
            "validate_finding_advocate.json",
        }:
            return FakeCodexResult({"reasons": []})
        if schema_name == "judge_finding.json":
            return FakeCodexResult({"verdict": "reject", "reason": "no finding"})
        raise AssertionError(schema_name)

    monkeypatch.setattr(main_module, "run_codex_exec", fake_run_codex_exec)

    result = runner.invoke(
        app, ["review", "oracle", "--scope", "full"], catch_exceptions=False
    )

    assert result.exit_code == 0
    assert (root / "INDEX.md").read_text() == "# generated review index\n"
    rendered = Path(
        [line for line in result.output.splitlines() if line.startswith("/")][-1]
    ).read_text()
    assert "review_join_commit: null" not in rendered
    review_root = root / ".cmoc" / "worktrees" / "review"
    assert (
        not any(path.name == ".git" for path in review_root.rglob(".git"))
        if review_root.exists()
        else True
    )


def test_file_access_mode_values_are_json_ready() -> None:
    assert FileAccessMode.READONLY.value == "readonly"
    assert FileAccessMode.REPO_WRITE.value == "repo_write"


def test_file_access_to_sandbox_mode_supports_repo_write() -> None:
    assert file_access_to_sandbox_mode(FileAccessMode.READONLY) == "read-only"
    assert file_access_to_sandbox_mode(FileAccessMode.PURE_ORACLE_READ) == "read-only"
    assert file_access_to_sandbox_mode(FileAccessMode.REALIZATION_WRITE) == "workspace-write"
    assert file_access_to_sandbox_mode(FileAccessMode.ORACLE_WRITE) == "workspace-write"
    assert file_access_to_sandbox_mode(FileAccessMode.REPO_WRITE) == "workspace-write"


def test_apply_fork_runs_codex_loop_and_updates_state(
    tmp_path: Path, monkeypatch
) -> None:
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    init_result = runner.invoke(app, ["init"], catch_exceptions=False)
    assert init_result.exit_code == 0
    fork_result = runner.invoke(app, ["session", "fork"], catch_exceptions=False)
    assert fork_result.exit_code == 0
    calls: list[str] = []

    class FakeCodexResult:
        def __init__(self, output_json):
            self.output_json = output_json

    def fake_run_codex_exec(parameter, **kwargs):
        calls.append(kwargs["purpose"])
        if parameter.structured_output_schema_path is None:
            return FakeCodexResult(None)
        return FakeCodexResult({"findings": []})

    monkeypatch.setattr(main_module, "run_codex_exec", fake_run_codex_exec)

    result = runner.invoke(
        app, ["apply", "fork", "--scope", "full"], catch_exceptions=False
    )

    assert result.exit_code == 0
    branch = run_git(root, "branch", "--show-current").stdout.strip()
    assert branch.startswith("cmoc/session/")
    session_id = branch.removeprefix("cmoc/session/")
    state = json.loads((root / ".cmoc" / "sessions" / f"{session_id}.json").read_text())
    assert state["apply"]["state"] == "completed"
    assert state["apply"]["apply_branch"].startswith(f"cmoc/apply/{session_id}/")
    assert apply_worktree_from_state(root, state).is_dir()
    assert "apply_worktree" not in state["apply"]
    assert calls
    assert any(call.startswith("apply fork enumerate findings") for call in calls)
    assert "apply fork refine findings" in calls


def test_apply_fork_writes_report_with_change_summary(
    tmp_path: Path, monkeypatch
) -> None:
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert runner.invoke(app, ["init"], catch_exceptions=False).exit_code == 0
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )
    finding = {
        "title": "Update README",
        "evidences": [
            {
                "path": str(root / "README.md"),
                "line_start": 1,
                "line_end": 1,
                "summary": "readme",
            }
        ],
        "oracle_requirement": "test requirement",
        "observed_implementation": "old",
        "reason": "needs update",
        "suggested_fix": "update readme",
    }
    calls: list[str] = []

    class FakeCodexResult:
        def __init__(self, output_json=None, output_text: str = ""):
            self.output_json = output_json
            self.output_text = output_text

    def fake_run_codex_exec(parameter, **kwargs):
        calls.append(kwargs["purpose"])
        schema = (
            parameter.structured_output_schema_path.name
            if parameter.structured_output_schema_path
            else None
        )
        if kwargs["purpose"].startswith("apply fork enumerate findings"):
            return FakeCodexResult({"findings": [finding]})
        if kwargs["purpose"] == "apply fork refine findings":
            return FakeCodexResult({"findings": [finding]})
        if kwargs["purpose"] == "apply fork finding application":
            (Path.cwd() / "README.md").write_text("# updated\n")
            return FakeCodexResult(None)
        if kwargs["purpose"] == "apply fork commit message":
            return FakeCodexResult(output_text="Update README from apply finding\n")
        if schema == "change_summary.json":
            return FakeCodexResult(
                {
                    "changes": [
                        {
                            "category": "ドキュメント",
                            "summary": "README を更新した",
                            "changed_paths": ["README.md"],
                        }
                    ]
                }
            )
        raise AssertionError(kwargs["purpose"])

    monkeypatch.setattr(main_module, "run_codex_exec", fake_run_codex_exec)

    result = runner.invoke(
        app, ["apply", "fork", "--scope", "full"], catch_exceptions=False
    )

    assert result.exit_code == 2
    report_lines = [
        line for line in result.output.splitlines() if line.startswith("- report:")
    ]
    assert report_lines
    report_path = Path(report_lines[-1].split("`")[1])
    assert report_path.is_file()
    rendered = report_path.read_text()
    assert "result: unconverged" in rendered
    assert "# cmoc apply fork report" in rendered
    assert "## Finding Count" in rendered
    assert "ドキュメント: README を更新した (README.md)" in rendered
    assert "apply fork change summary" in calls
    assert "apply fork commit message" in calls
    assert "- returncode: `2`" in result.output
    branch = run_git(root, "branch", "--show-current").stdout.strip()
    session_id = branch.removeprefix("cmoc/session/")
    state = json.loads((root / ".cmoc" / "sessions" / f"{session_id}.json").read_text())
    apply_branch = state["apply"]["apply_branch"]
    assert (
        run_git(root, "log", "-1", "--pretty=%s", apply_branch).stdout.strip()
        == "Update README from apply finding"
    )


def test_apply_fork_rechecks_dirty_files_until_converged(
    tmp_path: Path, monkeypatch
) -> None:
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert runner.invoke(app, ["init"], catch_exceptions=False).exit_code == 0
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )
    finding = {
        "title": "Update README",
        "evidences": [
            {
                "path": str(root / "README.md"),
                "line_start": 1,
                "line_end": 1,
                "summary": "readme",
            }
        ],
        "oracle_requirement": "test requirement",
        "observed_implementation": "old",
        "reason": "needs update",
        "suggested_fix": "update readme",
    }
    enumerate_calls = 0

    class FakeCodexResult:
        def __init__(self, output_json=None, output_text: str = ""):
            self.output_json = output_json
            self.output_text = output_text

    def fake_run_codex_exec(parameter, **kwargs):
        nonlocal enumerate_calls
        purpose = kwargs["purpose"]
        if purpose.startswith("apply fork enumerate findings"):
            enumerate_calls += 1
            return FakeCodexResult(
                {"findings": [finding] if enumerate_calls == 1 else []}
            )
        if purpose == "apply fork refine findings":
            return FakeCodexResult(
                {"findings": [finding] if enumerate_calls == 1 else []}
            )
        if purpose == "apply fork finding application":
            (Path.cwd() / "README.md").write_text("# updated\n")
            return FakeCodexResult(None)
        if purpose == "apply fork commit message":
            return FakeCodexResult(output_text="Update README from apply finding\n")
        if purpose == "apply fork change summary":
            return FakeCodexResult({"changes": []})
        raise AssertionError(purpose)

    monkeypatch.setattr(main_module, "run_codex_exec", fake_run_codex_exec)

    result = runner.invoke(
        app, ["apply", "fork", "--scope", "full"], catch_exceptions=False
    )

    assert result.exit_code == 0
    assert enumerate_calls >= 2
    report_line = [
        line for line in result.output.splitlines() if line.startswith("- report:")
    ][-1]
    report_path = Path(report_line.split("`")[1])
    assert "result: converged" in report_path.read_text()


def test_apply_fork_rejects_forbidden_agents_diff(tmp_path: Path, monkeypatch) -> None:
    root = make_repo(tmp_path)
    (root / ".agents").mkdir()
    (root / ".agents" / "skill.md").write_text("original\n")
    run_git(root, "add", ".agents/skill.md")
    run_git(root, "commit", "-m", "add agents")
    monkeypatch.chdir(root)
    assert runner.invoke(app, ["init"], catch_exceptions=False).exit_code == 0
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )
    finding = {
        "title": "Bad agents edit",
        "evidences": [
            {
                "path": str(root / "README.md"),
                "line_start": 1,
                "line_end": 1,
                "summary": "readme",
            }
        ],
        "oracle_requirement": "test requirement",
        "observed_implementation": "old",
        "reason": "needs update",
        "suggested_fix": "update agents",
    }

    class FakeCodexResult:
        def __init__(self, output_json=None, output_text: str = ""):
            self.output_json = output_json
            self.output_text = output_text

    def fake_run_codex_exec(parameter, **kwargs):
        purpose = kwargs["purpose"]
        if purpose.startswith("apply fork enumerate findings"):
            return FakeCodexResult({"findings": [finding]})
        if purpose == "apply fork refine findings":
            return FakeCodexResult({"findings": [finding]})
        if purpose == "apply fork finding application":
            (Path.cwd() / ".agents" / "skill.md").write_text("forbidden\n")
            return FakeCodexResult()
        raise AssertionError(purpose)

    monkeypatch.setattr(main_module, "run_codex_exec", fake_run_codex_exec)

    result = runner.invoke(app, ["apply", "fork", "--scope", "full"])

    assert result.exit_code != 0
    assert "編集禁止対象" in result.output
    branch = run_git(root, "branch", "--show-current").stdout.strip()
    session_id = branch.removeprefix("cmoc/session/")
    state = json.loads((root / ".cmoc" / "sessions" / f"{session_id}.json").read_text())
    assert state["apply"]["state"] == "error"


def test_apply_abandon_removes_apply_worktree_and_branch(
    tmp_path: Path, monkeypatch
) -> None:
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert runner.invoke(app, ["init"], catch_exceptions=False).exit_code == 0
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )

    class FakeCodexResult:
        output_json = {"findings": []}

    monkeypatch.setattr(
        main_module, "run_codex_exec", lambda parameter, **kwargs: FakeCodexResult()
    )
    assert runner.invoke(app, ["apply", "fork"], catch_exceptions=False).exit_code == 0
    session_branch = run_git(root, "branch", "--show-current").stdout.strip()
    session_id = session_branch.removeprefix("cmoc/session/")
    state_path = root / ".cmoc" / "sessions" / f"{session_id}.json"
    state = json.loads(state_path.read_text())
    apply_branch = state["apply"]["apply_branch"]
    apply_worktree = apply_worktree_from_state(root, state)
    assert apply_worktree.is_dir()

    result = runner.invoke(app, ["apply", "abandon"], catch_exceptions=False)

    assert result.exit_code == 0
    assert f"- apply_branch: `{apply_branch}`" in result.output
    assert f"- apply_worktree: `{apply_worktree}`" in result.output
    assert "- before: `completed`" in result.output
    assert "- after: `ready`" in result.output
    assert "- warnings:" in result.output
    assert not apply_worktree.exists()
    assert (
        subprocess.run(
            ["git", "rev-parse", "--verify", apply_branch], cwd=root
        ).returncode
        != 0
    )
    state = json.loads(state_path.read_text())
    assert state["apply"]["state"] == "ready"
    assert state["apply"]["apply_branch"] is None
    assert "apply_worktree" not in state["apply"]


def test_apply_abandon_reports_missing_cleanup_targets_as_warnings(
    tmp_path: Path, monkeypatch
) -> None:
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert runner.invoke(app, ["init"], catch_exceptions=False).exit_code == 0
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )

    class FakeCodexResult:
        output_json = {"findings": []}

    monkeypatch.setattr(
        main_module, "run_codex_exec", lambda parameter, **kwargs: FakeCodexResult()
    )
    assert runner.invoke(app, ["apply", "fork"], catch_exceptions=False).exit_code == 0
    session_branch = run_git(root, "branch", "--show-current").stdout.strip()
    session_id = session_branch.removeprefix("cmoc/session/")
    state_path = root / ".cmoc" / "sessions" / f"{session_id}.json"
    state = json.loads(state_path.read_text())
    apply_branch = state["apply"]["apply_branch"]
    apply_worktree = apply_worktree_from_state(root, state)
    run_git(root, "worktree", "remove", "--force", str(apply_worktree))
    run_git(root, "branch", "-D", apply_branch)

    result = runner.invoke(app, ["apply", "abandon"], catch_exceptions=False)

    assert result.exit_code == 0
    assert f"apply worktree already missing for branch: {apply_branch}" in result.output
    assert f"apply branch already missing: {apply_branch}" in result.output
    state = json.loads(state_path.read_text())
    assert state["apply"]["state"] == "ready"
    assert state["apply"]["apply_branch"] is None
    assert "apply_worktree" not in state["apply"]


def test_apply_abandon_can_run_from_apply_worktree(tmp_path: Path, monkeypatch) -> None:
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert runner.invoke(app, ["init"], catch_exceptions=False).exit_code == 0
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )

    class FakeCodexResult:
        output_json = {"findings": []}

    monkeypatch.setattr(
        main_module, "run_codex_exec", lambda parameter, **kwargs: FakeCodexResult()
    )
    assert runner.invoke(app, ["apply", "fork"], catch_exceptions=False).exit_code == 0
    session_branch = run_git(root, "branch", "--show-current").stdout.strip()
    session_id = session_branch.removeprefix("cmoc/session/")
    state_path = root / ".cmoc" / "sessions" / f"{session_id}.json"
    state = json.loads(state_path.read_text())
    apply_branch = state["apply"]["apply_branch"]
    apply_worktree = apply_worktree_from_state(root, state)
    monkeypatch.chdir(apply_worktree)

    result = runner.invoke(app, ["apply", "abandon"], catch_exceptions=False)

    assert result.exit_code == 0
    assert Path.cwd() == root
    assert not apply_worktree.exists()
    assert (
        subprocess.run(
            ["git", "rev-parse", "--verify", apply_branch], cwd=root
        ).returncode
        != 0
    )
    state = json.loads(state_path.read_text())
    assert state["apply"]["state"] == "ready"


def test_apply_join_removes_apply_worktree_and_resets_state(
    tmp_path: Path, monkeypatch
) -> None:
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert runner.invoke(app, ["init"], catch_exceptions=False).exit_code == 0
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )

    class FakeCodexResult:
        output_json = {"findings": []}

    monkeypatch.setattr(
        main_module, "run_codex_exec", lambda parameter, **kwargs: FakeCodexResult()
    )
    assert runner.invoke(app, ["apply", "fork"], catch_exceptions=False).exit_code == 0
    session_branch = run_git(root, "branch", "--show-current").stdout.strip()
    session_id = session_branch.removeprefix("cmoc/session/")
    state_path = root / ".cmoc" / "sessions" / f"{session_id}.json"
    state = json.loads(state_path.read_text())
    apply_branch = state["apply"]["apply_branch"]
    apply_worktree = apply_worktree_from_state(root, state)

    result = runner.invoke(app, ["apply", "join"], catch_exceptions=False)

    assert result.exit_code == 0
    assert not apply_worktree.exists()
    assert (
        subprocess.run(
            ["git", "rev-parse", "--verify", apply_branch], cwd=root
        ).returncode
        != 0
    )
    state = json.loads(state_path.read_text())
    assert state["apply"]["state"] == "ready"
    assert state["session"]["last_joined_apply_oracle_snapshot_commit"] is not None


def test_apply_join_can_run_from_apply_worktree(tmp_path: Path, monkeypatch) -> None:
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert runner.invoke(app, ["init"], catch_exceptions=False).exit_code == 0
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )

    class FakeCodexResult:
        output_json = {"findings": []}

    monkeypatch.setattr(
        main_module, "run_codex_exec", lambda parameter, **kwargs: FakeCodexResult()
    )
    assert runner.invoke(app, ["apply", "fork"], catch_exceptions=False).exit_code == 0
    session_branch = run_git(root, "branch", "--show-current").stdout.strip()
    session_id = session_branch.removeprefix("cmoc/session/")
    state_path = root / ".cmoc" / "sessions" / f"{session_id}.json"
    state = json.loads(state_path.read_text())
    apply_branch = state["apply"]["apply_branch"]
    apply_worktree = apply_worktree_from_state(root, state)
    monkeypatch.chdir(apply_worktree)

    result = runner.invoke(app, ["apply", "join"], catch_exceptions=False)

    assert result.exit_code == 0
    assert Path.cwd() == root
    assert not apply_worktree.exists()
    assert (
        subprocess.run(
            ["git", "rev-parse", "--verify", apply_branch], cwd=root
        ).returncode
        != 0
    )
    state = json.loads(state_path.read_text())
    assert state["apply"]["state"] == "ready"
    assert state["session"]["last_joined_apply_oracle_snapshot_commit"] is not None
    assert "- cleanup_reachable: `True`" in result.output
    assert "  - none" in result.output


def test_apply_join_from_apply_worktree_requires_clean_apply_worktree(
    tmp_path: Path, monkeypatch
) -> None:
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert runner.invoke(app, ["init"], catch_exceptions=False).exit_code == 0
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )

    class FakeCodexResult:
        output_json = {"findings": []}

    monkeypatch.setattr(
        main_module, "run_codex_exec", lambda parameter, **kwargs: FakeCodexResult()
    )
    assert runner.invoke(app, ["apply", "fork"], catch_exceptions=False).exit_code == 0
    session_branch = run_git(root, "branch", "--show-current").stdout.strip()
    session_id = session_branch.removeprefix("cmoc/session/")
    state_path = root / ".cmoc" / "sessions" / f"{session_id}.json"
    state = json.loads(state_path.read_text())
    apply_branch = state["apply"]["apply_branch"]
    apply_worktree = apply_worktree_from_state(root, state)
    (apply_worktree / "dirty.txt").write_text("dirty\n")
    monkeypatch.chdir(apply_worktree)

    result = runner.invoke(app, ["apply", "join"])

    assert result.exit_code != 0
    assert apply_worktree.exists()
    assert (
        subprocess.run(
            ["git", "rev-parse", "--verify", apply_branch], cwd=root
        ).returncode
        == 0
    )
    state = json.loads(state_path.read_text())
    assert state["apply"]["state"] == "completed"
    assert "git 未コミット差分が存在します。" in result.output
    assert result.stderr == ""


def test_apply_join_reports_unexpected_apply_diff_and_force_reverts(
    tmp_path: Path, monkeypatch
) -> None:
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert runner.invoke(app, ["init"], catch_exceptions=False).exit_code == 0
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )

    class FakeCodexResult:
        output_json = {"findings": []}

    monkeypatch.setattr(
        main_module, "run_codex_exec", lambda parameter, **kwargs: FakeCodexResult()
    )
    assert runner.invoke(app, ["apply", "fork"], catch_exceptions=False).exit_code == 0
    session_branch = run_git(root, "branch", "--show-current").stdout.strip()
    session_id = session_branch.removeprefix("cmoc/session/")
    state_path = root / ".cmoc" / "sessions" / f"{session_id}.json"
    state = json.loads(state_path.read_text())
    apply_worktree = apply_worktree_from_state(root, state)
    (apply_worktree / "oracle" / "spec.md").write_text("# changed oracle in apply\n")
    run_git(apply_worktree, "add", "oracle/spec.md")
    run_git(apply_worktree, "commit", "-m", "unexpected oracle change")

    normal = runner.invoke(app, ["apply", "join"], catch_exceptions=False)

    assert normal.exit_code == 1
    assert "想定外差分" in normal.output
    forced = runner.invoke(
        app, ["apply", "join", "--force-resolve"], catch_exceptions=False
    )
    assert forced.exit_code == 0
    assert (root / "oracle" / "spec.md").read_text() == "# spec\n"


def test_apply_join_treats_gitignore_change_as_unexpected_apply_diff(
    tmp_path: Path,
    monkeypatch,
) -> None:
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert runner.invoke(app, ["init"], catch_exceptions=False).exit_code == 0
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )

    class FakeCodexResult:
        output_json = {"findings": []}

    monkeypatch.setattr(
        main_module, "run_codex_exec", lambda parameter, **kwargs: FakeCodexResult()
    )
    assert runner.invoke(app, ["apply", "fork"], catch_exceptions=False).exit_code == 0
    state_path = (
        root
        / ".cmoc"
        / "sessions"
        / f"{run_git(root, 'branch', '--show-current').stdout.strip().removeprefix('cmoc/session/')}.json"
    )
    state = json.loads(state_path.read_text())
    apply_worktree = apply_worktree_from_state(root, state)
    original_gitignore = (apply_worktree / ".gitignore").read_text()
    (apply_worktree / ".gitignore").write_text(original_gitignore + "# unexpected\n")
    run_git(apply_worktree, "add", ".gitignore")
    run_git(apply_worktree, "commit", "-m", "unexpected gitignore change")

    normal = runner.invoke(app, ["apply", "join"], catch_exceptions=False)

    assert normal.exit_code == 1
    assert "想定外差分" in normal.output
    assert ".gitignore" in normal.output
    forced = runner.invoke(
        app, ["apply", "join", "--force-resolve"], catch_exceptions=False
    )
    assert forced.exit_code == 0
    assert (root / ".gitignore").read_text() == original_gitignore


def test_resolve_index_conflicts_deletes_index_and_commits(tmp_path: Path) -> None:
    root = make_repo(tmp_path)
    (root / "INDEX.md").write_text("base\n")
    run_git(root, "add", "INDEX.md")
    run_git(root, "commit", "-m", "add index")
    run_git(root, "switch", "-c", "side")
    (root / "INDEX.md").write_text("side\n")
    run_git(root, "add", "INDEX.md")
    run_git(root, "commit", "-m", "side index")
    run_git(root, "switch", "master")
    (root / "INDEX.md").write_text("master\n")
    run_git(root, "add", "INDEX.md")
    run_git(root, "commit", "-m", "master index")
    merge = subprocess.run(
        ["git", "merge", "--no-ff", "side"], cwd=root, text=True, capture_output=True
    )
    assert merge.returncode != 0

    resolved = main_module.resolve_index_conflicts(root)

    assert resolved is True
    assert not (root / "INDEX.md").exists()
    assert (
        subprocess.run(
            ["git", "diff", "--name-only", "--diff-filter=U"],
            cwd=root,
            text=True,
            capture_output=True,
        ).stdout.strip()
        == ""
    )
    assert "Merge branch 'side'" in run_git(root, "log", "-1", "--pretty=%B").stdout


def test_session_join_resolves_conflict_with_codex(tmp_path: Path, monkeypatch) -> None:
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert runner.invoke(app, ["init"], catch_exceptions=False).exit_code == 0
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )
    session_branch = run_git(root, "branch", "--show-current").stdout.strip()
    (root / "README.md").write_text("session change\n")
    run_git(root, "add", "README.md")
    run_git(root, "commit", "-m", "session change")
    run_git(root, "switch", "master")
    (root / "README.md").write_text("home change\n")
    run_git(root, "add", "README.md")
    run_git(root, "commit", "-m", "home change")
    run_git(root, "switch", session_branch)
    calls: list[str] = []

    class FakeCodexResult:
        output_json = None

    def fake_run_codex_exec(parameter, **kwargs):
        calls.append(kwargs["purpose"])
        (root / "README.md").write_text("resolved change\n")
        return FakeCodexResult()

    monkeypatch.setattr(main_module, "run_codex_exec", fake_run_codex_exec)

    result = runner.invoke(app, ["session", "join"], catch_exceptions=False)

    assert result.exit_code == 0
    assert run_git(root, "branch", "--show-current").stdout.strip() == "master"
    assert (root / "README.md").read_text() == "resolved change\n"
    assert calls == ["session join conflict resolution"]


def test_session_join_warns_when_session_branch_cannot_be_deleted(
    tmp_path: Path, monkeypatch
) -> None:
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert runner.invoke(app, ["init"], catch_exceptions=False).exit_code == 0
    assert (
        runner.invoke(app, ["session", "fork"], catch_exceptions=False).exit_code == 0
    )
    session_branch = run_git(root, "branch", "--show-current").stdout.strip()
    original_run_git = main_module.run_git

    def fake_run_git(args, cwd, check=True):
        if args == ["branch", "-d", session_branch]:
            return cmoc_runtime.CommandResult(1, "", "branch is checked out elsewhere")
        return original_run_git(args, cwd, check=check)

    monkeypatch.setattr(main_module, "run_git", fake_run_git)

    result = runner.invoke(app, ["session", "join"], catch_exceptions=False)

    assert result.exit_code == 0
    assert run_git(root, "branch", "--show-current").stdout.strip() == "master"
    assert (
        subprocess.run(
            ["git", "rev-parse", "--verify", session_branch], cwd=root
        ).returncode
        == 0
    )
    assert "- deleted_session_branch: `False`" in result.output
    assert f"session branch was not deleted: {session_branch}" in result.output


def test_indexing_uses_codex_index_entry_builder_and_commits(
    tmp_path: Path, monkeypatch
) -> None:
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert runner.invoke(app, ["init"], catch_exceptions=False).exit_code == 0
    calls: list[str] = []

    class FakeCodexResult:
        output_json = {
            "summary": ["generated summary"],
            "read_this_when": ["generated read condition"],
            "do_not_read_this_when": ["generated skip condition"],
        }

    def fake_run_codex_exec(parameter, **kwargs):
        calls.append(kwargs["purpose"])
        assert parameter.structured_output_schema_path.name == "index_entry.json"
        return FakeCodexResult()

    monkeypatch.setattr(main_module, "run_codex_exec", fake_run_codex_exec)

    result = runner.invoke(app, ["indexing"], catch_exceptions=False)

    assert result.exit_code == 0
    assert calls
    root_index = root / "INDEX.md"
    assert root_index.is_file()
    rendered = root_index.read_text()
    assert "generated summary" in rendered
    assert "generated read condition" in rendered
    assert "generated skip condition" in rendered
    assert run_git(root, "status", "--short").stdout.strip() == ""
    assert "cmoc indexing" in run_git(root, "log", "--oneline", "-1").stdout


def test_indexing_skips_codex_when_existing_hashes_are_fresh(
    tmp_path: Path, monkeypatch
) -> None:
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert runner.invoke(app, ["init"], catch_exceptions=False).exit_code == 0

    class FakeCodexResult:
        output_json = {
            "summary": ["generated summary"],
            "read_this_when": ["generated read condition"],
            "do_not_read_this_when": ["generated skip condition"],
        }

    monkeypatch.setattr(
        main_module, "run_codex_exec", lambda parameter, **kwargs: FakeCodexResult()
    )
    first = runner.invoke(app, ["indexing"], catch_exceptions=False)
    assert first.exit_code == 0
    root_index_before = (root / "INDEX.md").read_text()
    head_before = run_git(root, "rev-parse", "HEAD").stdout.strip()

    calls: list[str] = []

    def fail_if_called(parameter, **kwargs):
        calls.append(kwargs["purpose"])
        raise AssertionError("fresh INDEX.md should not require Codex")

    monkeypatch.setattr(main_module, "run_codex_exec", fail_if_called)
    second = runner.invoke(app, ["indexing"], catch_exceptions=False)

    assert second.exit_code == 0
    assert calls == []
    assert (root / "INDEX.md").read_text() == root_index_before
    assert run_git(root, "rev-parse", "HEAD").stdout.strip() == head_before
    assert run_git(root, "status", "--short").stdout.strip() == ""


def test_update_indexes_generates_sibling_entries_in_parallel(
    tmp_path: Path, monkeypatch
) -> None:
    root = make_repo(tmp_path)
    docs = root / "docs"
    docs.mkdir()
    (docs / "a.txt").write_text("a\n")
    (docs / "b.txt").write_text("b\n")
    cmoc_runtime.sync_config(root)
    active = 0
    max_active = 0
    lock = threading.Lock()

    def fake_build_index_entry(
        update_root: Path, path: Path, digest: str | None = None
    ) -> str:
        nonlocal active, max_active
        if path.parent == docs:
            with lock:
                active += 1
                max_active = max(max_active, active)
            time.sleep(0.05)
            with lock:
                active -= 1
        return main_module.render_index_entry(
            update_root,
            path,
            {
                "summary": [path.name],
                "read_this_when": [path.name],
                "do_not_read_this_when": [path.name],
            },
            digest=digest,
        ).rstrip()

    monkeypatch.setattr(main_module, "build_index_entry", fake_build_index_entry)

    updated = main_module.update_indexes(root)

    assert docs / "INDEX.md" in updated
    assert max_active >= 2


def test_command_codex_call_runs_indexing_preflight(
    tmp_path: Path, monkeypatch
) -> None:
    root = make_repo(tmp_path)
    index_path = root / "INDEX.md"
    parameter = AgentCallParameter(
        ModelClass.EFFICIENCY,
        ReasoningEffort.LOW,
        FileAccessMode.READONLY,
        "prompt",
        None,
    )
    events: list[str] = []

    def fake_update_indexes(update_root: Path) -> list[Path]:
        events.append("indexing")
        assert update_root == root
        index_path.write_text("# generated\n")
        return [index_path]

    class FakeCodexResult:
        output_json = None

    def fake_runtime_run_codex_exec(call_parameter, **kwargs):
        events.append("codex")
        assert call_parameter == parameter
        return FakeCodexResult()

    monkeypatch.setattr(main_module, "update_indexes", fake_update_indexes)
    monkeypatch.setattr(
        main_module, "runtime_run_codex_exec", fake_runtime_run_codex_exec
    )

    result = main_module.run_codex_exec(
        parameter, root=root, purpose="apply fork refine findings"
    )

    assert isinstance(result, FakeCodexResult)
    assert events == ["indexing", "codex"]
    assert run_git(root, "log", "-1", "--pretty=%s").stdout.strip() == "cmoc indexing"
    assert run_git(root, "status", "--short").stdout.strip() == ""


def test_command_codex_call_skips_indexing_for_index_entry_and_conflict_resolution(
    tmp_path: Path,
    monkeypatch,
) -> None:
    root = make_repo(tmp_path)
    parameter = AgentCallParameter(
        ModelClass.EFFICIENCY,
        ReasoningEffort.LOW,
        FileAccessMode.READONLY,
        "prompt",
        None,
    )
    calls: list[str] = []

    class FakeCodexResult:
        output_json = None

    def fail_update_indexes(update_root: Path) -> list[Path]:
        raise AssertionError("indexing preflight should be skipped")

    def fake_runtime_run_codex_exec(call_parameter, **kwargs):
        calls.append(kwargs["purpose"])
        return FakeCodexResult()

    monkeypatch.setattr(main_module, "update_indexes", fail_update_indexes)
    monkeypatch.setattr(
        main_module, "runtime_run_codex_exec", fake_runtime_run_codex_exec
    )

    main_module.run_codex_exec(
        parameter, root=root, purpose="indexing index entry for README.md"
    )
    main_module.run_codex_exec(
        parameter, root=root, purpose="session join conflict resolution"
    )

    assert calls == [
        "indexing index entry for README.md",
        "session join conflict resolution",
    ]


def test_run_codex_exec_uses_stdin_and_writes_logs(
    tmp_path: Path, monkeypatch, capsys
) -> None:
    root = make_repo(tmp_path)
    codex_home = setup_codex_home(tmp_path, monkeypatch)
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    recorder = tmp_path / "record.json"
    fake_codex = bin_dir / "codex"
    fake_codex.write_text(
        "\n".join(
            [
                "#!/usr/bin/env python3",
                "import json, os, pathlib, sys",
                f"record = pathlib.Path({str(recorder)!r})",
                "stdin = sys.stdin.read()",
                "args = sys.argv[1:]",
                "output = pathlib.Path(args[args.index('--output-last-message') + 1])",
                "output.write_text(json.dumps({'ok': True, 'stdin': stdin}))",
                "record.write_text(json.dumps({'args': args, 'stdin': stdin, 'codex_home': os.environ.get('CODEX_HOME')}))",
                "print(json.dumps({'type': 'turn.completed'}))",
            ]
        )
        + "\n"
    )
    fake_codex.chmod(0o755)
    monkeypatch.setenv("PATH", f"{bin_dir}:{Path('/usr/bin')}")
    schema = tmp_path / "schema.json"
    schema.write_text(
        json.dumps(
            {
                "type": "object",
                "additionalProperties": False,
                "required": ["ok", "stdin"],
                "properties": {"ok": {"type": "boolean"}, "stdin": {"type": "string"}},
            }
        )
    )
    parameter = AgentCallParameter(
        ModelClass.EFFICIENCY,
        ReasoningEffort.LOW,
        FileAccessMode.READONLY,
        "SECRET PROMPT BODY",
        schema,
    )
    logger = SubcommandLogger(root, "test")

    result = run_codex_exec(
        parameter,
        root=root,
        capacity_initial_sleep_sec=0,
        subcommand_logger=logger,
    )

    recorded = json.loads(recorder.read_text())
    assert recorded["stdin"] == "SECRET PROMPT BODY"
    assert recorded["codex_home"] == str(codex_home)
    assert "SECRET PROMPT BODY" not in " ".join(recorded["args"])
    assert recorded["args"][:2] == ["exec", "--profile"]
    assert recorded["args"][2].startswith("cmoc_")
    assert "/" not in recorded["args"][2]
    assert "--json" in recorded["args"]
    assert "--output-schema" in recorded["args"]
    assert recorded["args"][-1] == "-"
    assert result.output_json == {"ok": True, "stdin": "SECRET PROMPT BODY"}
    assert result.call_log_path.is_file()
    assert result.stdout_log_path.read_text().strip() == '{"type": "turn.completed"}'
    assert result.stderr_log_path.read_text() == ""
    assert result.codex_home == codex_home
    assert result.profile_name == recorded["args"][2]
    assert result.profile_path.name.startswith("cmoc_")
    assert result.profile_path.suffixes == [".config", ".toml"]
    assert result.profile_path.parent == codex_home
    assert result.schema_path is not None
    assert result.schema_path.parent == root / ".cmoc" / "state" / "schema"
    call_log = json.loads(result.call_log_path.read_text())
    assert call_log["codex_home"] == str(codex_home)
    assert call_log["profile_name"] == result.profile_name
    log_events = [json.loads(line) for line in logger.path.read_text().splitlines()]
    codex_events = [event for event in log_events if event["event"] == "codex_call"]
    assert len(codex_events) == 1
    assert codex_events[0]["purpose"] == "codex exec"
    assert codex_events[0]["status"] == "succeeded"
    assert codex_events[0]["returncode"] == 0
    assert codex_events[0]["call_log_path"] == str(result.call_log_path)
    assert codex_events[0]["stdout_log_path"] == str(result.stdout_log_path)
    assert codex_events[0]["codex_home"] == str(codex_home)
    assert codex_events[0]["profile_name"] == result.profile_name
    assert codex_events[0]["elapsed_sec"] >= 0
    console = capsys.readouterr().out
    assert "# " in console
    assert "Codex CLI call" in console
    assert "- purpose: `codex exec`" in console
    assert f"- call_log: `{result.call_log_path}`" in console
    assert "- returncode: `0`" in console


def test_run_codex_exec_stores_schema_in_cwd_work_root(
    tmp_path: Path, monkeypatch
) -> None:
    root = make_repo(tmp_path)
    setup_codex_home(tmp_path, monkeypatch)
    linked = root / ".cmoc" / "worktrees" / "apply"
    linked.parent.mkdir(parents=True)
    run_git(root, "worktree", "add", "-b", "apply-test", str(linked), "HEAD")
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    recorder = tmp_path / "record.json"
    fake_codex = bin_dir / "codex"
    fake_codex.write_text(
        "\n".join(
            [
                "#!/usr/bin/env python3",
                "import json, os, pathlib, sys",
                f"record = pathlib.Path({str(recorder)!r})",
                "args = sys.argv[1:]",
                "output = pathlib.Path(args[args.index('--output-last-message') + 1])",
                "output.write_text(json.dumps({'ok': True}))",
                "record.write_text(json.dumps({'args': args, 'cwd': os.getcwd()}))",
                "print(json.dumps({'type': 'turn.completed'}))",
            ]
        )
        + "\n"
    )
    fake_codex.chmod(0o755)
    monkeypatch.setenv("PATH", f"{bin_dir}:{Path('/usr/bin')}")
    schema = tmp_path / "schema.json"
    schema.write_text(
        json.dumps(
            {
                "type": "object",
                "additionalProperties": False,
                "required": ["ok"],
                "properties": {"ok": {"type": "boolean"}},
            }
        )
    )
    parameter = AgentCallParameter(
        ModelClass.EFFICIENCY,
        ReasoningEffort.LOW,
        FileAccessMode.READONLY,
        "prompt",
        schema,
    )

    result = run_codex_exec(
        parameter, root=root, cwd=linked, capacity_initial_sleep_sec=0
    )

    recorded = json.loads(recorder.read_text())
    schema_arg = recorded["args"][recorded["args"].index("--output-schema") + 1]
    assert recorded["cwd"] == str(linked)
    assert result.output_json == {"ok": True}
    assert result.call_log_path.parent == root / ".cmoc" / "log" / "codex"
    assert result.schema_path is not None
    assert result.schema_path.parent == linked / ".cmoc" / "state" / "schema"
    assert schema_arg == str(result.schema_path)
    assert not (root / ".cmoc" / "state" / "schema").exists()


def test_run_codex_tui_uses_codex_command_and_prompt_argument(
    tmp_path: Path,
    monkeypatch,
) -> None:
    root = make_repo(tmp_path)
    codex_home = setup_codex_home(tmp_path, monkeypatch)
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    fake_codex = bin_dir / "codex"
    fake_codex.write_text("#!/bin/sh\nexit 0\n")
    fake_codex.chmod(0o755)
    monkeypatch.setenv("PATH", f"{bin_dir}:{Path('/usr/bin')}")
    recorded = {}

    def fake_run(argv, **kwargs):
        recorded.update({"argv": argv, "kwargs": kwargs})
        return subprocess.CompletedProcess(argv, 0)

    monkeypatch.setattr(cmoc_runtime.subprocess, "run", fake_run)
    parameter = AgentCallParameter(
        ModelClass.MAINSTREAM,
        ReasoningEffort.MEDIUM,
        FileAccessMode.REPO_WRITE,
        "TUI PROMPT BODY",
        None,
    )

    result = run_codex_tui(parameter, root=root)

    assert recorded["kwargs"]["cwd"] == root
    assert recorded["kwargs"]["env"]["CODEX_HOME"] == str(codex_home)
    assert "capture_output" not in recorded["kwargs"]
    assert "stdout" not in recorded["kwargs"]
    assert "stderr" not in recorded["kwargs"]
    assert recorded["argv"][0] == "codex"
    assert recorded["argv"][1] == "--profile"
    assert recorded["argv"][2].startswith("cmoc_")
    assert "exec" not in recorded["argv"]
    assert recorded["argv"][-1] == "TUI PROMPT BODY"
    call_logs = list((root / ".cmoc" / "log" / "codex").glob("*_tui_call.json"))
    assert len(call_logs) == 1
    assert json.loads(call_logs[0].read_text())["argv"] == [
        "codex",
        "--profile",
        recorded["argv"][2],
        "TUI PROMPT BODY",
    ]
    assert result.returncode == 0
    assert result.stdout == ""
    assert result.stderr == ""


def test_run_codex_exec_loads_repo_config_json(tmp_path: Path, monkeypatch) -> None:
    root = make_repo(tmp_path)
    setup_codex_home(tmp_path, monkeypatch)
    config = cmoc_runtime.config_to_dict(cmoc_runtime.sync_config(root))
    config["codex"]["model"]["efficiency"] = "CUSTOM-EFFICIENCY"
    config["codex"]["reasoning_effort"]["low"] = "minimal"
    (root / ".cmoc" / "config.json").write_text(json.dumps(config, indent=2) + "\n")
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    fake_codex = bin_dir / "codex"
    fake_codex.write_text(
        "\n".join(
            [
                "#!/usr/bin/env python3",
                "import json, pathlib, sys",
                "args = sys.argv[1:]",
                "output = pathlib.Path(args[args.index('--output-last-message') + 1])",
                "output.write_text('done\\n')",
                "print(json.dumps({'type': 'turn.completed'}))",
            ]
        )
        + "\n"
    )
    fake_codex.chmod(0o755)
    monkeypatch.setenv("PATH", f"{bin_dir}:{Path('/usr/bin')}")
    parameter = AgentCallParameter(
        ModelClass.EFFICIENCY,
        ReasoningEffort.LOW,
        FileAccessMode.READONLY,
        "prompt",
        None,
    )

    result = run_codex_exec(parameter, root=root, capacity_initial_sleep_sec=0)

    profile = result.profile_path.read_text()
    assert 'model = "CUSTOM-EFFICIENCY"' in profile
    assert 'reasoning_effort = "minimal"' in profile


def test_run_codex_exec_uses_default_codex_home_when_env_unset(
    tmp_path: Path, monkeypatch
) -> None:
    root = make_repo(tmp_path)
    home = tmp_path / "home"
    codex_home = home / ".codex"
    codex_home.mkdir(parents=True)
    (codex_home / "auth.json").write_text("{}\n")
    monkeypatch.delenv("CODEX_HOME", raising=False)
    monkeypatch.setattr(Path, "home", lambda: home)
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    recorder = tmp_path / "record.json"
    fake_codex = bin_dir / "codex"
    fake_codex.write_text(
        "\n".join(
            [
                "#!/usr/bin/env python3",
                "import json, os, pathlib",
                f"record = pathlib.Path({str(recorder)!r})",
                "args = __import__('sys').argv[1:]",
                "output = pathlib.Path(args[args.index('--output-last-message') + 1])",
                "output.write_text('done\\n')",
                "record.write_text(json.dumps({'codex_home': os.environ.get('CODEX_HOME'), 'args': args}))",
                "print(json.dumps({'type': 'turn.completed'}))",
            ]
        )
        + "\n"
    )
    fake_codex.chmod(0o755)
    monkeypatch.setenv("PATH", f"{bin_dir}:{Path('/usr/bin')}")
    parameter = AgentCallParameter(
        ModelClass.EFFICIENCY,
        ReasoningEffort.LOW,
        FileAccessMode.READONLY,
        "prompt",
        None,
    )

    result = run_codex_exec(parameter, root=root, capacity_initial_sleep_sec=0)

    recorded = json.loads(recorder.read_text())
    assert recorded["codex_home"] == str(codex_home)
    assert recorded["args"][2] == result.profile_name
    assert result.codex_home == codex_home
    assert result.profile_path.parent == codex_home


def test_run_codex_exec_fails_before_codex_when_codex_home_missing(
    tmp_path: Path, monkeypatch
) -> None:
    root = make_repo(tmp_path)
    missing_home = tmp_path / "missing_codex_home"
    monkeypatch.setenv("CODEX_HOME", str(missing_home))
    parameter = AgentCallParameter(
        ModelClass.EFFICIENCY,
        ReasoningEffort.LOW,
        FileAccessMode.READONLY,
        "prompt",
        None,
    )

    try:
        run_codex_exec(parameter, root=root, capacity_initial_sleep_sec=0)
    except CmocError as exc:
        error = exc
    else:
        raise AssertionError("run_codex_exec should fail before invoking Codex CLI")

    assert error.summary == "Codex home が存在しません。"
    assert str(missing_home) in error.detail
    assert "Codex CLI の通常利用環境を初期化してください。" in error.next_actions


def test_run_codex_exec_fails_before_codex_when_codex_home_is_file(
    tmp_path: Path, monkeypatch
) -> None:
    root = make_repo(tmp_path)
    codex_home = tmp_path / "codex_home_file"
    codex_home.write_text("not a directory\n")
    monkeypatch.setenv("CODEX_HOME", str(codex_home))
    parameter = AgentCallParameter(
        ModelClass.EFFICIENCY,
        ReasoningEffort.LOW,
        FileAccessMode.READONLY,
        "prompt",
        None,
    )

    try:
        run_codex_exec(parameter, root=root, capacity_initial_sleep_sec=0)
    except CmocError as exc:
        error = exc
    else:
        raise AssertionError("run_codex_exec should fail before invoking Codex CLI")

    assert error.summary == "Codex home がディレクトリではありません。"
    assert str(codex_home) in error.detail
    assert "CODEX_HOME のファイル種別を確認してください。" in error.next_actions


def test_run_codex_exec_fails_before_codex_when_auth_json_missing(
    tmp_path: Path, monkeypatch
) -> None:
    root = make_repo(tmp_path)
    codex_home = tmp_path / "codex_home"
    codex_home.mkdir()
    monkeypatch.setenv("CODEX_HOME", str(codex_home))
    parameter = AgentCallParameter(
        ModelClass.EFFICIENCY,
        ReasoningEffort.LOW,
        FileAccessMode.READONLY,
        "prompt",
        None,
    )

    try:
        run_codex_exec(parameter, root=root, capacity_initial_sleep_sec=0)
    except CmocError as exc:
        error = exc
    else:
        raise AssertionError("run_codex_exec should fail before invoking Codex CLI")

    assert error.summary == "Codex CLI 認証情報が存在しません。"
    assert str(codex_home / "auth.json") in error.detail
    assert "既存の Codex home を指すように CODEX_HOME を設定してください。" in error.next_actions


def test_run_codex_exec_retries_semantic_output(tmp_path: Path, monkeypatch) -> None:
    root = make_repo(tmp_path)
    setup_codex_home(tmp_path, monkeypatch)
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    counter = tmp_path / "counter"
    fake_codex = bin_dir / "codex"
    fake_codex.write_text(
        "\n".join(
            [
                "#!/usr/bin/env python3",
                "import json, pathlib, sys",
                f"counter = pathlib.Path({str(counter)!r})",
                "count = int(counter.read_text()) if counter.exists() else 0",
                "counter.write_text(str(count + 1))",
                "args = sys.argv[1:]",
                "output = pathlib.Path(args[args.index('--output-last-message') + 1])",
                "payload = {'ok': True} if count else {'bad': True}",
                "output.write_text(json.dumps(payload))",
                "print(json.dumps({'type': 'turn.completed'}))",
            ]
        )
        + "\n"
    )
    fake_codex.chmod(0o755)
    monkeypatch.setenv("PATH", f"{bin_dir}:{Path('/usr/bin')}")
    schema = tmp_path / "schema.json"
    schema.write_text(
        json.dumps(
            {
                "type": "object",
                "additionalProperties": False,
                "required": ["ok"],
                "properties": {"ok": {"type": "boolean"}},
            }
        )
    )
    parameter = AgentCallParameter(
        ModelClass.EFFICIENCY,
        ReasoningEffort.LOW,
        FileAccessMode.READONLY,
        "prompt",
        schema,
    )

    result = run_codex_exec(parameter, root=root, capacity_initial_sleep_sec=0)

    assert result.output_json == {"ok": True}
    assert counter.read_text() == "2"


def test_run_codex_exec_polls_and_resumes_after_quota(
    tmp_path: Path, monkeypatch
) -> None:
    root = make_repo(tmp_path)
    codex_home = setup_codex_home(tmp_path, monkeypatch)
    monkeypatch.setattr(cmoc_runtime.time, "sleep", lambda _seconds: None)
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    calls = tmp_path / "calls.jsonl"
    fake_codex = bin_dir / "codex"
    fake_codex.write_text(
        "\n".join(
            [
                "#!/usr/bin/env python3",
                "import json, os, pathlib, sys",
                f"calls = pathlib.Path({str(calls)!r})",
                "args = sys.argv[1:]",
                "with calls.open('a') as f: f.write(json.dumps({'args': args, 'codex_home': os.environ.get('CODEX_HOME')}) + '\\n')",
                "if 'resume' in args:",
                "    output = pathlib.Path(args[args.index('--output-last-message') + 1])",
                "    output.write_text(json.dumps({'ok': True}))",
                "    print(json.dumps({'type': 'turn.completed'}))",
                "    sys.exit(0)",
                "if args == ['exec', '--json', '-']:",
                "    print(json.dumps({'type': 'turn.completed'}))",
                "    sys.exit(0)",
                "print(json.dumps({'type':'error','message':'Quota exceeded','session_id':'sess-1'}))",
                "sys.exit(1)",
            ]
        )
        + "\n"
    )
    fake_codex.chmod(0o755)
    monkeypatch.setenv("PATH", f"{bin_dir}:{Path('/usr/bin')}")
    parameter = AgentCallParameter(
        ModelClass.EFFICIENCY,
        ReasoningEffort.LOW,
        FileAccessMode.READONLY,
        "prompt",
        None,
    )

    result = run_codex_exec(
        parameter,
        root=root,
        quota_poll_interval_sec=0,
        max_quota_polls=1,
    )

    call_records = [json.loads(line) for line in calls.read_text().splitlines()]
    argv_calls = [record["args"] for record in call_records]
    assert argv_calls[0][-1] == "-"
    assert all(record["codex_home"] == str(codex_home) for record in call_records)
    assert argv_calls[1] == ["exec", "--json", "-"]
    assert "resume" in argv_calls[2]
    assert "sess-1" in argv_calls[2]
    assert result.output_json == {"ok": True}


def test_run_codex_exec_uses_single_representative_quota_probe(
    tmp_path: Path, monkeypatch
) -> None:
    root = make_repo(tmp_path)
    setup_codex_home(tmp_path, monkeypatch)
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    calls = tmp_path / "parallel_calls.jsonl"
    fake_codex = bin_dir / "codex"
    fake_codex.write_text(
        "\n".join(
            [
                "#!/usr/bin/env python3",
                "import json, pathlib, sys, time",
                f"calls = pathlib.Path({str(calls)!r})",
                "args = sys.argv[1:]",
                "kind = 'resume' if 'resume' in args else 'probe' if args == ['exec', '--json', '-'] else 'initial'",
                "with calls.open('a') as f: f.write(json.dumps({'kind': kind, 'args': args}) + '\\n')",
                "if kind == 'resume':",
                "    output = pathlib.Path(args[args.index('--output-last-message') + 1])",
                "    output.write_text(json.dumps({'ok': True}))",
                "    print(json.dumps({'type': 'turn.completed'}))",
                "    sys.exit(0)",
                "if kind == 'probe':",
                "    print(json.dumps({'type': 'turn.completed'}))",
                "    sys.exit(0)",
                "deadline = time.time() + 5",
                "while time.time() < deadline:",
                "    lines = calls.read_text().splitlines() if calls.exists() else []",
                "    if sum(1 for line in lines if json.loads(line)['kind'] == 'initial') >= 2:",
                "        break",
                "    time.sleep(0.01)",
                "print(json.dumps({'type':'error','message':'Quota exceeded','session_id':'sess-parallel'}))",
                "sys.exit(1)",
            ]
        )
        + "\n"
    )
    fake_codex.chmod(0o755)
    monkeypatch.setenv("PATH", f"{bin_dir}:{Path('/usr/bin')}")
    parameter = AgentCallParameter(
        ModelClass.EFFICIENCY,
        ReasoningEffort.LOW,
        FileAccessMode.READONLY,
        "prompt",
        None,
    )

    def call_codex():
        return run_codex_exec(
            parameter,
            root=root,
            quota_poll_interval_sec=0.05,
            max_quota_polls=1,
        )

    with ThreadPoolExecutor(max_workers=2) as executor:
        results = list(executor.map(lambda _index: call_codex(), range(2)))

    events = [json.loads(line) for line in calls.read_text().splitlines()]
    assert [event["kind"] for event in events].count("initial") == 2
    assert [event["kind"] for event in events].count("probe") == 1
    assert [event["kind"] for event in events].count("resume") == 2
    assert [result.output_json for result in results] == [{"ok": True}, {"ok": True}]
