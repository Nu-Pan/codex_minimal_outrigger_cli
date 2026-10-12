"""TUI 起動 builder の固定 parameter と prompt を検証する。

対応する正本: {{work-root}}/oracle/src/oracle/acp_builder/tui/launch_tui.py
"""

from pathlib import Path

import oracle.other.path_model as path_model_module
import pytest
from oracle.acp_builder.oracle.investigation.launch_tui import (
    build_oracle_investigation_launch_tui_parameter,
)
from oracle.acp_builder.tui.launch_tui import (
    build_tui_launch_tui_parameter as build_canonical_tui_launch_tui_parameter,
)

import acp.builder.tui.launch_tui as tui_launch_module
from acp.builder.tui.launch_tui import build_tui_launch_tui_parameter
from basic.acp import FileAccessMode, TuiResumeTarget


@pytest.mark.parametrize(
    "original_prompt",
    [
        "# 依頼\n\nsrc の実装を確認する。",
        "README の構成を調査する。",
        "{{original-prompt-here}}",
    ],
)
def test_tui_launch_builder_uses_fixed_parameter_and_policies(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    original_prompt: str,
) -> None:
    """オリジナル prompt によらず固定の規定と実行設定を使用する。"""
    # Git metadata の導出は test_basic_runtime.py と test_cli_tui.py に残す。
    # 文面・parameter の検査では root 探索結果だけを置換する。
    root = tmp_path / "repo"
    root.mkdir()
    monkeypatch.chdir(root)

    def resolve_test_roots(start_path: Path | None = None) -> tuple[Path, Path]:
        assert (Path.cwd() if start_path is None else start_path).resolve() == root
        return root, root

    monkeypatch.setattr(
        path_model_module, "_resolve_git_worktree_roots", resolve_test_roots
    )

    parameter = build_tui_launch_tui_parameter(original_prompt)

    assert parameter.agent_call_kind == "build_tui_launch_tui_parameter"
    assert parameter.file_access_mode == FileAccessMode.REPO_WRITE
    assert parameter.structured_output_schema_path is None
    assert parameter.agent_call_cwd == root.resolve()
    assert parameter.enable_editor_input_handoff_mcp is True
    assert parameter.enable_document_search_mcp is True
    complete_prompt = parameter.prompt
    assert f"- {{{{repo-root}}}} = {root}" in complete_prompt
    assert f"- {{{{work-root}}}} = {root}" in complete_prompt
    for heading in (
        "# oracle and realization basic",
        "# oracle policy",
        "# realization policy",
        "# realization findings policy",
        "# routing policy",
        "# editor input handoff",
    ):
        assert heading in complete_prompt
    for heading in (
        "# oracle findings policy",
        "# conflict resolution policy",
        "# index entry policy",
        "# realization oracle reference policy",
    ):
        assert heading not in complete_prompt
    objective = complete_prompt.split('<cmoc_block id="objective">', 1)[1].split(
        "</cmoc_block>", 1
    )[0]
    assert "# task" in objective
    assert (
        'オリジナルプロンプト <cmoc_ref target="original_prompt"/> が要求する作業'
        in (objective)
    )
    assert "# completion criteria" in objective
    assert "要求する成果と完了条件を満たしている" in objective
    assert "# scope" not in objective
    assert "# non-goals" not in objective
    assert complete_prompt.index('<cmoc_block id="objective">') < (
        complete_prompt.index('<cmoc_block id="original_prompt">')
    )
    original_block = complete_prompt.split('<cmoc_block id="original_prompt">', 1)[
        1
    ].split("</cmoc_block>", 1)[0]
    assert original_prompt in original_block
    assert not (root / ".cmoc" / "gu" / "log" / "editor_input").exists()


def test_tui_launch_module_exports_only_builder() -> None:
    """互換 module の公開面を現行 builder だけに限定する。"""
    assert tui_launch_module.__all__ == ["build_tui_launch_tui_parameter"]
    assert {name for name in vars(tui_launch_module) if not name.startswith("_")} == {
        "build_tui_launch_tui_parameter"
    }
    assert build_tui_launch_tui_parameter is build_canonical_tui_launch_tui_parameter


@pytest.mark.parametrize(
    "builder",
    [build_tui_launch_tui_parameter, build_oracle_investigation_launch_tui_parameter],
)
def test_resume_builder_keeps_workload_without_initial_input(
    cli_repository, tmp_path, monkeypatch, builder
):
    """現在の cwd や過去の prompt を使わず、保存 cwd と元の workload を保つ。"""
    monkeypatch.chdir(cli_repository)
    fresh = builder("original instruction")
    other = tmp_path / "unrelated_directory"
    other.mkdir()
    monkeypatch.chdir(other)

    resumed = builder(resume=TuiResumeTarget("exact-session-id", cli_repository))

    assert resumed.prompt is None
    assert resumed.tui_resume_session_id == "exact-session-id"
    assert resumed.agent_call_cwd == cli_repository.resolve()
    for field in (
        "agent_call_kind",
        "file_access_mode",
        "structured_output_schema_path",
        "enable_editor_input_handoff_mcp",
        "enable_document_search_mcp",
        "enable_feedback_reporting",
    ):
        assert getattr(resumed, field) == getattr(fresh, field)
