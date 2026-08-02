"""`cmoc oracle review` の所見採否判定 prompt 正本。"""

# std
from pathlib import Path

from oracle.acp_builder.basic import (
    AgentCallParameter,
    FileAccessMode,
    ModelClass,
    ReasoningEffort,
)
from oracle.other.path_model import AgentCallPathContext, resolve_repo_root

# cmoc
from oracle.other.struct_doc import StructCodeBlock, StructDoc, render_as_markdown
from oracle.prompt_builder.complete_prompt import build_complete_prompt


def build_oracle_review_judge_finding_parameter(
    finding: str,
    advocate_reasons: str,
    challenger_reasons: str,
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
    """
    # oracle review は main worktree を agent_call_cwd として先に確定する
    path_context = AgentCallPathContext(agent_call_cwd=resolve_repo_root())

    # プロンプト
    prompt = build_complete_prompt(
        role="- あなたはソフトウェア仕様断片レビュー所見の採否判定担当です",
        summary="- 指定の所見を人間へ提示すべきか判定すること",
        goal="- 指定された Structured Output schema に従って判定結果を返すこと",
        file_access_mode=FileAccessMode.PURE_ORACLE_READ,
        path_context=path_context,
        aux_dynamic_prompt=[
            StructDoc(
                "所見の内容",
                StructCodeBlock(
                    "text",
                    finding,
                ),
            ),
            StructDoc(
                "所見が妥当であるとする理由",
                StructCodeBlock(
                    "text",
                    advocate_reasons,
                ),
            ),
            StructDoc(
                "所見が妥当ではないとする理由",
                StructCodeBlock(
                    "text",
                    challenger_reasons,
                ),
            ),
        ],
        oracle_and_realization_basic=True,
    )
    # パラメータを生成して返す
    return AgentCallParameter(
        model_class=ModelClass.EFFICIENCY,
        reasoning_effort=ReasoningEffort.MAX,
        file_access_mode=FileAccessMode.PURE_ORACLE_READ,
        prompt=render_as_markdown(prompt),
        structured_output_schema_path=Path(__file__).with_suffix(".json"),
        agent_call_cwd=path_context.agent_call_cwd,
        run_indexing_preflight=True,
    )
