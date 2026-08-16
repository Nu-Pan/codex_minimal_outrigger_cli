"""StructDoc の Markdown renderer 単体の整形挙動を検証する。

根拠:
- {{work-root}}/oracle/src/oracle/other/struct_doc.py
- {{work-root}}/oracle/doc/app_spec/prompt_policy.md
"""

import pytest
from oracle.other.struct_doc import StructBlock as OracleStructBlock

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


def test_render_as_markdown_uses_fence_longer_than_dynamic_body() -> None:
    """本文の backtick 列が外側の code block を閉じないことを検証する。"""
    body = "before\n```\ninside\n````\nafter"

    rendered = render_as_markdown(StructDoc("root", StructCodeBlock("text", body)))

    assert rendered == f"# root\n\n`````text\n{body}\n`````\n"


def test_struct_block_is_reexported_from_realization_compatibility_module() -> None:
    """Oracle の参照 block 型を basic.struct_doc から同一型で公開する。"""
    assert StructBlock is OracleStructBlock

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

    assert (
        f'<cmoc_block id="outer-target">\n{pre_rendered}</cmoc_block>\n'
    ) in rendered


@pytest.mark.parametrize(
    ("roots", "error_message"),
    [
        pytest.param(
            [StructDoc("map", '<cmoc_ref target="missing"/>')],
            "cmoc_ref target is not present",
            id="missing-target",
        ),
        pytest.param(
            [
                StructBlock("duplicate", StructDoc("first", "body")),
                StructBlock("duplicate", StructDoc("second", "body")),
            ],
            "Duplicate cmoc_block id",
            id="duplicate-block-id",
        ),
        pytest.param(
            [StructDoc("map", '<cmoc_ref target="target" />')],
            "Invalid cmoc_ref syntax",
            id="invalid-reference-syntax",
        ),
    ],
)
def test_render_as_markdown_rejects_invalid_references(
    roots: list[StructDoc | StructBlock], error_message: str
) -> None:
    """参照先欠落、block id 重複、不正な参照記法を拒否する。"""
    with pytest.raises(ValueError, match=error_message):
        render_as_markdown(roots)
