from pathlib import Path

import typer

from cmoc_runtime import (
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
        # requires the current worktree, not the main worktree, to be clean.
        use_work_root_runtime=True,
    )


def _cmoc_indexing_body(
    codex_exec: CodexExec | None = None,
) -> None:
    """現在の work root に対して INDEX.md の maintenance を実行する。"""
    root = work_root()
    with indexing_lock(root):
        start_subcommand_step(2, "インデクシングを明示的に実行", "run indexing")
        updated = update_indexes(root, codex_exec)
        start_subcommand_step(
            3, "インデクシング差分を commit", "commit indexing changes"
        )
        commit_index_updates(root, updated)
    typer.echo(f"# cmoc indexing\n- updated_index_count: `{len(updated)}`")


def require_indexing_cli_preconditions(root: Path) -> None:
    """indexing CLI 実行前に worktree の安全条件を検査する。"""
    require_cmoc_ignored(root)
    require_clean_worktree(root)
