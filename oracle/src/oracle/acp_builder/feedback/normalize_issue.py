"""feedback issue の同一性判断用 prompt 文面と起動パラメータの構築定義。"""

# std
from pathlib import Path

# cmoc
from oracle.acp_builder.basic import (
    AgentCallParameter,
    DocumentSearchScope,
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
    *,
    document_search_scope: DocumentSearchScope,
) -> AgentCallParameter:
    """構造化 observation と絞り込み済み候補の同一性判断用 parameter を構築する。

    NOTE
        `{{cmoc-root}}/oracle/doc/app_spec/sub_command/feedback_report.md` の
        「agent observation と normalization」に従い、関連ファイルを判断材料にできる。
        読み取り専用の境界を伝える分類説明と、参照先を選ぶ routing を含める。
    """
    path_context = AgentCallPathContext(agent_call_cwd=agent_call_cwd)
    prompt = build_complete_prompt(
        task="""
        - 構造化済み observation を絞り込み済みの既存 issue candidate と比較し、同じ issue か新しい issue かだけを判断すること
        """,
        scope="""
        - 入力だけでは同一性の判断に必要な情報が得られない場合は、処理経路や原因を含む関連情報を、`{{work-root}}` 内の oracle file、realization file などから参照してよい
        """,
        non_goals="""
        - 独立した原因診断や、issue の summary、impact、現在性、actionability、remediation result、human action、relation の生成は行わないこと
        - 候補外の issue を探索しないこと
        """,
        file_access_mode=FileAccessMode.READONLY,
        path_context=path_context,
        document_search_scope=document_search_scope,
        aux_static_prompt=[
            SDHeader(
                "同一性判断の基準",
                """
                - agent が申告した原因、重要度、および重複判定用 hint を確定事実として扱わないこと
                - 観測当時の evidence と現在のファイル状態を区別し、ファイルの変化や問題の解消だけを理由に別 issue と判断しないこと
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
        document_search_scope=document_search_scope,
    )
