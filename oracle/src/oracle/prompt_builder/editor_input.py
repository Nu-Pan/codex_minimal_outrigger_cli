"""エディタ起動前に console へ表示する人間向け案内の構築定義。"""


def build_prompt_editor_input_console_guidance() -> str:
    """人間が editor input file に記入する内容を短く案内する。

    NOTE:
        意味仕様は `{{cmoc-root}}/oracle/doc/app_spec/prompt_editor_input.md` の
        「構築定義の参照」を参照。
    """
    # 依頼本文に含めず、エディタの起動前に表示する案内を返す。
    return (
        "これから開くエディタに、後続の AI エージェントへの指示を記入して下さい。\n"
        "求める成果、作業範囲、必要な制約を具体的に書いて下さい。\n"
    )
