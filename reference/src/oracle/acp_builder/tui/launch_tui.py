"""汎用 TUI の初回 exec・対話再開パラメータの構築定義。"""

# cmoc
from oracle.acp_builder.basic import (
    AgentCallParameter,
    FileAccessMode,
    TuiResumeTarget,
)
from oracle.other.path_model import AgentCallPathContext, resolve_repo_root
from oracle.other.struct_doc import SDHeader, SDTagBlock, render_sd_node_as_markdown
from oracle.prompt_builder.complete_prompt import build_complete_prompt


def build_tui_request(
    original_prompt: str | None = None,
    *,
    resume: TuiResumeTarget | None = None,
) -> AgentCallParameter:
    """初回 exec 用の新規入力か、検査済みの再開先の一方を受け取る。

    Args:
        original_prompt: ユーザーがエディタ入力した、AI Agent CLI/TUI に渡す
            オリジナルプロンプト。前後空白の strip は呼び出し側で完了している
            想定。handoff ガイドへ提示する完全プロンプトの skeleton を構築する場合は、
            `{{original-prompt-here}}` を渡す。再開時は指定しない。
        resume: 起動管理側が内部の自動移行または公開 `cmoc resume` の条件で
            検査した会話 ID と保存済み cwd。新規入力と同時には指定しない。

    Returns:
        同じ workload の制約を持つ、初回 exec または prompt 不在の対話再開の
        パラメータ。process の起動・移行制御は含まない。

    Raises:
        ValueError: 新規入力と再開先の両方、またはどちらも指定されていない。
    """
    if (original_prompt is None) == (resume is None):
        raise ValueError("specify exactly one of original_prompt and resume")
    path_context = AgentCallPathContext(
        agent_call_cwd=(
            resolve_repo_root() if resume is None else resume.agent_call_cwd
        )
    )
    prompt = None
    if original_prompt is not None:
        original_prompt_ref = '<cmoc_ref target="original_prompt"/>'
        complete_prompt = build_complete_prompt(
            task=f"""
            - オリジナルプロンプト {original_prompt_ref} が要求する作業を実行すること
            """,
            completion_criteria=f"""
            - オリジナルプロンプト {original_prompt_ref} が要求する成果と完了条件を満たしていること
            """,
            file_access_mode=FileAccessMode.REPO_WRITE,
            path_context=path_context,
            enable_document_search_mcp=True,
            aux_dynamic_prompt=[
                SDTagBlock(
                    "original_prompt",
                    SDHeader(
                        "オリジナルプロンプト",
                        original_prompt,
                    ),
                )
            ],
            oracle_and_realization_basic=True,
            oracle_policy=True,
            realization_policy=True,
            realization_findings_policy=True,
            routing_policy=True,
            editor_input_handoff_policy=True,
        )
        prompt = render_sd_node_as_markdown(*complete_prompt)
    return AgentCallParameter(
        agent_call_kind=build_tui_request.__name__,
        file_access_mode=FileAccessMode.REPO_WRITE,
        prompt=prompt,
        structured_output_schema_path=None,
        agent_call_cwd=path_context.agent_call_cwd,
        enable_editor_input_handoff_mcp=True,
        enable_document_search_mcp=True,
        tui_resume_session_id=None if resume is None else resume.codex_session_id,
    )
