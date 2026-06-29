"""`cmoc apply fork` のファイル単位所見列挙 builder。"""

from pathlib import Path

from acp.builder.apply.fork._common import (
    adapt_oracle_parameter,
    ensure_oracle_src_importable,
    resolve_repo_root,
)
from basic.acp import AgentCallParameter


def build_apply_fork_file_finding_enumeration_parameter(
    target_path: Path,
) -> AgentCallParameter:
    """所見列挙用 agent call parameter を構築する。"""
    repo_root = resolve_repo_root()
    ensure_oracle_src_importable(repo_root)

    from oracle.acp_builder.apply.fork.file_finding_enumeration import (
        build_apply_fork_file_finding_enumeration_parameter as build_oracle_parameter,
    )

    return adapt_oracle_parameter(
        build_oracle_parameter(target_path),
        Path(__file__).with_suffix(".json"),
    )
