"""oracle review の所見成立条件を伝える agent 向け文面の構築定義。"""

from functools import cache

from oracle.other.policy import PolicyCollection, PolicyGroup

from .common_policy import FINDING_BASIS_POLICY_GROUP
from .policy_definitions import (
    ORACLE_REVIEW_FATAL_POLICY,
    ORACLE_REVIEW_MINOR_POLICY,
    ORACLE_REVIEW_ORACLE_ONLY_POLICY,
)


@cache
def build_oracle_review_policy() -> PolicyCollection:
    """oracle review の全段階で共有する所見判定規定を選択する。"""
    oracle_review_group = PolicyGroup(
        group_id="60.oracle_review",
        title="oracle review policy",
        scope="oracle file の所見の列挙・統合・検証・採否判定時",
        policies=(
            ORACLE_REVIEW_FATAL_POLICY,
            ORACLE_REVIEW_MINOR_POLICY,
            ORACLE_REVIEW_ORACLE_ONLY_POLICY,
        ),
    )
    return PolicyCollection(
        groups=(FINDING_BASIS_POLICY_GROUP, oracle_review_group),
    )
