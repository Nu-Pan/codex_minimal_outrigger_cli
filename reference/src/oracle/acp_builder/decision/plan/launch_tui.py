"""oracle 調査 TUI の初回 exec・対話再開パラメータの構築定義。"""

# cmoc
from oracle.acp_builder.basic import (
    AgentCallParameter,
    FileAccessMode,
    TuiResumeTarget,
)
from oracle.other.path_model import AgentCallPathContext, resolve_repo_root
from oracle.other.struct_doc import SDHeader, SDTagBlock, render_sd_node_as_markdown
from oracle.prompt_builder.complete_prompt import build_complete_prompt


def build_decision_plan_request(
    user_instruction: str | None = None,
    *,
    resume: TuiResumeTarget | None = None,
) -> AgentCallParameter:
    """`cmoc decision plan` 用の agent call リクエストを構築する

    1 ターン目の exec リクエストと、2 ターン目移行用の TUI resume リクエスト両方をこの関数で構築する。

    Args:
        user_instruction:
            ユーザーがエディタから入力した指示。
            ユーザーの「ああしたい、こうしたい」が渡される。
            前後空白の strip は呼び出し側で完了している想定。
            handoff ガイドへ提示する完全プロンプトの skeleton を構築する場合は、
            `{{original-prompt-here}}` を渡す。再開時は指定しない。
            `resume` とは排他。
        resume:
            起動管理側が内部の自動移行または公開 `cmoc resume` の条件で検査した会話 ID と保存済み cwd。
            `user_instruction` とは排他。

    Returns:
        同じ workload の制約を持つ、初回 exec または prompt 不在の対話再開の
        パラメータ。process の起動・移行制御は含まない。

    Raises:
        ValueError: 新規入力と再開先の両方、またはどちらも指定されていない。
    """
    # 必要なパラメータを初期化
    # NOTE
    #   「新規セッション」「既存セッション再開」で必要な処理が異なる
    if (user_instruction is None) == (resume is None):
        raise ValueError("specify exactly one of user_instruction and resume")
    elif user_instruction is not None:
        path_context = AgentCallPathContext(agent_call_cwd=resolve_repo_root())
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
            file_access_mode=FileAccessMode.DECISION_PLAN,
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
            cmoc_basic_instruction=True,
            routing_policy=True,
            editor_input_handoff_policy=True,
        )
        prompt = render_sd_node_as_markdown(*complete_prompt)
    elif resume is not None:
        path_context = AgentCallPathContext(agent_call_cwd=resume.agent_call_cwd)
        prompt = None
    else:
        raise RuntimeError("Unexpected control path")
    # 正常終了
    return AgentCallParameter(
        agent_call_kind=build_decision_plan_request.__name__,
        file_access_mode=FileAccessMode.DECISION_PLAN,
        prompt=prompt,
        structured_output_schema_path=None,
        agent_call_cwd=path_context.agent_call_cwd,
        enable_editor_input_handoff_mcp=True,
        enable_document_search_mcp=True,
        tui_resume_session_id=None if resume is None else resume.codex_session_id,
    )
