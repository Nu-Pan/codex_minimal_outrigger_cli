"""TUI 起動直前の CLI 前処理の外部挙動を検証する。

正本仕様:
- {{work-root}}/oracle/doc/app_spec/sub_command/tui.md
- {{work-root}}/oracle/doc/app_spec/prompt_editor_input.md
- {{work-root}}/oracle/src/oracle/prompt_builder/editor_input.py
"""

from pathlib import Path

import pytest
from _cli_support import run_doctor, runner
from _command_support import write_python_executable
from _git_support import make_repo, run_git

import commons.prompt_editor_input as prompt_editor_input_module
import commons.runtime_cli as runtime_cli_module
import sub_commands.oracle.edit as oracle_edit_module
import sub_commands.oracle.investigation as investigation_module
import sub_commands.tui as tui_module
from basic.acp import AgentCallParameter, DocumentSearchScope, FileAccessMode
from main import app


@pytest.mark.parametrize(
    "command", [["tui"], ["oracle", "investigation"], ["oracle", "edit"]]
)
def test_editor_save_failure_preserves_input_and_prevents_agent_calls(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    command: list[str],
) -> None:
    """共通の確定保存に失敗した場合、各 CLI は本文を残して agent 起動前に止まる。"""
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert run_doctor(root).exit_code == 0
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    write_python_executable(
        bin_dir / "code",
        [
            "import pathlib, sys",
            "pathlib.Path(sys.argv[-1]).write_bytes(b'recoverable input\\r\\n')",
        ],
    )
    monkeypatch.setenv("PATH", f"{bin_dir}:/usr/bin")
    real_replace = prompt_editor_input_module.os.replace

    def fail_input_save(source, destination):
        if Path(destination).parent == root / ".cmoc/gu/log/editor_input":
            raise OSError("input save failed")
        return real_replace(source, destination)

    def unexpected_agent_call(*_args, **_kwargs):
        pytest.fail("input save failure must prevent agent calls")

    monkeypatch.setattr(prompt_editor_input_module.os, "replace", fail_input_save)
    monkeypatch.setattr(tui_module, "run_codex_tui", unexpected_agent_call)
    monkeypatch.setattr(investigation_module, "run_codex_tui", unexpected_agent_call)
    monkeypatch.setattr(oracle_edit_module, "run_codex_exec", unexpected_agent_call)

    result = runner.invoke(app, command, catch_exceptions=False)

    assert result.exit_code == 1
    files = list((root / ".cmoc/gu/log/editor_input").iterdir())
    assert len(files) == 1
    assert files[0].name.endswith("_orig.md")
    assert files[0].read_bytes() == b"recoverable input\r\n"


def test_tui_runs_editor_and_launches_codex_directly(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """既存差分を保ち、編集済み prompt から Codex TUI を直接起動する。"""
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert run_doctor(root).exit_code == 0
    readme_path = root / "README.md"
    readme_path.write_text("# staged change\n")
    run_git(root, "add", "README.md")
    readme_path.write_text("# unstaged change\n")
    staged_diff_before = run_git(root, "diff", "--cached", "--", "README.md").stdout
    unstaged_diff_before = run_git(root, "diff", "--", "README.md").stdout
    events: list[str] = []

    real_run_doctor_preprocess = runtime_cli_module.run_doctor_preprocess

    def record_run_doctor_preprocess(
        target_root: Path,
        *,
        sync_refactor_entries: bool = True,
    ) -> None:
        """TUI invocation 内の doctor preprocess を記録して本来の処理へ委譲する。"""
        events.append("doctor")
        real_run_doctor_preprocess(
            target_root,
            sync_refactor_entries=sync_refactor_entries,
        )

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
    builder_calls: list[tuple[str, AgentCallParameter]] = []
    tui_calls: list[tuple[AgentCallParameter, dict[str, object]]] = []

    real_build_parameter = tui_module.build_tui_launch_tui_parameter

    def record_build_parameter(
        original_prompt: str,
        *,
        document_search_scope: DocumentSearchScope,
    ) -> AgentCallParameter:
        """skeleton 用と実行用の builder 呼び出しを記録する。"""
        kind = (
            "build-skeleton"
            if original_prompt == prompt_editor_input_module.ORIGINAL_PROMPT_PLACEHOLDER
            else "build-parameter"
        )
        events.append(kind)
        parameter = real_build_parameter(
            original_prompt, document_search_scope=document_search_scope
        )
        builder_calls.append((original_prompt, parameter))
        return parameter

    def fake_run_codex_tui(parameter: AgentCallParameter, **kwargs: object) -> None:
        """TUI 起動 call を記録して生成パラメータを検証する。"""
        events.append("tui")
        tui_calls.append((parameter, kwargs))
        assert kwargs["purpose"] == "tui codex"
        assert kwargs["notification_command_name"] == "tui"
        assert parameter.file_access_mode == FileAccessMode.REPO_WRITE
        assert parameter.structured_output_schema_path is None
        assert parameter is builder_calls[1][1]

    monkeypatch.setattr(
        runtime_cli_module,
        "run_doctor_preprocess",
        record_run_doctor_preprocess,
    )
    monkeypatch.setattr(
        tui_module,
        "build_tui_launch_tui_parameter",
        record_build_parameter,
    )
    monkeypatch.setattr(tui_module, "run_codex_tui", fake_run_codex_tui)

    result = runner.invoke(app, ["tui"], catch_exceptions=False)

    assert result.exit_code == 0, result.output
    assert events == [
        "doctor",
        "build-skeleton",
        "build-parameter",
        "tui",
    ]
    assert len(builder_calls) == 2
    assert builder_calls[0][0] == prompt_editor_input_module.ORIGINAL_PROMPT_PLACEHOLDER
    assert len(tui_calls) == 1
    orig_files = list(
        (root / ".cmoc" / "gu" / "log" / "editor_input").glob("*_orig.md")
    )
    assert len(orig_files) == 1
    editor_contents = orig_files[0].read_text()
    assert (
        editor_contents
        == "\n<!-- remove me -->\n# 依頼\n\nsrc を確認して必要なら直す\n"
    )
    assert not list((root / ".cmoc" / "gu" / "editor_input").glob("*_orig.md"))
    assert not list((root / ".cmoc" / "gu" / "log" / "editor_input").glob("*_cmpl.md"))
    complete_prompt = tui_calls[0][0].prompt
    assert "# file access policy (repo_write)" in complete_prompt
    for heading in (
        "# oracle and realization basic",
        "# oracle policy",
        "# realization policy",
        "# realization findings policy",
        "# routing policy",
    ):
        assert heading in complete_prompt
    for heading in (
        "# oracle findings policy",
        "# realization oracle reference policy",
        "# index entry policy",
    ):
        assert heading not in complete_prompt
    assert '<cmoc_ref target="original_prompt"/>' in complete_prompt
    assert "# オリジナルプロンプト" in complete_prompt
    assert "src を確認して必要なら直す" in complete_prompt
    assert "<!-- remove me -->" in complete_prompt
    assert (
        builder_calls[1][0]
        == "<!-- remove me -->\n# 依頼\n\nsrc を確認して必要なら直す"
    )
    assert readme_path.read_text() == "# unstaged change\n"
    assert (
        run_git(root, "diff", "--cached", "--", "README.md").stdout
        == staged_diff_before
    )
    assert run_git(root, "diff", "--", "README.md").stdout == unstaged_diff_before
    assert "/.cmoc/gu/" in (root / ".gitignore").read_text()
    assert (root / ".cmoc" / "gu" / "log" / "sub_command").is_dir()
    assert not (root / ".cmoc" / "logs" / "sub_commands").exists()


def test_tui_saves_editor_input_in_main_worktree(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """linked worktree 起動でも editor 記録と agent call context は main 側に置く。"""
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert run_doctor(root).exit_code == 0
    linked = root / ".cmoc" / "gu" / "worktree" / "linked"
    run_git(root, "worktree", "add", "-b", "linked-test", str(linked), "HEAD")
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
            "path.write_text(path.read_text() + '\\nlinked worktree task\\n')",
        ],
    )
    monkeypatch.setenv("PATH", f"{bin_dir}:{Path('/usr/bin')}")
    tui_calls: list[tuple[AgentCallParameter, dict[str, object]]] = []

    def fake_run_codex_tui(parameter: AgentCallParameter, **kwargs: object) -> None:
        """linked worktree の TUI 起動 call を記録する。"""
        tui_calls.append((parameter, kwargs))

    monkeypatch.setattr(tui_module, "run_codex_tui", fake_run_codex_tui)

    result = runner.invoke(app, ["tui"], catch_exceptions=False)

    assert result.exit_code == 0, result.output
    assert len(tui_calls) == 1
    parameter, tui_kwargs = tui_calls[0]
    assert tui_kwargs["root"] == root.resolve()
    assert tui_kwargs["notification_command_name"] == "tui"
    assert parameter.agent_call_cwd == root.resolve()
    assert (
        len(list((root / ".cmoc" / "gu" / "log" / "editor_input").glob("*_orig.md")))
        == 1
    )
    assert not list(
        (linked / ".cmoc" / "gu" / "log" / "editor_input").glob("*_cmpl.md")
    )
    assert not list((root / ".cmoc" / "gu" / "log" / "editor_input").glob("*_cmpl.md"))
    complete_prompt = parameter.prompt
    assert "linked worktree task" in complete_prompt
    assert not list((root / ".cmoc" / "gu" / "editor_input").glob("*_orig.md"))
    assert not list((linked / ".cmoc" / "gu" / "editor_input").glob("*_orig.md"))


def test_tui_ignores_repo_and_work_cmoc_before_linked_worktree_logs(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """repository と linked worktree の両方で `.cmoc` ignore を保証する。"""
    root = make_repo(tmp_path)
    linked = root / ".cmoc" / "gu" / "worktree" / "linked"
    run_git(root, "worktree", "add", "-b", "linked-tui-ignore", str(linked), "HEAD")
    monkeypatch.chdir(linked)
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    fake_code = bin_dir / "code"
    write_python_executable(
        fake_code,
        [
            "import sys",
            "assert sys.argv[1:-1] == ['--wait']",
        ],
    )
    monkeypatch.setenv("PATH", f"{bin_dir}:{Path('/usr/bin')}")

    monkeypatch.setattr(tui_module, "run_codex_tui", lambda *_, **__: None)

    result = runner.invoke(app, ["tui"], catch_exceptions=False)

    assert result.exit_code == 0, result.output
    assert "/.cmoc/gu/" in (root / ".gitignore").read_text()
    assert "/.cmoc/gu/" in (linked / ".gitignore").read_text()
    assert (
        len(list((root / ".cmoc" / "gu" / "log" / "sub_command").glob("*.jsonl"))) == 1
    )
    assert (
        len(list((root / ".cmoc" / "gu" / "log" / "editor_input").glob("*_orig.md")))
        == 1
    )
    assert not list((root / ".cmoc" / "gu" / "log" / "editor_input").glob("*_cmpl.md"))
    assert not list(
        (linked / ".cmoc" / "gu" / "log" / "editor_input").glob("*_cmpl.md")
    )
    assert not list((root / ".cmoc" / "gu" / "editor_input").glob("*_orig.md"))
    assert run_git(root, "status", "--short", "--", ".cmoc/gu").stdout.strip() == ""
    assert run_git(linked, "status", "--short", "--", ".cmoc").stdout.strip() == ""
