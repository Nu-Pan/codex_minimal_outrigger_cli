"""quota availability probe 用の AgentCallParameter を構築する。"""

from basic.acp import AgentCallParameter, FileAccessMode, ModelClass, ReasoningEffort
from oracle.other.struct_doc import render_as_markdown
from oracle.prompt_builder.complete_prompt import build_complete_prompt


_PROMPT = "quota 回復確認です。実行可能なら OK とだけ返してください。"


def build_quota_availability_probe_parameter(
    base_parameter: AgentCallParameter,
) -> AgentCallParameter:
    prompt = render_as_markdown(
        build_complete_prompt(
            role="- quota 回復確認を行う担当です",
            summary=f"- {_PROMPT}",
            goal="- 実行可能なら OK とだけ返してください。",
            file_access_mode=FileAccessMode.READONLY,
        )
    )
    # <work-root>/oracle/doc/app_spec/codex_exec_rule.md
    # <work-root>/oracle/src/oracle/prompt_builder/complete_prompt.py
    # <work-root>/oracle/src/oracle/prompt_builder/parts/file_access_rule.py
    # Keep the READONLY rule in the prompt aligned with the argv setting; the
    # runtime passes this prompt to Codex unchanged.
    return AgentCallParameter(
        ModelClass.MINIMUM,
        ReasoningEffort.LOW,
        FileAccessMode.READONLY,
        prompt,
        None,
        run_indexing_preflight=False,
        cwd=base_parameter.cwd,
    )


__all__ = ["build_quota_availability_probe_parameter"]
