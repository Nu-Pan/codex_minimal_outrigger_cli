"""文書参照の入力境界と、ファイル・ID が混在する Markdown 表記を検証する。"""

from pathlib import Path

import pytest
from reference.other.doc_ref_model import (
    DocRef,
    render_doc_ref_as_inline_md,
    render_doc_ref_as_multiline_md,
)


@pytest.mark.parametrize(
    ("file_path", "identifier", "expected"),
    [
        (Path("/reference/guide.md"), None, "参照内容 (`/reference/guide.md`)"),
        (None, "DECI-000001", "参照内容 [DECI-000001]"),
        (None, "SPEC-000002", "参照内容 [SPEC-000002]"),
    ],
)
def test_inline_reference_preserves_description_and_location(
    file_path, identifier, expected
):
    reference = DocRef("参照内容", file_path, identifier)

    assert reference.location_info == (
        file_path if file_path is not None else identifier
    )
    assert render_doc_ref_as_inline_md(reference) == expected


@pytest.mark.parametrize(
    ("references", "expected"),
    [
        ((), ""),
        (
            (
                DocRef("仕様 B", None, "SPEC-000002"),
                DocRef("資料 B", Path("/reference/guide.md"), None),
                DocRef("決定事項", None, "DECI-000001"),
                DocRef("資料 A", Path("/reference/guide.md"), None),
                DocRef("仕様 A", None, "SPEC-000002"),
            ),
            "- `/reference/guide.md`\n"
            "    - 資料 A\n"
            "    - 資料 B\n"
            "- [DECI-000001]\n"
            "    - 決定事項\n"
            "- [SPEC-000002]\n"
            "    - 仕様 A\n"
            "    - 仕様 B",
        ),
    ],
)
def test_multiline_references_group_mixed_locations_from_an_iterator(
    references, expected
):
    assert render_doc_ref_as_multiline_md(iter(references)) == expected


@pytest.mark.parametrize(
    "description",
    ["", " \t", "first\nsecond", "first\rsecond", "first\r\nsecond", "description\n"],
)
def test_reference_rejects_blank_or_multiline_descriptions(description):
    with pytest.raises(ValueError):
        DocRef(description, None, "SPEC-000001")


@pytest.mark.parametrize(
    ("file_path", "identifier"),
    [
        (None, None),
        (Path("/reference/guide.md"), "DECI-000001"),
        (Path("/reference/guide.md"), ""),
        (Path("relative.md"), None),
        (None, ""),
        (None, "SPEC-12345"),
        (None, "SPEC-1234567"),
        (None, "UNKNOWN-123456"),
        (None, "DECI-123456\n"),
    ],
)
def test_reference_rejects_missing_ambiguous_or_invalid_locations(
    file_path, identifier
):
    with pytest.raises(ValueError):
        DocRef("参照内容", file_path, identifier)
