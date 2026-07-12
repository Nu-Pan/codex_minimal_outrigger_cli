from pathlib import Path
from typing import Callable

import typer

from cmoc_runtime import (
    CmocError,
    create_run_worktree,
    current_branch,
    delete_branch,
    ensure_cmoc_ignored,
    head_commit,
    load_config,
    load_state_for_branch,
    pushd,
    remove_worktree,
    repo_root,
    run_cli_subcommand,
    start_subcommand_step,
    run_codex_exec,
    timestamp,
    work_root,
    worktrees_dir,
)
from sub_commands.review_index import (
    commit_review_index_changes,
    merge_review_branch,
    review_branch_has_index_changes,
    resolve_review_index_conflicts,
    review_worktree_status_paths,
)
from sub_commands.review_loop import (
    apply_finding_merge_operations,
    run_review_oracle_loop,
)
from sub_commands.review_report import (
    path_display,
    render_finding_section,
    render_review_oracle_report,
    write_review_oracle_report,
)
from sub_commands.review_targets import (
    enumerate_review_all_oracle_files,
    enumerate_review_oracle_targets,
)
from commons.indexing import enable_indexing_preflight
from commons.runtime_git import status_path_statuses


CodexExec = Callable[..., object]

__all__ = [
    "CodexExec",
    "apply_finding_merge_operations",
    "cmoc_review_oracle_impl",
    "commit_review_index_changes",
    "enumerate_review_all_oracle_files",
    "enumerate_review_oracle_targets",
    "merge_review_branch",
    "path_display",
    "render_finding_section",
    "render_review_oracle_report",
    "resolve_review_index_conflicts",
    "review_worktree_status_paths",
    "run_review_oracle_loop",
    "write_review_oracle_report",
]


def cmoc_review_oracle_impl(scope: str) -> None:
    """CLI runtime を通して review oracle を実行する。"""
    enable_indexing_preflight()
    run_cli_subcommand(
        _cmoc_review_oracle_body,
        scope,
        run_codex_exec,
        command_name="review oracle",
        command_argv=["cmoc", "review", "oracle", "--scope", scope],
        total_steps=8,
    )


def _cmoc_review_oracle_body(
    scope: str,
    codex_exec: CodexExec,
) -> None:
    """現在の session branch の oracle を isolated review worktree 上でレビューする。"""
    root = repo_root()
    current_root = work_root()
    branch = current_branch(current_root)
    session_id, _state_path, state = load_state_for_branch(root, branch)
    if not branch.startswith("cmoc/session/") or state.session.state != "active":
        raise CmocError("review oracle は active session branch 上で実行してください。", [], branch)
    _require_clean_worktree(current_root)
    ensure_cmoc_ignored(current_root)
    config = load_config(root)
    run_id = timestamp()
    review_branch = f"cmoc/run/{session_id}/{run_id}"
    review_worktree = worktrees_dir(root) / session_id / run_id
    review_fork_commit = head_commit(current_root)
    review_join_commit = None
    all_oracle_files: list[Path] = []
    oracle_files: list[Path] = []
    findings: list[dict] = []
    worktree_created = False
    try:
        start_subcommand_step(2, "run の隔離実行を開始", "start isolated review")
        create_run_worktree(current_root, review_branch, review_worktree, "HEAD")
        worktree_created = True
        try:
            start_subcommand_step(3, "所見リストを初期化", "initialize findings")
            with pushd(review_worktree):
                all_oracle_files = enumerate_review_all_oracle_files(review_worktree)
                oracle_files = enumerate_review_oracle_targets(
                    review_worktree, scope, state, review_fork_commit
                )
                findings = run_review_oracle_loop(
                    root, review_worktree, oracle_files, config, codex_exec,
                    step_callback=start_subcommand_step,
                )
                start_subcommand_step(7, "run の隔離実行を終了", "finish isolated review")
                commit_review_index_changes(review_worktree)
                review_has_index_changes = review_branch_has_index_changes(
                    review_worktree, review_fork_commit
                )
            if review_has_index_changes:
                review_join_commit = merge_review_branch(current_root, review_branch)
        finally:
            if worktree_created:
                remove_worktree(current_root, review_worktree)
                delete_branch(current_root, review_branch, force=True)
        start_subcommand_step(8, "所見リストをレポート", "write review report")
        report_path = write_review_oracle_report(
            root,
            scope,
            branch,
            state,
            len(all_oracle_files),
            oracle_files,
            findings,
            review_branch,
            review_fork_commit,
            review_join_commit,
        )
    except Exception as exc:
        report_path = write_review_oracle_report(
            root,
            scope,
            branch,
            state,
            len(all_oracle_files),
            oracle_files,
            findings,
            review_branch,
            review_fork_commit,
            review_join_commit,
            error_message=str(exc) or exc.__class__.__name__,
        )
        typer.echo(str(report_path.resolve()))
        raise
    typer.echo(str(report_path.resolve()))


def _require_clean_worktree(root: Path) -> None:
    statuses = status_path_statuses(
        root, untracked_all=True, include_rename_sources=True
    )
    if statuses:
        raise CmocError(
            "review oracle は git 未コミット差分がある状態では実行できません。",
            ["差分を commit または退避してから再実行してください。"],
            "\n".join(str(path.relative_to(root)) for _status, path in statuses),
        )
