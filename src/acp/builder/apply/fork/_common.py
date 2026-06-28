"""apply fork ACP builder の共有補助。"""

import sys
import subprocess
from pathlib import Path


def resolve_repo_root() -> Path:
    """現在位置または git から `<repo-root>` を解決する。"""
    for candidate in (Path.cwd(), *Path.cwd().parents):
        if (candidate / ".git").is_dir():
            return candidate
    git_result = subprocess.run(
        ["git", "rev-parse", "--path-format=absolute", "--git-common-dir"],
        text=True,
        capture_output=True,
    )
    if git_result.returncode == 0 and git_result.stdout.strip():
        return Path(git_result.stdout.strip()).parent
    raise ValueError("`<repo-root>` was not found")


def ensure_oracle_src_importable(repo_root: Path) -> None:
    candidates = [
        repo_root / "oracle" / "src",
        Path(__file__).resolve().parents[5] / "oracle" / "src",
    ]
    for candidate in candidates:
        if (candidate / "oracle").is_dir():
            candidate_text = str(candidate)
            if candidate_text not in sys.path:
                sys.path.insert(0, candidate_text)
            return
    raise ValueError("`oracle/src` was not found")
