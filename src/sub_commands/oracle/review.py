# {{work-root}}/oracle/doc/app_spec/sub_command/oracle_review.md
from pathlib import Path

import typer

from cmoc_runtime import (
    CmocError,
    create_run_worktree,
    current_branch,
    current_subcommand_logger,
    delete_branch,
    ensure_cmoc_ignored,
    head_commit,
    load_config,
    load_state_for_branch,
    pushd,
    remove_worktree,
    repo_root,
    run_cli_subcommand,
    run_codex_exec,
    start_subcommand_step,
    timestamp,
    work_root,
    worktrees_dir,
)
from commons.indexing import enable_indexing_preflight
from commons.runtime_git import status_path_statuses
from commons.runtime_results import CodexExecCallable
from sub_commands.oracle.review_index import (
    commit_review_index_changes,
    merge_review_branch,
    resolve_review_index_conflicts,
    review_branch_has_index_changes,
    review_worktree_status_paths,
)
from sub_commands.oracle.review_loop import (
    OracleReviewInterrupted,
    apply_finding_merge_operations,
    run_oracle_review_loop,
)
from sub_commands.oracle.review_report import (
    path_display,
    render_finding_section,
    render_oracle_review_report,
    write_oracle_review_report,
)
from sub_commands.oracle.review_targets import (
    enumerate_oracle_review_targets,
    enumerate_review_all_oracle_files,
)

CodexExec = CodexExecCallable

__all__ = [
    "CodexExec",
    "apply_finding_merge_operations",
    "cmoc_oracle_review_impl",
    "commit_review_index_changes",
    "enumerate_review_all_oracle_files",
    "enumerate_oracle_review_targets",
    "merge_review_branch",
    "path_display",
    "render_finding_section",
    "render_oracle_review_report",
    "resolve_review_index_conflicts",
    "review_worktree_status_paths",
    "run_oracle_review_loop",
    "write_oracle_review_report",
]


def cmoc_oracle_review_impl(scope: str) -> None:
    """CLI runtime を通して oracle review を実行する。"""
    enable_indexing_preflight()
    run_cli_subcommand(
        _cmoc_oracle_review_body,
        scope,
        run_codex_exec,
        command_name="oracle review",
        command_argv=["cmoc", "oracle", "review", "--scope", scope],
        total_steps=8,
    )


def _cmoc_oracle_review_body(
    scope: str,
    codex_exec: CodexExec,
) -> None:
    """現在の session branch の oracle を isolated review worktree 上でレビューする。"""
    root = repo_root()
    current_root = work_root()
    branch = current_branch(current_root)
    session_id, _state_path, state = load_state_for_branch(root, branch)
    if (
        not branch.startswith("cmoc/session/")
        or state.session.state != "active"
        or state.run.state != "ready"
    ):
        raise CmocError(
            "oracle review は active session branch 上で実行してください。", [], branch
        )
    _require_clean_worktree(current_root)
    ensure_cmoc_ignored(current_root)
    config = load_config(current_root)
    run_id = timestamp()
    review_branch = f"cmoc/run/{session_id}/{run_id}"
    review_worktree = worktrees_dir(root) / session_id / run_id
    review_fork_commit = head_commit(current_root)
    review_join_commit = None
    all_oracle_files: list[Path] = []
    oracle_files: list[Path] = []
    evaluated_oracle_files: list[Path] = []
    findings: list[dict] = []
    worktree_created = False
    interrupted = False
    try:
        start_subcommand_step(2, "run の隔離実行を開始", "start isolated review")
        create_run_worktree(
            current_root, review_branch, review_worktree, review_fork_commit
        )
        worktree_created = True
        try:
            start_subcommand_step(3, "所見リストを初期化", "initialize findings")
            with pushd(review_worktree):
                all_oracle_files = enumerate_review_all_oracle_files(review_worktree)
                oracle_files = enumerate_oracle_review_targets(
                    review_worktree, scope, state, review_fork_commit
                )
                try:
                    findings = run_oracle_review_loop(
                        root,
                        review_worktree,
                        oracle_files,
                        config,
                        codex_exec,
                        step_callback=start_subcommand_step,
                        evaluated_files=evaluated_oracle_files,
                    )
                except OracleReviewInterrupted as interruption:
                    interrupted = True
                    findings = interruption.findings
                    evaluated_oracle_files = interruption.evaluated_files
                    _record_oracle_review_interruption()
                start_subcommand_step(
                    7, "run の隔離実行を終了", "finish isolated review"
                )
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
                worktree_created = False
        start_subcommand_step(8, "所見リストをレポート", "write review report")
        report_path = write_oracle_review_report(
            root,
            scope,
            branch,
            state,
            len(all_oracle_files),
            evaluated_oracle_files,
            findings,
            review_branch,
            review_fork_commit,
            review_join_commit,
            interrupted=interrupted,
        )
    except KeyboardInterrupt:
        # loop 外の中断も、確定済みとして記録済みの範囲だけで正常完了する。
        if not interrupted:
            interrupted = True
            _record_oracle_review_interruption()
        if worktree_created:
            remove_worktree(current_root, review_worktree)
            delete_branch(current_root, review_branch, force=True)
            worktree_created = False
        report_path = write_oracle_review_report(
            root,
            scope,
            branch,
            state,
            len(all_oracle_files),
            evaluated_oracle_files,
            findings,
            review_branch,
            review_fork_commit,
            review_join_commit,
            interrupted=True,
        )
        typer.echo(str(report_path.resolve()))
        return
    except Exception as exc:
        report_path = write_oracle_review_report(
            root,
            scope,
            branch,
            state,
            len(all_oracle_files),
            evaluated_oracle_files,
            findings,
            review_branch,
            review_fork_commit,
            review_join_commit,
            error_message=str(exc) or exc.__class__.__name__,
        )
        typer.echo(str(report_path.resolve()))
        raise
    typer.echo(str(report_path.resolve()))


def _record_oracle_review_interruption() -> None:
    """review 中断要求を console とサブコマンドログへ記録する。"""
    typer.echo(
        "# ユーザー中断要求を受け付けました\n"
        "- 確定済みの部分結果で oracle review を完了します。"
    )
    logger = current_subcommand_logger()
    if logger is not None:
        logger.event(
            "user_interruption",
            command="oracle review",
            result="interrupted",
        )


def _require_clean_worktree(root: Path) -> None:
    """git status を検査し、未コミット差分があれば CmocError を送出する。"""
    statuses = status_path_statuses(
        root, untracked_all=True, include_rename_sources=True
    )
    if statuses:
        raise CmocError(
            "oracle review は git 未コミット差分がある状態では実行できません。",
            ["差分を commit または退避してから再実行してください。"],
            "\n".join(str(path.relative_to(root)) for _status, path in statuses),
        )
