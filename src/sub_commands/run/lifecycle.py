"""editing run 共通 helper の旧 import path を保つ薄い shim。"""

# canonical 実装は共通処理の配置規則に従い commons に置く。
# {{work-root}}/oracle/doc/dev_rule/design_rule.md
# 旧 import path を利用する利用者が commons 側へ移行し、互換性が不要になった時に
# この shim と対応する INDEX entry を削除する。
# {{work-root}}/oracle/src/oracle/prompt_builder/parts/realization_standard.py
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
    unexpected_run_paths,
    unexpected_session_paths,
    worktree_change_paths,
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
    "unexpected_run_paths",
    "unexpected_session_paths",
    "worktree_change_paths",
]
