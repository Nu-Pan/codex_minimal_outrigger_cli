"""`cmoc review oracle` の所見擁護理由列挙 prompt 正本。"""

# std
from pathlib import Path

# cmoc
from utils.struct_doc import render_as_markdown
from utils.path_model import resolve_real_path
from agent_call_parameter.base import (
    AgentCallParameters,
    ModelClass,
    ReasoningEffort,
    FileAccessMode,
)
from agent_call_parameter.prompt_parts.complete_prompt import build_complete_prompt


def build_review_oracle_validate_finding_advocate_parameter(
    finding: str,
    known_advocate_reasons: str,
    known_challenger_reasons: str,
) -> AgentCallParameters:
    """
    `cmoc review oracle` サブコマンド、所見が妥当である理由の列挙用。
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
        "- あなたはソフトウェア仕様断片レビュー所見の擁護担当です",
        f"""
        - `{oracle_root}` ツリー内の oracle file を根拠に、対象所見が妥当である理由を調査すること
        - 対象所見は以下である

        ```text
        {finding}
        ```

        - 既知の妥当である理由は以下である

        ```text
        {known_advocate_reasons}
        ```

        - 既知の妥当ではない理由は以下である

        ```text
        {known_challenger_reasons}
        ```
        """,
        """
        - 対象所見が妥当である新規理由だけを列挙すること
        - 具体的な根拠を必ず示し、「かもしれない」「可能性がある」は根拠にしないこと
        - 既知理由と重複する理由が無い場合は空配列を返すこと
        """,
        FileAccessMode.PURE_ORACLE_READ,
        oracle_standard=True,
        structured_output=True,
    )
    # パラメータを生成して返す
    return AgentCallParameters(
        ModelClass.MAINSTREAM,
        ReasoningEffort.MEDIUM,
        FileAccessMode.PURE_ORACLE_READ,
        render_as_markdown(prompt),
        Path(__file__).with_suffix(".json"),
    )
