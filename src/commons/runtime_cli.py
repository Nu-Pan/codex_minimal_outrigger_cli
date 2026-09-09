"""最外側 CLI サブコマンドの実行ライフサイクルと終端処理を統括する。"""

import traceback
from collections.abc import Callable, Sequence
from contextvars import ContextVar
from pathlib import Path
from typing import Any, Literal

import typer

from .runtime_doctor import run_doctor_preprocess
from .runtime_errors import DEFAULT_NEXT_ACTION, CmocError, render_error
from .runtime_feedback import start_feedback_invocation, stop_feedback_invocation
from .runtime_feedback_store import feedback_completion_counts
from .runtime_logging import (
    SubcommandLogger,
    current_subcommand_logger,
    reset_current_subcommand_logger,
    set_current_subcommand_logger,
)
from .runtime_paths import console_timestamp, format_duration, repo_root, work_root
from .runtime_primary_report import (
    PrimaryReportSaveError,
    ensure_primary_report,
    reset_primary_report_context,
    start_primary_report_context,
)
from .runtime_results import TerminalResult
from .runtime_windows_toast import ToastState, notify_terminal_result

TerminalClassification = Literal["natural_completion", "user_interruption", "error"]

_CURRENT_STEP_TOTAL: ContextVar[int | None] = ContextVar(
    "CURRENT_STEP_TOTAL", default=None
)
_CURRENT_USER_INTERRUPTION: ContextVar[bool | None] = ContextVar(
    "CURRENT_USER_INTERRUPTION", default=None
)
_CURRENT_TUI_PROCESS_STARTED: ContextVar[bool | None] = ContextVar(
    "CURRENT_TUI_PROCESS_STARTED", default=None
)


class _FinalizedSubcommandExit(RuntimeError):
    """terminal result 確定後に non-zero 終了だけを外側へ伝える。"""

    def __init__(self, returncode: int) -> None:
        """確定済みの終了コードを保持する。"""
        super().__init__(f"finalized subcommand exit: {returncode}")
        self.returncode = returncode


def run_cli_subcommand(
    impl: Callable[..., Any],
    *args: Any,
    pre_log_check: Callable[[Path], None] | None = None,
    command_name: str | None = None,
    command_argv: Sequence[str] | None = None,
    use_work_root_runtime: bool = False,
    doctor_preprocess: bool = True,
    tui_process: bool = False,
    interruptible: bool = False,
    total_steps: int = 1,
    **kwargs: Any,
) -> None:
    """最外側 CLI サブコマンドの実行、診断ログ、terminal result を管理する。

    根拠:
    - {{work-root}}/oracle/doc/app_spec/console_and_file_log.md
    - {{work-root}}/oracle/doc/app_spec/error_handling.md
    """
    logger: SubcommandLogger | None = None
    logger_token = None
    feedback_invocation = None
    feedback_token = None
    step_total_token = None
    tui_process_started_token = _CURRENT_TUI_PROCESS_STARTED.set(False)
    interruption_token = _CURRENT_USER_INTERRUPTION.set(False)
    name = command_name or impl.__name__
    notification_root = Path.cwd()
    terminal_state: ToastState | None = None
    impl_started = False
    error_returncode: int | None = None
    argv = tuple(command_argv or [name])
    primary_report_token = start_primary_report_context(name)

    def stop_feedback() -> None:
        """collector を一度だけ drain し、terminal result 後の出力を防ぐ。"""
        nonlocal feedback_invocation, feedback_token
        if feedback_token is None:
            return
        token = feedback_token
        invocation = feedback_invocation
        feedback_token = None
        feedback_invocation = None
        stop_feedback_invocation(invocation, token)

    try:
        current_root = work_root()
        notification_root = repo_root()
        runtime_root = current_root if use_work_root_runtime else notification_root
        logger = SubcommandLogger(notification_root, name)
        logger_token = set_current_subcommand_logger(logger)
        _emit_progress(f"実行 ID: {logger.invocation_id}")
        step_total_token = _CURRENT_STEP_TOTAL.set(total_steps)
        logger.event("command_invoked", argv=list(argv))
        feedback_invocation, feedback_token = start_feedback_invocation(
            notification_root,
            current_root,
            name,
            logger,
        )
        _emit_progress(f"cmoc {name} を開始")
        require_current_directory_is_work_root(current_root)
        if doctor_preprocess:
            start_subcommand_step(1, "doctor preprocess", "doctor preprocess")
            run_doctor_preprocess(current_root)
        if pre_log_check is not None:
            pre_log_check(runtime_root)
        impl_started = True
        impl_result = impl(*args, **kwargs)
        if isinstance(impl_result, int):
            returncode = impl_result
            specific_result = TerminalResult()
        elif isinstance(impl_result, TerminalResult):
            returncode = 0
            specific_result = impl_result
        elif impl_result is None:
            returncode = 0
            specific_result = TerminalResult()
        else:
            raise TypeError(
                "subcommand implementation must return None, int, or TerminalResult"
            )
        if returncode:
            error_returncode = returncode
            raise CmocError(
                "サブコマンドがエラー終了しました。",
                ["診断用サブコマンドログを確認してから再実行してください。"],
                f"returncode: {returncode}",
                terminal_result=specific_result,
            )

        stop_feedback()
        classification: TerminalClassification = (
            "user_interruption"
            if _CURRENT_USER_INTERRUPTION.get()
            else "natural_completion"
        )
        finalized_returncode = _finalize_subcommand(
            logger,
            name,
            argv,
            classification,
            specific_result,
            returncode=0,
            emit_console=not tui_process,
        )
        if finalized_returncode != 0:
            raise _FinalizedSubcommandExit(finalized_returncode)
        if not tui_process:
            terminal_state = (
                "interrupted" if classification == "user_interruption" else "completed"
            )
    except _FinalizedSubcommandExit as exc:
        terminal_state = "failed"
        raise typer.Exit(exc.returncode) from exc
    except KeyboardInterrupt as exc:
        if interruptible and not impl_started:
            mark_current_subcommand_interrupted()
            stop_feedback()
            if logger is not None:
                logger.event("user_interruption", result="interrupted")
                finalized_returncode = _finalize_subcommand(
                    logger,
                    name,
                    argv,
                    "user_interruption",
                    TerminalResult(),
                    returncode=0,
                    emit_console=not tui_process,
                )
                if finalized_returncode != 0:
                    terminal_state = "failed"
                    raise typer.Exit(finalized_returncode) from exc
            terminal_state = None if tui_process else "interrupted"
            return

        stop_feedback()
        if tui_process and _CURRENT_TUI_PROCESS_STARTED.get():
            # TUI process に制御を渡した後の signal は TUI に委ね、追加表示しない。
            if logger is not None:
                _finalize_subcommand(
                    logger,
                    name,
                    argv,
                    "error",
                    TerminalResult(),
                    returncode=130,
                    error=exc,
                    emit_console=False,
                )
            raise

        if logger is not None:
            finalized_returncode = _finalize_subcommand(
                logger,
                name,
                argv,
                "error",
                TerminalResult(
                    next_actions=("必要な状態を確認してから再実行してください。",)
                ),
                returncode=130,
                error=exc,
                # TUI 起動前の中断は起動エラーとして表示する。その他の
                # KeyboardInterrupt は外側へ委ね、cmoc の表示を追加しない。
                emit_console=tui_process,
            )
        elif tui_process:
            typer.echo(render_error(exc), err=True)
        terminal_state = "failed"
        raise
    except BaseException as exc:
        failed_returncode = error_returncode if error_returncode is not None else 1
        stop_feedback()
        if logger is not None:
            supplied_result = getattr(exc, "terminal_result", None)
            if not isinstance(supplied_result, TerminalResult):
                supplied_result = getattr(exc, "cmoc_terminal_result", None)
            if not isinstance(supplied_result, TerminalResult):
                supplied_result = TerminalResult()
            finalized_returncode = _finalize_subcommand(
                logger,
                name,
                argv,
                "error",
                supplied_result,
                returncode=failed_returncode,
                error=exc,
                emit_console=True,
            )
            failed_returncode = finalized_returncode
        else:
            typer.echo(render_error(exc), err=True)
        terminal_state = "failed"
        raise typer.Exit(failed_returncode) from exc
    finally:
        # terminal result へ到達する通常経路では既に drain 済みである。初期化途中の
        # 想定外 failure だけをここで回収し、collector を残さない。
        if feedback_token is not None:
            stop_feedback_invocation(feedback_invocation, feedback_token)
        if step_total_token is not None:
            _CURRENT_STEP_TOTAL.reset(step_total_token)
        if logger_token is not None:
            reset_current_subcommand_logger(logger_token)
        _CURRENT_TUI_PROCESS_STARTED.reset(tui_process_started_token)
        _CURRENT_USER_INTERRUPTION.reset(interruption_token)
        reset_primary_report_context(primary_report_token)
        if terminal_state is not None:
            _notify_terminal_result_safely(name, notification_root, terminal_state)


def mark_current_subcommand_interrupted() -> None:
    """現在の最外側サブコマンドを正常なユーザー中断完了として印付けする。"""
    # {{work-root}}/oracle/doc/app_spec/subcommand_interruption.md
    if _CURRENT_USER_INTERRUPTION.get() is not None:
        _CURRENT_USER_INTERRUPTION.set(True)


def mark_current_tui_process_started() -> None:
    """現在の TUI invocation が Codex process の起動境界へ到達したと印付けする。"""
    # {{work-root}}/oracle/doc/app_spec/windows_toast_notification.md
    if _CURRENT_TUI_PROCESS_STARTED.get() is not None:
        _CURRENT_TUI_PROCESS_STARTED.set(True)


def _notify_terminal_result_safely(
    command_name: str,
    repository_root: Path,
    state: ToastState,
) -> None:
    """確定済み result を、通知失敗から完全に分離して送る。"""
    # {{work-root}}/oracle/doc/app_spec/windows_toast_notification.md
    try:
        notify_terminal_result(command_name, repository_root, state)
    except BaseException:
        pass


def start_subcommand_step(
    index: int | str,
    description: str,
    log_description: str | None = None,
) -> None:
    """全 step をログへ記録し、トップレベル step だけを stderr へ通知する。"""
    # {{work-root}}/oracle/doc/app_spec/console_and_file_log.md
    logger = current_subcommand_logger()
    if logger is None:
        return
    if isinstance(index, int):
        total = _CURRENT_STEP_TOTAL.get()
        step_index = f"{index}/{total}" if total is not None else str(index)
    else:
        step_index = index
    logger.start_step(step_index, description, log_description)
    if isinstance(index, int):
        _emit_progress(f"cmoc {logger.command}: {description}")


def require_current_directory_is_work_root(root: Path) -> None:
    """cmoc が work root で実行されている前提を検査する。

    根拠: {{work-root}}/oracle/doc/app_spec/codex_exec_rule.md の
    「cmoc process の cwd との関係」
    """
    if Path.cwd().resolve() == root.resolve():
        return
    raise CmocError(
        "cmoc は work root で実行してください。",
        ["git repository の root directory へ移動してから再実行してください。"],
        f"cwd: {Path.cwd().resolve()}\nwork_root: {root.resolve()}",
    )


def _emit_progress(message: str) -> None:
    """短い進行通知を stderr へ一行で表示する。"""
    typer.echo(f"# {console_timestamp()} {message}", err=True)


def _finalize_subcommand(
    logger: SubcommandLogger,
    command_name: str,
    command_argv: tuple[str, ...],
    classification: TerminalClassification,
    specific_result: TerminalResult,
    *,
    returncode: int,
    error: BaseException | None = None,
    emit_console: bool,
) -> int:
    """終了状態をログへ flush した後、terminal result を一度だけ表示する。"""
    try:
        logger.finish_current_step()
    except BaseException:
        pass

    pending: int | None
    feedback_warnings: list[str]
    try:
        pending, feedback_warnings = feedback_completion_counts(logger.root)
    except BaseException:
        pending = None
        feedback_warnings = ["feedback observation 件数を計算できませんでした。"]

    for warning in (*specific_result.warnings, *feedback_warnings):
        try:
            logger.record_warning(warning, emit=False)
        except BaseException:
            pass

    terminal_result = _error_terminal_result(specific_result, error)
    try:
        terminal_result = ensure_primary_report(
            logger.root,
            command_name,
            command_argv,
            classification,
            returncode,
            terminal_result,
            logger,
        )
    except PrimaryReportSaveError as report_error:
        # {{work-root}}/oracle/doc/app_spec/error_handling.md
        # report 保存失敗は元の終端結果に代わる internal failure とする。未保存の
        # role/path を持たない新しい result を使い、console へ候補 path を出さない。
        classification = "error"
        returncode = 1
        error = report_error
        terminal_result = _error_terminal_result(TerminalResult(), report_error)
    elapsed = logger.elapsed()
    terminal_record = _terminal_result_record(
        terminal_result,
        classification,
        command_name,
        logger.warning_messages,
        pending,
        elapsed,
        returncode,
        logger.path,
    )
    event_payload: dict[str, Any] = {
        "classification": classification,
        "returncode": returncode,
        "elapsed_sec": elapsed,
        "quota_wait_sec": logger.quota_wait_sec,
        "pending_feedback_observation_count": pending,
        "warnings": list(logger.warning_messages),
        "terminal_result": terminal_record,
    }
    if terminal_result.primary_report is not None:
        event_payload["primary_report_path"] = str(
            terminal_result.primary_report.resolve(strict=False)
        )
    if terminal_result.result is not None:
        event_payload["result"] = terminal_result.result
    if terminal_result.completion_reason is not None:
        event_payload["completion_reason"] = terminal_result.completion_reason
    if error is not None:
        event_payload["failure"] = _failure_record(error)
    try:
        logger.event("command_finished", **event_payload)
    except BaseException:
        # 元の結果を隠さない。ログ flush failure 自体は terminal result の診断 path
        # から確認できる既存の内部障害として扱う。
        pass

    if emit_console:
        typer.echo(
            _render_terminal_result(
                terminal_result,
                classification,
                command_name,
                logger.warning_messages,
                pending,
                elapsed,
                returncode,
                logger.path,
            ),
            err=classification == "error",
        )
    return returncode


def _error_terminal_result(
    result: TerminalResult,
    error: BaseException | None,
) -> TerminalResult:
    """error 分類に理由と実際の次の操作を補い、固有結果と統合する。"""
    if error is None:
        return result
    if isinstance(error, CmocError):
        reason = error.summary
        detail = _without_primary_report_path(error.detail, result.primary_report)
        actions = tuple(error.next_actions) or (DEFAULT_NEXT_ACTION,)
    elif isinstance(error, KeyboardInterrupt):
        reason = "サブコマンドが中断されました。"
        detail = "KeyboardInterrupt"
        actions = result.next_actions
    else:
        reason = str(error) or error.__class__.__name__
        detail = repr(error)
        actions = ("診断用サブコマンドログを確認してください。",)
    error_details: tuple[tuple[str, object], ...] = (("理由", reason),)
    if detail:
        error_details += (("詳細", detail),)
    return TerminalResult(
        primary_report=result.primary_report,
        primary_report_role=result.primary_report_role,
        result=result.result,
        completion_reason=result.completion_reason,
        details=(*result.details, *error_details),
        next_actions=_deduplicate((*result.next_actions, *actions)),
        warnings=result.warnings,
    )


def _without_primary_report_path(detail: str, report_path: Path | None) -> str:
    """primary report path を error detail に重複表示しない。"""
    if report_path is None:
        return detail
    candidates = {
        str(report_path),
        str(report_path.resolve(strict=False)),
    }
    return "\n".join(
        line
        for line in detail.splitlines()
        if not any(path in line for path in candidates)
    )


def _failure_record(error: BaseException) -> dict[str, object]:
    """handled/internal の分類と診断詳細を subcommand log へ保存する。"""
    if isinstance(error, CmocError):
        return {
            "classification": "handled_failure",
            "type": error.__class__.__name__,
            "summary": error.summary,
            "detail": error.detail,
            "next_actions": list(error.next_actions),
        }
    if isinstance(error, PrimaryReportSaveError):
        record: dict[str, object] = {
            "classification": "internal_failure",
            "type": error.__class__.__name__,
            "message": str(error),
            "traceback": "".join(traceback.format_exception(error)),
        }
        if error.target_path is not None:
            # {{work-root}}/oracle/doc/app_spec/error_handling.md
            # 未保存 path は terminal result へ出さないが、失敗対象の特定に必要な
            # 診断情報として subcommand log には絶対 path を残す。
            record["target_path"] = str(error.target_path.absolute())
        return record
    if isinstance(error, KeyboardInterrupt):
        return {
            "classification": "handled_failure",
            "type": error.__class__.__name__,
            "summary": "keyboard interruption",
        }
    return {
        "classification": "internal_failure",
        "type": error.__class__.__name__,
        "message": str(error),
        "traceback": "".join(traceback.format_exception(error)),
    }


def _terminal_result_record(
    result: TerminalResult,
    classification: TerminalClassification,
    command_name: str,
    warnings: list[str],
    pending: int | None,
    elapsed: float,
    returncode: int,
    log_path: Path,
) -> dict[str, object]:
    """console と同じ terminal result を JSON event 用 object にする。"""
    return {
        "classification": classification,
        "command": command_name,
        "primary_report_role": result.primary_report_role,
        "primary_report_path": (
            str(result.primary_report.resolve(strict=False))
            if result.primary_report is not None
            else None
        ),
        "result": result.result,
        "completion_reason": result.completion_reason,
        "details": [
            {"name": name, "value": _record_value(value)}
            for name, value in result.details
        ],
        "next_actions": list(result.next_actions),
        "warnings": list(warnings),
        "pending_feedback_observation_count": pending,
        "elapsed_sec": elapsed,
        "returncode": returncode,
        "diagnostic_log_path": str(log_path.resolve(strict=False)),
    }


def _render_terminal_result(
    result: TerminalResult,
    classification: TerminalClassification,
    command_name: str,
    warnings: list[str],
    pending: int | None,
    elapsed: float,
    returncode: int,
    log_path: Path,
) -> str:
    """仕様の優先順序で、一つの Markdown terminal result を描画する。"""
    heading = {
        "natural_completion": "完了",
        "user_interruption": "中断完了",
        "error": "失敗",
    }[classification]
    lines = [f"# {heading}: cmoc {command_name}"]
    if result.primary_report is not None:
        lines.append(
            f"- primary report ({result.primary_report_role}): "
            f"`{result.primary_report.resolve(strict=False)}`"
        )
    if result.result is not None:
        lines.append(f"- result: `{result.result}`")
    if result.completion_reason is not None:
        lines.append(f"- completion_reason: `{result.completion_reason}`")
    lines.extend(
        f"- {name}: `{_display_value(value)}`" for name, value in result.details
    )
    lines.extend(f"- 次の操作: {action}" for action in result.next_actions)
    lines.extend(f"- warning: {warning}" for warning in warnings)
    pending_text = "unavailable" if pending is None else str(pending)
    lines.extend(
        [
            f"- pending feedback observation: `{pending_text}`",
            f"- 経過時間: `{format_duration(elapsed)}`",
            f"- 終了コード: `{returncode}`",
            f"- 診断用サブコマンドログ: `{log_path.resolve(strict=False)}`",
        ]
    )
    return "\n".join(lines)


def _display_value(value: object) -> str:
    """terminal result の scalar を一つの Markdown field に収める。"""
    if isinstance(value, Path):
        return str(value.resolve(strict=False))
    return str(value).replace("`", "'").replace("\n", " | ")


def _record_value(value: object) -> object:
    """Path だけを JSON 化可能なフルパスへ変換する。"""
    if isinstance(value, Path):
        return str(value.resolve(strict=False))
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    return str(value)


def _deduplicate(values: Sequence[str]) -> tuple[str, ...]:
    """表示順を保ったまま重複する案内を除く。"""
    return tuple(dict.fromkeys(value for value in values if value))
