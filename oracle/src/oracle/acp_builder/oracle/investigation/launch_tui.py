"""`cmoc oracle investigation` の prompt 文面と TUI 起動パラメータの構築定義。"""

# cmoc
from oracle.acp_builder.basic import (
    AgentCallParameter,
    FileAccessMode,
    ModelClass,
    ReasoningEffort,
)
from oracle.other.path_model import AgentCallPathContext, resolve_repo_root
from oracle.other.struct_doc import StructBlock, StructDoc, render_as_markdown
from oracle.prompt_builder.complete_prompt import build_complete_prompt


def build_oracle_investigation_launch_tui_parameter(
    time_stamp: str,
    user_instruction: str,
) -> AgentCallParameter:
    """`cmoc oracle investigation` の TUI 起動パラメータを構築する。

    Args:
        time_stamp: この `cmoc oracle investigation` 呼び出しのタイムスタンプ文字列。
        user_instruction: ユーザーがエディタ入力した、oracle file に関する調査指示。
            コメント除去と strip は呼び出し側で完了している想定。エディタへ提示する
            完全プロンプトの skeleton を構築する場合は、
            `{{original-prompt-here}}` を渡す。

    Returns:
        Codex CLI の TUI 起動に使う固定パラメータ。
    """
    # main worktree を agent_call_cwd として先に確定する
    path_context = AgentCallPathContext(agent_call_cwd=resolve_repo_root())

    # ユーザー指示以外を固定した完全プロンプトを構築する
    complete_prompt = build_complete_prompt(
        role="- あなたは oracle file の調査担当です",
        summary="""
        - オリジナルのユーザー指示 <cmoc_ref target="original_user_instruction"/> が要求する調査を `{{work-root}}/oracle` ツリー内の oracle file に基づいて行い、結果をユーザーへ回答すること
        """,
        goal="""
        - ユーザー指示が要求する調査が完了し、その結果が回答されていること
        - 調査結果の根拠となる oracle file を回答から特定できること
        - oracle file で定義されている事項と未定義の事項を混同せず、未定義の事項を正本仕様として断定していないこと
        """,
        file_access_mode=FileAccessMode.PURE_ORACLE_READ,
        path_context=path_context,
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

    # cmoc が管理する TUI ログへ完全プロンプトを保存する
    complete_prompt_path = (
        path_context.repo_root
        / ".cmoc"
        / "gu"
        / "ar"
        / "log"
        / "editor_input"
        / f"{time_stamp}_cmpl.md"
    )
    with open(complete_prompt_path, "w", encoding="utf-8") as f:
        f.write(render_as_markdown(complete_prompt))

    # TUI を起動する
    return AgentCallParameter(
        agent_call_kind=build_oracle_investigation_launch_tui_parameter.__name__,
        model_class=ModelClass.FLAGSHIP,
        reasoning_effort=ReasoningEffort.MAX,
        file_access_mode=FileAccessMode.PURE_ORACLE_READ,
        prompt=f"{complete_prompt_path} を読んで、その指示に従って下さい",
        structured_output_schema_path=None,
        agent_call_cwd=path_context.agent_call_cwd,
        run_indexing_preflight=True,
    )
