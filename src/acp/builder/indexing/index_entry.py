"""`cmoc indexing` の目次情報生成 prompt 構築実装。

対応 oracle file: `<work-root>/oracle/src/acp/builder/indexing/index_entry.py`。
"""

# std
from pathlib import Path

# cmoc
from basic.struct_doc import StructDoc, StructCodeBlock, render_as_markdown
from basic.path_model import resolve_real_path
from basic.acp import (
    AgentCallParameter,
    ModelClass,
    ReasoningEffort,
    FileAccessMode,
)
from acp.prompt_parts.complete_prompt import build_complete_prompt


def build_indexing_index_entry_parameter(
    target_path: Path,
    target_content: str,
) -> AgentCallParameter:
    """
    `cmoc indexing` サブコマンド、目次情報生成用。
    AI エージェント呼び出しパラメータを構築する。

    target_path: Path
        目次情報生成対象のファイルまたはディレクトリ

    target_content: str
        目次情報生成対象の内容
        ディレクトリの場合は、その直下の `INDEX.md` の内容が渡される想定
    """
    # パス
    target_path = resolve_real_path(target_path)
    # プロンプト
    prompt = build_complete_prompt(
        role="- あなたはソフトウェアリポジトリのルーティング文書作成担当です",
        summary=f"- `{target_path}` の `INDEX.md` 用エントリーを生成すること",
        goal="- 指定された Structured Output schema に従ってエントリーを返すこと",
        file_access_mode=FileAccessMode.READONLY,
        aux_prompt=[
            StructDoc(
                "エントリー生成規則",
                f"""
                - 必ずオリジナルの本文のみを根拠にエントリーを生成すること
                - 既存の `INDEX.md` を読むのは禁止
                - `{target_path}` 以外の文章も必要に応じて参照すること
                """,
            ),
            StructDoc(
                f"`{target_path}` の内容",
                StructCodeBlock(
                    None,
                    target_content,
                ),
            ),
        ],
        index_entry_standard=True,
    )
    # パラメータを生成して返す
    return AgentCallParameter(
        ModelClass.EFFICIENCY,
        ReasoningEffort.LOW,
        FileAccessMode.READONLY,
        render_as_markdown(prompt),
        Path(__file__).with_suffix(".json"),
    )
