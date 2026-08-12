"""feedback issue verification builder の互換 import 経路。

対応する oracle file:
`{{work-root}}/oracle/src/oracle/acp_builder/feedback/verify_issue.py`。
"""

from dataclasses import replace as _replace
from functools import wraps as _wraps
from pathlib import Path as _Path

from oracle.acp_builder.basic import AgentCallParameter as _AgentCallParameter
from oracle.acp_builder.feedback.verify_issue import (
    build_feedback_verify_issue_parameter as _build_parameter,
)

from ..common.prompt_fence import _protect_code_block_fence

__all__ = ["build_feedback_verify_issue_parameter"]


@_wraps(_build_parameter)
def build_feedback_verify_issue_parameter(
    candidate_json: str,
    report_cut_references_json: str,
    agent_call_cwd: _Path,
) -> _AgentCallParameter:
    """canonical prompt を再公開し、動的 JSON の fence を保護する。"""
    parameter = _build_parameter(
        candidate_json,
        report_cut_references_json,
        agent_call_cwd,
    )
    # {{work-root}}/oracle/doc/app_spec/prompt_standard.md
    # 動的入力中の backtick が後続の prompt section を命令として解釈させないようにする。
    prompt = _protect_code_block_fence(
        parameter.prompt,
        section_heading="# issue candidate",
        section_end_marker="\n\n# report cut references",
        info_string="json",
        section_body=candidate_json,
    )
    prompt = _protect_code_block_fence(
        prompt,
        section_heading="# report cut references",
        section_end_marker="\n\n# place holder definition",
        info_string="json",
        section_body=report_cut_references_json,
    )
    return _replace(parameter, prompt=prompt)
