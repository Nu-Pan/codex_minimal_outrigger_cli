import threading
from collections.abc import Callable
from contextvars import ContextVar
from pathlib import Path
from typing import Any

from basic.acp import AgentCallParameter
from commons.runtime_codex import (
    run_codex_exec as runtime_run_codex_exec,
    run_codex_tui as runtime_run_codex_tui,
)
from commons.runtime_paths import repo_root, work_root
from commons.runtime_results import CodexExecResult, CommandResult


CodexExec = Callable[..., object]
IndexingPreflight = Callable[[Path, CodexExec], None]

_INDEXING_LOCK = threading.Lock()
_INDEXING_ACTIVE: ContextVar[bool] = ContextVar("INDEXING_ACTIVE", default=False)
_INDEXING_PREFLIGHT: IndexingPreflight | None = None


def configure_indexing_preflight(preflight: IndexingPreflight) -> None:
    global _INDEXING_PREFLIGHT
    _INDEXING_PREFLIGHT = preflight


def disable_indexing_preflight() -> None:
    global _INDEXING_PREFLIGHT
    _INDEXING_PREFLIGHT = None


def run_codex_exec(parameter: AgentCallParameter, **kwargs: Any) -> CodexExecResult:
    purpose = str(kwargs.get("purpose", "codex exec"))
    _run_indexing_before_codex(purpose, _indexing_root_for_codex(kwargs))
    return runtime_run_codex_exec(parameter, **kwargs)


def run_codex_tui(parameter: AgentCallParameter, **kwargs: Any) -> CommandResult:
    purpose = str(kwargs.get("purpose", "codex tui"))
    _run_indexing_before_codex(purpose, _indexing_root_for_codex(kwargs))
    return runtime_run_codex_tui(parameter, **kwargs)


def _indexing_root_for_codex(kwargs: dict[str, Any]) -> Path:
    cwd = kwargs.get("cwd")
    return work_root(cwd) if cwd else kwargs.get("root") or repo_root()


def _run_indexing_before_codex(purpose: str, root: Path) -> None:
    if (
        _INDEXING_PREFLIGHT is None
        or _INDEXING_ACTIVE.get()
        or should_skip_indexing_before_codex(purpose)
    ):
        return
    with _INDEXING_LOCK:
        token = _INDEXING_ACTIVE.set(True)
        try:
            _INDEXING_PREFLIGHT(root, run_codex_exec)
        finally:
            _INDEXING_ACTIVE.reset(token)


def should_skip_indexing_before_codex(purpose: str) -> bool:
    return purpose.startswith("indexing index entry") or "conflict resolution" in purpose
