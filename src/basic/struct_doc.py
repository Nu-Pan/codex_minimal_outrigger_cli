"""`<work-root>/oracle/src/oracle/other/struct_doc.py` の構造化文書実装を再公開する。

正本実装を realization 側へ複製せず既存の `basic.struct_doc` 参照を保つために残す。
削除条件は realization 側と利用者向け公開面から `basic.struct_doc` 参照がなくなること。
"""

from oracle.other.struct_doc import (
    StructCodeBlock,
    StructDoc,
    ntqs,
    render_as_markdown,
)

__all__ = [
    "StructCodeBlock",
    "StructDoc",
    "ntqs",
    "render_as_markdown",
]
