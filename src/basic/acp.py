"""`<work-root>/oracle/src/oracle/acp_builder/basic.py` の ACP 型を再公開する。

正本型を realization 側へ複製せず既存の `basic.acp` 参照を保つために残す。
削除条件は realization 側と利用者向け公開面から `basic.acp` 参照がなくなること。
"""

from dataclasses import dataclass

from oracle.acp_builder.basic import (
    AgentCallParameter as OracleAgentCallParameter,
    FileAccessMode,
    ModelClass,
    ReasoningEffort,
)


@dataclass(frozen=True)
class AgentCallParameter(OracleAgentCallParameter):
    """旧 `basic.acp` 経由の直接生成に既定 preflight 挙動を足す互換型。"""

    run_indexing_preflight: bool = True


__all__ = [
    "AgentCallParameter",
    "FileAccessMode",
    "ModelClass",
    "ReasoningEffort",
]
