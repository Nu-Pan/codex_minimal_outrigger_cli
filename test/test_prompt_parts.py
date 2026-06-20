from basic.acp import FileAccessMode
from basic.struct_doc import StructDoc, render_as_markdown
from acp.prompt_parts.apply_review_aspect import build_apply_review_aspect
from acp.prompt_parts.complete_prompt import build_complete_prompt


def test_build_apply_review_aspect_renders_core_review_aspects() -> None:
    doc = build_apply_review_aspect()

    assert isinstance(doc, StructDoc)
    assert doc.title == "apply review aspect"

    rendered = render_as_markdown(doc)
    assert "oracle file と realization file の明確な不整合" in rendered
    assert "仕様断片の隙間" in rendered
    assert "致命的問題" in rendered
    assert "クオリティアップ" in rendered


def test_complete_prompt_can_include_apply_review_aspect() -> None:
    prompt = build_complete_prompt(
        role="- role",
        summary="- summary",
        goal="- goal",
        file_access_mode=FileAccessMode.READONLY,
        aux_prompt=[],
        apply_review_aspect=True,
    )

    rendered = render_as_markdown(prompt)
    assert "# oracle and realization basic" in rendered
    assert "# apply review aspect" in rendered


def test_complete_prompt_omits_apply_review_aspect_by_default() -> None:
    prompt = build_complete_prompt(
        role="- role",
        summary="- summary",
        goal="- goal",
        file_access_mode=FileAccessMode.READONLY,
        aux_prompt=[],
    )

    rendered = render_as_markdown(prompt)
    assert "apply review aspect" not in rendered
