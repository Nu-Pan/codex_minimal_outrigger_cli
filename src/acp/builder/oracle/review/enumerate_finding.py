"""oracle review finding enumeration の互換 import 経路。

`acp.builder.oracle.review.enumerate_finding` から import する呼び出し元が
残る間だけ維持する。canonical 実装は
`{{work-root}}/oracle/src/oracle/acp_builder/oracle/review/enumerate_finding.py`。
"""

from oracle.acp_builder.oracle.review.enumerate_finding import (
    build_oracle_review_enumerate_finding_parameter,
)

__all__ = ["build_oracle_review_enumerate_finding_parameter"]
