"""CLI サブコマンド共通の実行制御。"""

from collections.abc import Callable
from pathlib import Path
from time import perf_counter

import typer

from .errors import format_error_report
from .repo import enter_repo_root
from .subcommand_log import subcommand_log
from .timing import clear_current_timer, format_duration, report_current_timer


def run_command(handler: Callable[[Path], int | None]) -> None:
    """repo root 解決と共通エラー報告を行って本体処理を実行する。"""
    # Typer 関数を薄く保つため、横断的な実行制御は commons 側に集約する。
    repo_root = enter_repo_root()
    exit_code = 0
    try:
        with subcommand_log(repo_root) as log_context:
            try:
                clear_current_timer()
                result = handler(repo_root)
                if isinstance(result, int):
                    exit_code = result
            except typer.Exit as exit_error:
                exit_code = exit_error.exit_code or 0
                raise
            except Exception as error:
                print(format_error_report(error))
                exit_code = getattr(error, "exit_code", 1)
                raise typer.Exit(exit_code) from error
            finally:
                report_current_timer()
                print(
                    "subcommand total elapsed: "
                    f"{format_duration(perf_counter() - log_context.started)}"
                )
                print(
                    "subcommand quota wait elapsed: "
                    f"{format_duration(log_context.quota_wait_seconds)}"
                )
                print(f"subcommand return code: {exit_code}")
                clear_current_timer()
    except typer.Exit:
        raise

    if exit_code != 0:
        raise typer.Exit(exit_code)
