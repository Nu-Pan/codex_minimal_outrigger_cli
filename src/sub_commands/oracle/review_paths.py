import os
from pathlib import Path

from basic.path_model import RootPathPlaceHolder, resolve_real_path
from commons.runtime_paths import pushd, worktrees_dir


def finding_oracle_path(finding: dict, worktree: Path) -> Path | None:
    """finding の oracle_path を symlink を追跡しない絶対 path に変換する。

    根拠:
    - {{work-root}}/oracle/doc/app_spec/sub_command/oracle_review.md
    - {{work-root}}/oracle/src/oracle/prompt_builder/parts/oracle_and_realization_basic.py
    """
    raw_path = finding.get("oracle_path")
    if not isinstance(raw_path, str) or not raw_path:
        return None
    path = Path(raw_path)
    if path.is_absolute():
        return _absolute_without_symlink(path)
    if path.parts and path.parts[0] == "{{oracle-root}}":
        # enumerate_finding prompt はこの略記を oracle root alias として公開する。
        # symlink は oracle 配下の repository path として扱う。
        return _absolute_without_symlink(worktree / "oracle" / Path(*path.parts[1:]))
    if path.parts:
        try:
            placeholder = RootPathPlaceHolder(path.parts[0])
            with pushd(worktree):
                root = resolve_real_path(placeholder)
            return _absolute_without_symlink(root / Path(*path.parts[1:]))
        except (TypeError, ValueError):
            return None
    return None


def oracle_path_key(root: Path, path: Path) -> str | None:
    """oracle file を symlink 非追跡の repository-relative key に変換する。

    report の評価対象は isolated worktree 上の path であり、finding は main
    worktree を基準にする場合がある。main worktree と cmoc 管理下の isolated
    worktree だけを既知の root として扱い、それ以外の path は無視する。

    根拠:
    - {{work-root}}/oracle/doc/app_spec/sub_command/oracle_review.md
    - {{work-root}}/oracle/src/oracle/prompt_builder/parts/oracle_and_realization_basic.py
    """

    root = _absolute_without_symlink(root)
    candidate = _absolute_without_symlink(path)
    try:
        relative = candidate.relative_to(root)
    except ValueError:
        relative = None
    if relative is None or relative.parts[:1] != ("oracle",):
        try:
            managed_relative = candidate.relative_to(
                _absolute_without_symlink(worktrees_dir(root))
            )
        except ValueError:
            return None
        # review report は worktree 削除後にも path を描画するため、git の
        # worktree 登録ではなく、cmoc が予約する session/run の 2 階層だけを
        # isolated worktree の所属境界として使う。
        if len(managed_relative.parts) < 3:
            return None
        relative = Path(*managed_relative.parts[2:])
    if relative is None or relative.parts[:1] != ("oracle",):
        return None
    return relative.as_posix()


def _absolute_without_symlink(path: Path) -> Path:
    """path を正規化しつつ symlink の link 先を保持する。"""
    return Path(os.path.abspath(path))
