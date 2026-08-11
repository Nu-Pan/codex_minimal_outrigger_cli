"""refactor fork の変更要約用 prompt 文面と起動パラメータの構築定義。"""

# std
from pathlib import Path

# cmoc
from oracle.acp_builder.basic import (
    AgentCallParameter,
    FileAccessMode,
    ModelClass,
    ReasoningEffort,
)
from oracle.other.path_model import AgentCallPathContext
from oracle.other.struct_doc import StructCodeBlock, StructDoc, render_as_markdown
from oracle.prompt_builder.complete_prompt import build_complete_prompt


def build_realization_refactor_fork_change_summary_parameter(
    raw_git_diff: str,
    run_worktree: Path,
) -> AgentCallParameter:
    """refactor fork report 用の変更要約パラメータを構築する。

    Args:
        raw_git_diff: run branch 上の refactor 作業差分。
        run_worktree: AgentCallParameter.agent_call_cwd とする linked worktree。
    """
    # run worktree を agent_call_cwd として先に確定する
    path_context = AgentCallPathContext(agent_call_cwd=run_worktree)

    # 確定済み差分だけを入力とする変更要約 prompt を構築する。
    prompt = build_complete_prompt(
        role="- あなたはソフトウェア変更内容の要約担当です",
        summary="""
        - `{{work-root}}` ツリー内の refactor 差分を、人間が読むために要約すること
        """,
        goal="""
        - 指定された Structured Output schema に従って変更要約を返すこと
        """,
        file_access_mode=FileAccessMode.READONLY,
        path_context=path_context,
        aux_dynamic_prompt=[
            StructDoc(
                "run branch 上の refactor 差分",
                StructCodeBlock("diff", raw_git_diff),
            ),
        ],
        routing_rule=False,
    )

    # report 用の分類は品質より経済性を優先する。
    return AgentCallParameter(
        agent_call_kind=(
            build_realization_refactor_fork_change_summary_parameter.__name__
        ),
        model_class=ModelClass.EFFICIENCY,
        reasoning_effort=ReasoningEffort.MEDIUM,
        file_access_mode=FileAccessMode.READONLY,
        prompt=render_as_markdown(prompt),
        structured_output_schema_path=Path(__file__).with_suffix(".json"),
        agent_call_cwd=path_context.agent_call_cwd,
        run_indexing_preflight=True,
    )
