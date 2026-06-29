"""`cmoc apply fork` の変更要約生成 builder。"""

from pathlib import Path

from acp.builder.apply.fork._common import (
    adapt_oracle_parameter,
    ensure_oracle_src_importable,
    resolve_repo_root,
)
from basic.acp import AgentCallParameter


def build_apply_fork_change_summary_parameter(raw_git_diff: str) -> AgentCallParameter:
    """作業レポート用の変更要約 agent call parameter を構築する。"""
    repo_root = resolve_repo_root()
    ensure_oracle_src_importable(repo_root)

    from oracle.acp_builder.apply.fork.change_summary import (
        build_apply_fork_change_summary_parameter as build_oracle_parameter,
    )

    return adapt_oracle_parameter(
        build_oracle_parameter(raw_git_diff),
        Path(__file__).with_suffix(".json"),
    )
