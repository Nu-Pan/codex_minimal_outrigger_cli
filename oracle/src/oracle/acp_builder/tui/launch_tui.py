"""`cmoc tui` の TUI 起動 prompt 正本。"""

# std
from pathlib import Path

# cmoc
from oracle.acp_builder.basic import (
    AgentCallParameter,
    FileAccessMode,
    ModelClass,
    ReasoningEffort,
)
from oracle.other.path_model import resolve_repo_root
from oracle.other.struct_doc import StructBlock, StructDoc, render_as_markdown
from oracle.prompt_builder.complete_prompt import build_complete_prompt


def build_tui_launch_tui_parameter(
    time_stamp: str,
    original_prompt: str,
    oracle_standard: bool,
    realization_standard: bool,
    oracle_review_standard: bool,
    apply_review_standard: bool,
) -> AgentCallParameter:
    """`cmoc tui` サブコマンドの TUI 起動パラメータを構築する。

    Args:
        time_stamp: この `cmoc tui` 呼び出しのタイムスタンプ文字列。
        original_prompt: ユーザーがエディタ入力した、AI Agent CLI/TUI に渡す
            オリジナルプロンプト。コメント除去と strip は呼び出し側で完了している
            想定。
        oracle_standard: oracle standard を適用するかどうか。
        realization_standard: realization standard を適用するかどうか。
        oracle_review_standard: oracle review standard を適用するかどうか。
        apply_review_standard: apply review standard を適用するかどうか。

    Returns:
        Codex CLI の TUI 起動に使う固定パラメータ。
    """
    # 完全なプロンプトを生成してファイルに保存
    original_prompt_ref = '<cmoc_ref target="original_prompt"/>'
    complete_prompt = build_complete_prompt(
        role=original_prompt_ref,
        summary=original_prompt_ref,
        goal=original_prompt_ref,
        file_access_mode=FileAccessMode.REPO_WRITE,
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
        oracle_standard=oracle_standard,
        realization_standard=realization_standard,
        oracle_review_standard=oracle_review_standard,
        apply_review_standard=apply_review_standard,
        index_entry_standard=False,
    )
    complete_prompt_path = (
        resolve_repo_root()
        / ".cmoc"
        / "gu"
        / "ar"
        / "log"
        / "editor_input"
        / f"{time_stamp}_cmpl.md"
    )
    with open(complete_prompt_path, "w") as f:
        f.write(render_as_markdown(complete_prompt))
    # パラメータを生成して返す
    # NOTE
    #   TUI による対話的作業では人間の認知コスト的な負荷が大きいので、最大限 AI に頑張ってもらいたい
    #   入力タスクの難易度を正確に測るには最高性能モデルを使わざるを得ないし、だったら最初から最高性能モデルで作業させたほうが安い
    #   過剰になりうることは割り切って、最高品質設定にする
    return AgentCallParameter(
        ModelClass.FLAGSHIP,
        ReasoningEffort.MAX,
        FileAccessMode.REPO_WRITE,
        f"{complete_prompt_path} を読んで、その指示に従って下さい",
        Path(__file__).with_suffix(".json"),
        True,
    )
