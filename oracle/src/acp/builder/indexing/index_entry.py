"""`cmoc indexing` の目次情報生成 prompt 正本。"""

# std
from pathlib import Path

# cmoc
from basic.struct_doc import render_as_markdown
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
    sibling_entries: str,
) -> AgentCallParameter:
    """
    `cmoc indexing` サブコマンド、目次情報生成用。
    AI エージェント呼び出しパラメータを構築する。

    target_path: Path
        目次情報生成対象のファイルまたはディレクトリ。
    target_content: str
        目次情報生成対象の内容。ディレクトリの場合は直下エントリ情報を渡す想定。
    sibling_entries: str
        同じ INDEX.md に並ぶ他エントリの情報。
    """
    # パス
    target_path = resolve_real_path(target_path)
    # プロンプト
    prompt = build_complete_prompt(
        "- あなたはソフトウェアリポジトリのルーティング文書作成担当です",
        f"""
        - `{target_path}` の INDEX.md 用目次情報を生成すること
        - 対象内容は以下である

        ```text
        {target_content}
        ```

        - 同じ INDEX.md に並ぶ他エントリの情報は以下である

        ```text
        {sibling_entries}
        ```
        """,
        """
        - summary には対象に何が書いてあるか、または何が入っているかを箇条書き項目として返すこと
        - read_this_when には AI が対象を読む判断を下す条件を箇条書き項目として返すこと
        - do_not_read_this_when には過剰に読みに行かないための条件を箇条書き項目として返すこと
        - ファイル名、ディレクトリ名、hash は返さないこと
        """,
        FileAccessMode.READONLY,
        structured_output=True,
    )
    # パラメータを生成して返す
    return AgentCallParameter(
        ModelClass.EFFICIENCY,
        ReasoningEffort.MEDIUM,
        FileAccessMode.READONLY,
        render_as_markdown(prompt),
        Path(__file__).with_suffix(".json"),
    )
