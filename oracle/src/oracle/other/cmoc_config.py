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
                model="gpt-6-astra",
                reasoning_effort="high",
            ),
            "build_feedback_remediate_issue_parameter": CodexCallConfig(
                model_provider="openai",
                model="gpt-5.6-luna",
                reasoning_effort="max",
            ),
            # NOTE
            #   oracle file に影響を与えるので astra を使う
            #   TUI で人間とターンを回すので astra を使う
            "build_oracle_investigation_launch_tui_parameter": CodexCallConfig(
                model_provider="openai",
                model="gpt-6-astra",
                reasoning_effort="high",
            ),
            # NOTE oracle file に影響を与えるので astra を使う
            "build_oracle_edit_main_launch_exec_parameter": CodexCallConfig(
                model_provider="openai",
                model="gpt-6-astra",
                reasoning_effort="high",
            ),
            # NOTE oracle file に影響を与えるので astra を使う
            "build_oracle_edit_reduction_launch_exec_parameter": CodexCallConfig(
                model_provider="openai",
                model="gpt-6-astra",
                reasoning_effort="high",
            ),
            # oracle --> realization のメインルート
            # NOTE
            #   大規模な修正になる可能性に備えて ultra にしたら、一生収束しない大事故が発生
            #   安定している max に戻した
            # NOTE
            #   realization file は GPT-5.6 で問題を感じていない
            #   astra は使わない
            "build_realization_apply_fork_launch_exec_parameter": CodexCallConfig(
                model_provider="openai",
                model="gpt-5-astra",
                reasoning_effort="medium",
            ),
            "build_feedback_normalize_issue_parameter": CodexCallConfig(
                model_provider="openai",
                model="gpt-5.6-sol",
                reasoning_effort="max",
            ),
            # NOTE TUI で人間とターンを回すので astra を使う
            "build_tui_launch_tui_parameter": CodexCallConfig(
                model_provider="openai",
                model="gpt-6-astra",
                reasoning_effort="high",
            ),
            # NOTE
            #   ファイル単位処理なので呼び出し回数が非常に多く、その分コストが掛かる
            #   よって、コスパに優れる Luna しか選べない
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
            # NOTE 呼び出し回数が多い単純な要約タスクなので、Luna しか選べない。
            "build_indexing_index_entry_parameter": CodexCallConfig(
                model_provider="openai",
                model="gpt-5.6-luna",
                reasoning_effort="low",
            ),
            # NOTE 終了結果だけを使う probe なので、一番安いモデルで良い。
            "build_quota_availability_probe_parameter": CodexCallConfig(
                model_provider="openai",
                model="gpt-5.6-luna",
                reasoning_effort="low",
            ),
        }
    )

    # ファイルアクセス規定違反時のリカバリ試行回数
    num_try_falv_recovery: int = field(default=1)
