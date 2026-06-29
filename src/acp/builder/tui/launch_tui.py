from dataclasses import replace

from oracle.acp_builder.tui.launch_tui import (
    build_tui_launch_tui_parameter as _build_tui_launch_tui_parameter,
)


def build_tui_launch_tui_parameter(*args, **kwargs):
    # <work-root>/oracle/src/oracle/acp_builder/tui/launch_tui.py
    # The oracle fragment currently points at a non-existent launch_tui.json.
    # TUI launch does not consume Structured Output, so expose the runtime-safe
    # contract allowed by AgentCallParameter instead of publishing a dead path.
    return replace(
        _build_tui_launch_tui_parameter(*args, **kwargs),
        structured_output_schema_path=None,
    )


__all__ = ["build_tui_launch_tui_parameter"]
