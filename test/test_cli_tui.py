"""TUI 起動直前の CLI 前処理の外部挙動を検証する。"""

import json
import subprocess
from pathlib import Path

import commons.runtime_codex_preflight as codex_preflight_module
from basic.acp import AgentCallParameter, FileAccessMode, ModelClass, ReasoningEffort
import pytest

from _support import (
    make_repo,
    run_git,
    runner,
    run_init,
    setup_codex_home,
    stub_codex_profile,
    write_python_executable,
)
from main import app
import sub_commands.tui as tui_module

def test_tui_runs_editor_resolves_parameters_and_launches_codex(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert run_init(root).exit_code == 0
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    fake_code = bin_dir / "code"
    write_python_executable(
        fake_code,
        [
            "import pathlib, sys",
            "path = pathlib.Path(sys.argv[-1])",
            "text = path.read_text()",
            "path.write_text(text + '\\n<!-- remove me -->\\n# 依頼\\n\\nsrc を確認して必要なら直す\\n')",
        ],
    )
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

    def fake_run_codex_exec(
        parameter: AgentCallParameter, **kwargs: object
    ) -> FakeResolveResult:
        exec_calls.append((parameter, kwargs))
        assert kwargs["purpose"] == "tui resolve parameter"
        assert parameter.model_class == ModelClass.MAINSTREAM
        assert parameter.reasoning_effort == ReasoningEffort.MEDIUM
        assert parameter.file_access_mode == FileAccessMode.READONLY
        assert parameter.structured_output_schema_path.name == "resolve_parameter.json"
        assert "remove me" not in parameter.prompt
        assert "src を確認して必要なら直す" in parameter.prompt
        return FakeResolveResult()

    def fake_run_codex_tui(parameter: AgentCallParameter, **kwargs: object) -> None:
        tui_calls.append((parameter, kwargs))
        assert kwargs["purpose"] == "tui codex"
        assert parameter.model_class == ModelClass.MAINSTREAM
        assert parameter.reasoning_effort == ReasoningEffort.MEDIUM
        assert parameter.file_access_mode == FileAccessMode.REPO_WRITE
        assert parameter.structured_output_schema_path is not None
        assert parameter.structured_output_schema_path.name == "launch_tui.json"
        assert parameter.prompt.endswith("_cmpl.md を読んで、その指示に従って下さい")
        assert len(kwargs["extra_read_paths"]) == 1
        assert str(kwargs["extra_read_paths"][0]) in parameter.prompt

    monkeypatch.setattr(tui_module, "run_codex_exec", fake_run_codex_exec)
    monkeypatch.setattr(tui_module, "run_codex_tui", fake_run_codex_tui)

    result = runner.invoke(app, ["tui"], catch_exceptions=False)

    assert result.exit_code == 0
    assert len(exec_calls) == 1
    assert len(tui_calls) == 1
    orig_files = list((root / ".cmoc" / "local" / "log" / "tui").glob("*_orig.md"))
    assert len(orig_files) == 1
    assert "TODO ここから書き始める" in orig_files[0].read_text()
    complete_files = list((root / ".cmoc" / "local" / "log" / "tui").glob("*_cmpl.md"))
    assert len(complete_files) == 1
    complete_prompt = complete_files[0].read_text()
    assert "# file read write rule - repo_write" in complete_prompt
    assert "# オリジナルプロンプト" in complete_prompt
    assert "src を確認して必要なら直す" in complete_prompt
    assert "remove me" not in complete_prompt
    assert str(complete_files[0]) in tui_calls[0][0].prompt
    assert "/.cmoc/local/" in (root / ".gitignore").read_text()
    assert (root / ".cmoc" / "local" / "log" / "sub_command").is_dir()
    assert not (root / ".cmoc" / "logs" / "sub_commands").exists()


def test_tui_uses_default_file_access_mode_for_empty_resolved_value(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    (root / ".cmoc" / "local" / "log" / "tui").mkdir(parents=True, exist_ok=True)
    parameter = tui_module.build_tui_codex_parameter(
        "確認して下さい。",
        {"file_access_mode": {"value": "", "reason": "default accepted"}},
    )

    assert parameter.file_access_mode == FileAccessMode.READONLY
    assert parameter.structured_output_schema_path is not None
    assert parameter.structured_output_schema_path.name == "launch_tui.json"


def test_tui_saves_complete_prompt_in_linked_worktree(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    root = make_repo(tmp_path)
    setup_codex_home(tmp_path, monkeypatch)
    stub_codex_profile(tmp_path, monkeypatch)
    monkeypatch.chdir(root)
    assert run_init(root).exit_code == 0
    linked = root / ".cmoc" / "local" / "worktree" / "linked"
    run_git(root, "worktree", "add", "-b", "linked-test", str(linked), "HEAD")
    monkeypatch.chdir(linked)
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    recorder = tmp_path / "codex_record.json"
    fake_code = bin_dir / "code"
    write_python_executable(
        fake_code,
        [
            "import pathlib, sys",
            "path = pathlib.Path(sys.argv[-1])",
            "path.write_text(path.read_text() + '\\nlinked worktree task\\n')",
        ],
    )
    fake_codex = bin_dir / "codex"
    write_python_executable(
        fake_codex,
        [
            "import json, os, pathlib, sys",
            f"record = pathlib.Path({str(recorder)!r})",
            "args = sys.argv[1:]",
            "output = pathlib.Path(args[args.index('--output-last-message') + 1])",
            "data = {key: {'value': False, 'reason': 'test'} for key in [",
            "    'oracle_and_realization_basic',",
            "    'oracle_standard',",
            "    'realization_standard',",
            "    'review_oracle_standard',",
            "    'apply_review_standard',",
            "    'index_entry_standard',",
            "]}",
            "data['file_access_mode'] = {'value': 'repo_write', 'reason': 'test'}",
            "data['role'] = {'value': 'role', 'reason': 'test'}",
            "data['summary'] = {'value': 'summary', 'reason': 'test'}",
            "data['goal'] = {'value': 'goal', 'reason': 'test'}",
            "output.write_text(json.dumps(data))",
            "record.write_text(json.dumps({'args': args, 'cwd': os.getcwd()}))",
            "print(json.dumps({'type': 'turn.completed'}))",
        ],
    )
    monkeypatch.setenv("PATH", f"{bin_dir}:{Path('/usr/bin')}")
    tui_calls = []

    def fake_run_codex_tui(parameter: AgentCallParameter, **kwargs: object) -> None:
        tui_calls.append((parameter, kwargs))

    monkeypatch.setattr(tui_module, "enable_indexing_preflight", lambda: None)
    codex_preflight_module.disable_indexing_preflight()
    monkeypatch.setattr(tui_module, "run_codex_tui", fake_run_codex_tui)

    result = runner.invoke(app, ["tui"], catch_exceptions=False)

    assert result.exit_code == 0
    assert len(tui_calls) == 1
    assert tui_calls[0][1]["root"] == root.resolve()
    assert tui_calls[0][1]["cwd"] == linked.resolve()
    assert len(list((root / ".cmoc" / "local" / "log" / "tui").glob("*_orig.md"))) == 1
    complete_files = list((root / ".cmoc" / "local" / "log" / "tui").glob("*_cmpl.md"))
    assert not list((linked / ".cmoc" / "local" / "log" / "tui").glob("*_cmpl.md"))
    assert len(complete_files) == 1
    assert str(complete_files[0]) in tui_calls[0][0].prompt
    assert tui_calls[0][1]["extra_read_paths"] == [complete_files[0]]
    recorded = json.loads(recorder.read_text())
    schema_arg = recorded["args"][recorded["args"].index("--output-schema") + 1]
    assert recorded["cwd"] == str(linked)
    assert Path(schema_arg).parent == root / ".cmoc" / "local" / "schema"
    assert not (linked / ".cmoc" / "local" / "schema").exists()


def test_tui_ignores_repo_and_work_cmoc_before_linked_worktree_logs(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    root = make_repo(tmp_path)
    config_path = root / ".cmoc" / "config.json"
    config_path.parent.mkdir()
    config_path.write_text("{}\n")
    linked = root / ".cmoc" / "local" / "worktree" / "linked"
    run_git(root, "worktree", "add", "-b", "linked-tui-ignore", str(linked), "HEAD")
    monkeypatch.chdir(linked)
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    fake_code = bin_dir / "code"
    write_python_executable(
        fake_code,
        [
            "import pathlib, sys",
            "path = pathlib.Path(sys.argv[-1])",
            "path.write_text(path.read_text() + '\\nlinked ignore task\\n')",
        ],
    )
    monkeypatch.setenv("PATH", f"{bin_dir}:{Path('/usr/bin')}")

    class FakeResolveResult:
        output_json = {"file_access_mode": {"value": "readonly", "reason": "test"}}

    monkeypatch.setattr(tui_module, "enable_indexing_preflight", lambda: None)
    monkeypatch.setattr(tui_module, "run_codex_exec", lambda *_, **__: FakeResolveResult())
    monkeypatch.setattr(tui_module, "run_codex_tui", lambda *_, **__: None)

    result = runner.invoke(app, ["tui"], catch_exceptions=False)

    assert result.exit_code == 0
    assert "/.cmoc/local/" in (root / ".gitignore").read_text()
    assert "/.cmoc/local/" in (linked / ".gitignore").read_text()
    assert len(list((root / ".cmoc" / "local" / "log" / "sub_command").glob("*.jsonl"))) == 1
    assert len(list((root / ".cmoc" / "local" / "log" / "tui").glob("*_orig.md"))) == 1
    assert len(list((root / ".cmoc" / "local" / "log" / "tui").glob("*_cmpl.md"))) == 1
    assert not list((linked / ".cmoc" / "local" / "log" / "tui").glob("*_cmpl.md"))
    assert run_git(root, "status", "--short", "--", ".cmoc/local").stdout.strip() == ""
    assert run_git(linked, "status", "--short", "--", ".cmoc").stdout.strip() == ""
