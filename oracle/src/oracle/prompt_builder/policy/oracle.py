"""oracle file を扱う agent call 向け instruction 文面の構築定義。"""

from functools import cache

from .basic import PolicyCollection, PolicyGroup
from .common import (
    ORACLE_AUTHORITY_CORE_POLICY_GROUP,
    ORACLE_AUTHORITY_POLICY_GROUP,
)
from .definitions import (
    ORACLE_AUTHORITATIVE_BASIS_POLICY,
    ORACLE_CONSISTENCY_AND_SEARCHABILITY_POLICY,
    ORACLE_DEFINED_AND_UNDEFINED_POLICY,
    ORACLE_EDIT_AUTHORITATIVE_BASIS_POLICY,
    ORACLE_IMPLEMENTATION_CONSTRAINT_POLICY,
    ORACLE_INTENT_AND_GAPS_POLICY,
    ORACLE_NO_REVERSE_ENGINEERING_POLICY,
)


@cache
def build_oracle_policy() -> PolicyCollection:
    """oracle file の作成・変更・レビューに必要な規定を選択する。"""
    oracle_group = PolicyGroup(
        group_id="20.oracle",
        title="oracle policy",
        scope="oracle file の作成・変更・レビュー時",
        policies=(
            ORACLE_AUTHORITATIVE_BASIS_POLICY,
            ORACLE_EDIT_AUTHORITATIVE_BASIS_POLICY,
            ORACLE_INTENT_AND_GAPS_POLICY,
            ORACLE_NO_REVERSE_ENGINEERING_POLICY,
            ORACLE_IMPLEMENTATION_CONSTRAINT_POLICY,
            ORACLE_CONSISTENCY_AND_SEARCHABILITY_POLICY,
        ),
    )
    return PolicyCollection(
        groups=(ORACLE_AUTHORITY_POLICY_GROUP, oracle_group),
    )


@cache
def build_oracle_investigation_policy() -> PolicyCollection:
    """oracle file の読み取り専用調査に必要な規定だけを選択する。"""
    investigation_group = PolicyGroup(
        group_id="20.oracle_investigation",
        title="oracle investigation policy",
        scope="oracle file の読み取り専用調査時",
        policies=(
            ORACLE_AUTHORITATIVE_BASIS_POLICY,
            ORACLE_NO_REVERSE_ENGINEERING_POLICY,
            ORACLE_DEFINED_AND_UNDEFINED_POLICY,
        ),
    )
    return PolicyCollection(
        groups=(ORACLE_AUTHORITY_CORE_POLICY_GROUP, investigation_group),
    )
