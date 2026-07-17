"""apply fork ACP builder の共有補助。"""

import importlib.util
import sys
from pathlib import Path

from basic.acp import AgentCallParameter
from basic.path_model import RootPathPlaceHolder, resolve_real_path


def resolve_repo_root() -> Path:
    """apply fork builder が oracle 委譲前に使う repo root を解決する。"""
    return resolve_real_path(RootPathPlaceHolder.REPO)


def ensure_oracle_src_importable(repo_root: Path) -> None:
    """packaged layout と開発 tree layout の両方で oracle builder を import 可能にする。"""
    # `{{work-root}}/oracle/src/oracle/acp_builder/apply/fork/*.py` は `oracle.*` として
    # package 化される。installed layout では `oracle/src` が残るとは限らない。
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
    """oracle 側が返した ACP parameter を realization 側公開型として受け渡す。"""
    # `{{work-root}}/oracle/src/oracle/acp_builder/basic.py` が runtime ACP type を所有する。
    # `basic.acp` は copy を保持せず、同じ class を再公開する。
    return parameter
