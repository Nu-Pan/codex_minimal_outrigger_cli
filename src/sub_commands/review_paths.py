from pathlib import Path

from basic.path_model import resolve_real_path


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
            return resolve_real_path(path)
        except (TypeError, ValueError):
            return None
    return (worktree / path).resolve()
