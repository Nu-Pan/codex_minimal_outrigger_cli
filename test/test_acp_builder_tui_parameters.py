"""TUI resolve parameter builder の出力と schema を検証する。

対応する正本: {{work-root}}/oracle/src/oracle/acp_builder/tui/resolve_parameter.py
"""

import json

import acp.builder.tui.resolve_parameter as tui_resolve_parameter_module
from acp.builder.tui.resolve_parameter import (
    TUI_FILE_ACCESS_MODES,
    build_tui_resolve_parameter_parameter,
)
from basic.acp import FileAccessMode, ModelClass, ReasoningEffort


def test_tui_resolve_parameter_builder_embeds_original_prompt() -> None:
    original_prompt = "# 依頼\n\nsrc の実装を調べて必要なら修正して下さい。"

    parameter = build_tui_resolve_parameter_parameter(original_prompt)

    assert parameter.model_class == ModelClass.EFFICIENCY
    assert parameter.reasoning_effort == ReasoningEffort.MAX
    assert parameter.file_access_mode == FileAccessMode.READONLY
    assert parameter.structured_output_schema_path is not None
    assert parameter.structured_output_schema_path.name == "resolve_parameter.json"
    assert parameter.structured_output_schema_path.exists()
    assert "AI Agent CLI/TUI の実行パラメータ選定担当" in parameter.prompt
    assert "作業担当者 CLI/TUI" not in parameter.prompt
    assert "パラメータ選択結果" in parameter.prompt
    assert original_prompt in parameter.prompt
    assert "# oracle and realization basic" in parameter.prompt
    assert "# oracle standard" in parameter.prompt
    assert "# realization standard" in parameter.prompt
    assert "# review oracle standard" in parameter.prompt
    assert "# apply review standard" in parameter.prompt
    assert "# index entry standard" in parameter.prompt


def test_tui_resolve_parameter_schema_matches_logical_enum_values() -> None:
    parameter = build_tui_resolve_parameter_parameter("調査して下さい。")
    assert parameter.structured_output_schema_path is not None

    schema = json.loads(parameter.structured_output_schema_path.read_text())

    assert schema["required"] == [
        "role",
        "summary",
        "goal",
        "file_access_mode",
        "oracle_and_realization_basic",
        "oracle_standard",
        "realization_standard",
        "review_oracle_standard",
        "apply_review_standard",
        "index_entry_standard",
    ]
    assert schema["additionalProperties"] is False
    for parameter_name in schema["required"]:
        parameter_schema = schema["properties"][parameter_name]
        assert parameter_schema["type"] == "object"
        assert parameter_schema["additionalProperties"] is False
        assert parameter_schema["required"] == ["value", "reason"]
        assert parameter_schema["properties"]["reason"]["type"] == "string"
        assert parameter_schema["properties"]["reason"]["description"]
    assert schema["properties"]["file_access_mode"]["properties"]["value"]["enum"] == [
        file_access_mode.value for file_access_mode in TUI_FILE_ACCESS_MODES
    ]
    assert (
        "repo_write"
        in schema["properties"]["file_access_mode"]["properties"]["value"]["enum"]
    )
    for flag_name in [
        "oracle_and_realization_basic",
        "oracle_standard",
        "realization_standard",
        "review_oracle_standard",
        "apply_review_standard",
        "index_entry_standard",
    ]:
        assert (
            schema["properties"][flag_name]["properties"]["value"]["type"] == "boolean"
        )


def test_tui_resolve_parameter_module_exports_only_required_names() -> None:
    assert tui_resolve_parameter_module.__all__ == [
        "build_tui_resolve_parameter_parameter",
        "TUI_FILE_ACCESS_MODES",
    ]
    assert not hasattr(tui_resolve_parameter_module, "render_as_markdown")
