"""`cmoc tui` の実行パラメータ解決 prompt 正本。"""

# std
from pathlib import Path

# cmoc
from oracle.acp_builder.basic import (
    AgentCallParameter,
    FileAccessMode,
    ModelClass,
    ReasoningEffort,
)
from oracle.other.path_model import AgentCallPathContext, resolve_repo_root
from oracle.other.struct_doc import (
    StructBlock,
    StructCodeBlock,
    StructDoc,
    render_as_markdown,
)
from oracle.prompt_builder.complete_prompt import build_complete_prompt


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
    # 後続 TUI と同じ main worktree を cwd として先に確定する
    path_context = AgentCallPathContext(resolve_repo_root())

    # プロンプト
    prompt = build_complete_prompt(
        role="- あなたの役割は、後続の AI Agent CLI/TUI 実行に必要な情報を選定することです",
        summary="""
        - `{{repo-root}}` ツリー内で、オリジナルプロンプト <cmoc_ref target="original_prompt"/> を、このセッションとは別の、後続の AI Agent CLI/TUI で実行する予定です
        - この実行に `oracle_standard`, `realization_standard`, `oracle_review_standard`, `apply_review_standard` を適用するかどうかを選択して下さい
        """,
        goal="""
        - Structured Output schema に従って4つの標準の選択結果を返していること
        - 選択の根拠として、オリジナルプロンプト <cmoc_ref target="original_prompt"/> の該当行、あるいは `{{work-root}}` ツリー内の file の該当行が具体的に示されていること
        """,
        file_access_mode=FileAccessMode.READONLY,
        path_context=path_context,
        aux_dynamic_prompt=[
            StructBlock(
                "original_prompt",
                StructDoc(
                    "オリジナルプロンプト",
                    StructCodeBlock(
                        "markdown",
                        original_prompt,
                    ),
                ),
            )
        ],
        oracle_and_realization_basic=True,
        oracle_standard=True,
        realization_standard=True,
        oracle_review_standard=True,
        apply_review_standard=True,
        index_entry_standard=False,
    )
    # パラメータを生成して返す
    # NOTE
    #   性質的にはかなり簡単なタスクなので、品質を切り詰めやすい
    #   しかし、ここで間違えられると、後続の本命作業がパーになってキレそうになる
    #   経済性重視系の最高性能を使用する
    return AgentCallParameter(
        model_class=ModelClass.EFFICIENCY,
        reasoning_effort=ReasoningEffort.MAX,
        file_access_mode=FileAccessMode.READONLY,
        prompt=render_as_markdown(prompt),
        structured_output_schema_path=Path(__file__).with_suffix(".json"),
        cwd=path_context.cwd,
        run_indexing_preflight=True,
    )
