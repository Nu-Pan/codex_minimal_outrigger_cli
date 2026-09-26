"""session join conflict resolution builder の契約を検証する。

対応する正本: {{work-root}}/oracle/src/oracle/acp_builder/session/join/conflict_resolution.py
"""

from pathlib import Path

import pytest
from _git_support import make_repo
from oracle.acp_builder.session.join.conflict_resolution import (
    build_session_join_conflict_resolution_parameter as build_canonical_conflict_parameter,
)

import acp.builder.session.join.conflict_resolution as session_conflict_resolution_module
from acp.builder.session.join.conflict_resolution import (
    build_session_join_conflict_resolution_parameter,
)
from basic.acp import DocumentSearchScope, FileAccessMode


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
    assert (
        build_session_join_conflict_resolution_parameter
        is build_canonical_conflict_parameter
    )


def test_session_join_conflict_resolution_uses_repo_write_mode(
    session_join_root: Path,
) -> None:
    """conflict resolution 用パラメータが repo write 権限を使う契約を検証する。"""

    source, target = "a" * 40, "b" * 40
    scope = DocumentSearchScope(allowed_subtrees=("oracle/doc",))
    parameter = build_session_join_conflict_resolution_parameter(
        source, target, session_join_root, document_search_scope=scope
    )

    assert parameter.file_access_mode == FileAccessMode.REPO_WRITE
    assert parameter.structured_output_schema_path is None
    assert parameter.agent_call_cwd == session_join_root.resolve()
    assert source in parameter.prompt
    assert target in parameter.prompt
    assert "conflict 対象ファイル" not in parameter.prompt
    objective = parameter.prompt.split('<cmoc_block id="objective">', 1)[1].split(
        "</cmoc_block>", 1
    )[0]
    assert "# task" in objective
    assert "進行中の merge" in objective
    assert parameter.document_search_scope == scope
    assert "# conflict resolution policy" in parameter.prompt
    assert "# routing policy" in parameter.prompt
    for heading in ("# oracle policy", "# realization policy"):
        assert heading in parameter.prompt
    assert "# realization findings policy" not in parameter.prompt


def test_session_join_conflict_prompt_passes_commit_references_without_path_list(
    session_join_root: Path,
) -> None:
    """差分と競合一覧は agent が Git から取得できる参照だけを渡す。"""
    parameter = build_session_join_conflict_resolution_parameter(
        "c" * 40,
        "d" * 40,
        session_join_root,
        document_search_scope=DocumentSearchScope(allowed_subtrees=("oracle/doc",)),
    )
    assert "共通祖先" in parameter.prompt
    assert "進行中の merge の Git index" in parameter.prompt
    assert "`" + "c" * 40 + "`" in parameter.prompt
    assert "`" + "d" * 40 + "`" in parameter.prompt
