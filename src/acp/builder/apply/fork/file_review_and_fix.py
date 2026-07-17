"""`cmoc apply fork` のファイル単位レビュー・修正 builder。

Oracle: {{work-root}}/oracle/src/oracle/acp_builder/apply/fork/file_review_and_fix.py
"""

from pathlib import Path

from acp.builder.apply.fork._common import (
    adapt_oracle_parameter,
    ensure_oracle_src_importable,
    resolve_repo_root,
)
from basic.acp import AgentCallParameter


def build_apply_fork_file_review_and_fix_parameter(
    target_path: Path,
) -> AgentCallParameter:
    """ファイル単位レビュー・修正用 agent call parameter を構築する。"""
    repo_root = resolve_repo_root()
    ensure_oracle_src_importable(repo_root)

    from oracle.acp_builder.apply.fork.file_review_and_fix import (
        build_apply_fork_file_review_and_fix_parameter as build_oracle_parameter,
    )

    return adapt_oracle_parameter(build_oracle_parameter(target_path))
