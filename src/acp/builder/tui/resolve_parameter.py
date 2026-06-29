from oracle.acp_builder.basic import FileAccessMode
from oracle.acp_builder.tui.resolve_parameter import (
    build_tui_resolve_parameter_parameter,
)

TUI_FILE_ACCESS_MODES = tuple(FileAccessMode)

__all__ = ["build_tui_resolve_parameter_parameter", "TUI_FILE_ACCESS_MODES"]
