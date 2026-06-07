"""CLI サブコマンド共通の実行制御。"""

from collections.abc import Callable
from collections.abc import Iterable
from pathlib import Path
import sys
from time import perf_counter

import typer

from .errors import CmocError
from .errors import format_error_report
from .repo import enter_repo_root
from .subcommand_log import log_event
from .subcommand_log import subcommand_log
from .timing import clear_current_timer, format_duration, report_current_timer


def run_command(
    handler: Callable[[Path], int | None],
    *,
    command_path: str | None = None,
    non_error_exit_codes: Iterable[int] = (),
) -> None:
    """repo root 解決と共通エラー報告を行って本体処理を実行する。"""
    # Typer 関数を薄く保つため、横断的な実行制御は commons 側に集約する。
    exit_code = 0
    non_error_exit_code_set = set(non_error_exit_codes)
    started = perf_counter()
    invocation_cwd = Path.cwd()
    argv = list(sys.argv)
    try:
        repo_root = enter_repo_root()
        with subcommand_log(
            repo_root,
            command_path=command_path,
            argv=argv,
            cwd=invocation_cwd,
        ) as log_context:
            try:
                clear_current_timer()
                result = handler(repo_root)
                if isinstance(result, int):
                    exit_code = result
            except typer.Exit as exit_error:
                exit_code = exit_error.exit_code or 0
                if (
                    exit_code != 0
                    and exit_code not in non_error_exit_code_set
                ):
                    report_error = CmocError(
                        "サブコマンドがエラー終了しました。",
                        actions=[
                            "直前の出力に個別の失敗理由がある場合は、"
                            "その内容に従って入力値やリポジトリ状態を"
                            "修正してください。",
                            "原因が特定できない場合は、Detail と Call stack を"
                            "確認してから cmoc を再実行してください。",
                        ],
                        detail=(
                            "サブコマンド本体が "
                            f"typer.Exit({exit_code}) を送出しました。"
                        ),
                        exit_code=exit_code,
                    )
                    report_error = report_error.with_traceback(
                        exit_error.__traceback__
                    )
                    print(format_error_report(report_error))
                raise
            except Exception as error:
                print(format_error_report(error))
                exit_code = getattr(error, "exit_code", 1)
                raise typer.Exit(exit_code) from error
            finally:
                _print_completion_report(
                    started=started,
                    log_path=log_context.path,
                    quota_wait_seconds=log_context.quota_wait_seconds,
                    exit_code=exit_code,
                )
    except typer.Exit:
        raise
    except Exception as error:
        print(format_error_report(error))
        exit_code = getattr(error, "exit_code", 1)
        _print_completion_report(
            started=started,
            log_path=None,
            quota_wait_seconds=0.0,
            exit_code=exit_code,
        )
        raise typer.Exit(exit_code) from error

    if exit_code != 0:
        raise typer.Exit(exit_code)


def _print_completion_report(
    *,
    started: float,
    log_path: Path | None,
    quota_wait_seconds: float,
    exit_code: int,
) -> None:
    """サブコマンド終了時に可能な範囲の集計を stdout へ出す。"""
    # 途中経過ログと終了時の集計ブロックを視覚的に分ける。
    total_elapsed_seconds = perf_counter() - started
    log_event(
        "subcommand_end",
        {
            "subcommand_log": str(log_path) if log_path is not None else None,
            "quota_wait_seconds": quota_wait_seconds,
            "returncode": exit_code,
            "total_elapsed_seconds": total_elapsed_seconds,
        },
    )
    print("# Command completion report")
    if log_path is None:
        print("subcommand log: unavailable")
    else:
        print(f"subcommand log: {log_path}")
    report_current_timer()
    print(
        "subcommand total elapsed: "
        f"{format_duration(total_elapsed_seconds)}"
    )
    print(
        "subcommand quota wait elapsed: "
        f"{format_duration(quota_wait_seconds)}"
    )
    print(f"subcommand return code: {exit_code}")
    clear_current_timer()
