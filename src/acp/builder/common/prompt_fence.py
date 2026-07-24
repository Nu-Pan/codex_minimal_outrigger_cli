"""realization ACP builder で共有する Markdown code fence 補正。"""

import re as _re


def _protect_code_block_fence(
    prompt: str,
    *,
    section_heading: str,
    section_end_marker: str,
    info_string: str | None,
) -> str:
    """動的本文を含む code block の外側 fence を本文より長くする。

    正本 builder の固定長 fence が動的本文で閉じないようにする補正である。
    根拠: `{{work-root}}/oracle/doc/app_spec/prompt_standard.md`。
    """
    heading = f"{section_heading}\n\n"
    heading_start = prompt.find(heading)
    if heading_start == -1:
        return prompt

    section_start = heading_start + len(heading)
    section_end = prompt.rfind(section_end_marker, section_start)
    if section_end == -1:
        return prompt

    section = prompt[section_start:section_end]
    prefix = f"```{info_string or ''}\n"
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

    opening = f"{fence}{info_string or ''}\n"
    replacement = f"{opening}{body}\n{fence}"
    return prompt[:section_start] + replacement + prompt[section_end:]
