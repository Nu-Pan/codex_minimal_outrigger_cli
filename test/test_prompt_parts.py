import json
from pathlib import Path

import pytest
from jsonschema import ValidationError, validate

from basic.acp import FileAccessMode
from basic.acp import ModelClass, ReasoningEffort
from basic.struct_doc import StructCodeBlock, StructDoc, render_as_markdown
from acp.builder.apply.fork.file_finding_enumeration import (
    build_apply_fork_file_finding_enumeration_parameter,
)
from acp.builder.apply.fork.change_summary import (
    build_apply_fork_change_summary_parameter,
)
from acp.builder.apply.fork.finding_application import (
    build_apply_fork_finding_application_parameter,
)
from acp.builder.indexing.index_entry import build_indexing_index_entry_parameter
from acp.builder.review.oracle.merge_finding import (
    build_review_oracle_merge_finding_parameter,
)
from acp.builder.session.join.conflict_resolution import (
    build_session_join_conflict_resolution_parameter,
)
from acp.builder.tui.resolve_parameter import build_tui_resolve_parameter_parameter
from acp.builder.tui.resolve_parameter import TUI_FILE_ACCESS_MODES
from acp.prompt_parts.file_access_rule import build_file_access_rule
from acp.prompt_parts.apply_review_standard import build_apply_review_standard
from acp.prompt_parts.complete_prompt import build_complete_prompt
from acp.prompt_parts.index_entry_standard import build_index_entry_standard
from acp.prompt_parts.oracle_review_standard import build_review_oracle_standard
from acp.prompt_parts.realization_standard import build_realization_standard
from acp.prompt_parts.routing_rule import build_routing_rule


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
        aux_prompt=[],
    )

    rendered = render_as_markdown(prompt)
    assert "# routing rule" in rendered


def test_render_as_markdown_collapses_consecutive_blank_lines() -> None:
    doc = StructDoc(
        "root",
        "first\n\n\n   \nsecond",
    )

    rendered = render_as_markdown(doc)

    assert "\n\n\n" not in rendered
    assert rendered == "# root\n\nfirst\n\nsecond\n"


def test_render_as_markdown_preserves_code_block_blank_lines() -> None:
    doc = StructDoc("root", StructCodeBlock("text", "first\n\n\nsecond"))

    rendered = render_as_markdown(doc)

    assert rendered == "# root\n\n```text\nfirst\n\n\nsecond\n```\n"


def test_apply_fork_prompts_use_expected_roots(
    tmp_path: Path, monkeypatch
) -> None:
    repo_root = tmp_path / "repo"
    apply_worktree = repo_root / ".cmoc" / "worktrees" / "session" / "run"
    apply_worktree.mkdir(parents=True)
    (repo_root / ".git").mkdir()
    (apply_worktree / ".git").write_text("gitdir: ignored\n")
    target = apply_worktree / "src" / "app.py"
    target.parent.mkdir()
    target.write_text("print('ok')\n")
    monkeypatch.chdir(apply_worktree)

    finding_application = build_apply_fork_finding_application_parameter([{"title": "t"}])
    finding_enumeration = build_apply_fork_file_finding_enumeration_parameter(target)
    change_summary = build_apply_fork_change_summary_parameter("diff")

    assert f"`{repo_root}` ツリー内の realization file" in finding_application.prompt
    assert f"`{apply_worktree}` ツリー内の所見" in finding_enumeration.prompt
    assert f"`{repo_root}` ツリー内の所見" not in finding_enumeration.prompt
    assert f"`{repo_root}` ツリー内の差分" in change_summary.prompt


def test_apply_fork_change_summary_schema_rejects_empty_changes() -> None:
    parameter = build_apply_fork_change_summary_parameter("diff")
    assert parameter.structured_output_schema_path is not None

    schema = json.loads(parameter.structured_output_schema_path.read_text())

    with pytest.raises(ValidationError):
        validate({"changes": []}, schema)
    validate(
        {
            "changes": [
                {
                    "category": "実装",
                    "summary": "変更要約 schema の検証制約を追加した。",
                    "changed_paths": [
                        "src/acp/builder/apply/fork/change_summary.json"
                    ],
                }
            ]
        },
        schema,
    )


def test_file_access_rule_titles_and_bodies_match_modes() -> None:
    expected = {
        FileAccessMode.READONLY: [
            "ツリー外は読み書き禁止",
            "ツリー内は書き込み禁止",
            "/.agents` ツリー内は書き込み禁止",
            "/memo` は読み書き禁止",
        ],
        FileAccessMode.PURE_ORACLE_READ: [
            "ツリー外は読み書き禁止",
            "/oracle` ツリー内は書き込み禁止",
            "/oracle` ツリー外は読み書き禁止",
            "/.agents` ツリー内は読み書き禁止",
        ],
        FileAccessMode.REALIZATION_WRITE: [
            "ツリー外は読み書き禁止",
            "/oracle` ツリー内は書き込み禁止",
            "/.agents` ツリー内は書き込み禁止",
            "/memo` は読み書き禁止",
        ],
        FileAccessMode.ORACLE_WRITE: [
            "ツリー外は読み書き禁止",
            "/oracle` ツリー外は書き込み禁止",
            "/.agents` ツリー内は書き込み禁止",
            "/memo` は読み書き禁止",
        ],
        FileAccessMode.REPO_WRITE: [
            "ツリー外は読み書き禁止",
            "/.agents` ツリー内は書き込み禁止",
            "/memo` は読み書き禁止",
        ],
    }

    for mode, fragments in expected.items():
        doc = build_file_access_rule(mode)
        rendered = render_as_markdown(doc)
        assert doc.title == f"file read write rule - {mode.value}"
        for fragment in fragments:
            assert fragment in rendered


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


def test_complete_prompt_preserves_injected_standard_terms() -> None:
    prompt = build_complete_prompt(
        role="- role",
        summary="- summary",
        goal="- goal",
        file_access_mode=FileAccessMode.READONLY,
        aux_prompt=[],
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
    for expected in [
        "oracle and realization basic",
        "oracle standard",
        "realization standard",
        "review oracle standard",
        "apply review standard",
        "index entry standard",
        "oracle file",
        "oracles file",
        "oracle spec",
        "realization file",
    ]:
        assert expected in rendered
    for forbidden in [
        "仕様ファイル（基準用語）",
        "仕様説明（別名）",
        "仕様ファイル（和訳表記）",
        "仕様ファイルズ",
    ]:
        assert forbidden not in rendered


def test_complete_prompt_preserves_base_prompt_parts() -> None:
    prompt = build_complete_prompt(
        role="- cmoc から呼び出された AI Agent です",
        summary="- <repo-root> ツリー内の realization file を修正すること",
        goal="- realization standard と oracle standard に従うこと",
        file_access_mode=FileAccessMode.READONLY,
        aux_prompt=[
            StructDoc(
                "aux realization file",
                "- <work-root> 配下の oracle file と realization file を確認すること",
            ),
            StructDoc(
                "所見本文",
                StructCodeBlock(
                    "json",
                    '{"summary": "realization file and <repo-root> stay in code block"}',
                ),
            ),
        ],
    )

    rendered = render_as_markdown(prompt)

    assert "- cmoc から呼び出された AI Agent です" in rendered
    assert "- <repo-root> ツリー内の realization file を修正すること" in rendered
    assert "- realization standard と oracle standard に従うこと" in rendered
    assert "# aux realization file" in rendered
    assert "- <work-root> 配下の oracle file と realization file を確認すること" in rendered
    assert (
        '```json\n'
        '{"summary": "realization file and <repo-root> stay in code block"}\n'
        '```'
    ) in rendered


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


def test_build_realization_standard_renders_file_split_and_merge_rules() -> None:
    doc = build_realization_standard()

    assert isinstance(doc, StructDoc)
    assert doc.title == "realization standard"

    rendered = render_as_markdown(doc)
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
        aux_prompt=[],
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


def test_tui_resolve_parameter_builder_embeds_original_prompt() -> None:
    original_prompt = "# 依頼\n\nsrc の実装を調べて必要なら修正して下さい。"

    parameter = build_tui_resolve_parameter_parameter(original_prompt)

    assert parameter.model_class == ModelClass.EFFICIENCY
    assert parameter.reasoning_effort == ReasoningEffort.MEDIUM
    assert parameter.file_access_mode == FileAccessMode.READONLY
    assert parameter.structured_output_schema_path is not None
    assert parameter.structured_output_schema_path.name == "resolve_parameter.json"
    assert parameter.structured_output_schema_path.exists()
    assert "AI Agent CLI/TUI の実行パラメータ選定担当" in parameter.prompt
    assert "作業担当者 CLI/TUI" not in parameter.prompt
    assert "パラメータ選択結果" in parameter.prompt
    assert original_prompt in parameter.prompt
    assert "# oracle and realization basic" in parameter.prompt
    assert "# oracle standard" in parameter.prompt
    assert "# realization standard" in parameter.prompt
    assert "# review oracle standard" in parameter.prompt
    assert "# apply review standard" in parameter.prompt
    assert "# index entry standard" in parameter.prompt


def test_tui_resolve_parameter_schema_matches_logical_enum_values() -> None:
    parameter = build_tui_resolve_parameter_parameter("調査して下さい。")
    assert parameter.structured_output_schema_path is not None

    schema = json.loads(parameter.structured_output_schema_path.read_text())

    assert schema["required"] == [
        "file_access_mode",
        "oracle_and_realization_basic",
        "oracle_standard",
        "realization_standard",
        "review_oracle_standard",
        "apply_review_standard",
        "index_entry_standard",
    ]
    assert schema["additionalProperties"] is False
    for parameter_name in schema["required"]:
        parameter_schema = schema["properties"][parameter_name]
        assert parameter_schema["type"] == "object"
        assert parameter_schema["additionalProperties"] is False
        assert parameter_schema["required"] == ["value", "reason"]
        assert parameter_schema["properties"]["reason"]["type"] == "string"
        assert parameter_schema["properties"]["reason"]["description"]
    assert schema["properties"]["file_access_mode"]["properties"]["value"]["enum"] == [
        file_access_mode.value for file_access_mode in TUI_FILE_ACCESS_MODES
    ]
    assert "repo_write" in schema["properties"]["file_access_mode"]["properties"]["value"]["enum"]
    for flag_name in [
        "oracle_and_realization_basic",
        "oracle_standard",
        "realization_standard",
        "review_oracle_standard",
        "apply_review_standard",
        "index_entry_standard",
    ]:
        assert schema["properties"][flag_name]["properties"]["value"]["type"] == "boolean"


def test_indexing_index_entry_uses_low_reasoning() -> None:
    parameter = build_indexing_index_entry_parameter(__file__, "# README")

    assert parameter.model_class == ModelClass.EFFICIENCY
    assert parameter.reasoning_effort == ReasoningEffort.LOW
    assert parameter.file_access_mode == FileAccessMode.READONLY


def test_review_oracle_merge_finding_uses_efficiency_model() -> None:
    parameter = build_review_oracle_merge_finding_parameter("[]")

    assert parameter.model_class == ModelClass.EFFICIENCY
    assert parameter.reasoning_effort == ReasoningEffort.MEDIUM
    assert parameter.file_access_mode == FileAccessMode.PURE_ORACLE_READ


@pytest.mark.parametrize(
    "operation",
    [
        {
            "kind": "delete",
            "target_ids": ["finding-0001"],
            "finding": {"severity": "minor"},
        },
        {
            "kind": "replace",
            "target_ids": ["finding-0001", "finding-0002"],
            "finding": {
                "severity": "minor",
                "title": "t",
                "oracle_path": "oracle/spec.md",
                "reason": "r",
            },
        },
        {"kind": "replace", "target_ids": ["finding-0001"], "finding": None},
        {
            "kind": "merge",
            "target_ids": ["finding-0001"],
            "finding": {
                "severity": "minor",
                "title": "t",
                "oracle_path": "oracle/spec.md",
                "reason": "r",
            },
        },
        {
            "kind": "merge",
            "target_ids": ["finding-0001", "finding-0002"],
            "finding": None,
        },
    ],
)
def test_review_oracle_merge_finding_schema_enforces_kind_contract(
    operation: dict,
) -> None:
    parameter = build_review_oracle_merge_finding_parameter("[]")
    assert parameter.structured_output_schema_path is not None
    schema = json.loads(parameter.structured_output_schema_path.read_text())
    finding = {
        "severity": "fatal",
        "title": "merged",
        "oracle_path": "oracle/spec.md",
        "reason": "merged reason",
    }

    with pytest.raises(ValidationError):
        validate({"operations": [operation]}, schema)
    validate(
        {
            "operations": [
                {"kind": "delete", "target_ids": ["finding-0001"], "finding": None},
                {
                    "kind": "replace",
                    "target_ids": ["finding-0002"],
                    "finding": finding,
                },
                {
                    "kind": "merge",
                    "target_ids": ["finding-0003", "finding-0004"],
                    "finding": finding,
                },
            ]
        },
        schema,
    )


def test_session_join_conflict_resolution_uses_realization_write_mode() -> None:
    parameter = build_session_join_conflict_resolution_parameter([__file__])

    assert parameter.model_class == ModelClass.MAINSTREAM
    assert parameter.reasoning_effort == ReasoningEffort.MEDIUM
    assert parameter.file_access_mode == FileAccessMode.REALIZATION_WRITE
    assert "conflict 対象ファイル" in parameter.prompt


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
