"""session join conflict resolution の互換 import 経路。

`acp.builder.session.join.conflict_resolution` から import する caller が残る間だけ維持する。
canonical 実装は
`{{work-root}}/oracle/src/oracle/acp_builder/session/join/conflict_resolution.py`。
全 caller が canonical oracle path を直接使うようになったら削除する。
"""

from oracle.acp_builder.session.join.conflict_resolution import (
    build_session_join_conflict_resolution_parameter,
)

__all__ = ["build_session_join_conflict_resolution_parameter"]
