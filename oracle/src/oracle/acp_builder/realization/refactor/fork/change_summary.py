"""`cmoc realization refactor fork` の変更要約生成 prompt 正本。"""

# std
from pathlib import Path

# cmoc
from oracle.acp_builder.basic import (
    AgentCallParameter,
    FileAccessMode,
    ModelClass,
    ReasoningEffort,
)
from oracle.other.path_model import resolve_repo_root
from oracle.other.struct_doc import StructCodeBlock, StructDoc, render_as_markdown
from oracle.prompt_builder.complete_prompt import build_complete_prompt


def build_realization_refactor_fork_change_summary_parameter(
    raw_git_diff: str,
) -> AgentCallParameter:
    """refactor fork report 用の変更要約パラメータを構築する。

    Args:
        raw_git_diff: refactor branch 上の作業差分。
    """
    # 確定済み差分だけを入力とする変更要約 prompt を構築する。
    prompt = build_complete_prompt(
        role="- あなたはソフトウェア変更内容の要約担当です",
        summary="""
        - `{{repo-root}}` ツリー内の refactor 差分を、人間が読むために要約すること
        """,
        goal="""
        - 指定された Structured Output schema に従って変更要約を返すこと
        """,
        file_access_mode=FileAccessMode.READONLY,
        aux_dynamic_prompt=[
            StructDoc(
                "refactor branch 上の差分",
                StructCodeBlock("diff", raw_git_diff),
            ),
        ],
        aux_placeholder_def={
            "repo-root": resolve_repo_root(),
        },
        oracle_and_realization_basic=True,
    )

    # report 用の分類は品質より経済性を優先する。
    return AgentCallParameter(
        model_class=ModelClass.EFFICIENCY,
        reasoning_effort=ReasoningEffort.MEDIUM,
        file_access_mode=FileAccessMode.READONLY,
        prompt=render_as_markdown(prompt),
        structured_output_schema_path=Path(__file__).with_suffix(".json"),
        run_indexing_preflight=True,
    )
