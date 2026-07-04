from collections.abc import Callable, Sequence
from dataclasses import dataclass
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


@dataclass(frozen=True)
class CliRunResult:
    """標準サマリー以外の stdout 契約を持つサブコマンド用の結果。"""

    returncode: int = 0
    stdout: str | None = None


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

    work root 検査後、必要な pre-log 処理を済ませてからサブコマンドログを作成し、
    開始・完了表示、戻り値の終了コード化、例外のエラー表示を一箇所で扱う。
    runtime state は通常 repo root に置き、linked worktree 前処理では work root に置く。
    サブコマンドログは常に repo root に置く。
    """
    logger = None
    logger_token = None
    name = command_name or impl.__name__
    total_steps = 3
    try:
        current_root = work_root()
        require_current_directory_is_work_root(current_root)
        log_root = repo_root()
        runtime_root = current_root if use_work_root_runtime else log_root
        if pre_log_check is not None:
            # <work-root>/oracle/doc/app_spec/sub_command/tui.md
            # require .cmoc ignore guarantees before any .cmoc log file is created.
            pre_log_check(runtime_root)
        logger = SubcommandLogger(log_root, name)
        logger_token = set_current_subcommand_logger(logger)
        logger.event("command_invoked", argv=list(command_argv or [name]))
        logger.start_step(f"1/{total_steps}", f"開始 {name}", f"start {name}")
        typer.echo(f"# {console_timestamp()} (1/{total_steps}) 開始 {name}")
        typer.echo(f"- サブコマンドログ: `{logger.path}`")
        logger.start_step(
            f"{total_steps - 1}/{total_steps}", f"実行 {name}", f"run {name}"
        )
        typer.echo(
            f"# {console_timestamp()} ({total_steps - 1}/{total_steps}) 実行 {name}"
        )
        impl_result = impl(*args, **kwargs)
        if isinstance(impl_result, CliRunResult):
            returncode = impl_result.returncode
            result_stdout = impl_result.stdout
        else:
            returncode = impl_result if isinstance(impl_result, int) else 0
            result_stdout = None
        logger.start_step(
            f"{total_steps}/{total_steps}", f"完了 {name}", f"complete {name}"
        )
        logger.finish_current_step()
        logger.event(
            "command_finished",
            returncode=returncode,
            elapsed_sec=logger.elapsed(),
            quota_wait_sec=logger.quota_wait_sec,
        )
        _emit_completion_summary(logger, name, returncode, total_steps)
        if result_stdout is not None:
            typer.echo(result_stdout)
        if returncode:
            raise typer.Exit(returncode)
    except typer.Exit:
        raise
    except BaseException as exc:
        if logger:
            logger.start_step(
                f"{total_steps}/{total_steps}", f"完了 {name}", f"complete {name}"
            )
            logger.finish_current_step()
            logger.event(
                "command_finished",
                returncode=1,
                elapsed_sec=logger.elapsed(),
                quota_wait_sec=logger.quota_wait_sec,
                error=str(exc),
            )
            _emit_completion_summary(logger, name, 1, total_steps)
        result_stdout = getattr(exc, "cmoc_stdout", None)
        if result_stdout is not None:
            typer.echo(str(result_stdout))
        # <work-root>/oracle/doc/app_spec/error_handling.md leaves stdout as
        # the default; command-specific oracle rules may mark exceptions for stderr.
        typer.echo(
            render_error(exc),
            err=(
                error_to_stderr
                or bool(getattr(exc, "cmoc_error_to_stderr", False))
            ),
        )
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
        f"# {console_timestamp()} ({total_steps}/{total_steps}) 完了 {command_name}"
    )
    typer.echo(f"- サブコマンドログ: `{logger.path}`")
    for step in logger.step_timings:
        step_elapsed = step.elapsed_sec
        if step_elapsed is None:
            step_elapsed = elapsed - (step.started_at - logger.started_at)
        typer.echo(
            f"- ステップ経過時間[{step.index} {step.description}]: `{format_duration(step_elapsed)}`"
        )
    typer.echo(f"- 経過時間: `{format_duration(elapsed)}`")
    typer.echo(f"- quota 待機時間: `{format_duration(logger.quota_wait_sec)}`")
    typer.echo(f"- 終了コード: `{returncode}`")
