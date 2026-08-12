"""oracle review advocate validation の互換 import 経路。

canonical 実装は
`{{work-root}}/oracle/src/oracle/acp_builder/oracle/review/validate_finding_advocate.py`。
"""

from oracle.acp_builder.oracle.review.validate_finding_advocate import (
    build_oracle_review_validate_finding_advocate_parameter,
)

__all__ = ["build_oracle_review_validate_finding_advocate_parameter"]
