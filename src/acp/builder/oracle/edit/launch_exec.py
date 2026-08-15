"""oracle edit の正本 exec builder を公開する互換 import 経路。"""

from oracle.acp_builder.oracle.edit.launch_exec import (
    build_oracle_edit_main_launch_exec_parameter,
    build_oracle_edit_reduction_launch_exec_parameter,
)

# {{work-root}}/oracle/src/oracle/acp_builder/oracle/edit/launch_exec.py
__all__ = [
    "build_oracle_edit_main_launch_exec_parameter",
    "build_oracle_edit_reduction_launch_exec_parameter",
]
