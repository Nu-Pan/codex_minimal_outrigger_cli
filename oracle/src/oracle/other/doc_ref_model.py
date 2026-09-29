"""文書参照の Python データ構造と Markdown 表記の正本。

意味仕様は `{{cmoc-root}}/oracle/doc/app_spec/editor_input_handoff.md` の
「参照情報」を参照する。
"""

# std
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class DocRef:
    """参照先ファイルと、その中の参照箇所を保持する。"""

    # 参照先ファイルのパス
    file_path: Path

    # 参照先ファイル内の「どこ」を指しているのかを表す短い説明
    # ファイル全体が参照先の場合は None を書く
    # NOTE
    #   行番号は書いてはいけない。
    #   行番号はちょっとした編集で変わるものなので不安定。
    # NOTE
    #   ある任意の箇所を編集する際には、影響範囲を特定する必要があるが、
    #   この「影響範囲」には当然この「参照」も含まれる。
    #   単純なキーワード検索で参照元を逆引き出来ることが望ましいので、
    #   例えば「参照先の見出しの名前」のような形式で記述するのが良い。
    loc_desc: str | None

    def __post_init__(self) -> None:
        """相対パスと空の参照箇所を拒否する。"""
        # 値の補完や正規化はせず、入力の基本条件を検査する。
        if not self.file_path.is_absolute():
            raise ValueError("Document reference requires an absolute file path")
        if isinstance(self.loc_desc, str) and not self.loc_desc.strip():
            raise ValueError("Document reference location must be nonblank or None")


def render_doc_ref_as_inline_md(doc_ref: DocRef) -> str:
    """単一の文書参照を Markdown のインライン形式へ変換する。"""
    # ファイル全体への参照では、箇所の表記を省く。
    if doc_ref.loc_desc is None:
        return f"`{doc_ref.file_path}`"
    return f"`{doc_ref.file_path}:{doc_ref.loc_desc}`"


def render_doc_ref_as_multiline_md(doc_ref: Iterable[DocRef]) -> str:
    """複数の文書参照をファイルごとにまとめた Markdown の一覧へ変換する。"""
    # 一度しか走査できない iterable でも、各ファイルの参照箇所を保持する。
    references = tuple(doc_ref)
    lines: list[str] = []
    file_paths = sorted({dr.file_path for dr in references})
    for fp in file_paths:
        lines.append(f"- `{fp}`")
        for loc_desc in [dr.loc_desc for dr in references if dr.file_path == fp]:
            if loc_desc is not None:
                lines.append("    - " + loc_desc)
    return "\n".join(lines)
