"""`cmoc tui` の実行パラメータ解決 prompt 正本。"""

# std
from pathlib import Path

# cmoc
from basic.struct_doc import StructDoc, StructCodeBlock, render_as_markdown
from basic.path_model import resolve_repo_root, resolve_work_root
from basic.acp import (
    AgentCallParameter,
    ModelClass,
    ReasoningEffort,
    FileAccessMode,
)
from acp.prompt_parts.complete_prompt import build_complete_prompt
from acp.prompt_parts.file_access_rule import build_file_access_rule


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
    # パス
    repo_root = resolve_repo_root()
    work_root = resolve_work_root()
    # プロンプト
    prompt = build_complete_prompt(
        role="- あなたは AI Agent CLI/TUI の実行パラメータ選定担当です",
        summary=f"""
        - `{repo_root}` ツリー内で、後述する「オリジナルプロンプト」を AI Agent CLI/TUI で実行します
        - この AI Agent CLI/TUI に与えるべきパラメータを選択して下さい
        """,
        goal=f"""
        - Structured Output schema に従ってパラメータ選択結果を返していること
        - パラメータ選択の根拠として、オリジナルプロンプトの該当行、あるいは `{work_root}` ツリー内のファイルの該当行が示されていること
        """,
        file_access_mode=FileAccessMode.READONLY,
        aux_prompt=[
            StructDoc(
                "オリジナルプロンプト",
                StructCodeBlock(
                    "markdown",
                    original_prompt,
                ),
            ),
            StructDoc(
                "ファイルアクセスモード",
                *[build_file_access_rule(fam) for fam in FileAccessMode],
            ),
        ],
        oracle_and_realization_basic=True,
        oracle_standard=True,
        realization_standard=True,
        review_oracle_standard=True,
        apply_review_standard=True,
        index_entry_standard=True,
    )
    # パラメータを生成して返す
    return AgentCallParameter(
        ModelClass.EFFICIENCY,
        ReasoningEffort.MEDIUM,
        FileAccessMode.READONLY,
        render_as_markdown(prompt),
        Path(__file__).with_suffix(".json"),
    )
