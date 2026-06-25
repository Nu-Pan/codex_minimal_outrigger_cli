from collections.abc import Callable, Sequence
from pathlib import Path
from typing import Any

import typer

from commons.runtime_errors import CmocError, render_error
from commons.runtime_logging import (
    SubcommandLogger,
    reset_current_subcommand_logger,
    set_current_subcommand_logger,
)
from commons.runtime_paths import console_timestamp, format_duration, repo_root, work_root


def run_cli_subcommand(
    impl: Callable[..., Any],
    *args: Any,
    pre_log_check: Callable[[Path], None] | None = None,
    command_name: str | None = None,
    command_argv: Sequence[str] | None = None,
    **kwargs: Any,
) -> None:
    logger = None
    logger_token = None
    name = command_name or impl.__name__
    try:
        current_root = work_root()
        require_current_directory_is_work_root(current_root)
        root = repo_root()
        if pre_log_check is not None:
            pre_log_check(root)
        logger = SubcommandLogger(root, name)
        logger_token = set_current_subcommand_logger(logger)
        logger.event("command_invoked", argv=list(command_argv or [name]))
        typer.echo(f"# {console_timestamp()} (1/3) start {name}")
        typer.echo(f"- sub_command_log: `{logger.path}`")
        logger.event("step_started", step="execute")
        typer.echo(f"# {console_timestamp()} (2/3) execute {name}")
        impl_result = impl(*args, **kwargs)
        returncode = impl_result if isinstance(impl_result, int) else 0
        logger.event(
            "command_finished",
            returncode=returncode,
            elapsed_sec=logger.elapsed(),
            quota_wait_sec=logger.quota_wait_sec,
        )
        _emit_completion_summary(logger, name, returncode)
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
            _emit_completion_summary(logger, name, 1)
        typer.echo(render_error(exc), err=True)
        raise typer.Exit(1) from exc
    finally:
        if logger_token is not None:
            reset_current_subcommand_logger(logger_token)


def require_current_directory_is_work_root(root: Path) -> None:
    if Path.cwd().resolve() == root.resolve():
        return
    raise CmocError(
        "cmoc は work root で実行してください。",
        ["git repository の root directory へ移動してから再実行してください。"],
        f"cwd: {Path.cwd().resolve()}\nwork_root: {root.resolve()}",
    )


def _emit_completion_summary(
    logger: SubcommandLogger, command_name: str, returncode: int
) -> None:
    elapsed = logger.elapsed()
    typer.echo(f"# {console_timestamp()} (3/3) completed {command_name}")
    typer.echo(f"- sub_command_log: `{logger.path}`")
    typer.echo(f"- step_execute_elapsed: `{format_duration(elapsed)}`")
    typer.echo(f"- elapsed: `{format_duration(elapsed)}`")
    typer.echo(f"- quota_wait: `{format_duration(logger.quota_wait_sec)}`")
    typer.echo(f"- returncode: `{returncode}`")
