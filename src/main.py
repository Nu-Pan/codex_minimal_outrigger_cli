"""cmoc CLI エントリーポイント。"""

import importlib.util
from pathlib import Path
from types import ModuleType

import click
import typer

from commons.errors import CmocError
from commons.errors import format_error_report
from sub_commands.apply import cmoc_apply_impl
from sub_commands.apply_abandon import cmoc_apply_abandon_impl
from sub_commands.apply_join import cmoc_apply_join_impl
from sub_commands.init import cmoc_init_impl
from sub_commands.session_abandon import cmoc_session_abandon_impl
from sub_commands.session_fork import cmoc_session_fork_impl
from sub_commands.session_join import cmoc_session_join_impl


app: typer.Typer = typer.Typer(name="cmoc", no_args_is_help=True)
session_app: typer.Typer = typer.Typer(
    name="session",
    no_args_is_help=True,
)
apply_app: typer.Typer = typer.Typer(
    name="apply",
    no_args_is_help=True,
)
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

app.add_typer(session_app, name="session")
app.add_typer(apply_app, name="apply")


@app.command("init")
def init_command() -> None:
    """Initialize a repository for cmoc work."""
    # CLI callback は init の本体実装へ処理を委譲する。
    cmoc_init_impl()


@session_app.command("fork")
def session_fork_command() -> None:
    """Start a cmoc session."""
    # CLI callback は session fork の本体実装へ処理を委譲する。
    cmoc_session_fork_impl()


@session_app.command("join")
def session_join_command() -> None:
    """Join the active cmoc session."""
    # CLI callback は session join の本体実装へ処理を委譲する。
    cmoc_session_join_impl()


@session_app.command("abandon")
def session_abandon_command() -> None:
    """Abandon the active cmoc session."""
    # CLI callback は session abandon の本体実装へ処理を委譲する。
    cmoc_session_abandon_impl()


@app.command("eval-oracles")
@app.command("eval-oracle", hidden=True)
def eval_oracles_command(
    full: bool = typer.Option(False, "--full", "-f"),
) -> None:
    """Evaluate oracle files."""
    # CLI callback は eval-oracles の本体実装へ処理を委譲する。
    cmoc_eval_oracles_impl(full=full)


@apply_app.command("fork")
def apply_fork_command(
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
    # CLI callback は apply fork の本体実装へ処理を委譲する。
    cmoc_apply_impl(
        repeat_investigate_and_fix=repeat_investigate_and_fix,
        repeat_improove_fixing_list=repeat_improove_fixing_list,
        full=full,
    )


@apply_app.command("join")
def apply_join_command(
    force_resolve: bool = typer.Option(False, "--force-resolve"),
) -> None:
    """Join the last completed apply run."""
    # CLI callback は apply join の本体実装へ処理を委譲する。
    cmoc_apply_join_impl(force_resolve=force_resolve)


@apply_app.command("abandon")
def apply_abandon_command() -> None:
    """Abandon the active apply run."""
    # CLI callback は apply abandon の本体実装へ処理を委譲する。
    cmoc_apply_abandon_impl()


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
                    "`cmoc init`, `cmoc session fork`, `cmoc eval-oracles`, "
                    "`cmoc apply fork`, `cmoc apply join`, "
                    "`cmoc session join` のいずれかを実行してください。",
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
