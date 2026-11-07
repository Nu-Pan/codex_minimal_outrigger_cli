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
    """参照先ファイルと、その中の参照箇所を保持する。"""

    # 参照先 (何を参照しているのか) の短い説明
    # NOTE
    #   省略不可
    description: str

    # 参照先ファイルのパス
    # NOTE
    #   spec, realization などの ID が定義されていない要素用
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
        if "\n" in self.description:
            raise ValueError("TODO メッセージ書く")
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
        if self.file_path and not self.id:
            return self.file_path
        elif not self.file_path and self.id:
            return self.id
        else:
            raise ValueError("TODO メッセージ書く")


def render_doc_ref_as_inline_md(doc_ref: DocRef) -> str:
    """単一の文書参照を Markdown のインライン形式へ変換する。"""
    if doc_ref.file_path and not doc_ref.id:
        return f"{doc_ref.description} (`{doc_ref.file_path}`)"
    elif not doc_ref.file_path and doc_ref.id:
        return f"{doc_ref.description} ({doc_ref.id})"
    else:
        raise ValueError("TODO メッセージ書く")


def render_doc_ref_as_multiline_md(doc_refs: Iterable[DocRef]) -> str:
    """複数の文書参照を複数行の Markdown へ変換する。

    - 箇条書き形式にする
    - 短く済むように、ファイル・IDごとにまとめる
    """
    # 先に都合の良いデータ構造に変換する
    doc_ref_tree: dict[Path | str, list[str]] = dict()
    for dr in doc_refs:
        if dr.location_info in doc_ref_tree:
            doc_ref_tree[dr.location_info].append(dr.description)
        else:
            doc_ref_tree[dr.location_info] = [dr.description]
    # テキストに変換する
    lines: list[str] = list()
    for location_info in sorted(doc_ref_tree.keys()):
        lines.append(f"- {location_info}")
        for description in sorted(doc_ref_tree[location_info]):
            lines.append(f"    - {description}")
    # 正常終了
    return "\n".join(lines)
