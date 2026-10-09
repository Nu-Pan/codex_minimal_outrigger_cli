"""session join conflict resolution builder の契約を検証する。

対応する正本: {{work-root}}/oracle/src/oracle/acp_builder/session/join/conflict_resolution.py
"""

from pathlib import Path

from oracle.acp_builder.session.join.conflict_resolution import (
    build_session_join_conflict_resolution_parameter as build_canonical_conflict_parameter,
)

import acp.builder.session.join.conflict_resolution as session_conflict_resolution_module
from acp.builder.session.join.conflict_resolution import (
    build_session_join_conflict_resolution_parameter,
)
from basic.acp import FileAccessMode


def test_session_join_compatibility_module_reexports_canonical_builder() -> None:
    """公開モジュールが正本 builder だけを加工せず再公開する。"""

    assert session_conflict_resolution_module.__all__ == [
        "build_session_join_conflict_resolution_parameter"
    ]
    assert {
        name
        for name in vars(session_conflict_resolution_module)
        if not name.startswith("_")
    } == {"build_session_join_conflict_resolution_parameter"}
    assert (
        build_session_join_conflict_resolution_parameter
        is build_canonical_conflict_parameter
    )


def test_session_join_conflict_resolution_preserves_parameters_and_git_inputs(
    cli_repository: Path,
) -> None:
    """起動設定・編集範囲と、agent が Git から取得するための入力を検証する。"""

    source, target = "c" * 40, "d" * 40
    parameter = build_session_join_conflict_resolution_parameter(
        source, target, cli_repository
    )

    assert parameter.file_access_mode == FileAccessMode.REPO_WRITE
    assert parameter.structured_output_schema_path is None
    assert parameter.agent_call_cwd == cli_repository.resolve()
    assert f"`{source}`" in parameter.prompt
    assert f"`{target}`" in parameter.prompt
    assert "共通祖先" in parameter.prompt
    assert "進行中の merge の Git index" in parameter.prompt
    assert "conflict 対象ファイル" not in parameter.prompt
    objective = parameter.prompt.split('<cmoc_block id="objective">', 1)[1].split(
        "</cmoc_block>", 1
    )[0]
    assert "# task" in objective
    assert "進行中の merge" in objective
    assert parameter.enable_document_search_mcp is True
    assert "# conflict resolution policy" in parameter.prompt
    assert "# routing policy" in parameter.prompt
    for heading in ("# oracle policy", "# realization policy"):
        assert heading in parameter.prompt
    assert "# realization findings policy" not in parameter.prompt
