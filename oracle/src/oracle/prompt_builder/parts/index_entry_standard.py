"""INDEX.md 用エントリーを生成する agent 向け文面の構築定義。"""

from functools import cache

from oracle.other.standard import StandardCollection, StandardGroup

from .standard_definitions import (
    INDEX_ENTRY_EVIDENCE_STANDARD,
    INDEX_ENTRY_ROUTING_STANDARD,
    INDEX_ENTRY_SEMANTIC_INFORMATION_STANDARD,
)


@cache
def build_index_entry_standard() -> StandardCollection:
    """INDEX.md エントリーが従う規範を選択する。"""
    index_entry_group = StandardGroup(
        group_id="80.index_entry",
        title="index entry standard",
        scope="`INDEX.md` 用エントリー生成時",
        standards=(
            INDEX_ENTRY_ROUTING_STANDARD,
            INDEX_ENTRY_EVIDENCE_STANDARD,
            INDEX_ENTRY_SEMANTIC_INFORMATION_STANDARD,
        ),
    )
    return StandardCollection(groups=(index_entry_group,))
