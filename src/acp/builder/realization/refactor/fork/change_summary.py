"""realization refactor の change summary builder を再公開する互換入口。

対応する oracle file:
`{{work-root}}/oracle/src/oracle/acp_builder/realization/refactor/fork/change_summary.py`。
"""

from oracle.acp_builder.realization.refactor.fork.change_summary import (
    build_realization_refactor_fork_change_summary_parameter,
)

__all__ = ["build_realization_refactor_fork_change_summary_parameter"]
