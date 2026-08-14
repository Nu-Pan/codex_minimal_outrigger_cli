"""realization apply fork の正本 builder を再公開する互換入口。

対応する oracle file:
`{{work-root}}/oracle/src/oracle/acp_builder/realization/apply/fork/launch_exec.py`。

既存の `acp.builder.realization.apply.fork.launch_exec` 参照を維持するために残す。
削除条件は realization 側と利用者向け公開面から同参照がなくなること。
"""

from oracle.acp_builder.realization.apply.fork.launch_exec import (
    build_realization_apply_fork_launch_exec_parameter,
)

__all__ = ["build_realization_apply_fork_launch_exec_parameter"]
