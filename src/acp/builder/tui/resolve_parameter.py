"""Compatibility import path for TUI resolve-parameter building.

Kept while callers import from `acp.builder.tui.resolve_parameter`; the
canonical builder is
`<work-root>/oracle/src/oracle/acp_builder/tui/resolve_parameter.py`, while
`TUI_FILE_ACCESS_MODES` exposes the canonical `FileAccessMode` choices for the
existing TUI import surface. Delete this module after callers use the canonical
oracle path and no longer need this exported mode tuple.
"""

from oracle.acp_builder.basic import FileAccessMode
from oracle.acp_builder.tui.resolve_parameter import (
    build_tui_resolve_parameter_parameter,
)

TUI_FILE_ACCESS_MODES = tuple(FileAccessMode)

__all__ = ["build_tui_resolve_parameter_parameter", "TUI_FILE_ACCESS_MODES"]
