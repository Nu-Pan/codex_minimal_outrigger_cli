"""StructDoc の Markdown renderer 単体の整形挙動を検証する。

根拠:
- {{work-root}}/oracle/src/oracle/other/struct_doc.py
- {{work-root}}/oracle/doc/app_spec/prompt_standard.md
"""

from basic.struct_doc import (
    StructBlock,
    StructCodeBlock,
    StructDoc,
    render_as_markdown,
)


def test_render_as_markdown_collapses_consecutive_blank_lines() -> None:
    """Markdown rendererが連続blank lineを一つへ縮約することを検証する。"""
    doc = StructDoc(
        "root",
        "first\n\n\n   \nsecond",
    )

    rendered = render_as_markdown(doc)

    assert "\n\n\n" not in rendered
    assert rendered == "# root\n\nfirst\n\nsecond\n"


def test_render_as_markdown_collapses_code_block_blank_lines() -> None:
    """Markdown rendererがcode block内の連続blank lineも縮約することを検証する。"""
    doc = StructDoc("root", StructCodeBlock("text", "first\n\n\nsecond"))

    rendered = render_as_markdown(doc)

    assert rendered == "# root\n\n```text\nfirst\n\nsecond\n```\n"


def test_struct_block_is_reexported_from_realization_compatibility_module() -> None:
    """Oracle の参照 block 型を basic.struct_doc から同一型で公開する。"""
    rendered = render_as_markdown(
        [
            StructDoc("map", '<cmoc_ref target="target"/>'),
            StructBlock("target", StructDoc("body", "content")),
        ]
    )

    assert '<cmoc_block id="target">' in rendered
    assert "# body" in rendered


def test_struct_block_accepts_pre_rendered_markdown_as_opaque_child() -> None:
    """描画済み文字列 child を外側で再検査せずそのまま埋め込む。"""
    pre_rendered = '# rendered\n\n<cmoc_ref target="inner-target"/>\n'

    rendered = render_as_markdown(
        [
            StructDoc("map", '<cmoc_ref target="outer-target"/>'),
            StructDoc(
                "container",
                StructBlock("outer-target", pre_rendered),
            ),
        ]
    )

    assert pre_rendered in rendered
    assert '<cmoc_block id="outer-target">' in rendered
