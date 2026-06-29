"""apply fork ACP builder の共有補助。"""

import importlib.util
import sys
from pathlib import Path

from basic.acp import AgentCallParameter
from basic.path_model import RootPathPlaceHolder, resolve_real_path


def resolve_repo_root() -> Path:
    return resolve_real_path(RootPathPlaceHolder.REPO)


def ensure_oracle_src_importable(repo_root: Path) -> None:
    # `<work-root>/oracle/src/oracle/acp_builder/apply/fork/*.py` are packaged
    # as `oracle.*`; installed layouts do not necessarily retain `oracle/src`.
    try:
        if importlib.util.find_spec("oracle.acp_builder") is not None:
            return
    except ModuleNotFoundError:
        pass

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


def adapt_oracle_parameter(parameter: AgentCallParameter) -> AgentCallParameter:
    # `<work-root>/oracle/src/oracle/acp_builder/basic.py` owns the runtime ACP
    # type; `basic.acp` re-exports that same class instead of keeping a copy.
    return parameter
