"""構造化文書の Markdown renderer 単体の整形挙動を検証する。

根拠:
- {{work-root}}/oracle/src/oracle/other/struct_doc.py
- {{work-root}}/oracle/doc/app_spec/prompt_policy.md
"""

from collections.abc import Callable

import pytest
from oracle.other.struct_doc import (
    SDCodeBlock,
    SDHeader,
    SDPolicy,
    SDTagBlock,
    render_sd_node_as_markdown,
)

from basic.struct_doc import (
    StructBlock as CompatStructBlock,
)
from basic.struct_doc import (
    StructCodeBlock as CompatStructCodeBlock,
)
from basic.struct_doc import (
    StructDoc as CompatStructDoc,
)
from basic.struct_doc import (
    render_as_markdown as render_compat_as_markdown,
)


def test_render_sd_node_as_markdown_collapses_consecutive_blank_lines() -> None:
    """Markdown rendererが連続blank lineを一つへ縮約することを検証する。"""
    doc = SDHeader(
        "root",
        "first\n\n\n   \nsecond",
    )

    rendered = render_sd_node_as_markdown(doc)

    assert "\n\n\n" not in rendered
    assert rendered == "# root\n\nfirst\n\nsecond\n"


def test_render_sd_node_as_markdown_collapses_code_block_blank_lines() -> None:
    """Markdown rendererがcode block内の連続blank lineも縮約することを検証する。"""
    doc = SDHeader("root", SDCodeBlock("text", "first\n\n\nsecond"))

    rendered = render_sd_node_as_markdown(doc)

    assert rendered == "# root\n\n```text\nfirst\n\nsecond\n```\n\n"


def test_render_sd_node_as_markdown_uses_fence_longer_than_dynamic_body() -> None:
    """本文の backtick 列が外側の code block を閉じないことを検証する。"""
    body = "before\n```\ninside\n````\nafter"

    rendered = render_sd_node_as_markdown(SDHeader("root", SDCodeBlock("text", body)))

    assert rendered == f"# root\n\n`````text\n{body}\n`````\n\n"


def test_sd_tag_block_renders_variadic_roots_and_generates_its_reference() -> None:
    """参照 block を可変長 root として描画し、対応する参照表記を生成する。"""
    block = SDTagBlock("target", SDHeader("body", "content"))

    rendered = render_sd_node_as_markdown(
        SDHeader("map", block.ref_tag),
        block,
    )

    assert block.ref_tag == '<cmoc_ref target="target"/>'
    assert '<cmoc_block id="target">' in rendered
    assert "## body" in rendered


def test_sd_tag_block_accepts_pre_rendered_markdown_as_opaque_child() -> None:
    """描画済み文字列 child を外側で再検査せずそのまま埋め込む。"""
    pre_rendered = '# rendered\n\n<cmoc_ref target="inner-target"/>\n'

    rendered = render_sd_node_as_markdown(
        SDHeader("map", '<cmoc_ref target="outer-target"/>'),
        SDHeader(
            "container",
            SDTagBlock("outer-target", pre_rendered),
        ),
    )

    assert (
        f'<cmoc_block id="outer-target">\n\n{pre_rendered}\n</cmoc_block>\n'
    ) in rendered


@pytest.mark.parametrize(
    ("roots", "expected_counts"),
    [
        pytest.param(
            [SDHeader("map", '<cmoc_ref target="missing"/>')],
            {'<cmoc_ref target="missing"/>': 1},
            id="missing-target",
        ),
        pytest.param(
            [
                SDTagBlock("duplicate", SDHeader("first", "body")),
                SDTagBlock("duplicate", SDHeader("second", "body")),
            ],
            {'<cmoc_block id="duplicate">': 2},
            id="duplicate-block-id",
        ),
        pytest.param(
            [SDHeader("map", '<cmoc_ref target="target" />')],
            {'<cmoc_ref target="target" />': 1},
            id="invalid-reference-syntax",
        ),
    ],
)
def test_render_sd_node_as_markdown_does_not_validate_references(
    roots: list[SDHeader | SDTagBlock], expected_counts: dict[str, int]
) -> None:
    """参照先欠落、block id 重複、不正な参照記法をそのまま render する。"""
    rendered = render_sd_node_as_markdown(*roots)

    for fragment, count in expected_counts.items():
        assert rendered.count(fragment) == count


def test_sd_policy_renders_only_non_empty_categories_in_fixed_order() -> None:
    """SDPolicy は適用条件と存在するカテゴリだけを所定順で描画する。"""
    rendered = render_sd_node_as_markdown(
        SDHeader(
            "policy",
            SDPolicy(
                when_use_this="適用条件",
                require=("必須事項",),
                prohibit=("禁止事項",),
                supplemental=("補足事項",),
            ),
        )
    )

    assert [
        line
        for line in rendered.splitlines()
        if line in {"**必須**", "**禁止**", "**許容**", "**補足情報**"}
    ] == ["**必須**", "**禁止**", "**補足情報**"]
    assert "適用条件" in rendered
    assert "- 必須事項" in rendered
    assert "- 禁止事項" in rendered
    assert "- 補足事項" in rendered


def test_realization_compatibility_module_reexports_canonical_nodes() -> None:
    """旧 basic.struct_doc API が canonical 型と renderer を再公開する。"""
    assert CompatStructBlock is SDTagBlock
    assert CompatStructCodeBlock is SDCodeBlock
    assert CompatStructDoc is SDHeader

    nodes = [
        CompatStructDoc("map", '<cmoc_ref target="target"/>'),
        CompatStructBlock("target", CompatStructDoc("body", "content")),
    ]
    assert render_compat_as_markdown(nodes) == render_sd_node_as_markdown(*nodes)


@pytest.mark.parametrize(
    ("constructor", "context"),
    [
        pytest.param(
            lambda: SDHeader("root", object()),
            "title=root",
            id="sd-header",
        ),
        pytest.param(
            lambda: SDTagBlock("root", object()),
            "block_id=root",
            id="sd-tag-block",
        ),
    ],
)
def test_struct_nodes_reject_an_invalid_single_child(
    constructor: Callable[[], object], context: str
) -> None:
    """単一の不正 child は構築対象を示す TypeError で拒否する。"""
    with pytest.raises(TypeError, match=context):
        constructor()
