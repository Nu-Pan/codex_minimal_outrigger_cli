"""oracle review の所見採否判定用 prompt 文面と起動パラメータの構築定義。"""

# std
from pathlib import Path

from oracle.acp_builder.basic import (
    AgentCallParameter,
    FileAccessMode,
)
from oracle.other.path_model import AgentCallPathContext

# cmoc
from oracle.other.struct_doc import (
    SDCodeBlock,
    SDHeader,
    render_sd_node_as_markdown,
)
from oracle.prompt_builder.complete_prompt import build_complete_prompt


def build_oracle_review_judge_finding_parameter(
    finding: str,
    advocate_reasons: str,
    challenger_reasons: str,
    *,
    agent_call_cwd: Path,
) -> AgentCallParameter:
    """
    `cmoc oracle review` サブコマンド、所見採否判定用。
    AI エージェント呼び出しパラメータを構築する。

    finding: str
        判定対象所見の詳細。
    advocate_reasons: str
        所見が妥当である理由。
    challenger_reasons: str
        所見が妥当ではない理由。

    agent_call_cwd: Path
        oracle review agent call を実行する worktree
    """
    path_context = AgentCallPathContext(agent_call_cwd=agent_call_cwd)
    prompt = build_complete_prompt(
        summary="""
        - あなたはソフトウェア仕様断片レビュー所見の採否判定担当です
        - 指定の所見を人間へ提示すべきか判定すること
        """,
        goal="""
        - 指定された Structured Output schema に従って判定結果を返すこと
        """,
        file_access_mode=FileAccessMode.PURE_ORACLE_READ,
        path_context=path_context,
        aux_dynamic_prompt=[
            SDHeader(
                "所見の内容",
                SDCodeBlock(
                    "text",
                    finding,
                ),
            ),
            SDHeader(
                "所見が妥当であるとする理由",
                SDCodeBlock(
                    "text",
                    advocate_reasons,
                ),
            ),
            SDHeader(
                "所見が妥当ではないとする理由",
                SDCodeBlock(
                    "text",
                    challenger_reasons,
                ),
            ),
        ],
        oracle_and_realization_basic=True,
        oracle_policy=True,
        oracle_findings_policy=True,
        routing_policy=True,
    )
    return AgentCallParameter(
        agent_call_kind=build_oracle_review_judge_finding_parameter.__name__,
        file_access_mode=FileAccessMode.PURE_ORACLE_READ,
        prompt=render_sd_node_as_markdown(*prompt),
        structured_output_schema_path=Path(__file__).with_suffix(".json"),
        agent_call_cwd=path_context.agent_call_cwd,
        run_indexing_preflight=True,
    )
