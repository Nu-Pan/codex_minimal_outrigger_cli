"""`cmoc review oracle` の所見否定理由列挙 prompt 構築実装。

対応 oracle file: `<work-root>/oracle/src/acp/builder/review/oracle/validate_finding_challenger.py`。
"""

# std
from pathlib import Path

# cmoc
from basic.struct_doc import StructDoc, StructCodeBlock, render_as_markdown
from basic.path_model import resolve_real_path
from basic.acp import (
    AgentCallParameter,
    ModelClass,
    ReasoningEffort,
    FileAccessMode,
)
from acp.prompt_parts.complete_prompt import build_complete_prompt


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
    # パス
    oracle_root = resolve_real_path(Path("<work-root>/oracle"))
    # プロンプト
    prompt = build_complete_prompt(
        role="- あなたはソフトウェア仕様断片レビュー所見の反証担当です",
        summary="- 対象所見が妥当ではない理由を調査すること",
        goal=f"""
        - 指定の Structured Output schema に従って、対象所見が妥当ではない理由を返していること
        - 既存の理由と重複しないよう、新規理由だけが列挙されていること
        - `{oracle_root}` ツリー内の oracle file を具体的な根拠とし、「かもしれない」「可能性がある」は根拠にしないこと
        - 新規理由が無い場合は空配列を返すこと
        """,
        file_access_mode=FileAccessMode.PURE_ORACLE_READ,
        aux_prompt=[
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
        oracle_standard=True,
        review_oracle_standard=True,
    )
    # パラメータを生成して返す
    return AgentCallParameter(
        ModelClass.EFFICIENCY,
        ReasoningEffort.MEDIUM,
        FileAccessMode.PURE_ORACLE_READ,
        render_as_markdown(prompt),
        Path(__file__).with_suffix(".json"),
    )
