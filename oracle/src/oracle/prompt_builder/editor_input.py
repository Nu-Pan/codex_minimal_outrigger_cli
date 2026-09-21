"""人間が直接記入する editor input の初期文面の構築定義。"""


def build_prompt_editor_input_initial_text() -> str:
    """入力先を案内する短い HTML コメントを構築する。

    NOTE:
        意味仕様は `{{cmoc-root}}/oracle/doc/app_spec/prompt_editor_input.md` の
        「構築定義の参照」を参照。
    """
    # 人間向けの説明だけを初期表示する。
    return (
        "<!--\n"
        "後続の AI エージェントへの指示を、このコメントの外に記入して下さい。\n"
        "求める成果、作業範囲、必要な制約を具体的に書いて下さい。\n"
        "-->\n"
    )
