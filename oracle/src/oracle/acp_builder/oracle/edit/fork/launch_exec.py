"""`cmoc oracle edit fork` の `codex exec` prompt 正本。"""

# std
from pathlib import Path

# cmoc
from oracle.acp_builder.basic import (
    AgentCallParameter,
    FileAccessMode,
    ModelClass,
    ReasoningEffort,
)
from oracle.other.struct_doc import StructBlock, StructDoc, render_as_markdown
from oracle.prompt_builder.complete_prompt import build_complete_prompt


def build_oracle_edit_fork_launch_exec_parameter(
    user_instruction: str,
    run_worktree: Path,
) -> AgentCallParameter:
    """oracle edit run の AgentCallParameter を構築する。

    Args:
        user_instruction: oracle file の最終状態に関するユーザー指示。
        run_worktree: `codex exec` の cwd とする linked worktree。
    """
    # ユーザー指示以外を固定した完全 prompt を構築する。
    complete_prompt = build_complete_prompt(
        role="- あなたは oracle file の編集担当です",
        summary="""
        - オリジナルのユーザー指示 <cmoc_ref target="original_user_instruction"/> が要求する最終状態を `{{work-root}}/oracle` ツリー内の oracle file に反映すること
        """,
        goal="""
        - オリジナルのユーザー指示 <cmoc_ref target="original_user_instruction"/> が要求する最終状態が oracle file 上で満たされていること
        - 関連する oracle file と論理的に整合していること
        - ユーザー指示の実現に必要な箇所以外の既存仕様の意味論が維持されていること
        """,
        file_access_mode=FileAccessMode.PURE_ORACLE_WRITE,
        aux_dynamic_prompt=[
            StructBlock(
                "original_user_instruction",
                StructDoc(
                    "ユーザー指示",
                    user_instruction,
                ),
            )
        ],
        oracle_and_realization_basic=True,
        oracle_standard=True,
    )

    # 完全 prompt と run worktree を `codex exec` 用パラメータへ直接設定する。
    return AgentCallParameter(
        model_class=ModelClass.FLAGSHIP,
        reasoning_effort=ReasoningEffort.MAX,
        file_access_mode=FileAccessMode.PURE_ORACLE_WRITE,
        prompt=render_as_markdown(complete_prompt),
        structured_output_schema_path=None,
        run_indexing_preflight=True,
        cwd=run_worktree.resolve(),
    )
