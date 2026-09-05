"""`cmoc realization apply fork` の prompt 文面と起動パラメータの構築定義。"""

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
    SDTagBlock,
    render_sd_node_as_markdown,
)
from oracle.prompt_builder.complete_prompt import build_complete_prompt


def build_realization_apply_fork_launch_exec_parameter(
    diff_base_commit: str,
    run_fork_commit: str,
    run_worktree: Path,
) -> AgentCallParameter:
    """差分駆動の realization 追従用 AgentCallParameter を構築する。

    Args:
        diff_base_commit: 追従対象差分の始点 commit。
        run_fork_commit: 追従対象差分の終点である run fork commit。
        run_worktree: AgentCallParameter.agent_call_cwd とする linked worktree。
    """
    # 確定した commit 範囲を一意な参照対象にまとめる。
    # パラメータを生成
    path_context = AgentCallPathContext(agent_call_cwd=run_worktree)
    complete_prompt = build_complete_prompt(
        task="""
        - 追従対象変更 <cmoc_ref target="realization_apply_change"/> の指定 commit 範囲から読み取れる oracle file の変更を、`{{work-root}}` リポジトリ全体の realization file に反映すること
        """,
        scope="""
        - 差分に現れた file だけを作業範囲にせず、関連する oracle file と realization file をリポジトリ全体から調査すること
        """,
        completion_criteria="""
        - 追従対象変更 <cmoc_ref target="realization_apply_change"/> の指定 commit 範囲から読み取れる oracle 変更について、oracle file と realization file の間に齟齬がないこと
        """,
        file_access_mode=FileAccessMode.REALIZATION_WRITE,
        path_context=path_context,
        aux_static_prompt=[
            SDHeader(
                "追従対象差分の取得方法",
                """
                - cwd と `{{work-root}}` が示す repository で、指定された始点・終点の commit 間の差分を Git から取得すること
                - 両端のいずれかで oracle file だった path を対象に rename を考慮すること。追加・削除と oracle 内外の移動を含め、現在の oracle 配下だけに候補を限定しないこと
                - realization file、`INDEX.md`、その他の非 oracle file の変更だけを理由に追従対象としないこと。ただし、両端での判定と rename の扱いを優先し、oracle 内外の移動を除外しないこと
                - 差分を取得できない場合は失敗として報告し、正常に取得できた空差分として扱わないこと
                """,
            ),
        ],
        aux_dynamic_prompt=[
            SDTagBlock(
                "realization_apply_change",
                SDHeader(
                    "追従対象変更",
                    SDHeader(
                        "commit 範囲",
                        f"- 始点: `{diff_base_commit}`\n- 終点: `{run_fork_commit}`",
                    ),
                ),
            )
        ],
        oracle_and_realization_basic=True,
        realization_policy=True,
        realization_findings_policy=True,
        routing_policy=True,
    )
    return AgentCallParameter(
        agent_call_kind=build_realization_apply_fork_launch_exec_parameter.__name__,
        file_access_mode=FileAccessMode.REALIZATION_WRITE,
        prompt=render_sd_node_as_markdown(*complete_prompt),
        structured_output_schema_path=None,
        agent_call_cwd=path_context.agent_call_cwd,
        run_indexing_preflight=True,
    )
