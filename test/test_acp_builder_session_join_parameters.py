"""session join conflict resolution builder の契約を検証する。

対応する正本: {{work-root}}/oracle/src/oracle/acp_builder/session/join/conflict_resolution.py
"""

from pathlib import Path

import pytest
from _git_support import make_repo

import acp.builder.session.join.conflict_resolution as session_conflict_resolution_module
from acp.builder.session.join.conflict_resolution import (
    build_session_join_conflict_resolution_parameter,
)
from basic.acp import FileAccessMode, ModelClass, ReasoningEffort


@pytest.fixture
def session_join_root(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """session join builder が参照する repository root を test 内に隔離する。"""
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    return root


def test_session_join_compatibility_module_exports_only_builder() -> None:
    """公開モジュールが conflict resolution builder だけを export することを検証する。"""

    assert session_conflict_resolution_module.__all__ == [
        "build_session_join_conflict_resolution_parameter"
    ]
    assert {
        name
        for name in vars(session_conflict_resolution_module)
        if not name.startswith("_")
    } == {"build_session_join_conflict_resolution_parameter"}


def test_session_join_conflict_resolution_uses_repo_write_mode(
    session_join_root: Path,
) -> None:
    """conflict resolution 用パラメータが repo write 権限を使う契約を検証する。"""

    conflicted_path = session_join_root / "conflict.md"
    parameter = build_session_join_conflict_resolution_parameter([conflicted_path])

    assert parameter.model_class == ModelClass.FLAGSHIP
    assert parameter.reasoning_effort == ReasoningEffort.MAX
    assert parameter.file_access_mode == FileAccessMode.REPO_WRITE
    assert parameter.structured_output_schema_path is None
    assert parameter.agent_call_cwd == session_join_root.resolve()
    assert "conflict 対象ファイル" in parameter.prompt
    assert str(conflicted_path) in parameter.prompt
    assert parameter.run_indexing_preflight is False
    assert "# conflict resolution standard" in parameter.prompt
    for heading in (
        "# oracle standard",
        "# realization standard",
        "# oracle review standard",
        "# apply review standard",
    ):
        assert heading not in parameter.prompt


def test_session_join_conflict_paths_protect_nested_code_fences(
    session_join_root: Path,
) -> None:
    """競合 path 内の三連 backtick が code block の境界を閉じないことを検証する。"""
    conflicted_path = Path("{{work-root}}/conflict" + "```" + ".txt")
    resolved_path = session_join_root / ("conflict" + "```" + ".txt")

    parameter = build_session_join_conflict_resolution_parameter([conflicted_path])

    start = parameter.prompt.index("# conflict 対象ファイル")
    end = parameter.prompt.index("\n\n# additional file access rule", start)
    section = parameter.prompt[start:end]
    assert section.startswith("# conflict 対象ファイル\n\n````text\n")
    assert str(resolved_path) in section
    assert "conflict```" in section
    assert section.endswith("\n````")
