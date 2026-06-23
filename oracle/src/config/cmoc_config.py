"""
# cmoc config

- cmoc の挙動設定のうち、開発対象リポジトリごとに変わりうる事柄は `CmocConfig` に集約する
- `CmocConfig` は `<repo-root>/.cmoc/config.json` として永続化される
- Enum 系を継承したクラスのインスタンスは value 化して json に保存する
    - e.g. `ModelClass.MAINSTREAM` --> `mainstream`
- `<repo-root>/.cmoc/config.json` は `cmoc init` によって生成・同期される
- `<repo-root>/.cmoc/config.json` は人間によって編集・調整される
"""

# std
from dataclasses import dataclass, field

# cmoc
from basic.acp import ModelClass, ReasoningEffort


@dataclass(frozen=True)
class CmocConfig:
    """
    cmoc の設定 (config) を集約したクラス
    """

    # AI エージェント呼び出しの最大並列数
    num_parallel: int = field(default=8)

    # Codex CLI 用の設定
    codex: "CmocConfigCodex" = field(default_factory=lambda: CmocConfigCodex())

    # `cmoc apply fork` サブコマンドの挙動設定
    apply_fork: "CmocConfigApplyFork" = field(
        default_factory=lambda: CmocConfigApplyFork()
    )

    # `cmoc review oracle` サブコマンドの挙動設定
    review_oracle: "CmocConfigReviewOracle" = field(
        default_factory=lambda: CmocConfigReviewOracle()
    )


@dataclass(frozen=True)
class CmocConfigApplyFork:
    """
    `cmoc apply fork` サブコマンドの挙動に関する設定を集約したクラス
    """

    # apply ループの最大反復回数
    num_apply_loop: int = field(default=5)

    # 所見リスト改善ループの最大回数
    num_improve_findings_loop: int = field(default=1)


@dataclass(frozen=True)
class CmocConfigReviewOracle:
    """
    `cmoc review oracle` サブコマンドの挙動に関する設定を集約したクラス
    """

    # 所見リスト列挙ループの上限回数
    num_enumerate_findings_loop: int = field(default=3)

    # 所見リストマージループの上限回数
    num_merge_findings_loop: int = field(default=3)

    # 所見リスト検証ループの上限回数
    num_validate_findings_loop: int = field(default=3)


@dataclass(frozen=True)
class CmocConfigCodex:
    """
    cmoc の設定 (config) のうち Codex CLI 向けの設定を集約したクラス
    """

    # `ModelClass` --> Codex CLI が受理可能な Model 名
    model: dict[ModelClass, str] = field(
        default_factory=lambda: {
            ModelClass.MAINSTREAM: "GPT-5.5",
            ModelClass.FLAGSHIP: "GPT-5.5",
            ModelClass.EFFICIENCY: "GPT-5.4-mini",
            ModelClass.MINIMUM: "GPT-5.4-mini",
        }
    )

    # `ReasoningEffort` --> Codex CLI が受理可能な Reasoning Effort 名
    reasoning_effort: dict[ReasoningEffort, str] = field(
        default_factory=lambda: {
            ReasoningEffort.LOW: "low",
            ReasoningEffort.MEDIUM: "medium",
            ReasoningEffort.HIGH: "high",
        }
    )
