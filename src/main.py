import os
import threading
from collections.abc import Sequence
from contextvars import ContextVar
from pathlib import Path
from typing import TypedDict, Unpack

import click
import typer

from cmoc_runtime import (
    CmocError,
    CodexExecResult,
    CommandResult,
    SubcommandLogger,
    render_error,
    repo_root,
    require_cmoc_ignored,
    run_cli_subcommand,
    run_codex_exec as runtime_run_codex_exec,
    run_codex_tui as runtime_run_codex_tui,
    run_git,
    work_root,
)
from basic.acp import AgentCallParameter
from config.cmoc_config import CmocConfig
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
from sub_commands.tui import cmoc_tui_command_impl


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
                ),
                err=True,
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


class _CodexExecKwargs(TypedDict, total=False):
    root: Path | None
    cwd: Path | None
    config: CmocConfig | None
    purpose: str
    max_semantic_retries: int
    max_capacity_retries: int
    capacity_initial_sleep_sec: float
    quota_poll_interval_sec: float
    max_quota_polls: int | None
    subcommand_logger: SubcommandLogger | None


class _CodexTuiKwargs(TypedDict, total=False):
    root: Path | None
    cwd: Path | None
    config: CmocConfig | None
    purpose: str


def run_codex_exec(
    parameter: AgentCallParameter, **kwargs: Unpack[_CodexExecKwargs]
) -> CodexExecResult:
    purpose = str(kwargs.get("purpose", "codex exec"))
    _run_indexing_before_codex(purpose, _indexing_root_for_codex(kwargs))
    return runtime_run_codex_exec(parameter, **kwargs)


def run_codex_tui(
    parameter: AgentCallParameter, **kwargs: Unpack[_CodexTuiKwargs]
) -> CommandResult:
    purpose = str(kwargs.get("purpose", "codex tui"))
    _run_indexing_before_codex(purpose, _indexing_root_for_codex(kwargs))
    return runtime_run_codex_tui(parameter, **kwargs)


def _indexing_root_for_codex(
    kwargs: _CodexExecKwargs | _CodexTuiKwargs,
) -> Path:
    cwd = kwargs.get("cwd")
    return work_root(cwd) if cwd else kwargs.get("root") or repo_root()


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


@app.command()
def init() -> None:
    run_cli_subcommand(cmoc_init_impl, command_name="handler")


@app.command()
def tui() -> None:
    run_cli_subcommand(
        cmoc_tui_command_impl,
        run_codex_exec,
        run_codex_tui,
        command_name="handler",
    )


@session_app.command("fork")
def session_fork() -> None:
    run_cli_subcommand(cmoc_session_fork_impl, command_name="handler")


@session_app.command("join")
def session_join() -> None:
    run_cli_subcommand(
        cmoc_session_join_impl,
        run_codex_exec,
        run_git,
        command_name="handler",
    )


@session_app.command("abandon")
def session_abandon() -> None:
    run_cli_subcommand(cmoc_session_abandon_impl, command_name="handler")


@apply_app.command("fork")
def apply_fork(scope: str = typer.Option("rolling", "--scope", "-s")) -> None:
    run_cli_subcommand(
        cmoc_apply_fork_impl,
        scope,
        run_codex_exec,
        command_name="handler",
    )


@apply_app.command("join")
def apply_join(force_resolve: bool = typer.Option(False, "--force-resolve")) -> None:
    run_cli_subcommand(
        cmoc_apply_join_impl,
        force_resolve,
        command_name="handler",
    )


@apply_app.command("abandon")
def apply_abandon() -> None:
    run_cli_subcommand(cmoc_apply_abandon_impl, command_name="handler")


@review_app.command("oracle")
def review_oracle(scope: str = typer.Option("session", "--scope", "-s")) -> None:
    run_cli_subcommand(
        cmoc_review_oracle_impl,
        scope,
        run_codex_exec,
        command_name="handler",
    )


@app.command()
def indexing() -> None:
    run_cli_subcommand(
        indexing_command.cmoc_indexing_impl,
        codex_exec=run_codex_exec,
        pre_log_check=require_cmoc_ignored,
        command_name="handler",
    )


def main() -> None:
    app(prog_name="cmoc")


if __name__ == "__main__":
    main()
