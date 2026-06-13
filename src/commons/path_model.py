"""Bridge to the oracle path model implementation."""

import subprocess
from pathlib import Path

from utils.path_model import RootToken
from utils.path_model import resolve_cmoc_root
from utils.path_model import resolve_real_path
from utils.path_model import resolve_repo_root as _oracle_resolve_repo_root
from utils.path_model import resolve_run_root
from utils.path_model import resolve_token_path
from utils.path_model import resolve_work_root

__all__ = [
    "RootToken",
    "resolve_real_path",
    "resolve_cmoc_root",
    "resolve_repo_root",
    "resolve_run_root",
    "resolve_work_root",
    "resolve_token_path",
]


def resolve_repo_root(start_path: Path | None = None) -> Path:
    """Return `<repo-root>` using the oracle path model.

    The oracle implementation walks ancestors before consulting git. In the
    sandbox test environment `/tmp/.git` can exist, so an unrelated parent git
    directory may be found before a linked worktree's common dir. For explicit
    start paths, verify that result against git's common dir and correct it
    when git can identify the owning main worktree.
    """
    resolved = _oracle_resolve_repo_root(start_path)
    if start_path is None:
        return resolved

    start = start_path.resolve()
    start_dir = start if start.is_dir() else start.parent
    corrected = _git_common_repo_root(start_dir)
    if corrected is None:
        return resolved
    return corrected


def _git_common_repo_root(start_dir: Path) -> Path | None:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--path-format=absolute", "--git-common-dir"],
            cwd=start_dir,
            text=True,
            capture_output=True,
            check=False,
        )
    except OSError:
        return None
    if result.returncode != 0:
        return None
    common_dir = result.stdout.strip()
    if not common_dir:
        return None
    common_path = Path(common_dir)
    if not common_path.is_absolute():
        common_path = (start_dir / common_path).resolve()
    if common_path.name != ".git":
        return start_dir.resolve()
    return common_path.parent.resolve()
