"""session join conflict resolution builder の契約を検証する。

対応する正本: <work-root>/oracle/src/oracle/acp_builder/session/join/conflict_resolution.py
"""

import acp.builder.session.join.conflict_resolution as session_conflict_resolution_module
from acp.builder.session.join.conflict_resolution import (
    build_session_join_conflict_resolution_parameter,
)
from basic.acp import FileAccessMode, ModelClass, ReasoningEffort


def test_session_join_compatibility_module_exports_only_builder() -> None:
    assert session_conflict_resolution_module.__all__ == [
        "build_session_join_conflict_resolution_parameter"
    ]
    for internal_name in [
        "Path",
        "StructDoc",
        "StructCodeBlock",
        "render_as_markdown",
        "resolve_real_path",
        "build_complete_prompt",
        "AgentCallParameter",
    ]:
        assert not hasattr(session_conflict_resolution_module, internal_name)


def test_session_join_conflict_resolution_uses_repo_write_mode() -> None:
    parameter = build_session_join_conflict_resolution_parameter([__file__])

    assert parameter.model_class == ModelClass.FLAGSHIP
    assert parameter.reasoning_effort == ReasoningEffort.MAX
    assert parameter.file_access_mode == FileAccessMode.REPO_WRITE
    assert "conflict 対象ファイル" in parameter.prompt
