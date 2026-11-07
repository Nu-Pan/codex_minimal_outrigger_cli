"""文書参照の Python データ構造と Markdown 表記の正本。

意味仕様は `{{cmoc-root}}/spec/app_spec/editor_input_handoff.md` の
「参照情報」を参照する。
"""

# std
import re
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class DocRef:
    """参照先の説明と、ファイルパスまたは ID を保持する。"""

    # 参照先 (何を参照しているのか) の短い説明
    # NOTE
    #   省略不可
    description: str

    # 参照先ファイルのパス
    # NOTE
    #   reference, realization などの ID が定義されていない要素用
    #   `id` と排他
    file_path: Path | None

    # 参照先の ID
    # NOTE
    #   decision, spec などの ID が定義されている要素用
    #   `file_path` と排他
    id: str | None

    def __post_init__(self) -> None:
        """設定された値を検証する。"""
        if not self.description.strip():
            raise ValueError("A document reference must have a non-blank description.")
        if "\n" in self.description or "\r" in self.description:
            raise ValueError(
                "A document reference description must not contain line breaks."
            )
        if (self.file_path is None) == (self.id is None):
            raise ValueError("Provide either 'file_path' or 'id', but not both.")
        if self.file_path is not None and not self.file_path.is_absolute():
            raise ValueError("The file path must be absolute.")
        if (
            self.id is not None
            and re.fullmatch(r"(?:DECI|SPEC)-\d{6}", self.id) is None
        ):
            raise ValueError(
                "The reference ID must be 'DECI-' or 'SPEC-' followed by exactly six digits."
            )

    @property
    def location_info(self) -> Path | str:
        """参照先のファイルパスまたは ID を返す。"""
        if self.file_path is not None and self.id is None:
            return self.file_path
        elif self.file_path is None and self.id is not None:
            return self.id
        else:
            raise ValueError("Provide either 'file_path' or 'id', but not both.")


def render_doc_ref_as_inline_md(doc_ref: DocRef) -> str:
    """単一の文書参照を Markdown のインライン形式へ変換する。"""
    return f"{doc_ref.description} (`{doc_ref.location_info}`)"


def render_doc_ref_as_multiline_md(doc_refs: Iterable[DocRef]) -> str:
    """複数の文書参照を複数行の Markdown へ変換する。

    - 箇条書き形式にする
    - 短く済むように、ファイル・IDごとにまとめる
    """
    # 先に都合の良いデータ構造に変換する
    doc_ref_tree: dict[Path | str, list[str]] = dict()
    for dr in doc_refs:
        doc_ref_tree.setdefault(dr.location_info, []).append(dr.description)
    # テキストに変換する
    lines: list[str] = list()
    for location_info in sorted(doc_ref_tree, key=str):
        lines.append(f"- `{location_info}`")
        for description in sorted(doc_ref_tree[location_info]):
            lines.append(f"    - {description}")
    # 正常終了
    return "\n".join(lines)
