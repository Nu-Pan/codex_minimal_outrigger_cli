"""項目別入力と送信元情報から handoff 本文を構築する正本。

意味仕様は `{{cmoc-root}}/oracle/doc/app_spec/editor_input_handoff.md` の
「本文の生成」と「送信元情報」を参照する。
"""

# std
from dataclasses import dataclass
from pathlib import Path

# local
from ..other.doc_ref_model import DocRef, render_doc_ref_as_multiline_md
from ..other.struct_doc import SDHeader, render_sd_node_as_markdown


@dataclass(frozen=True)
class EditorInputHandoffSource:
    """cmoc が実際の送信側 TUI process に付与・保持する値。

    識別子の発行、ログの探索、および相対パスの補完は行わない。
    """

    subcommand: str
    execution_id: str
    codex_call_id: str
    sub_command_log_path: Path

    def __post_init__(self) -> None:
        """不足した識別情報とフルパスでないログパスを拒否する。"""
        # 値の補完や正規化をせず、呼び出し元が確定した値を保持する。
        if not all(
            value.strip()
            for value in (self.subcommand, self.execution_id, self.codex_call_id)
        ):
            raise ValueError("Editor input handoff requires source identifiers")
        if not self.sub_command_log_path.is_absolute():
            raise ValueError(
                "Editor input handoff requires an absolute subcommand log path"
            )


def build_editor_input_handoff_body(
    goal: str,
    instructions: str,
    background: str,
    decisions: str,
    open_questions: str,
    oracle_references: list[DocRef],
    source: EditorInputHandoffSource,
) -> str:
    """MCP が検証した項目と実際の送信元情報を本文へ配置する。

    Args:
        goal: 受信側で達成してほしい目標状態。
        instructions: 受信側へ依頼する具体的な作業。
        background: 依頼の意図・背景。
        decisions: 決定事項とその理由。
        open_questions: 未確定事項。
        oracle_references: 入力から変換・検証した oracle の文書参照。
        source: 送信側 TUI process の呼び出し元コンテキストから取得した値。

    Returns:
        editor work file 全体を置換する Markdown 本文。

    Raises:
        ValueError: 自由記述項目が空文字列または空白だけの場合。

    NOTE
        `{{cmoc-root}}/oracle/src/oracle/editor_input_handoff/overwrite_input.json`
        の root schema（JSON Pointer `#`）による入力検証、参照情報の変換、
        送信元情報の取得、target の検証、および書き込みは呼び出し側が担う。
    """
    # 引数チェック
    if not all(
        value.strip()
        for value in (goal, instructions, background, decisions, open_questions)
    ):
        raise ValueError("Editor input handoff requires nonblank text fields")
    # 基本セクション
    sections = [
        SDHeader(
            "目標",
            goal,
        ),
        SDHeader(
            "依頼内容",
            instructions,
        ),
        SDHeader(
            "意図・背景",
            background,
        ),
        SDHeader(
            "決定事項と理由",
            decisions,
        ),
        SDHeader(
            "未確定事項",
            open_questions,
        ),
    ]
    # 参照
    if oracle_references:
        sections.append(
            SDHeader(
                "参照ファイル",
                render_doc_ref_as_multiline_md(oracle_references),
            )
        )
    # 機械的な値
    sections.append(
        SDHeader(
            "送信元情報",
            f"""
            - 送信元のサブコマンド名: {source.subcommand}
            - 送信元の実行 ID: {source.execution_id}
            - 送信元 TUI process の Codex call ID: {source.codex_call_id}
            - 診断用サブコマンドログのフルパス: {source.sub_command_log_path}
            """,
        )
    )
    # レンダリングして返す
    return render_sd_node_as_markdown(*sections)
