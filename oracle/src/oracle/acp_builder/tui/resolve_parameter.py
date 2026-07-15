"""`cmoc tui` の実行パラメータ解決 prompt 正本。"""

# std
from pathlib import Path

from oracle.acp_builder.basic import (
    AgentCallParameter,
    FileAccessMode,
    ModelClass,
    ReasoningEffort,
)
from oracle.other.path_model import resolve_repo_root, resolve_work_root

# cmoc
from oracle.other.struct_doc import StructCodeBlock, StructDoc, render_as_markdown
from oracle.prompt_builder.basic import PlaceholderMap
from oracle.prompt_builder.complete_prompt import build_complete_prompt
from oracle.prompt_builder.parts.file_access_rule import build_file_access_rule


def build_tui_resolve_parameter_parameter(
    original_prompt: str,
) -> AgentCallParameter:
    """
    `cmoc tui` サブコマンド、実行パラメータ解決用。
    AI エージェント呼び出しパラメータを構築する。

    original_prompt: str
        ユーザーがエディタ入力した、AI Agent CLI/TUI に渡す元プロンプト。
        コメント除去と strip は呼び出し側で完了している想定。
    """
    # ファイルアクセスモード関係だけ先に処理
    fam_prompt: list[StructDoc] = list()
    fam_ph_def: PlaceholderMap = dict()
    for fam in FileAccessMode:
        temp_ph_def, temp_fam_prompt = build_file_access_rule(fam)
        fam_prompt.append(temp_fam_prompt)
        fam_ph_def.update(fam_ph_def)

    # プロンプト
    # NOTE
    #   oracle_and_realization_basic 以降の固定プロンプト系フラグは全て True にする
    prompt = build_complete_prompt(
        role="- あなたは AI Agent CLI/TUI の実行パラメータ選定担当です",
        summary="""
        - `{{repo-root}}` ツリー内で、後述する「オリジナルプロンプト」を AI Agent CLI/TUI で実行します
        - この AI Agent CLI/TUI 実行に与えるべきパラメータを選択して下さい
        """,
        goal="""
        - Structured Output schema に従ってパラメータ選択結果を返していること
        - パラメータ選択の根拠として、オリジナルプロンプトの該当行、あるいは `{{work-root}}` ツリー内のファイルの該当行が具体的に示されていること
        """,
        file_access_mode=FileAccessMode.READONLY,
        aux_dynamic_prompt=[
            StructDoc(
                "オリジナルプロンプト",
                StructCodeBlock(
                    "markdown",
                    original_prompt,
                ),
            ),
            StructDoc(
                "ファイルアクセスモード",
                *fam_prompt,
            ),
        ],
        aux_placeholder_def={
            "repo-root": resolve_repo_root(),
            "work-root": resolve_work_root(),
            **fam_ph_def,
        },
        oracle_and_realization_basic=True,
        oracle_standard=True,
        realization_standard=True,
        review_oracle_standard=True,
        apply_review_standard=True,
        index_entry_standard=True,
    )
    # パラメータを生成して返す
    # NOTE
    #   性質的にはかなり簡単なタスクなので、品質を切り詰めやすい
    #   しかし、ここで間違えられると、後続の本命作業がパーになってキレそうになる
    #   経済性重視系の最高性能を使用する
    return AgentCallParameter(
        ModelClass.EFFICIENCY,
        ReasoningEffort.MAX,
        FileAccessMode.READONLY,
        render_as_markdown(prompt),
        Path(__file__).with_suffix(".json"),
        True,
    )
