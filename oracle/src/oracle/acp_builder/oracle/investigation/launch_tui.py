"""`cmoc oracle investigation` の prompt 文面と TUI 起動パラメータの構築定義。"""

# cmoc
from oracle.acp_builder.basic import (
    AgentCallParameter,
    FileAccessMode,
)
from oracle.other.path_model import AgentCallPathContext, resolve_repo_root
from oracle.other.struct_doc import SDHeader, SDTagBlock, render_sd_node_as_markdown
from oracle.prompt_builder.complete_prompt import build_complete_prompt


def build_oracle_investigation_launch_tui_parameter(
    user_instruction: str,
) -> AgentCallParameter:
    """`cmoc oracle investigation` の TUI 起動パラメータを構築する。

    Args:
        user_instruction: ユーザーがエディタ入力した、oracle file に関する調査指示。
            コメント除去と strip は呼び出し側で完了している想定。エディタへ提示する
            完全プロンプトの skeleton を構築する場合は、
            `{{original-prompt-here}}` を渡す。

    Returns:
        Codex CLI の TUI 起動に使う固定パラメータ。
    """
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
        file_access_mode=FileAccessMode.PURE_ORACLE_READ,
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
        editor_input_handoff_policy=True,
    )
    return AgentCallParameter(
        agent_call_kind=build_oracle_investigation_launch_tui_parameter.__name__,
        file_access_mode=FileAccessMode.PURE_ORACLE_READ,
        prompt=render_sd_node_as_markdown(*complete_prompt),
        structured_output_schema_path=None,
        agent_call_cwd=path_context.agent_call_cwd,
        enable_editor_input_handoff_mcp=True,
        run_indexing_preflight=True,
    )
