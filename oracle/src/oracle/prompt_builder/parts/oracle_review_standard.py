"""oracle review の所見成立条件を伝える agent 向け文面の構築定義。"""

from functools import cache

from oracle.other.standard import StandardCollection, StandardGroup

from .common_standard import FINDING_BASIS_STANDARD_GROUP
from .standard_definitions import (
    ORACLE_REVIEW_FATAL_STANDARD,
    ORACLE_REVIEW_MINOR_STANDARD,
    ORACLE_REVIEW_ORACLE_ONLY_STANDARD,
)


@cache
def build_oracle_review_standard() -> StandardCollection:
    """oracle review の全段階で共有する所見判定規範を選択する。"""
    oracle_review_group = StandardGroup(
        group_id="60.oracle_review",
        title="oracle review standard",
        scope="oracle file の所見の列挙・統合・検証・採否判定時",
        standards=(
            ORACLE_REVIEW_FATAL_STANDARD,
            ORACLE_REVIEW_MINOR_STANDARD,
            ORACLE_REVIEW_ORACLE_ONLY_STANDARD,
        ),
    )
    return StandardCollection(
        groups=(FINDING_BASIS_STANDARD_GROUP, oracle_review_group),
    )
