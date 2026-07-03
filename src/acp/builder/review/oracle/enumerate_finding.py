"""review finding enumeration の互換 import 経路。

`acp.builder.review.oracle.enumerate_finding` から import する呼び出し元が
残る間だけ維持する。canonical 実装は
`<work-root>/oracle/src/oracle/acp_builder/review/oracle/enumerate_finding.py`。
全呼び出し元が canonical oracle path を直接使うようになったら削除できる。
"""

from oracle.acp_builder.review.oracle.enumerate_finding import (
    build_review_oracle_enumerate_finding_parameter,
)

__all__ = ["build_review_oracle_enumerate_finding_parameter"]
