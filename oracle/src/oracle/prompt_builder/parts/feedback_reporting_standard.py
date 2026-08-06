# cmoc
from oracle.other.path_model import AgentCallPathContext
from oracle.other.struct_doc import StructDoc
from oracle.prompt_builder.basic import PlaceholderMap


def build_feedback_reporting_standard(
    path_context: AgentCallPathContext,
) -> tuple[PlaceholderMap, StructDoc]:
    """全 agent call に共通する人間向け feedback の報告規範を構築する。"""
    root_definitions = path_context.root_placeholder_definitions()
    return (
        {"repo-root": root_definitions["repo-root"]},
        StructDoc(
            "human feedback reporting",
            """
            - 現在の作業外にいる人間の対応によって、再発防止、反復的な浪費の削減、または人間意図の確定が可能な問題だけを報告する
            - 通常の作業内で解決した問題、期待された制約、および根拠のない改善案は報告しない
            - 報告対象を発見した時点で `{{repo-root}}/.cmoc/gu/ar/feedback/reporter submit` を使用し、入力方法は同 reporter の `describe` に従う。feedback 保存 file は直接編集しない
            - 報告後も可能なら本命作業を継続する。報告対象がない場合は、feedback 用の出力または tool call を行わない
            """,
        ),
    )
