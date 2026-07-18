"""`cmoc realization apply fork` の TUI 起動 prompt 正本。"""

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


def build_realization_apply_fork_launch_tui_parameter(
    time_stamp: str,
    diff_base_commit: str,
    oracle_snapshot_commit: str,
    raw_oracle_git_diff: str,
) -> AgentCallParameter:
    """差分駆動の realization 追従 TUI パラメータを構築する。

    Args:
        time_stamp: この fork 呼び出しのタイムスタンプ。
        diff_base_commit: 追従対象差分の始点 commit。
        oracle_snapshot_commit: 追従対象差分の終点 commit。
        raw_oracle_git_diff: 始点と終点の間にある oracle file の raw git diff。
    """
    # 追従対象と完了条件を固定した完全プロンプトを構築する。
    complete_prompt = build_complete_prompt(
        role="- あなたは realization file の差分追従担当です",
        summary="""
        - 後述する commit 差分から読み取れる oracle file の変更を、`{{work-root}}` リポジトリ全体の realization file に反映すること
        - 差分に現れた file だけを作業範囲にせず、関連する oracle file と realization file をリポジトリ全体から調査すること
        """,
        goal="""
        - 注入された commit 差分から読み取れる変更について、oracle file と realization file の間に齟齬がないこと
        - 関連する既存 oracle file、realization file、standard と論理的に整合していること
        - 必要な realization implementation、realization test、realization ancillary の変更と検証が完了していること
        - realization file が realization standard に従っていること
        - oracle file を変更していないこと
        """,
        file_access_mode=FileAccessMode.REALIZATION_WRITE,
        aux_dynamic_prompt=[
            StructDoc(
                "追従対象 commit 範囲",
                f"- 始点: `{diff_base_commit}`\n- 終点: `{oracle_snapshot_commit}`",
            ),
            StructDoc(
                "追従対象差分",
                StructCodeBlock("diff", raw_oracle_git_diff),
            ),
        ],
        oracle_and_realization_basic=True,
        oracle_standard=True,
        realization_standard=True,
        apply_review_standard=True,
    )

    # main worktree 側の TUI ログへ完全プロンプトを保存する。
    complete_prompt_path = (
        resolve_repo_root()
        / ".cmoc"
        / "gu"
        / "ar"
        / "log"
        / "editor_input"
        / f"{time_stamp}_cmpl.md"
    )
    with open(complete_prompt_path, "w", encoding="utf-8") as file:
        file.write(render_as_markdown(complete_prompt))

    # リポジトリ全体の追従を 1 セッションへ委ねるため最高品質設定を使う。
    return AgentCallParameter(
        model_class=ModelClass.FLAGSHIP,
        reasoning_effort=ReasoningEffort.MAX,
        file_access_mode=FileAccessMode.REALIZATION_WRITE,
        prompt=f"{complete_prompt_path} を読んで、その指示に従って下さい",
        structured_output_schema_path=None,
        run_indexing_preflight=True,
    )
