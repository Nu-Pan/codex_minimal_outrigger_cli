from pathlib import Path

from commons.runtime_paths import console_timestamp, format_duration


def emit_codex_call_console(
    purpose: str, call_path: Path, elapsed_sec: float, returncode: int
) -> None:
    """oracle が定める Codex CLI 呼び出し通知を利用者の console へ出す。

    根拠: <work-root>/oracle/doc/app_spec/console_and_file_log.md
    """
    print(
        "\n".join(
            [
                f"# {console_timestamp()} Codex CLI call",
                f"- Purpose: `{purpose}`",
                f"- Call log: `{call_path}`",
                f"- Elapsed time: `{format_duration(elapsed_sec)}`",
                f"- Exit code: `{returncode}`",
            ]
        ),
        flush=True,
    )
