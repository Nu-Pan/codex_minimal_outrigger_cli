"""
# cmoc config

- cmoc の挙動設定のうち、開発対象リポジトリごとに変わりうる事柄は `CmocConfig` に集約する
- `CmocConfig` は `{{work-root}}/.cmoc/gt/ar/config.json` として永続化される
- `CmocConfig` を json にシリアライズする際、メンバーの順序は保持される
- Enum 系を継承したクラスのインスタンスは value 化して json に保存する
    - e.g. `ModelClass.MAINSTREAM` --> `mainstream`
- `{{work-root}}/.cmoc/gt/ar/config.json` は `cmoc doctor` によって生成・同期される
- `{{work-root}}/.cmoc/gt/ar/config.json` は人間によって編集・調整される
"""

# std
from dataclasses import dataclass, field

# cmoc
from oracle.acp_builder.basic import ModelClass, ReasoningEffort

# JSON と TOML の両方で表現できる設定値
type JsonTomlValue = (
    str | int | float | bool | list[JsonTomlValue] | dict[str, JsonTomlValue]
)


@dataclass(frozen=True)
class CodexModelProviderConfig:
    """単一 model provider の provider-local Codex config。"""

    # provider-local key --> JSON/TOML 共通の設定値
    settings: dict[str, JsonTomlValue] = field(default_factory=dict)


@dataclass(frozen=True)
class CmocConfig:
    """
    cmoc の設定 (config) を集約したクラス
    """

    # AI エージェント呼び出しの最大並列数
    num_parallel: int = field(default=8)

    # Codex CLI 関係の設定
    codex: "CmocConfigCodex" = field(default_factory=lambda: CmocConfigCodex())

    # `cmoc oracle review` サブコマンドの挙動設定
    oracle_review: "CmocConfigOracleReview" = field(
        default_factory=lambda: CmocConfigOracleReview()
    )


@dataclass(frozen=True)
class CodexModelSpec:
    """Codex CLI 上のモデル指定"""

    # model provider ID。None の場合は Codex CLI の既定値を使う
    model_provider: str | None

    # モデル名
    model: str


@dataclass(frozen=True)
class CmocConfigCodex:
    """
    cmoc の設定 (config) のうち Codex CLI 向けの設定を集約したクラス
    """

    # model provider ID --> provider-local な Codex config
    model_providers: dict[str, CodexModelProviderConfig] = field(default_factory=dict)

    # `ModelClass` --> Codex CLI が受理可能な Model 名
    # NOTE
    #   モデル名の未定義は禁止
    #   モデル名は case sensitive なので注意
    model: dict[ModelClass, CodexModelSpec] = field(
        default_factory=lambda: {
            ModelClass.MAINSTREAM: CodexModelSpec(None, "gpt-5.6-terra"),
            ModelClass.FLAGSHIP: CodexModelSpec(None, "gpt-5.6-sol"),
            ModelClass.EFFICIENCY: CodexModelSpec(None, "gpt-5.6-luna"),
            ModelClass.MINIMUM: CodexModelSpec(None, "gpt-5.4-mini"),
        }
    )

    # `ReasoningEffort` --> Codex CLI が受理可能な Reasoning Effort 名
    reasoning_effort: dict[ReasoningEffort, str] = field(
        default_factory=lambda: {
            ReasoningEffort.LOW: "low",
            ReasoningEffort.MEDIUM: "medium",
            ReasoningEffort.HIGH: "high",
            ReasoningEffort.XHIGH: "xhigh",
            ReasoningEffort.MAX: "max",
        }
    )

    # ファイルアクセス規則違反時のリカバリ試行回数
    num_try_falv_recovery: int = field(default=1)


@dataclass(frozen=True)
class CmocConfigOracleReview:
    """
    `cmoc oracle review` サブコマンドの挙動に関する設定を集約したクラス
    """

    # 所見リスト列挙ループの上限回数
    num_enumerate_findings_loop: int = field(default=2)

    # 所見リストマージループの上限回数
    num_merge_findings_loop: int = field(default=2)

    # 所見リスト検証ループの上限回数
    # NOTE
    #   検証ループは収束性が無く、無限に理由を追記し続ける傾向がある（これは現在の仕様上しょうがない）
    #   よってこのループ回数は「judge 前に advocate/challenger にどれだけ議論させるかの予算」という意味合いを持つ。
    #   生成される理由の妥当性もわからないので、１度だけ反論の機会を与えるという意味でループ数 2 としている。
    num_validate_findings_loop: int = field(default=2)
