"""`cmoc review oracle` の所見否定理由列挙 prompt 正本。"""

# std
from pathlib import Path

# cmoc
from oracle.other.file_access_profile import FAPProfilePreset
from oracle.other.struct_doc import StructDoc, StructCodeBlock, render_as_markdown
from oracle.other.path_model import resolve_real_path
from oracle.acp_builder.basic import (
    AgentCallParameter,
    ModelClass,
    ReasoningEffort,
)
from oracle.prompt_builder.complete_prompt import build_complete_prompt


def build_review_oracle_validate_finding_challenger_parameter(
    finding: str,
    known_advocate_reasons: str,
    known_challenger_reasons: str,
) -> AgentCallParameter:
    """
    `cmoc review oracle` サブコマンド、所見が妥当ではない理由の列挙用。
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
        role="- あなたはソフトウェア仕様断片レビュー所見の反証担当です",
        summary="- 対象所見が妥当ではない理由を調査すること",
        goal="""
        - 指定の Structured Output schema に従って、対象所見が妥当ではない理由を返していること
        - 既存の理由と重複しないよう、新規理由だけが列挙されていること
        - `<oracle-root>` ツリー内の oracle file を具体的な根拠とし、「かもしれない」「可能性がある」は根拠にしないこと
        - 新規理由が無い場合は空配列を返すこと
        """,
        file_access_mode=FAPProfilePreset.PURE_ORACLE_READ,
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
            "oracle-root": resolve_real_path("<work-root>/oracle"),
        },
        oracle_standard=True,
        review_oracle_standard=True,
    )
    # パラメータを生成して返す
    return AgentCallParameter(
        ModelClass.EFFICIENCY,
        ReasoningEffort.MEDIUM,
        FAPProfilePreset.PURE_ORACLE_READ,
        render_as_markdown(prompt),
        Path(__file__).with_suffix(".json"),
    )
