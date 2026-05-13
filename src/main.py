"""cmoc CLI エントリーポイント。"""

import sys
from collections.abc import Callable
from pathlib import Path

import typer

from commons.errors import format_error_report
from commons.repo import enter_repo_root
from sub_commands.apply import cmoc_apply_impl
from sub_commands.branch import cmoc_branch_impl
from sub_commands.eval_oracles import cmoc_eval_oracles_impl
from sub_commands.init import cmoc_init_impl
from sub_commands.merge import cmoc_merge_impl

app = typer.Typer(no_args_is_help=True)


@app.command("init")
def init_command() -> None:
    """Initialize a repository for cmoc work."""
    _run_command(lambda repo_root: cmoc_init_impl(repo_root))


@app.command("branch")
def branch_command() -> None:
    """Create a cmoc work branch."""
    _run_command(lambda repo_root: cmoc_branch_impl(repo_root))


@app.command("eval-oracles")
def eval_oracles_command(full: bool = typer.Option(False, "--full", "-f")) -> None:
    """Evaluate oracle files."""
    _run_command(lambda repo_root: cmoc_eval_oracles_impl(repo_root, full=full))


@app.command("apply")
def apply_command() -> None:
    """Apply oracle requirements to implementation."""
    _run_command(lambda repo_root: cmoc_apply_impl(repo_root))


@app.command("merge")
def merge_command(cmoc_branch: str | None = typer.Argument(None)) -> None:
    """Merge a cmoc branch into the current branch."""
    _run_command(lambda repo_root: cmoc_merge_impl(repo_root, cmoc_branch))


def _run_command(handler: Callable[[Path], int | None]) -> None:
    """例外を仕様通り stdout のエラーレポートへ変換する。"""
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


if __name__ == "__main__":
    # `bin/cmoc` から直接実行される経路でも typer を起動する。
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    app()
