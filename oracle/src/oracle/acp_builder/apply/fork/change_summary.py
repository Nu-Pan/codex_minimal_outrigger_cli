"""`cmoc apply fork` の変更要約生成 prompt 正本。"""

# std
from pathlib import Path

# cmoc
from oracle.other.file_access_profile import build_faprofile
from oracle.other.struct_doc import StructDoc, StructCodeBlock, render_as_markdown
from oracle.other.path_model import resolve_repo_root
from oracle.acp_builder.basic import (
    AgentCallParameter,
    ModelClass,
    ReasoningEffort,
)
from oracle.prompt_builder.complete_prompt import build_complete_prompt


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
    # ファイルアクセスプロファイル
    faprofile = build_faprofile(
        oracle="read",
        realization="read",
        index="read",
    )
    # プロンプト
    prompt = build_complete_prompt(
        role="- あなたはソフトウェア変更内容の要約担当です",
        summary="""
        - `<repo-root>` ツリー内の差分を、人間が読む用に要約すること
        """,
        goal="""
        - `<repo-root>` ツリー内の差分を、指定の Structured Output schema に従って返却すること
        """,
        faprofile=faprofile,
        aux_dynamic_prompt=[
            StructDoc(
                "ツリー内の差分",
                StructCodeBlock(
                    "diff",
                    raw_git_diff,
                ),
            ),
        ],
        aux_placeholder_def={
            "repo-root": resolve_repo_root(),
        },
        oracle_and_realization_basic=True,
    )
    # パラメータを生成して返す
    return AgentCallParameter(
        ModelClass.EFFICIENCY,
        ReasoningEffort.MEDIUM,
        faprofile,
        render_as_markdown(prompt),
        Path(__file__).with_suffix(".json"),
    )
