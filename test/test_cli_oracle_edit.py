"""`cmoc oracle edit` のエディタ入力と TUI 起動境界を検証する。

根拠:
- {{work-root}}/oracle/doc/app_spec/prompt_editor_input.md
- {{work-root}}/oracle/doc/app_spec/sub_command/oracle_edit.md
"""

from collections.abc import Iterator
from pathlib import Path

import pytest
from _cli_support import runner
from _command_support import write_python_executable
from _git_support import make_repo, run_git
from _ollama_support import run_doctor

import commons.runtime_codex_preflight as codex_preflight_module
import sub_commands.oracle.edit as oracle_edit_module
from basic.acp import AgentCallParameter, FileAccessMode, ModelClass, ReasoningEffort
from main import app


@pytest.fixture(autouse=True)
def reset_indexing_preflight() -> Iterator[None]:
    """各テスト間で indexing preflight の登録状態を分離する。"""
    codex_preflight_module.disable_indexing_preflight()
    yield
    codex_preflight_module.disable_indexing_preflight()


def _install_editor(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """初期値を保持したままテスト用指示を追記する code executable を置く。"""
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    write_python_executable(
        bin_dir / "code",
        [
            "import pathlib, sys",
            "assert sys.argv[1:-1] == ['--wait']",
            "path = pathlib.Path(sys.argv[-1])",
            "path.write_text(path.read_text() + '\\n<!-- editor-only-comment -->\\n# 依頼\\n\\noracle/spec.md を明瞭にする\\n')",
        ],
    )
    monkeypatch.setenv("PATH", f"{bin_dir}:{Path('/usr/bin')}")


def test_oracle_edit_uses_shared_editor_input_and_fixed_tui_parameter(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """共通テンプレートを編集し、正本の固定 parameter を TUI へ渡す。"""
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    run_doctor(root)
    _install_editor(tmp_path, monkeypatch)
    tui_calls: list[tuple[AgentCallParameter, dict[str, object]]] = []

    def fake_run_codex_tui(
        parameter: AgentCallParameter,
        **kwargs: object,
    ) -> None:
        """TUI 起動 parameter と runtime context を記録する。"""
        tui_calls.append((parameter, kwargs))

    monkeypatch.setattr(oracle_edit_module, "enable_indexing_preflight", lambda: None)
    monkeypatch.setattr(oracle_edit_module, "run_codex_tui", fake_run_codex_tui)

    result = runner.invoke(app, ["oracle", "edit"], catch_exceptions=False)

    assert result.exit_code == 0
    assert len(tui_calls) == 1
    parameter, kwargs = tui_calls[0]
    assert parameter.model_class == ModelClass.FLAGSHIP
    assert parameter.reasoning_effort == ReasoningEffort.MAX
    assert parameter.file_access_mode == FileAccessMode.PURE_ORACLE_WRITE
    assert parameter.structured_output_schema_path is None
    assert parameter.run_indexing_preflight is True
    assert kwargs["root"] == root.resolve()
    assert kwargs["cwd"] == root.resolve()
    assert kwargs["purpose"] == "oracle edit codex"

    editor_dir = root / ".cmoc" / "gu" / "ar" / "log" / "editor_input"
    original_files = list(editor_dir.glob("*_orig.md"))
    complete_files = list(editor_dir.glob("*_cmpl.md"))
    assert len(original_files) == 1
    assert len(complete_files) == 1
    original = original_files[0].read_text()
    assert "cmoc oracle edit` で自動注入" in original
    assert "# ゴール" in original
    assert "# 制約境界" in original
    assert "AI Agent が知りえない概念" in original
    complete = complete_files[0].read_text()
    assert "oracle/spec.md を明瞭にする" in complete
    assert "editor-only-comment" not in complete
    assert "# file read write rule - pure_oracle_write" in complete
    assert "# oracle standard" in complete
    assert str(complete_files[0]) in parameter.prompt


def test_oracle_edit_leaves_tui_oracle_changes_uncommitted(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """TUI が変更した oracle file を command 終了時に自動 commit しない。"""
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    run_doctor(root)
    _install_editor(tmp_path, monkeypatch)
    head_before = run_git(root, "rev-parse", "HEAD").stdout.strip()

    def fake_run_codex_tui(
        parameter: AgentCallParameter,
        **kwargs: object,
    ) -> None:
        """Codex TUI による oracle 編集だけを再現する。"""
        assert parameter.file_access_mode == FileAccessMode.PURE_ORACLE_WRITE
        (root / "oracle" / "spec.md").write_text("# edited by TUI\n")

    monkeypatch.setattr(oracle_edit_module, "enable_indexing_preflight", lambda: None)
    monkeypatch.setattr(oracle_edit_module, "run_codex_tui", fake_run_codex_tui)

    result = runner.invoke(app, ["oracle", "edit"], catch_exceptions=False)

    assert result.exit_code == 0
    assert run_git(root, "rev-parse", "HEAD").stdout.strip() == head_before
    assert run_git(root, "status", "--short", "--", "oracle/spec.md").stdout == (
        " M oracle/spec.md\n"
    )
