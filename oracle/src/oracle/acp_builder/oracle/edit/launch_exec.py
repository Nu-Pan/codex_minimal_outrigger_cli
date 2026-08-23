"""`cmoc oracle edit` の 2 回の `codex exec` 起動パラメータ構築定義。"""

# cmoc
from oracle.acp_builder.basic import (
    AgentCallParameter,
    FileAccessMode,
    ModelClass,
    ReasoningEffort,
)
from oracle.other.path_model import AgentCallPathContext, resolve_repo_root
from oracle.other.struct_doc import SDHeader, SDTagBlock, render_sd_node_as_markdown
from oracle.prompt_builder.complete_prompt import build_complete_prompt


def build_oracle_edit_main_launch_exec_parameter(
    user_instruction: str,
) -> AgentCallParameter:
    """`cmoc oracle edit` の本命 agent call 用パラメータを構築する。

    Args:
        user_instruction: oracle file の最終状態に関するユーザー指示。
            エディタへ提示する完全 prompt の skeleton を構築する場合は、
            `{{original-prompt-here}}` を渡す。

    Returns:
        新しい `codex exec` session の初回 call に使う固定パラメータ。
    """
    path_context = AgentCallPathContext(agent_call_cwd=resolve_repo_root())
    complete_prompt = build_complete_prompt(
        summary="""
        - あなたは oracle file の編集担当です
        - オリジナルのユーザー指示 <cmoc_ref target="original_user_instruction"/> が要求する最終状態を `{{work-root}}/oracle` ツリー内の oracle file に反映すること
        """,
        goal="""
        - オリジナルのユーザー指示 <cmoc_ref target="original_user_instruction"/> が要求する最終状態が oracle file 上で満たされていること
        - 関連する oracle file と論理的に整合していること
        - ユーザー指示の実現に必要な箇所以外の既存仕様の意味が維持されていること
        - oracle file だけを編集し、realization file、`INDEX.md`、`AGENTS.md` を編集していないこと
        - `git add`、`git commit`、`git stash`、branch 切替、worktree 操作を行わず、変更を未コミットのまま残していること
        """,
        file_access_mode=FileAccessMode.PURE_ORACLE_WRITE,
        path_context=path_context,
        aux_dynamic_prompt=[
            SDTagBlock(
                "original_user_instruction",
                SDHeader(
                    "ユーザー指示",
                    user_instruction,
                ),
            )
        ],
        oracle_and_realization_basic=True,
        oracle_policy=True,
        routing_policy=True,
    )
    return AgentCallParameter(
        agent_call_kind=build_oracle_edit_main_launch_exec_parameter.__name__,
        model_class=ModelClass.FLAGSHIP,
        reasoning_effort=ReasoningEffort.MAX,
        file_access_mode=FileAccessMode.PURE_ORACLE_WRITE,
        prompt=render_sd_node_as_markdown(*complete_prompt),
        structured_output_schema_path=None,
        agent_call_cwd=path_context.agent_call_cwd,
        run_indexing_preflight=True,
    )


def build_oracle_edit_reduction_launch_exec_parameter(
    user_instruction: str,
) -> AgentCallParameter:
    """本命成功後に実行する仕様削減 agent call 用パラメータを構築する。"""
    path_context = AgentCallPathContext(agent_call_cwd=resolve_repo_root())
    complete_prompt = build_complete_prompt(
        summary="""
        - あなたは oracle file の仕様削減担当です
        - オリジナルのユーザー指示 <cmoc_ref target="original_user_instruction"/>、現在の oracle file、および oracle file に関する現在の Git 未コミット差分を根拠として、過剰な仕様文言の削除、仕様の簡素化、および関連する仕様・規定への違反の修正を行うこと
        """,
        goal="""
        - オリジナルのユーザー指示が要求する人間意図と、実装差を許容しない境界が維持されていること
        - ユーザー指示の対象外である既存仕様の意味が維持されていること
        - 過剰な仕様文言が残らず、関連する oracle file と論理的に整合していること
        - oracle file だけを編集し、realization file、`INDEX.md`、`AGENTS.md` を編集していないこと
        - `git add`、`git commit`、`git stash`、branch 切替、worktree 操作を行わず、変更を未コミットのまま残していること
        """,
        file_access_mode=FileAccessMode.PURE_ORACLE_WRITE,
        path_context=path_context,
        aux_dynamic_prompt=[
            SDTagBlock(
                "original_user_instruction",
                SDHeader(
                    "ユーザー指示",
                    user_instruction,
                ),
            ),
            SDHeader(
                "仕様削減の判断と参照の境界",
                """
                - 直前の本命 agent call が仕様変更を行い、その編集結果は起動前の既存差分と分離されず、現在の Git 未コミット差分に含まれています
                - 本命 agent call が仕様変更を行ったという事実以外の作業経緯は、この agent call に渡されていません
                - 本命成果の参照経路は、現在の oracle file と oracle file に関する現在の Git 未コミット差分だけにして下さい
                - 固定の削減率または文字数目標を設けず、オリジナルのユーザー指示に必要な仕様を基準に判断して下さい
                - 作業に適用できる installed skill は、補助規定として使用して構いません
                - installed skill がこの prompt、オリジナルのユーザー指示、cmoc 固有契約、または関連する oracle file と競合する場合は、installed skill 以外を優先して下さい
                - installed skill の有無を作業完了条件にしてはいけません
                - 本命 agent call の prompt、stdout、stderr、最終回答、call metadata、session ID、およびその他の session log を読んだり、判断根拠にしたりしてはいけません
                - 本命 agent の回答、要約、session ID、および log 内容は、この agent call の入力に含まれていません。それらを探索してはいけません
                """,
            ),
        ],
        oracle_and_realization_basic=True,
        oracle_policy=True,
        routing_policy=True,
    )
    return AgentCallParameter(
        agent_call_kind=build_oracle_edit_reduction_launch_exec_parameter.__name__,
        model_class=ModelClass.FLAGSHIP,
        reasoning_effort=ReasoningEffort.MAX,
        file_access_mode=FileAccessMode.PURE_ORACLE_WRITE,
        prompt=render_sd_node_as_markdown(*complete_prompt),
        structured_output_schema_path=None,
        agent_call_cwd=path_context.agent_call_cwd,
        # NOTE 本命実行と条件を揃えたいので indexing は無し
        run_indexing_preflight=False,
    )
