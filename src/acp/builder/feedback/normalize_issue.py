"""feedback issue 同一性判断の realization adapter。

対応する oracle file:
`{{work-root}}/oracle/src/oracle/acp_builder/feedback/normalize_issue.py`。

oracle builder が schema で表現済みの分岐条件を prompt に重複させているため、
実運用へ渡す prompt からその重複だけを除去する。
"""

from dataclasses import replace as _replace
from functools import wraps as _wraps
from pathlib import Path as _Path

from oracle.acp_builder.basic import AgentCallParameter as _AgentCallParameter
from oracle.acp_builder.feedback.normalize_issue import (
    build_feedback_normalize_issue_parameter as _build_parameter,
)

__all__ = ["build_feedback_normalize_issue_parameter"]


def _remove_schema_duplicate_decision_instruction(prompt: str) -> str:
    """schema と重複する new 分岐の指示だけを canonical prompt から除く。"""
    heading = "# Structured Output の決定論的事後条件\n"
    section_start = prompt.find(heading)
    section_end = prompt.find("\n\n# ", section_start + len(heading))
    if section_start < 0 or section_end < 0:
        raise ValueError("normalization prompt postcondition section is missing")

    section = prompt[section_start:section_end]
    duplicate = "- `result.decision=new` の `result.existing_issue_id` は `null` とする"
    filtered = "\n".join(line for line in section.splitlines() if line != duplicate)
    return prompt[:section_start] + filtered + prompt[section_end:]


@_wraps(_build_parameter)
def build_feedback_normalize_issue_parameter(
    observation_json: str,
    candidate_issues_json: str,
    agent_call_cwd: _Path,
) -> _AgentCallParameter:
    """canonical builder を再公開し、schema 重複の prompt 指示だけを補正する。"""
    parameter = _build_parameter(
        observation_json,
        candidate_issues_json,
        agent_call_cwd,
    )
    # {{work-root}}/oracle/doc/app_spec/prompt_standard.md
    return _replace(
        parameter,
        prompt=_remove_schema_duplicate_decision_instruction(parameter.prompt),
    )
