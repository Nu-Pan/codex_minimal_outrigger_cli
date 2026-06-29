"""`<work-root>/oracle/src/oracle/acp_builder/tui/launch_tui.py` を再公開する。

TUI 起動パラメータの正本を oracle 側に保ったまま既存の
`acp.builder.tui.launch_tui` 参照を成立させるために残す。削除条件は
realization 側と利用者向け公開面からこの import path 参照がなくなること。
"""

from oracle.acp_builder.tui.launch_tui import (
    build_tui_launch_tui_parameter,
)


__all__ = ["build_tui_launch_tui_parameter"]
