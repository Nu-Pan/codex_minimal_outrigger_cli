import os
import threading
from collections.abc import Sequence
from contextvars import ContextVar
from pathlib import Path

import click
import typer

from cmoc_runtime import (
    CmocError,
    SubcommandLogger,
    console_timestamp,
    format_duration,
    load_config,
    render_error,
    repo_root,
    reset_current_subcommand_logger,
    require_cmoc_ignored,
    run_codex_exec as runtime_run_codex_exec,
    run_codex_tui as runtime_run_codex_tui,
    run_git,
    set_current_subcommand_logger,
    work_root,
)
from basic.acp import AgentCallParameter
import sub_commands.indexing as indexing_command
from sub_commands.init import cmoc_init_impl
from sub_commands.apply.abandon import cmoc_apply_abandon_impl
from sub_commands.apply.fork import cmoc_apply_fork_impl
from sub_commands.apply.join import cmoc_apply_join_impl
from sub_commands.session.abandon import cmoc_session_abandon_impl
from sub_commands.session.fork import cmoc_session_fork_impl
from sub_commands.session.join import cmoc_session_join_impl
from sub_commands.review import (
    cmoc_review_oracle_impl,
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
_INITIAL_STATUS: ContextVar[str | None] = ContextVar("INITIAL_STATUS", default=None)


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
            indexing_command.run_indexing_preflight(root, run_codex_exec)
        finally:
            _INDEXING_ACTIVE.reset(token)


def should_skip_indexing_before_codex(purpose: str) -> bool:
    return purpose.startswith("indexing index entry") or "conflict resolution" in purpose


def _status_without_cmoc(status: str) -> str:
    lines = []
    for line in status.splitlines():
        path = line[3:]
        if " -> " in path:
            path = path.rsplit(" -> ", 1)[1]
        if path == ".cmoc" or path.startswith(".cmoc/"):
            continue
        lines.append(line)
    return "\n".join(lines)


def _run(handler, pre_log_check=None) -> None:
    logger = None
    logger_token = None
    status_token = None
    try:
        current_root = work_root()
        require_current_directory_is_work_root(current_root)
        root = repo_root()
        status_token = _INITIAL_STATUS.set(
            _status_without_cmoc(run_git(["status", "--short"], root).stdout.strip())
        )
        if pre_log_check is not None:
            pre_log_check(root)
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
        if status_token is not None:
            _INITIAL_STATUS.reset(status_token)


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
        return cmoc_apply_fork_impl(scope, run_codex_exec)

    _run(handler)


@apply_app.command("join")
def apply_join(force_resolve: bool = typer.Option(False, "--force-resolve")) -> None:
    def handler() -> None:
        cmoc_apply_join_impl(force_resolve)

    _run(handler)


@apply_app.command("abandon")
def apply_abandon() -> None:
    def handler() -> None:
        cmoc_apply_abandon_impl()

    _run(handler)


@review_app.command("oracle")
def review_oracle(scope: str = typer.Option("session", "--scope", "-s")) -> None:
    def handler() -> None:
        cmoc_review_oracle_impl(scope, run_codex_exec)

    _run(handler)


@app.command()
def indexing() -> None:
    def handler() -> None:
        indexing_command.cmoc_indexing_impl(_INITIAL_STATUS.get(), run_codex_exec)

    _run(handler, require_cmoc_ignored)


def main() -> None:
    app(prog_name="cmoc")


if __name__ == "__main__":
    main()
