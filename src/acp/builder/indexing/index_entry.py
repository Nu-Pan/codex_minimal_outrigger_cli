"""`{{work-root}}/oracle/src/oracle/acp_builder/indexing/index_entry.py` を再公開する。

既存の `acp.builder.indexing.index_entry` 参照を維持するために残す互換入口。
削除条件は realization 側と利用者向け公開面から同参照がなくなること。
"""

import re as _re
from dataclasses import replace as _replace
from pathlib import Path as _Path

from oracle.acp_builder.indexing.index_entry import (
    build_indexing_index_entry_parameter as _build_indexing_index_entry_parameter,
)

from basic.acp import AgentCallParameter as _AgentCallParameter

__all__ = ["build_indexing_index_entry_parameter"]


def build_indexing_index_entry_parameter(
    target_path: _Path,
    target_content: str,
) -> _AgentCallParameter:
    """正本 builder の parameter を再公開し、対象本文の fence を保護する。"""
    parameter = _build_indexing_index_entry_parameter(target_path, target_content)
    return _replace(parameter, prompt=_protect_target_content_fence(parameter.prompt))


def _protect_target_content_fence(prompt: str) -> str:
    """対象本文中の backtick が prompt の外側 fence を閉じないようにする。

    `{{work-root}}/oracle/src/oracle/acp_builder/indexing/index_entry.py` は
    任意の本文を固定長の StructCodeBlock に渡すため、realization 側で本文内の
    連続 backtick より長い outer fence へ置き換える。
    """
    heading = "# `{{target-path}}` の内容\n\n"
    heading_start = prompt.find(heading)
    if heading_start == -1:
        return prompt

    section_start = heading_start + len(heading)
    placeholder_heading = "\n\n# place holder definition"
    section_end = prompt.rfind(placeholder_heading, section_start)
    if section_end == -1:
        return prompt

    section = prompt[section_start:section_end]
    prefix = "```\n"
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

    replacement = f"{fence}\n{body}\n{fence}"
    return prompt[:section_start] + replacement + prompt[section_end:]
