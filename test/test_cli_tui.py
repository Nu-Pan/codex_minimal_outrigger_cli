"""TUI 起動直前の CLI 前処理の外部挙動を検証する。

正本仕様: {{work-root}}/oracle/doc/app_spec/sub_command/tui.md
"""

import json
from collections.abc import Iterator
from pathlib import Path

import pytest
from _cli_support import runner
from _codex_support import setup_codex_home, stub_codex_overrides
from _command_support import write_python_executable
from _git_support import make_repo, run_git
from _ollama_support import run_doctor

import commons.runtime_codex_preflight as codex_preflight_module
import sub_commands.tui as tui_module
from basic.acp import AgentCallParameter, FileAccessMode, ModelClass, ReasoningEffort
from main import app


@pytest.fixture(autouse=True)
def reset_indexing_preflight() -> Iterator[None]:
    """各テスト間で indexing preflight の有効状態をリセットする。"""
    codex_preflight_module.disable_indexing_preflight()
    yield
    codex_preflight_module.disable_indexing_preflight()


def test_tui_runs_editor_resolves_parameters_and_launches_codex(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """編集済み prompt の解決と Codex TUI 起動までを検証する。"""
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert run_doctor(root).exit_code == 0
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    fake_code = bin_dir / "code"
    write_python_executable(
        fake_code,
        [
            "import pathlib, sys",
            "assert sys.argv[1:-1] == ['--wait']",
            "path = pathlib.Path(sys.argv[-1])",
            "text = path.read_text()",
            "path.write_text(text + '\\n<!-- remove me -->\\n# 依頼\\n\\nsrc を確認して必要なら直す\\n')",
        ],
    )
    monkeypatch.setenv("PATH", f"{bin_dir}:{Path('/usr/bin')}")
    exec_calls: list[tuple[AgentCallParameter, dict[str, object]]] = []
    tui_calls: list[tuple[AgentCallParameter, dict[str, object]]] = []

    class FakeResolveResult:
        """parameter 解決 call が返す最小の fake result。"""

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
        """解決パラメータ取得 call を記録して期待値を検証する。"""
        exec_calls.append((parameter, kwargs))
        assert kwargs["purpose"] == "tui resolve parameter"
        assert parameter.model_class == ModelClass.EFFICIENCY
        assert parameter.reasoning_effort == ReasoningEffort.MAX
        assert parameter.file_access_mode == FileAccessMode.READONLY
        assert parameter.structured_output_schema_path.name == "resolve_parameter.json"
        assert "remove me" not in parameter.prompt
        assert "src を確認して必要なら直す" in parameter.prompt
        return FakeResolveResult()

    def fake_run_codex_tui(parameter: AgentCallParameter, **kwargs: object) -> None:
        """TUI 起動 call を記録して生成パラメータを検証する。"""
        tui_calls.append((parameter, kwargs))
        assert kwargs["purpose"] == "tui codex"
        assert parameter.model_class == ModelClass.FLAGSHIP
        assert parameter.reasoning_effort == ReasoningEffort.MAX
        assert parameter.file_access_mode == FileAccessMode.REPO_WRITE
        assert parameter.structured_output_schema_path is not None
        assert parameter.structured_output_schema_path.name == "launch_tui.json"
        assert parameter.prompt.endswith("_cmpl.md を読んで、その指示に従って下さい")
        assert "extra_read_paths" not in kwargs

    monkeypatch.setattr(tui_module, "run_codex_exec", fake_run_codex_exec)
    monkeypatch.setattr(tui_module, "run_codex_tui", fake_run_codex_tui)

    result = runner.invoke(app, ["tui"], catch_exceptions=False)

    assert result.exit_code == 0
    assert len(exec_calls) == 1
    assert len(tui_calls) == 1
    orig_files = list((root / ".cmoc" / "gu" / "ar" / "log" / "tui").glob("*_orig.md"))
    assert len(orig_files) == 1
    original_prompt = orig_files[0].read_text()
    assert "基本的な考え方は以下の通り" in original_prompt
    assert "手順の過剰固定" in original_prompt
    assert "# 目的" in original_prompt
    assert "# 裁量範囲" in original_prompt
    complete_files = list(
        (root / ".cmoc" / "gu" / "ar" / "log" / "tui").glob("*_cmpl.md")
    )
    assert len(complete_files) == 1
    complete_prompt = complete_files[0].read_text()
    assert "# file read write rule - repo_write" in complete_prompt
    assert "# オリジナルプロンプト" in complete_prompt
    assert "src を確認して必要なら直す" in complete_prompt
    assert "remove me" not in complete_prompt
    assert str(complete_files[0]) in tui_calls[0][0].prompt
    assert "/.cmoc/gu/" in (root / ".gitignore").read_text()
    assert (root / ".cmoc" / "gu" / "ar" / "log" / "sub_command").is_dir()
    assert not (root / ".cmoc" / "logs" / "sub_commands").exists()


def test_tui_uses_default_file_access_mode_for_empty_resolved_value(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """空の解決値が TUI の readonly 既定値へ戻ることを検証する。"""
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    (root / ".cmoc" / "gu" / "ar" / "log" / "tui").mkdir(parents=True, exist_ok=True)
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
    """linked worktree でも complete prompt を repository 側へ保存する。"""
    root = make_repo(tmp_path)
    setup_codex_home(tmp_path, monkeypatch)
    stub_codex_overrides(monkeypatch)
    monkeypatch.chdir(root)
    assert run_doctor(root).exit_code == 0
    linked = root / ".cmoc" / "gu" / "worktree" / "linked"
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
            "assert sys.argv[1:-1] == ['--wait']",
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
    tui_calls: list[tuple[AgentCallParameter, dict[str, object]]] = []

    def fake_run_codex_tui(parameter: AgentCallParameter, **kwargs: object) -> None:
        """linked worktree の TUI 起動 call を記録する。"""
        tui_calls.append((parameter, kwargs))

    monkeypatch.setattr(tui_module, "enable_indexing_preflight", lambda: None)
    monkeypatch.setattr(tui_module, "run_codex_tui", fake_run_codex_tui)

    result = runner.invoke(app, ["tui"], catch_exceptions=False)

    assert result.exit_code == 0
    assert len(tui_calls) == 1
    assert tui_calls[0][1]["root"] == root.resolve()
    assert tui_calls[0][1]["cwd"] == linked.resolve()
    assert (
        len(list((root / ".cmoc" / "gu" / "ar" / "log" / "tui").glob("*_orig.md"))) == 1
    )
    complete_files = list(
        (root / ".cmoc" / "gu" / "ar" / "log" / "tui").glob("*_cmpl.md")
    )
    assert not list((linked / ".cmoc" / "gu" / "ar" / "log" / "tui").glob("*_cmpl.md"))
    assert len(complete_files) == 1
    assert str(complete_files[0]) in tui_calls[0][0].prompt
    assert "extra_read_paths" not in tui_calls[0][1]
    recorded = json.loads(recorder.read_text())
    schema_arg = recorded["args"][recorded["args"].index("--output-schema") + 1]
    assert recorded["cwd"] == str(linked)
    assert Path(schema_arg).parent == root / ".cmoc" / "gu" / "ar" / "schema"
    assert not (linked / ".cmoc" / "gu" / "ar" / "schema").exists()


def test_tui_ignores_repo_and_work_cmoc_before_linked_worktree_logs(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """repository と linked worktree の両方で `.cmoc` ignore を保証する。"""
    root = make_repo(tmp_path)
    config_path = root / ".cmoc" / "gt" / "ar" / "config.json"
    config_path.parent.mkdir(parents=True)
    config_path.write_text("{}\n")
    linked = root / ".cmoc" / "gu" / "worktree" / "linked"
    run_git(root, "worktree", "add", "-b", "linked-tui-ignore", str(linked), "HEAD")
    monkeypatch.chdir(linked)
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    fake_code = bin_dir / "code"
    write_python_executable(
        fake_code,
        [
            "import pathlib, sys",
            "assert sys.argv[1:-1] == ['--wait']",
            "path = pathlib.Path(sys.argv[-1])",
            "path.write_text(path.read_text() + '\\nlinked ignore task\\n')",
        ],
    )
    monkeypatch.setenv("PATH", f"{bin_dir}:{Path('/usr/bin')}")

    class FakeResolveResult:
        """parameter 解決 call が返す最小の fake result。"""

        output_json = {"file_access_mode": {"value": "readonly", "reason": "test"}}

    monkeypatch.setattr(tui_module, "enable_indexing_preflight", lambda: None)
    monkeypatch.setattr(
        tui_module, "run_codex_exec", lambda *_, **__: FakeResolveResult()
    )
    monkeypatch.setattr(tui_module, "run_codex_tui", lambda *_, **__: None)

    result = runner.invoke(app, ["tui"], catch_exceptions=False)

    assert result.exit_code == 0
    assert "/.cmoc/gu/" in (root / ".gitignore").read_text()
    assert "/.cmoc/gu/" in (linked / ".gitignore").read_text()
    assert (
        len(
            list((root / ".cmoc" / "gu" / "ar" / "log" / "sub_command").glob("*.jsonl"))
        )
        == 1
    )
    assert (
        len(list((root / ".cmoc" / "gu" / "ar" / "log" / "tui").glob("*_orig.md"))) == 1
    )
    assert (
        len(list((root / ".cmoc" / "gu" / "ar" / "log" / "tui").glob("*_cmpl.md"))) == 1
    )
    assert not list((linked / ".cmoc" / "gu" / "ar" / "log" / "tui").glob("*_cmpl.md"))
    assert run_git(root, "status", "--short", "--", ".cmoc/gu").stdout.strip() == ""
    assert run_git(linked, "status", "--short", "--", ".cmoc").stdout.strip() == ""
