"""`{{work-root}}/oracle/src/oracle/other/struct_doc.py` の構造化文書実装を再公開する。

正本実装を realization 側へ複製せず既存の `basic.struct_doc` 参照を保つために残す。
削除条件は realization 側と利用者向け公開面から `basic.struct_doc` 参照がなくなること。
"""

from oracle.other.struct_doc import (
    SDCodeBlock as StructCodeBlock,
)
from oracle.other.struct_doc import (
    SDHeader as StructDoc,
)
from oracle.other.struct_doc import (
    SDTagBlock as StructBlock,
)
from oracle.other.struct_doc import (
    ntqs,
    render_sd_node_as_markdown,
)


def render_as_markdown(
    struct_node: StructDoc | StructBlock | list[StructDoc | StructBlock],
) -> str:
    """旧 API の単一 root または root list を canonical renderer で描画する。"""
    # 旧 list input を新しい variadic interface へ変換する
    if isinstance(struct_node, list):
        return render_sd_node_as_markdown(*struct_node)

    # 単一 root は一要素の variadic input として渡す
    return render_sd_node_as_markdown(struct_node)


__all__ = [
    "StructBlock",
    "StructCodeBlock",
    "StructDoc",
    "ntqs",
    "render_as_markdown",
]
