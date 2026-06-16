"""`cmoc review oracle` の所見採否判定 prompt 正本。"""

# std
from pathlib import Path

# cmoc
from utils.struct_doc import render_as_markdown
from utils.path_model import resolve_real_path
from agent_call_parameter.base import AgentCallParameters, ModelClass, ReasoningEffort
from prompt_parts.complete_prompt import build_complete_prompt


def build_review_oracle_judge_finding_parameter(
    finding: str,
    advocate_reasons: str,
    challenger_reasons: str,
) -> AgentCallParameters:
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
    # パス
    oracle_root = resolve_real_path(Path("<work-root>/oracle"))
    # プロンプト
    prompt = build_complete_prompt(
        "- あなたはソフトウェア仕様断片レビュー所見の採否判定担当です",
        f"""
        - `{oracle_root}` ツリー内の oracle file を根拠に、対象所見を人間へ提示すべきか判定すること
        - 対象所見は以下である

        ```text
        {finding}
        ```

        - 所見が妥当である理由は以下である

        ```text
        {advocate_reasons}
        ```

        - 所見が妥当ではない理由は以下である

        ```text
        {challenger_reasons}
        ```
        """,
        """
        - 人間に要確認項目として提示すべき所見なら accept と判定すること
        - 提示すべきではない所見なら reject と判定すること
        - 判定理由は具体的に書くこと
        """,
        "pure_oracle_read",
        oracle_standard=True,
        structured_output=True,
    )
    # パラメータを生成して返す
    return AgentCallParameters(
        ModelClass.FLAGSHIP,
        ReasoningEffort.HIGH,
        render_as_markdown(prompt),
        Path(__file__).with_suffix(".json"),
    )
