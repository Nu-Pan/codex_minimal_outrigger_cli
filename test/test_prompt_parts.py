"""標準 prompt parts と complete prompt の組み立て結果を検証する。

分割根拠: {{work-root}}/oracle/src/oracle/prompt_builder/parts/realization_standard.py
"""

from pathlib import Path

import pytest
from oracle.prompt_builder.complete_prompt import build_complete_prompt
from oracle.prompt_builder.parts.apply_review_standard import (
    build_apply_review_standard as _build_apply_review_standard,
)
from oracle.prompt_builder.parts.file_access_rule import (
    build_file_access_rule as _build_file_access_rule,
)
from oracle.prompt_builder.parts.index_entry_standard import (
    build_index_entry_standard as _build_index_entry_standard,
)
from oracle.prompt_builder.parts.oracle_review_standard import (
    build_review_oracle_standard as _build_review_oracle_standard,
)
from oracle.prompt_builder.parts.realization_standard import (
    build_realization_standard as _build_realization_standard,
)
from oracle.prompt_builder.parts.routing_rule import (
    build_routing_rule as _build_routing_rule,
)

from basic.acp import FileAccessMode
from basic.struct_doc import StructCodeBlock, StructDoc, render_as_markdown


def build_apply_review_standard() -> StructDoc:
    return _build_apply_review_standard()[1]


def build_file_access_rule(mode: FileAccessMode) -> StructDoc:
    return _build_file_access_rule(mode)[1]


def build_index_entry_standard() -> StructDoc:
    return _build_index_entry_standard()[1]


def build_review_oracle_standard() -> StructDoc:
    return _build_review_oracle_standard()[1]


def build_realization_standard() -> StructDoc:
    return _build_realization_standard()[1]


def build_routing_rule() -> StructDoc:
    return _build_routing_rule()[1]


def test_build_apply_review_standard_renders_core_review_aspects() -> None:
    doc = build_apply_review_standard()

    assert isinstance(doc, StructDoc)
    assert doc.title == "apply review standard"

    rendered = render_as_markdown(doc)
    assert "oracle file と realization file の明確な不整合" in rendered
    assert "仕様断片の隙間" in rendered
    assert "致命的問題" in rendered
    assert "クオリティアップ" in rendered


def test_build_routing_rule_renders_core_reading_rules() -> None:
    doc = build_routing_rule()

    assert isinstance(doc, StructDoc)
    assert doc.title == "routing rule"

    rendered = render_as_markdown(doc)
    assert "INDEX.md" in rendered
    assert "Summary" in rendered
    assert "Read this when" in rendered
    assert "Do not read this when" in rendered
    assert "必要な文章を読みに行く" in rendered
    assert "総当たりで読む前" in rendered


def test_complete_prompt_always_includes_routing_rule() -> None:
    prompt = build_complete_prompt(
        role="- role",
        summary="- summary",
        goal="- goal",
        file_access_mode=FileAccessMode.READONLY,
        aux_dynamic_prompt=[],
    )

    rendered = render_as_markdown(prompt)
    assert "# routing rule" in rendered


def test_file_access_rule_titles_and_bodies_match_modes() -> None:
    expected = {
        FileAccessMode.READONLY: [
            "ツリー外は読み書き禁止",
            "/.git` ツリー内は書き込み禁止",
            "oracle file は書き込み禁止",
            "realization file は書き込み禁止",
            "/memo` は読み書き禁止",
        ],
        FileAccessMode.PURE_ORACLE_READ: [
            "ツリー外は読み書き禁止",
            "oracle file は書き込み禁止",
            "realization file は読み書き禁止",
        ],
        FileAccessMode.REPO_WRITE: [
            "ツリー外は読み書き禁止",
            "/memo` は読み書き禁止",
            "/.git` ツリー内は書き込み禁止",
            "/.agents` ツリー内は書き込み禁止",
            "/.codex` ツリー内は書き込み禁止",
            "`AGENTS.md` は書き込み禁止",
            "`INDEX.md` は書き込み禁止",
        ],
        FileAccessMode.SKILL_AUTHORING_WRITE: [
            "ツリー外は読み書き禁止",
            "/memo` は読み書き禁止",
            "/.git` ツリー内は書き込み禁止",
            "/.agents` ツリー内は、`{{work-root}}/.agents/skills` ツリー内を除いて書き込み禁止",
            "repo-local Skill の作成・保守を明示した作業でだけ書き込み可能",
            "`AGENTS.md` は書き込み禁止",
            "`INDEX.md` は書き込み禁止",
        ],
        FileAccessMode.PURE_ORACLE_WRITE: [
            "ツリー外は読み書き禁止",
            "/memo` は読み書き禁止",
            "realization file は読み書き禁止",
        ],
        FileAccessMode.REALIZATION_WRITE: [
            "ツリー外は読み書き禁止",
            "/memo` は読み書き禁止",
            "oracle file は書き込み禁止",
        ],
    }

    for mode, fragments in expected.items():
        doc = build_file_access_rule(mode)
        rendered = render_as_markdown(doc)
        assert doc.title == f"file read write rule - {mode.value}"
        for fragment in fragments:
            assert fragment in rendered


def test_no_rule_complete_prompt_omits_standard_file_access_rule() -> None:
    prompt = build_complete_prompt(
        role="role",
        summary="summary",
        goal="goal",
        file_access_mode=FileAccessMode.NO_RULE,
    )
    rendered = render_as_markdown(prompt)

    assert "file read write rule" not in rendered


def test_complete_prompt_can_include_apply_review_standard() -> None:
    prompt = build_complete_prompt(
        role="- role",
        summary="- summary",
        goal="- goal",
        file_access_mode=FileAccessMode.READONLY,
        aux_dynamic_prompt=[],
        apply_review_standard=True,
    )

    rendered = render_as_markdown(prompt)
    assert "# oracle and realization basic" in rendered
    assert "# apply review standard" in rendered


def test_complete_prompt_preserves_injected_standard_terms() -> None:
    prompt = build_complete_prompt(
        role="- role",
        summary="- summary",
        goal="- goal",
        file_access_mode=FileAccessMode.READONLY,
        aux_dynamic_prompt=[],
        oracle_standard=True,
        realization_standard=True,
        review_oracle_standard=True,
        apply_review_standard=True,
        index_entry_standard=True,
    )

    rendered = render_as_markdown(prompt)
    assert "`oracle file` を検索語" in rendered
    assert "`oracle spec`" in rendered
    assert "`仕様ファイル`" in rendered
    assert "`oracles file` のような typo" in rendered
    for forbidden in ["{{cmoc-root}}", "{{run-root}}"]:
        assert forbidden not in rendered
    assert "{{repo-root}}" in rendered
    assert (
        "コメントにプレースホルダ `{{work-root}}` 起点の oracle file path を書く"
        in rendered
    )
    assert "`{{work-root}}/oracle/doc/...` のように根拠 path" in rendered
    for expected in [
        "oracle and realization basic",
        "oracle standard",
        "realization standard",
        "review oracle standard",
        "apply review standard",
        "index entry standard",
        "oracle file",
        "oracles file",
        "realization file",
    ]:
        assert expected in rendered


def test_complete_prompt_keeps_root_tokens_and_records_work_root_placeholder(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    repo_root = tmp_path / "repo"
    repo_root.mkdir()
    (repo_root / ".git").mkdir()
    monkeypatch.chdir(repo_root)

    prompt = build_complete_prompt(
        role="- cmoc から呼び出された AI Agent です",
        summary="- {{repo-root}} ツリー内の realization file を修正すること",
        goal="- realization standard と oracle standard に従うこと",
        file_access_mode=FileAccessMode.READONLY,
        aux_dynamic_prompt=[
            StructDoc(
                "aux realization file",
                "- {{cmoc-root}} と {{run-root}} と {{work-root}} 配下を確認すること",
            ),
            StructDoc(
                "所見本文",
                StructCodeBlock(
                    "json",
                    '{"summary": "realization file and {{repo-root}} stay in code block"}',
                ),
            ),
        ],
    )

    rendered = render_as_markdown(prompt)

    assert "- realization standard と oracle standard に従うこと" in rendered
    assert "# aux realization file" in rendered
    assert "cmoc から呼び出された" in rendered
    assert "{{repo-root}} ツリー内の realization file" in rendered
    assert "{{cmoc-root}} と {{run-root}} と {{work-root}} 配下" in rendered
    assert (
        '"summary": "realization file and {{repo-root}} stay in code block"' in rendered
    )
    assert f"- {{{{repo-root}}}} = {repo_root}" in rendered
    assert f"- {{{{work-root}}}} = {repo_root}" in rendered


def test_complete_prompt_keeps_literal_root_token_comment_requirement(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    repo_root = tmp_path / "repo"
    repo_root.mkdir()
    (repo_root / ".git").mkdir()
    monkeypatch.chdir(repo_root)

    prompt = build_complete_prompt(
        role="- role",
        summary="- {{work-root}}/src/app.py を確認すること",
        goal="- goal",
        file_access_mode=FileAccessMode.READONLY,
        aux_dynamic_prompt=[],
        realization_standard=True,
    )

    rendered = render_as_markdown(prompt)

    assert "- {{work-root}}/src/app.py を確認すること" in rendered
    assert (
        "コメントにプレースホルダ `{{work-root}}` 起点の oracle file path を書く"
        in rendered
    )
    assert "`{{work-root}}/oracle/doc/...` のように根拠 path" in rendered
    assert f"- {{{{work-root}}}} = {repo_root}" in rendered


def test_complete_prompt_omits_apply_review_standard_by_default() -> None:
    prompt = build_complete_prompt(
        role="- role",
        summary="- summary",
        goal="- goal",
        file_access_mode=FileAccessMode.READONLY,
        aux_dynamic_prompt=[],
    )

    rendered = render_as_markdown(prompt)
    assert "apply review standard" not in rendered


def test_build_realization_standard_renders_file_split_and_merge_rules() -> None:
    doc = build_realization_standard()

    assert isinstance(doc, StructDoc)
    assert doc.title == "realization standard"

    rendered = render_as_markdown(doc)
    assert "コメントや docstring は実装意図と根拠を補う" in rendered
    assert "対応する oracle file" in rendered
    assert "前後のコードを読むだけでは分からない情報" in rendered
    assert "INDEX.md" in rendered
    assert "8,000" in rendered
    assert "16,000" in rendered
    assert "責務境界" in rendered
    assert "分割" in rendered
    assert "統合" in rendered


def test_complete_prompt_can_include_realization_standard() -> None:
    prompt = build_complete_prompt(
        role="- role",
        summary="- summary",
        goal="- goal",
        file_access_mode=FileAccessMode.READONLY,
        aux_dynamic_prompt=[],
        realization_standard=True,
    )

    rendered = render_as_markdown(prompt)
    assert "# realization standard" in rendered
    assert "意味上のまとまりと適度なサイズ" in rendered
    assert "16,000" in rendered


def test_build_index_entry_standard_renders_core_output_rules() -> None:
    doc = build_index_entry_standard()

    assert isinstance(doc, StructDoc)
    assert doc.title == "index entry standard"

    rendered = render_as_markdown(doc)
    assert "読むべき対象へのルーティング情報" in rendered
    assert "対象内容に根拠" in rendered
    assert "機械的に補える情報" in rendered
    assert (
        "ファイル・ディレクトリの識別子、ハッシュ、出力形式は、この agent call の外側"
        in rendered
    )
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
        aux_dynamic_prompt=[],
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
        aux_dynamic_prompt=[],
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
    assert "`cmoc review oracle`" in rendered


def test_complete_prompt_can_include_review_oracle_standard() -> None:
    prompt = build_complete_prompt(
        role="- role",
        summary="- summary",
        goal="- goal",
        file_access_mode=FileAccessMode.READONLY,
        aux_dynamic_prompt=[],
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
        aux_dynamic_prompt=[],
    )

    rendered = render_as_markdown(prompt)
    assert "review oracle standard" not in rendered
