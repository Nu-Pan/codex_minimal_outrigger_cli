"""
# cmoc config

- cmoc の挙動設定のうち、開発対象リポジトリごとに変わりうる事柄は `CmocConfig` に集約する
- `CmocConfig` は `{{work-root}}/.cmoc/gt/config.json` として永続化される
- `CmocConfig` を json にシリアライズする際、メンバーの順序は保持される
- 検索 tuning の意味仕様は、`{{cmoc-root}}/oracle/doc/app_spec/document_search.md` の
  「設定と未確定事項」に従う
- 設定の生成・検索設定の補完・保存済み設定の検証は、
  `{{cmoc-root}}/oracle/doc/app_spec/doctor_preprocess.md` の
  「検索設定の検証と補完」に従う（旧 `document_search: null` 入力の扱いを含む）
- `{{work-root}}/.cmoc/gt/config.json` は人間によって編集・調整される
"""

# std
from dataclasses import dataclass, field

# JSON と TOML の両方で表現できる設定値
type JsonTomlValue = (
    str | int | float | bool | list[JsonTomlValue] | dict[str, JsonTomlValue]
)


@dataclass(frozen=True)
class DocumentSearchConfig:
    """検索 tuning の型・制約と、生成・補完に使う暫定既定値。

    NOTE
        int の項目は JSON 整数、float の項目は有限の JSON 数値とする。
        bool を数値として受理しない。chunk_overlap_tokens 以外は正数、
        chunk_overlap_tokens は 0 以上 chunk_tokens 未満。
        candidate_count は `{{cmoc-root}}/oracle/src/oracle/other/document_search.py` の
        SEARCH_CANDIDATE_COUNT_MIN 以上 SEARCH_CANDIDATE_COUNT_MAX 以下。
        chunk_tokens は embedding_context_tokens より小さくし、
        本文以外の入力の余地を残す。この大小関係だけで入力全体の収容を保証せず、
        文書・query それぞれに入力整形・特殊 token を加えた実入力が
        embedding tokenizer の context 上限内に収まることも検証する。
    """

    chunk_tokens: int = 512
    chunk_overlap_tokens: int = 64
    candidate_count: int = 50
    embedding_context_tokens: int = 2048
    batch_tokens: int = 512
    threads: int = 4
    startup_timeout_seconds: float = 120.0
    request_timeout_seconds: float = 600.0
    shutdown_grace_seconds: float = 5.0
    resource_wait_timeout_seconds: float = 600.0
    sync_no_progress_timeout_seconds: float = 600.0
    post_sync_search_timeout_seconds: float = 600.0
    search_request_timeout_seconds: float = 3600.0


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

    # 新規生成用の既定状態。保存済み入力の検証規則はモジュール docstring の参照先に従う。
    document_search: DocumentSearchConfig = field(default_factory=DocumentSearchConfig)


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
    #   なので、GPT-5.6 Astra xhigh にして料金をケチりたい所だった。
    #   現実には xhigh だと取りこぼしがきになるので max で運用している。
    agent_calls: dict[str, CodexCallConfig] = field(
        default_factory=lambda: {
            # NOTE
            #   ここでミスるとブランチ上の作業結果がぶち壊しになる
            #   リスクを鑑みて、品質が至上命題
            "build_session_join_conflict_resolution_parameter": CodexCallConfig(
                model_provider="openai",
                model="gpt-6-astra",
                reasoning_effort="max",
            ),
            "build_run_join_conflict_resolution_parameter": CodexCallConfig(
                model_provider="openai",
                model="gpt-6-astra",
                reasoning_effort="max",
            ),
            # NOTE
            #   oracle file に影響を与えるので品質が至上命題
            #   TUI で人間とターンを回すので品質が至上命題
            "build_oracle_investigation_launch_tui_parameter": CodexCallConfig(
                model_provider="openai",
                model="gpt-6-astra",
                reasoning_effort="max",
            ),
            # NOTE oracle file に影響を与えるので品質が至上命題
            "build_oracle_edit_main_launch_exec_parameter": CodexCallConfig(
                model_provider="openai",
                model="gpt-6-astra",
                reasoning_effort="max",
            ),
            # oracle --> realization のメインルート
            # NOTE
            #   大規模な修正になる可能性に備えて ultra にしたら、一生収束しない大事故が発生した
            #   GPT の事故調査報告によれば、修正が別の修正を呼ぶループに入ったっぽい
            #   元々存在する実装や修正のプランの筋が良くなくて、AIがメンテ出来る汚さの限界付近に居るのかも
            #   あるいは、サブエージェントどうしてコンディションレースしたか
            # NOTE
            #   実装タスクはテストによる機械的検証が可能だが、機械的検証は「今回の実装が将来に禍根を残す可能性」までは見てくれない
            #   品質はあまり犠牲に出来ない
            #   gpt-6.1-sol で様子を見る
            "build_realization_apply_fork_launch_exec_parameter": CodexCallConfig(
                model_provider="openai",
                model="gpt-6.1-sol",
                reasoning_effort="max",
            ),
            # NOTE
            #   報告１つ毎に呼ぶ関係でコストが嵩みやすい
            #   調査結果の正しさを機械的検証出来ないので、調査の網羅性は大事
            #   意外と難しいタスクっぽいので、一度 astra で様子見
            #   状況を見てもうちょっと安いモデルに下げたい
            "build_feedback_remediate_issue_parameter": CodexCallConfig(
                model_provider="openai",
                model="gpt-6.1-sol",
                reasoning_effort="max",
            ),
            # NOTE
            #   feedback report の整理作業が反復的かつ機械的検証不能なので、モデルがアホだと暴走しやすい
            #   怖すぎるので Astra しか選べない
            "build_feedback_normalize_issue_parameter": CodexCallConfig(
                model_provider="openai",
                model="gpt-6.1-sol",
                reasoning_effort="max",
            ),
            # NOTE TUI で人間とターンを回すので品質が至上命題
            "build_tui_launch_tui_parameter": CodexCallConfig(
                model_provider="openai",
                model="gpt-6-astra",
                reasoning_effort="max",
            ),
            # NOTE
            #   ファイル単位処理なので呼び出し回数が非常に多く、その分コストが掛かる
            #   仕様適合と検出能力を保つ改善の判断には品質も必要なので、バランスの良い gpt-6.1-sol を選ぶ
            "build_realization_refactor_fork_file_review_and_fix_parameter": CodexCallConfig(
                model_provider="openai",
                model="gpt-6.1-sol",
                reasoning_effort="max",
            ),
            # NOTE 終了結果だけを使う probe なので、一番安いモデルなら何でも良い
            "build_quota_availability_probe_parameter": CodexCallConfig(
                model_provider="openai",
                model="gpt-6-luna",
                reasoning_effort="low",
            ),
        }
    )

    # ファイルアクセス規定違反時のリカバリ試行回数
    num_try_falv_recovery: int = field(default=1)
