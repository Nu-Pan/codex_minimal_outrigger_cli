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
    error_to_stderr: bool = False,
    use_work_root_runtime: bool = False,
    **kwargs: Any,
) -> None:
    """CLI サブコマンドの共通実行ライフサイクルを管理する。

    work root 検査後に任意の事前検査を行ってからサブコマンドログを作成し、
    開始・完了表示、戻り値の終了コード化、例外のエラー表示を一箇所で扱う。
    runtime state は通常 repo root に置き、init だけは初期化対象である work root に置く。
    サブコマンドログは常に repo root に置く。
    エラーレポートは `<work-root>/oracle/doc/app_spec/error_handling.md` に従い stdout へ出す。
    """
    logger = None
    logger_token = None
    name = command_name or impl.__name__
    try:
        current_root = work_root()
        require_current_directory_is_work_root(current_root)
        log_root = repo_root()
        runtime_root = current_root if use_work_root_runtime else log_root
        if pre_log_check is not None:
            pre_log_check(runtime_root)
        total_steps = 3
        logger = SubcommandLogger(log_root, name)
        logger_token = set_current_subcommand_logger(logger)
        logger.event("command_invoked", argv=list(command_argv or [name]))
        typer.echo(f"# {console_timestamp()} (1/{total_steps}) start {name}")
        typer.echo(f"- sub_command_log: `{logger.path}`")
        logger.event("step_started", step="execute")
        typer.echo(
            f"# {console_timestamp()} ({total_steps - 1}/{total_steps}) execute {name}"
        )
        impl_result = impl(*args, **kwargs)
        returncode = impl_result if isinstance(impl_result, int) else 0
        logger.event(
            "command_finished",
            returncode=returncode,
            elapsed_sec=logger.elapsed(),
            quota_wait_sec=logger.quota_wait_sec,
        )
        _emit_completion_summary(logger, name, returncode, total_steps)
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
            _emit_completion_summary(logger, name, 1, total_steps)
        typer.echo(render_error(exc), err=error_to_stderr)
        raise typer.Exit(1) from exc
    finally:
        if logger_token is not None:
            reset_current_subcommand_logger(logger_token)


def require_current_directory_is_work_root(root: Path) -> None:
    """cmoc が work root で実行されている前提を検査する。"""
    if Path.cwd().resolve() == root.resolve():
        return
    raise CmocError(
        "cmoc は work root で実行してください。",
        ["git repository の root directory へ移動してから再実行してください。"],
        f"cwd: {Path.cwd().resolve()}\nwork_root: {root.resolve()}",
    )


def _emit_completion_summary(
    logger: SubcommandLogger, command_name: str, returncode: int, total_steps: int
) -> None:
    """サブコマンド完了時に標準の stdout サマリーを出力する。"""
    elapsed = logger.elapsed()
    typer.echo(
        f"# {console_timestamp()} ({total_steps}/{total_steps}) completed {command_name}"
    )
    typer.echo(f"- sub_command_log: `{logger.path}`")
    typer.echo(f"- step_execute_elapsed: `{format_duration(elapsed)}`")
    typer.echo(f"- elapsed: `{format_duration(elapsed)}`")
    typer.echo(f"- quota_wait: `{format_duration(logger.quota_wait_sec)}`")
    typer.echo(f"- returncode: `{returncode}`")
