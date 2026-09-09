"""quota availability probe の prompt 文面と起動パラメータの構築定義。"""

from pathlib import Path

from oracle.acp_builder.basic import (
    AgentCallParameter,
    FileAccessMode,
)
from oracle.other.path_model import AgentCallPathContext
from oracle.other.struct_doc import render_sd_node_as_markdown
from oracle.prompt_builder.complete_prompt import build_complete_prompt


def build_quota_availability_probe_parameter(
    agent_call_cwd: Path,
) -> AgentCallParameter:
    """Codex CLI の quota 回復確認用 agent call を構築する。"""
    path_context = AgentCallPathContext(agent_call_cwd=agent_call_cwd)
    prompt = build_complete_prompt(
        task="""
        - Codex CLI の利用可能性を確認するため、短い応答を 1 回返すこと
        """,
        non_goals="""
        - 追加の調査や作業を行わないこと
        """,
        file_access_mode=FileAccessMode.READONLY,
        path_context=path_context,
        # NOTE 利用可否の観測だけが目的なので policy は一切不要
    )
    return AgentCallParameter(
        agent_call_kind=build_quota_availability_probe_parameter.__name__,
        file_access_mode=FileAccessMode.READONLY,
        prompt=render_sd_node_as_markdown(*prompt),
        structured_output_schema_path=None,
        agent_call_cwd=path_context.agent_call_cwd,
        # NOTE quota probe から indexing preflight が再帰するのを避ける。
        run_indexing_preflight=False,
    )
