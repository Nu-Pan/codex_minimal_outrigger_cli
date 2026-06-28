"""`cmoc apply fork` の変更要約生成 builder。"""

from pathlib import Path

from acp.builder.apply.fork._common import (
    ensure_oracle_src_importable,
    resolve_repo_root,
)
from basic.acp import (
    AgentCallParameter,
    FileAccessMode,
    ModelClass,
    ReasoningEffort,
)


def build_apply_fork_change_summary_parameter(raw_git_diff: str) -> AgentCallParameter:
    """作業レポート用の変更要約 agent call parameter を構築する。"""
    # `<work-root>/oracle/src/oracle/acp_builder/apply/fork/change_summary.py`
    # is the canonical fragment. Prompt standards are owned by oracle/src, so
    # this builder loads that source of truth only at construction time.
    return AgentCallParameter(
        ModelClass.EFFICIENCY,
        ReasoningEffort.MEDIUM,
        FileAccessMode.READONLY,
        _prompt(raw_git_diff),
        Path(__file__).with_suffix(".json"),
    )


def _prompt(raw_git_diff: str) -> str:
    repo_root = resolve_repo_root()
    ensure_oracle_src_importable(repo_root)

    from oracle.acp_builder.basic import FileAccessMode as OracleFileAccessMode
    from oracle.other.struct_doc import StructCodeBlock, StructDoc, render_as_markdown
    from oracle.prompt_builder.complete_prompt import build_complete_prompt

    prompt = build_complete_prompt(
        role="- あなたはソフトウェア変更内容の要約担当です",
        summary="""
        - `<repo-root>` ツリー内の差分を、人間が読む用に要約すること
        """,
        goal="""
        - `<repo-root>` ツリー内の差分を、指定の Structured Output schema に従って返却すること
        """,
        file_access_mode=OracleFileAccessMode.READONLY,
        aux_dynamic_prompt=[
            StructDoc("ツリー内の差分", StructCodeBlock("diff", raw_git_diff)),
        ],
        aux_placeholder_def={"repo-root": repo_root},
        oracle_and_realization_basic=True,
    )
    return render_as_markdown(prompt)
