"""CLI・外部コマンド・Codex exec の共有結果モデルを定義する。"""

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Protocol, Sequence


@dataclass(frozen=True)
class TerminalResult:
    """最外側サブコマンドの terminal result に渡す固有情報。"""

    # {{work-root}}/oracle/doc/app_spec/console_and_file_log.md
    primary_report: Path | None = None
    primary_report_role: str | None = None
    result: str | None = None
    completion_reason: str | None = None
    details: tuple[tuple[str, object], ...] = ()
    next_actions: tuple[str, ...] = ()
    warnings: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        """競合するサブコマンド固有結果と不完全な report 指定を拒否する。"""
        if self.result is not None and self.completion_reason is not None:
            raise ValueError("result and completion_reason are mutually exclusive")
        if (self.primary_report is None) != (self.primary_report_role is None):
            raise ValueError(
                "primary_report and primary_report_role must be specified together"
            )


class CodexExecOutput(Protocol):
    """Codex exec 利用側が structured output から参照する最小契約。"""

    @property
    def output_json(self) -> Any:
        """Codex Structured Output の検証済み JSON 値。"""
        ...


CodexExecCallable = Callable[..., CodexExecOutput]


@dataclass(frozen=True)
class CommandResult:
    """外部コマンド実行の終了コードと標準入出力を表す。"""

    returncode: int
    stdout: str
    stderr: str


# {{work-root}}/oracle/doc/app_spec/codex_exec_rule.md
@dataclass(frozen=True)
class StructuredOutputValidationIssue:
    """Structured Output の補正 prompt へ渡す機械的検証エラー。"""

    condition: str
    location: str
    expected: str
    observed: str


StructuredOutputPostcondition = Callable[
    [Any, frozenset[str]], Sequence[StructuredOutputValidationIssue]
]


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
