# cmoc
from oracle.other.path_model import AgentCallPathContext
from oracle.other.struct_doc import StructDoc
from oracle.prompt_builder.basic import PlaceholderMap


def build_feedback_reporting_policy(
    path_context: AgentCallPathContext,
) -> tuple[PlaceholderMap, StructDoc]:
    """全 agent call に共通する人間向け feedback の報告規定を構築する。"""
    return (
        {},
        StructDoc(
            "human feedback reporting",
            """
            - 現在の workload だけでは解消できず、現在の作業外にいる人間の対応によって、再発防止、反復的な浪費の削減、または外部挙動を左右する人間意図の確定が可能な問題だけを報告する
            - 通常の workload 内で解決した問題、仕様どおりの制約、および具体的な根拠がない改善案は報告しない
            - 報告対象を発見した時点で MCP tool `cmoc_feedback.submit_observation` を使用する。feedback 保存 file は直接編集しない
            - 報告後も可能なら本命 workload を継続する。tool が利用不能な場合または報告が拒否された場合も、本命 workload を継続する
            - 報告対象がない場合は、feedback 用の出力または tool call を行わない
            """,
        ),
    )
