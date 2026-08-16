"""prompt policy と complete prompt の組み立て結果を検証する。

各 prompt part の rendering と complete prompt の有効化・placeholder 展開は同じ
StructDoc 出力を共有する一つの責務であるため、prompt builder 回帰として一箇所に保つ。

対応する正本:
- {{work-root}}/oracle/doc/app_spec/prompt_policy.md
- {{work-root}}/oracle/doc/app_spec/feedback_observation.md
- {{work-root}}/oracle/src/oracle/prompt_builder/policy/basic.py
- {{work-root}}/oracle/src/oracle/prompt_builder/complete_prompt.py
- {{work-root}}/oracle/src/oracle/prompt_builder/policy/apply_review.py
- {{work-root}}/oracle/src/oracle/prompt_builder/policy/common.py
- {{work-root}}/oracle/src/oracle/prompt_builder/policy/conflict_resolution.py
- {{work-root}}/oracle/src/oracle/prompt_builder/policy/editor_handoff.py
- {{work-root}}/oracle/src/oracle/prompt_builder/policy/feedback_reporting.py
- {{work-root}}/oracle/src/oracle/prompt_builder/policy/file_access.py
- {{work-root}}/oracle/src/oracle/prompt_builder/policy/index_entry.py
- {{work-root}}/oracle/src/oracle/prompt_builder/parts/oracle_and_realization_basic.py
- {{work-root}}/oracle/src/oracle/prompt_builder/policy/oracle_review.py
- {{work-root}}/oracle/src/oracle/prompt_builder/policy/oracle.py
- {{work-root}}/oracle/src/oracle/prompt_builder/policy/realization_oracle_reference.py
- {{work-root}}/oracle/src/oracle/prompt_builder/policy/realization.py
- {{work-root}}/oracle/src/oracle/prompt_builder/policy/routing.py
- {{work-root}}/oracle/src/oracle/prompt_builder/policy/definitions.py
"""

from dataclasses import FrozenInstanceError
from pathlib import Path

import pytest
from _git_support import make_repo, run_git
from oracle.prompt_builder.complete_prompt import build_complete_prompt
from oracle.prompt_builder.policy.apply_review import (
    build_apply_review_policy as _build_apply_review_policy,
)
from oracle.prompt_builder.policy.basic import (
    Policy,
    PolicyCollection,
    PolicyGroup,
    combine_policy_collections,
    policy_collection_to_struct_docs,
)
from oracle.prompt_builder.policy.conflict_resolution import (
    build_conflict_resolution_policy as _build_conflict_resolution_policy,
)
from oracle.prompt_builder.policy.editor_handoff import (
    build_editor_handoff_policy as _build_editor_handoff_policy,
)
from oracle.prompt_builder.policy.file_access import (
    build_file_access_policy as _build_file_access_policy,
)
from oracle.prompt_builder.policy.index_entry import (
    build_index_entry_policy as _build_index_entry_policy,
)
from oracle.prompt_builder.policy.oracle import (
    build_oracle_investigation_policy as _build_oracle_investigation_policy,
)
from oracle.prompt_builder.policy.oracle import (
    build_oracle_policy as _build_oracle_policy,
)
from oracle.prompt_builder.policy.oracle_review import (
    build_oracle_review_policy as _build_oracle_review_policy,
)
from oracle.prompt_builder.policy.realization import (
    build_realization_policy as _build_realization_policy,
)
from oracle.prompt_builder.policy.realization_oracle_reference import (
    build_realization_oracle_reference_policy as _build_realization_oracle_reference_policy,
)
from oracle.prompt_builder.policy.routing import (
    build_routing_policy as _build_routing_policy,
)

from basic.acp import FileAccessMode
from basic.path_model import AgentCallPathContext
from basic.struct_doc import StructCodeBlock, StructDoc, render_as_markdown


def _path_context() -> AgentCallPathContext:
    """現在の test repository を起点に call-scoped path context を作る。"""
    return AgentCallPathContext(agent_call_cwd=Path.cwd())


def _render_policy_collection(collection: PolicyCollection) -> str:
    """PolicyCollection を complete prompt と同じ経路で render する。"""
    return render_as_markdown(policy_collection_to_struct_docs(collection))


def test_policy_values_are_immutable_and_require_meaningful_text() -> None:
    """Policy は入れ子の文面も固定し、空の規定を拒否する。"""
    policy = Policy(
        policy_id="sample.policy",
        title="sample",
        required=["required"],
        prohibited=["prohibited"],
    )

    assert policy.required == ("required",)
    assert policy.prohibited == ("prohibited",)
    with pytest.raises(FrozenInstanceError):
        setattr(policy, "title", "changed")
    with pytest.raises(ValueError, match="at least one requirement"):
        Policy(policy_id="empty.policy", title="empty")
    with pytest.raises(ValueError, match="non-empty strings"):
        Policy(
            policy_id="invalid.policy",
            title="invalid",
            required=("",),
        )


def test_policy_collection_renders_labels_without_internal_ids() -> None:
    """規定本文は label 順に render し、合成用 ID を prompt へ出さない。"""
    policy = Policy(
        policy_id="internal.policy-id",
        title="規定タイトル",
        required=("必須本文",),
        prohibited=("禁止本文",),
        recommended=("推奨本文",),
        permitted=("許容本文",),
        examples=("判断例本文",),
    )
    collection = PolicyCollection(
        groups=(
            PolicyGroup(
                group_id="internal.group-id",
                title="group title",
                scope="適用範囲",
                policies=(policy,),
            ),
        )
    )

    rendered = _render_policy_collection(collection)

    assert "# 規定タイトル（適用範囲）" in rendered
    labels = ("**必須**", "**禁止**", "**推奨**", "**許容**", "**判断例**")
    assert [rendered.index(label) for label in labels] == sorted(
        rendered.index(label) for label in labels
    )
    assert "internal.policy-id" not in rendered
    assert "internal.group-id" not in rendered


def test_combined_policy_collections_are_deduplicated_and_order_independent() -> None:
    """共有 Policy を一度だけ残し、builder の選択順から出力順を切り離す。"""
    realization = _build_realization_policy()
    apply_review = _build_apply_review_policy()

    forward = combine_policy_collections(realization, apply_review)
    reverse = combine_policy_collections(apply_review, realization)

    assert forward == reverse
    rendered = _render_policy_collection(forward)
    assert (
        rendered.count(
            "realization file の都合または挙動を根拠に oracle file の意味を変更"
        )
        == 1
    )
    assert rendered.index("oracle file を正本仕様断片として扱う") < rendered.index(
        "realization policy"
    )
    assert rendered.index("realization policy") < rendered.index(
        "所見・修正対象に具体的な根拠を求める"
    )


def test_combined_policy_collections_reject_conflicting_ids() -> None:
    """同じ ID に異なる Policy または group 定義を割り当てない。"""
    first_policy = Policy("shared.policy", "first", required=("body",))
    conflicting_policy = Policy("shared.policy", "conflicting", required=("body",))
    first = PolicyCollection(
        (PolicyGroup("group.first", "first group", "scope", (first_policy,)),)
    )
    conflicting = PolicyCollection(
        (
            PolicyGroup(
                "group.second",
                "second group",
                "scope",
                (conflicting_policy,),
            ),
        )
    )

    with pytest.raises(ValueError, match="Conflicting Policy definition"):
        combine_policy_collections(first, conflicting)

    conflicting_group = PolicyCollection(
        (
            PolicyGroup(
                "group.first",
                "conflicting group",
                "scope",
                (Policy("other.policy", "other", required=("body",)),),
            ),
        )
    )
    with pytest.raises(ValueError, match="Conflicting PolicyGroup definition"):
        combine_policy_collections(first, conflicting_group)


def test_oracle_policies_separate_investigation_from_editing_policies() -> None:
    """読み取り専用調査には、編集判断にだけ必要な規定を含めない。"""
    editing = _render_policy_collection(_build_oracle_policy())
    investigation = _render_policy_collection(_build_oracle_investigation_policy())

    for shared in (
        "oracle file を正本仕様断片として扱う",
        "判断根拠と installed skill の優先関係を守る",
        "実装から正本仕様を逆算しない",
    ):
        assert shared in editing
        assert shared in investigation
    assert "定義済みの事項と未定義の事項を区別する" in investigation
    for editing_only in (
        "realization file から oracle file へ意味を逆流させない",
        "一般論だけを根拠に oracle file の要求を変更しない",
        "重要な人間意図へ絞り、仕様の隙間を許容する",
        "実装上の制約は仕様の矛盾または実現不能の調査に限って使用する",
        "正本仕様断片の整合性と検索性を保つ",
    ):
        assert editing_only in editing
        assert editing_only not in investigation


def test_complete_prompt_can_include_oracle_investigation_policy() -> None:
    """調査用 Policy を基本定義とともに独立して注入する。"""
    prompt = build_complete_prompt(
        summary="- summary",
        goal="- goal",
        file_access_mode=FileAccessMode.PURE_ORACLE_READ,
        path_context=_path_context(),
        oracle_investigation_policy=True,
    )

    rendered = render_as_markdown(prompt)
    assert "# oracle and realization basic" in rendered
    assert "# oracle investigation policy" in rendered
    assert "# oracle policy" not in rendered
    assert "定義済みの事項と未定義の事項を区別する" in rendered


def test_build_apply_review_policy_renders_core_review_aspects() -> None:
    """apply review policy の主要な所見境界が render される。"""
    collection = _build_apply_review_policy()

    assert isinstance(collection, PolicyCollection)

    rendered = _render_policy_collection(collection)
    assert "apply review policy" in rendered
    assert "oracle file に対する realization file の追従要否" in rendered
    assert "明確な不適合または致命的な実装問題" in rendered
    assert "所見・修正対象に具体的な根拠を求める" in rendered
    assert "oracle file に記述がないこと、仕様の隙間" in rendered
    assert "調査開始時点ですでに解消されている問題" in rendered


def test_conflict_resolution_policy_is_injected_without_editing_policies() -> None:
    """conflict 解消には専用規定だけを編集規定として注入する。"""
    collection = _build_conflict_resolution_policy()
    rendered_doc = _render_policy_collection(collection)
    assert "`cmoc session join` の conflict marker 解消時だけ" in rendered_doc
    assert "conflict marker の解消に不要な仕様変更" in rendered_doc

    prompt = build_complete_prompt(
        summary="- summary",
        goal="- goal",
        file_access_mode=FileAccessMode.REPO_WRITE,
        path_context=_path_context(),
        conflict_resolution_policy=True,
    )
    rendered = render_as_markdown(prompt)
    assert "# oracle and realization basic" in rendered
    assert "# 両 branch の意味を保って conflict marker だけを解消する" in rendered
    for heading in (
        "# oracle policy",
        "# realization policy",
        "# oracle review policy",
        "# apply review policy",
    ):
        assert heading not in rendered


def test_editor_handoff_policy_preserves_call_responsibility() -> None:
    """handoff の追加でも元の access mode と正式な結果を維持する。"""
    collection = _build_editor_handoff_policy()
    rendered_doc = _render_policy_collection(collection)
    assert "editor handoff でも agent call の責務を維持する" in rendered_doc
    assert "file access mode と Codex CLI sandbox を維持する" in rendered_doc
    assert "正式な結果または成果物を満たす" in rendered_doc
    assert "対象 path と理由を限定した sandbox escalation" in rendered_doc

    prompt = build_complete_prompt(
        summary="- summary",
        goal="- goal",
        file_access_mode=FileAccessMode.PURE_ORACLE_READ,
        path_context=_path_context(),
        editor_handoff_policy=True,
    )
    rendered = render_as_markdown(prompt)
    assert "# oracle and realization basic" in rendered
    assert "editor handoff でも agent call の責務を維持する" in rendered
    assert "# oracle policy" not in rendered
    assert "# realization policy" not in rendered


def test_realization_oracle_reference_policy_is_independently_selectable() -> None:
    """oracle path コメント用 policy を realization policy と分離して注入する。"""
    doc = _build_realization_oracle_reference_policy(_path_context())[1]
    rendered_doc = render_as_markdown(doc)
    assert doc.title == "realization oracle reference policy"
    assert "realization code を作成または変更する場合" in rendered_doc
    assert "`{{work-root}}` 起点の oracle file path" in rendered_doc

    prompt = build_complete_prompt(
        summary="- summary",
        goal="- goal",
        file_access_mode=FileAccessMode.REALIZATION_WRITE,
        path_context=_path_context(),
        realization_oracle_reference_policy=True,
    )
    rendered = render_as_markdown(prompt)
    assert "# oracle and realization basic" in rendered
    assert "# realization oracle reference policy" in rendered
    assert "# oracle policy" not in rendered
    assert "# realization policy" not in rendered


def test_build_routing_policy_renders_core_reading_requirements() -> None:
    """routing policy が INDEX 案内の主要な見出しを render することを検証する。"""
    doc = _build_routing_policy(_path_context())[1]

    assert isinstance(doc, StructDoc)
    assert doc.title == "routing policy"

    rendered = render_as_markdown(doc)
    assert "INDEX.md" in rendered
    assert "Summary" in rendered
    assert "Read this when" in rendered
    assert "Do not read this when" in rendered
    assert "必要な本文を読む" in rendered
    assert "総当たりで読む前" in rendered


def test_complete_prompt_controls_routing_policy_explicitly() -> None:
    """repository 参照の有無に応じて routing policy を選択する。"""
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
        routing_policy=True,
    )

    assert "# routing policy" not in render_as_markdown(default_prompt)
    assert "# routing policy" in render_as_markdown(repository_prompt)


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
    assert "現在の workload だけでは解消できず" in rendered
    assert "外部挙動を左右する人間意図の確定" in rendered
    assert "通常の workload 内で解決した問題" in rendered


def test_complete_prompt_renders_file_classification_boundaries() -> None:
    """基本定義が exact root と owning repository の分類境界を伝える。"""
    prompt = build_complete_prompt(
        summary="- summary",
        goal="- goal",
        file_access_mode=FileAccessMode.READONLY,
        path_context=_path_context(),
        oracle_and_realization_basic=True,
    )

    rendered = render_as_markdown(prompt)
    for expected in (
        "nested の同名 path は、名前だけで対象外にしない",
        "nested Git working tree の `.git` path",
        "最内側の検証済み Git working tree を owning repository とする",
        "tracked な regular file は、ignore pattern に一致しても分類対象に含める",
        "untracked かつ ignored な regular file だけとする",
    ):
        assert expected in rendered


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


def test_file_access_policy_titles_and_bodies_match_modes() -> None:
    """各 file access mode に対応する policy の内容を検証する。"""
    mode_specific_denials = {
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
    all_mode_specific_denials = set().union(*mode_specific_denials.values())
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
        doc = _build_file_access_policy(mode, _path_context())[1]
        rendered = render_as_markdown(doc)
        assert doc.title == f"file read write policy - {mode.value}"
        for fragment in fragments:
            assert fragment in rendered
        for fragment in all_mode_specific_denials - mode_specific_denials[mode]:
            assert fragment not in rendered


def test_file_access_policy_uses_root_specific_deny_lists(
    tmp_path: Path,
) -> None:
    """main と linked worktree の各 path context に deny-list を構築する。"""
    root = make_repo(tmp_path)
    main_context = AgentCallPathContext(agent_call_cwd=root)
    main_rendered = render_as_markdown(
        _build_file_access_policy(FileAccessMode.REPO_WRITE, main_context)[1]
    )
    assert "`{{repo-root}}` ツリー外は読み書き禁止" in main_rendered
    assert "`{{repo-root}}/.cmoc/g*/ar` ツリー内は書き込み禁止" not in main_rendered

    linked = root / ".cmoc" / "gu" / "worktree" / "linked"
    run_git(root, "worktree", "add", "-b", "prompt-parts-linked", str(linked), "HEAD")
    linked_context = AgentCallPathContext(agent_call_cwd=linked)
    linked_rendered = render_as_markdown(
        _build_file_access_policy(FileAccessMode.REPO_WRITE, linked_context)[1]
    )
    assert (
        "`{{work-root}}` ツリー外かつ `{{repo-root}}/.cmoc/g*/ar` ツリー外は読み書き禁止"
        in linked_rendered
    )
    assert "`{{repo-root}}/.cmoc/g*/ar` ツリー内は書き込み禁止" in linked_rendered
    assert "例外的に `{{repo-root}}/.cmoc/g*/ar` ツリー内は読み込み可能" not in (
        linked_rendered
    )


def test_no_policy_complete_prompt_omits_file_access_policy() -> None:
    """NO_POLICY 時に file access policy を挿入しないことを検証する。"""
    prompt = build_complete_prompt(
        summary="summary",
        goal="goal",
        file_access_mode=FileAccessMode.NO_POLICY,
        path_context=_path_context(),
    )
    rendered = render_as_markdown(prompt)

    assert "file read write policy" not in rendered


def test_complete_prompt_can_include_apply_review_policy() -> None:
    """complete promptへapply review policyを追加できることを検証する。"""
    prompt = build_complete_prompt(
        summary="- summary",
        goal="- goal",
        file_access_mode=FileAccessMode.READONLY,
        path_context=_path_context(),
        aux_dynamic_prompt=[],
        apply_review_policy=True,
    )

    rendered = render_as_markdown(prompt)
    assert "# oracle and realization basic" in rendered
    assert "# oracle policy" in rendered
    assert "# realization policy" in rendered
    assert "# apply review policy" in rendered


def test_complete_prompt_preserves_injected_policy_terms() -> None:
    """complete promptが注入した各policyの主要語とplaceholderを保持することを検証する。"""
    prompt = build_complete_prompt(
        summary="- summary",
        goal="- goal",
        file_access_mode=FileAccessMode.READONLY,
        path_context=_path_context(),
        aux_dynamic_prompt=[],
        oracle_policy=True,
        realization_policy=True,
        oracle_review_policy=True,
        apply_review_policy=True,
        conflict_resolution_policy=True,
        realization_oracle_reference_policy=True,
        index_entry_policy=True,
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
        "oracle policy",
        "realization policy",
        "oracle review policy",
        "apply review policy",
        "両 branch の意味を保って conflict marker だけを解消する",
        "realization oracle reference policy",
        "index entry policy",
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
        goal="- realization policy と oracle policy に従うこと",
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

    assert "- realization policy と oracle policy に従うこと" in rendered
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
    """literal work-root token と oracle 参照コメント要求を prompt に残す。"""
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
        realization_policy=True,
        realization_oracle_reference_policy=True,
    )

    rendered = render_as_markdown(prompt)

    assert "- {{work-root}}/src/app.py を確認すること" in rendered
    assert (
        "realization code のコメントに `{{work-root}}` 起点の oracle file path を書く"
        in rendered
    )
    assert f"- {{{{work-root}}}} = {repo_root}" in rendered


def test_complete_prompt_omits_apply_review_policy_by_default() -> None:
    """既定のcomplete promptがapply review policyを含めないことを検証する。"""
    prompt = build_complete_prompt(
        summary="- summary",
        goal="- goal",
        file_access_mode=FileAccessMode.READONLY,
        path_context=_path_context(),
        aux_dynamic_prompt=[],
    )

    rendered = render_as_markdown(prompt)
    assert "apply review policy" not in rendered


def test_build_realization_policy_renders_core_conformance_requirements() -> None:
    """realization policy の適合性と検証境界が render される。"""
    collection = _build_realization_policy()

    assert isinstance(collection, PolicyCollection)

    rendered = _render_policy_collection(collection)
    assert "realization policy" in rendered
    assert "realization file を現行の oracle file に適合させる" in rendered
    assert "現行仕様に必要な実装だけを保つ" in rendered
    assert "対象 repository 固有の手順で変更を検証する" in rendered
    assert "配置場所にかかわらず特定" in rendered
    assert "`.agents/skills` に限定" in rendered


def test_complete_prompt_can_include_realization_policy() -> None:
    """complete promptへrealization policyを追加できることを検証する。"""
    prompt = build_complete_prompt(
        summary="- summary",
        goal="- goal",
        file_access_mode=FileAccessMode.READONLY,
        path_context=_path_context(),
        aux_dynamic_prompt=[],
        realization_policy=True,
    )

    rendered = render_as_markdown(prompt)
    assert "# oracle policy" in rendered
    assert "# realization policy" in rendered
    assert "対象 repository 固有の手順で変更を検証する" in rendered
    assert "# realization oracle reference policy" not in rendered


def test_build_index_entry_policy_renders_core_output_requirements() -> None:
    """index entry policyの出力境界がrenderされることを検証する。"""
    collection = _build_index_entry_policy()

    assert isinstance(collection, PolicyCollection)

    rendered = _render_policy_collection(collection)
    assert "index entry policy" in rendered
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


def test_complete_prompt_can_include_index_entry_policy() -> None:
    """complete promptへindex entry policyを追加できることを検証する。"""
    prompt = build_complete_prompt(
        summary="- summary",
        goal="- goal",
        file_access_mode=FileAccessMode.READONLY,
        path_context=_path_context(),
        aux_dynamic_prompt=[],
        index_entry_policy=True,
    )

    rendered = render_as_markdown(prompt)
    assert "# oracle and realization basic" not in rendered
    assert "# index entry policy" in rendered
    assert "# oracle policy" not in rendered
    assert "# realization policy" not in rendered


def test_complete_prompt_omits_index_entry_policy_by_default() -> None:
    """既定のcomplete promptがindex entry policyを含めないことを検証する。"""
    prompt = build_complete_prompt(
        summary="- summary",
        goal="- goal",
        file_access_mode=FileAccessMode.READONLY,
        path_context=_path_context(),
        aux_dynamic_prompt=[],
    )

    rendered = render_as_markdown(prompt)
    assert "index entry policy" not in rendered


def test_build_oracle_review_policy_renders_core_review_requirements() -> None:
    """oracle review policyのseverityと所見境界がrenderされることを検証する。"""
    collection = _build_oracle_review_policy()

    assert isinstance(collection, PolicyCollection)

    rendered = _render_policy_collection(collection)
    assert "oracle review policy" in rendered
    assert "fatal" in rendered
    assert "minor" in rendered
    assert "正本仕様断片同士に解釈の余地がない明確な矛盾" in rendered
    assert "実装者の裁量では解消不能" in rendered
    assert "誤字" in rendered
    assert "用語不統一" in rendered
    assert "oracle file だけから成立する問題を所見にする" in rendered
    assert "所見の列挙、統合、擁護理由列挙、反証理由列挙、および採否判定" in rendered


def test_complete_prompt_can_include_oracle_review_policy() -> None:
    """complete promptへoracle review policyを追加できることを検証する。"""
    prompt = build_complete_prompt(
        summary="- summary",
        goal="- goal",
        file_access_mode=FileAccessMode.READONLY,
        path_context=_path_context(),
        aux_dynamic_prompt=[],
        oracle_review_policy=True,
    )

    rendered = render_as_markdown(prompt)
    assert "# oracle and realization basic" in rendered
    assert "# oracle policy" in rendered
    assert "# oracle review policy" in rendered
    assert "# realization policy" not in rendered


def test_complete_prompt_omits_oracle_review_policy_by_default() -> None:
    """既定のcomplete promptがoracle review policyを含めないことを検証する。"""
    prompt = build_complete_prompt(
        summary="- summary",
        goal="- goal",
        file_access_mode=FileAccessMode.READONLY,
        path_context=_path_context(),
        aux_dynamic_prompt=[],
    )

    rendered = render_as_markdown(prompt)
    assert "oracle review policy" not in rendered
