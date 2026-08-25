"""feedback issue の検証用 prompt 文面と起動パラメータの構築定義。"""

# std
from pathlib import Path

# cmoc
from oracle.acp_builder.basic import (
    AgentCallParameter,
    FileAccessMode,
    ModelClass,
    ReasoningEffort,
)
from oracle.other.path_model import AgentCallPathContext
from oracle.other.struct_doc import (
    SDCodeBlock,
    SDHeader,
    render_sd_node_as_markdown,
)
from oracle.prompt_builder.complete_prompt import build_complete_prompt


def build_feedback_verify_issue_parameter(
    candidate_json: str,
    report_cut_references_json: str,
    agent_call_cwd: Path,
) -> AgentCallParameter:
    """report cut で固定した参照だけから 1 件の issue candidate を検証する。"""
    path_context = AgentCallPathContext(agent_call_cwd=agent_call_cwd)
    prompt = build_complete_prompt(
        summary="""
        - あなたは人間向け feedback issue の検証担当です
        - 1 件の issue candidate を report cut 時点の固定済み参照だけから検証すること
        """,
        goal="""
        - 指定された Structured Output schema に従って検証結果を返すこと
        """,
        file_access_mode=FileAccessMode.READONLY,
        path_context=path_context,
        aux_static_prompt=[
            SDHeader(
                "参照と変更の禁止",
                """
                - 入力された report cut reference 以外の file、live repository state、raw log、過去の Codex session、別 candidate、および feedback state を読んではならない
                - candidate 外の問題を探索してはならない
                - repository file、config、feedback state、または問題の根拠を変更してはならない
                """,
            ),
            SDHeader(
                "Structured Output の決定論的事後条件",
                """
                - `result.candidate_id` は入力 candidate ID と完全一致させる
                - current evidence の `reference_id` は入力された report cut reference ID だけから選ぶ
                - `unresolved | resolved | not_actionable` は少なくとも 1 件の `repository_content | current_fingerprint | probe_result` reference を根拠にし、過去の observation だけを根拠にしてはならない
                - fingerprint だけでは問題の存在を意味的に確認できない場合は `inconclusive` とする
                """,
            ),
        ],
        aux_dynamic_prompt=[
            SDHeader(
                "issue candidate",
                SDCodeBlock("json", candidate_json),
            ),
            SDHeader(
                "report cut references",
                SDCodeBlock("json", report_cut_references_json),
            ),
        ],
        oracle_and_realization_basic=True,
        routing_policy=True,
    )

    return AgentCallParameter(
        agent_call_kind=build_feedback_verify_issue_parameter.__name__,
        model_class=ModelClass.FLAGSHIP,
        reasoning_effort=ReasoningEffort.MAX,
        file_access_mode=FileAccessMode.READONLY,
        prompt=render_sd_node_as_markdown(*prompt),
        structured_output_schema_path=Path(__file__).with_suffix(".json"),
        agent_call_cwd=path_context.agent_call_cwd,
        run_indexing_preflight=True,
    )
