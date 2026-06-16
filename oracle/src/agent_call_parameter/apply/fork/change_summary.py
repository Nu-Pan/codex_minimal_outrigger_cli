"""`cmoc apply fork` の変更要約生成 prompt 正本。"""

# std
from pathlib import Path

# cmoc
from utils.struct_doc import render_as_markdown
from utils.path_model import resolve_repo_root
from agent_call_parameter.base import AgentCallParameters, ModelClass, ReasoningEffort
from prompt_parts.complete_prompt import build_complete_prompt


def build_apply_fork_change_summary_parameter(
    diff_summary: str,
) -> AgentCallParameters:
    """
    `cmoc apply fork` サブコマンド、作業レポート用変更要約生成。
    AI エージェント呼び出しパラメータを構築する。

    diff_summary: str
        `<cmoc-apply-branch>` 上の差分情報。
    """
    # パス
    repo_root = resolve_repo_root()
    # プロンプト
    prompt = build_complete_prompt(
        "- あなたはソフトウェア変更内容の要約担当です",
        f"""
        - `{repo_root}` ツリー内の変更内容を、人間向け作業レポートに使える形で要約すること
        - 差分情報は以下である

        ```text
        {diff_summary}
        ```
        """,
        """
        - 変更内容を意味論に基づくカテゴリへ分けること
        - 各カテゴリで何をどう変えたかを要約すること
        - 主要な変更ファイルを changed_paths に列挙すること
        """,
        "readonly",
        oracle_standard=True,
        realization_standard=True,
        structured_output=True,
    )
    # パラメータを生成して返す
    return AgentCallParameters(
        ModelClass.EFFICIENCY,
        ReasoningEffort.MEDIUM,
        render_as_markdown(prompt),
        Path(__file__).with_suffix(".json"),
    )
