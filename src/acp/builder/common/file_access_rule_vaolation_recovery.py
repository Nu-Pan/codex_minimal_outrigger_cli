"""
ファイルアクセス規則違反 recovery builder の互換 wrapper。

Oracle: <work-root>/oracle/src/oracle/acp_builder/common/file_access_rule_vaolation_recovery.py
"""

from pathlib import Path

from acp.builder.apply.fork._common import (
    adapt_oracle_parameter,
    ensure_oracle_src_importable,
    resolve_repo_root,
)
from basic.acp import AgentCallParameter, FileAccessMode


def build_file_access_rule_vaolation_recovery_parameter(
    violated_agent_call_log: Path,
    violated_file_list: list[Path],
    violated_file_access_mode: FileAccessMode,
) -> AgentCallParameter:
    """正本側 recovery builder から agent call parameter を取得する。"""
    ensure_oracle_src_importable(resolve_repo_root())

    from oracle.acp_builder.common.file_access_rule_vaolation_recovery import (
        build_file_access_rule_vaolation_recovery_parameter as build_oracle_parameter,
    )

    return adapt_oracle_parameter(
        build_oracle_parameter(
            violated_agent_call_log,
            violated_file_list,
            violated_file_access_mode,
        )
    )


__all__ = ["build_file_access_rule_vaolation_recovery_parameter"]
