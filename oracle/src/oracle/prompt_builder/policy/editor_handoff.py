"""editor work file への handoff 用 instruction 文面の構築定義。"""

from functools import cache

from .basic import PolicyCollection, PolicyGroup
from .definitions import EDITOR_HANDOFF_PRESERVE_RESULT_POLICY


@cache
def build_editor_handoff_policy() -> PolicyCollection:
    """任意の agent call から editor work file へ handoff する規定を選択する。"""
    editor_handoff_group = PolicyGroup(
        group_id="90.editor_handoff",
        title="editor handoff policy",
        scope="agent call から editor work file へ handoff する時",
        policies=(EDITOR_HANDOFF_PRESERVE_RESULT_POLICY,),
    )
    return PolicyCollection(groups=(editor_handoff_group,))
