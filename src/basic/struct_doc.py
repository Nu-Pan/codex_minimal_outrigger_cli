"""`{{work-root}}/oracle/src/oracle/other/struct_doc.py` の構造化文書 API を公開する。

正本の型と処理を複製せず既存の `basic.struct_doc` 参照を保つために残す。
`StructBlock` の描画済み文字列 child だけは、正本 renderer の追従漏れを局所的に補う。
"""

import re
from uuid import uuid4

from oracle.other.struct_doc import (
    StructBlock,
    StructCodeBlock,
    StructDoc,
    ntqs,
)
from oracle.other.struct_doc import render_as_markdown as _canonical_render_as_markdown


def render_as_markdown(
    struct_doc: StructDoc | StructBlock | list[StructDoc | StructBlock],
) -> str:
    """描画済み文字列 child を不透明な内容として Markdown へ埋め込む。

    根拠: {{work-root}}/oracle/doc/app_spec/prompt_standard.md
    """
    # NOTE: 正本 renderer が文字列 child を扱えるようになれば、この補正を削除して
    # oracle.other.struct_doc.render_as_markdown の再公開へ戻す。
    replacements: dict[str, str] = {}

    # 文字列 child を一時 StructDoc に変え、外側の参照だけ正本で検査する。
    if isinstance(struct_doc, list):
        adapted: StructDoc | StructBlock | list[StructDoc | StructBlock] = [
            _replace_opaque_string_blocks(root, replacements) for root in struct_doc
        ]
    else:
        adapted = _replace_opaque_string_blocks(struct_doc, replacements)
    rendered = _canonical_render_as_markdown(adapted)

    # 一時 StructDoc の描画結果を、事前検査済みの不透明な Markdown へ戻す。
    for marker, markdown in replacements.items():
        pattern = re.compile(rf"(?m)^#+ {re.escape(marker)}\n\n{re.escape(marker)}\n")
        matches = list(pattern.finditer(rendered))
        if len(matches) != 1:
            raise RuntimeError("opaque StructBlock child marker was not rendered once")
        match = matches[0]
        rendered = rendered[: match.start()] + markdown + rendered[match.end() :]
    return rendered


def _replace_opaque_string_blocks(
    node: StructDoc | StructBlock,
    replacements: dict[str, str],
) -> StructDoc | StructBlock:
    """文字列 child を参照検査用の一時 StructDoc へ置換する。"""
    if isinstance(node, StructBlock):
        if isinstance(node.child, str):
            marker = f"cmoc-opaque-struct-block-{uuid4().hex}"
            replacements[marker] = node.child
            return StructBlock(node.block_id, StructDoc(marker, marker))
        return StructBlock(
            node.block_id,
            _replace_opaque_string_blocks_in_doc(node.child, replacements),
        )
    return _replace_opaque_string_blocks_in_doc(node, replacements)


def _replace_opaque_string_blocks_in_doc(
    doc: StructDoc,
    replacements: dict[str, str],
) -> StructDoc:
    """StructDoc 内に入れ子になった文字列 block を置換する。"""
    if isinstance(doc.children, list):
        return StructDoc(
            doc.title,
            *(
                _replace_opaque_string_blocks(child, replacements)
                for child in doc.children
            ),
        )
    return StructDoc(doc.title, doc.children)


__all__ = [
    "StructBlock",
    "StructCodeBlock",
    "StructDoc",
    "ntqs",
    "render_as_markdown",
]
