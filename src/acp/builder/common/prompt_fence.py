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
    prefix = f"```{info_string or ''}\n"
    suffix = "\n```"
    heading = f"{section_heading}\n\n"
    if not section_end_marker:
        return prompt

    # 動的本文に同じ見出しや終了マーカーが現れても、code block の境界を探し続ける。
    heading_search_start = 0
    selected_section: tuple[int, int, str] | None = None
    while (heading_start := prompt.find(heading, heading_search_start)) != -1:
        candidate_start = heading_start + len(heading)
        if prompt.startswith(prefix, candidate_start):
            end_search_start = candidate_start
            fallback_section: tuple[int, int, str] | None = None
            while (
                candidate_end := prompt.find(section_end_marker, end_search_start)
            ) != -1:
                candidate_section = prompt[candidate_start:candidate_end]
                if candidate_section.endswith(suffix):
                    candidate = (candidate_start, candidate_end, candidate_section)
                    fallback_section = candidate
                    # StructDoc の次の code block が続く境界を優先する。
                    if prompt.startswith(
                        "\n\n```", candidate_end + len(section_end_marker)
                    ):
                        selected_section = candidate
                        break
                end_search_start = candidate_end + len(section_end_marker)
            if selected_section is None:
                selected_section = fallback_section
            if selected_section is not None:
                break
        heading_search_start = candidate_start

    if selected_section is None:
        return prompt
    section_start, section_end, section = selected_section

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
