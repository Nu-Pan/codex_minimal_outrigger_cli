from pathlib import Path

from basic.path_model import resolve_real_path
from commons.runtime_paths import pushd


def finding_oracle_path(finding: dict, worktree: Path) -> Path | None:
    raw_path = finding.get("oracle_path")
    if not isinstance(raw_path, str) or not raw_path:
        return None
    path = Path(raw_path)
    if path.is_absolute():
        return path.resolve()
    if path.parts and path.parts[0] == "<oracle-root>":
        # enumerate_finding prompt exposes this shorthand as an oracle root alias.
        # 根拠: <work-root>/oracle/src/oracle/acp_builder/review/oracle/enumerate_finding.py
        return (worktree / "oracle" / Path(*path.parts[1:])).resolve()
    if path.parts and path.parts[0].startswith("<"):
        try:
            # <work-root>/oracle/src/oracle/other/path_model.py
            # review oracle の finding は隔離 worktree 上の path として照合する。
            with pushd(worktree):
                return resolve_real_path(path)
        except (TypeError, ValueError):
            return None
    return None
