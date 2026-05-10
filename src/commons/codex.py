"""Codex CLI 呼び出しの共通処理。"""

from pathlib import Path

from commons.process import run_command


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

    result = run_command(args, repo_root)
    return result.stdout
