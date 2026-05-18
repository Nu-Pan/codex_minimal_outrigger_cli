"""CLI サブコマンド共通の実行制御。"""

from collections.abc import Callable
from pathlib import Path

import typer

from .errors import format_error_report
from .repo import enter_repo_root


def run_command(handler: Callable[[Path], int | None]) -> None:
    """repo root 解決と共通エラー報告を行って本体処理を実行する。"""
    # Typer 関数を薄く保つため、横断的な実行制御は commons 側に集約する。
    try:
        repo_root = enter_repo_root()
        result = handler(repo_root)
        if isinstance(result, int):
            raise typer.Exit(result)
    except typer.Exit:
        raise
    except Exception as error:
        print(format_error_report(error))
        code = getattr(error, "exit_code", 1)
        raise typer.Exit(code) from error
