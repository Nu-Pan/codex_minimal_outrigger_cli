from pathlib import Path

from commons.runtime_paths import console_timestamp, format_duration


def emit_codex_call_console(
    purpose: str, call_path: Path, elapsed_sec: float, returncode: int
) -> None:
    """Codex 呼び出し単位の完了サマリーを利用者の console へ出す。"""
    print(
        "\n".join(
            [
                f"# {console_timestamp()} Codex CLI call",
                f"- purpose: `{purpose}`",
                f"- call_log: `{call_path}`",
                f"- elapsed: `{format_duration(elapsed_sec)}`",
                f"- returncode: `{returncode}`",
            ]
        ),
        flush=True,
    )
