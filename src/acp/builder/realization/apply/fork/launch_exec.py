"""realization apply fork の正本 builder を再公開する互換入口。

対応する oracle file:
`{{work-root}}/oracle/src/oracle/acp_builder/realization/apply/fork/launch_exec.py`。
"""

from oracle.acp_builder.realization.apply.fork.launch_exec import (
    build_realization_apply_fork_launch_exec_parameter,
)

__all__ = ["build_realization_apply_fork_launch_exec_parameter"]
