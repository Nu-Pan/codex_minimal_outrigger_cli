"""`cmoc indexing` の agent 向け prompt 文面と起動パラメータの構築定義。"""

# std
from pathlib import Path

from oracle.acp_builder.basic import (
    AgentCallParameter,
    FileAccessMode,
    ModelClass,
    ReasoningEffort,
)
from oracle.other.path_model import AgentCallPathContext, resolve_real_path

# cmoc
from oracle.other.struct_doc import StructCodeBlock, StructDoc, render_as_markdown
from oracle.prompt_builder.complete_prompt import build_complete_prompt


def build_indexing_index_entry_parameter(
    target_path: Path,
    target_content: str,
    agent_call_cwd: Path,
) -> AgentCallParameter:
    """
    `cmoc indexing` サブコマンド、目次情報生成用。
    AI エージェント呼び出しパラメータを構築する。

    target_path: Path
        目次情報生成対象のファイルまたはディレクトリ

    target_content: str
        目次情報生成対象の内容
        ディレクトリの場合は、その直下の `INDEX.md` の内容が渡される想定

    agent_call_cwd: Path
        目次情報生成 agent call に設定する cwd
    """
    # agent_call_cwd を確定してから完全 prompt 用の path context を構築する
    path_context = AgentCallPathContext(agent_call_cwd=agent_call_cwd)

    # プロンプト
    prompt = build_complete_prompt(
        role="- あなたはソフトウェアリポジトリのルーティング文書作成担当です",
        summary="- `{{target-path}}` の `INDEX.md` 用エントリーを生成すること",
        goal="- 指定された Structured Output schema に従ってエントリーを返すこと",
        file_access_mode=FileAccessMode.READONLY,
        path_context=path_context,
        aux_dynamic_prompt=[
            StructDoc(
                "エントリー生成規則",
                """
                - 必ずオリジナルの本文のみを根拠にエントリーを生成すること
                - 既存の `INDEX.md` を読むのは禁止
                - `{{target-path}}` 以外の文章も必要に応じて参照すること
                """,
            ),
            StructDoc(
                "`{{target-path}}` の内容",
                StructCodeBlock(
                    None,
                    target_content,
                ),
            ),
        ],
        aux_placeholder_def={
            "target-path": resolve_real_path(target_path, path_context),
        },
        index_entry_standard=True,
    )
    # パラメータを生成して返す
    # NOTE
    #   この agent call は indexing preflight そのもの。
    #   よって run_indexing_preflight=False が正しい。
    # NOTE
    #   呼び出し回数がとにかく多いので、経済性がとても大事
    #   非常に単純な要約タスクなので、かなり品質を下げても成立しやすい
    #   cmoc 上の下限設定を採用
    return AgentCallParameter(
        agent_call_kind=build_indexing_index_entry_parameter.__name__,
        model_class=ModelClass.MINIMUM,
        reasoning_effort=ReasoningEffort.LOW,
        file_access_mode=FileAccessMode.READONLY,
        prompt=render_as_markdown(prompt),
        structured_output_schema_path=Path(__file__).with_suffix(".json"),
        agent_call_cwd=path_context.agent_call_cwd,
        run_indexing_preflight=False,
    )
