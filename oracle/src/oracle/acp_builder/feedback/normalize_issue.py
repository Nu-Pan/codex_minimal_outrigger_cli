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
        summary="""
        - あなたは人間向け feedback issue の同一性判断担当です
        - 構造化済み observation を、絞り込み済みの既存 issue candidate と比較すること
        - observation が入力候補と同じ issue か、新しい issue かだけを判断すること
        """,
        goal="""
        - 指定された Structured Output schema に従って同一性判断を返すこと
        - agent が申告した原因、重要度、および重複判定用 hint を確定事実として扱っていないこと
        - issue の summary、impact、原因、現在性、actionability、human action、verification verdict、または relation を生成していないこと
        """,
        file_access_mode=FileAccessMode.READONLY,
        path_context=path_context,
        aux_static_prompt=[
            SDHeader(
                "参照禁止",
                """
                - 入力以外の file、raw log、過去の Codex session、feedback state、および候補外 issue を読んではならない
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
        routing_policy=True,
    )
    return AgentCallParameter(
        agent_call_kind=build_feedback_normalize_issue_parameter.__name__,
        file_access_mode=FileAccessMode.READONLY,
        prompt=render_sd_node_as_markdown(*prompt),
        structured_output_schema_path=Path(__file__).with_suffix(".json"),
        agent_call_cwd=path_context.agent_call_cwd,
        run_indexing_preflight=True,
    )
