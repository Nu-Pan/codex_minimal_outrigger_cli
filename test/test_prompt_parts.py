"""標準 prompt parts と complete prompt の組み立て結果を検証する。

各 prompt part の rendering と complete prompt の有効化・placeholder 展開は同じ
StructDoc 出力を共有する一つの責務であるため、prompt builder 回帰として一箇所に保つ。

対応する正本:
- {{work-root}}/oracle/doc/app_spec/prompt_standard.md
- {{work-root}}/oracle/doc/app_spec/feedback_observation.md
- {{work-root}}/oracle/src/oracle/other/standard.py
- {{work-root}}/oracle/src/oracle/prompt_builder/complete_prompt.py
- {{work-root}}/oracle/src/oracle/prompt_builder/parts/apply_review_standard.py
- {{work-root}}/oracle/src/oracle/prompt_builder/parts/common_standard.py
- {{work-root}}/oracle/src/oracle/prompt_builder/parts/conflict_resolution_standard.py
- {{work-root}}/oracle/src/oracle/prompt_builder/parts/feedback_reporting_standard.py
- {{work-root}}/oracle/src/oracle/prompt_builder/parts/file_access_rule.py
- {{work-root}}/oracle/src/oracle/prompt_builder/parts/index_entry_standard.py
- {{work-root}}/oracle/src/oracle/prompt_builder/parts/oracle_and_realization_basic.py
- {{work-root}}/oracle/src/oracle/prompt_builder/parts/oracle_review_standard.py
- {{work-root}}/oracle/src/oracle/prompt_builder/parts/oracle_standard.py
- {{work-root}}/oracle/src/oracle/prompt_builder/parts/realization_oracle_reference_rule.py
- {{work-root}}/oracle/src/oracle/prompt_builder/parts/realization_standard.py
- {{work-root}}/oracle/src/oracle/prompt_builder/parts/routing_rule.py
- {{work-root}}/oracle/src/oracle/prompt_builder/parts/standard_definitions.py
"""

from dataclasses import FrozenInstanceError
from pathlib import Path

import pytest
from oracle.other.standard import (
    Standard,
    StandardCollection,
    StandardGroup,
    combine_standard_collections,
    standard_collection_to_struct_docs,
)
from oracle.prompt_builder.complete_prompt import build_complete_prompt
from oracle.prompt_builder.parts.apply_review_standard import (
    build_apply_review_standard as _build_apply_review_standard,
)
from oracle.prompt_builder.parts.conflict_resolution_standard import (
    build_conflict_resolution_standard as _build_conflict_resolution_standard,
)
from oracle.prompt_builder.parts.file_access_rule import (
    build_file_access_rule as _build_file_access_rule,
)
from oracle.prompt_builder.parts.index_entry_standard import (
    build_index_entry_standard as _build_index_entry_standard,
)
from oracle.prompt_builder.parts.oracle_review_standard import (
    build_oracle_review_standard as _build_oracle_review_standard,
)
from oracle.prompt_builder.parts.realization_oracle_reference_rule import (
    build_realization_oracle_reference_rule as _build_realization_oracle_reference_rule,
)
from oracle.prompt_builder.parts.realization_standard import (
    build_realization_standard as _build_realization_standard,
)
from oracle.prompt_builder.parts.routing_rule import (
    build_routing_rule as _build_routing_rule,
)

from basic.acp import FileAccessMode
from basic.path_model import AgentCallPathContext
from basic.struct_doc import StructCodeBlock, StructDoc, render_as_markdown


def _path_context() -> AgentCallPathContext:
    """現在の test repository を起点に call-scoped path context を作る。"""
    return AgentCallPathContext(agent_call_cwd=Path.cwd())


def _render_standard_collection(collection: StandardCollection) -> str:
    """StandardCollection を complete prompt と同じ経路で render する。"""
    return render_as_markdown(standard_collection_to_struct_docs(collection))


def test_standard_values_are_immutable_and_require_meaningful_text() -> None:
    """Standard は入れ子の文面も固定し、空の規範を拒否する。"""
    standard = Standard(
        standard_id="sample.standard",
        title="sample",
        required=["required"],
        prohibited=["prohibited"],
    )

    assert standard.required == ("required",)
    assert standard.prohibited == ("prohibited",)
    with pytest.raises(FrozenInstanceError):
        setattr(standard, "title", "changed")
    with pytest.raises(ValueError, match="at least one requirement"):
        Standard(standard_id="empty.standard", title="empty")
    with pytest.raises(ValueError, match="non-empty strings"):
        Standard(
            standard_id="invalid.standard",
            title="invalid",
            required=("",),
        )


def test_standard_collection_renders_labels_without_internal_ids() -> None:
    """規範本文は label 順に render し、合成用 ID を prompt へ出さない。"""
    standard = Standard(
        standard_id="internal.standard-id",
        title="規範タイトル",
        required=("必須本文",),
        prohibited=("禁止本文",),
        recommended=("推奨本文",),
        permitted=("許容本文",),
        examples=("判断例本文",),
    )
    collection = StandardCollection(
        groups=(
            StandardGroup(
                group_id="internal.group-id",
                title="group title",
                scope="適用範囲",
                standards=(standard,),
            ),
        )
    )

    rendered = _render_standard_collection(collection)

    assert "# 規範タイトル（適用範囲）" in rendered
    labels = ("**必須**", "**禁止**", "**推奨**", "**許容**", "**判断例**")
    assert [rendered.index(label) for label in labels] == sorted(
        rendered.index(label) for label in labels
    )
    assert "internal.standard-id" not in rendered
    assert "internal.group-id" not in rendered


def test_combined_standard_collections_are_deduplicated_and_order_independent() -> None:
    """共有 Standard を一度だけ残し、builder の選択順から出力順を切り離す。"""
    realization = _build_realization_standard()
    apply_review = _build_apply_review_standard()

    forward = combine_standard_collections(realization, apply_review)
    reverse = combine_standard_collections(apply_review, realization)

    assert forward == reverse
    rendered = _render_standard_collection(forward)
    assert (
        rendered.count(
            "realization file の都合または挙動を根拠に oracle file の意味を変更"
        )
        == 1
    )
    assert rendered.index("oracle file を正本として扱う") < rendered.index(
        "realization standard"
    )
    assert rendered.index("realization standard") < rendered.index(
        "所見・修正対象に具体的な根拠を求める"
    )


def test_combined_standard_collections_reject_conflicting_ids() -> None:
    """同じ ID に異なる Standard または group 定義を割り当てない。"""
    first_standard = Standard("shared.standard", "first", required=("body",))
    conflicting_standard = Standard(
        "shared.standard", "conflicting", required=("body",)
    )
    first = StandardCollection(
        (StandardGroup("group.first", "first group", "scope", (first_standard,)),)
    )
    conflicting = StandardCollection(
        (
            StandardGroup(
                "group.second",
                "second group",
                "scope",
                (conflicting_standard,),
            ),
        )
    )

    with pytest.raises(ValueError, match="Conflicting Standard definition"):
        combine_standard_collections(first, conflicting)

    conflicting_group = StandardCollection(
        (
            StandardGroup(
                "group.first",
                "conflicting group",
                "scope",
                (Standard("other.standard", "other", required=("body",)),),
            ),
        )
    )
    with pytest.raises(ValueError, match="Conflicting StandardGroup definition"):
        combine_standard_collections(first, conflicting_group)


def test_build_apply_review_standard_renders_core_review_aspects() -> None:
    """apply review standard の主要な所見境界が render される。"""
    collection = _build_apply_review_standard()

    assert isinstance(collection, StandardCollection)

    rendered = _render_standard_collection(collection)
    assert "apply review standard" in rendered
    assert "oracle file に対する realization file の追従要否" in rendered
    assert "明確な不適合または致命的な実装問題" in rendered
    assert "所見・修正対象に具体的な根拠を求める" in rendered
    assert "oracle file に記述がないこと、仕様の隙間" in rendered
    assert "調査開始時点ですでに解消されている問題" in rendered


def test_conflict_resolution_standard_is_injected_without_editing_standards() -> None:
    """conflict 解消には専用規範だけを編集規範として注入する。"""
    collection = _build_conflict_resolution_standard()
    rendered_doc = _render_standard_collection(collection)
    assert "`cmoc session join` の conflict marker 解消時だけ" in rendered_doc
    assert "conflict marker の解消に不要な仕様変更" in rendered_doc

    prompt = build_complete_prompt(
        summary="- summary",
        goal="- goal",
        file_access_mode=FileAccessMode.REPO_WRITE,
        path_context=_path_context(),
        conflict_resolution_standard=True,
    )
    rendered = render_as_markdown(prompt)
    assert "# oracle and realization basic" in rendered
    assert "# 両 branch の意味を保って conflict marker だけを解消する" in rendered
    for heading in (
        "# oracle standard",
        "# realization standard",
        "# oracle review standard",
        "# apply review standard",
    ):
        assert heading not in rendered


def test_realization_oracle_reference_rule_is_independently_selectable() -> None:
    """oracle path コメント規則を realization standard と分離して注入する。"""
    doc = _build_realization_oracle_reference_rule(_path_context())[1]
    rendered_doc = render_as_markdown(doc)
    assert doc.title == "realization oracle reference rule"
    assert "realization code を作成または変更する場合" in rendered_doc
    assert "`{{work-root}}` 起点の oracle file path" in rendered_doc

    prompt = build_complete_prompt(
        summary="- summary",
        goal="- goal",
        file_access_mode=FileAccessMode.REALIZATION_WRITE,
        path_context=_path_context(),
        realization_oracle_reference_rule=True,
    )
    rendered = render_as_markdown(prompt)
    assert "# oracle and realization basic" in rendered
    assert "# realization oracle reference rule" in rendered
    assert "# oracle standard" not in rendered
    assert "# realization standard" not in rendered


def test_build_routing_rule_renders_core_reading_rules() -> None:
    """routing ruleがINDEX案内の主要な見出しをrenderすることを検証する。"""
    doc = _build_routing_rule(_path_context())[1]

    assert isinstance(doc, StructDoc)
    assert doc.title == "routing rule"

    rendered = render_as_markdown(doc)
    assert "INDEX.md" in rendered
    assert "Summary" in rendered
    assert "Read this when" in rendered
    assert "Do not read this when" in rendered
    assert "必要な本文を読む" in rendered
    assert "総当たりで読む前" in rendered


def test_complete_prompt_controls_routing_rule_explicitly() -> None:
    """repository 参照の有無に応じて routing rule を選択する。"""
    default_prompt = build_complete_prompt(
        summary="- summary",
        goal="- goal",
        file_access_mode=FileAccessMode.READONLY,
        path_context=_path_context(),
        aux_dynamic_prompt=[],
    )
    repository_prompt = build_complete_prompt(
        summary="- summary",
        goal="- goal",
        file_access_mode=FileAccessMode.READONLY,
        path_context=_path_context(),
        aux_dynamic_prompt=[],
        routing_rule=True,
    )

    assert "# routing rule" not in render_as_markdown(default_prompt)
    assert "# routing rule" in render_as_markdown(repository_prompt)


def test_complete_prompt_maps_responsibility_and_task_to_summary() -> None:
    """担当と主作業を独立 role ではなく summary から参照する。"""
    prompt = build_complete_prompt(
        summary="- あなたは prompt 検証担当です\n- 対象 prompt を確認すること",
        goal="- prompt の参照関係が妥当であること",
        file_access_mode=FileAccessMode.READONLY,
        path_context=_path_context(),
    )

    rendered = render_as_markdown(prompt)
    assert '## 担当と依頼の概要\n\n<cmoc_ref target="summary"/>' in rendered
    assert "あなたは prompt 検証担当です" in rendered
    assert "対象 prompt を確認すること" in rendered
    assert '<cmoc_ref target="role"/>' not in rendered
    assert '<cmoc_block id="role">' not in rendered


def test_complete_prompt_includes_feedback_instruction_exactly_once() -> None:
    """全 agent call の共通 feedback instruction が一経路だけで注入される。"""
    prompt = build_complete_prompt(
        summary="- summary",
        goal="- goal",
        file_access_mode=FileAccessMode.READONLY,
        path_context=_path_context(),
        aux_dynamic_prompt=[],
    )

    rendered = render_as_markdown(prompt)
    assert rendered.count("# human feedback reporting") == 1
    assert rendered.count("cmoc_feedback.submit_observation") == 1
    assert "feedback 保存 file は直接編集しない" in rendered


def test_complete_prompt_merges_equal_root_definitions_and_rejects_conflicts(
    tmp_path: Path,
) -> None:
    """root placeholder は同値なら統合し、異値なら prompt 構築を失敗させる。"""
    context = _path_context()

    prompt = build_complete_prompt(
        summary="- summary",
        goal="- goal",
        file_access_mode=FileAccessMode.READONLY,
        path_context=context,
        aux_placeholder_def={"work-root": context.work_root},
    )
    assert render_as_markdown(prompt).count("- {{work-root}} =") == 1

    with pytest.raises(ValueError, match="Conflicting placeholder definition"):
        build_complete_prompt(
            summary="- summary",
            goal="- goal",
            file_access_mode=FileAccessMode.READONLY,
            path_context=context,
            aux_placeholder_def={"work-root": tmp_path / "other-worktree"},
        )


def test_file_access_rule_titles_and_bodies_match_modes() -> None:
    """各file access modeに対応する標準ruleの内容を検証する。"""
    mode_specific_rules = {
        FileAccessMode.READONLY: {
            "oracle file は書き込み禁止",
            "realization file は書き込み禁止",
        },
        FileAccessMode.PURE_ORACLE_READ: {
            "oracle file は書き込み禁止",
            "realization file は読み書き禁止",
        },
        FileAccessMode.REPO_WRITE: set(),
        FileAccessMode.PURE_ORACLE_WRITE: {
            "realization file は読み書き禁止",
        },
        FileAccessMode.REALIZATION_WRITE: {
            "oracle file は書き込み禁止",
        },
    }
    all_mode_specific_rules = set().union(*mode_specific_rules.values())
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
        doc = _build_file_access_rule(mode, _path_context())[1]
        rendered = render_as_markdown(doc)
        assert doc.title == f"file read write rule - {mode.value}"
        for fragment in fragments:
            assert fragment in rendered
        for fragment in all_mode_specific_rules - mode_specific_rules[mode]:
            assert fragment not in rendered


def test_no_rule_complete_prompt_omits_standard_file_access_rule() -> None:
    """NO_RULE時に標準file access ruleを挿入しないことを検証する。"""
    prompt = build_complete_prompt(
        summary="summary",
        goal="goal",
        file_access_mode=FileAccessMode.NO_RULE,
        path_context=_path_context(),
    )
    rendered = render_as_markdown(prompt)

    assert "file read write rule" not in rendered


def test_complete_prompt_can_include_apply_review_standard() -> None:
    """complete promptへapply review standardを追加できることを検証する。"""
    prompt = build_complete_prompt(
        summary="- summary",
        goal="- goal",
        file_access_mode=FileAccessMode.READONLY,
        path_context=_path_context(),
        aux_dynamic_prompt=[],
        apply_review_standard=True,
    )

    rendered = render_as_markdown(prompt)
    assert "# oracle and realization basic" in rendered
    assert "# oracle standard" in rendered
    assert "# realization standard" in rendered
    assert "# apply review standard" in rendered


def test_complete_prompt_preserves_injected_standard_terms() -> None:
    """complete promptが注入した各standardの主要語とplaceholderを保持することを検証する。"""
    prompt = build_complete_prompt(
        summary="- summary",
        goal="- goal",
        file_access_mode=FileAccessMode.READONLY,
        path_context=_path_context(),
        aux_dynamic_prompt=[],
        oracle_standard=True,
        realization_standard=True,
        oracle_review_standard=True,
        apply_review_standard=True,
        conflict_resolution_standard=True,
        realization_oracle_reference_rule=True,
        index_entry_standard=True,
    )

    rendered = render_as_markdown(prompt)
    assert "cmoc 固有契約または oracle file と installed skill" in rendered
    assert "現行仕様に必要な実装だけを保つ" in rendered
    assert "所見の列挙、統合、擁護理由列挙、反証理由列挙、および採否判定" in rendered
    assert "両 branch の意味を保って conflict marker だけを解消する" in rendered
    assert "### 背景" not in rendered
    for forbidden in ["{{cmoc-root}}", "{{run-root}}"]:
        assert forbidden not in rendered
    assert "{{repo-root}}" in rendered
    assert (
        "realization code のコメントに `{{work-root}}` 起点の oracle file path を書く"
        in rendered
    )
    for expected in [
        "oracle and realization basic",
        "oracle standard",
        "realization standard",
        "oracle review standard",
        "apply review standard",
        "両 branch の意味を保って conflict marker だけを解消する",
        "realization oracle reference rule",
        "index entry standard",
        "oracle file",
        "realization file",
    ]:
        assert expected in rendered


def test_complete_prompt_keeps_root_tokens_and_records_work_root_placeholder(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """complete promptが入力root tokenを保持し、実pathの定義行を追加することを検証する。"""
    repo_root = tmp_path / "repo"
    repo_root.mkdir()
    (repo_root / ".git").mkdir()
    monkeypatch.chdir(repo_root)

    prompt = build_complete_prompt(
        summary=(
            "- cmoc から呼び出された AI Agent です\n"
            "- {{repo-root}} ツリー内の realization file を修正すること"
        ),
        goal="- realization standard と oracle standard に従うこと",
        file_access_mode=FileAccessMode.READONLY,
        path_context=_path_context(),
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
    """literal work-root tokenとコメント根拠規則がpromptに残ることを検証する。"""
    repo_root = tmp_path / "repo"
    repo_root.mkdir()
    (repo_root / ".git").mkdir()
    monkeypatch.chdir(repo_root)

    prompt = build_complete_prompt(
        summary="- {{work-root}}/src/app.py を確認すること",
        goal="- goal",
        file_access_mode=FileAccessMode.READONLY,
        path_context=_path_context(),
        aux_dynamic_prompt=[],
        realization_standard=True,
        realization_oracle_reference_rule=True,
    )

    rendered = render_as_markdown(prompt)

    assert "- {{work-root}}/src/app.py を確認すること" in rendered
    assert (
        "realization code のコメントに `{{work-root}}` 起点の oracle file path を書く"
        in rendered
    )
    assert f"- {{{{work-root}}}} = {repo_root}" in rendered


def test_complete_prompt_omits_apply_review_standard_by_default() -> None:
    """既定のcomplete promptがapply review standardを含めないことを検証する。"""
    prompt = build_complete_prompt(
        summary="- summary",
        goal="- goal",
        file_access_mode=FileAccessMode.READONLY,
        path_context=_path_context(),
        aux_dynamic_prompt=[],
    )

    rendered = render_as_markdown(prompt)
    assert "apply review standard" not in rendered


def test_build_realization_standard_renders_core_conformance_rules() -> None:
    """realization standard の適合性と検証境界が render される。"""
    collection = _build_realization_standard()

    assert isinstance(collection, StandardCollection)

    rendered = _render_standard_collection(collection)
    assert "realization standard" in rendered
    assert "realization file を現行の oracle file に適合させる" in rendered
    assert "現行仕様に必要な実装だけを保つ" in rendered
    assert "対象 repository 固有の手順で変更を検証する" in rendered
    assert "配置場所にかかわらず特定" in rendered
    assert "`.agents/skills` に限定" in rendered


def test_complete_prompt_can_include_realization_standard() -> None:
    """complete promptへrealization standardを追加できることを検証する。"""
    prompt = build_complete_prompt(
        summary="- summary",
        goal="- goal",
        file_access_mode=FileAccessMode.READONLY,
        path_context=_path_context(),
        aux_dynamic_prompt=[],
        realization_standard=True,
    )

    rendered = render_as_markdown(prompt)
    assert "# oracle standard" in rendered
    assert "# realization standard" in rendered
    assert "対象 repository 固有の手順で変更を検証する" in rendered
    assert "# realization oracle reference rule" not in rendered


def test_build_index_entry_standard_renders_core_output_rules() -> None:
    """index entry standardの出力境界がrenderされることを検証する。"""
    collection = _build_index_entry_standard()

    assert isinstance(collection, StandardCollection)

    rendered = _render_standard_collection(collection)
    assert "index entry standard" in rendered
    assert "読むべき対象へのルーティング情報" in rendered
    assert "対象内容に根拠" in rendered
    assert "機械的に補える情報" in rendered
    assert "対象が担う責務と、同階層の他対象ではなくその対象へ進む理由" in rendered
    assert "ファイル名・ディレクトリ名・ハッシュ値" in rendered
    assert "Structured Output schema を読めば分かる出力項目名・型・形式" in rendered
    assert "関連しそうという理由だけ" in rendered
    assert "summary" not in rendered
    assert "read_this_when" not in rendered
    assert "do_not_read_this_when" not in rendered


def test_complete_prompt_can_include_index_entry_standard() -> None:
    """complete promptへindex entry standardを追加できることを検証する。"""
    prompt = build_complete_prompt(
        summary="- summary",
        goal="- goal",
        file_access_mode=FileAccessMode.READONLY,
        path_context=_path_context(),
        aux_dynamic_prompt=[],
        index_entry_standard=True,
    )

    rendered = render_as_markdown(prompt)
    assert "# oracle and realization basic" not in rendered
    assert "# index entry standard" in rendered
    assert "# oracle standard" not in rendered
    assert "# realization standard" not in rendered


def test_complete_prompt_omits_index_entry_standard_by_default() -> None:
    """既定のcomplete promptがindex entry standardを含めないことを検証する。"""
    prompt = build_complete_prompt(
        summary="- summary",
        goal="- goal",
        file_access_mode=FileAccessMode.READONLY,
        path_context=_path_context(),
        aux_dynamic_prompt=[],
    )

    rendered = render_as_markdown(prompt)
    assert "index entry standard" not in rendered


def test_build_oracle_review_standard_renders_core_review_rules() -> None:
    """oracle review standardのseverityと所見境界がrenderされることを検証する。"""
    collection = _build_oracle_review_standard()

    assert isinstance(collection, StandardCollection)

    rendered = _render_standard_collection(collection)
    assert "oracle review standard" in rendered
    assert "fatal" in rendered
    assert "minor" in rendered
    assert "正本仕様断片同士に解釈の余地がない明確な矛盾" in rendered
    assert "実装者の裁量では解消不能" in rendered
    assert "誤字" in rendered
    assert "用語不統一" in rendered
    assert "oracle file だけから成立する問題を所見にする" in rendered
    assert "所見の列挙、統合、擁護理由列挙、反証理由列挙、および採否判定" in rendered


def test_complete_prompt_can_include_oracle_review_standard() -> None:
    """complete promptへoracle review standardを追加できることを検証する。"""
    prompt = build_complete_prompt(
        summary="- summary",
        goal="- goal",
        file_access_mode=FileAccessMode.READONLY,
        path_context=_path_context(),
        aux_dynamic_prompt=[],
        oracle_review_standard=True,
    )

    rendered = render_as_markdown(prompt)
    assert "# oracle and realization basic" in rendered
    assert "# oracle standard" in rendered
    assert "# oracle review standard" in rendered
    assert "# realization standard" not in rendered


def test_complete_prompt_omits_oracle_review_standard_by_default() -> None:
    """既定のcomplete promptがoracle review standardを含めないことを検証する。"""
    prompt = build_complete_prompt(
        summary="- summary",
        goal="- goal",
        file_access_mode=FileAccessMode.READONLY,
        path_context=_path_context(),
        aux_dynamic_prompt=[],
    )

    rendered = render_as_markdown(prompt)
    assert "oracle review standard" not in rendered
