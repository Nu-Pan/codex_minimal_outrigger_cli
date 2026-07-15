from dataclasses import dataclass
from pathlib import Path
from typing import Any, Protocol


class CodexExecResultLike(Protocol):
    """Minimum structured-output surface required by Codex call consumers."""

    @property
    def output_json(self) -> Any:
        """Return the schema-validated JSON payload."""
        ...


class CommandResultLike(Protocol):
    """Minimum subprocess result surface used by injectable command runners."""

    @property
    def returncode(self) -> int: ...

    @property
    def stdout(self) -> str: ...

    @property
    def stderr(self) -> str: ...


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
    schema_path: Path | None
    elapsed_sec: float = 0.0
    quota_wait_sec: float = 0.0
    quota_polls: int = 0
