"""`cmoc tui` の prompt 文面と TUI 起動パラメータの構築定義。"""

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


def build_tui_launch_tui_parameter(
    time_stamp: str,
    original_prompt: str,
) -> AgentCallParameter:
    """`cmoc tui` サブコマンドの TUI 起動パラメータを構築する。

    Args:
        time_stamp: この `cmoc tui` 呼び出しのタイムスタンプ文字列。
        original_prompt: ユーザーがエディタ入力した、AI Agent CLI/TUI に渡す
            オリジナルプロンプト。コメント除去と strip は呼び出し側で完了している
            想定。エディタへ提示する完全プロンプトの skeleton を構築する場合は、
            `{{original-prompt-here}}` を渡す。

    Returns:
        Codex CLI の TUI 起動に使う固定パラメータ。
    """
    # main worktree を agent_call_cwd として先に確定する
    path_context = AgentCallPathContext(agent_call_cwd=resolve_repo_root())

    # 完全なプロンプトを生成してファイルに保存
    original_prompt_ref = '<cmoc_ref target="original_prompt"/>'
    complete_prompt = build_complete_prompt(
        role=original_prompt_ref,
        summary=original_prompt_ref,
        goal=original_prompt_ref,
        file_access_mode=FileAccessMode.REPO_WRITE,
        path_context=path_context,
        aux_dynamic_prompt=[
            StructBlock(
                "original_prompt",
                StructDoc(
                    "オリジナルプロンプト",
                    original_prompt,
                ),
            )
        ],
        oracle_and_realization_basic=True,
        oracle_standard=True,
        realization_standard=True,
        oracle_review_standard=True,
        apply_review_standard=True,
        realization_oracle_reference_rule=True,
    )
    complete_prompt_path = (
        path_context.repo_root
        / ".cmoc"
        / "gu"
        / "ar"
        / "log"
        / "editor_input"
        / f"{time_stamp}_cmpl.md"
    )
    complete_prompt_path.parent.mkdir(parents=True, exist_ok=True)
    complete_prompt_path.write_text(
        render_as_markdown(complete_prompt),
        encoding="utf-8",
    )
    # パラメータを生成して返す
    # NOTE
    #   TUI による対話的作業では人間の認知コスト的な負荷が大きいので、最大限 AI に頑張ってもらいたい
    #   入力タスクの難易度を正確に測るには最高性能モデルを使わざるを得ないし、だったら最初から最高性能モデルで作業させたほうが安い
    #   過剰になりうることは割り切って、最高品質設定にする
    return AgentCallParameter(
        agent_call_kind=build_tui_launch_tui_parameter.__name__,
        model_class=ModelClass.FLAGSHIP,
        reasoning_effort=ReasoningEffort.MAX,
        file_access_mode=FileAccessMode.REPO_WRITE,
        prompt=f"{complete_prompt_path} を読んで、その指示に従って下さい",
        structured_output_schema_path=None,
        agent_call_cwd=path_context.agent_call_cwd,
        run_indexing_preflight=True,
    )
