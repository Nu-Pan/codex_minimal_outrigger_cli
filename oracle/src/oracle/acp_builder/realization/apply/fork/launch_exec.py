"""`cmoc realization apply fork` の prompt 文面と起動パラメータの構築定義。"""

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
from oracle.other.struct_doc import (
    SDCodeBlock,
    SDHeader,
    SDTagBlock,
    render_sd_node_as_markdown,
)
from oracle.prompt_builder.complete_prompt import build_complete_prompt


def build_realization_apply_fork_launch_exec_parameter(
    diff_base_commit: str,
    run_fork_commit: str,
    raw_oracle_git_diff: str,
    run_worktree: Path,
) -> AgentCallParameter:
    """差分駆動の realization 追従用 AgentCallParameter を構築する。

    Args:
        diff_base_commit: 追従対象差分の始点 commit。
        run_fork_commit: 追従対象差分の終点である run fork commit。
        raw_oracle_git_diff: 始点と終点の間にある oracle file の raw git diff。
        run_worktree: AgentCallParameter.agent_call_cwd とする linked worktree。
    """
    # commit 範囲と差分を一意な参照対象にまとめる。
    apply_change = SDTagBlock(
        "realization_apply_change",
        SDHeader(
            "追従対象変更",
            SDHeader(
                "commit 範囲",
                f"- 始点: `{diff_base_commit}`\n- 終点: `{run_fork_commit}`",
            ),
            SDHeader(
                "oracle file の raw git diff",
                SDCodeBlock("diff", raw_oracle_git_diff),
            ),
        ),
    )
    # パラメータを生成
    path_context = AgentCallPathContext(agent_call_cwd=run_worktree)
    complete_prompt = build_complete_prompt(
        summary="""
        - あなたは realization file の差分追従担当です
        - 追従対象変更 <cmoc_ref target="realization_apply_change"/> から読み取れる oracle file の変更を、`{{work-root}}` リポジトリ全体の realization file に反映すること
        - 差分に現れた file だけを作業範囲にせず、関連する oracle file と realization file をリポジトリ全体から調査すること
        """,
        goal="""
        - 追従対象変更 <cmoc_ref target="realization_apply_change"/> から読み取れる変更について、oracle file と realization file の間に齟齬がないこと
        - 関連する既存 oracle file と realization file に論理的に整合していること
        - 必要な realization implementation、realization test、realization ancillary の変更と検証が完了していること
        - oracle file を変更していないこと
        """,
        file_access_mode=FileAccessMode.REALIZATION_WRITE,
        path_context=path_context,
        aux_dynamic_prompt=[apply_change],
        oracle_and_realization_basic=True,
        oracle_policy=True,
        realization_policy=True,
        realization_findings_policy=True,
        routing_policy=True,
    )
    return AgentCallParameter(
        agent_call_kind=build_realization_apply_fork_launch_exec_parameter.__name__,
        model_class=ModelClass.FLAGSHIP,
        reasoning_effort=ReasoningEffort.MAX,
        file_access_mode=FileAccessMode.REALIZATION_WRITE,
        prompt=render_sd_node_as_markdown(*complete_prompt),
        structured_output_schema_path=None,
        agent_call_cwd=path_context.agent_call_cwd,
        run_indexing_preflight=True,
    )
