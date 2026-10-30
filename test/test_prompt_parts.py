"""prompt part と complete prompt の組み立て結果を検証する。

各 prompt part の rendering と complete prompt の有効化・placeholder 展開は同じ
SDHeader 出力を共有する一つの責務であるため、prompt builder 回帰として一箇所に保つ。

対応する正本:
- {{work-root}}/spec/app_spec/codex_common_rule.md
- {{work-root}}/spec/app_spec/feedback_observation.md
- {{work-root}}/spec/app_spec/editor_input_handoff.md
- {{work-root}}/spec/app_spec/document_search.md
- {{work-root}}/spec/app_spec/cmoc_basic_instruction.md
- {{work-root}}/spec/app_spec/cmoc_basic_instruction_file_enumeration.md
- {{work-root}}/spec/app_spec/sub_command/session_join.md
- {{work-root}}/reference/src/oracle/other/struct_doc.py
- {{work-root}}/reference/src/oracle/prompt_builder/basic.py
- {{work-root}}/reference/src/oracle/prompt_builder/complete_prompt.py
- {{work-root}}/reference/src/oracle/prompt_builder/policy/conflict_resolution.py
- {{work-root}}/reference/src/oracle/prompt_builder/policy/editor_input_handoff.py
- {{work-root}}/reference/src/oracle/prompt_builder/policy/feedback_reporting.py
- {{work-root}}/reference/src/oracle/prompt_builder/policy/file_access.py
- {{work-root}}/reference/src/oracle/prompt_builder/parts/cmoc_basic_instruction.py
- {{work-root}}/reference/src/oracle/prompt_builder/policy/oracle.py
- {{work-root}}/reference/src/oracle/prompt_builder/policy/realization_findings.py
- {{work-root}}/reference/src/oracle/prompt_builder/policy/realization.py
- {{work-root}}/reference/src/oracle/prompt_builder/policy/routing.py
"""

from pathlib import Path

import oracle.other.path_model as path_model_module
import pytest
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
from oracle.prompt_builder.policy.oracle import (
    build_oracle_policy as _build_oracle_policy,
)
from oracle.prompt_builder.policy.realization import (
    build_realization_policy as _build_realization_policy,
)
from oracle.prompt_builder.policy.realization_findings import (
    build_realization_findings_policy as _build_realization_findings_policy,
)

from basic.acp import FileAccessMode
from basic.path_model import AgentCallPathContext


@pytest.fixture(scope="module")
def path_context(tmp_path_factory: pytest.TempPathFactory) -> AgentCallPathContext:
    """文面検査用の異なる両 root を共有し、Git process の起動を省く。"""
    root = tmp_path_factory.mktemp("prompt-roots")
    linked = root / "linked"
    linked.mkdir()
    # 実 Git metadata からの導出は test_basic_runtime.py で検査する。
    # 構築時だけ探索結果を置換し、不変 context と renderer は実物を使う。
    with pytest.MonkeyPatch.context() as monkeypatch:
        monkeypatch.setattr(
            path_model_module,
            "_resolve_git_worktree_roots",
            lambda _agent_call_cwd: (linked, root),
        )
        return AgentCallPathContext(agent_call_cwd=linked)


@pytest.fixture(scope="module")
def default_prompt_markdown(path_context: AgentCallPathContext) -> str:
    """既定規定・objective 省略・入力保持の検査で、構築と描画を共有する。"""
    prompt = build_complete_prompt(
        task="- {{repo-root}} ツリー内の realization file を修正すること",
        file_access_mode=FileAccessMode.READONLY,
        path_context=path_context,
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
    return render_sd_node_as_markdown(*prompt)


@pytest.fixture(scope="module")
def customized_prompt_markdown(path_context: AgentCallPathContext) -> str:
    """順序・規定の併用・同値 root 統合に、一度構築した不変 Markdown を使う。"""
    # 単独 flag の独立性と異値 root の拒否は、それぞれ専用 test で検査する。
    prompt = build_complete_prompt(
        task="- 対象 prompt を確認すること",
        scope="- 入力された prompt を根拠とすること",
        completion_criteria="- prompt の参照関係が妥当であること",
        non_goals="- prompt を変更しないこと",
        file_access_mode=FileAccessMode.READONLY,
        path_context=path_context,
        aux_static_prompt=[SDHeader("caller static", "- static")],
        aux_dynamic_prompt=[SDHeader("caller dynamic", "- dynamic")],
        aux_placeholder_def={"work-root": path_context.work_root},
        cmoc_basic_instruction=True,
        spec_policy=True,
        realization_policy=True,
        realization_findings_policy=True,
        conflict_resolution_policy=True,
    )
    return render_sd_node_as_markdown(*prompt)


def _render_policy(
    builder_result: tuple[PlaceholderMap, SDHeader],
    categories: tuple[str, ...],
    *,
    policy_count: int = 1,
) -> str:
    """文面検査に使う描画を一度だけ行い、構造とカテゴリ順序も検証する。"""
    policy_header = builder_result[1]
    assert len(policy_header.children) == policy_count
    assert isinstance(policy_header.children[0], SDPolicy)
    if policy_count != 3:
        assert all(isinstance(child, SDPolicy) for child in policy_header.children)

    rendered = render_sd_node_as_markdown(policy_header)
    lines = rendered.splitlines()

    assert len([line for line in lines if line.startswith("# ")]) == 1
    assert len([line for line in lines if line.startswith("## ")]) == (
        2 if policy_count == 3 else 0
    )
    assert [
        line
        for line in lines
        if line in {"**必須**", "**禁止**", "**許容**", "**例外**", "**補足情報**"}
    ] == list(categories)
    return rendered


_POLICY_FLAG_HEADINGS = (
    ("cmoc_basic_instruction", "# oracle and realization basic"),
    ("oracle_policy", "# oracle policy"),
    ("realization_policy", "# realization policy"),
    ("realization_findings_policy", "# realization findings policy"),
    ("conflict_resolution_policy", "# conflict resolution policy"),
    ("routing_policy", "# routing policy"),
    ("editor_input_handoff_policy", "# editor input handoff"),
)


# 基本定義と routing の flag 検査は、それぞれの文面検査と同じ prompt で行う。
@pytest.mark.parametrize(
    ("selected_flag", "selected_heading"),
    [
        case
        for case in _POLICY_FLAG_HEADINGS
        if case[0] not in {"cmoc_basic_instruction", "routing_policy"}
    ],
)
def test_each_policy_flag_adds_only_its_block_once(
    selected_flag: str,
    selected_heading: str,
    path_context: AgentCallPathContext,
) -> None:
    """各 flag は対応する policy block だけを一度追加する。"""
    prompt = build_complete_prompt(
        task="- task",
        file_access_mode=FileAccessMode.READONLY,
        path_context=path_context,
        **{selected_flag: True},
    )

    rendered = render_sd_node_as_markdown(*prompt)
    for _, heading in _POLICY_FLAG_HEADINGS:
        assert rendered.count(heading) == (1 if heading == selected_heading else 0)


def test_oracle_policy_keeps_reference_and_authority_boundaries() -> None:
    """oracle policy が参照形式、正本責務、未定義事項を区別する。"""
    rendered = _render_policy(
        _build_oracle_policy(),
        ("**必須**", "**禁止**", "**例外**", "**補足情報**", "**必須**", "**禁止**"),
        policy_count=2,
    )

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

    rendered = _render_policy(builder_result, ("**必須**", "**禁止**"))
    assert "realization findings policy" in rendered
    assert "oracle file の具体的な要求と realization file の具体的な挙動" in rendered
    assert "realization file 上に明確に存在する致命的な問題" in rendered
    assert "oracle file 自体の問題" in rendered
    assert "明示要求のない事項を、仕様への不適合の根拠にしてはいけない" in rendered
    assert "この call の目的として明示された改善" in rendered
    assert "その目的に対応する対象箇所と具体的な改善根拠" in rendered
    assert "この call の目的に含まれない一般的な品質改善" in rendered
    assert "調査開始時点ですでに解消されている問題" in rendered


def test_conflict_resolution_policy_renders_merge_result_requirements() -> None:
    """conflict 解消結果の保持・報告・変更境界を伝える。"""
    builder_result = _build_conflict_resolution_policy()
    rendered_doc = _render_policy(
        builder_result, ("**必須**", "**禁止**"), policy_count=3
    )
    assert "両 branch の変更を整合したマージ結果" in rendered_doc
    assert "両 branch の両立する意図と挙動" in rendered_doc
    assert "新しい人間意図の選択が必要な場合" in rendered_doc
    assert "適用される規定に違反する解消結果" in rendered_doc
    assert "初期の競合一覧にない関連ファイル" in rendered_doc


@pytest.mark.parametrize("enable_document_search_mcp", [False, True])
def test_complete_prompt_renders_search_routing_for_call_availability(
    enable_document_search_mcp: bool,
    path_context: AgentCallPathContext,
) -> None:
    """routing だけを一度挿入し、検索の併用条件と call の有効状態を伝える。"""
    prompt = build_complete_prompt(
        task="- task",
        file_access_mode=FileAccessMode.READONLY,
        path_context=path_context,
        routing_policy=True,
        enable_document_search_mcp=enable_document_search_mcp,
    )
    rendered = render_sd_node_as_markdown(*prompt)
    for flag, heading in _POLICY_FLAG_HEADINGS:
        assert rendered.count(heading) == (1 if flag == "routing_policy" else 0)
    routing = rendered.split("# routing policy\n", 1)[1].split("</cmoc_block>", 1)[0]
    required = routing.split("\n**必須**\n", 1)[1].split("\n**禁止**\n", 1)[0]
    prohibited = routing.split("\n**禁止**\n", 1)[1].split("\n**例外**\n", 1)[0]
    exceptions = routing.split("\n**例外**\n", 1)[1].split("\n## ", 1)[0]

    assert "原文を読んで確認" in required
    assert "ファイルアクセス制限は、検索結果についても適用" in required
    assert "「検索失敗」と「検索成功の上でヒットゼロ件」は区別" in required
    assert "検索ヒットゼロ件だけを根拠" in prohibited
    assert "「仕様の不存在」「調査完了」と判断してはいけない" in prohibited
    assert "検索に失敗した場合は、許可された手段で調査を続けて良い" in exceptions
    for tool_detail in (
        "query",
        "limit",
        "hits",
        "ranges",
        "candidate_count",
        "structuredContent",
        "isError",
        "inputSchema",
        "outputSchema",
    ):
        assert tool_detail not in routing

    if not enable_document_search_mcp:
        assert "任意の方法で関係文章を検索すること" in required
        assert "cmoc_document_search.search" not in routing
        assert "ベクトル検索も併用" not in required
    else:
        assert "キーワード検索に加えて" in required
        assert (
            "MCP tool `cmoc_document_search.search` によるベクトル検索も併用"
            in required
        )


def test_complete_prompt_orders_static_objective_and_dynamic_sections(
    customized_prompt_markdown: str,
) -> None:
    """完全 prompt は固定部から動的部へ並べ、call 固有 objective を構築する。"""
    rendered = customized_prompt_markdown
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


def test_complete_prompt_omits_unset_optional_objective_sections(
    default_prompt_markdown: str,
) -> None:
    """task だけの call では未指定の objective 項目を描画しない。"""
    objective = default_prompt_markdown.split('<cmoc_block id="objective">', 1)[
        1
    ].split("</cmoc_block>", 1)[0]
    assert "# task\n\n- {{repo-root}} ツリー内の realization file を修正すること" in (
        objective
    )
    for omitted_heading in ("# scope", "# completion criteria", "# non-goals"):
        assert omitted_heading not in objective


def test_complete_prompt_includes_feedback_instruction_exactly_once(
    default_prompt_markdown: str,
    path_context: AgentCallPathContext,
) -> None:
    """全 agent call の共通 feedback instruction が一経路だけで注入される。"""
    assert default_prompt_markdown.count("# feedback observation reporting") == 1
    assert default_prompt_markdown.count("cmoc_feedback.submit_observation") == 1
    fundamental_policy = default_prompt_markdown.split(
        '<cmoc_block id="fundamental_policy">', 1
    )[1].split("</cmoc_block>", 1)[0]
    expected_policy = _render_policy(
        _build_feedback_reporting_policy(path_context),
        ("**必須**", "**禁止**", "**補足情報**"),
    )
    assert fundamental_policy.count(expected_policy) == 1


def test_complete_prompt_renders_file_classification_boundaries(
    path_context: AgentCallPathContext,
) -> None:
    """基本定義だけを挿入し、三分類と owning repository の判定境界を伝える。"""
    prompt = build_complete_prompt(
        task="- task",
        file_access_mode=FileAccessMode.READONLY,
        path_context=path_context,
        cmoc_basic_instruction=True,
    )

    rendered = render_sd_node_as_markdown(*prompt)
    for flag, heading in _POLICY_FLAG_HEADINGS:
        assert rendered.count(heading) == (1 if flag == "cmoc_basic_instruction" else 0)
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
    path_context: AgentCallPathContext,
    customized_prompt_markdown: str,
) -> None:
    """root placeholder は同値なら統合し、異値なら prompt 構築を失敗させる。"""
    context = path_context

    assert customized_prompt_markdown.count("- {{work-root}} =") == 1

    with pytest.raises(ValueError, match="Conflicting placeholder definition"):
        build_complete_prompt(
            task="- task",
            file_access_mode=FileAccessMode.READONLY,
            path_context=context,
            aux_placeholder_def={"work-root": context.work_root / "other-worktree"},
        )


def test_file_access_policy_titles_and_bodies_match_modes(
    path_context: AgentCallPathContext,
) -> None:
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
    common_denials = {
        "`{{work-root}}` ツリー外は書き込み禁止",
        "`{{work-root}}/.git` ツリー内は書き込み禁止",
        "Git metadata は配置先によらず変更禁止",
        "`{{work-root}}/.agents` ツリー内は書き込み禁止",
        "`{{work-root}}/.codex` ツリー内は書き込み禁止",
        "`{{work-root}}/.cmoc` ツリー内は書き込み禁止",
        "`AGENTS.md` は書き込み禁止",
        "`{{work-root}}/memo` は読み書き禁止",
        "一時作業領域を禁止・制限事項の迂回に使って",
    }

    for mode, fragments in mode_specific_denials.items():
        builder_result = _build_file_access_policy(mode, path_context)
        doc = builder_result[1]
        rendered = _render_policy(
            builder_result, ("**禁止**", "**例外**", "**補足情報**")
        )
        assert doc.title == f"file access policy ({mode.value})"
        assert (
            "この policy は deny list で記述しており、禁止されていない読み書きは暗に許容される"
            in rendered
        )
        assert "ツリー外は読み書き禁止" not in rendered
        assert "Git metadata の読み取り例外" not in rendered
        exceptions = rendered.split("**例外**\n", 1)[1].split("**補足情報**", 1)[0]
        assert "`/tmp`, `%TMPDIR` ツリー内は読み書きして良い" in exceptions
        assert "\n**必須**\n" not in rendered
        assert "作業専用の一時ディレクトリ" not in rendered
        assert "MCP 経由の外部ツールによるファイル書き込み" in exceptions
        assert "Structured Output を受け取った外部ツールによるファイル書き込み" in (
            exceptions
        )
        for fragment in common_denials | fragments:
            assert fragment in rendered
        for fragment in all_mode_specific_denials - mode_specific_denials[mode]:
            assert fragment not in rendered


def test_file_access_policy_keeps_same_boundaries_in_linked_worktree(
    path_context: AgentCallPathContext,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """main と linked の path context に同じ直接アクセス境界を伝える。"""
    root = path_context.repo_root
    linked = path_context.work_root

    # 実 Git metadata から両 root を導く検証は test_basic_runtime.py に残す。
    # 文面比較ではその探索結果だけを置換し、context と renderer は実物を使う。
    def resolve_test_roots(agent_call_cwd: Path) -> tuple[Path, Path]:
        assert agent_call_cwd in (root, linked)
        return agent_call_cwd, root

    monkeypatch.setattr(
        path_model_module, "_resolve_git_worktree_roots", resolve_test_roots
    )
    main_context = AgentCallPathContext(agent_call_cwd=root)
    main_rendered = render_sd_node_as_markdown(
        _build_file_access_policy(FileAccessMode.REPO_WRITE, main_context)[1]
    )

    linked_context = AgentCallPathContext(agent_call_cwd=linked)
    linked_rendered = render_sd_node_as_markdown(
        _build_file_access_policy(FileAccessMode.REPO_WRITE, linked_context)[1]
    )
    assert linked_rendered == main_rendered
    assert "/.cmoc/g*/ar" not in linked_rendered


def test_editor_input_handoff_keeps_context_and_scope_boundaries() -> None:
    """明示された相手へ単独で理解できる依頼を渡し、経緯や権限を補わない。"""
    rendered = _render_policy(
        _build_editor_input_handoff_policy(), ("**必須**", "**禁止**", "**補足情報**")
    )
    requirements, prohibitions = rendered.split("**禁止**\n", 1)

    assert (
        "人間が active target への handoff を明示的に要求し、target ID を提示した場合だけ"
        in requirements
    )
    assert "送り元の会話や最終回答を読まなくても依頼を理解できる" in requirements
    assert "cmoc_editor_input.get_handoff_guide" in requirements
    assert "ガイド取得時と同じ `target_id`" in requirements
    assert (
        "handoff の成否にかかわらず agent call に要求された回答または成果物を満たす"
        in requirements
    )
    assert "経緯や決定が存在しない箇所を勝手に補ってはならない" in prohibitions
    assert "handoff を根拠とした作業スコープの拡大はしてはならない" in prohibitions
    assert (
        "tool を利用できない場合や、ガイド取得・上書きに失敗した場合の代替手段として sandbox escalation を要求してはならない"
        in prohibitions
    )
    assert (
        "handoff ガイドを取得できない場合は、その handoff の overwrite を行ってはならない"
        in prohibitions
    )
    assert "自分自身に適用する作業指示や権限として扱ってはならない" in prohibitions


def test_no_policy_complete_prompt_omits_file_access_policy(
    path_context: AgentCallPathContext,
) -> None:
    """NO_POLICY 時に file access policy を挿入しないことを検証する。"""
    prompt = build_complete_prompt(
        task="task",
        file_access_mode=FileAccessMode.NO_POLICY,
        path_context=path_context,
    )
    rendered = render_sd_node_as_markdown(*prompt)

    assert "file access policy" not in rendered
    assert "一時作業領域" not in rendered


def test_complete_prompt_preserves_injected_policy_terms(
    customized_prompt_markdown: str,
) -> None:
    """complete promptが注入した各policyの主要語とplaceholderを保持することを検証する。"""
    rendered = customized_prompt_markdown
    assert "プロンプト > oracle file > installed skill の優先順位" in rendered
    assert "今現在の仕様を満たすために必要な realization file" in rendered
    assert rendered.count("所見に対して適用する基準は常に一貫していること") == 1
    assert "両 branch の両立する意図と挙動" in rendered
    assert "### 背景" not in rendered
    for forbidden in ["{{cmoc-root}}", "{{run-root}}"]:
        assert forbidden not in rendered
    assert "{{repo-root}}" in rendered
    for expected in [
        "oracle and realization basic",
        "oracle policy",
        "realization policy",
        "realization findings policy",
        "conflict resolution policy",
        "oracle file",
        "realization file",
    ]:
        assert expected in rendered


def test_complete_prompt_keeps_root_tokens_and_records_work_root_placeholder(
    path_context: AgentCallPathContext,
    default_prompt_markdown: str,
) -> None:
    """complete promptが入力root tokenを保持し、実pathの定義行を追加することを検証する。"""
    rendered = default_prompt_markdown

    assert "# aux realization file" in rendered
    assert "{{repo-root}} ツリー内の realization file" in rendered
    assert "{{cmoc-root}} と {{run-root}} と {{work-root}} 配下" in rendered
    assert (
        '"summary": "realization file and {{repo-root}} stay in code block"' in rendered
    )
    assert f"- {{{{repo-root}}}} = {path_context.repo_root}" in rendered
    assert f"- {{{{work-root}}}} = {path_context.work_root}" in rendered


def test_build_realization_policy_renders_core_conformance_requirements(
    path_context: AgentCallPathContext,
) -> None:
    """realization policy の適合性と検証境界が render される。"""
    builder_result = _build_realization_policy(path_context)

    assert isinstance(builder_result[1], SDHeader)
    assert builder_result[0] == path_context.root_placeholder_definitions()

    rendered = _render_policy(builder_result, ("**必須**", "**禁止**", "**例外**"))
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
