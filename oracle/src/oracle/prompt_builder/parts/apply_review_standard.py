"""oracle file への適合性を判断する agent 向け文面の構築定義。"""

from functools import cache

from oracle.other.standard import StandardCollection, StandardGroup

from .common_standard import (
    FINDING_BASIS_STANDARD_GROUP,
    ORACLE_AUTHORITY_STANDARD_GROUP,
)
from .standard_definitions import (
    APPLY_REVIEW_ALREADY_RESOLVED_STANDARD,
    APPLY_REVIEW_FIX_TARGETS_STANDARD,
)


@cache
def build_apply_review_standard() -> StandardCollection:
    """realization の追従要否と所見を判断する規範を選択する。"""
    apply_review_group = StandardGroup(
        group_id="50.apply_review",
        title="apply review standard",
        scope="oracle file に対する realization file の追従要否・所見・修正の判断時",
        standards=(
            APPLY_REVIEW_FIX_TARGETS_STANDARD,
            APPLY_REVIEW_ALREADY_RESOLVED_STANDARD,
        ),
    )
    return StandardCollection(
        groups=(
            ORACLE_AUTHORITY_STANDARD_GROUP,
            FINDING_BASIS_STANDARD_GROUP,
            apply_review_group,
        ),
    )
