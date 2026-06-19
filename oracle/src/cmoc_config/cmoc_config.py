"""
# cmoc config

- cmoc の設定は `CmocConfig` に集約する
- `CmocConfig` は `<cmoc-root>/.cmoc/config.json` として永続化される
- Enum 系を継承したクラスのインスタンスは value 化して json に保存する
    - e.g. `ModelClass.MAINSTREAM` --> `mainstream`
"""

# std
from dataclasses import dataclass

# cmoc
from agent_call_parameter.base import BackendType, ModelClass, ReasoningEffort


@dataclass(frozen=True)
class CmocConfig:
    """
    cmoc の設定 (config) を集約したクラス
    """

    # 使用するバックエンドの種類
    backend: BackendType

    # Codex CLI 用の設定
    codex: "CmocConfigCodex"


@dataclass(frozen=True)
class CmocConfigCodex:
    """
    cmoc の設定 (config) のうち Codex CLI 向けの設定を集約したクラス
    """

    # `ModelClass` --> Codex CLI が受理可能な Model 名
    model: dict[ModelClass, str]

    # `ReasoningEffort` --> Codex CLI が受理可能な Reasoning Effort 名
    reasoning_effort: dict[ReasoningEffort, str]
