"""indexing index entry builder の parameter、schema、互換公開面を検証する。

対応する正本: {{work-root}}/oracle/src/oracle/acp_builder/indexing/index_entry.py、
{{work-root}}/oracle/src/oracle/acp_builder/indexing/index_entry.json
"""

import json
from pathlib import Path

import acp.builder.indexing.index_entry as indexing_index_entry_module
from acp.builder.indexing.index_entry import build_indexing_index_entry_parameter
from basic.acp import FileAccessMode, ModelClass, ReasoningEffort


def test_indexing_index_entry_uses_minimum_model_and_low_reasoning() -> None:
    """index entry builderがminimum modelとlow reasoningを選ぶことを検証する。"""
    parameter = build_indexing_index_entry_parameter(Path(__file__), "# README")

    assert parameter.model_class == ModelClass.MINIMUM
    assert parameter.reasoning_effort == ReasoningEffort.LOW
    assert parameter.file_access_mode == FileAccessMode.READONLY
    assert parameter.run_indexing_preflight is False


def test_indexing_index_entry_schema_requires_non_empty_semantic_lists() -> None:
    """INDEX entry の各 semantic 配列を空にできないことを検証する。"""
    parameter = build_indexing_index_entry_parameter(Path(__file__), "# README")
    assert parameter.structured_output_schema_path is not None
    schema = json.loads(parameter.structured_output_schema_path.read_text())

    for key in ("summary", "read_this_when", "do_not_read_this_when"):
        assert schema["properties"][key]["minItems"] == 1


def test_indexing_index_entry_keeps_nested_code_fences_in_target_content() -> None:
    """対象本文内の三連 backtick が prompt の本文境界を閉じないことを検証する。"""
    target_content = "before\n```\ninside\n```\nafter"

    parameter = build_indexing_index_entry_parameter(Path(__file__), target_content)

    assert "````\nbefore\n```\ninside\n```\nafter\n````" in parameter.prompt


def test_indexing_index_entry_module_exports_only_compatibility_builder() -> None:
    """index entry互換moduleがbuilderだけを公開することを検証する。"""
    assert indexing_index_entry_module.__all__ == [
        "build_indexing_index_entry_parameter"
    ]
    assert not hasattr(indexing_index_entry_module, "Path")
    assert not hasattr(indexing_index_entry_module, "render_as_markdown")
