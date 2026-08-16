"""INDEX.md 用エントリーを生成する agent 向け文面の構築定義。"""

from functools import cache

from ..parts.policy_definitions import (
    INDEX_ENTRY_EVIDENCE_POLICY,
    INDEX_ENTRY_ROUTING_POLICY,
    INDEX_ENTRY_SEMANTIC_INFORMATION_POLICY,
)
from .basic import PolicyCollection, PolicyGroup


@cache
def build_index_entry_policy() -> PolicyCollection:
    """INDEX.md エントリーが従う規定を選択する。"""
    index_entry_group = PolicyGroup(
        group_id="80.index_entry",
        title="index entry policy",
        scope="`INDEX.md` 用エントリー生成時",
        policies=(
            INDEX_ENTRY_ROUTING_POLICY,
            INDEX_ENTRY_EVIDENCE_POLICY,
            INDEX_ENTRY_SEMANTIC_INFORMATION_POLICY,
        ),
    )
    return PolicyCollection(groups=(index_entry_group,))
