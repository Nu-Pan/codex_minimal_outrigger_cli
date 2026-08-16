"""複数用途で共有する PolicyGroup の構成定義。"""

from oracle.other.policy import PolicyGroup

from .policy_definitions import (
    FINDING_BASIS_EVIDENCE_POLICY,
    ORACLE_AUTHORITY_NO_REVERSE_FLOW_POLICY,
    ORACLE_AUTHORITY_POLICY,
)

ORACLE_AUTHORITY_CORE_POLICY_GROUP = PolicyGroup(
    group_id="10.oracle_authority",
    title="oracle authority policy",
    scope="oracle・realization file を扱う時",
    policies=(ORACLE_AUTHORITY_POLICY,),
)

ORACLE_AUTHORITY_POLICY_GROUP = PolicyGroup(
    group_id=ORACLE_AUTHORITY_CORE_POLICY_GROUP.group_id,
    title=ORACLE_AUTHORITY_CORE_POLICY_GROUP.title,
    scope=ORACLE_AUTHORITY_CORE_POLICY_GROUP.scope,
    policies=(
        *ORACLE_AUTHORITY_CORE_POLICY_GROUP.policies,
        ORACLE_AUTHORITY_NO_REVERSE_FLOW_POLICY,
    ),
)


FINDING_BASIS_POLICY_GROUP = PolicyGroup(
    group_id="40.finding_basis",
    title="finding basis policy",
    scope="所見・修正対象の判断時",
    policies=(FINDING_BASIS_EVIDENCE_POLICY,),
)
