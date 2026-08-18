"""StructDoc の Markdown renderer 単体の整形挙動を検証する。

根拠:
- {{work-root}}/oracle/src/oracle/other/struct_doc.py
- {{work-root}}/oracle/doc/app_spec/prompt_policy.md
"""

from collections.abc import Callable

import pytest
from oracle.other.struct_doc import SDTagBlock as OracleStructBlock

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

    assert rendered == "# root\n\n```text\nfirst\n\nsecond\n```\n\n"


def test_render_as_markdown_uses_fence_longer_than_dynamic_body() -> None:
    """本文の backtick 列が外側の code block を閉じないことを検証する。"""
    body = "before\n```\ninside\n````\nafter"

    rendered = render_as_markdown(StructDoc("root", StructCodeBlock("text", body)))

    assert rendered == f"# root\n\n`````text\n{body}\n`````\n\n"


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
        f'<cmoc_block id="outer-target">\n\n{pre_rendered}\n</cmoc_block>\n'
    ) in rendered


@pytest.mark.parametrize(
    ("roots", "expected_counts"),
    [
        pytest.param(
            [StructDoc("map", '<cmoc_ref target="missing"/>')],
            {'<cmoc_ref target="missing"/>': 1},
            id="missing-target",
        ),
        pytest.param(
            [
                StructBlock("duplicate", StructDoc("first", "body")),
                StructBlock("duplicate", StructDoc("second", "body")),
            ],
            {'<cmoc_block id="duplicate">': 2},
            id="duplicate-block-id",
        ),
        pytest.param(
            [StructDoc("map", '<cmoc_ref target="target" />')],
            {'<cmoc_ref target="target" />': 1},
            id="invalid-reference-syntax",
        ),
    ],
)
def test_render_as_markdown_does_not_validate_references(
    roots: list[StructDoc | StructBlock], expected_counts: dict[str, int]
) -> None:
    """参照先欠落、block id 重複、不正な参照記法をそのまま render する。"""
    rendered = render_as_markdown(roots)

    for fragment, count in expected_counts.items():
        assert rendered.count(fragment) == count


@pytest.mark.parametrize(
    ("constructor", "context"),
    [
        pytest.param(
            lambda: StructDoc("root", object()),
            "title=root",
            id="struct-doc",
        ),
        pytest.param(
            lambda: StructBlock("root", object()),
            "block_id=root",
            id="struct-block",
        ),
    ],
)
def test_struct_nodes_reject_an_invalid_single_child(
    constructor: Callable[[], object], context: str
) -> None:
    """単一の不正 child は構築対象を示す TypeError で拒否する。"""
    with pytest.raises(TypeError, match=context):
        constructor()
