"""quota availability probe の prompt 文面と起動パラメータの構築定義。"""

from pathlib import Path

from oracle.acp_builder.basic import (
    AgentCallParameter,
    FileAccessMode,
    ModelClass,
    ReasoningEffort,
)
from oracle.other.path_model import AgentCallPathContext
from oracle.other.struct_doc import render_as_markdown
from oracle.prompt_builder.complete_prompt import build_complete_prompt


def build_quota_availability_probe_parameter(
    agent_call_cwd: Path,
) -> AgentCallParameter:
    """Codex CLI の quota 回復確認用 agent call を構築する。"""
    # quota probe 自身の cwd から完全 prompt と起動パラメータを構築する。
    path_context = AgentCallPathContext(agent_call_cwd=agent_call_cwd)
    prompt = build_complete_prompt(
        role="- あなたは Codex CLI の利用可能性確認担当です",
        summary="- 追加の調査や作業を行わず、短い応答を 1 回返すこと",
        goal="- 応答を返して呼び出しを完了していること",
        file_access_mode=FileAccessMode.READONLY,
        path_context=path_context,
        routing_rule=False,
    )

    # availability の判定は Codex CLI の終了結果だけを使用する。
    return AgentCallParameter(
        agent_call_kind=build_quota_availability_probe_parameter.__name__,
        model_class=ModelClass.MINIMUM,
        reasoning_effort=ReasoningEffort.LOW,
        file_access_mode=FileAccessMode.READONLY,
        prompt=render_as_markdown(prompt),
        structured_output_schema_path=None,
        agent_call_cwd=path_context.agent_call_cwd,
        run_indexing_preflight=False,
    )
