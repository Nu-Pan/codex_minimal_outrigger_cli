from collections.abc import Callable, Sequence
from contextvars import ContextVar
from pathlib import Path
from typing import Any

import typer

from commons.runtime_doctor import run_doctor_preprocess
from commons.runtime_errors import CmocError, render_error
from commons.runtime_logging import (
    SubcommandLogger,
    current_subcommand_logger,
    reset_current_subcommand_logger,
    set_current_subcommand_logger,
)
from commons.runtime_paths import (
    console_timestamp,
    format_duration,
    repo_root,
    work_root,
)

_CURRENT_STEP_TOTAL: ContextVar[int | None] = ContextVar(
    "CURRENT_STEP_TOTAL", default=None
)


def run_cli_subcommand(
    impl: Callable[..., Any],
    *args: Any,
    pre_log_check: Callable[[Path], None] | None = None,
    command_name: str | None = None,
    command_argv: Sequence[str] | None = None,
    error_to_stderr: bool = False,
    use_work_root_runtime: bool = False,
    doctor_preprocess: bool = True,
    total_steps: int = 1,
    **kwargs: Any,
) -> None:
    """CLI サブコマンドの共通実行ライフサイクルを管理する。

    work root 検査後、doctor preprocess より前にサブコマンドログを作成し、
    各サブコマンドの step 通知、完了表示、戻り値の終了コード化、例外のエラー表示を
    一箇所で扱う。
    runtime state は通常 repo root に置き、linked worktree 前処理では work root に置く。
    doctor preprocess は current work root を起点に、current と main repo root の
    両方を修復する。
    サブコマンドログは常に repo root に置く。
    """
    logger = None
    logger_token = None
    step_total_token = None
    error_returncode: int | None = None
    name = command_name or impl.__name__
    try:
        current_root = work_root()
        require_current_directory_is_work_root(current_root)
        log_root = repo_root()
        runtime_root = current_root if use_work_root_runtime else log_root
        logger = SubcommandLogger(log_root, name)
        logger_token = set_current_subcommand_logger(logger)
        step_total_token = _CURRENT_STEP_TOTAL.set(total_steps)
        logger.event("command_invoked", argv=list(command_argv or [name]))
        typer.echo(f"# {console_timestamp()} 開始 {name}")
        typer.echo(f"- サブコマンドログ: `{logger.path}`")
        if doctor_preprocess:
            # {{work-root}}/oracle/doc/app_spec/doctor_preprocess.md
            # {{work-root}}/oracle/doc/app_spec/console_and_file_log.md
            # 共通修復の失敗もサブコマンド単位の終了経路として記録する。
            start_subcommand_step(1, "doctor preprocess", "doctor preprocess")
            run_doctor_preprocess(current_root)
        if pre_log_check is not None:
            # {{work-root}}/oracle/doc/app_spec/console_and_file_log.md
            # 固有の事前条件で失敗しても、サブコマンドログは先に作成しておく。
            pre_log_check(runtime_root)
        impl_result = impl(*args, **kwargs)
        returncode = impl_result if isinstance(impl_result, int) else 0
        if returncode:
            # {{work-root}}/oracle/doc/app_spec/error_handling.md
            # callback の非 0 return を typer.Exit で終えると report を迂回するため、
            # 共通の例外経路へ変換する。
            error_returncode = returncode
            raise CmocError(
                "サブコマンドがエラー終了しました。",
                [
                    "サブコマンドログを確認してから同じコマンドを再実行してください。",
                    "入力、設定、作業ツリーの状態を確認してから再実行してください。",
                ],
                f"returncode: {returncode}",
            )
        logger.finish_current_step()
        logger.event(
            "command_finished",
            returncode=returncode,
            elapsed_sec=logger.elapsed(),
            quota_wait_sec=logger.quota_wait_sec,
        )
        _emit_completion_summary(logger, name, returncode)
    except BaseException as exc:
        failed_returncode = error_returncode if error_returncode is not None else 1
        if logger:
            logger.finish_current_step()
            logger.event(
                "command_finished",
                returncode=failed_returncode,
                elapsed_sec=logger.elapsed(),
                quota_wait_sec=logger.quota_wait_sec,
                error=str(exc),
            )
            _emit_completion_summary(logger, name, failed_returncode)
        result_stdout = getattr(exc, "cmoc_stdout", None)
        if result_stdout is not None:
            typer.echo(str(result_stdout))
        # {{work-root}}/oracle/doc/app_spec/error_handling.md は stdout を既定とし、
        # サブコマンド固有の正本だけが stderr への変更を許可する。
        typer.echo(
            render_error(exc),
            err=(error_to_stderr or bool(getattr(exc, "cmoc_error_to_stderr", False))),
        )
        raise typer.Exit(failed_returncode) from exc
    finally:
        if step_total_token is not None:
            _CURRENT_STEP_TOTAL.reset(step_total_token)
        if logger_token is not None:
            reset_current_subcommand_logger(logger_token)


def start_subcommand_step(
    index: int | str,
    description: str,
    log_description: str | None = None,
) -> None:
    """現在のサブコマンドの step 開始をログとコンソールへ通知する。

    根拠: {{work-root}}/oracle/doc/app_spec/console_and_file_log.md
    """
    logger = current_subcommand_logger()
    if logger is None:
        return
    if isinstance(index, int):
        total = _CURRENT_STEP_TOTAL.get()
        step_index = f"{index}/{total}" if total is not None else str(index)
    else:
        step_index = index
    logger.start_step(step_index, description, log_description)
    typer.echo(f"# {console_timestamp()} ({step_index}) {description}")


def require_current_directory_is_work_root(root: Path) -> None:
    """cmoc が work root で実行されている前提を検査する。

    根拠: {{work-root}}/oracle/doc/app_spec/misc_spec.md
    """
    if Path.cwd().resolve() == root.resolve():
        return
    raise CmocError(
        "cmoc は work root で実行してください。",
        ["git repository の root directory へ移動してから再実行してください。"],
        f"cwd: {Path.cwd().resolve()}\nwork_root: {root.resolve()}",
    )


def _emit_completion_summary(
    logger: SubcommandLogger, command_name: str, returncode: int
) -> None:
    """サブコマンド完了時に記録済み step の stdout サマリーを出力する。

    根拠: {{work-root}}/oracle/doc/app_spec/console_and_file_log.md
    """
    elapsed = logger.elapsed()
    typer.echo(f"# {console_timestamp()} 完了 {command_name}")
    typer.echo(f"- サブコマンドログ: `{logger.path}`")
    for step in logger.step_timings:
        step_elapsed = step.elapsed_sec
        if step_elapsed is None:
            step_elapsed = elapsed - (step.started_at - logger.started_at)
        typer.echo(
            f"- ステップ経過時間[{step.index} {step.description}]: `{format_duration(step_elapsed)}`"
        )
    typer.echo(f"- 経過時間: `{format_duration(elapsed)}`")
    typer.echo(f"- quota 待機時間: `{format_duration(logger.quota_wait_sec)}`")
    typer.echo(f"- 終了コード: `{returncode}`")
