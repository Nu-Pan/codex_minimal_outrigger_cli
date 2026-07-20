"""TUI resolve parameter builder の出力と schema を検証する。

対応する正本: {{work-root}}/oracle/src/oracle/acp_builder/tui/resolve_parameter.py
"""

import json

import acp.builder.tui.resolve_parameter as tui_resolve_parameter_module
from acp.builder.tui.resolve_parameter import (
    build_tui_resolve_parameter_parameter,
)
from basic.acp import FileAccessMode, ModelClass, ReasoningEffort


def test_tui_resolve_parameter_builder_embeds_original_prompt() -> None:
    """TUI parameter builderが元promptと標準promptを埋め込むことを検証する。"""
    original_prompt = "# 依頼\n\nsrc の実装を調べて必要なら修正して下さい。"

    parameter = build_tui_resolve_parameter_parameter(original_prompt)

    assert parameter.model_class == ModelClass.EFFICIENCY
    assert parameter.reasoning_effort == ReasoningEffort.MAX
    assert parameter.file_access_mode == FileAccessMode.READONLY
    assert parameter.structured_output_schema_path is not None
    assert parameter.structured_output_schema_path.name == "resolve_parameter.json"
    assert parameter.structured_output_schema_path.exists()
    assert "後続の AI Agent CLI/TUI 実行に必要な情報を選定" in parameter.prompt
    assert "4つの標準の選択結果" in parameter.prompt
    assert original_prompt in parameter.prompt
    assert "# oracle and realization basic" in parameter.prompt
    assert "# oracle standard" in parameter.prompt
    assert "# realization standard" in parameter.prompt
    assert "# oracle review standard" in parameter.prompt
    assert "# apply review standard" in parameter.prompt
    assert "# index entry standard" not in parameter.prompt


def test_tui_resolve_parameter_schema_contains_only_standard_flags() -> None:
    """TUI parameter schema が4つの standard 選択だけを求めることを検証する。"""
    parameter = build_tui_resolve_parameter_parameter("調査して下さい。")
    assert parameter.structured_output_schema_path is not None

    schema = json.loads(parameter.structured_output_schema_path.read_text())

    assert schema["required"] == [
        "oracle_standard",
        "realization_standard",
        "oracle_review_standard",
        "apply_review_standard",
    ]
    assert schema["additionalProperties"] is False
    for parameter_name in schema["required"]:
        parameter_schema = schema["properties"][parameter_name]
        assert parameter_schema["type"] == "object"
        assert parameter_schema["additionalProperties"] is False
        assert parameter_schema["required"] == ["value", "reason"]
        assert parameter_schema["properties"]["reason"]["type"] == "string"
        assert parameter_schema["properties"]["reason"]["description"]
    for flag_name in schema["required"]:
        assert (
            schema["properties"][flag_name]["properties"]["value"]["type"] == "boolean"
        )


def test_tui_resolve_parameter_module_exports_only_required_names() -> None:
    """TUI resolve互換moduleが必要な公開名だけを持つことを検証する。"""
    assert tui_resolve_parameter_module.__all__ == [
        "build_tui_resolve_parameter_parameter"
    ]
    assert not hasattr(tui_resolve_parameter_module, "render_as_markdown")
