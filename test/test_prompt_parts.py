from basic.acp import FileAccessMode
from basic.struct_doc import StructDoc, render_as_markdown
from acp.prompt_parts.apply_review_standard import build_apply_review_standard
from acp.prompt_parts.complete_prompt import build_complete_prompt
from acp.prompt_parts.index_entry_standard import build_index_entry_standard
from acp.prompt_parts.oracle_review_standard import build_review_oracle_standard


def test_build_apply_review_standard_renders_core_review_aspects() -> None:
    doc = build_apply_review_standard()

    assert isinstance(doc, StructDoc)
    assert doc.title == "apply review standard"

    rendered = render_as_markdown(doc)
    assert "oracle file と realization file の明確な不整合" in rendered
    assert "仕様断片の隙間" in rendered
    assert "致命的問題" in rendered
    assert "クオリティアップ" in rendered


def test_complete_prompt_can_include_apply_review_standard() -> None:
    prompt = build_complete_prompt(
        role="- role",
        summary="- summary",
        goal="- goal",
        file_access_mode=FileAccessMode.READONLY,
        aux_prompt=[],
        apply_review_standard=True,
    )

    rendered = render_as_markdown(prompt)
    assert "# oracle and realization basic" in rendered
    assert "# apply review standard" in rendered


def test_complete_prompt_omits_apply_review_standard_by_default() -> None:
    prompt = build_complete_prompt(
        role="- role",
        summary="- summary",
        goal="- goal",
        file_access_mode=FileAccessMode.READONLY,
        aux_prompt=[],
    )

    rendered = render_as_markdown(prompt)
    assert "apply review standard" not in rendered


def test_build_index_entry_standard_renders_core_output_rules() -> None:
    doc = build_index_entry_standard()

    assert isinstance(doc, StructDoc)
    assert doc.title == "index entry standard"

    rendered = render_as_markdown(doc)
    assert "読むべき対象へのルーティング情報" in rendered
    assert "対象内容に根拠" in rendered
    assert "機械的に補える情報" in rendered
    assert "ファイル名・ディレクトリ名・ハッシュ値" in rendered
    assert "Structured Output schema を読めば分かる出力項目名・型・形式" in rendered
    assert "関連しそうという理由だけ" in rendered
    assert "summary" not in rendered
    assert "read_this_when" not in rendered
    assert "do_not_read_this_when" not in rendered


def test_complete_prompt_can_include_index_entry_standard() -> None:
    prompt = build_complete_prompt(
        role="- role",
        summary="- summary",
        goal="- goal",
        file_access_mode=FileAccessMode.READONLY,
        aux_prompt=[],
        index_entry_standard=True,
    )

    rendered = render_as_markdown(prompt)
    assert "# index entry standard" in rendered


def test_complete_prompt_omits_index_entry_standard_by_default() -> None:
    prompt = build_complete_prompt(
        role="- role",
        summary="- summary",
        goal="- goal",
        file_access_mode=FileAccessMode.READONLY,
        aux_prompt=[],
    )

    rendered = render_as_markdown(prompt)
    assert "index entry standard" not in rendered


def test_build_review_oracle_standard_renders_core_review_rules() -> None:
    doc = build_review_oracle_standard()

    assert isinstance(doc, StructDoc)
    assert doc.title == "review oracle standard"

    rendered = render_as_markdown(doc)
    assert "fatal" in rendered
    assert "minor" in rendered
    assert "仕様断片同士に明確な矛盾" in rendered
    assert "実装者の裁量では解消不能" in rendered
    assert "誤字" in rendered
    assert "用語の不統一" in rendered
    assert "oracle file だけからは問題だとは言い切れない" in rendered
    assert "仕様からは実装が一意に定まらない" in rendered


def test_complete_prompt_can_include_review_oracle_standard() -> None:
    prompt = build_complete_prompt(
        role="- role",
        summary="- summary",
        goal="- goal",
        file_access_mode=FileAccessMode.READONLY,
        aux_prompt=[],
        review_oracle_standard=True,
    )

    rendered = render_as_markdown(prompt)
    assert "# oracle and realization basic" in rendered
    assert "# review oracle standard" in rendered


def test_complete_prompt_omits_review_oracle_standard_by_default() -> None:
    prompt = build_complete_prompt(
        role="- role",
        summary="- summary",
        goal="- goal",
        file_access_mode=FileAccessMode.READONLY,
        aux_prompt=[],
    )

    rendered = render_as_markdown(prompt)
    assert "review oracle standard" not in rendered
