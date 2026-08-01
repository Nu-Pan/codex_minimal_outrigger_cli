"""session join conflict resolution の互換 import 経路。

`acp.builder.session.join.conflict_resolution` から import する caller が残る間だけ維持する。
canonical 実装は
`{{work-root}}/oracle/src/oracle/acp_builder/session/join/conflict_resolution.py`。
全 caller が canonical oracle path を直接使うようになったら削除する。
"""

from dataclasses import replace as _replace
from pathlib import Path as _Path

from oracle.acp_builder.basic import AgentCallParameter as _AgentCallParameter
from oracle.acp_builder.session.join.conflict_resolution import (
    build_session_join_conflict_resolution_parameter as _build_parameter,
)

from basic.path_model import AgentCallPathContext as _AgentCallPathContext
from basic.path_model import resolve_real_path as _resolve_real_path

from ...common.prompt_fence import _protect_code_block_fence

__all__ = ["build_session_join_conflict_resolution_parameter"]


def build_session_join_conflict_resolution_parameter(
    conflicted_paths: list[_Path],
) -> _AgentCallParameter:
    """canonical parameterを再公開し、競合 path の fence を保護する。"""
    parameter = _build_parameter(conflicted_paths)
    path_context = _AgentCallPathContext(parameter.agent_call_cwd)
    path_list = "\n".join(
        str(_resolve_real_path(path, path_context)) for path in conflicted_paths
    )
    return _replace(
        parameter,
        prompt=_protect_code_block_fence(
            parameter.prompt,
            section_heading="# conflict 対象ファイル",
            section_end_marker="\n\n# additional file access rule",
            info_string="text",
            section_body=path_list,
        ),
    )
