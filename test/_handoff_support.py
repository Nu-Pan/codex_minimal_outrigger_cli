"""handoff の項目別入力と、正本 builder による期待本文を共有する。"""

from oracle.editor_input_handoff.body import build_editor_input_handoff_body


def handoff_input(target_id, instructions):
    return {
        "target_id": target_id,
        "goal": "依頼した変更が反映されていること",
        "instructions": instructions,
        "background": "入力の受け渡しを検証する",
        "decisions": "追加の決定なし",
        "open_questions": "未確定事項なし",
        "oracle_references": [],
    }


def handoff_body(instructions, source):
    fields = handoff_input("unused", instructions)
    fields.pop("target_id")
    return build_editor_input_handoff_body(**fields, source=source)
