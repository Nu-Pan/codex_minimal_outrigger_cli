"""外部コマンド実行の薄いラッパー。"""

import subprocess
import sys
from pathlib import Path

from commons.errors import CmotError


def run_command(
    args: list[str],
    cwd: Path,
    *,
    capture_output: bool = True,
    check: bool = True,
    stream_stderr_to_stdout: bool = False,
) -> subprocess.CompletedProcess[str]:
    """外部コマンドを実行し、失敗時は cmot のエラーへ変換する。

    Args:
        args: 実行するコマンドと引数。
        cwd: コマンドの実行ディレクトリ。
        capture_output: 標準出力と標準エラーを捕捉するか。
        check: 非ゼロ終了をエラーにするか。
        stream_stderr_to_stdout: 標準エラーを cmot の標準出力へ流すか。

    Returns:
        コマンドの実行結果。
    """
    try:
        # capture_output=True と明示的な stderr 指定は併用できないため分岐する。
        stdout = subprocess.PIPE if capture_output else None
        if stream_stderr_to_stdout:
            stderr = sys.stdout
        else:
            stderr = subprocess.PIPE if capture_output else None

        return subprocess.run(
            args,
            cwd=cwd,
            text=True,
            stdout=stdout,
            stderr=stderr,
            check=check,
        )
    except FileNotFoundError as exc:
        raise CmotError(f"command not found: {args[0]}") from exc
    except subprocess.CalledProcessError as exc:
        stderr = (exc.stderr or "").strip()
        stdout = (exc.stdout or "").strip()
        detail = stderr or stdout or f"exit status {exc.returncode}"
        raise CmotError(f"command failed: {' '.join(args)}\n{detail}") from exc
