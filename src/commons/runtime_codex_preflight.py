# {{work-root}}/oracle/doc/app_spec/indexing.md
import threading
from collections.abc import Callable
from contextvars import ContextVar
from pathlib import Path
from typing import Any

from basic.acp import AgentCallParameter
from basic.path_model import AgentCallPathContext

from .runtime_codex import (
    run_codex_exec as runtime_run_codex_exec,
)
from .runtime_codex import (
    run_codex_tui as runtime_run_codex_tui,
)
from .runtime_results import CodexExecCallable, CodexExecResult, CommandResult

_IndexingPreflight = Callable[[Path, CodexExecCallable], None]

_INDEXING_LOCK = threading.Lock()
_INDEXING_ACTIVE: ContextVar[bool] = ContextVar("INDEXING_ACTIVE", default=False)
_INDEXING_PREFLIGHT: _IndexingPreflight | None = None


def configure_indexing_preflight(preflight: _IndexingPreflight) -> None:
    """Codex 呼び出し前に実行する indexing preflight を登録する。"""
    global _INDEXING_PREFLIGHT
    _INDEXING_PREFLIGHT = preflight


def disable_indexing_preflight() -> None:
    """テストや限定実行向けに indexing preflight 登録を解除する。"""
    global _INDEXING_PREFLIGHT
    _INDEXING_PREFLIGHT = None


def run_codex_exec(
    parameter: AgentCallParameter,
    *,
    before_agent_call: Callable[[], None] | None = None,
    **kwargs: Any,
) -> CodexExecResult:
    """INDEX 更新 preflight を挟んで Codex exec 実行本体へ委譲する。"""
    if parameter.run_indexing_preflight:
        _run_indexing_before_codex(_indexing_root_for_codex(parameter))
    if before_agent_call is not None:
        # preflight が作った cmoc 管理 commit を workload が agent の commit と
        # 誤認しないよう、本命 subprocess の直前に呼び出し元へ境界を通知する。
        before_agent_call()
    return runtime_run_codex_exec(parameter, **kwargs)


def run_codex_tui(
    parameter: AgentCallParameter,
    **kwargs: Any,
) -> CommandResult:
    """INDEX 更新を挟んで Codex TUI 実行本体へ委譲する。"""
    if parameter.run_indexing_preflight:
        _run_indexing_before_codex(_indexing_root_for_codex(parameter))
    return runtime_run_codex_tui(parameter, **kwargs)


def _indexing_root_for_codex(parameter: AgentCallParameter) -> Path:
    """Codex 呼び出し設定から indexing の起点 root を決める。"""
    return AgentCallPathContext(parameter.agent_call_cwd).work_root


def _run_indexing_before_codex(root: Path) -> None:
    """再入を抑止しながら登録済み indexing preflight を直列実行する。"""
    if _INDEXING_PREFLIGHT is None or _INDEXING_ACTIVE.get():
        return
    with _INDEXING_LOCK:
        token = _INDEXING_ACTIVE.set(True)
        try:
            _INDEXING_PREFLIGHT(root, run_codex_exec)
        finally:
            _INDEXING_ACTIVE.reset(token)
