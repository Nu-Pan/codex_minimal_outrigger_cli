import os
import threading
from collections.abc import Sequence
from contextvars import ContextVar
from pathlib import Path

import click
import typer

from cmoc_runtime import (
    CmocError,
    SessionState,
    SubcommandLogger,
    console_timestamp,
    load_config,
    render_error,
    repo_root,
    reset_current_subcommand_logger,
    format_duration,
    run_codex_exec as runtime_run_codex_exec,
    run_codex_tui as runtime_run_codex_tui,
    run_git,
    set_current_subcommand_logger,
    work_root,
)
from basic.acp import AgentCallParameter
from config.cmoc_config import CmocConfig
from sub_commands.init import cmoc_init_impl
from sub_commands.indexing import (
    build_index_entry_impl,
    commit_index_updates_impl,
    cmoc_indexing_impl,
    index_target_hash,
    indexable_children,
    parse_index_entries,
    render_index_entry,
    target_content_for_indexing,
    update_indexes_impl,
)
from sub_commands.apply import (
    cmoc_apply_abandon_impl,
    cmoc_apply_join_impl,
    collect_apply_join_unexpected_changes as collect_apply_join_unexpected_changes_impl,
    is_expected_apply_change as is_expected_apply_change_impl,
    is_expected_session_change as is_expected_session_change_impl,
    resolve_index_conflicts as resolve_index_conflicts_impl,
    restore_path_from_commit as restore_path_from_commit_impl,
    revert_unexpected_changes as revert_unexpected_changes_impl,
    worktree_for_branch as worktree_for_branch_impl,
    worktree_for_branch_optional as worktree_for_branch_optional_impl,
)
from sub_commands.apply_fork import (
    changed_worktree_paths,
    cmoc_apply_fork_impl,
    ensure_no_forbidden_apply_diff,
    enumerate_apply_findings as enumerate_apply_findings_impl,
    enumerate_apply_findings_for_targets as enumerate_apply_findings_for_targets_impl,
    enumerate_apply_targets,
    generate_apply_commit_message as generate_apply_commit_message_impl,
    normalize_apply_targets,
    related_apply_paths,
    sanitize_commit_message,
)
from sub_commands.apply_fork_report import (
    render_apply_fork_report,
    write_apply_fork_error_report,
    write_apply_fork_report as write_apply_fork_report_impl,
)
from sub_commands.session import (
    cmoc_session_abandon_impl,
    cmoc_session_fork_impl,
    cmoc_session_join_impl,
)
from sub_commands.review import (
    apply_finding_merge_operations as apply_finding_merge_operations_impl,
    cmoc_review_oracle_impl,
    commit_review_index_changes as commit_review_index_changes_impl,
    enumerate_review_all_oracle_files as enumerate_review_all_oracle_files_impl,
    enumerate_review_oracle_targets as enumerate_review_oracle_targets_impl,
    merge_review_branch as merge_review_branch_impl,
    path_display as path_display_impl,
    render_finding_section as render_finding_section_impl,
    render_review_oracle_report as render_review_oracle_report_impl,
    resolve_review_index_conflicts as resolve_review_index_conflicts_impl,
    run_review_oracle_loop as run_review_oracle_loop_impl,
)
from sub_commands.tui import cmoc_tui_impl


class _CmocTyperGroup(typer.core.TyperGroup):
    """通常の CLI 引数解析エラーを cmoc のエラーレポートへ変換する。"""

    def main(
        self,
        args: Sequence[str] | None = None,
        prog_name: str | None = None,
        complete_var: str | None = None,
        standalone_mode: bool = True,
        windows_expand_args: bool = True,
        **extra: object,
    ) -> object:
        click_kwargs = {
            "args": args,
            "prog_name": prog_name,
            "complete_var": complete_var,
            "windows_expand_args": windows_expand_args,
            **extra,
        }
        if "_CMOC_COMPLETE" in os.environ:
            return super().main(standalone_mode=standalone_mode, **click_kwargs)
        try:
            result = super().main(standalone_mode=False, **click_kwargs)
        except click.ClickException as exc:
            typer.echo(
                render_error(
                    CmocError(
                        "CLI 引数解析に失敗しました。",
                        ["コマンド名、サブコマンド名、option、引数を確認して再実行してください。"],
                        exc.format_message(),
                    )
                )
            )
            if standalone_mode:
                raise SystemExit(exc.exit_code) from exc
            raise
        if standalone_mode and isinstance(result, int):
            raise SystemExit(result)
        return result


app = typer.Typer(cls=_CmocTyperGroup, no_args_is_help=True)
session_app = typer.Typer(no_args_is_help=True)
apply_app = typer.Typer(no_args_is_help=True)
review_app = typer.Typer(no_args_is_help=True)
app.add_typer(session_app, name="session")
app.add_typer(apply_app, name="apply")
app.add_typer(review_app, name="review")
_INDEXING_LOCK = threading.Lock()
_INDEXING_ACTIVE: ContextVar[bool] = ContextVar("INDEXING_ACTIVE", default=False)


def run_codex_exec(parameter: AgentCallParameter, **kwargs):
    purpose = str(kwargs.get("purpose", "codex exec"))
    _run_indexing_before_codex(purpose, kwargs.get("root") or repo_root())
    return runtime_run_codex_exec(parameter, **kwargs)


def run_codex_tui(parameter: AgentCallParameter, **kwargs):
    purpose = str(kwargs.get("purpose", "codex tui"))
    _run_indexing_before_codex(purpose, kwargs.get("root") or repo_root())
    return runtime_run_codex_tui(parameter, **kwargs)


def _run_indexing_before_codex(purpose: str, root: Path) -> None:
    if _INDEXING_ACTIVE.get() or should_skip_indexing_before_codex(purpose):
        return
    with _INDEXING_LOCK:
        token = _INDEXING_ACTIVE.set(True)
        try:
            commit_index_updates(root, update_indexes(root))
        finally:
            _INDEXING_ACTIVE.reset(token)


def should_skip_indexing_before_codex(purpose: str) -> bool:
    return purpose.startswith("indexing index entry") or "conflict resolution" in purpose


def _run(handler) -> None:
    logger = None
    logger_token = None
    try:
        current_root = work_root()
        require_current_directory_is_work_root(current_root)
        root = repo_root()
        logger = SubcommandLogger(root, handler.__name__)
        logger_token = set_current_subcommand_logger(logger)
        logger.event("command_invoked", argv=[])
        typer.echo(f"# {console_timestamp()} (1/3) start {handler.__name__}")
        typer.echo(f"- sub_command_log: `{logger.path}`")
        logger.event("step_started", step="execute")
        typer.echo(f"# {console_timestamp()} (2/3) execute {handler.__name__}")
        handler_result = handler()
        returncode = handler_result if isinstance(handler_result, int) else 0
        if logger:
            logger.event(
                "command_finished",
                returncode=returncode,
                elapsed_sec=logger.elapsed(),
                quota_wait_sec=logger.quota_wait_sec,
            )
            _emit_completion_summary(logger, handler.__name__, returncode)
        if returncode:
            raise typer.Exit(returncode)
    except typer.Exit:
        raise
    except BaseException as exc:
        if logger:
            logger.event(
                "command_finished",
                returncode=1,
                elapsed_sec=logger.elapsed(),
                quota_wait_sec=logger.quota_wait_sec,
                error=str(exc),
            )
            _emit_completion_summary(logger, handler.__name__, 1)
        typer.echo(render_error(exc))
        raise typer.Exit(1) from exc
    finally:
        if logger_token is not None:
            reset_current_subcommand_logger(logger_token)


def _emit_completion_summary(
    logger: SubcommandLogger, handler_name: str, returncode: int
) -> None:
    elapsed = logger.elapsed()
    typer.echo(f"# {console_timestamp()} (3/3) completed {handler_name}")
    typer.echo(f"- sub_command_log: `{logger.path}`")
    typer.echo(f"- step_execute_elapsed: `{format_duration(elapsed)}`")
    typer.echo(f"- elapsed: `{format_duration(elapsed)}`")
    typer.echo(f"- quota_wait: `{format_duration(logger.quota_wait_sec)}`")
    typer.echo(f"- returncode: `{returncode}`")


def require_current_directory_is_work_root(root: Path) -> None:
    if Path.cwd().resolve() == root.resolve():
        return
    raise CmocError(
        "cmoc は work root で実行してください。",
        ["git repository の root directory へ移動してから再実行してください。"],
        f"cwd: {Path.cwd().resolve()}\nwork_root: {root.resolve()}",
    )


@app.command()
def init() -> None:
    def handler() -> None:
        cmoc_init_impl()

    _run(handler)


@app.command()
def tui() -> None:
    def handler() -> None:
        root = repo_root()
        current_root = work_root()
        cmoc_tui_impl(
            run_codex_exec,
            run_codex_tui,
            root=root,
            work_root=current_root,
            config=load_config(root),
        )

    _run(handler)


@session_app.command("fork")
def session_fork() -> None:
    def handler() -> None:
        cmoc_session_fork_impl()

    _run(handler)


@session_app.command("join")
def session_join() -> None:
    def handler() -> None:
        cmoc_session_join_impl(run_codex_exec, run_git)

    _run(handler)


@session_app.command("abandon")
def session_abandon() -> None:
    def handler() -> None:
        cmoc_session_abandon_impl()

    _run(handler)


@apply_app.command("fork")
def apply_fork(scope: str = typer.Option("rolling", "--scope", "-s")) -> None:
    def handler() -> None:
        return cmoc_apply_fork_impl(
            scope,
            run_codex_exec,
            enumerate_apply_targets,
            enumerate_apply_findings_for_targets,
            related_apply_paths,
            ensure_no_forbidden_apply_diff,
            changed_worktree_paths,
            generate_apply_commit_message,
            normalize_apply_targets,
            write_apply_fork_report,
            write_apply_fork_error_report,
        )

    _run(handler)


def write_apply_fork_report(
    root: Path,
    apply_worktree: Path,
    session_branch: str,
    state: SessionState,
    finding_counts: list[int],
    result_label: str,
    config: CmocConfig,
) -> Path:
    return write_apply_fork_report_impl(
        root,
        apply_worktree,
        session_branch,
        state,
        finding_counts,
        result_label,
        config,
        run_codex_exec,
    )


def write_apply_fork_error_report(
    root: Path,
    session_branch: str,
    state: SessionState,
    finding_counts: list[int],
    apply_worktree: Path,
) -> Path:
    return write_apply_fork_error_report_impl(
        root,
        session_branch,
        state,
        finding_counts,
        apply_worktree,
    )


def generate_apply_commit_message(
    root: Path,
    apply_worktree: Path,
    finding: dict,
    config: CmocConfig,
) -> str:
    return generate_apply_commit_message_impl(
        root,
        apply_worktree,
        finding,
        config,
        run_codex_exec,
    )


def enumerate_apply_findings(root: Path, scope: str, config: CmocConfig, log_root: Path | None = None) -> list[dict]:
    return enumerate_apply_findings_impl(
        root,
        scope,
        config,
        run_codex_exec,
        log_root=log_root,
    )


def enumerate_apply_findings_for_targets(
    root: Path,
    targets: list[Path],
    config: CmocConfig,
    log_root: Path | None = None,
) -> list[dict]:
    return enumerate_apply_findings_for_targets_impl(
        root,
        targets,
        config,
        run_codex_exec,
        log_root=log_root,
    )


@apply_app.command("join")
def apply_join(force_resolve: bool = typer.Option(False, "--force-resolve")) -> None:
    def handler() -> None:
        cmoc_apply_join_impl(force_resolve)

    _run(handler)


def collect_apply_join_unexpected_changes(root: Path, state: SessionState, apply_branch: str, session_branch: str) -> dict[str, list[str]]:
    return collect_apply_join_unexpected_changes_impl(root, state, apply_branch, session_branch)


def is_expected_apply_change(root: Path, path: str) -> bool:
    return is_expected_apply_change_impl(root, path)


def is_expected_session_change(path: str) -> bool:
    return is_expected_session_change_impl(path)


def revert_unexpected_changes(root: Path, unexpected: dict[str, list[str]], state: SessionState) -> None:
    revert_unexpected_changes_impl(root, unexpected, state)


def restore_path_from_commit(root: Path, commit: str, path: str) -> None:
    restore_path_from_commit_impl(root, commit, path)


def resolve_index_conflicts(root: Path) -> bool:
    return resolve_index_conflicts_impl(root)


@apply_app.command("abandon")
def apply_abandon() -> None:
    def handler() -> None:
        cmoc_apply_abandon_impl()

    _run(handler)


def worktree_for_branch(root: Path, branch: str) -> Path:
    return worktree_for_branch_impl(root, branch)


def worktree_for_branch_optional(root: Path, branch: str) -> Path | None:
    return worktree_for_branch_optional_impl(root, branch)


@review_app.command("oracle")
def review_oracle(scope: str = typer.Option("session", "--scope", "-s")) -> None:
    def handler() -> None:
        cmoc_review_oracle_impl(
            scope,
            run_codex_exec,
            enumerate_review_all_oracle_files,
            enumerate_review_oracle_targets,
            run_review_oracle_loop,
            commit_review_index_changes,
            merge_review_branch,
            render_review_oracle_report,
        )

    _run(handler)


def commit_review_index_changes(review_worktree: Path) -> bool:
    return commit_review_index_changes_impl(review_worktree)


def merge_review_branch(root: Path, review_branch: str) -> str:
    return merge_review_branch_impl(root, review_branch)


def resolve_review_index_conflicts(root: Path) -> bool:
    return resolve_review_index_conflicts_impl(root)


def enumerate_review_oracle_targets(root: Path, scope: str, state: SessionState) -> list[Path]:
    return enumerate_review_oracle_targets_impl(root, scope, state)


def enumerate_review_all_oracle_files(root: Path) -> list[Path]:
    return enumerate_review_all_oracle_files_impl(root)


def run_review_oracle_loop(
    log_root: Path,
    worktree: Path,
    oracle_files: list[Path],
    config: CmocConfig,
    codex_exec=None,
) -> list[dict]:
    return run_review_oracle_loop_impl(log_root, worktree, oracle_files, config, codex_exec or run_codex_exec)


def apply_finding_merge_operations(findings: list[dict], operations: list[dict], next_id: int) -> list[dict]:
    return apply_finding_merge_operations_impl(findings, operations, next_id)


def render_review_oracle_report(
    root: Path,
    scope: str,
    session_branch: str,
    session_id: str,
    state: SessionState,
    oracle_count_total: int,
    oracle_files: list[Path],
    findings: list[dict],
    review_branch: str | None,
    review_fork_commit: str | None,
    review_join_commit: str | None,
) -> str:
    return render_review_oracle_report_impl(
        root,
        scope,
        session_branch,
        session_id,
        state,
        oracle_count_total,
        oracle_files,
        findings,
        review_branch,
        review_fork_commit,
        review_join_commit,
    )


def render_finding_section(findings: list[dict]) -> str:
    return render_finding_section_impl(findings)


def path_display(root: Path, path: Path) -> str:
    return path_display_impl(root, path)


@app.command()
def indexing() -> None:
    def handler() -> None:
        cmoc_indexing_impl(update_indexes, commit_index_updates)

    _run(handler)


def commit_index_updates(root: Path, updated: list[Path]) -> None:
    commit_index_updates_impl(root, updated)


def update_indexes(root: Path) -> list[Path]:
    return update_indexes_impl(root, build_index_entry)


def build_index_entry(root: Path, path: Path, digest: str | None = None) -> str:
    return build_index_entry_impl(root, path, run_codex_exec, digest=digest)


def main() -> None:
    app(prog_name="cmoc")


if __name__ == "__main__":
    main()
