"""oracle file を扱う agent call 向け instruction 文面の構築定義。"""

from functools import cache

from oracle.other.standard import StandardCollection, StandardGroup

from .common_standard import (
    ORACLE_AUTHORITY_CORE_STANDARD_GROUP,
    ORACLE_AUTHORITY_STANDARD_GROUP,
)
from .standard_definitions import (
    ORACLE_AUTHORITATIVE_BASIS_STANDARD,
    ORACLE_CONSISTENCY_AND_SEARCHABILITY_STANDARD,
    ORACLE_DEFINED_AND_UNDEFINED_STANDARD,
    ORACLE_EDIT_AUTHORITATIVE_BASIS_STANDARD,
    ORACLE_IMPLEMENTATION_CONSTRAINT_STANDARD,
    ORACLE_INTENT_AND_GAPS_STANDARD,
    ORACLE_NO_REVERSE_ENGINEERING_STANDARD,
)


@cache
def build_oracle_standard() -> StandardCollection:
    """oracle file の作成・変更・レビューに必要な規範を選択する。"""
    oracle_group = StandardGroup(
        group_id="20.oracle",
        title="oracle standard",
        scope="oracle file の作成・変更・レビュー時",
        standards=(
            ORACLE_AUTHORITATIVE_BASIS_STANDARD,
            ORACLE_EDIT_AUTHORITATIVE_BASIS_STANDARD,
            ORACLE_INTENT_AND_GAPS_STANDARD,
            ORACLE_NO_REVERSE_ENGINEERING_STANDARD,
            ORACLE_IMPLEMENTATION_CONSTRAINT_STANDARD,
            ORACLE_CONSISTENCY_AND_SEARCHABILITY_STANDARD,
        ),
    )
    return StandardCollection(
        groups=(ORACLE_AUTHORITY_STANDARD_GROUP, oracle_group),
    )


@cache
def build_oracle_investigation_standard() -> StandardCollection:
    """oracle file の読み取り専用調査に必要な規範だけを選択する。"""
    investigation_group = StandardGroup(
        group_id="20.oracle_investigation",
        title="oracle investigation standard",
        scope="oracle file の読み取り専用調査時",
        standards=(
            ORACLE_AUTHORITATIVE_BASIS_STANDARD,
            ORACLE_NO_REVERSE_ENGINEERING_STANDARD,
            ORACLE_DEFINED_AND_UNDEFINED_STANDARD,
        ),
    )
    return StandardCollection(
        groups=(ORACLE_AUTHORITY_CORE_STANDARD_GROUP, investigation_group),
    )
