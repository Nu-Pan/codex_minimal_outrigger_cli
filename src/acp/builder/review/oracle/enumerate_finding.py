"""Compatibility import path for review finding enumeration.

Kept while callers import from `acp.builder.review.oracle.enumerate_finding`;
the canonical implementation is
`<work-root>/oracle/src/oracle/acp_builder/review/oracle/enumerate_finding.py`.
Delete this module after all callers use the canonical oracle path directly.
"""

from oracle.acp_builder.review.oracle.enumerate_finding import (
    build_review_oracle_enumerate_finding_parameter,
)

__all__ = ["build_review_oracle_enumerate_finding_parameter"]
