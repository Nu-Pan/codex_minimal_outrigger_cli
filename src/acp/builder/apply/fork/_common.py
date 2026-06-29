"""apply fork ACP builder の共有補助。"""

import sys
from typing import Any
from pathlib import Path

from basic.acp import (
    AgentCallParameter,
    FileAccessMode,
    ModelClass,
    ReasoningEffort,
)

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


def adapt_oracle_parameter(
    parameter: Any,
    structured_output_schema_path: Path | None,
) -> AgentCallParameter:
    # `<work-root>/oracle/doc/app_spec/prompt_standard.md` requires prompts to
    # come from oracle ACP builders; this adapter only maps oracle enum classes
    # and schema paths into the runtime package used by realization code.
    return AgentCallParameter(
        ModelClass(parameter.model_class.value),
        ReasoningEffort(parameter.reasoning_effort.value),
        FileAccessMode(parameter.file_access_mode.value),
        parameter.prompt,
        structured_output_schema_path,
    )
