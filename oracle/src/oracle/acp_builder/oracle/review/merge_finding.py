"""oracle review の所見統合用 prompt 文面と起動パラメータの構築定義。"""

# std
from pathlib import Path

from oracle.acp_builder.basic import (
    AgentCallParameter,
    FileAccessMode,
    ModelClass,
    ReasoningEffort,
)
from oracle.other.path_model import AgentCallPathContext

# cmoc
from oracle.other.struct_doc import (
    SDCodeBlock,
    SDHeader,
    render_sd_node_as_markdown,
)
from oracle.prompt_builder.complete_prompt import build_complete_prompt


def build_oracle_review_merge_finding_parameter(
    findings: str,
    *,
    agent_call_cwd: Path,
) -> AgentCallParameter:
    """
    `cmoc oracle review` サブコマンド、所見リストマージ用。
    AI エージェント呼び出しパラメータを構築する。

    findings: str
        現状の所見リスト。各所見は finding_id を含む想定。

    agent_call_cwd: Path
        oracle review agent call を実行する worktree
    """
    # 隔離済み review worktree を起点に prompt と起動パラメータを構築する
    path_context = AgentCallPathContext(agent_call_cwd=agent_call_cwd)

    # プロンプト
    prompt = build_complete_prompt(
        summary="""
        - あなたはソフトウェア仕様断片レビュー結果の整理担当です
        - `{{work-root}}/oracle` ツリー内の oracle file に対する所見リストを整理すること
        """,
        goal="""
        - 指定の Structured Output schema に従って編集操作を列挙すること
        - 編集操作実行後、所見同士の内容的な重複や相互矛盾が解消されていること
        - 十分コンパクトで整合的なら空配列を返すこと
        """,
        file_access_mode=FileAccessMode.PURE_ORACLE_READ,
        path_context=path_context,
        aux_static_prompt=[
            SDHeader(
                "Structured Output の決定論的事後条件",
                """
                - 各 `operations[].target_ids` の各値は、「現状の所見リスト」に入力された `finding_id` 集合の要素でなければならない
                """,
            ),
        ],
        aux_dynamic_prompt=[
            SDHeader(
                "現状の所見リスト",
                SDCodeBlock("text", findings),
            ),
        ],
        oracle_and_realization_basic=True,
        oracle_policy=True,
        oracle_review_policy=True,
        routing_policy=True,
    )
    # パラメータを生成して返す
    return AgentCallParameter(
        agent_call_kind=build_oracle_review_merge_finding_parameter.__name__,
        model_class=ModelClass.EFFICIENCY,
        reasoning_effort=ReasoningEffort.MAX,
        file_access_mode=FileAccessMode.PURE_ORACLE_READ,
        prompt=render_sd_node_as_markdown(prompt),
        structured_output_schema_path=Path(__file__).with_suffix(".json"),
        agent_call_cwd=path_context.agent_call_cwd,
        run_indexing_preflight=True,
    )
