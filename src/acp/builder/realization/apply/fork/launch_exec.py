"""realization apply fork の正本 builder を再公開する adapter。

対応する oracle file: `{{work-root}}/oracle/src/oracle/acp_builder/realization/apply/fork/launch_exec.py`。
"""

import re as _re
from dataclasses import replace as _replace
from pathlib import Path as _Path

from oracle.acp_builder.basic import AgentCallParameter as _AgentCallParameter
from oracle.acp_builder.realization.apply.fork.launch_exec import (
    build_realization_apply_fork_launch_exec_parameter as _build_parameter,
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
    return _replace(parameter, prompt=_protect_raw_diff_fence(parameter.prompt))


def _protect_raw_diff_fence(prompt: str) -> str:
    """raw diff 内の backtick が外側の GFM fence を閉じないようにする。

    正本 builder は `StructCodeBlock` の固定長 fence を使うが、raw diff には
    Markdown のコード fenceが含まれ得る。oracle src 側の prompt を維持したまま、
    realization 側で必要最小限の境界補正を行う。

    根拠: `{{work-root}}/oracle/doc/app_spec/prompt_standard.md`。
    """
    heading = "# oracle file の raw git diff\n\n"
    heading_start = prompt.find(heading)
    if heading_start == -1:
        return prompt

    section_start = heading_start + len(heading)
    section_end = prompt.rfind("\n\n</cmoc_block>", section_start)
    if section_end == -1:
        return prompt

    section = prompt[section_start:section_end]
    prefix = "```diff\n"
    suffix = "\n```"
    if not section.startswith(prefix) or not section.endswith(suffix):
        return prompt

    body = section[len(prefix) : -len(suffix)]
    longest_backtick_run = max(
        (len(match.group()) for match in _re.finditer(r"`+", body)),
        default=0,
    )
    fence = "`" * max(3, longest_backtick_run + 1)
    if fence == "```":
        return prompt

    replacement = f"{fence}diff\n{body}\n{fence}"
    return prompt[:section_start] + replacement + prompt[section_end:]
