"""
# cmoc config

- cmoc の挙動設定のうち、開発対象リポジトリごとに変わりうる事柄は `CmocConfig` に集約する
- `CmocConfig` は `{{work-root}}/.cmoc/gt/ar/config.json` として永続化される
- `CmocConfig` を json にシリアライズする際、メンバーの順序は保持される
- `{{work-root}}/.cmoc/gt/ar/config.json` は `cmoc doctor` によって生成・同期される
- `{{work-root}}/.cmoc/gt/ar/config.json` は人間によって編集・調整される
"""

# std
from dataclasses import dataclass, field

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
class CodexCallConfig:
    """一つの agent call 種別から各 Codex call へ直接渡す設定。"""

    # model provider ID
    model_provider: str

    # Model 名
    model: str

    # Reasoning Effort 名
    reasoning_effort: str


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
class CmocConfigCodex:
    """
    cmoc の設定 (config) のうち Codex CLI 向けの設定を集約したクラス
    """

    # model provider ID --> provider-local な Codex config
    model_providers: dict[str, CodexModelProviderConfig] = field(
        default_factory=lambda: {"openai": CodexModelProviderConfig()}
    )

    # `AgentCallParameter.agent_call_kind` --> Codex CLI へ直接渡す設定
    agent_calls: dict[str, CodexCallConfig] = field(
        default_factory=lambda: {
            # NOTE merge 結果を守るため、既定設定の中で最も品質を優先する。
            "build_session_join_conflict_resolution_parameter": CodexCallConfig(
                model_provider="openai",
                model="gpt-5.6-sol",
                reasoning_effort="max",
            ),
            "build_feedback_verify_issue_parameter": CodexCallConfig(
                model_provider="openai",
                model="gpt-5.6-sol",
                reasoning_effort="max",
            ),
            # NOTE TUI 起動系なので性能最優先で ultra
            "build_oracle_investigation_launch_tui_parameter": CodexCallConfig(
                model_provider="openai",
                model="gpt-5.6-sol",
                reasoning_effort="ultra",
            ),
            "build_oracle_edit_main_launch_exec_parameter": CodexCallConfig(
                model_provider="openai",
                model="gpt-5.6-sol",
                reasoning_effort="max",
            ),
            "build_oracle_edit_reduction_launch_exec_parameter": CodexCallConfig(
                model_provider="openai",
                model="gpt-5.6-sol",
                reasoning_effort="max",
            ),
            # NOTE
            #   oracle --> realization のメインルート
            #   大規模な修正になる可能性に備えて ultra
            "build_realization_apply_fork_launch_exec_parameter": CodexCallConfig(
                model_provider="openai",
                model="gpt-5.6-sol",
                reasoning_effort="ultra",
            ),
            "build_feedback_normalize_issue_parameter": CodexCallConfig(
                model_provider="openai",
                model="gpt-5.6-sol",
                reasoning_effort="max",
            ),
            # NOTE TUI 起動系なので性能最優先で ultra
            "build_tui_launch_tui_parameter": CodexCallConfig(
                model_provider="openai",
                model="gpt-5.6-sol",
                reasoning_effort="ultra",
            ),
            "build_oracle_review_enumerate_finding_parameter": CodexCallConfig(
                model_provider="openai",
                model="gpt-5.6-luna",
                reasoning_effort="max",
            ),
            "build_oracle_review_merge_finding_parameter": CodexCallConfig(
                model_provider="openai",
                model="gpt-5.6-luna",
                reasoning_effort="max",
            ),
            "build_oracle_review_validate_finding_advocate_parameter": CodexCallConfig(
                model_provider="openai",
                model="gpt-5.6-luna",
                reasoning_effort="max",
            ),
            "build_oracle_review_validate_finding_challenger_parameter": CodexCallConfig(
                model_provider="openai",
                model="gpt-5.6-luna",
                reasoning_effort="max",
            ),
            "build_oracle_review_judge_finding_parameter": CodexCallConfig(
                model_provider="openai",
                model="gpt-5.6-luna",
                reasoning_effort="max",
            ),
            "build_realization_refactor_fork_file_review_and_fix_parameter": CodexCallConfig(
                model_provider="openai",
                model="gpt-5.6-luna",
                reasoning_effort="max",
            ),
            "build_realization_refactor_fork_change_summary_parameter": CodexCallConfig(
                model_provider="openai",
                model="gpt-5.6-luna",
                reasoning_effort="medium",
            ),
            # NOTE 呼び出し回数が多い単純な要約タスクなので、quota 消費を抑える。
            "build_indexing_index_entry_parameter": CodexCallConfig(
                model_provider="openai",
                model="gpt-5.6-luna",
                reasoning_effort="low",
            ),
            # NOTE 終了結果だけを使う probe なので、quota 消費を抑える。
            "build_quota_availability_probe_parameter": CodexCallConfig(
                model_provider="openai",
                model="gpt-5.6-luna",
                reasoning_effort="low",
            ),
        }
    )

    # ファイルアクセス規定違反時のリカバリ試行回数
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
