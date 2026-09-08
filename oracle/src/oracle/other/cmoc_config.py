"""
# cmoc config

- cmoc の挙動設定のうち、開発対象リポジトリごとに変わりうる事柄は `CmocConfig` に集約する
- `CmocConfig` は `{{work-root}}/.cmoc/gt/config.json` として永続化される
- `CmocConfig` を json にシリアライズする際、メンバーの順序は保持される
- `{{work-root}}/.cmoc/gt/config.json` は `cmoc doctor` によって生成・同期される
- `{{work-root}}/.cmoc/gt/config.json` は人間によって編集・調整される
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
    # NOTE
    #   ベンチマークスコア上、GPT-5.6 Astra は xhigh, max に知能差はほとんど無いが、料金差はきっちりある
    #   個別ベンチスコアで見ても、ほとんど横並び
    #   よって、この設定ファイル内の選択基準的には GPT-5.6 Astra xhigh を最高品質とみなす
    #   コスパを重視るすなら high に落としても良い
    agent_calls: dict[str, CodexCallConfig] = field(
        default_factory=lambda: {
            # NOTE merge 結果を守るため、品質が最優先
            "build_session_join_conflict_resolution_parameter": CodexCallConfig(
                model_provider="openai",
                model="gpt-6-astra",
                reasoning_effort="xhigh",
            ),
            # NOTE
            #   oracle file に影響を与えるので品質が重要
            #   TUI で人間とターンを回すので品質・速度が重要
            "build_oracle_investigation_launch_tui_parameter": CodexCallConfig(
                model_provider="openai",
                model="gpt-6-astra",
                reasoning_effort="xhigh",
            ),
            # NOTE oracle file に影響を与えるので品質が重要
            "build_oracle_edit_main_launch_exec_parameter": CodexCallConfig(
                model_provider="openai",
                model="gpt-6-astra",
                reasoning_effort="xhigh",
            ),
            # NOTE oracle file に影響を与えるので品質が重要
            "build_oracle_edit_reduction_launch_exec_parameter": CodexCallConfig(
                model_provider="openai",
                model="gpt-6-astra",
                reasoning_effort="xhigh",
            ),
            # oracle --> realization のメインルート
            # NOTE
            #   大規模な修正になる可能性に備えて ultra にしたら、一生収束しない大事故が発生した
            #   GPT の事故調査報告によれば、修正が別の修正を呼ぶループに入ったっぽい
            #   元々存在する実装や修正のプランの筋が良くなくて、AIがメンテ出来る汚さの限界付近に居るのかも
            #   実装タスクはテストによる機械的検証が可能だが、機械的検証は「今回の実装が将来に禍根を残す可能性」までは見てくれない
            #   よって、結論としては品質が重要
            "build_realization_apply_fork_launch_exec_parameter": CodexCallConfig(
                model_provider="openai",
                model="gpt-6-astra",
                reasoning_effort="xhigh",
            ),
            # NOTE
            #   報告１つ毎に呼ぶ関係でコストが嵩みやすい
            #   調査結果の正しさを機械的検証出来ないので、調査の網羅性は大事
            #   Luna max しか選べない
            "build_feedback_remediate_issue_parameter": CodexCallConfig(
                model_provider="openai",
                model="gpt-5.6-luna",
                reasoning_effort="max",
            ),
            # NOTE
            #   issue の意味論的一致判定は比較的難易度が低いと予想して、まずは Luna で様子を見る
            #   実際の feedback report が冗長気味なら Astra に上げる
            "build_feedback_normalize_issue_parameter": CodexCallConfig(
                model_provider="openai",
                model="gpt-5.6-luna",
                reasoning_effort="max",
            ),
            # NOTE TUI で人間とターンを回すので品質が重要
            "build_tui_launch_tui_parameter": CodexCallConfig(
                model_provider="openai",
                model="gpt-6-astra",
                reasoning_effort="xhigh",
            ),
            # NOTE
            #   ファイル単位処理なので呼び出し回数が非常に多く、その分コストが掛かる
            #   よって、コスパに優れる Luna しか選べない
            "build_realization_refactor_fork_file_review_and_fix_parameter": CodexCallConfig(
                model_provider="openai",
                model="gpt-5.6-luna",
                reasoning_effort="max",
            ),
            # NOTE 単純な要約タスクなので Luna で良い
            "build_realization_refactor_fork_change_summary_parameter": CodexCallConfig(
                model_provider="openai",
                model="gpt-5.6-luna",
                reasoning_effort="medium",
            ),
            # NOTE 呼び出し回数が非常に多い単純な要約タスクなので、Luna しか選べない。
            "build_indexing_index_entry_parameter": CodexCallConfig(
                model_provider="openai",
                model="gpt-5.6-luna",
                reasoning_effort="low",
            ),
            # NOTE 終了結果だけを使う probe なので、一番安いモデルなら何でも良い
            "build_quota_availability_probe_parameter": CodexCallConfig(
                model_provider="openai",
                model="gpt-5.6-luna",
                reasoning_effort="low",
            ),
        }
    )

    # ファイルアクセス規定違反時のリカバリ試行回数
    num_try_falv_recovery: int = field(default=1)
