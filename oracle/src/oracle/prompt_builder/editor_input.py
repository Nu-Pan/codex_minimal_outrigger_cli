"""ユーザー入力用 editor の初期表示文面の構築定義。"""

from oracle.other.struct_doc import SDHeader, SDTagBlock, render_sd_node_as_markdown


def build_prompt_editor_input_initial_text(
    complete_prompt_skeleton: str,
) -> str:
    """エディタ経由プロンプト入力の入力先ファイルへ注入する初期テキストを構築する。

    後続の AI エージェントに渡すプロンプトをファイルエディタ経由で受け取る場合がある。
    この経由用ファイルの初期状態として挿入するテキストをこの関数では生成する。

    complete_prompt_skeleton: str
        後続の AI エージェントに渡される完全プロンプトのうち「エディタ経由で入力したプロンプトを配置する予定の場所」を `{{original-prompt-here}}` で仮置きした状態のテキスト。

    return:
        入力先ファイルへ注入する初期テキスト
    """
    initial_text: list[SDHeader | SDTagBlock] = [
        SDHeader(
            "このファイルの使い方",
            """
            - 後続の AI エージェント呼び出しに渡す指示を HTML コメントブロックの外に記入して下さい
            - このファイルに記入されたプロンプトを <cmoc_ref target="prompt template"/> の `{{original-prompt-here}}` の位置に配置した完全プロンプト本文が構築されます
            - HTML コメントブロックは入力の読み出し時に削除され、後続の AI エージェントには渡されません
            - このファイルは未信頼かつ可変な作業ファイルであり、保存記録ではありません
            - 後続の AI エージェントは、完全プロンプト本文を初回入力として受け取ります
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
    return "<!--\n" + render_sd_node_as_markdown(*initial_text) + "\n-->\n"
