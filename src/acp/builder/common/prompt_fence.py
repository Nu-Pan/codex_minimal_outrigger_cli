"""realization ACP builder で共有する Markdown code fence 補正。"""

import re as _re

from basic.struct_doc import ntqs as _ntqs


def _protect_code_block_fence(
    prompt: str,
    *,
    section_heading: str,
    section_end_marker: str,
    info_string: str | None,
    section_body: str,
) -> str:
    """動的本文を含む code block の外側 fence を本文より長くする。

    正本 builder の固定長 fence が動的本文で閉じないようにする補正である。
    根拠: `{{work-root}}/oracle/doc/app_spec/prompt_standard.md`。
    """
    prefix = f"```{info_string or ''}\n"
    suffix = "\n```"
    heading = f"{section_heading}\n\n"
    if not section_end_marker:
        return prompt

    # Dynamic input may contain the next heading and a code block, so identify
    # the exact rendered body before changing its outer fence.
    # {{work-root}}/oracle/doc/app_spec/prompt_standard.md
    body = _ntqs(section_body)
    section_start = -1
    section_end = -1
    heading_search_start = 0
    while (heading_start := prompt.find(heading, heading_search_start)) != -1:
        candidate_start = heading_start + len(heading)
        if prompt.startswith(prefix, candidate_start):
            body_start = candidate_start + len(prefix)
            candidate_end = body_start + len(body)
            if (
                prompt.startswith(body, body_start)
                and prompt.startswith(suffix, candidate_end)
                and prompt.startswith(section_end_marker, candidate_end + len(suffix))
            ):
                section_start = candidate_start
                section_end = candidate_end + len(suffix)
                break
        heading_search_start = candidate_start
    if section_start == -1:
        return prompt
    section = prompt[section_start:section_end]

    body = section[len(prefix) : -len(suffix)]
    longest_backtick_run = max(
        (len(match.group()) for match in _re.finditer(r"`+", body)),
        default=0,
    )
    fence = "`" * max(3, longest_backtick_run + 1)
    if fence == "```":
        return prompt

    opening = f"{fence}{info_string or ''}\n"
    replacement = f"{opening}{body}\n{fence}"
    return prompt[:section_start] + replacement + prompt[section_end:]
