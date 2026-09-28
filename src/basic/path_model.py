"""`{{work-root}}/oracle/src/oracle/other/path_model.py` の公開 path model を再公開する。

正本実装を realization 側へ複製せず既存の `basic.path_model` 参照を保つために残す。
削除条件は realization 側と利用者向け公開面から `basic.path_model` 参照がなくなること。
"""

from pathlib import Path

from oracle.other.path_model import (
    AgentCallPathContext,
    RootPathPlaceHolder,
    resolve_ph_path,
)
from oracle.other.path_model import (
    resolve_real_path as _resolve_real_path,
)


def resolve_real_path(
    source: RootPathPlaceHolder | str | Path,
    path_context: AgentCallPathContext | None = None,
) -> Path:
    """oracle resolver を使い、run-root が最寄りの linked worktree と一致するか確認する。"""
    if not _uses_run_root_placeholder(source):
        return _resolve_real_path(source, path_context)

    try:
        resolved_context = path_context or AgentCallPathContext(Path.cwd())
        run_root = _resolve_real_path(RootPathPlaceHolder.RUN, resolved_context)
    except ValueError:
        raise ValueError("`{{run-root}}` was not found") from None

    if (
        resolved_context.work_root == resolved_context.repo_root
        or resolved_context.work_root != run_root
    ):
        raise ValueError("`{{run-root}}` was not found")

    return _resolve_real_path(source, resolved_context)


def _uses_run_root_placeholder(source: RootPathPlaceHolder | str | Path) -> bool:
    """source が `{{run-root}}` 自体またはその配下を指すか返す。"""
    if isinstance(source, RootPathPlaceHolder):
        return source is RootPathPlaceHolder.RUN
    if isinstance(source, str):
        source = Path(source)
    return bool(source.parts) and source.parts[0] == RootPathPlaceHolder.RUN.value


__all__ = [
    "AgentCallPathContext",
    "RootPathPlaceHolder",
    "resolve_ph_path",
    "resolve_real_path",
]
