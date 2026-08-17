"""editor work file への handoff 用 instruction 文面の構築定義。"""

from oracle.other.struct_doc import StructDoc
from oracle.prompt_builder.basic import PlaceholderMap


def build_editor_handoff_policy() -> tuple[PlaceholderMap, StructDoc]:
    """任意の agent call から editor work file へ handoff する規定を構築する。"""
    return (
        {},
        StructDoc(
            "editor handoff policy（agent call から editor work file へ handoff する時）",
            """
            **必須**

            - editor handoff でも、agent call に選択された file access mode と Codex CLI sandbox を維持する
            - handoff file への書き込みとは別に、その agent call が要求する正式な結果または成果物を満たす

            **許容**

            - agent call の責務を維持したまま、handoff file への書き込みに必要な command だけについて、対象 path と理由を限定した sandbox escalation を要求してよい
            """,
        ),
    )
