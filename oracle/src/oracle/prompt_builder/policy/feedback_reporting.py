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
                what_is_this="このセッション内では解決出来ない問題に対する規定を以下に示す",
                require=(
                    "MCP tool `cmoc_feedback.submit_observation` を使用して問題を報告すること",
                    "「これは明確に問題である」と断言できるだけの具体的な根拠のある問題だけを報告すること",
                ),
                prohibit=(
                    "問題報告の成功・失敗を根拠にセッションを中断・続行を判断してはならない",
                    "このセッション内で解決可能な問題は報告してはならない",
                    "根拠が曖昧な問題の可能性は報告してはならない",
                    "仕様どおりの制約は問題ではないので報告してはならない",
                ),
                supplemental=(
                    "報告された問題は、セッション外の後続処理で修正の候補となる",
                ),
            ),
        ),
    )
