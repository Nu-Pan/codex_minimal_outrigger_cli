"""`cmoc apply fork` の要修正点対応作業 prompt 正本。"""

# std
from pathlib import Path

# cmoc
from basic.struct_doc import render_as_markdown
from basic.path_model import resolve_repo_root
from basic.acp import (
    AgentCallParameter,
    ModelClass,
    ReasoningEffort,
    FileAccessMode,
)
from acp.prompt_parts.complete_prompt import build_complete_prompt


def build_apply_fork_fixing_point_application_parameter(
    fixing_point: str,
) -> AgentCallParameter:
    """
    `cmoc apply fork` サブコマンド、要修正点対応作業用。
    AI エージェント呼び出しパラメータを構築する。

    fixing_point: str
        対応対象の要修正点。
    """
    # パス
    repo_root = resolve_repo_root()
    # プロンプト
    prompt = build_complete_prompt(
        "- あなたはソフトウェア実装の修正担当です",
        f"""
        - `{repo_root}` ツリー内の realization file を修正すること
        - 対応対象の要修正点は以下である

        ```text
        {fixing_point}
        ```
        """,
        """
        - 要修正点として指摘されている問題の修正作業をベストエフォートで行うこと
        - 要修正点情報は作業のためのヒントであり、絶対に従うべき指示書としては扱わないこと
        - git add と git commit は実行しないこと
        """,
        FileAccessMode.REALIZATION_WRITE,
        oracle_standard=True,
        realization_standard=True,
        structured_output=False,
    )
    # パラメータを生成して返す
    return AgentCallParameter(
        ModelClass.MAINSTREAM,
        ReasoningEffort.MEDIUM,
        FileAccessMode.REALIZATION_WRITE,
        render_as_markdown(prompt),
        None,
    )
