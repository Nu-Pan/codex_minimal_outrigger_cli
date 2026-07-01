from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class CommandResult:
    """外部コマンド実行の終了コードと標準入出力を表す。"""

    returncode: int
    stdout: str
    stderr: str


@dataclass(frozen=True)
class CodexExecResult:
    """Codex exec 呼び出しの生成物と実行結果をまとめて保持する。"""

    returncode: int
    output_text: str
    output_json: Any
    call_log_path: Path
    prompt_log_path: Path
    stdout_log_path: Path
    stderr_log_path: Path
    output_path: Path
    codex_home: Path
    profile_name: str
    profile_path: Path
    schema_path: Path | None
    elapsed_sec: float = 0.0
    quota_wait_sec: float = 0.0
    quota_polls: int = 0
