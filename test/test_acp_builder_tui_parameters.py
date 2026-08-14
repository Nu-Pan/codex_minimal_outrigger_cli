"""TUI 起動 builder の固定 parameter と prompt を検証する。

対応する正本: {{work-root}}/oracle/src/oracle/acp_builder/tui/launch_tui.py
"""

from pathlib import Path

import pytest
from _git_support import make_repo
from oracle.acp_builder.tui.launch_tui import (
    build_tui_launch_tui_parameter as build_canonical_tui_launch_tui_parameter,
)

import acp.builder.tui.launch_tui as tui_launch_module
from acp.builder.tui.launch_tui import build_tui_launch_tui_parameter
from basic.acp import FileAccessMode, ModelClass, ReasoningEffort


@pytest.mark.parametrize(
    "original_prompt",
    [
        "# 依頼\n\nsrc の実装を確認する。",
        "README の構成を調査する。",
        "{{original-prompt-here}}",
    ],
)
def test_tui_launch_builder_uses_fixed_parameter_and_standards(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    original_prompt: str,
) -> None:
    """オリジナル prompt によらず固定の規範と実行設定を使用する。"""
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)

    parameter = build_tui_launch_tui_parameter(
        "2026-08-03_12-00_00_000000000",
        original_prompt,
    )

    assert parameter.agent_call_kind == "build_tui_launch_tui_parameter"
    assert parameter.model_class == ModelClass.FLAGSHIP
    assert parameter.reasoning_effort == ReasoningEffort.MAX
    assert parameter.file_access_mode == FileAccessMode.REPO_WRITE
    assert parameter.structured_output_schema_path is None
    assert parameter.agent_call_cwd == root.resolve()
    assert parameter.run_indexing_preflight is True
    complete_path = (
        root
        / ".cmoc"
        / "gu"
        / "ar"
        / "log"
        / "editor_input"
        / "2026-08-03_12-00_00_000000000_cmpl.md"
    )
    assert parameter.prompt == f"{complete_path} を読んで、その指示に従って下さい"
    complete_prompt = complete_path.read_text(encoding="utf-8")
    for heading in (
        "# oracle and realization basic",
        "# oracle standard",
        "# realization standard",
        "# oracle review standard",
        "# apply review standard",
        "# realization oracle reference rule",
    ):
        assert heading in complete_prompt
    assert "# 両 branch の意味を保って conflict marker だけを解消する" not in (
        complete_prompt
    )
    assert "# index entry standard" not in complete_prompt
    assert "# routing rule" in complete_prompt
    assert original_prompt in complete_prompt
    if original_prompt == "{{original-prompt-here}}":
        assert complete_prompt.count(original_prompt) == 1


def test_tui_launch_module_exports_only_builder() -> None:
    """互換 module の公開面を現行 builder だけに限定する。"""
    assert tui_launch_module.__all__ == ["build_tui_launch_tui_parameter"]
    assert {name for name in vars(tui_launch_module) if not name.startswith("_")} == {
        "build_tui_launch_tui_parameter"
    }
    assert build_tui_launch_tui_parameter is build_canonical_tui_launch_tui_parameter
