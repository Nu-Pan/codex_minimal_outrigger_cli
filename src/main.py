import os
from collections.abc import Sequence

import click
import typer

from cmoc_runtime import (
    CmocError,
    render_error,
)
from sub_commands.apply.abandon import cmoc_apply_abandon_command_impl
from sub_commands.apply.fork import cmoc_apply_fork_command_impl
from sub_commands.apply.join import cmoc_apply_join_command_impl
from sub_commands.indexing import cmoc_indexing_command_impl
from sub_commands.init import cmoc_init_command_impl
from sub_commands.review import (
    cmoc_review_oracle_command_impl,
)
from sub_commands.session.abandon import cmoc_session_abandon_command_impl
from sub_commands.session.fork import cmoc_session_fork_command_impl
from sub_commands.session.join import cmoc_session_join_command_impl
from sub_commands.tui import cmoc_tui_command_impl


class _CmocTyperGroup(typer.core.TyperGroup):
    """通常の CLI 引数解析エラーを cmoc のエラーレポートへ変換する。"""

    def main(
        self,
        args: Sequence[str] | None = None,
        prog_name: str | None = None,
        complete_var: str | None = None,
        standalone_mode: bool = True,
        windows_expand_args: bool = True,
        **extra: object,
    ) -> object:
        click_kwargs = {
            "args": args,
            "prog_name": prog_name,
            "complete_var": complete_var,
            "windows_expand_args": windows_expand_args,
            **extra,
        }
        if "_CMOC_COMPLETE" in os.environ:
            return super().main(standalone_mode=standalone_mode, **click_kwargs)
        try:
            result = super().main(standalone_mode=False, **click_kwargs)
        except click.ClickException as exc:
            typer.echo(
                render_error(
                    CmocError(
                        "CLI 引数解析に失敗しました。",
                        ["コマンド名、サブコマンド名、option、引数を確認して再実行してください。"],
                        exc.format_message(),
                    )
                ),
                err=True,
            )
            if standalone_mode:
                raise SystemExit(exc.exit_code) from exc
            raise
        if standalone_mode and isinstance(result, int):
            raise SystemExit(result)
        return result


app = typer.Typer(cls=_CmocTyperGroup, no_args_is_help=True)
session_app = typer.Typer(no_args_is_help=True)
apply_app = typer.Typer(no_args_is_help=True)
review_app = typer.Typer(no_args_is_help=True)
app.add_typer(session_app, name="session")
app.add_typer(apply_app, name="apply")
app.add_typer(review_app, name="review")


@app.command()
def init() -> None:
    cmoc_init_command_impl()


@app.command()
def tui() -> None:
    cmoc_tui_command_impl()


@session_app.command("fork")
def session_fork() -> None:
    cmoc_session_fork_command_impl()


@session_app.command("join")
def session_join() -> None:
    cmoc_session_join_command_impl()


@session_app.command("abandon")
def session_abandon() -> None:
    cmoc_session_abandon_command_impl()


@apply_app.command("fork")
def apply_fork(scope: str = typer.Option("rolling", "--scope", "-s")) -> None:
    cmoc_apply_fork_command_impl(scope)


@apply_app.command("join")
def apply_join(force_resolve: bool = typer.Option(False, "--force-resolve")) -> None:
    cmoc_apply_join_command_impl(force_resolve)


@apply_app.command("abandon")
def apply_abandon() -> None:
    cmoc_apply_abandon_command_impl()


@review_app.command("oracle")
def review_oracle(scope: str = typer.Option("session", "--scope", "-s")) -> None:
    cmoc_review_oracle_command_impl(scope)


@app.command()
def indexing() -> None:
    cmoc_indexing_command_impl()


def main() -> None:
    app(prog_name="cmoc")


if __name__ == "__main__":
    main()
