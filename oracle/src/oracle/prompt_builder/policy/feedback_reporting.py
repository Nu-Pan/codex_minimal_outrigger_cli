# cmoc
from oracle.other.path_model import AgentCallPathContext
from oracle.other.struct_doc import SDHeader
from oracle.prompt_builder.basic import PlaceholderMap


def build_feedback_reporting_policy(
    path_context: AgentCallPathContext,
) -> tuple[PlaceholderMap, SDHeader]:
    """全 agent call に共通する人間向け feedback の報告規定を構築する。"""
    return (
        {},
        SDHeader(
            "human feedback reporting",
            """
            - このセッションの規定内では解決できなかった問題を MCP tool `cmoc_feedback.submit_observation` を使用して報告すること
            - 以下の情報は報告しなくて良い
                - セッション内で解決した問題
                - 仕様どおりの制約
                - 具体的な根拠がない改善案
            - 問題報告の成功・失敗を根拠にセッションを中断・続行を判断してはならない
            """,
        ),
    )
