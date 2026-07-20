"""TUI resolve-parameter building の互換 import 経路。

`acp.builder.tui.resolve_parameter` から import する caller が残る間だけ維持する。
canonical builder は
`{{work-root}}/oracle/src/oracle/acp_builder/tui/resolve_parameter.py` にある。
"""

from oracle.acp_builder.tui.resolve_parameter import (
    build_tui_resolve_parameter_parameter,
)

__all__ = ["build_tui_resolve_parameter_parameter"]
