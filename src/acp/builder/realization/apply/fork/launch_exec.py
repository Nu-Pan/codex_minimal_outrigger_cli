"""realization apply fork の正本 builder を再公開する adapter。

対応する oracle file: `{{work-root}}/oracle/src/oracle/acp_builder/realization/apply/fork/launch_exec.py`。
"""

from dataclasses import replace as _replace
from pathlib import Path as _Path

from oracle.acp_builder.basic import AgentCallParameter as _AgentCallParameter
from oracle.acp_builder.realization.apply.fork.launch_exec import (
    build_realization_apply_fork_launch_exec_parameter as _build_parameter,
)

from acp.builder.common.prompt_fence import (
    _protect_code_block_fence,
)

__all__ = ["build_realization_apply_fork_launch_exec_parameter"]


def build_realization_apply_fork_launch_exec_parameter(
    diff_base_commit: str,
    run_fork_commit: str,
    raw_oracle_git_diff: str,
    run_worktree: _Path,
) -> _AgentCallParameter:
    """正本 builder の prompt を再公開し、raw diff の fence を保護する。"""
    parameter = _build_parameter(
        diff_base_commit,
        run_fork_commit,
        raw_oracle_git_diff,
        run_worktree,
    )
    return _replace(
        parameter,
        prompt=_protect_code_block_fence(
            parameter.prompt,
            section_heading="# oracle file の raw git diff",
            section_end_marker="\n\n</cmoc_block>",
            info_string="diff",
            section_body=raw_oracle_git_diff,
        ),
    )
