"""indexing index entry builder の parameter と互換公開面を検証する。

対応する正本: {{work-root}}/oracle/src/oracle/acp_builder/indexing/index_entry.py
"""

from pathlib import Path

import acp.builder.indexing.index_entry as indexing_index_entry_module
from acp.builder.indexing.index_entry import build_indexing_index_entry_parameter
from basic.acp import FileAccessMode, ModelClass, ReasoningEffort


def test_indexing_index_entry_uses_minimum_model_and_low_reasoning() -> None:
    parameter = build_indexing_index_entry_parameter(Path(__file__), "# README")

    assert parameter.model_class == ModelClass.MINIMUM
    assert parameter.reasoning_effort == ReasoningEffort.LOW
    assert parameter.file_access_mode == FileAccessMode.READONLY
    assert parameter.run_indexing_preflight is False


def test_indexing_index_entry_module_exports_only_compatibility_builder() -> None:
    assert indexing_index_entry_module.__all__ == [
        "build_indexing_index_entry_parameter"
    ]
    assert not hasattr(indexing_index_entry_module, "Path")
    assert not hasattr(indexing_index_entry_module, "render_as_markdown")
