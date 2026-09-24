"""work root の INDEX.md を更新して commit する CLI 入口を提供する。"""

from pathlib import Path

from cmoc_runtime import (
    TerminalResult,
    head_commit,
    require_clean_worktree,
    require_cmoc_ignored,
    run_cli_subcommand,
    run_codex_exec,
    start_subcommand_step,
    work_root,
)
from commons.indexing import (
    CodexExec,
    commit_index_updates,
    enable_indexing_preflight,
    indexing_lock,
    update_indexes,
)
from commons.runtime_primary_report import update_primary_report_fields


def cmoc_indexing_impl() -> None:
    """CLI runtime を通して indexing subcommand を実行する。"""
    enable_indexing_preflight()
    run_cli_subcommand(
        _cmoc_indexing_body,
        codex_exec=run_codex_exec,
        pre_log_check=require_indexing_cli_preconditions,
        command_name="indexing",
        command_argv=["cmoc", "indexing"],
        total_steps=3,
        # `{{work-root}}/oracle/doc/app_spec/sub_command/indexing.md`
        # main worktree ではなく current worktree が clean であることを求める。
        use_work_root_runtime=True,
    )


def _cmoc_indexing_body(
    codex_exec: CodexExec | None = None,
) -> TerminalResult:
    """現在の work root に対して INDEX.md の maintenance を実行する。"""
    root = work_root()
    with indexing_lock(root):
        commit_before_indexing = head_commit(root)
        start_subcommand_step(2, "インデクシングを明示的に実行", "run indexing")
        update_primary_report_fields(
            indexing_status="started",
            updated_indexes=[],
        )
        try:
            updated = update_indexes(root, codex_exec)
        except KeyboardInterrupt:
            update_primary_report_fields(indexing_status="interrupted")
            raise
        except BaseException:
            update_primary_report_fields(indexing_status="failed")
            raise
        updated_indexes = [str(path.relative_to(root)) for path in updated]
        update_primary_report_fields(
            indexing_status="completed",
            updated_indexes=updated_indexes,
        )
        start_subcommand_step(
            3, "インデクシング差分を commit", "commit indexing changes"
        )
        update_primary_report_fields(
            commit_status="not_needed" if not updated else "started"
        )
        try:
            commit_index_updates(root, updated)
        except KeyboardInterrupt:
            update_primary_report_fields(commit_status="interrupted")
            raise
        except BaseException:
            update_primary_report_fields(commit_status="failed")
            raise
        commit_after_indexing = head_commit(root)
    commit_id = (
        commit_after_indexing
        if commit_after_indexing != commit_before_indexing
        else None
    )
    update_primary_report_fields(
        commit_id=commit_id,
        commit_status="completed" if updated else "not_needed",
    )
    return TerminalResult(
        details=(
            ("updated_index_count", len(updated)),
            ("commit_id", commit_id),
            ("updated_indexes", updated_indexes),
        )
    )


def require_indexing_cli_preconditions(root: Path) -> None:
    """indexing CLI 実行前に worktree の安全条件を検査する。"""
    require_cmoc_ignored(root)
    require_clean_worktree(root)
