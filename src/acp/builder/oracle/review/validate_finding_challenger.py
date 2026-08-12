"""oracle review challenger validation の互換 import 経路。

`acp.builder.oracle.review.validate_finding_challenger` から import する caller が
残る間だけ維持する。canonical 実装は
`{{work-root}}/oracle/src/oracle/acp_builder/oracle/review/validate_finding_challenger.py`。
"""

from oracle.acp_builder.oracle.review.validate_finding_challenger import (
    build_oracle_review_validate_finding_challenger_parameter,
)

__all__ = ["build_oracle_review_validate_finding_challenger_parameter"]
