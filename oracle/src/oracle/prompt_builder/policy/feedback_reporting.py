# cmoc
from oracle.other.path_model import AgentCallPathContext
from oracle.other.struct_doc import SDHeader, SDPolicy
from oracle.prompt_builder.basic import PlaceholderMap


def build_feedback_reporting_policy(
    path_context: AgentCallPathContext,
) -> tuple[PlaceholderMap, SDHeader]:
    """全 agent call に共通する人間向け feedback の報告規定を構築する。

    NOTE
        関連仕様は `{{cmoc-root}}/oracle/doc/app_spec/feedback_observation.md` にある。
    """
    return (
        {},
        SDHeader(
            "human feedback reporting",
            SDPolicy(
                what_is_this="このセッション内でエージェントに課された規定の範囲内では解決できない問題を人間に報告する方法を以下に示す",
                require=(
                    "MCP tool `cmoc_feedback.submit_observation` を使用して問題を報告すること",
                ),
                prohibit=(
                    "問題報告の成功・失敗を根拠にセッションを中断・続行を判断してはならない",
                    "セッション内で解決した問題は報告してはならない",
                    "仕様どおりの制約は報告してはいけない",
                    "具体的な根拠がない改善案は報告してはいけない",
                ),
            ),
        ),
    )
