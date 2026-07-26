"""realization ACP builder で共有する Markdown code fence 補正。"""

import re as _re

from basic import struct_doc as _struct_doc


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

    # 動的入力には次の見出しや code block が含まれ得るため、外側の fence を変更する前に
    # 描画後の本文を正確に特定する。canonical renderer を通すことで、空行の折りたたみと
    # indentation の正規化も維持する。
    # {{work-root}}/oracle/doc/app_spec/prompt_standard.md
    body = _rendered_code_block_body(info_string, section_body)
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


def _rendered_code_block_body(info_string: str | None, section_body: str) -> str:
    """Return the body text after canonical Markdown rendering normalization."""
    title = "__cmoc_prompt_fence_body__"
    rendered = _struct_doc.render_as_markdown(
        _struct_doc.StructDoc(
            title,
            _struct_doc.StructCodeBlock(info_string, section_body),
        )
    )
    prefix = f"# {title}\n\n```{info_string or ''}\n"
    suffix = "\n```\n"
    if not rendered.startswith(prefix) or not rendered.endswith(suffix):
        raise ValueError("Unexpected canonical code block rendering")
    return rendered[len(prefix) : -len(suffix)]
