"""`cmoc eval-oracle` の所見リストマージ prompt 構築実装。

対応 oracle file: `<work-root>/oracle/src/acp/builder/review/oracle/merge_finding.py`。
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


def build_review_oracle_merge_finding_parameter(
    findings: str,
) -> AgentCallParameter:
    """
    `cmoc eval-oracle` サブコマンド、所見リストマージ用。
    AI エージェント呼び出しパラメータを構築する。

    findings: str
        現状の所見リスト。各所見は finding_id を含む想定。
    """
    # パス
    oracle_root = resolve_real_path(Path("<work-root>/oracle"))
    # プロンプト
    prompt = build_complete_prompt(
        role="- あなたはソフトウェア仕様断片レビュー結果の整理担当です",
        summary=f"- `{oracle_root}` ツリー内の oracle file に対する所見リストを整理すること",
        goal="""
        - 指定の Structured Output schema に従って編集操作を列挙すること
        - 編集操作実行後、所見同士の内容的な重複や相互矛盾が解消されていること
        - 十分コンパクトで整合的なら空配列を返すこと
        - target_ids には入力所見の finding_id を指定すること
        """,
        file_access_mode=FileAccessMode.PURE_ORACLE_READ,
        aux_prompt=[
            StructDoc(
                "現状の所見リスト",
                StructCodeBlock("text", findings),
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
