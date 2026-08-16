"""oracle file への適合性を判断する agent 向け文面の構築定義。"""

from functools import cache

from .basic import PolicyCollection, PolicyGroup
from .common import (
    FINDING_BASIS_POLICY_GROUP,
    ORACLE_AUTHORITY_POLICY_GROUP,
)
from .definitions import (
    APPLY_REVIEW_ALREADY_RESOLVED_POLICY,
    APPLY_REVIEW_FIX_TARGETS_POLICY,
)


@cache
def build_apply_review_policy() -> PolicyCollection:
    """realization の追従要否と所見を判断する規定を選択する。"""
    apply_review_group = PolicyGroup(
        group_id="50.apply_review",
        title="apply review policy",
        scope="oracle file に対する realization file の追従要否・所見・修正の判断時",
        policies=(
            APPLY_REVIEW_FIX_TARGETS_POLICY,
            APPLY_REVIEW_ALREADY_RESOLVED_POLICY,
        ),
    )
    return PolicyCollection(
        groups=(
            ORACLE_AUTHORITY_POLICY_GROUP,
            FINDING_BASIS_POLICY_GROUP,
            apply_review_group,
        ),
    )
