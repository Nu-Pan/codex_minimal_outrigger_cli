"""quota availability probe の canonical builder への互換入口。

`acp.builder.quota_probe` を参照する caller が残る間だけ維持する。
canonical 実装は
`{{work-root}}/oracle/src/oracle/acp_builder/quota_probe.py`。
"""

from oracle.acp_builder.basic import AgentCallParameter as _AgentCallParameter
from oracle.acp_builder.quota_probe import (
    build_quota_availability_probe_parameter as _build_parameter,
)

__all__ = ["build_quota_availability_probe_parameter"]


def build_quota_availability_probe_parameter(
    base_parameter: _AgentCallParameter,
) -> _AgentCallParameter:
    """既存 API の base parameter から probe の cwd を正本 builder へ渡す。"""
    return _build_parameter(base_parameter.agent_call_cwd)
