"""cmoc CLI エントリーポイント。"""

import sys
from pathlib import Path

import click
import typer

from commons.errors import format_error_report
from sub_commands.apply import cmoc_apply_impl
from sub_commands.branch import cmoc_branch_impl
from sub_commands.eval_oracles import cmoc_eval_oracles_impl
from sub_commands.init import cmoc_init_impl
from sub_commands.merge import cmoc_merge_impl

app = typer.Typer(no_args_is_help=True)


@app.command("init")
def init_command() -> None:
    """Initialize a repository for cmoc work."""
    cmoc_init_impl()


@app.command("branch")
def branch_command() -> None:
    """Create a cmoc work branch."""
    cmoc_branch_impl()


@app.command("eval-oracles")
def eval_oracles_command(
    full: bool = typer.Option(False, "--full", "-f"),
) -> None:
    """Evaluate oracle files."""
    cmoc_eval_oracles_impl(full=full)


@app.command("apply")
def apply_command() -> None:
    """Apply oracle requirements to implementation."""
    cmoc_apply_impl()


@app.command("merge")
def merge_command(cmoc_branch: str | None = typer.Argument(None)) -> None:
    """Merge a cmoc branch into the current branch."""
    cmoc_merge_impl(cmoc_branch=cmoc_branch)


def main() -> None:
    """Typer の parse error も共通エラーレポートへ変換して起動する。"""
    # standalone_mode=False で Click/Typer の例外を cmoc 側で整形する。
    try:
        app(standalone_mode=False)
    except typer.Exit as exit_error:
        raise SystemExit(exit_error.exit_code) from exit_error
    except click.ClickException as error:
        # CLI parse error は Click の exit_code を維持する。
        print(format_error_report(error))
        raise SystemExit(error.exit_code) from error
    except Exception as error:
        # 想定外エラーも共通形式で表示し、可能なら例外側の exit_code を使う。
        print(format_error_report(error))
        code = getattr(error, "exit_code", 1)
        raise SystemExit(code) from error


if __name__ == "__main__":
    # `bin/cmoc` から直接実行される経路でも typer を起動する。
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    main()
