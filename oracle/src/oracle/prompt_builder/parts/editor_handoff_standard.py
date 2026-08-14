"""editor work file への handoff 用 instruction 文面の構築定義。"""

from functools import cache

from oracle.other.standard import StandardCollection, StandardGroup

from .standard_definitions import EDITOR_HANDOFF_PRESERVE_RESULT_STANDARD


@cache
def build_editor_handoff_standard() -> StandardCollection:
    """任意の agent call から editor work file へ handoff する規範を選択する。"""
    editor_handoff_group = StandardGroup(
        group_id="90.editor_handoff",
        title="editor handoff standard",
        scope="agent call から editor work file へ handoff する時",
        standards=(EDITOR_HANDOFF_PRESERVE_RESULT_STANDARD,),
    )
    return StandardCollection(groups=(editor_handoff_group,))
