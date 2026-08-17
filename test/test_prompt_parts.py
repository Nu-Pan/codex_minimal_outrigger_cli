"""prompt policy と complete prompt の組み立て結果を検証する。

各 prompt part の rendering と complete prompt の有効化・placeholder 展開は同じ
StructDoc 出力を共有する一つの責務であるため、prompt builder 回帰として一箇所に保つ。

対応する正本:
- {{work-root}}/oracle/doc/app_spec/prompt_policy.md
- {{work-root}}/oracle/doc/app_spec/feedback_observation.md
- {{work-root}}/oracle/src/oracle/other/struct_doc.py
- {{work-root}}/oracle/src/oracle/prompt_builder/basic.py
- {{work-root}}/oracle/src/oracle/prompt_builder/complete_prompt.py
- {{work-root}}/oracle/src/oracle/prompt_builder/policy/apply_review.py
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
"""

from collections.abc import Callable
from pathlib import Path

import pytest
from _git_support import make_repo, run_git
from oracle.prompt_builder.basic import PlaceholderMap
from oracle.prompt_builder.complete_prompt import build_complete_prompt
from oracle.prompt_builder.policy.apply_review import (
    build_apply_review_policy as _build_apply_review_policy,
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


def _render_policy(builder_result: tuple[PlaceholderMap, StructDoc]) -> str:
    """policy builder の StructDoc を complete prompt と同じ経路で render する。"""
    return render_as_markdown(builder_result[1])


@pytest.mark.parametrize(
    ("builder", "categories"),
    [
        pytest.param(
            _build_oracle_policy,
            ("**必須**", "**禁止**", "**許容**"),
            id="oracle",
        ),
        pytest.param(
            _build_oracle_investigation_policy,
            ("**必須**", "**禁止**"),
            id="oracle-investigation",
        ),
        pytest.param(
            _build_realization_policy,
            ("**必須**", "**禁止**"),
            id="realization",
        ),
        pytest.param(
            _build_oracle_review_policy,
            ("**必須**", "**禁止**"),
            id="oracle-review",
        ),
        pytest.param(
            _build_apply_review_policy,
            ("**必須**", "**禁止**"),
            id="apply-review",
        ),
        pytest.param(
            _build_conflict_resolution_policy,
            ("**必須**", "**禁止**"),
            id="conflict-resolution",
        ),
        pytest.param(
            _build_editor_handoff_policy,
            ("**必須**", "**許容**"),
            id="editor-handoff",
        ),
        pytest.param(
            _build_index_entry_policy,
            ("**必須**", "**禁止**"),
            id="index-entry",
        ),
    ],
)
def test_category_policy_blocks_are_flat_and_keep_category_order(
    builder: Callable[[], tuple[PlaceholderMap, StructDoc]],
    categories: tuple[str, ...],
) -> None:
    """カテゴリ付き policy block は一つの見出しと順序付きカテゴリだけを持つ。"""
    rendered = _render_policy(builder())
    lines = rendered.splitlines()

    assert len([line for line in lines if line.startswith("# ")]) == 1
    assert not any(line.startswith("## ") for line in lines)
    assert [
        line for line in lines if line in {"**必須**", "**禁止**", "**許容**"}
    ] == list(categories)


_POLICY_FLAG_HEADINGS = (
    ("oracle_and_realization_basic", "# oracle and realization basic"),
    ("oracle_policy", "# oracle policy"),
    ("oracle_investigation_policy", "# oracle investigation policy"),
    ("realization_policy", "# realization policy"),
    ("oracle_review_policy", "# oracle review policy"),
    ("apply_review_policy", "# apply review policy"),
    ("conflict_resolution_policy", "# conflict resolution policy"),
    ("editor_handoff_policy", "# editor handoff policy"),
    (
        "realization_oracle_reference_policy",
        "# realization oracle reference policy",
    ),
    ("index_entry_policy", "# index entry policy"),
    ("routing_policy", "# routing policy"),
)


@pytest.mark.parametrize(("selected_flag", "selected_heading"), _POLICY_FLAG_HEADINGS)
def test_each_policy_flag_adds_only_its_block_once(
    selected_flag: str,
    selected_heading: str,
) -> None:
    """各 flag は対応する policy block だけを一度追加する。"""
    prompt = build_complete_prompt(
        summary="- summary",
        goal="- goal",
        file_access_mode=FileAccessMode.READONLY,
        path_context=_path_context(),
        **{selected_flag: True},
    )

    rendered = render_as_markdown(prompt)
    for _, heading in _POLICY_FLAG_HEADINGS:
        assert rendered.count(heading) == (1 if heading == selected_heading else 0)


def test_selected_policy_blocks_remain_separate_without_deduplication() -> None:
    """選択した policy block は共有文面を削らず、それぞれ一度だけ注入する。"""
    prompt = build_complete_prompt(
        summary="- summary",
        goal="- goal",
        file_access_mode=FileAccessMode.READONLY,
        path_context=_path_context(),
        realization_policy=True,
        apply_review_policy=True,
    )

    rendered = render_as_markdown(prompt)
    assert (
        rendered.count(
            "realization file の都合または挙動を根拠に oracle file の意味を変更"
        )
        == 2
    )
    assert rendered.index("# realization policy") < rendered.index(
        "# apply review policy"
    )


def test_oracle_policies_separate_investigation_from_editing_policies() -> None:
    """読み取り専用調査には、編集判断にだけ必要な規定を含めない。"""
    editing = _render_policy(_build_oracle_policy())
    investigation = _render_policy(_build_oracle_investigation_policy())

    for shared in (
        "oracle authority policy（oracle・realization file を扱う時）",
        "判断の根拠を関連する oracle file に置く",
        "realization file または実装だけから正本仕様を逆算してはいけない",
    ):
        assert shared in editing
        assert shared in investigation
    assert "oracle file で定義されている事項と未定義の事項を区別する" in (investigation)
    for editing_only in (
        "realization file の都合または挙動を根拠に oracle file の意味を変更",
        "一般的なベストプラクティスだけを根拠に oracle file の要求を変更",
        "仕様全体を網羅するためだけの分類、列挙、説明を追加",
        "正本仕様の矛盾または実現不能を調べる場合に限り",
        "一般方針と個別仕様の優先関係を読み取れるようにする",
    ):
        assert editing_only in editing
        assert editing_only not in investigation


def test_build_apply_review_policy_renders_core_review_aspects() -> None:
    """apply review policy の主要な所見境界が render される。"""
    builder_result = _build_apply_review_policy()

    assert isinstance(builder_result[1], StructDoc)

    rendered = _render_policy(builder_result)
    assert "apply review policy" in rendered
    assert "oracle file に対する realization file の追従要否" in rendered
    assert "oracle file の具体的な要求と realization file の具体的な挙動" in rendered
    assert "realization file だけから実行不能または明白な致命的バグ" in rendered
    assert "finding basis policy（所見・修正対象の判断時）" in rendered
    assert "oracle file に記述がないこと、仕様の隙間" in rendered
    assert "調査開始時点ですでに解消されている問題" in rendered


def test_conflict_resolution_policy_preserves_both_sides() -> None:
    """conflict 解消 policy が両側の意味を保つ境界を伝える。"""
    builder_result = _build_conflict_resolution_policy()
    rendered_doc = _render_policy(builder_result)
    assert "`cmoc session join` の conflict marker 解消時だけ" in rendered_doc
    assert "conflict 対象の両側と関連する oracle file を読み" in rendered_doc
    assert "conflict marker の解消に不要な仕様変更" in rendered_doc


def test_editor_handoff_policy_preserves_call_responsibility() -> None:
    """handoff の追加でも元の access mode と正式な結果を維持する。"""
    builder_result = _build_editor_handoff_policy()
    rendered_doc = _render_policy(builder_result)
    assert "editor handoff でも、agent call に選択された" in rendered_doc
    assert "file access mode と Codex CLI sandbox を維持する" in rendered_doc
    assert "正式な結果または成果物を満たす" in rendered_doc
    assert "対象 path と理由を限定した sandbox escalation" in rendered_doc


def test_realization_oracle_reference_policy_is_independently_selectable() -> None:
    """oracle path コメント用 policy を realization policy と分離して注入する。"""
    doc = _build_realization_oracle_reference_policy(_path_context())[1]
    rendered_doc = render_as_markdown(doc)
    assert doc.title == (
        "realization oracle reference policy（realization code の作成・変更時）"
    )
    assert "対応する oracle file が存在する場合" in rendered_doc
    assert "`{{work-root}}` 起点の oracle file path" in rendered_doc


def test_build_routing_policy_renders_core_reading_requirements() -> None:
    """routing policy が INDEX 案内の主要な見出しを render することを検証する。"""
    doc = _build_routing_policy(_path_context())[1]

    assert isinstance(doc, StructDoc)
    assert doc.title == "routing policy"

    rendered = render_as_markdown(doc)
    assert "INDEX.md" in rendered
    assert "どのファイル・ディレクトリを読むべきか判断・特定" in rendered
    assert "作業対象に近い階層の `INDEX.md` を起点" in rendered
    assert "内容が食い違う場合は本文を優先" in rendered
    assert "本文の代替にせず、必ず本文を判断の根拠" in rendered


def test_complete_prompt_orders_static_objective_and_dynamic_sections() -> None:
    """完全 prompt は固定部から動的部へ並べ、summary と goal を objective に置く。"""
    prompt = build_complete_prompt(
        summary="- あなたは prompt 検証担当です\n- 対象 prompt を確認すること",
        goal="- prompt の参照関係が妥当であること",
        file_access_mode=FileAccessMode.READONLY,
        path_context=_path_context(),
        aux_static_prompt=[StructDoc("caller static", "- static")],
        aux_dynamic_prompt=[StructDoc("caller dynamic", "- dynamic")],
        oracle_policy=True,
    )

    rendered = render_as_markdown(prompt)
    assert '<cmoc_ref target="fundamental_policy"/>' in rendered
    assert '<cmoc_ref target="objective"/>' in rendered
    objective = rendered.split('<cmoc_block id="objective">', 1)[1].split(
        "</cmoc_block>", 1
    )[0]
    assert "# summary\n\n- あなたは prompt 検証担当です" in objective
    assert "- 対象 prompt を確認すること" in objective
    assert "# goal\n\n- prompt の参照関係が妥当であること" in objective
    assert '<cmoc_ref target="role"/>' not in rendered
    assert '<cmoc_block id="role">' not in rendered
    markers = (
        "# プロンプト内の重要な情報",
        '<cmoc_block id="fundamental_policy">',
        "# oracle policy",
        "# caller static",
        '<cmoc_block id="objective">',
        "# caller dynamic",
        "# place holder definition",
    )
    positions = [rendered.index(marker) for marker in markers]
    assert positions == sorted(positions)


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
    assert "このセッションの規定内では解決できなかった問題" in rendered
    assert "セッション内で解決した問題" in rendered
    assert "仕様どおりの制約" in rendered
    assert "具体的な根拠がない改善案" in rendered
    assert "成功・失敗を根拠にセッションを中断・続行を判断してはならない" in (rendered)


def test_complete_prompt_renders_file_classification_boundaries() -> None:
    """基本定義が三分類と owning repository の判定境界を伝える。"""
    prompt = build_complete_prompt(
        summary="- summary",
        goal="- goal",
        file_access_mode=FileAccessMode.READONLY,
        path_context=_path_context(),
        oracle_and_realization_basic=True,
    )

    rendered = render_as_markdown(prompt)
    for expected in (
        "# uncategorised file",
        "以下の条件をすべて満たすものを oracle file とする",
        "以下の条件をすべて満たすものを realization file とする",
        "uncategorised file ではない",
        "`{{work-root}}/oracle` ツリー外である",
        "名前を持つファイルはすべて uncategorised file",
        "git 未追跡である",
        "git ignore 判定で無視される",
        "最も内側の git repository を owning repository",
        "git -C <owning-repository-root> check-ignore --quiet",
        "実際に git repository metadata である",
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
        assert doc.title == f"file R/W policy ({mode.value})"
        assert "以上のルールで禁止されていない読み書きは暗黙に許可される" in (rendered)
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

    assert "file R/W policy" not in rendered


def test_complete_prompt_preserves_injected_policy_terms() -> None:
    """complete promptが注入した各policyの主要語とplaceholderを保持することを検証する。"""
    prompt = build_complete_prompt(
        summary="- summary",
        goal="- goal",
        file_access_mode=FileAccessMode.READONLY,
        path_context=_path_context(),
        aux_dynamic_prompt=[],
        oracle_and_realization_basic=True,
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
    assert "現行仕様を満たすために必要な implementation" in rendered
    assert "列挙、統合、擁護理由列挙、反証理由列挙、および採否判定" in rendered
    assert "conflict 対象の両側と関連する oracle file を読み" in rendered
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
        "conflict resolution policy",
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


def test_build_realization_policy_renders_core_conformance_requirements() -> None:
    """realization policy の適合性と検証境界が render される。"""
    builder_result = _build_realization_policy()

    assert isinstance(builder_result[1], StructDoc)

    rendered = _render_policy(builder_result)
    assert "realization policy" in rendered
    assert "関連する oracle file を先に確認し、その明示要求と矛盾しない" in rendered
    assert "現行仕様を満たすために必要な implementation" in rendered
    assert "対象 repository で追跡されている関連手順" in rendered
    assert "配置場所にかかわらず特定" in rendered
    assert "`.agents/skills` に限定" in rendered


def test_build_index_entry_policy_renders_core_output_requirements() -> None:
    """index entry policyの出力境界がrenderされることを検証する。"""
    builder_result = _build_index_entry_policy()

    assert isinstance(builder_result[1], StructDoc)

    rendered = _render_policy(builder_result)
    assert "index entry policy" in rendered
    assert "INDEX.md エントリーのルーティング情報" in rendered
    assert "対象内容から根拠を持って言える責務・入口・読む条件" in rendered
    assert "機械的に補える情報" in rendered
    assert "対象が担う責務と、同階層の他対象ではなくその対象へ進む理由" in rendered
    assert "ファイル名・ディレクトリ名・ハッシュ値" in rendered
    assert "Structured Output schema を読めば分かる出力項目名・型・形式" in rendered
    assert "関連しそうという理由だけ" in rendered
    assert "summary" not in rendered
    assert "read_this_when" not in rendered
    assert "do_not_read_this_when" not in rendered


def test_build_oracle_review_policy_renders_core_review_requirements() -> None:
    """oracle review policyのseverityと所見境界がrenderされることを検証する。"""
    builder_result = _build_oracle_review_policy()

    assert isinstance(builder_result[1], StructDoc)

    rendered = _render_policy(builder_result)
    assert "oracle review policy" in rendered
    assert "fatal" in rendered
    assert "minor" in rendered
    assert "正本仕様断片同士に解釈の余地がない明確な矛盾" in rendered
    assert "実装者の裁量では解消不能" in rendered
    assert "誤字" in rendered
    assert "用語不統一" in rendered
    assert "oracle file だけから成立する所見について" in rendered
    assert "列挙、統合、擁護理由列挙、反証理由列挙、および採否判定" in rendered
