"""editing run 共通 helper の旧 import path を保つ薄い shim。"""

from collections.abc import Collection
from pathlib import Path

# canonical 実装は共通処理の配置規則に従い commons に置く。
# {{work-root}}/oracle/doc/dev_rule/design_rule.md
# 旧 import path を利用する利用者が commons 側へ移行し、互換性が不要になった時に
# この shim と対応する INDEX entry を削除する。
# {{work-root}}/oracle/src/oracle/prompt_builder/policy/realization.py
from commons.runtime_run_lifecycle import (
    EditingRunContext,
    GitChange,
    commit_work_unit,
    flattened_change_paths,
    raw_oracle_diff,
    refresh_indexes,
    require_ready_session,
    resolve_active_run,
    rollback_work_unit,
    set_run_state,
    start_editing_run,
    tree_changes,
    unexpected_agent_paths,
    unexpected_run_paths,
    worktree_change_paths,
)
from commons.runtime_run_lifecycle import (
    unexpected_session_paths as _canonical_unexpected_session_paths,
)


def unexpected_session_paths(
    session_worktree: Path,
    changes: list[GitChange],
    *,
    base: str = "HEAD",
    ignored_paths: Collection[str] = (),
) -> list[str]:
    """旧 import path の base 省略呼び出しを canonical helper へ委譲する。"""
    return _canonical_unexpected_session_paths(
        session_worktree,
        changes,
        base=base,
        ignored_paths=ignored_paths,
    )


__all__ = [
    "EditingRunContext",
    "GitChange",
    "commit_work_unit",
    "flattened_change_paths",
    "refresh_indexes",
    "raw_oracle_diff",
    "require_ready_session",
    "resolve_active_run",
    "rollback_work_unit",
    "set_run_state",
    "start_editing_run",
    "tree_changes",
    "unexpected_agent_paths",
    "unexpected_run_paths",
    "unexpected_session_paths",
    "worktree_change_paths",
]
