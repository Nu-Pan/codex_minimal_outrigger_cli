"""`cmoc oracle review` の所見擁護理由列挙 prompt 正本。"""

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


def build_oracle_review_validate_finding_advocate_parameter(
    finding: str,
    known_advocate_reasons: str,
    known_challenger_reasons: str,
) -> AgentCallParameter:
    """
    `cmoc oracle review` サブコマンド、所見が妥当である理由の列挙用。
    AI エージェント呼び出しパラメータを構築する。

    finding: str
        レビュー対象所見の詳細。
    known_advocate_reasons: str
        既知の妥当である理由。
    known_challenger_reasons: str
        既知の妥当ではない理由。
    """
    # oracle review は main worktree を agent_call_cwd として先に確定する
    path_context = AgentCallPathContext(agent_call_cwd=resolve_repo_root())

    # プロンプト
    prompt = build_complete_prompt(
        role="- あなたはソフトウェア仕様断片レビュー所見の擁護担当です",
        summary="- 対象所見が妥当である理由を調査すること",
        goal="""
        - 指定の Structured Output schema に従って、対象所見が妥当である理由を返していること
        - 既存の理由と重複しないよう、新規理由だけが列挙されていること
        - 新規理由が無い場合、空配列を返していること
        """,
        file_access_mode=FileAccessMode.PURE_ORACLE_READ,
        path_context=path_context,
        aux_dynamic_prompt=[
            StructDoc(
                "対象所見",
                StructCodeBlock(
                    "text",
                    finding,
                ),
            ),
            StructDoc(
                "既知の妥当であるとする理由",
                StructCodeBlock(
                    "text",
                    known_advocate_reasons,
                ),
            ),
            StructDoc(
                "既知の妥当ではないとする理由",
                StructCodeBlock(
                    "text",
                    known_challenger_reasons,
                ),
            ),
        ],
        oracle_and_realization_basic=True,
        oracle_review_standard=True,
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
