"""`cmoc oracle review` の所見擁護理由列挙 prompt 正本。"""

# std
from pathlib import Path

# cmoc
from oracle.other.struct_doc import StructDoc, StructCodeBlock, render_as_markdown
from oracle.other.path_model import resolve_real_path
from oracle.acp_builder.basic import (
    AgentCallParameter,
    ModelClass,
    ReasoningEffort,
    FileAccessMode,
)
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
    # プロンプト
    prompt = build_complete_prompt(
        role="- あなたはソフトウェア仕様断片レビュー所見の擁護担当です",
        summary="- 対象所見が妥当である理由を調査すること",
        goal=f"""
        - 指定の Structured Output schema に従って、対象所見が妥当である理由を返していること
        - 既存の理由と重複しないよう、新規理由だけが列挙されていること
        - `{{{{oracle_root}}}}` ツリー内の oracle file を具体的な根拠とし、「かもしれない」「可能性がある」は根拠にしていないこと
        - 新規理由が無い場合、空配列を返していること
        """,
        file_access_mode=FileAccessMode.PURE_ORACLE_READ,
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
        aux_placeholder_def={
            "oracle-root": resolve_real_path("{{work-root}}/oracle"),
        },
        oracle_standard=True,
        oracle_review_standard=True,
    )
    # パラメータを生成して返す
    return AgentCallParameter(
        ModelClass.EFFICIENCY,
        ReasoningEffort.MAX,
        FileAccessMode.PURE_ORACLE_READ,
        render_as_markdown(prompt),
        Path(__file__).with_suffix(".json"),
        True,
    )
