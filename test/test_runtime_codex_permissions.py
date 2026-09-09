"""Codex sandbox argv が permission profile に依存しないことを検証する。

根拠:
- {{work-root}}/oracle/doc/app_spec/codex_exec_rule.md
- {{work-root}}/oracle/doc/dev_rule/test_rule.md
"""

from pathlib import Path

import pytest

from basic.acp import AgentCallParameter, FileAccessMode
from commons.runtime_codex_profile import (
    build_codex_override_args,
    prepare_codex_override_args,
)
from config.cmoc_config import CmocConfig


def _parameter(mode: FileAccessMode) -> AgentCallParameter:
    """指定modeの最小AgentCallParameterを作る。"""
    return AgentCallParameter(
        agent_call_kind="build_indexing_index_entry_parameter",
        file_access_mode=mode,
        prompt="prompt",
        structured_output_schema_path=None,
        agent_call_cwd=Path.cwd(),
    )


def test_path_based_permission_inputs_are_absent_from_builder_api() -> None:
    """path 別の read/write 例外を argv builder へ渡す入口を残さない。"""
    parameter = _parameter(FileAccessMode.READONLY)
    config = CmocConfig()
    for builder in (build_codex_override_args, prepare_codex_override_args):
        for name in (
            "root",
            "extra_read_paths",
            "extra_writable_paths",
            "extra_read_root",
            "allow_oracle_conflict_writes",
        ):
            with pytest.raises(TypeError, match=name):
                builder(
                    parameter,
                    config,
                    **{name: Path("path")},
                )
