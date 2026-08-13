"""session join の conflict 解消用 instruction 文面の構築定義。"""

from functools import cache

from oracle.other.standard import StandardCollection, StandardGroup

from .common_standard import ORACLE_AUTHORITY_STANDARD_GROUP
from .standard_definitions import (
    CONFLICT_RESOLUTION_PRESERVE_BOTH_BRANCHES_STANDARD,
)


@cache
def build_conflict_resolution_standard() -> StandardCollection:
    """oracle / realization の意味を保つ conflict 解消規範を選択する。"""
    conflict_group = StandardGroup(
        group_id="70.conflict_resolution",
        title="conflict resolution standard",
        scope="`cmoc session join` の conflict marker 解消時だけ",
        standards=(CONFLICT_RESOLUTION_PRESERVE_BOTH_BRANCHES_STANDARD,),
    )
    return StandardCollection(
        groups=(ORACLE_AUTHORITY_STANDARD_GROUP, conflict_group),
    )
