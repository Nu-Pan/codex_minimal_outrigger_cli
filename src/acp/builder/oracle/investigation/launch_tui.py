"""oracle investigation の正本 builder を公開する互換 import 経路。

既存の `acp.builder.oracle.investigation.launch_tui` import を維持する間だけ残し、
呼び出し元が `oracle.*` へ移行したら削除する。
"""

from oracle.acp_builder.oracle.investigation.launch_tui import (
    build_oracle_investigation_launch_tui_parameter,
)

# {{work-root}}/oracle/src/oracle/acp_builder/oracle/investigation/launch_tui.py
__all__ = ["build_oracle_investigation_launch_tui_parameter"]
