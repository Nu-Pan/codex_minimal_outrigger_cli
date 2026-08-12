"""oracle review finding judgment の互換 import 経路。

`acp.builder.oracle.review.judge_finding` から import する caller が残る間だけ
維持する。canonical 実装は
`{{work-root}}/oracle/src/oracle/acp_builder/oracle/review/judge_finding.py`。
"""

from oracle.acp_builder.oracle.review.judge_finding import (
    build_oracle_review_judge_finding_parameter,
)

__all__ = ["build_oracle_review_judge_finding_parameter"]
