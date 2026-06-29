"""Compatibility import path for review finding judgment.

Kept while callers import from `acp.builder.review.oracle.judge_finding`;
the canonical implementation is
`<work-root>/oracle/src/oracle/acp_builder/review/oracle/judge_finding.py`.
Delete this module after all callers use the canonical oracle path directly.
"""

from oracle.acp_builder.review.oracle.judge_finding import *  # noqa: F403
