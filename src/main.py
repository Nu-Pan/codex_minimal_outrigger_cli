"""cmoc CLI エントリーポイント。"""

import importlib.util
from pathlib import Path
from types import ModuleType

import click
import typer

from commons.errors import CmocError
from commons.errors import format_error_report
from sub_commands.apply import cmoc_apply_impl
from sub_commands.branch import cmoc_branch_impl
from sub_commands.init import cmoc_init_impl
from sub_commands.merge import cmoc_merge_impl


app: typer.Typer = typer.Typer(name="cmoc", no_args_is_help=True)
_EVAL_ORACLES_PATH = Path(__file__).parent / "sub_commands" / "eval-oracles.py"
_EVAL_ORACLES_SPEC = importlib.util.spec_from_file_location(
    "sub_commands.eval-oracles",
    _EVAL_ORACLES_PATH,
)
if _EVAL_ORACLES_SPEC is None or _EVAL_ORACLES_SPEC.loader is None:
    raise ImportError(f"cannot load subcommand module: {_EVAL_ORACLES_PATH}")
_eval_oracles_module = importlib.util.module_from_spec(_EVAL_ORACLES_SPEC)
assert isinstance(_eval_oracles_module, ModuleType)
_EVAL_ORACLES_SPEC.loader.exec_module(_eval_oracles_module)
cmoc_eval_oracles_impl = _eval_oracles_module.cmoc_eval_oracles_impl


@app.command("init")
def init_command() -> None:
    """Initialize a repository for cmoc work."""
    # CLI callback は init の本体実装へ処理を委譲する。
    cmoc_init_impl()


@app.command("branch")
def branch_command() -> None:
    """Create a cmoc work branch."""
    # CLI callback は branch の本体実装へ処理を委譲する。
    cmoc_branch_impl()


@app.command("eval-oracles")
@app.command("eval-oracle", hidden=True)
def eval_oracles_command(
    full: bool = typer.Option(False, "--full", "-f"),
) -> None:
    """Evaluate oracle files."""
    # CLI callback は eval-oracles の本体実装へ処理を委譲する。
    cmoc_eval_oracles_impl(full=full)


@app.command("apply")
def apply_command(
    repeat_investigate_and_fix: int = typer.Option(
        5,
        "--repeat-investigate-and-fix",
        "--repeat",
        "-r",
    ),
    repeat_improove_fixing_list: int = typer.Option(
        3,
        "--repeat-improove-fixing-list",
    ),
    full: bool = typer.Option(False, "--full", "-f"),
) -> None:
    """Apply oracle requirements to implementation."""
    # CLI callback は apply の本体実装へ処理を委譲する。
    cmoc_apply_impl(
        repeat_investigate_and_fix=repeat_investigate_and_fix,
        repeat_improove_fixing_list=repeat_improove_fixing_list,
        full=full,
    )


@app.command("merge")
def merge_command(cmoc_branch: str | None = typer.Argument(None)) -> None:
    """Merge a cmoc branch into the current branch."""
    # CLI callback は merge の本体実装へ処理を委譲する。
    cmoc_merge_impl(cmoc_branch=cmoc_branch)


def main() -> None:
    """Typer の parse error も共通エラーレポートへ変換して起動する。"""
    # standalone_mode=False で Click/Typer の例外を cmoc 側で整形する。
    try:
        result = app(prog_name="cmoc", standalone_mode=False)
        if isinstance(result, int):
            raise SystemExit(result)
    except typer.Exit as exit_error:
        raise SystemExit(exit_error.exit_code) from exit_error
    except click.ClickException as error:
        # CLI parse error は Click の exit_code を維持する。
        report_error: BaseException = error
        exit_code = error.exit_code
        if isinstance(error, click.exceptions.NoArgsIsHelpError):
            report_error = CmocError(
                "コマンドが指定されていません。",
                [
                    "利用可能なコマンドを確認するには `cmoc --help` を実行してください。",
                    "`cmoc init`, `cmoc branch`, `cmoc eval-oracles`, "
                    "`cmoc apply`, `cmoc merge` のいずれかを実行してください。",
                ],
                (
                    "cmoc がサブコマンドなしで起動されました。"
                    "実行する workflow を cmoc が判断するため、サブコマンドが必要です。"
                ),
                exit_code=error.exit_code,
            )
            exit_code = report_error.exit_code
        print(format_error_report(report_error))
        raise SystemExit(exit_code) from error
    except Exception as error:
        # 想定外エラーも共通形式で表示し、可能なら例外側の exit_code を使う。
        print(format_error_report(error))
        code = getattr(error, "exit_code", 1)
        raise SystemExit(code) from error


if __name__ == "__main__":
    # `python src/main.py` で直接実行される経路でも typer を起動する。
    main()
