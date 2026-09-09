"""refactor fork の変更要約用 prompt 文面と起動パラメータの構築定義。"""

# std
from pathlib import Path

# cmoc
from oracle.acp_builder.basic import (
    AgentCallParameter,
    FileAccessMode,
)
from oracle.other.path_model import AgentCallPathContext
from oracle.other.struct_doc import (
    SDHeader,
    render_sd_node_as_markdown,
)
from oracle.prompt_builder.complete_prompt import build_complete_prompt


def build_realization_refactor_fork_change_summary_parameter(
    run_fork_commit: str,
    summary_head_commit: str,
    run_worktree: Path,
) -> AgentCallParameter:
    """refactor fork report 用の変更要約パラメータを構築する。

    Args:
        run_fork_commit: 要約対象差分の始点である run fork commit ID。
        summary_head_commit: 要約対象の確定時点における run branch HEAD の commit ID。
        run_worktree: AgentCallParameter.agent_call_cwd とする linked worktree。
    """
    path_context = AgentCallPathContext(agent_call_cwd=run_worktree)
    prompt = build_complete_prompt(
        task="""
        - 指定された commit 範囲の tree 差分全体を Git から取得し、人間が読むために要約すること
        """,
        file_access_mode=FileAccessMode.READONLY,
        path_context=path_context,
        aux_static_prompt=[
            SDHeader(
                "要約対象差分の取得",
                """
                - cwd と `{{work-root}}` が示す repository で、指定された始点・終点の commit 間の差分を Git から取得すること
                - 現在の HEAD、branch 名、または未コミット編集によって比較範囲を動かさないこと
                - 差分を取得できない場合は失敗として報告し、正常に取得できた空差分として扱わないこと
                """,
            ),
        ],
        aux_dynamic_prompt=[
            SDHeader(
                "要約対象の commit 範囲",
                f"- 始点: `{run_fork_commit}`\n- 終点: `{summary_head_commit}`",
            ),
        ],
        oracle_and_realization_basic=True,
        routing_policy=True,
    )

    return AgentCallParameter(
        agent_call_kind=(
            build_realization_refactor_fork_change_summary_parameter.__name__
        ),
        file_access_mode=FileAccessMode.READONLY,
        prompt=render_sd_node_as_markdown(*prompt),
        structured_output_schema_path=Path(__file__).with_suffix(".json"),
        agent_call_cwd=path_context.agent_call_cwd,
        run_indexing_preflight=True,
    )
