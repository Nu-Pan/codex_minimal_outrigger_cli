"""realization file を扱う agent call 向け instruction 文面の構築定義。"""

from functools import cache

from ..parts.policy_definitions import (
    REALIZATION_CURRENT_SPEC_ONLY_POLICY,
    REALIZATION_ORACLE_CONFORMANCE_POLICY,
    REALIZATION_REPOSITORY_VERIFICATION_POLICY,
)
from .basic import PolicyCollection, PolicyGroup
from .common import ORACLE_AUTHORITY_POLICY_GROUP


@cache
def build_realization_policy() -> PolicyCollection:
    """realization file の作成・変更・レビューに必要な規定を選択する。"""
    realization_group = PolicyGroup(
        group_id="30.realization",
        title="realization policy",
        scope="realization file の作成・変更・リファクタ・レビュー時",
        policies=(
            REALIZATION_ORACLE_CONFORMANCE_POLICY,
            REALIZATION_CURRENT_SPEC_ONLY_POLICY,
            REALIZATION_REPOSITORY_VERIFICATION_POLICY,
        ),
    )
    return PolicyCollection(
        groups=(ORACLE_AUTHORITY_POLICY_GROUP, realization_group),
    )
