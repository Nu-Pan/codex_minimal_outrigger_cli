"""feedback issue の同一性判断用 prompt 文面と起動パラメータの構築定義。"""

# std
from pathlib import Path

# cmoc
from oracle.acp_builder.basic import (
    AgentCallParameter,
    FileAccessMode,
)
from oracle.other.path_model import AgentCallPathContext
from oracle.other.struct_doc import (
    SDCodeBlock,
    SDHeader,
    render_sd_node_as_markdown,
)
from oracle.prompt_builder.complete_prompt import build_complete_prompt


def build_feedback_normalize_issue_parameter(
    observation_json: str,
    candidate_issues_json: str,
    agent_call_cwd: Path,
) -> AgentCallParameter:
    """構造化 observation と絞り込み済み候補から issue の同一性だけを判断する。"""
    path_context = AgentCallPathContext(agent_call_cwd=agent_call_cwd)
    prompt = build_complete_prompt(
        task="""
        - 構造化済み observation を絞り込み済みの既存 issue candidate と比較し、同じ issue か新しい issue かだけを判断すること
        """,
        scope="""
        - 入力された observation と既存 issue candidate だけを根拠とすること
        - 入力以外 (file、raw log、過去の Codex session、feedback state) を作業範囲に含めないこと
        """,
        non_goals="""
        - issue の summary、impact、原因、現在性、actionability、human action、verification verdict、または relation を生成しないこと
        - 候補外の issue を探索しないこと
        """,
        file_access_mode=FileAccessMode.READONLY,
        path_context=path_context,
        aux_static_prompt=[
            SDHeader(
                "同一性判断の基準",
                """
                - agent が申告した原因、重要度、および重複判定用 hint を確定事実として扱わないこと
                """,
            ),
            SDHeader(
                "Structured Output の決定論的事後条件",
                """
                - `result.decision=existing` の `result.existing_issue_id` は、入力された既存 issue candidate の issue ID と完全一致させる
                """,
            ),
        ],
        aux_dynamic_prompt=[
            SDHeader(
                "構造化済み observation",
                SDCodeBlock("json", observation_json),
            ),
            SDHeader(
                "既存 issue candidate",
                SDCodeBlock("json", candidate_issues_json),
            ),
        ],
        oracle_and_realization_basic=True,
        routing_policy=False,
    )
    return AgentCallParameter(
        agent_call_kind=build_feedback_normalize_issue_parameter.__name__,
        file_access_mode=FileAccessMode.READONLY,
        prompt=render_sd_node_as_markdown(*prompt),
        structured_output_schema_path=Path(__file__).with_suffix(".json"),
        agent_call_cwd=path_context.agent_call_cwd,
        run_indexing_preflight=True,
    )
