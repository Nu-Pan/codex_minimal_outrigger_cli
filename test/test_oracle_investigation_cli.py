"""`cmoc oracle investigation` の CLI 起動条件を検証する。

根拠:
- {{work-root}}/oracle/doc/app_spec/sub_command/oracle_investigation.md
- {{work-root}}/oracle/doc/app_spec/prompt_editor_input.md
- {{work-root}}/oracle/src/oracle/acp_builder/oracle/investigation/launch_tui.py
"""

from collections.abc import Iterator
from pathlib import Path

import pytest
from _cli_support import run_doctor, runner
from _git_support import make_repo

import acp.builder.oracle.investigation.launch_tui as launch_tui_module
import commons.runtime_codex_preflight as codex_preflight_module
import sub_commands.oracle.investigation as investigation_module
from basic.acp import AgentCallParameter, FileAccessMode, ModelClass, ReasoningEffort
from main import app


@pytest.fixture(autouse=True)
def reset_indexing_preflight() -> Iterator[None]:
    """各 test の前後で indexing preflight の process-local state を初期化する。"""
    codex_preflight_module.disable_indexing_preflight()
    yield
    codex_preflight_module.disable_indexing_preflight()


def test_oracle_investigation_has_no_session_precondition(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """oracle investigation が session なしの main worktree でも起動できる。"""
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert run_doctor(root).exit_code == 0
    time_stamp = "2026-08-03_00-00-00_000000000"
    editor_path = (
        root / ".cmoc" / "gu" / "ar" / "log" / "editor_input" / f"{time_stamp}_orig.md"
    )
    editor_calls: list[tuple[Path, str]] = []

    def fake_collect_prompt_editor_input(
        target_root: Path,
        automatically_injected_instruction: str,
    ) -> tuple[Path, str]:
        """エディタ入力 call と自動注入指示を記録する。"""
        editor_calls.append((target_root, automatically_injected_instruction))
        return editor_path, "oracle の根拠を調査する"

    monkeypatch.setattr(
        investigation_module,
        "collect_prompt_editor_input",
        fake_collect_prompt_editor_input,
    )
    calls: list[tuple[AgentCallParameter, dict[str, object]]] = []
    monkeypatch.setattr(
        investigation_module,
        "run_codex_tui",
        lambda parameter, **kwargs: calls.append((parameter, kwargs)),
    )

    result = runner.invoke(
        app,
        ["oracle", "investigation"],
        catch_exceptions=False,
    )

    assert result.exit_code == 0
    assert len(editor_calls) == 1
    assert editor_calls[0][0] == root
    assert "oracle file は読み取り専用" in editor_calls[0][1]
    assert "realization file の読み書き禁止" in editor_calls[0][1]
    assert "oracle file の調査に必要な cmoc 固有の契約は自動注入" in editor_calls[0][1]
    assert len(calls) == 1
    parameter, kwargs = calls[0]
    assert parameter.model_class == ModelClass.FLAGSHIP
    assert parameter.reasoning_effort == ReasoningEffort.MAX
    assert parameter.file_access_mode == FileAccessMode.PURE_ORACLE_READ
    assert parameter.structured_output_schema_path is None
    assert parameter.agent_call_cwd == root.resolve()
    assert parameter.run_indexing_preflight is True
    assert kwargs["notification_command_name"] == "oracle investigation"
    prompt_path = (
        root / ".cmoc" / "gu" / "ar" / "log" / "editor_input" / f"{time_stamp}_cmpl.md"
    )
    assert parameter.prompt == f"{prompt_path} を読んで、その指示に従って下さい"
    complete_prompt = prompt_path.read_text(encoding="utf-8")
    assert "# oracle standard" in complete_prompt
    assert "oracle の根拠を調査する" in complete_prompt


def test_oracle_investigation_builder_exports_only_the_builder() -> None:
    """investigation の realization adapter が補助名を公開しない。"""
    expected = ["build_oracle_investigation_launch_tui_parameter"]
    assert launch_tui_module.__all__ == expected
    assert (
        sorted(name for name in vars(launch_tui_module) if not name.startswith("_"))
        == expected
    )
