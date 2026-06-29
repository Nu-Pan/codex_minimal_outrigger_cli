"""apply fork ACP builder の共有補助。"""

import sys
from pathlib import Path

# `<work-root>/oracle/src/oracle/other/path_model.py` owns repo-root
# resolution; this module keeps the existing apply builder import boundary.
from basic.path_model import resolve_repo_root as resolve_repo_root


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
