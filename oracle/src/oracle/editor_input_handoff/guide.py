"""editor input と独立した handoff ガイドの文面の構築定義。"""

from oracle.other.struct_doc import SDHeader, SDTagBlock, render_sd_node_as_markdown


def build_editor_input_handoff_guide(complete_prompt_skeleton: str) -> str:
    """受信先の完全 prompt の雛形から handoff ガイドを構築する。

    Args:
        complete_prompt_skeleton: 依頼の入力位置を `{{original-prompt-here}}` で
            示した受信先の完全 prompt の雛形。

    Returns:
        handoff ガイドファイルへ保存する Markdown 文面。

    NOTE:
        意味仕様は `{{cmoc-root}}/oracle/doc/app_spec/editor_input_handoff.md` の
        「handoff ガイド」を参照。
    """
    # 依頼作成の案内と受信先の雛形を、参照用の文書としてまとめる。
    guide: list[SDHeader | SDTagBlock] = [
        SDHeader(
            "handoff ガイドの使い方",
            """
            - 受信先への項目別の依頼内容を作成するために、このガイドを参照して下さい
            - <cmoc_ref target="prompt template"/> の作業範囲・制約と、`{{original-prompt-here}}` で示された依頼の入力位置を確認して下さい
            """,
        ),
        SDHeader(
            "記入の目安",
            """
            - GitHub Flavored Markdown で、求める成果、作業範囲、および完了条件を具体的に書いて下さい
            - 必要な制約、禁止事項、および検証方法がある場合は明示して下さい
            - agent が参照できる情報は、本文を複製せず参照先または検索可能な手掛かりを示して下さい
            - agent が参照できない用語、前提、または判断基準は、作業に必要な範囲で説明して下さい
            """,
        ),
        SDTagBlock("prompt template", complete_prompt_skeleton),
    ]
    return render_sd_node_as_markdown(*guide)
