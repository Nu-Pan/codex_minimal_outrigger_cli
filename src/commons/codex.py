"""Codex CLI 呼び出しの共通処理。"""

from pathlib import Path

from commons.errors import CmotError
from commons.process import run_command
from commons.progress import format_elapsed, progress, start_timer


def run_codex_exec(repo_root: Path, prompt: str, *, read_only: bool) -> str:
    """codex exec へ prompt を渡して実行する。

    Args:
        repo_root: 操作対象 repository root。
        prompt: Codex CLI に渡す指示。
        read_only: Codex 側の sandbox を read-only にするか。

    Returns:
        codex exec の標準出力。
    """
    # Codex CLI 側にも作業 root を明示する。
    args = ["codex", "exec", "--cd", str(repo_root)]
    if read_only:
        args.extend(["--sandbox", "read-only"])
    args.append(prompt)

    # Codex の標準出力は戻り値として使い、標準エラーの実行ログだけ表示する。
    sandbox = "read-only" if read_only else "workspace-write"
    started_at = start_timer()
    progress(f"codex exec started ({sandbox})")
    try:
        result = run_command(args, repo_root, stream_stderr_to_stdout=True)
    except CmotError:
        progress(f"codex exec failed in {format_elapsed(started_at)}")
        raise

    progress(f"codex exec completed in {format_elapsed(started_at)}")
    return result.stdout
