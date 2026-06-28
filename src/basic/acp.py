"""ACP の実行時共有型。

`<work-root>/oracle/src/oracle/acp_builder/basic.py` が正本。通常起動時の
import path は `src` のみなので、実行時に使う型は realization 側にも置く。
"""

from dataclasses import dataclass
from enum import StrEnum, auto
from pathlib import Path


class ModelClass(StrEnum):
    MAINSTREAM = auto()
    FLAGSHIP = auto()
    EFFICIENCY = auto()
    MINIMUM = auto()


class ReasoningEffort(StrEnum):
    LOW = auto()
    MEDIUM = auto()
    HIGH = auto()


class FileAccessMode(StrEnum):
    READONLY = auto()
    PURE_ORACLE_READ = auto()
    REALIZATION_WRITE = auto()
    ORACLE_WRITE = auto()
    REPO_WRITE = auto()


@dataclass(frozen=True)
class AgentCallParameter:
    model_class: ModelClass
    reasoning_effort: ReasoningEffort
    file_access_mode: FileAccessMode
    prompt: str
    structured_output_schema_path: Path | None
