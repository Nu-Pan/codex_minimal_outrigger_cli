"""oracle review finding judgment の realization adapter。

`acp.builder.oracle.review.judge_finding` から import する caller が残る間だけ維持する。
canonical 実装は
`{{work-root}}/oracle/src/oracle/acp_builder/oracle/review/judge_finding.py`。
全 caller が canonical oracle path を直接使うようになったら削除する。
"""

from oracle.acp_builder.oracle.review.judge_finding import (
    build_oracle_review_judge_finding_parameter,
)

__all__ = ["build_oracle_review_judge_finding_parameter"]
