"""realization refactor の change summary builder を適合させる adapter。

対応する oracle file:
`{{work-root}}/oracle/src/oracle/acp_builder/realization/refactor/fork/change_summary.py`
`{{work-root}}/oracle/src/oracle/acp_builder/realization/refactor/fork/change_summary.json`。
"""

import re as _re
from dataclasses import replace as _replace

from oracle.acp_builder.basic import AgentCallParameter as _AgentCallParameter
from oracle.acp_builder.realization.refactor.fork.change_summary import (
    build_realization_refactor_fork_change_summary_parameter as _build_parameter,
)

__all__ = ["build_realization_refactor_fork_change_summary_parameter"]


def build_realization_refactor_fork_change_summary_parameter(
    raw_git_diff: str,
) -> _AgentCallParameter:
    """正本 builder の prompt を再公開し、raw diff の fence を保護する。"""
    parameter = _build_parameter(raw_git_diff)
    return _replace(parameter, prompt=_protect_raw_diff_fence(parameter.prompt))


def _protect_raw_diff_fence(prompt: str) -> str:
    """raw diff 内の backtick が GFM の外側 fence を閉じないようにする。

    正本 builder は固定長の fence を使うため、Markdown を含む diff は realization
    側で本文中の連続 backtick より長い fence へ置き換える。
    根拠: `{{work-root}}/oracle/doc/app_spec/prompt_standard.md`。
    """
    heading = "# run branch 上の refactor 差分\n\n"
    heading_start = prompt.find(heading)
    if heading_start == -1:
        return prompt

    section_start = heading_start + len(heading)
    placeholder_heading = "\n\n# place holder definition"
    section_end = prompt.rfind(placeholder_heading, section_start)
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
