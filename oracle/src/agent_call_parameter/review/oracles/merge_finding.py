"""`cmoc review oracle` の所見リストマージ prompt 正本。"""

# std
from pathlib import Path

# cmoc
from utils.struct_doc import render_as_markdown
from utils.path_model import resolve_real_path
from agent_call_parameter.base import AgentCallParameters, ModelClass, ReasoningEffort
from prompt_parts.complete_prompt import build_complete_prompt


def build_review_oracle_merge_finding_parameter(
    findings: str,
) -> AgentCallParameters:
    """
    `cmoc review oracle` サブコマンド、所見リストマージ用。
    AI エージェント呼び出しパラメータを構築する。

    findings: str
        現状の所見リスト。各所見は finding_id を含む想定。
    """
    # パス
    oracle_root = resolve_real_path(Path("<work-root>/oracle"))
    # プロンプト
    prompt = build_complete_prompt(
        "- あなたはソフトウェア仕様断片レビュー結果の整理担当です",
        f"""
        - `{oracle_root}` ツリー内の oracle file に対する所見リストを整理すること
        - 現状の所見リストは以下である

        ```text
        {findings}
        ```
        """,
        """
        - 所見同士の内容的な重複や相互矛盾を解消する編集操作を列挙すること
        - 十分コンパクトで整合的なら空配列を返すこと
        - target_ids には入力所見の finding_id を指定すること
        """,
        "pure_oracle_read",
        oracle_standard=True,
        structured_output=True,
    )
    # パラメータを生成して返す
    return AgentCallParameters(
        ModelClass.MAINSTREAM,
        ReasoningEffort.MEDIUM,
        render_as_markdown(prompt),
        Path(__file__).with_suffix(".json"),
    )
