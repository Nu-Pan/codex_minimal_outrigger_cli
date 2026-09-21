"""`cmoc oracle edit` の共通編集パラメータ構築定義。

意味仕様は `{{cmoc-root}}/oracle/doc/app_spec/sub_command/oracle_edit.md` の
「ユーザー指示と prompt の構築」「編集目的と判断材料」「実行順序」
および「agent の編集境界」を参照する。
"""

# cmoc
from oracle.acp_builder.basic import (
    AgentCallParameter,
    FileAccessMode,
)
from oracle.other.path_model import AgentCallPathContext, resolve_repo_root
from oracle.other.struct_doc import SDHeader, SDTagBlock, render_sd_node_as_markdown
from oracle.prompt_builder.complete_prompt import build_complete_prompt


def build_oracle_edit_main_launch_exec_parameter(
    user_instruction: str,
) -> AgentCallParameter:
    """`cmoc oracle edit` の両回で共用するパラメータを構築する。

    Args:
        user_instruction: oracle file の最終状態に関する、入力確定済みのユーザー指示。
            handoff ガイドへ提示する完全 prompt の skeleton を構築する場合は、
            `{{original-prompt-here}}` を渡す。

    Returns:
        新しい `codex exec` session の初回 call に使う固定パラメータ。
    """
    # main worktree の path context と、現在状態から判断する共通 prompt を構築する。
    path_context = AgentCallPathContext(agent_call_cwd=resolve_repo_root())
    complete_prompt = build_complete_prompt(
        task="""
        - オリジナルのユーザー指示 <cmoc_ref target="original_user_instruction"/> から導かれる目標状態を、現在の `{{work-root}}/oracle` 内の oracle file が満たすように編集すること
        """,
        scope="""
        - オリジナルのユーザー指示、現在の関連 oracle file、および oracle file に関する現在の Git 未コミット差分を照合し、目標状態との差を判断すること
        - 作業範囲は、目標状態の達成に必要な関連仕様のまとまりとすること
        """,
        completion_criteria="""
        - 関連する oracle file が、オリジナルのユーザー指示から導かれる目標状態を満たしていること。既に満たしている場合は、追加変更なしで完了してよい
        """,
        file_access_mode=FileAccessMode.PURE_ORACLE_WRITE,
        path_context=path_context,
        aux_static_prompt=[
            SDHeader(
                "変更操作の制約",
                """
                - `git add`、`git commit`、`git stash`、branch 切替、および worktree 操作を行わないこと
                - 変更を未コミットのまま残すこと
                """,
            ),
            SDHeader(
                "編集の判断条件",
                """
                - 指示に明記された箇所や既に差分がある箇所だけに編集を限定せず、目標状態の達成に必要な追加・削除・統合・再構成を選ぶこと
                - ユーザー指示が要求する人間意図と実装差を許容しない境界を満たし、対象外の既存仕様の意味を維持すること
                - 未コミット差分は起動前からの変更も含み得る判断材料であり、完成済みの成果や今回の呼び出しだけに由来する成果とはみなさないこと
                - 差分を取得できない場合は、空差分として扱わず取得失敗として報告すること
                """,
            ),
        ],
        aux_dynamic_prompt=[
            SDTagBlock(
                "original_user_instruction",
                SDHeader(
                    "ユーザー指示",
                    user_instruction,
                ),
            ),
            SDHeader(
                "未コミット差分の参照情報",
                """
                - `{{work-root}}` の Git worktree で、oracle file に関する現在の未コミット差分を取得すること。staging area、working tree、および Git 未追跡の新規 oracle file の状態を含めること
                """,
            ),
        ],
        oracle_and_realization_basic=True,
        oracle_policy=True,
        routing_policy=True,
    )
    # indexing は呼び出し元が編集の外側で管理するため、自動 preflight を無効にする。
    return AgentCallParameter(
        agent_call_kind=build_oracle_edit_main_launch_exec_parameter.__name__,
        file_access_mode=FileAccessMode.PURE_ORACLE_WRITE,
        prompt=render_sd_node_as_markdown(*complete_prompt),
        structured_output_schema_path=None,
        agent_call_cwd=path_context.agent_call_cwd,
        run_indexing_preflight=False,
    )
