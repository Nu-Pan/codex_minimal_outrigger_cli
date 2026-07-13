import os
from pathlib import Path

from basic.path_model import resolve_real_path
from commons.runtime_paths import pushd


def finding_oracle_path(finding: dict, worktree: Path) -> Path | None:
    """finding の oracle_path を symlink を追跡しない絶対 path に変換する。

    根拠:
    - <work-root>/oracle/doc/app_spec/sub_command/review_oracle.md
    - <work-root>/oracle/src/oracle/prompt_builder/parts/oracle_and_realization_basic.py
    """
    raw_path = finding.get("oracle_path")
    if not isinstance(raw_path, str) or not raw_path:
        return None
    path = Path(raw_path)
    if path.is_absolute():
        return _absolute_without_symlink(path)
    if path.parts and path.parts[0] == "<oracle-root>":
        # enumerate_finding prompt exposes this shorthand as an oracle root alias.
        # symlink は oracle 配下の repository path として扱う。
        return _absolute_without_symlink(
            worktree / "oracle" / Path(*path.parts[1:])
        )
    if path.parts and path.parts[0].startswith("<"):
        try:
            with pushd(worktree):
                root = resolve_real_path(path.parts[0])
            return _absolute_without_symlink(root / Path(*path.parts[1:]))
        except (TypeError, ValueError):
            return None
    return None


def oracle_path_key(root: Path, path: Path) -> str | None:
    """oracle file を symlink 非追跡の repository-relative key に変換する。

    report の評価対象は isolated worktree 上の path であり、finding は main
    worktree を基準にする場合があるため、root 外の path でも oracle suffix を
    同じ key として扱う。

    根拠:
    - <work-root>/oracle/doc/app_spec/sub_command/review_oracle.md
    - <work-root>/oracle/src/oracle/prompt_builder/parts/oracle_and_realization_basic.py
    """

    candidate = _absolute_without_symlink(path)
    relative = None
    try:
        relative = candidate.relative_to(_absolute_without_symlink(root))
    except ValueError:
        pass
    if relative is None or relative.parts[:1] != ("oracle",):
        relative = None
        for index in range(len(candidate.parts) - 1, -1, -1):
            if candidate.parts[index] == "oracle":
                relative = Path(*candidate.parts[index:])
                break
    if relative is None:
        return None
    return relative.as_posix()


def _absolute_without_symlink(path: Path) -> Path:
    """path を正規化しつつ symlink の link 先を保持する。"""
    return Path(os.path.abspath(path))
