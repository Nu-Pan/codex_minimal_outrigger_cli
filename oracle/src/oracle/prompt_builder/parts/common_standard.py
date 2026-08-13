"""複数用途で共有する StandardGroup の構成定義。"""

from oracle.other.standard import StandardGroup

from .standard_definitions import (
    FINDING_BASIS_EVIDENCE_STANDARD,
    ORACLE_AUTHORITY_NO_REVERSE_FLOW_STANDARD,
    ORACLE_AUTHORITY_STANDARD,
)

ORACLE_AUTHORITY_CORE_STANDARD_GROUP = StandardGroup(
    group_id="10.oracle_authority",
    title="oracle authority standard",
    scope="oracle・realization file を扱う時",
    standards=(ORACLE_AUTHORITY_STANDARD,),
)

ORACLE_AUTHORITY_STANDARD_GROUP = StandardGroup(
    group_id=ORACLE_AUTHORITY_CORE_STANDARD_GROUP.group_id,
    title=ORACLE_AUTHORITY_CORE_STANDARD_GROUP.title,
    scope=ORACLE_AUTHORITY_CORE_STANDARD_GROUP.scope,
    standards=(
        *ORACLE_AUTHORITY_CORE_STANDARD_GROUP.standards,
        ORACLE_AUTHORITY_NO_REVERSE_FLOW_STANDARD,
    ),
)


FINDING_BASIS_STANDARD_GROUP = StandardGroup(
    group_id="40.finding_basis",
    title="finding basis standard",
    scope="所見・修正対象の判断時",
    standards=(FINDING_BASIS_EVIDENCE_STANDARD,),
)
