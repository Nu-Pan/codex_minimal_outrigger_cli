"""session join conflict resolution builder の契約を検証する。

対応する正本: {{work-root}}/oracle/src/oracle/acp_builder/session/join/conflict_resolution.py
"""

from pathlib import Path

import acp.builder.session.join.conflict_resolution as session_conflict_resolution_module
from acp.builder.session.join.conflict_resolution import (
    build_session_join_conflict_resolution_parameter,
)
from basic.acp import FileAccessMode, ModelClass, ReasoningEffort


def test_session_join_compatibility_module_exports_only_builder() -> None:
    """公開モジュールが conflict resolution builder だけを export することを検証する。"""

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
    """conflict resolution 用パラメータが repo write 権限を使う契約を検証する。"""

    conflicted_path = Path(__file__).resolve()
    parameter = build_session_join_conflict_resolution_parameter([conflicted_path])

    assert parameter.model_class == ModelClass.FLAGSHIP
    assert parameter.reasoning_effort == ReasoningEffort.MAX
    assert parameter.file_access_mode == FileAccessMode.REPO_WRITE
    assert "conflict 対象ファイル" in parameter.prompt
    assert str(conflicted_path) in parameter.prompt
    assert parameter.run_indexing_preflight is False
