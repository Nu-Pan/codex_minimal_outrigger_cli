"""realization file を扱う agent call 向け instruction 文面の構築定義。"""

from functools import cache

from oracle.other.standard import StandardCollection, StandardGroup

from .common_standard import ORACLE_AUTHORITY_STANDARD_GROUP
from .standard_definitions import (
    REALIZATION_CURRENT_SPEC_ONLY_STANDARD,
    REALIZATION_ORACLE_CONFORMANCE_STANDARD,
    REALIZATION_REPOSITORY_VERIFICATION_STANDARD,
)


@cache
def build_realization_standard() -> StandardCollection:
    """realization file の作成・変更・レビューに必要な規範を選択する。"""
    realization_group = StandardGroup(
        group_id="30.realization",
        title="realization standard",
        scope="realization file の作成・変更・リファクタ・レビュー時",
        standards=(
            REALIZATION_ORACLE_CONFORMANCE_STANDARD,
            REALIZATION_CURRENT_SPEC_ONLY_STANDARD,
            REALIZATION_REPOSITORY_VERIFICATION_STANDARD,
        ),
    )
    return StandardCollection(
        groups=(ORACLE_AUTHORITY_STANDARD_GROUP, realization_group),
    )
