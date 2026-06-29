"""Compatibility import path for TUI resolve-parameter building.

Kept while callers import from `acp.builder.tui.resolve_parameter`; the
canonical builder is
`<work-root>/oracle/src/oracle/acp_builder/tui/resolve_parameter.py`.
Delete this module after callers use the canonical oracle path.
"""

from oracle.acp_builder.tui.resolve_parameter import (
    build_tui_resolve_parameter_parameter,
)

__all__ = ["build_tui_resolve_parameter_parameter"]
