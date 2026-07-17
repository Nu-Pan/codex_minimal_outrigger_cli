"""review finding judgment の互換 import 経路。

`acp.builder.review.oracle.judge_finding` から import する caller が残る間だけ維持する。
canonical 実装は
`{{work-root}}/oracle/src/oracle/acp_builder/review/oracle/judge_finding.py`。
全 caller が canonical oracle path を直接使うようになったら削除する。
"""

from oracle.acp_builder.review.oracle.judge_finding import (
    build_review_oracle_judge_finding_parameter,
)

__all__ = ["build_review_oracle_judge_finding_parameter"]
