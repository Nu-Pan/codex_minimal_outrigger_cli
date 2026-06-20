# cmoc
from basic.struct_doc import StructDoc, StructCodeBlock, render_as_markdown
from basic.path_model import resolve_repo_root
from basic.acp import (
    AgentCallParameter,
    ModelClass,
    ReasoningEffort,
    FileAccessMode,
)
from acp.prompt_parts.complete_prompt import build_complete_prompt


def build_apply_fork_consume_fixing_point_parameter(
    fixing_point: str,
) -> AgentCallParameter:
    """
    `cmoc apply fork` サブコマンドの「要修正点対応作業用」の agent call パラメータを構築する

    fixing_point: str
        対応対象の要修正点。
    """
    # パス
    repo_root = resolve_repo_root()
    # プロンプト
    prompt = build_complete_prompt(
        role="- あなたはソフトウェア実装の修正担当です",
        summary=f"- `{repo_root}` ツリー内の realization file を修正すること",
        goal="""
        - 要修正点として指摘されている問題の修正作業をベストエフォートで実施したこと
        - 修正後の realization file が realization standard に従っている事
        """,
        file_access_mode=FileAccessMode.REALIZATION_WRITE,
        aux_prompt=[
            StructDoc(
                "作業上の注意点",
                """
                - 要修正点情報は作業のためのヒントであり、絶対に従うべき指示書ではない
                - git add と git commit は実行禁止
                """,
            ),
            StructDoc("要修正点", StructCodeBlock("text", fixing_point)),
        ],
        oracle_and_realization_basic=True,
        realization_standard=True,
    )
    # パラメータを生成して返す
    return AgentCallParameter(
        ModelClass.MAINSTREAM,
        ReasoningEffort.MEDIUM,
        FileAccessMode.REALIZATION_WRITE,
        render_as_markdown(prompt),
        None,
    )
