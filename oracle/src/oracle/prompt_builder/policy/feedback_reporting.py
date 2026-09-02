"""全 agent call に共通する feedback observation 報告規定文面の構築定義。"""

# cmoc
from oracle.other.path_model import AgentCallPathContext
from oracle.other.struct_doc import SDHeader, SDPolicy
from oracle.prompt_builder.basic import PlaceholderMap


def build_feedback_reporting_policy(
    path_context: AgentCallPathContext,
) -> tuple[PlaceholderMap, SDHeader]:
    """全 agent call に共通する feedback observation の報告規定を構築する。

    NOTE
        意味仕様は `oracle/doc/app_spec/feedback_observation.md` の
        「報告基準」を参照。
    """
    return (
        {},
        SDHeader(
            "feedback observation reporting",
            SDPolicy(
                what_is_this=(
                    "現在の workload の規定範囲内では解消できず、後続の "
                    "automatic remediation または人間対応の候補となる、具体的な"
                    "根拠のある問題を収集する方法を以下に示す"
                ),
                require=(
                    "MCP tool `cmoc_feedback.submit_observation` を使用して問題を報告すること",
                ),
                prohibit=(
                    "問題報告の成功・失敗を根拠にセッションを中断・続行を判断してはならない",
                    "現在の workload 内で解決した問題は報告してはならない",
                    "仕様どおりの制約は報告してはいけない",
                    "具体的な根拠がない改善案は報告してはいけない",
                ),
            ),
        ),
    )
