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
    section_heading_start: int | None = None,
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
    # 複数の動的 section を持つ caller は canonical prompt 上の見出し位置を
    # 固定できる。入力本文に後続 section そっくりの文字列があっても、実際の
    # section を補正するための指定である。
    # {{work-root}}/oracle/doc/app_spec/prompt_standard.md
    if section_heading_start is None:
        heading_starts: list[int] = []
        heading_search_start = 0
        while (heading_start := prompt.find(heading, heading_search_start)) != -1:
            heading_starts.append(heading_start)
            heading_search_start = heading_start + len(heading)
    elif 0 <= section_heading_start <= len(prompt) and prompt.startswith(
        heading, section_heading_start
    ):
        heading_starts = [section_heading_start]
    else:
        heading_starts = []

    for heading_start in heading_starts:
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


def _find_review_section_heading_starts(
    prompt: str,
    section_specs: tuple[tuple[str, str, str], ...],
) -> tuple[int, ...] | None:
    """Review prompt 内の連続する動的 section の実体位置を返す。"""
    # 動的本文に後続 section そっくりの文字列があっても、その本文ではなく
    # canonical builder が連続して構築した review section を補正対象にする。
    # {{work-root}}/oracle/src/oracle/acp_builder/oracle/review/judge_finding.py
    rendered_sections = [
        (
            section_heading,
            f"```text\n{_rendered_code_block_body('text', section_body)}\n```",
        )
        for section_heading, _, section_body in section_specs
    ]
    rendered_parts = [
        part
        for section_heading, block in rendered_sections
        for part in (section_heading, block)
    ]
    rendered_parts.append("# place holder definition")
    dynamic_region = "\n\n".join(rendered_parts)
    region_start = prompt.find(dynamic_region)
    if region_start == -1:
        return None

    starts: list[int] = []
    offset = region_start
    for heading, block in rendered_sections:
        starts.append(offset)
        offset += len(heading) + 2 + len(block) + 2
    return tuple(starts)


def _protect_review_sections(
    prompt: str,
    section_specs: tuple[tuple[str, str, str], ...],
) -> str:
    """Review prompt の動的 section を実体位置に基づいて補正する。"""
    section_starts = _find_review_section_heading_starts(prompt, section_specs)
    indices = (
        range(len(section_specs))
        if section_starts is None
        else reversed(range(len(section_specs)))
    )
    for index in indices:
        section_heading, section_end_marker, section_body = section_specs[index]
        prompt = _protect_code_block_fence(
            prompt,
            section_heading=section_heading,
            section_end_marker=section_end_marker,
            info_string="text",
            section_body=section_body,
            section_heading_start=(
                None if section_starts is None else section_starts[index]
            ),
        )
    return prompt


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
