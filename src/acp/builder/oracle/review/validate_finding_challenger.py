"""oracle review challenger validation の realization adapter。

`acp.builder.oracle.review.validate_finding_challenger` から import する caller が残る間だけ
維持する。canonical 実装は
`{{work-root}}/oracle/src/oracle/acp_builder/oracle/review/validate_finding_challenger.py`。
全 caller が canonical oracle path を直接使うようになったら削除する。
"""

from oracle.acp_builder.oracle.review.validate_finding_challenger import (
    build_oracle_review_validate_finding_challenger_parameter,
)

__all__ = ["build_oracle_review_validate_finding_challenger_parameter"]
