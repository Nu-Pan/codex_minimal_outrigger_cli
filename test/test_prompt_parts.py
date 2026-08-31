"""prompt part と complete prompt の組み立て結果を検証する。

各 prompt part の rendering と complete prompt の有効化・placeholder 展開は同じ
SDHeader 出力を共有する一つの責務であるため、prompt builder 回帰として一箇所に保つ。

対応する正本:
- {{work-root}}/oracle/doc/app_spec/codex_exec_rule.md
- {{work-root}}/oracle/doc/app_spec/feedback_observation.md
- {{work-root}}/oracle/src/oracle/other/struct_doc.py
- {{work-root}}/oracle/src/oracle/prompt_builder/basic.py
- {{work-root}}/oracle/src/oracle/prompt_builder/complete_prompt.py
- {{work-root}}/oracle/src/oracle/prompt_builder/policy/conflict_resolution.py
- {{work-root}}/oracle/src/oracle/prompt_builder/policy/feedback_reporting.py
- {{work-root}}/oracle/src/oracle/prompt_builder/policy/file_access.py
- {{work-root}}/oracle/src/oracle/prompt_builder/policy/index_entry.py
- {{work-root}}/oracle/src/oracle/prompt_builder/parts/oracle_and_realization_basic.py
- {{work-root}}/oracle/src/oracle/prompt_builder/policy/oracle_findings.py
- {{work-root}}/oracle/src/oracle/prompt_builder/policy/oracle.py
- {{work-root}}/oracle/src/oracle/prompt_builder/policy/realization_findings.py
- {{work-root}}/oracle/src/oracle/prompt_builder/policy/realization.py
- {{work-root}}/oracle/src/oracle/prompt_builder/policy/routing.py
"""

from collections.abc import Callable
from pathlib import Path

import pytest
from _git_support import make_repo, run_git
from oracle.other.struct_doc import (
    SDCodeBlock,
    SDHeader,
    SDPolicy,
    render_sd_node_as_markdown,
)
from oracle.prompt_builder.basic import PlaceholderMap
from oracle.prompt_builder.complete_prompt import build_complete_prompt
from oracle.prompt_builder.policy.conflict_resolution import (
    build_conflict_resolution_policy as _build_conflict_resolution_policy,
)
from oracle.prompt_builder.policy.editor_input_handoff import (
    build_editor_input_handoff_policy as _build_editor_input_handoff_policy,
)
from oracle.prompt_builder.policy.feedback_reporting import (
    build_feedback_reporting_policy as _build_feedback_reporting_policy,
)
from oracle.prompt_builder.policy.file_access import (
    build_file_access_policy as _build_file_access_policy,
)
from oracle.prompt_builder.policy.index_entry import (
    build_index_entry_policy as _build_index_entry_policy,
)
from oracle.prompt_builder.policy.oracle import (
    build_oracle_policy as _build_oracle_policy,
)
from oracle.prompt_builder.policy.oracle_findings import (
    build_oracle_findings_policy as _build_oracle_findings_policy,
)
from oracle.prompt_builder.policy.realization import (
    build_realization_policy as _build_realization_policy,
)
from oracle.prompt_builder.policy.realization_findings import (
    build_realization_findings_policy as _build_realization_findings_policy,
)
from oracle.prompt_builder.policy.routing import (
    build_routing_policy as _build_routing_policy,
)

from basic.acp import FileAccessMode
from basic.path_model import AgentCallPathContext


def _path_context() -> AgentCallPathContext:
    """現在の test repository を起点に call-scoped path context を作る。"""
    return AgentCallPathContext(agent_call_cwd=Path.cwd())


def _render_policy(builder_result: tuple[PlaceholderMap, SDHeader]) -> str:
    """policy builder の SDHeader を complete prompt と同じ経路で render する。"""
    return render_sd_node_as_markdown(builder_result[1])


@pytest.mark.parametrize(
    ("builder", "categories", "policy_count"),
    [
        pytest.param(
            _build_oracle_policy,
            (
                "**必須**",
                "**禁止**",
                "**許容**",
                "**補足情報**",
                "**必須**",
                "**禁止**",
            ),
            2,
            id="oracle",
        ),
        pytest.param(
            lambda: _build_realization_policy(_path_context()),
            ("**必須**", "**禁止**", "**許容**"),
            1,
            id="realization",
        ),
        pytest.param(
            _build_oracle_findings_policy,
            ("**必須**", "**禁止**"),
            1,
            id="oracle-findings",
        ),
        pytest.param(
            _build_realization_findings_policy,
            ("**必須**", "**禁止**"),
            1,
            id="realization-findings",
        ),
        pytest.param(
            _build_conflict_resolution_policy,
            ("**必須**", "**禁止**"),
            1,
            id="conflict-resolution",
        ),
        pytest.param(
            lambda: _build_feedback_reporting_policy(_path_context()),
            ("**必須**", "**禁止**"),
            1,
            id="feedback-reporting",
        ),
        pytest.param(
            _build_editor_input_handoff_policy,
            ("**必須**", "**禁止**"),
            1,
            id="editor-input-handoff",
        ),
        pytest.param(
            lambda: _build_file_access_policy(FileAccessMode.READONLY, _path_context()),
            ("**禁止**", "**許容**"),
            1,
            id="file-access",
        ),
        pytest.param(
            _build_index_entry_policy,
            ("**必須**", "**禁止**"),
            1,
            id="index-entry",
        ),
        pytest.param(
            lambda: _build_routing_policy(_path_context()),
            ("**必須**", "**補足情報**"),
            1,
            id="routing",
        ),
    ],
)
def test_category_policy_blocks_are_flat_and_keep_category_order(
    builder: Callable[[], tuple[PlaceholderMap, SDHeader]],
    categories: tuple[str, ...],
    policy_count: int,
) -> None:
    """全 policy builder が flat な SDPolicy と順序付きカテゴリだけを持つ。"""
    builder_result = builder()
    policy_header = builder_result[1]
    assert len(policy_header.children) == policy_count
    assert all(isinstance(child, SDPolicy) for child in policy_header.children)

    rendered = _render_policy(builder_result)
    lines = rendered.splitlines()

    assert len([line for line in lines if line.startswith("# ")]) == 1
    assert not any(line.startswith("## ") for line in lines)
    assert [
        line
        for line in lines
        if line in {"**必須**", "**禁止**", "**許容**", "**補足情報**"}
    ] == list(categories)


_POLICY_FLAG_HEADINGS = (
    ("oracle_and_realization_basic", "# oracle and realization basic"),
    ("oracle_policy", "# oracle policy"),
    ("realization_policy", "# realization policy"),
    ("oracle_findings_policy", "# oracle findings policy"),
    ("realization_findings_policy", "# realization findings policy"),
    ("conflict_resolution_policy", "# conflict resolution policy"),
    ("index_entry_policy", "# index entry policy"),
    ("routing_policy", "# routing policy"),
    ("editor_input_handoff_policy", "# editor input handoff"),
)


@pytest.mark.parametrize(("selected_flag", "selected_heading"), _POLICY_FLAG_HEADINGS)
def test_each_policy_flag_adds_only_its_block_once(
    selected_flag: str,
    selected_heading: str,
) -> None:
    """各 flag は対応する policy block だけを一度追加する。"""
    prompt = build_complete_prompt(
        task="- task",
        file_access_mode=FileAccessMode.READONLY,
        path_context=_path_context(),
        **{selected_flag: True},
    )

    rendered = render_sd_node_as_markdown(*prompt)
    for _, heading in _POLICY_FLAG_HEADINGS:
        assert rendered.count(heading) == (1 if heading == selected_heading else 0)


def test_selected_policy_blocks_remain_separate_without_deduplication() -> None:
    """選択した policy block は共有文面を削らず、それぞれ一度だけ注入する。"""
    prompt = build_complete_prompt(
        task="- task",
        file_access_mode=FileAccessMode.READONLY,
        path_context=_path_context(),
        oracle_findings_policy=True,
        realization_findings_policy=True,
    )

    rendered = render_sd_node_as_markdown(*prompt)
    assert rendered.count("oracle file の具体的な記述だけから成立する問題") == 1
    assert (
        rendered.count(
            "所見は oracle file, realization file の記述・挙動を根拠として持つ"
        )
        == 1
    )
    assert rendered.index("# oracle findings policy") < rendered.index(
        "# realization findings policy"
    )


def test_oracle_policy_keeps_reference_and_authority_boundaries() -> None:
    """oracle policy が参照形式、正本責務、未定義事項を区別する。"""
    rendered = _render_policy(_build_oracle_policy())

    assert "root path placeholder を起点とする path、安定した locator" in rendered
    assert "合わせて読む必要がある oracle file への参照に行番号を含めてはいけない" in (
        rendered
    )
    assert (
        "oracle doc は意味仕様を所有し、oracle src は oracle doc から明示的に委譲"
        in (rendered)
    )
    assert "同じ仕様事項の正本所有者は一つだけ" in rendered
    assert "仕様断片上定義されている事項と、未定義の事項とを区別する" in rendered
    assert "正本仕様断片の隙間の未定義事項を正本仕様として断定" in rendered
    assert "oracle investigation policy" not in rendered


def test_build_realization_findings_policy_renders_core_review_aspects() -> None:
    """realization findings policy の主要な所見境界が render される。"""
    builder_result = _build_realization_findings_policy()

    assert isinstance(builder_result[1], SDHeader)

    rendered = _render_policy(builder_result)
    assert "realization findings policy" in rendered
    assert "oracle file の具体的な要求と realization file の具体的な挙動" in rendered
    assert "realization file 上に明確に存在する致命的な問題" in rendered
    assert "oracle file 自体の問題" in rendered
    assert "規定上必須とされていない事" in rendered
    assert "調査開始時点ですでに解消されている問題" in rendered


def test_conflict_resolution_policy_renders_merge_result_requirements() -> None:
    """conflict 解消結果の保持・報告・変更境界を伝える。"""
    builder_result = _build_conflict_resolution_policy()
    rendered_doc = _render_policy(builder_result)
    assert "merge conflict を解決した結果が満たすべき規定" in rendered_doc
    assert "両方のマージ元ブランチの oracle file" in rendered_doc
    assert "意味を両立できる解決方法が無い場合" in rendered_doc
    assert "realization file の都合または挙動を根拠に" in rendered_doc
    assert "conflict marker の解消に対して不必要な変更" in rendered_doc


def test_build_routing_policy_renders_core_reading_requirements() -> None:
    """routing policy が INDEX 案内の主要な見出しを render することを検証する。"""
    doc = _build_routing_policy(_path_context())[1]

    assert isinstance(doc, SDHeader)
    assert doc.title == "routing policy"

    rendered = render_sd_node_as_markdown(doc)
    assert "INDEX.md" in rendered
    assert "どのファイル・ディレクトリを読むべきか判断・特定" in rendered
    assert "作業対象に近い階層の `INDEX.md` を起点" in rendered
    assert "内容が食い違う場合は本文を優先" in rendered
    assert "本文の代替にせず、必ず本文を判断の根拠" in rendered


def test_complete_prompt_orders_static_objective_and_dynamic_sections() -> None:
    """完全 prompt は固定部から動的部へ並べ、call 固有 objective を構築する。"""
    prompt = build_complete_prompt(
        task="- 対象 prompt を確認すること",
        scope="- 入力された prompt を根拠とすること",
        completion_criteria="- prompt の参照関係が妥当であること",
        non_goals="- prompt を変更しないこと",
        file_access_mode=FileAccessMode.READONLY,
        path_context=_path_context(),
        aux_static_prompt=[SDHeader("caller static", "- static")],
        aux_dynamic_prompt=[SDHeader("caller dynamic", "- dynamic")],
        oracle_policy=True,
    )

    rendered = render_sd_node_as_markdown(*prompt)
    assert '<cmoc_ref target="fundamental_policy"/>' in rendered
    assert '<cmoc_ref target="objective"/>' in rendered
    objective = rendered.split('<cmoc_block id="objective">', 1)[1].split(
        "</cmoc_block>", 1
    )[0]
    objective_markers = (
        "# task\n\n- 対象 prompt を確認すること",
        "# scope\n\n- 入力された prompt を根拠とすること",
        "# completion criteria\n\n- prompt の参照関係が妥当であること",
        "# non-goals\n\n- prompt を変更しないこと",
    )
    objective_positions = [objective.index(marker) for marker in objective_markers]
    assert objective_positions == sorted(objective_positions)
    assert "# summary" not in objective
    assert "# goal" not in objective
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


def test_complete_prompt_omits_unset_optional_objective_sections() -> None:
    """task だけの call では未指定の objective 項目を描画しない。"""
    prompt = build_complete_prompt(
        task="- 短い応答を返すこと",
        file_access_mode=FileAccessMode.READONLY,
        path_context=_path_context(),
    )

    rendered = render_sd_node_as_markdown(*prompt)
    objective = rendered.split('<cmoc_block id="objective">', 1)[1].split(
        "</cmoc_block>", 1
    )[0]
    assert "# task\n\n- 短い応答を返すこと" in objective
    for omitted_heading in ("# scope", "# completion criteria", "# non-goals"):
        assert omitted_heading not in objective


def test_complete_prompt_includes_feedback_instruction_exactly_once() -> None:
    """全 agent call の共通 feedback instruction が一経路だけで注入される。"""
    prompt = build_complete_prompt(
        task="- task",
        file_access_mode=FileAccessMode.READONLY,
        path_context=_path_context(),
        aux_dynamic_prompt=[],
    )

    rendered = render_sd_node_as_markdown(*prompt)
    assert rendered.count("# human feedback reporting") == 1
    assert rendered.count("cmoc_feedback.submit_observation") == 1
    assert (
        "このセッション内でエージェントに課された規定の範囲内では解決できない問題"
        in rendered
    )
    assert "セッション内で解決した問題" in rendered
    assert "仕様どおりの制約" in rendered
    assert "具体的な根拠がない改善案" in rendered
    assert "成功・失敗を根拠にセッションを中断・続行を判断してはならない" in (rendered)


def test_complete_prompt_renders_file_classification_boundaries() -> None:
    """基本定義が三分類と owning repository の判定境界を伝える。"""
    prompt = build_complete_prompt(
        task="- task",
        file_access_mode=FileAccessMode.READONLY,
        path_context=_path_context(),
        oracle_and_realization_basic=True,
    )

    rendered = render_sd_node_as_markdown(*prompt)
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
        "`{{work-root}}/src` に配置されている",
        "`{{work-root}}/test` に配置されている",
    ):
        assert expected in rendered
    assert "通常は `{{work-root}}/src` に配置されている" not in rendered
    assert "通常は `{{work-root}}/test` に配置されている" not in rendered


def test_complete_prompt_merges_equal_root_definitions_and_rejects_conflicts(
    tmp_path: Path,
) -> None:
    """root placeholder は同値なら統合し、異値なら prompt 構築を失敗させる。"""
    context = _path_context()

    prompt = build_complete_prompt(
        task="- task",
        file_access_mode=FileAccessMode.READONLY,
        path_context=context,
        aux_placeholder_def={"work-root": context.work_root},
    )
    assert render_sd_node_as_markdown(*prompt).count("- {{work-root}} =") == 1

    with pytest.raises(ValueError, match="Conflicting placeholder definition"):
        build_complete_prompt(
            task="- task",
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
        rendered = render_sd_node_as_markdown(doc)
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
    main_rendered = render_sd_node_as_markdown(
        _build_file_access_policy(FileAccessMode.REPO_WRITE, main_context)[1]
    )
    assert "`{{repo-root}}` ツリー外は読み書き禁止" in main_rendered
    assert "`{{repo-root}}/.cmoc/g*/ar` ツリー内は書き込み禁止" not in main_rendered

    linked = root / ".cmoc" / "gu" / "worktree" / "linked"
    run_git(root, "worktree", "add", "-b", "prompt-parts-linked", str(linked), "HEAD")
    linked_context = AgentCallPathContext(agent_call_cwd=linked)
    linked_rendered = render_sd_node_as_markdown(
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
        task="task",
        file_access_mode=FileAccessMode.NO_POLICY,
        path_context=_path_context(),
    )
    rendered = render_sd_node_as_markdown(*prompt)

    assert "file R/W policy" not in rendered


def test_complete_prompt_preserves_injected_policy_terms() -> None:
    """complete promptが注入した各policyの主要語とplaceholderを保持することを検証する。"""
    prompt = build_complete_prompt(
        task="- task",
        file_access_mode=FileAccessMode.READONLY,
        path_context=_path_context(),
        aux_dynamic_prompt=[],
        oracle_and_realization_basic=True,
        oracle_policy=True,
        realization_policy=True,
        oracle_findings_policy=True,
        realization_findings_policy=True,
        conflict_resolution_policy=True,
        index_entry_policy=True,
    )

    rendered = render_sd_node_as_markdown(*prompt)
    assert "プロンプト > oracle file > installed skill の優先順位" in rendered
    assert "今現在の仕様を満たすために必要な realization file" in rendered
    assert rendered.count("所見に対して適用する基準は常に一貫していること") == 2
    assert "両方のマージ元ブランチの oracle file" in rendered
    assert "### 背景" not in rendered
    for forbidden in ["{{cmoc-root}}", "{{run-root}}"]:
        assert forbidden not in rendered
    assert "{{repo-root}}" in rendered
    for expected in [
        "oracle and realization basic",
        "oracle policy",
        "realization policy",
        "oracle findings policy",
        "realization findings policy",
        "conflict resolution policy",
        "index entry policy",
        "oracle file",
        "realization file",
    ]:
        assert expected in rendered


def test_complete_prompt_keeps_root_tokens_and_records_work_root_placeholder(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """complete promptが入力root tokenを保持し、実pathの定義行を追加することを検証する。"""
    repo_root = make_repo(tmp_path)
    monkeypatch.chdir(repo_root)

    prompt = build_complete_prompt(
        task="- {{repo-root}} ツリー内の realization file を修正すること",
        file_access_mode=FileAccessMode.READONLY,
        path_context=_path_context(),
        aux_dynamic_prompt=[
            SDHeader(
                "aux realization file",
                "- {{cmoc-root}} と {{run-root}} と {{work-root}} 配下を確認すること",
            ),
            SDHeader(
                "所見本文",
                SDCodeBlock(
                    "json",
                    '{"summary": "realization file and {{repo-root}} stay in code block"}',
                ),
            ),
        ],
    )

    rendered = render_sd_node_as_markdown(*prompt)

    assert "# aux realization file" in rendered
    assert "{{repo-root}} ツリー内の realization file" in rendered
    assert "{{cmoc-root}} と {{run-root}} と {{work-root}} 配下" in rendered
    assert (
        '"summary": "realization file and {{repo-root}} stay in code block"' in rendered
    )
    assert f"- {{{{repo-root}}}} = {repo_root}" in rendered
    assert f"- {{{{work-root}}}} = {repo_root}" in rendered


def test_build_realization_policy_renders_core_conformance_requirements() -> None:
    """realization policy の適合性と検証境界が render される。"""
    path_context = _path_context()
    builder_result = _build_realization_policy(path_context)

    assert isinstance(builder_result[1], SDHeader)
    assert builder_result[0] == path_context.root_placeholder_definitions()

    rendered = _render_policy(builder_result)
    assert "realization policy" in rendered
    assert "関連する oracle file を先に確認し、その明示要求と矛盾しない" in rendered
    assert (
        "oracle file 側に実装が存在する場合、可能な限りそれをそのまま使用する"
        in rendered
    )
    assert "今現在の仕様を満たすために必要な realization file" in rendered
    assert "エージェントから参照可能な文章上で指示されている手順" in rendered
    assert "作業後の状態が検証・テストに合格する状態であること" in rendered
    assert "`{{work-root}}` 固有の指示を根拠に含めず" in rendered


def test_build_index_entry_policy_renders_core_output_requirements() -> None:
    """index entry policyの出力境界がrenderされることを検証する。"""
    builder_result = _build_index_entry_policy()

    assert isinstance(builder_result[1], SDHeader)

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


def test_build_oracle_findings_policy_renders_core_review_requirements() -> None:
    """oracle findings policy の severity と所見境界を検証する。"""
    builder_result = _build_oracle_findings_policy()

    assert isinstance(builder_result[1], SDHeader)

    rendered = _render_policy(builder_result)
    assert "oracle findings policy" in rendered
    assert "oracle file の具体的な記述だけから成立する問題" in rendered
    assert "fatal" in rendered
    assert "minor" in rendered
    assert "正本仕様断片同士の解釈の余地がない明確な矛盾" in rendered
    assert "実装者裁量の範囲内で解決出来ない問題" in rendered
    assert "誤字" in rendered
    assert "用語不統一" in rendered
    assert "所見に対して適用する基準は常に一貫していること" in rendered
    assert "規定上必須とされていない事" in rendered
