"""Compatibility import path for challenger finding validation.

Kept while callers import from
`acp.builder.review.oracle.validate_finding_challenger`; the canonical
implementation is
`{{work-root}}/oracle/src/oracle/acp_builder/review/oracle/validate_finding_challenger.py`.
Delete this module after all callers use the canonical oracle path directly.
"""

from oracle.acp_builder.review.oracle.validate_finding_challenger import (
    build_review_oracle_validate_finding_challenger_parameter,
)

__all__ = ["build_review_oracle_validate_finding_challenger_parameter"]
