"""`cmoc tui` の prompt 文面と TUI 起動パラメータの構築定義。"""

# cmoc
from oracle.acp_builder.basic import (
    AgentCallParameter,
    FileAccessMode,
)
from oracle.other.path_model import AgentCallPathContext, resolve_repo_root
from oracle.other.struct_doc import SDHeader, SDTagBlock, render_sd_node_as_markdown
from oracle.prompt_builder.complete_prompt import build_complete_prompt


def build_tui_launch_tui_parameter(
    original_prompt: str,
) -> AgentCallParameter:
    """`cmoc tui` サブコマンドの TUI 起動パラメータを構築する。

    Args:
        original_prompt: ユーザーがエディタ入力した、AI Agent CLI/TUI に渡す
            オリジナルプロンプト。コメント除去と strip は呼び出し側で完了している
            想定。エディタへ提示する完全プロンプトの skeleton を構築する場合は、
            `{{original-prompt-here}}` を渡す。

    Returns:
        Codex CLI の TUI 起動に使う固定パラメータ。
    """
    path_context = AgentCallPathContext(agent_call_cwd=resolve_repo_root())
    original_prompt_ref = '<cmoc_ref target="original_prompt"/>'
    complete_prompt = build_complete_prompt(
        summary=f"""
        - オリジナルプロンプト {original_prompt_ref} に従って作業すること
        """,
        goal=f"""
        - オリジナルプロンプト {original_prompt_ref} が要求する成果と完了条件を満たしていること
        """,
        file_access_mode=FileAccessMode.REPO_WRITE,
        path_context=path_context,
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
        oracle_findings_policy=True,
        realization_findings_policy=True,
        routing_policy=True,
        editor_input_handoff_policy=True,
    )
    return AgentCallParameter(
        agent_call_kind=build_tui_launch_tui_parameter.__name__,
        file_access_mode=FileAccessMode.REPO_WRITE,
        prompt=render_sd_node_as_markdown(*complete_prompt),
        structured_output_schema_path=None,
        agent_call_cwd=path_context.agent_call_cwd,
        enable_editor_input_handoff_mcp=True,
        run_indexing_preflight=True,
    )
