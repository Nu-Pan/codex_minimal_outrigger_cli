"""
`cmoc apply fork` の変更要約生成 builder。

Oracle: <work-root>/oracle/src/oracle/acp_builder/apply/fork/change_summary.py
"""

import json
import shlex
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

    return adapt_oracle_parameter(build_oracle_parameter(raw_git_diff))


def build_acp_change_summary_file(
    acp_branch_diff_file: str | Path, acp_change_summary_file: str | Path
) -> None:
    # Oracle: <work-root>/oracle/src/oracle/acp_builder/apply/fork/change_summary.py
    raw_diff = Path(acp_branch_diff_file).read_text()
    paths = _changed_paths_from_diff(raw_diff)
    payload = {
        "changes": [
            {
                "category": "ACP branch diff" if paths else "変更なし",
                "summary": (
                    "ACP branch diff から変更 path を機械的に記録しました。"
                    if paths
                    else "ACP branch diff に変更はありません。"
                ),
                "changed_paths": paths,
            }
        ]
    }
    output = Path(acp_change_summary_file)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")


def _changed_paths_from_diff(raw_diff: str) -> list[str]:
    paths: list[str] = []
    for line in raw_diff.splitlines():
        if not line.startswith("diff --git "):
            continue
        parts = shlex.split(line)
        if len(parts) < 4:
            continue
        path = _diff_path(parts[3]) or _diff_path(parts[2])
        if path and path not in paths:
            paths.append(path)
    return paths


def _diff_path(token: str) -> str:
    if token == "/dev/null":
        return ""
    return token[2:] if token.startswith(("a/", "b/")) else token
