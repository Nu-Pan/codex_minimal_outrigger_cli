"""TUI 起動直前の CLI 前処理の外部挙動を検証する。

正本仕様:
- {{work-root}}/oracle/doc/app_spec/sub_command/tui.md
- {{work-root}}/oracle/doc/app_spec/prompt_editor_input.md
- {{work-root}}/oracle/src/oracle/prompt_builder/editor_input.py
"""

from collections.abc import Iterator
from pathlib import Path

import pytest
from _cli_support import run_doctor, runner
from _command_support import write_python_executable
from _git_support import make_repo, run_git

import commons.prompt_editor_input as prompt_editor_input_module
import commons.runtime_cli as runtime_cli_module
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
    builder_calls: list[tuple[str, str, AgentCallParameter, str]] = []
    tui_calls: list[tuple[AgentCallParameter, dict[str, object]]] = []

    real_build_parameter = tui_module.build_tui_launch_tui_parameter

    def record_build_parameter(
        time_stamp: str,
        original_prompt: str,
    ) -> AgentCallParameter:
        """builder の引数、戻り値、および編集前の skeleton を記録する。"""
        events.append("build")
        parameter = real_build_parameter(time_stamp, original_prompt)
        prompt_suffix = " を読んで、その指示に従って下さい"
        complete_path = Path(parameter.prompt.removesuffix(prompt_suffix))
        builder_calls.append(
            (
                time_stamp,
                original_prompt,
                parameter,
                complete_path.read_text(encoding="utf-8"),
            )
        )
        return parameter

    def fake_run_codex_tui(parameter: AgentCallParameter, **kwargs: object) -> None:
        """TUI 起動 call を記録して生成パラメータを検証する。"""
        events.append("tui")
        tui_calls.append((parameter, kwargs))
        assert kwargs["purpose"] == "tui codex"
        assert kwargs["notification_command_name"] == "tui"
        assert parameter.model_class == ModelClass.FLAGSHIP
        assert parameter.reasoning_effort == ReasoningEffort.MAX
        assert parameter.file_access_mode == FileAccessMode.REPO_WRITE
        assert parameter.structured_output_schema_path is None
        assert parameter.prompt.endswith("_cmpl.md を読んで、その指示に従って下さい")
        assert parameter is builder_calls[0][2]

    monkeypatch.setattr(
        tui_module,
        "enable_indexing_preflight",
        lambda: events.append("enable"),
    )
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

    assert result.exit_code == 0
    assert events == ["enable", "doctor", "build", "tui"]
    assert len(builder_calls) == 1
    assert builder_calls[0][1] == prompt_editor_input_module.ORIGINAL_PROMPT_PLACEHOLDER
    assert (
        builder_calls[0][3].count(
            prompt_editor_input_module.ORIGINAL_PROMPT_PLACEHOLDER
        )
        == 1
    )
    assert len(tui_calls) == 1
    orig_files = list(
        (root / ".cmoc" / "gu" / "ar" / "log" / "editor_input").glob("*_orig.md")
    )
    assert len(orig_files) == 1
    editor_contents = orig_files[0].read_text()
    assert editor_contents.startswith("<!--\n# このファイルの使い方")
    assert '<cmoc_block id="prompt template">' in editor_contents
    assert "# file read write rule - repo_write" in editor_contents
    assert prompt_editor_input_module.ORIGINAL_PROMPT_PLACEHOLDER in editor_contents
    assert "remove me" in editor_contents
    assert not list((root / ".cmoc" / "gu" / "aw" / "editor_input").glob("*_orig.md"))
    complete_files = list(
        (root / ".cmoc" / "gu" / "ar" / "log" / "editor_input").glob("*_cmpl.md")
    )
    assert len(complete_files) == 1
    complete_prompt = complete_files[0].read_text()
    assert "# file read write rule - repo_write" in complete_prompt
    assert "# oracle and realization basic" in complete_prompt
    assert "# oracle standard" in complete_prompt
    assert "# realization standard" in complete_prompt
    assert "# oracle review standard" in complete_prompt
    assert "# apply review standard" in complete_prompt
    assert "# realization oracle reference rule" in complete_prompt
    assert "# index entry standard" not in complete_prompt
    assert '<cmoc_ref target="original_prompt"/>' in complete_prompt
    assert "# オリジナルプロンプト" in complete_prompt
    assert "src を確認して必要なら直す" in complete_prompt
    assert "remove me" not in complete_prompt
    assert prompt_editor_input_module.ORIGINAL_PROMPT_PLACEHOLDER not in complete_prompt
    assert complete_prompt == builder_calls[0][3].replace(
        prompt_editor_input_module.ORIGINAL_PROMPT_PLACEHOLDER,
        "# 依頼\n\nsrc を確認して必要なら直す",
        1,
    )
    assert str(complete_files[0]) in tui_calls[0][0].prompt
    assert readme_path.read_text() == "# unstaged change\n"
    assert (
        run_git(root, "diff", "--cached", "--", "README.md").stdout
        == staged_diff_before
    )
    assert run_git(root, "diff", "--", "README.md").stdout == unstaged_diff_before
    assert "/.cmoc/gu/" in (root / ".gitignore").read_text()
    assert (root / ".cmoc" / "gu" / "ar" / "log" / "sub_command").is_dir()
    assert not (root / ".cmoc" / "logs" / "sub_commands").exists()


def test_tui_saves_complete_prompt_in_linked_worktree(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """linked worktree 起動でも prompt と agent call context は main 側に置く。"""
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

    monkeypatch.setattr(tui_module, "enable_indexing_preflight", lambda: None)
    monkeypatch.setattr(tui_module, "run_codex_tui", fake_run_codex_tui)

    result = runner.invoke(app, ["tui"], catch_exceptions=False)

    assert result.exit_code == 0
    assert len(tui_calls) == 1
    parameter, tui_kwargs = tui_calls[0]
    assert tui_kwargs["root"] == root.resolve()
    assert tui_kwargs["notification_command_name"] == "tui"
    assert parameter.agent_call_cwd == root.resolve()
    assert (
        len(
            list(
                (root / ".cmoc" / "gu" / "ar" / "log" / "editor_input").glob(
                    "*_orig.md"
                )
            )
        )
        == 1
    )
    complete_files = list(
        (root / ".cmoc" / "gu" / "ar" / "log" / "editor_input").glob("*_cmpl.md")
    )
    assert not list(
        (linked / ".cmoc" / "gu" / "ar" / "log" / "editor_input").glob("*_cmpl.md")
    )
    assert len(complete_files) == 1
    complete_prompt = complete_files[0].read_text(encoding="utf-8")
    assert "linked worktree task" in complete_prompt
    assert prompt_editor_input_module.ORIGINAL_PROMPT_PLACEHOLDER not in complete_prompt
    assert str(complete_files[0]) in parameter.prompt
    assert not list((root / ".cmoc" / "gu" / "aw" / "editor_input").glob("*_orig.md"))
    assert not list((linked / ".cmoc" / "gu" / "aw" / "editor_input").glob("*_orig.md"))


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

    monkeypatch.setattr(tui_module, "enable_indexing_preflight", lambda: None)
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
        len(
            list(
                (root / ".cmoc" / "gu" / "ar" / "log" / "editor_input").glob(
                    "*_orig.md"
                )
            )
        )
        == 1
    )
    assert (
        len(
            list(
                (root / ".cmoc" / "gu" / "ar" / "log" / "editor_input").glob(
                    "*_cmpl.md"
                )
            )
        )
        == 1
    )
    assert not list(
        (linked / ".cmoc" / "gu" / "ar" / "log" / "editor_input").glob("*_cmpl.md")
    )
    assert not list((root / ".cmoc" / "gu" / "aw" / "editor_input").glob("*_orig.md"))
    assert run_git(root, "status", "--short", "--", ".cmoc/gu").stdout.strip() == ""
    assert run_git(linked, "status", "--short", "--", ".cmoc").stdout.strip() == ""
