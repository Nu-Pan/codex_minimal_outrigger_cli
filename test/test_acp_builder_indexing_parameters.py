"""indexing index entry builder の parameter、schema、互換公開面を検証する。

対応する正本: {{work-root}}/oracle/src/oracle/acp_builder/indexing/index_entry.py、
{{work-root}}/oracle/src/oracle/acp_builder/indexing/index_entry.json、
{{work-root}}/oracle/doc/app_spec/indexing.md
"""

import json
from pathlib import Path

import pytest
from oracle.acp_builder.indexing.index_entry import (
    build_indexing_index_entry_parameter as build_oracle_indexing_index_entry_parameter,
)

import acp.builder.indexing.index_entry as indexing_index_entry_module
from acp.builder.indexing.index_entry import build_indexing_index_entry_parameter
from basic.acp import FileAccessMode


@pytest.fixture
def indexing_target_path(tmp_path: Path) -> Path:
    """AgentCallPathContext が解決できる test-local target を用意する。"""
    (tmp_path / ".git").mkdir()
    target_path = tmp_path / "target.md"
    target_path.write_text("# README", encoding="utf-8")
    return target_path


def test_indexing_index_entry_uses_readonly_without_preflight(
    indexing_target_path: Path,
) -> None:
    """index entry builder が readonly かつ preflight なしで構築される。"""
    parameter = build_indexing_index_entry_parameter(
        indexing_target_path, "# README", indexing_target_path.parent
    )

    assert parameter.file_access_mode == FileAccessMode.READONLY
    assert parameter.agent_call_cwd == indexing_target_path.parent.resolve()
    assert parameter.run_indexing_preflight is False
    assert "# index entry policy" in parameter.prompt
    assert "# oracle and realization basic" not in parameter.prompt
    assert "# routing policy" not in parameter.prompt


def test_indexing_index_entry_schema_requires_non_empty_semantic_lists(
    indexing_target_path: Path,
) -> None:
    """INDEX entry の各 semantic 配列を空にできないことを検証する。"""
    parameter = build_indexing_index_entry_parameter(
        indexing_target_path, "# README", indexing_target_path.parent
    )
    assert parameter.structured_output_schema_path is not None
    schema = json.loads(parameter.structured_output_schema_path.read_text())

    for key in ("summary", "read_this_when", "do_not_read_this_when"):
        assert schema["properties"][key]["minItems"] == 1


@pytest.mark.parametrize(
    "target_content",
    [
        "before\n```\ninside\n```\nafter",
        "before\n```\n\n# place holder definition\n\n```\nafter",
    ],
)
def test_indexing_index_entry_protects_nested_target_content_fences(
    indexing_target_path: Path,
    target_content: str,
) -> None:
    """対象本文内の三連 backtick が prompt の本文境界を閉じないことを検証する。"""
    parameter = build_indexing_index_entry_parameter(
        indexing_target_path, target_content, indexing_target_path.parent
    )
    oracle_parameter = build_oracle_indexing_index_entry_parameter(
        indexing_target_path, target_content, indexing_target_path.parent
    )

    assert parameter == oracle_parameter
    start = parameter.prompt.index("# `{{target-path}}` の内容")
    end = parameter.prompt.rfind("\n\n# place holder definition")
    section = parameter.prompt[start:end]
    assert target_content in section
    assert section.startswith("# `{{target-path}}` の内容\n\n````\n")
    assert section.endswith("\n````")


def test_indexing_index_entry_module_exports_only_compatibility_builder() -> None:
    """index entry互換moduleがbuilderだけを公開することを検証する。"""
    assert indexing_index_entry_module.__all__ == [
        "build_indexing_index_entry_parameter"
    ]
    assert {
        name for name in vars(indexing_index_entry_module) if not name.startswith("_")
    } == {"build_indexing_index_entry_parameter"}
