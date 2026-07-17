"""TUI resolve-parameter building の互換 import 経路。

`acp.builder.tui.resolve_parameter` から import する caller が残る間だけ維持する。
canonical builder は
`{{work-root}}/oracle/src/oracle/acp_builder/tui/resolve_parameter.py` であり、
`TUI_FILE_ACCESS_MODES` は既存 TUI import surface のため canonical `FileAccessMode` 選択肢を
公開する。caller が canonical oracle path を使い、この exported mode tuple を不要としたら削除する。
"""

from oracle.acp_builder.basic import FileAccessMode
from oracle.acp_builder.tui.resolve_parameter import (
    build_tui_resolve_parameter_parameter,
)

TUI_FILE_ACCESS_MODES: tuple[FileAccessMode, ...] = tuple(
    mode for mode in FileAccessMode if mode != FileAccessMode.NO_RULE
)

__all__ = ["build_tui_resolve_parameter_parameter", "TUI_FILE_ACCESS_MODES"]
