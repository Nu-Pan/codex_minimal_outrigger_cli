from pathlib import Path

import typer

from cmoc_runtime import (
    require_clean_worktree,
    require_cmoc_ignored,
    run_cli_subcommand,
    run_codex_exec,
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
    )


def _cmoc_indexing_body(
    codex_exec: CodexExec | None = None,
) -> None:
    """現在の work root に対して INDEX.md の maintenance を実行する。"""
    root = work_root()
    with indexing_lock(root):
        updated = update_indexes(root, codex_exec)
        commit_index_updates(root, updated)
    typer.echo(f"# cmoc indexing\n- updated_index_count: `{len(updated)}`")


def require_indexing_cli_preconditions(root: Path) -> None:
    """indexing CLI 実行前に worktree の安全条件を検査する。"""
    require_cmoc_ignored(root)
    require_clean_worktree(root)
