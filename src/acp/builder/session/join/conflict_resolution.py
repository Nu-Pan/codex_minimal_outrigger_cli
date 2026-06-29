"""Compatibility import path for session join conflict resolution.

Kept while callers import from `acp.builder.session.join.conflict_resolution`;
the canonical implementation is
`<work-root>/oracle/src/oracle/acp_builder/session/join/conflict_resolution.py`.
Delete this module after all callers use the canonical oracle path directly.
"""

from oracle.acp_builder.session.join.conflict_resolution import *  # noqa: F403
