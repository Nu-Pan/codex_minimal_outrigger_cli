"""oracle 調査 TUI の新規起動・対話再開パラメータの構築定義。"""

# cmoc
from oracle.acp_builder.basic import (
    AgentCallParameter,
    FileAccessMode,
    TuiResumeTarget,
)
from oracle.other.path_model import AgentCallPathContext, resolve_repo_root
from oracle.other.struct_doc import SDHeader, SDTagBlock, render_sd_node_as_markdown
from oracle.prompt_builder.complete_prompt import build_complete_prompt


def build_oracle_investigation_launch_tui_parameter(
    user_instruction: str | None = None,
    *,
    resume: TuiResumeTarget | None = None,
) -> AgentCallParameter:
    """oracle 調査 TUI の新規入力か、検査済みの再開先の一方を受け取る。

    Args:
        user_instruction: ユーザーがエディタ入力した、oracle file に関する調査指示。
            前後空白の strip は呼び出し側で完了している想定。handoff ガイドへ提示する
            完全プロンプトの skeleton を構築する場合は、
            `{{original-prompt-here}}` を渡す。再開時は指定しない。
        resume: `cmoc resume` が検査した会話 ID と保存済み cwd。

    Returns:
        同じ workload の設定を持つ、新規起動または対話再開のパラメータ。

    Raises:
        ValueError: 新規入力と再開先の両方、またはどちらも指定されていない。
    """
    if (user_instruction is None) == (resume is None):
        raise ValueError("specify exactly one of user_instruction and resume")
    path_context = AgentCallPathContext(
        agent_call_cwd=(
            resolve_repo_root() if resume is None else resume.agent_call_cwd
        )
    )
    prompt = None
    if user_instruction is not None:
        complete_prompt = build_complete_prompt(
            task="""
            - オリジナルのユーザー指示 <cmoc_ref target="original_user_instruction"/> が要求する事項を調査し、結果を回答すること
            """,
            scope="""
            - `{{work-root}}/oracle` ツリー内の関連する oracle file を根拠とすること
            """,
            completion_criteria="""
            - ユーザー指示が要求する調査結果がユーザーへ回答されていること
            - 調査結果の根拠となる oracle file を回答から特定できること
            """,
            file_access_mode=FileAccessMode.PURE_ORACLE_READ,
            path_context=path_context,
            enable_document_search_mcp=True,
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
            editor_input_handoff_policy=True,
        )
        prompt = render_sd_node_as_markdown(*complete_prompt)
    return AgentCallParameter(
        agent_call_kind=build_oracle_investigation_launch_tui_parameter.__name__,
        file_access_mode=FileAccessMode.PURE_ORACLE_READ,
        prompt=prompt,
        structured_output_schema_path=None,
        agent_call_cwd=path_context.agent_call_cwd,
        enable_editor_input_handoff_mcp=True,
        enable_document_search_mcp=True,
        tui_resume_session_id=None if resume is None else resume.codex_session_id,
    )
