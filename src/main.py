import os
from collections.abc import Sequence
from enum import Enum
from typing import Any, cast

import click
import typer

from cmoc_runtime import (
    CmocError,
    render_error,
)
from sub_commands.doctor import cmoc_doctor_impl
from sub_commands.indexing import cmoc_indexing_impl
from sub_commands.oracle.edit import cmoc_oracle_edit_impl
from sub_commands.oracle.investigation import cmoc_oracle_investigation_impl
from sub_commands.oracle.review import cmoc_oracle_review_impl
from sub_commands.realization.apply.fork import cmoc_realization_apply_fork_impl
from sub_commands.realization.refactor.fork import cmoc_realization_refactor_fork_impl
from sub_commands.run.abandon import cmoc_run_abandon_impl
from sub_commands.run.join import cmoc_run_join_impl
from sub_commands.session.abandon import cmoc_session_abandon_impl
from sub_commands.session.fork import cmoc_session_fork_impl
from sub_commands.session.join import cmoc_session_join_impl
from sub_commands.tui import cmoc_tui_impl


class OracleReviewScope(str, Enum):
    """oracle review の調査対象範囲を CLI option 値として表す。"""

    session = "session"
    full = "full"


def _click_exception_types() -> tuple[type[BaseException], ...]:
    """Typer の版によって異なる Click 例外クラスを安全に集める。"""
    compatibility_module = getattr(typer.core, "_click", None)
    compatibility_exception = getattr(compatibility_module, "ClickException", None)
    if isinstance(compatibility_exception, type) and issubclass(
        compatibility_exception, BaseException
    ):
        return (click.ClickException, compatibility_exception)
    return (click.ClickException,)


_CLICK_EXCEPTION_TYPES = _click_exception_types()


class _CmocTyperGroup(typer.core.TyperGroup):
    """通常の CLI 引数解析エラーを cmoc のエラーレポートへ変換する。"""

    def main(
        self: "_CmocTyperGroup",
        args: Sequence[str] | None = None,
        prog_name: str | None = None,
        complete_var: str | None = None,
        standalone_mode: bool = True,
        windows_expand_args: bool = True,
        **extra: Any,
    ) -> Any:
        """補完時以外の Click 例外を cmoc 形式に変換して実行する。"""
        click_kwargs = {
            "args": args,
            "prog_name": prog_name,
            "complete_var": complete_var,
            "windows_expand_args": windows_expand_args,
            **extra,
        }
        if "_CMOC_COMPLETE" in os.environ:
            # {{work-root}}/oracle/doc/app_spec/cli_auto_completion.md
            # 空の marker も通常実行ではなく補完 probe として扱い、副作用を防ぐ。
            if not os.environ["_CMOC_COMPLETE"]:
                if standalone_mode:
                    raise SystemExit(0)
                return 0
            return super().main(standalone_mode=standalone_mode, **click_kwargs)
        try:
            result = super().main(standalone_mode=False, **click_kwargs)
        # {{work-root}}/oracle/doc/app_spec/error_handling.md
        # Typer 0.27 は Click compatibility module を通じて parse するため、version に
        # 依存しない error-handling contract のため両方の exception class に対応する。
        except _CLICK_EXCEPTION_TYPES as exc:
            click_exception = cast(click.ClickException, exc)
            # {{work-root}}/oracle/doc/app_spec/error_handling.md
            # 未 raise の例外を render_error すると Call stack が概要だけになるため、
            # parser error を cause にした report exception を raise してから描画する。
            try:
                raise CmocError(
                    "CLI 引数解析に失敗しました。",
                    [
                        "コマンド名、サブコマンド名、option、引数を確認して再実行してください。"
                    ],
                    click_exception.format_message(),
                ) from exc
            except CmocError as report_error:
                typer.echo(render_error(report_error))
            if standalone_mode:
                raise SystemExit(click_exception.exit_code) from exc
            raise
        if standalone_mode and isinstance(result, int):
            raise SystemExit(result)
        return result


app = typer.Typer(
    cls=_CmocTyperGroup,
    no_args_is_help=True,
    rich_markup_mode=None,
)
session_app = typer.Typer(no_args_is_help=True, rich_markup_mode=None)
oracle_app = typer.Typer(no_args_is_help=True, rich_markup_mode=None)
realization_app = typer.Typer(no_args_is_help=True, rich_markup_mode=None)
realization_apply_app = typer.Typer(no_args_is_help=True, rich_markup_mode=None)
realization_refactor_app = typer.Typer(no_args_is_help=True, rich_markup_mode=None)
run_app = typer.Typer(no_args_is_help=True, rich_markup_mode=None)
app.add_typer(session_app, name="session")
app.add_typer(oracle_app, name="oracle")
app.add_typer(realization_app, name="realization")
realization_app.add_typer(realization_apply_app, name="apply")
realization_app.add_typer(realization_refactor_app, name="refactor")
app.add_typer(run_app, name="run")


@app.command()
def doctor() -> None:
    """cmoc 実行前の共通検証・修復を明示実行する CLI 入口。"""
    cmoc_doctor_impl()


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


@oracle_app.command("review")
def oracle_review(
    scope: OracleReviewScope = typer.Option(OracleReviewScope.session, "--scope", "-s"),
) -> None:
    """oracle review を隔離 worktree で実行する CLI 入口。"""
    # {{work-root}}/oracle/doc/app_spec/sub_command/oracle_review.md
    cmoc_oracle_review_impl(scope.value)


@oracle_app.command("edit")
def oracle_edit() -> None:
    """oracle file を main worktree の Codex TUI で編集する CLI 入口。"""
    cmoc_oracle_edit_impl()


@oracle_app.command("investigation")
def oracle_investigation() -> None:
    """oracle file の read-only 調査 TUI を起動する CLI 入口。"""
    cmoc_oracle_investigation_impl()


@realization_apply_app.command("fork")
def realization_apply_fork() -> None:
    """oracle 差分へ追従する realization run を開始する CLI 入口。"""
    cmoc_realization_apply_fork_impl()


@realization_refactor_app.command("fork")
def realization_refactor_fork() -> None:
    """full realization refactor cycle を開始する CLI 入口。"""
    cmoc_realization_refactor_fork_impl()


@run_app.command("join")
def run_join(force_resolve: bool = typer.Option(False, "--force-resolve")) -> None:
    """active editing run を session branch へ取り込む CLI 入口。"""
    cmoc_run_join_impl(force_resolve)


@run_app.command("abandon")
def run_abandon() -> None:
    """active editing run を破棄する CLI 入口。"""
    cmoc_run_abandon_impl()


@app.command()
def indexing() -> None:
    """work root の INDEX.md を更新する CLI 入口。"""
    cmoc_indexing_impl()


def main() -> None:
    """console script から Typer app を起動する。"""
    app(prog_name="cmoc")


if __name__ == "__main__":
    main()
