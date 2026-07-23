"""`cmoc oracle review` の所見リストマージ prompt 正本。"""

# std
from pathlib import Path

from oracle.acp_builder.basic import (
    AgentCallParameter,
    FileAccessMode,
    ModelClass,
    ReasoningEffort,
)
from oracle.other.path_model import resolve_work_root

# cmoc
from oracle.other.struct_doc import StructCodeBlock, StructDoc, render_as_markdown
from oracle.prompt_builder.complete_prompt import build_complete_prompt


def build_oracle_review_merge_finding_parameter(
    findings: str,
) -> AgentCallParameter:
    """
    `cmoc oracle review` サブコマンド、所見リストマージ用。
    AI エージェント呼び出しパラメータを構築する。

    findings: str
        現状の所見リスト。各所見は finding_id を含む想定。
    """
    # プロンプト
    prompt = build_complete_prompt(
        role="- あなたはソフトウェア仕様断片レビュー結果の整理担当です",
        summary="- `{{work-root}}/oracle` ツリー内の oracle file に対する所見リストを整理すること",
        goal="""
        - 指定の Structured Output schema に従って編集操作を列挙すること
        - 編集操作実行後、所見同士の内容的な重複や相互矛盾が解消されていること
        - 十分コンパクトで整合的なら空配列を返すこと
        - target_ids には入力所見の finding_id を指定すること
        """,
        file_access_mode=FileAccessMode.PURE_ORACLE_READ,
        aux_dynamic_prompt=[
            StructDoc(
                "現状の所見リスト",
                StructCodeBlock("text", findings),
            ),
        ],
        aux_placeholder_def={
            "work-root": resolve_work_root(),
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
