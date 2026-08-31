"""feedback issue の検証用 prompt 文面と起動パラメータの構築定義。"""

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


def build_feedback_verify_issue_parameter(
    candidate_json: str,
    report_cut_references_json: str,
    agent_call_cwd: Path,
) -> AgentCallParameter:
    """report cut で固定した参照だけから 1 件の issue candidate を検証する。"""
    path_context = AgentCallPathContext(agent_call_cwd=agent_call_cwd)
    prompt = build_complete_prompt(
        task="""
        - 1 件の issue candidate を report cut 時点の固定済み参照だけから検証すること
        """,
        scope="""
        - 入力された candidate と report cut reference だけを根拠とする
        - それ以外 (file、live repository state、raw log、過去の Codex session、feedback state) を作業範囲に含めないこと
        """,
        non_goals="""
        - candidate 外の問題を探索しないこと
        """,
        file_access_mode=FileAccessMode.READONLY,
        path_context=path_context,
        aux_static_prompt=[
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
        routing_policy=False,
    )

    return AgentCallParameter(
        agent_call_kind=build_feedback_verify_issue_parameter.__name__,
        file_access_mode=FileAccessMode.READONLY,
        prompt=render_sd_node_as_markdown(*prompt),
        structured_output_schema_path=Path(__file__).with_suffix(".json"),
        agent_call_cwd=path_context.agent_call_cwd,
        run_indexing_preflight=True,
    )
