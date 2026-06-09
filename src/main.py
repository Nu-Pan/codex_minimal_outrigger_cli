"""cmoc CLI エントリーポイント。"""

import os
import sys
from typing import Literal

import click
import typer

from commons.errors import CmocError
from commons.errors import format_error_report
from sub_commands.apply.abandon import cmoc_apply_abandon_impl
from sub_commands.apply.fork import cmoc_apply_impl
from sub_commands.apply.join import cmoc_apply_join_impl
from sub_commands.init import cmoc_init_impl
from sub_commands.indexing import cmoc_indexing_impl
from sub_commands.review.oracles import cmoc_review_oracles_impl
from sub_commands.session.abandon import cmoc_session_abandon_impl
from sub_commands.session.fork import cmoc_session_fork_impl
from sub_commands.session.join import cmoc_session_join_impl


app: typer.Typer = typer.Typer(name="cmoc", no_args_is_help=False)
session_app: typer.Typer = typer.Typer(
    name="session",
    no_args_is_help=False,
)
apply_app: typer.Typer = typer.Typer(
    name="apply",
    no_args_is_help=False,
)
review_app: typer.Typer = typer.Typer(
    name="review",
    no_args_is_help=False,
)

app.add_typer(session_app, name="session")
app.add_typer(apply_app, name="apply")
app.add_typer(review_app, name="review")


@app.command("init")
def init_command() -> None:
    """Initialize a repository for cmoc work."""
    # CLI callback は init の本体実装へ処理を委譲する。
    cmoc_init_impl()


@app.command("indexing")
def indexing_command() -> None:
    """Run INDEX.md maintenance explicitly."""
    # CLI callback は indexing の本体実装へ処理を委譲する。
    cmoc_indexing_impl()


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


@app.command("eval-oracle", hidden=True)
@app.command("eval-oracles", hidden=True)
@review_app.command("oracles")
def review_oracles_command(
    scope: Literal["session", "full"] = typer.Option(
        "session",
        "--scope",
        "-s",
    ),
    enumerate_findings_loop: int = typer.Option(
        3,
        "--enumerate-findings-loop",
        min=0,
    ),
    merge_findings_loop: int = typer.Option(
        3,
        "--merge-findings-loop",
        min=0,
    ),
    refine_findings_loop: int = typer.Option(
        3,
        "--refine-findings-loop",
        min=0,
    ),
    full: bool = typer.Option(False, "--full", "-f", hidden=True),
    repeat_improve_issues_list: int | None = typer.Option(
        None,
        "--repeat-improve-issues-list",
        min=0,
        hidden=True,
    ),
) -> None:
    """Review oracle files."""
    # CLI callback は review oracles の本体実装へ処理を委譲する。
    if full:
        scope = "full"
    if repeat_improve_issues_list is not None:
        refine_findings_loop = repeat_improve_issues_list
    cmoc_review_oracles_impl(
        scope=scope,
        enumerate_findings_loop=enumerate_findings_loop,
        merge_findings_loop=merge_findings_loop,
        refine_findings_loop=refine_findings_loop,
    )


@apply_app.command("fork")
def apply_fork_command(
    repeat_investigate_and_fix: int = typer.Option(
        5,
        "--apply-loop",
        "--repeat-investigate-and-fix",
        "--repeat",
        "-r",
    ),
    repeat_improove_fixing_list: int = typer.Option(
        3,
        "--improove-fixing-list-loop",
        "--repeat-improove-fixing-list",
    ),
    scope: Literal["rolling", "session", "full"] = typer.Option(
        "rolling",
        "--scope",
        "-s",
    ),
) -> None:
    """Apply oracle requirements to implementation."""
    # CLI callback は apply fork の本体実装へ処理を委譲する。
    cmoc_apply_impl(
        repeat_investigate_and_fix=repeat_investigate_and_fix,
        repeat_improove_fixing_list=repeat_improove_fixing_list,
        scope=scope,
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
    if _is_completion_probe():
        app(prog_name="cmoc")
        return

    # standalone_mode=False で Click/Typer の例外を cmoc 側で整形する。
    try:
        _raise_missing_command_error_if_needed(sys.argv[1:])
        result = app(prog_name="cmoc", standalone_mode=False)
        if isinstance(result, int):
            raise SystemExit(result)
    except typer.Exit as exit_error:
        raise SystemExit(exit_error.exit_code) from exit_error
    except click.ClickException as error:
        # CLI parse error は Click の exit_code を維持する。
        exit_code = error.exit_code
        print(format_error_report(error))
        raise SystemExit(exit_code) from error
    except Exception as error:
        # 想定外エラーも共通形式で表示し、可能なら例外側の exit_code を使う。
        print(format_error_report(error))
        code = getattr(error, "exit_code", 1)
        raise SystemExit(code) from error


def _is_completion_probe() -> bool:
    """Click/Typer の自動補完プローブとして起動されたか判定する。"""
    return "_CMOC_COMPLETE" in os.environ


def _raise_missing_command_error_if_needed(arguments: list[str]) -> None:
    """help 表示にフォールバックする前に command path の不足をエラーにする。"""
    if _is_root_missing_command(arguments):
        raise _missing_command_error("cmoc")
    if _is_group_missing_command(arguments):
        raise _missing_command_error(f"cmoc {arguments[0]}")


def _is_root_missing_command(arguments: list[str]) -> bool:
    """root command が指定されていない引数列か判定する。"""
    return arguments == []


def _is_group_missing_command(arguments: list[str]) -> bool:
    """階層 command group だけが指定された引数列か判定する。"""
    return len(arguments) == 1 and arguments[0] in {"session", "apply", "review"}


def _missing_command_error(command_path: str) -> CmocError:
    """サブコマンド未指定用の利用者向けエラーを作る。"""
    return CmocError(
        "コマンドが指定されていません。",
        [
            f"利用可能なコマンドを確認するには `{command_path} --help` を実行してください。",
            "`cmoc init`, `cmoc indexing`, `cmoc session fork`, "
            "`cmoc review oracles`, "
            "`cmoc apply fork`, `cmoc apply join`, "
            "`cmoc session join` のいずれかを実行してください。",
        ],
        (
            f"{command_path} がサブコマンドなしで起動されました。"
            "実行する workflow を cmoc が判断するため、サブコマンドが必要です。"
        ),
        exit_code=2,
    )


if __name__ == "__main__":
    # `python src/main.py` で直接実行される経路でも typer を起動する。
    main()
