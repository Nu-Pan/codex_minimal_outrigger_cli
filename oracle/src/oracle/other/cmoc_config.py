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
from typing import Literal

# cmoc
from oracle.acp_builder.basic import ModelClass, ReasoningEffort


@dataclass(frozen=True)
class CmocConfig:
    """
    cmoc の設定 (config) を集約したクラス
    """

    # AI エージェント呼び出しの最大並列数
    num_parallel: int = field(default=8)

    # Codex CLI 関係の設定
    codex: "CmocConfigCodex" = field(default_factory=lambda: CmocConfigCodex())

    # cmoc managed ollama 起動の挙動
    # default:
    #   エンドユーザー環境で使用する通常モード。
    #   `CodexModelSpec.model_provider=="cmoc"` が存在する場合のみ、cmoc managed ollama service の起動保証を実行する。
    # bypass:
    #   「cmoc を用いた cmoc の自己開発」シナリオで使用する開発用モード。
    #   cmoc managed ollama service の起動保証処理をバイパスする。
    #   サンドボックス環境内からでは `~/.cmoc/ollama` を触れない (cmoc managed ollama service を起動できない) ので、それをバイパスするために使う。
    # force:
    #   「cmoc を用いた cmoc の自己開発」シナリオで使用する開発用モード。
    #   cmoc managed ollama service の起動保証を必ず実行する。
    #   サンドボックス環境内からでは cmoc managed ollama service を起動できないため、サンドボックス外で強制起動するために使う。
    cmoc_managed_ollama_service_launch_behavior: Literal[
        "default", "bypass", "force"
    ] = field(default="default")

    # `cmoc oracle review` サブコマンドの挙動設定
    oracle_review: "CmocConfigOracleReview" = field(
        default_factory=lambda: CmocConfigOracleReview()
    )


@dataclass(frozen=True)
class CodexModelSpec:
    """Codex CLI 上のモデル指定"""

    # model provider 設定
    # codex:
    #   Codex CLI 標準のモデル設定を使う
    #   いわば未指定 (default)
    # cmoc:
    #   cmoc managed ollama を使う
    model_provider: Literal["codex", "cmoc"]

    # モデル名
    model: str


@dataclass(frozen=True)
class CmocConfigCodex:
    """
    cmoc の設定 (config) のうち Codex CLI 向けの設定を集約したクラス
    """

    # `ModelClass` --> Codex CLI が受理可能な Model 名
    # NOTE
    #   モデル名の未定義は禁止
    #   モデル名は case sensitive なので注意
    model: dict[ModelClass, CodexModelSpec] = field(
        default_factory=lambda: {
            ModelClass.MAINSTREAM: CodexModelSpec("codex", "gpt-5.6-terra"),
            ModelClass.FLAGSHIP: CodexModelSpec("codex", "gpt-5.6-sol"),
            ModelClass.EFFICIENCY: CodexModelSpec("codex", "gpt-5.6-luna"),
            ModelClass.MINIMUM: CodexModelSpec("codex", "gpt-5.4-mini"),
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
