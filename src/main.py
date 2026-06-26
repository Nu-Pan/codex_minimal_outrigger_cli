import os
from collections.abc import Sequence

import click
import typer

from cmoc_runtime import (
    CmocError,
    render_error,
)
from sub_commands.apply.abandon import cmoc_apply_abandon_impl
from sub_commands.apply.fork import cmoc_apply_fork_impl
from sub_commands.apply.join import cmoc_apply_join_impl
from sub_commands.indexing import cmoc_indexing_impl
from sub_commands.init import cmoc_init_impl
from sub_commands.review import (
    cmoc_review_oracle_impl,
)
from sub_commands.session.abandon import cmoc_session_abandon_impl
from sub_commands.session.fork import cmoc_session_fork_impl
from sub_commands.session.join import cmoc_session_join_impl
from sub_commands.tui import cmoc_tui_impl


class _CmocTyperGroup(typer.core.TyperGroup):
    """通常の CLI 引数解析エラーを cmoc のエラーレポートへ変換する。"""

    def main(
        self: "_CmocTyperGroup",
        args: Sequence[str] | None = None,
        prog_name: str | None = None,
        complete_var: str | None = None,
        standalone_mode: bool = True,
        windows_expand_args: bool = True,
        **extra: object,
    ) -> object:
        """補完時以外の Click 例外を cmoc 形式に変換して実行する。"""
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
                )
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
    """work root を cmoc 管理状態へ同期する CLI 入口。"""
    cmoc_init_impl()


@app.command()
def tui() -> None:
    """Codex TUI を cmoc の依頼文と設定で起動する CLI 入口。"""
    cmoc_tui_impl()


@session_app.command("fork")
def session_fork() -> None:
    """現在 branch から session branch を作る CLI 入口。"""
    cmoc_session_fork_impl()


@session_app.command("join")
def session_join() -> None:
    """session branch の成果を home branch へ取り込む CLI 入口。"""
    cmoc_session_join_impl()


@session_app.command("abandon")
def session_abandon() -> None:
    """session branch を取り込まず破棄する CLI 入口。"""
    cmoc_session_abandon_impl()


@apply_app.command("fork")
def apply_fork(scope: str = typer.Option("rolling", "--scope", "-s")) -> None:
    """finding 適用用の apply run を開始する CLI 入口。"""
    cmoc_apply_fork_impl(scope)


@apply_app.command("join")
def apply_join(force_resolve: bool = typer.Option(False, "--force-resolve")) -> None:
    """apply run の成果を session branch へ取り込む CLI 入口。"""
    cmoc_apply_join_impl(force_resolve)


@apply_app.command("abandon")
def apply_abandon() -> None:
    """apply run を取り込まず破棄する CLI 入口。"""
    cmoc_apply_abandon_impl()


@review_app.command("oracle")
def review_oracle(scope: str = typer.Option("session", "--scope", "-s")) -> None:
    """oracle review を隔離 worktree で実行する CLI 入口。"""
    cmoc_review_oracle_impl(scope)


@app.command()
def indexing() -> None:
    """work root の INDEX.md を更新する CLI 入口。"""
    cmoc_indexing_impl()


def main() -> None:
    """console script から Typer app を起動する。"""
    app(prog_name="cmoc")


if __name__ == "__main__":
    main()
