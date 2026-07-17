"""session join conflict の制約を prompt と共通 sandbox へ分離して検証する。

根拠:
- {{work-root}}/oracle/src/oracle/acp_builder/session/join/conflict_resolution.py
- {{work-root}}/oracle/doc/app_spec/codex_exec_rule.md
"""

from pathlib import Path

from _codex_support import codex_arg_value, codex_override_config

from acp.builder.session.join.conflict_resolution import (
    build_session_join_conflict_resolution_parameter,
)
from basic.acp import FileAccessMode
from commons.runtime_codex_profile import build_codex_override_args
from config.cmoc_config import CmocConfig


def test_session_join_targets_stay_in_prompt_and_not_sandbox_argv(
    tmp_path: Path,
) -> None:
    """conflict path は prompt だけへ反映し、path 別 sandbox 設定へ変換しない。"""
    first = tmp_path / "repo" / "oracle" / "spec.md"
    second = tmp_path / "repo" / "src" / "main.py"
    first.parent.mkdir(parents=True)
    second.parent.mkdir(parents=True)

    first_parameter = build_session_join_conflict_resolution_parameter([first])
    second_parameter = build_session_join_conflict_resolution_parameter([second])
    first_args = build_codex_override_args(first_parameter, CmocConfig())
    second_args = build_codex_override_args(second_parameter, CmocConfig())

    assert first_parameter.file_access_mode == FileAccessMode.REPO_WRITE
    assert second_parameter.file_access_mode == FileAccessMode.REPO_WRITE
    assert str(first) in first_parameter.prompt
    assert str(second) in second_parameter.prompt
    assert first_args == second_args
    assert codex_arg_value(first_args, "--sandbox") == "workspace-write"
    assert all(str(first) not in arg and str(second) not in arg for arg in first_args)
    parsed = codex_override_config(first_args)
    assert "permissions" not in parsed
    assert "default_permissions" not in parsed
