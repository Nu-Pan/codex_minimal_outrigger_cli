"""feedback issue の同一性判断用 prompt 文面と起動パラメータの構築定義。"""

# std
from pathlib import Path

from oracle.other.path_model import AgentCallPathContext
from oracle.other.struct_doc import (
    SDCodeBlock,
    SDHeader,
    SDTagBlock,
    render_sd_node_as_markdown,
)
from oracle.prompt_builder.complete_prompt import build_complete_prompt

# cmoc
from oracle.request_builder.basic import (
    AgentCallParameter,
    FileAccessMode,
)


def build_feedback_issue_normalization_request(
    query_observation_json: str,
    known_issues_json: str,
    agent_call_cwd: Path,
) -> AgentCallParameter:
    """クエリ観測が既知の問題であるか判定するリスクエストを構築する。"""
    # 同一性判断中の追加報告を無効にし、MCP と prompt の選択をそろえる。
    enable_feedback_reporting = False
    path_context = AgentCallPathContext(agent_call_cwd=agent_call_cwd)
    query_observation_block = SDTagBlock(
        "query_observation",
        SDHeader(
            "query observation",
            SDCodeBlock("json", query_observation_json),
        ),
    )
    known_issue_block = SDTagBlock(
        "known_issue",
        SDHeader(
            "known issue",
            SDCodeBlock("json", known_issues_json),
        ),
    )
    prompt = build_complete_prompt(
        task=f"""
        - {query_observation_block.ref_tag} と同一の issue が {known_issue_block.ref_tag} 上に存在するか判断すること
        """,
        scope=f"""
        - 判断の対象は {query_observation_block.ref_tag} だけ
        - 判断の根拠はプロンプトで与えられた情報に限定されない
        """,
        completion_criteria="""
        - AI エージェントによる申告と確定事項とを区別すること
        - 観測当時に得られた根拠と現在に得た根拠とを区別すること
        """,
        file_access_mode=FileAccessMode.READONLY,
        path_context=path_context,
        enable_document_search_mcp=True,
        enable_feedback_reporting=enable_feedback_reporting,
        aux_dynamic_prompt=[
            query_observation_block,
            known_issue_block,
        ],
        cmoc_basic_instruction=True,
        routing_policy=True,
    )
    return AgentCallParameter(
        agent_call_kind=build_feedback_issue_normalization_request.__name__,
        file_access_mode=FileAccessMode.READONLY,
        prompt=render_sd_node_as_markdown(*prompt),
        structured_output_schema_path=Path(__file__).with_suffix(".json"),
        agent_call_cwd=path_context.agent_call_cwd,
        enable_document_search_mcp=True,
        enable_feedback_reporting=enable_feedback_reporting,
    )
