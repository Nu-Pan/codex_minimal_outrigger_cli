"""`cmoc apply fork` の変更要約生成 prompt 正本。"""

# std
from pathlib import Path

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


def build_apply_fork_change_summary_parameter(
    raw_git_diff: str,
) -> AgentCallParameter:
    """
    `cmoc apply fork` サブコマンド、作業レポート用変更要約生成。
    AI エージェント呼び出しパラメータを構築する。

    raw_git_diff:
        `<cmoc-apply-branch>` 上の変更内容を表す、git コマンド出力そのままの差分テキスト。
        典型的には `git diff` の標準出力を、解析・整形せずに渡す。
    """
    # パス
    repo_root = resolve_repo_root()
    # プロンプト
    prompt = build_complete_prompt(
        role="""
        - あなたはソフトウェア変更内容の要約担当です
        """,
        summary=f"""
        - `{repo_root}` ツリー内の変更内容を、人間向け作業レポートに使える形で要約すること
        """,
        goal="""
        - `{repo_root}` ツリー内の変更内容を、指定の Structured Output schema に従って返却すること
        """,
        file_access_mode=FileAccessMode.READONLY,
        aux_prompt=[
            StructDoc(
                "ツリー内の差分",
                StructCodeBlock(
                    "diff",
                    raw_git_diff,
                ),
            ),
        ],
        oracle_and_realization_basic=True,
    )
    # パラメータを生成して返す
    return AgentCallParameter(
        ModelClass.EFFICIENCY,
        ReasoningEffort.MEDIUM,
        FileAccessMode.READONLY,
        render_as_markdown(prompt),
        Path(__file__).with_suffix(".json"),
    )
