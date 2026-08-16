"""session join の conflict 解消用 instruction 文面の構築定義。"""

from functools import cache

from ..parts.policy_definitions import (
    CONFLICT_RESOLUTION_PRESERVE_BOTH_BRANCHES_POLICY,
)
from .basic import PolicyCollection, PolicyGroup
from .common import ORACLE_AUTHORITY_POLICY_GROUP


@cache
def build_conflict_resolution_policy() -> PolicyCollection:
    """oracle / realization の意味を保つ conflict 解消規定を選択する。"""
    conflict_group = PolicyGroup(
        group_id="70.conflict_resolution",
        title="conflict resolution policy",
        scope="`cmoc session join` の conflict marker 解消時だけ",
        policies=(CONFLICT_RESOLUTION_PRESERVE_BOTH_BRANCHES_POLICY,),
    )
    return PolicyCollection(
        groups=(ORACLE_AUTHORITY_POLICY_GROUP, conflict_group),
    )
