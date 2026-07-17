"""challenger finding validation の互換 import 経路。

`acp.builder.review.oracle.validate_finding_challenger` から import する caller が残る間だけ
維持する。canonical 実装は
`{{work-root}}/oracle/src/oracle/acp_builder/review/oracle/validate_finding_challenger.py`。
全 caller が canonical oracle path を直接使うようになったら削除する。
"""

from oracle.acp_builder.review.oracle.validate_finding_challenger import (
    build_review_oracle_validate_finding_challenger_parameter,
)

__all__ = ["build_review_oracle_validate_finding_challenger_parameter"]
