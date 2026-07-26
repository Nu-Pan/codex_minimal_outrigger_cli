"""oracle review finding judgment の realization adapter。

`acp.builder.oracle.review.judge_finding` から import する caller が残る間だけ維持する。
canonical 実装は
`{{work-root}}/oracle/src/oracle/acp_builder/oracle/review/judge_finding.py`。
全 caller が canonical oracle path を直接使うようになったら削除する。
"""

from dataclasses import replace as _replace

from oracle.acp_builder.basic import AgentCallParameter as _AgentCallParameter
from oracle.acp_builder.oracle.review.judge_finding import (
    build_oracle_review_judge_finding_parameter as _build_parameter,
)

from acp.builder.common.prompt_fence import (
    _protect_code_block_fence,
    _rendered_code_block_body,
)

__all__ = ["build_oracle_review_judge_finding_parameter"]


def build_oracle_review_judge_finding_parameter(
    finding: str,
    advocate_reasons: str,
    challenger_reasons: str,
) -> _AgentCallParameter:
    """canonical builder の parameter を再公開し、動的所見の fence を保護する。"""
    parameter = _build_parameter(finding, advocate_reasons, challenger_reasons)
    section_specs = (
        (
            "# 所見の内容",
            "\n\n# 所見が妥当であるとする理由",
            finding,
        ),
        (
            "# 所見が妥当であるとする理由",
            "\n\n# 所見が妥当ではないとする理由",
            advocate_reasons,
        ),
        (
            "# 所見が妥当ではないとする理由",
            "\n\n# place holder definition",
            challenger_reasons,
        ),
    )
    section_starts = _find_section_heading_starts(parameter.prompt, section_specs)
    prompt = parameter.prompt
    indices = (
        range(len(section_specs))
        if section_starts is None
        else reversed(range(len(section_specs)))
    )
    for index in indices:
        section_heading, section_end_marker, section_body = section_specs[index]
        section_heading_start = (
            None if section_starts is None else section_starts[index]
        )
        prompt = _protect_code_block_fence(
            prompt,
            section_heading=section_heading,
            section_end_marker=section_end_marker,
            info_string="text",
            section_body=section_body,
            section_heading_start=section_heading_start,
        )
    return _replace(parameter, prompt=prompt)


def _find_section_heading_starts(
    prompt: str,
    section_specs: tuple[tuple[str, str, str], ...],
) -> tuple[int, ...] | None:
    """canonical prompt 内の review 用動的 section の見出し位置を返す。"""
    # canonical builder が連続して構築する動的 section 全体を先に特定し、本文内の
    # section 風文字列を検索対象から外す。
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
