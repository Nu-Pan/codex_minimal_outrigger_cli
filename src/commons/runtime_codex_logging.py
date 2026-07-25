import sys
from pathlib import Path

from commons.runtime_errors import CmocError
from commons.runtime_paths import console_timestamp, format_duration


def emit_codex_call_console(
    purpose: str,
    call_path: Path,
    elapsed_sec: float,
    returncode: int | None,
    error: str | None = None,
) -> None:
    """Codex CLI 呼び出し通知を利用者の console へ出す。

    起動前に失敗して終了コードを得られない場合は、起動されなかったことと
    起動エラーを併記する。

    根拠: {{work-root}}/oracle/doc/app_spec/console_and_file_log.md
    """
    lines = [
        f"# {console_timestamp()} Codex CLI call",
        f"- Purpose: `{purpose}`",
        f"- Call log: `{call_path}`",
        f"- Elapsed time: `{format_duration(elapsed_sec)}`",
        f"- Exit code: `{returncode if returncode is not None else 'not started'}`",
    ]
    if error is not None:
        safe_error = error.replace("\n", " ")
        lines.append(f"- Error: `{safe_error}`")
    # {{work-root}}/oracle/doc/app_spec/console_and_file_log.md
    # 非 0 終了も Codex 呼び出しのエラーなので、起動後の失敗も stderr に出す。
    is_error = error is not None or returncode not in (None, 0)
    print(
        "\n".join(lines),
        file=sys.stderr if is_error else sys.stdout,
        flush=True,
    )


def format_codex_call_error(error: BaseException) -> str:
    """Codex 起動失敗を console と event に共通の error text へ変換する。

    根拠: {{work-root}}/oracle/doc/app_spec/console_and_file_log.md
    """
    if isinstance(error, CmocError):
        return f"{error.summary}: {error.detail}"
    return str(error) or repr(error)
