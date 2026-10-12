"""session join conflict resolution builder の契約を検証する。

対応する正本:
- {{work-root}}/oracle/src/oracle/acp_builder/session/join/conflict_resolution.py
- {{work-root}}/oracle/doc/app_spec/codex_exec_rule.md
"""

from pathlib import Path

import oracle.other.path_model as path_model_module
import pytest
from _codex_support import codex_arg_value, codex_override_config
from oracle.acp_builder.session.join.conflict_resolution import (
    build_session_join_conflict_resolution_parameter as build_canonical_conflict_parameter,
)

import acp.builder.session.join.conflict_resolution as session_conflict_resolution_module
from acp.builder.session.join.conflict_resolution import (
    build_session_join_conflict_resolution_parameter,
)
from basic.acp import FileAccessMode
from commons.runtime_codex_profile import build_codex_override_args
from config.cmoc_config import CmocConfig


@pytest.fixture
def home_worktree(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """builder が渡す cwd を検査し、Git metadata 探索だけを置換する。"""
    # 実 Git の root 解決は test_basic_runtime.py と session join 結合 test に残す。
    home = tmp_path / "home"
    home.mkdir()

    def _resolve_worktree_roots(agent_call_cwd: Path) -> tuple[Path, Path]:
        assert agent_call_cwd == home.resolve()
        return home.resolve(), home.resolve()

    monkeypatch.setattr(
        path_model_module, "_resolve_git_worktree_roots", _resolve_worktree_roots
    )
    monkeypatch.chdir(tmp_path)
    return home


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


def test_session_join_conflict_resolution_preserves_prompt_and_launch_parameters(
    home_worktree: Path,
) -> None:
    """Git 入力を prompt のみに渡し、起動設定・編集範囲を維持する。"""

    source, target = "c" * 40, "d" * 40
    parameter = build_session_join_conflict_resolution_parameter(
        source, target, home_worktree
    )

    assert parameter.file_access_mode == FileAccessMode.REPO_WRITE
    assert parameter.structured_output_schema_path is None
    assert parameter.agent_call_cwd == home_worktree.resolve()
    assert f"- {{{{repo-root}}}} = {home_worktree.resolve()}" in parameter.prompt
    assert f"- {{{{work-root}}}} = {home_worktree.resolve()}" in parameter.prompt
    assert f"- source（取り込む側）: `{source}`" in parameter.prompt
    assert f"- target（取り込み先の merge 前）: `{target}`" in parameter.prompt
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
    # prompt 契約を検査した parameter を argv の検査にも使い、再構築しない。
    swapped_parameter = build_session_join_conflict_resolution_parameter(
        target, source, home_worktree
    )
    assert swapped_parameter.file_access_mode == FileAccessMode.REPO_WRITE
    assert f"- source（取り込む側）: `{target}`" in swapped_parameter.prompt
    assert f"- target（取り込み先の merge 前）: `{source}`" in swapped_parameter.prompt
    config = CmocConfig()
    args = build_codex_override_args(parameter, config)
    swapped_args = build_codex_override_args(swapped_parameter, config)

    assert args == swapped_args
    assert codex_arg_value(args, "--sandbox") == "workspace-write"
    assert all(source not in arg and target not in arg for arg in args)
    parsed = codex_override_config(args)
    assert "permissions" not in parsed
    assert "default_permissions" not in parsed
