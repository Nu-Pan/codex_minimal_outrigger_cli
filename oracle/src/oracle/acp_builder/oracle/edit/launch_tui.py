"""`cmoc oracle edit` の TUI 起動 prompt 正本。"""

# cmoc
from oracle.other.struct_doc import StructDoc, render_as_markdown
from oracle.other.path_model import resolve_repo_root
from oracle.acp_builder.basic import (
    AgentCallParameter,
    ModelClass,
    ReasoningEffort,
    FileAccessMode,
)
from oracle.prompt_builder.complete_prompt import build_complete_prompt


def build_oracle_edit_launch_tui_parameter(
    time_stamp: str,
    user_instruction: str,
) -> AgentCallParameter:
    """`cmoc oracle edit` の TUI 起動パラメータを構築する。

    Args:
        time_stamp: この `cmoc oracle edit` 呼び出しのタイムスタンプ文字列。
        user_instruction: ユーザーがエディタ入力した、oracle file の最終状態に
            関する指示。コメント除去と strip は呼び出し側で完了している想定。

    Returns:
        Codex CLI の TUI 起動に使う固定パラメータ。
    """
    # ユーザー指示以外を固定した完全プロンプトを構築する
    complete_prompt = build_complete_prompt(
        role="- あなたは oracle file の編集担当です",
        summary="""
        - ユーザー指示が要求する最終状態を `{{work-root}}/oracle` ツリー内の oracle file に反映すること
        - realization file を読み書きせず、oracle file だけを正本として作業すること
        """,
        goal="""
        - ユーザー指示が要求する最終状態が oracle file 上で満たされていること
        - 関連する oracle file と論理的に整合していること
        - ユーザー指示の実現に必要な箇所以外の既存仕様の意味論が維持されていること
        """,
        file_access_mode=FileAccessMode.PURE_ORACLE_WRITE,
        aux_dynamic_prompt=[
            StructDoc(
                "ユーザー指示",
                user_instruction,
            ),
        ],
        oracle_and_realization_basic=True,
        oracle_standard=True,
    )

    # cmoc が管理する TUI ログへ完全プロンプトを保存する
    complete_prompt_path = (
        resolve_repo_root()
        / ".cmoc"
        / "gu"
        / "ar"
        / "log"
        / "tui"
        / f"{time_stamp}_cmpl.md"
    )
    with open(complete_prompt_path, "w", encoding="utf-8") as f:
        f.write(render_as_markdown(complete_prompt))

    # TUI を起動する
    return AgentCallParameter(
        model_class=ModelClass.FLAGSHIP,
        reasoning_effort=ReasoningEffort.MAX,
        file_access_mode=FileAccessMode.PURE_ORACLE_WRITE,
        prompt=f"{complete_prompt_path} を読んで、その指示に従って下さい",
        structured_output_schema_path=None,
        run_indexing_preflight=True,
    )
