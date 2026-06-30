"""`cmoc review oracle` の所見採否判定 prompt 正本。"""

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


def build_review_oracle_judge_finding_parameter(
    finding: str,
    advocate_reasons: str,
    challenger_reasons: str,
) -> AgentCallParameter:
    """
    `cmoc review oracle` サブコマンド、所見採否判定用。
    AI エージェント呼び出しパラメータを構築する。

    finding: str
        判定対象所見の詳細。
    advocate_reasons: str
        所見が妥当である理由。
    challenger_reasons: str
        所見が妥当ではない理由。
    """
    # プロンプト
    prompt = build_complete_prompt(
        role="- あなたはソフトウェア仕様断片レビュー所見の採否判定担当です",
        summary="- 指定の所見を人間へ提示すべきか判定すること",
        goal="- 指定された Structured Output schema に従って判定結果を返すこと",
        file_access_mode=FileAccessMode.PURE_ORACLE_READ,
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
        FileAccessMode.PURE_ORACLE_READ,
        render_as_markdown(prompt),
        Path(__file__).with_suffix(".json"),
    )
