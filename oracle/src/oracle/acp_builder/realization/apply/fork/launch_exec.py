"""`cmoc realization apply fork` の `codex exec` prompt 正本。"""

# std
from pathlib import Path

# cmoc
from oracle.acp_builder.basic import (
    AgentCallParameter,
    FileAccessMode,
    ModelClass,
    ReasoningEffort,
)
from oracle.other.struct_doc import (
    StructBlock,
    StructCodeBlock,
    StructDoc,
    render_as_markdown,
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
        run_worktree: `codex exec` の cwd とする linked worktree。
    """
    # commit 範囲と差分を一意な参照対象にまとめる。
    apply_change = StructBlock(
        "realization_apply_change",
        StructDoc(
            "追従対象変更",
            StructDoc(
                "commit 範囲",
                f"- 始点: `{diff_base_commit}`\n- 終点: `{run_fork_commit}`",
            ),
            StructDoc(
                "oracle file の raw git diff",
                StructCodeBlock("diff", raw_oracle_git_diff),
            ),
        ),
    )

    # 追従対象と完了条件を固定した完全 prompt を構築する。
    complete_prompt = build_complete_prompt(
        role="- あなたは realization file の差分追従担当です",
        summary="""
        - 追従対象変更 <cmoc_ref target="realization_apply_change"/> から読み取れる oracle file の変更を、`{{work-root}}` リポジトリ全体の realization file に反映すること
        - 差分に現れた file だけを作業範囲にせず、関連する oracle file と realization file をリポジトリ全体から調査すること
        """,
        goal="""
        - 追従対象変更 <cmoc_ref target="realization_apply_change"/> から読み取れる変更について、oracle file と realization file の間に齟齬がないこと
        - 関連する既存 oracle file、realization file、standard と論理的に整合していること
        - 必要な realization implementation、realization test、realization ancillary の変更と検証が完了していること
        - realization file が realization standard に従っていること
        - oracle file を変更していないこと
        """,
        file_access_mode=FileAccessMode.REALIZATION_WRITE,
        aux_dynamic_prompt=[apply_change],
        oracle_and_realization_basic=True,
        oracle_standard=True,
        realization_standard=True,
        apply_review_standard=True,
    )

    # リポジトリ全体の追従を 1 agent call へ委ねるため最高品質設定を使う。
    return AgentCallParameter(
        model_class=ModelClass.FLAGSHIP,
        reasoning_effort=ReasoningEffort.MAX,
        file_access_mode=FileAccessMode.REALIZATION_WRITE,
        prompt=render_as_markdown(complete_prompt),
        structured_output_schema_path=None,
        run_indexing_preflight=True,
        cwd=run_worktree.resolve(),
    )
