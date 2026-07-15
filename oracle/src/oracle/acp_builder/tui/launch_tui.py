"""`cmoc tui` の TUI 起動 prompt 正本。"""

# std
from pathlib import Path

from oracle.acp_builder.basic import (
    AgentCallParameter,
    FileAccessMode,
    ModelClass,
    ReasoningEffort,
)
from oracle.other.path_model import resolve_repo_root

# cmoc
from oracle.other.struct_doc import StructDoc, render_as_markdown
from oracle.prompt_builder.complete_prompt import build_complete_prompt


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
    """`cmoc tui` サブコマンド、TUI 起動パラメータ解決用。
    AI エージェント呼び出しパラメータを構築する。

    time_stamp: str
        この `cmoc tui` 呼び出しのタイムスタンプ文字列

    role: str
    summary: str
    goal: str
    file_access_mode: str
    oracle_and_realization_basic: bool
    oracle_standard: bool
    realization_standard: bool
    review_oracle_standard: bool
    apply_review_standard: bool
    index_entry_standard: bool
        関数 `build_complete_prompt` の docstring を参照

    original_prompt: str
        ユーザーがエディタ入力した、AI Agent CLI/TUI に渡す元プロンプト。
        コメント除去と strip は呼び出し側で完了している想定。
    """
    # 完全なプロンプトを生成してファイルに保存
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
        resolve_repo_root()
        / ".cmoc"
        / "gu"
        / "ar"
        / "log"
        / "tui"
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
        file_access_mode,
        f"{complete_prompt_path} を読んで、その指示に従って下さい",
        Path(__file__).with_suffix(".json"),
        True,
    )
