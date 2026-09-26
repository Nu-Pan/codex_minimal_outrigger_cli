"""editing run 共通 helper の旧 import path を保つ薄い shim。"""

# canonical 実装は共通処理の配置規則に従い commons に置く。
# {{work-root}}/oracle/doc/dev_rule/design_rule.md
# 旧 import path を利用する利用者が commons 側へ移行し、互換性が不要になった時に
# この shim と対応する INDEX entry を削除する。
# {{work-root}}/oracle/doc/app_spec/oracle_and_realization.md の
# 「realization file を扱う判断基準」
from commons.runtime_run_lifecycle import (
    EditingRunContext,
    GitChange,
    commit_work_unit,
    flattened_change_paths,
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

__all__ = [
    "EditingRunContext",
    "GitChange",
    "commit_work_unit",
    "flattened_change_paths",
    "require_ready_session",
    "resolve_active_run",
    "rollback_work_unit",
    "set_run_state",
    "start_editing_run",
    "tree_changes",
    "unexpected_agent_paths",
    "unexpected_run_paths",
    "worktree_change_paths",
]
