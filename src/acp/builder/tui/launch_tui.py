"""TUI 起動 parameter builder の realization 側互換入口。

oracle 側の builder は prompt 構築を正本として使うが、実行時の保存先は
realization runtime の `.cmoc/local` 配置に従う。
"""

from oracle.acp_builder.basic import (
    AgentCallParameter,
    FileAccessMode,
    ModelClass,
    ReasoningEffort,
)
from oracle.other.path_model import resolve_repo_root
from oracle.other.struct_doc import StructDoc, render_as_markdown
from oracle.prompt_builder.complete_prompt import build_complete_prompt

from commons.runtime_paths import logs_dir


def build_tui_launch_tui_parameter(
    time_stamp: str,
    role: str,
    summary: str,
    goal: str,
    file_access_mode: FileAccessMode,
    original_prompt: str,
    oracle_and_realization_basic: bool,
    oracle_standard: bool,
    realization_standard: bool,
    review_oracle_standard: bool,
    apply_review_standard: bool,
    index_entry_standard: bool,
) -> AgentCallParameter:
    """`cmoc tui` の TUI 起動用 AgentCallParameter を構築する。"""
    complete_prompt = build_complete_prompt(
        role=role,
        summary=summary,
        goal=goal,
        file_access_mode=file_access_mode,
        aux_dynamic_prompt=[
            StructDoc(
                "オリジナルプロンプト",
                original_prompt,
            ),
        ],
        oracle_and_realization_basic=oracle_and_realization_basic,
        oracle_standard=oracle_standard,
        realization_standard=realization_standard,
        review_oracle_standard=review_oracle_standard,
        apply_review_standard=apply_review_standard,
        index_entry_standard=index_entry_standard,
    )
    complete_prompt_path = (
        logs_dir(resolve_repo_root()).parent / "tui" / f"{time_stamp}_cmpl.md"
    )
    complete_prompt_path.parent.mkdir(parents=True, exist_ok=True)
    complete_prompt_path.write_text(render_as_markdown(complete_prompt))
    return AgentCallParameter(
        ModelClass.MAINSTREAM,
        ReasoningEffort.MEDIUM,
        file_access_mode,
        f"{complete_prompt_path} を読んで、その指示に従って下さい",
        # <work-root>/oracle/doc/app_spec/sub_command/tui.md: TUI 起動は
        # codex exec ではなく、Structured Output schema を要求しない。
        None,
        True,
    )


__all__ = ["build_tui_launch_tui_parameter"]
