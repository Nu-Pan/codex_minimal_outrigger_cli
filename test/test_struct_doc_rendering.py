"""StructDoc の Markdown renderer 単体の整形挙動を検証する。

分割根拠: <work-root>/oracle/src/oracle/prompt_builder/parts/realization_standard.py
"""

from basic.struct_doc import StructCodeBlock, StructDoc, render_as_markdown


def test_render_as_markdown_collapses_consecutive_blank_lines() -> None:
    doc = StructDoc(
        "root",
        "first\n\n\n   \nsecond",
    )

    rendered = render_as_markdown(doc)

    assert "\n\n\n" not in rendered
    assert rendered == "# root\n\nfirst\n\nsecond\n"


def test_render_as_markdown_collapses_code_block_blank_lines() -> None:
    doc = StructDoc("root", StructCodeBlock("text", "first\n\n\nsecond"))

    rendered = render_as_markdown(doc)

    assert rendered == "# root\n\n```text\nfirst\n\nsecond\n```\n"
