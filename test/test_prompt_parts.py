"""prompt part と ACP builder の生成結果を横断的に検証する。

このファイルは 16,000 文字を超えるが、責務境界は agent prompt と structured output
schema の構築結果を検証することに閉じている。標準 prompt、routing、file access、
builder parameter は最終 prompt の同じ読み取り文脈で組み合わさるため、分割すると
共通の render/schema 期待値を追うために複数ファイルを読む必要が生じる。
現状は prompt 構築の回帰観点を一箇所に保つ方が凝集性が高い。
"""

import json
import os
import shutil
import subprocess
import sys
import tomllib
from pathlib import Path
from typing import Callable

import pytest
from jsonschema import validate

from basic.acp import FileAccessMode
from basic.acp import AgentCallParameter
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
from acp.builder.review.oracle.enumerate_finding import (
    build_review_oracle_enumerate_finding_parameter,
)
from acp.builder.review.oracle.merge_finding import (
    build_review_oracle_merge_finding_parameter,
)
from acp.builder.review.oracle.validate_finding_advocate import (
    build_review_oracle_validate_finding_advocate_parameter,
)
from acp.builder.review.oracle.validate_finding_challenger import (
    build_review_oracle_validate_finding_challenger_parameter,
)
from acp.builder.session.join.conflict_resolution import (
    build_session_join_conflict_resolution_parameter,
)
from acp.builder.tui.resolve_parameter import build_tui_resolve_parameter_parameter
from acp.builder.tui.resolve_parameter import TUI_FILE_ACCESS_MODES
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


def test_render_as_markdown_collapses_consecutive_blank_lines() -> None:
    doc = StructDoc(
        "root",
        "first\n\n\n   \nsecond",
    )

    rendered = render_as_markdown(doc)

    assert "\n\n\n" not in rendered
    assert rendered == "# root\n\nfirst\n\nsecond\n"


def test_render_as_markdown_collapses_code_block_blank_lines() -> None:
    doc = StructDoc("root", StructCodeBlock("text", "first\n\n\nsecond"))

    rendered = render_as_markdown(doc)

    assert rendered == "# root\n\n```text\nfirst\n\nsecond\n```\n"


def test_apply_fork_prompts_use_expected_roots(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
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

    assert "`<repo-root>` ツリー内の realization file" in finding_application.prompt
    assert f"- <repo-root> = {repo_root}" in finding_application.prompt
    assert f"- <work-root> = {apply_worktree}" in finding_application.prompt
    assert "`<repo-root>` ツリー内の所見" in finding_enumeration.prompt
    assert f"- <repo-root> = {repo_root}" in finding_enumeration.prompt
    assert f"`{apply_worktree}` ツリー内の所見" not in finding_enumeration.prompt
    assert "`<repo-root>` ツリー内の差分" in change_summary.prompt
    assert f"- <repo-root> = {repo_root}" in change_summary.prompt
    assert "# oracle and realization basic" in change_summary.prompt


def test_apply_fork_change_summary_schema_matches_oracle_source() -> None:
    parameter = build_apply_fork_change_summary_parameter("diff")
    oracle_schema_path = (
        Path(__file__).parents[1]
        / "oracle"
        / "src"
        / "oracle"
        / "acp_builder"
        / "apply"
        / "fork"
        / "change_summary.json"
    )

    assert parameter.structured_output_schema_path == oracle_schema_path

    schema = json.loads(parameter.structured_output_schema_path.read_text())
    validate(
        {
            "changes": [
                {
                    "category": "実装",
                    "summary": "変更要約 schema を正本仕様に合わせた。",
                    "changed_paths": [
                        "oracle/src/oracle/acp_builder/apply/fork/change_summary.json"
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
            "/memo` は読み書き禁止",
        ],
        FileAccessMode.PURE_ORACLE_READ: [
            "ツリー外は読み書き禁止",
            "/oracle` ツリー内は書き込み禁止",
            "/oracle` ツリー外は読み書き禁止",
        ],
        FileAccessMode.REALIZATION_WRITE: [
            "ツリー外は読み書き禁止",
            "/oracle` ツリー内は書き込み禁止",
            "/memo` は読み書き禁止",
        ],
        FileAccessMode.ORACLE_WRITE: [
            "ツリー外は読み書き禁止",
            "/oracle` ツリー外は書き込み禁止",
            "/memo` は読み書き禁止",
        ],
        FileAccessMode.REPO_WRITE: [
            "ツリー外は読み書き共に禁止",
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
    for forbidden in ["<cmoc-root>", "<repo-root>", "<run-root>"]:
        assert forbidden not in rendered
    assert "コメントにプレースホルダ `<work-root>` 起点の oracle file path を書く" in rendered
    assert "`<work-root>/oracle/doc/...` のように根拠 path" in rendered
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
        summary="- <repo-root> ツリー内の realization file を修正すること",
        goal="- realization standard と oracle standard に従うこと",
        file_access_mode=FileAccessMode.READONLY,
        aux_dynamic_prompt=[
            StructDoc(
                "aux realization file",
                "- <cmoc-root> と <run-root> と <work-root> 配下を確認すること",
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

    assert "- realization standard と oracle standard に従うこと" in rendered
    assert "# aux realization file" in rendered
    assert "cmoc から呼び出された" in rendered
    assert "<repo-root> ツリー内の realization file" in rendered
    assert "<cmoc-root> と <run-root> と <work-root> 配下" in rendered
    assert '"summary": "realization file and <repo-root> stay in code block"' in rendered
    assert f"- <work-root> = {repo_root}" in rendered


def test_complete_prompt_keeps_literal_root_token_comment_requirement(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    repo_root = tmp_path / "repo"
    repo_root.mkdir()
    (repo_root / ".git").mkdir()
    monkeypatch.chdir(repo_root)

    prompt = build_complete_prompt(
        role="- role",
        summary="- <work-root>/src/app.py を確認すること",
        goal="- goal",
        file_access_mode=FileAccessMode.READONLY,
        aux_dynamic_prompt=[],
        realization_standard=True,
    )

    rendered = render_as_markdown(prompt)

    assert "- <work-root>/src/app.py を確認すること" in rendered
    assert "コメントにプレースホルダ `<work-root>` 起点の oracle file path を書く" in rendered
    assert "`<work-root>/oracle/doc/...` のように根拠 path" in rendered
    assert f"- <work-root> = {repo_root}" in rendered


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
    assert "ファイル・ディレクトリの識別子、ハッシュ、出力形式は、この agent call の外側" in rendered
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
        "role",
        "summary",
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


def test_review_oracle_enumerate_finding_schema_matches_oracle_source() -> None:
    parameter = build_review_oracle_enumerate_finding_parameter(
        Path("<work-root>/oracle/spec.md"),
        "[]",
    )
    assert parameter.structured_output_schema_path is not None
    schema = json.loads(parameter.structured_output_schema_path.read_text())
    oracle_schema = json.loads(
        (
            Path(__file__).parents[1]
            / "oracle"
            / "src"
            / "oracle"
            / "acp_builder"
            / "review"
            / "oracle"
            / "enumerate_finding.json"
        ).read_text()
    )

    assert schema == oracle_schema
    validate({"findings": []}, schema)
    validate(
        {
            "findings": [
                {
                    "severity": "fatal",
                    "title": "missing requirement",
                    "oracle_path": "oracle/spec.md",
                    "reason": "仕様断片として致命的な欠落がある。",
                },
                {
                    "severity": "minor",
                    "title": "ambiguous wording",
                    "oracle_path": "oracle/spec.md",
                    "reason": "軽微な曖昧さとして改善余地がある。",
                },
            ]
        },
        schema,
    )


def test_review_oracle_enumerate_builder_imports_from_packaged_layout(
    tmp_path: Path,
) -> None:
    root = Path(__file__).parents[1]
    pyproject = tomllib.loads((root / "pyproject.toml").read_text())
    setuptools_config = pyproject["tool"]["setuptools"]
    assert "oracle" not in setuptools_config["py-modules"]
    assert setuptools_config["package-dir"]["oracle"] == "oracle/src/oracle"
    assert "oracle/src" in setuptools_config["packages"]["find"]["where"]

    target = tmp_path / "site"
    shutil.copytree(root / "src" / "acp", target / "acp")
    shutil.copytree(root / "src" / "basic", target / "basic")
    shutil.copytree(root / "oracle" / "src" / "oracle", target / "oracle")

    work = tmp_path / "work"
    (work / ".git").mkdir(parents=True)
    result = subprocess.run(
        [
            sys.executable,
            "-c",
            (
                "import json; "
                "from pathlib import Path; "
                "from acp.builder.review.oracle.enumerate_finding import "
                "build_review_oracle_enumerate_finding_parameter as build; "
                "p = build(Path('<work-root>/oracle/spec.md'), '[]'); "
                "assert p.structured_output_schema_path.name == 'enumerate_finding.json'; "
                "schema = json.loads(p.structured_output_schema_path.read_text()); "
                "assert schema['required'] == ['findings']; "
                "assert '# review oracle standard' in p.prompt"
            ),
        ],
        cwd=work,
        env={**os.environ, "PYTHONPATH": str(target), "PYTHONNOUSERSITE": "1"},
        text=True,
        capture_output=True,
    )

    assert result.returncode == 0, result.stderr


def test_review_oracle_merge_finding_schema_matches_oracle_source() -> None:
    parameter = build_review_oracle_merge_finding_parameter("[]")
    assert "<<oracle-root>>" not in parameter.prompt
    assert "<oracle-root>" in parameter.prompt
    assert "- <oracle-root> =" in parameter.prompt
    assert parameter.structured_output_schema_path is not None
    schema = json.loads(parameter.structured_output_schema_path.read_text())
    oracle_schema = json.loads(
        (
            Path(__file__).parents[1]
            / "oracle"
            / "src"
            / "oracle"
            / "acp_builder"
            / "review"
            / "oracle"
            / "merge_finding.json"
        ).read_text()
    )
    finding = {
        "severity": "fatal",
        "title": "merged",
        "oracle_path": "oracle/spec.md",
        "reason": "merged reason",
    }

    assert schema == oracle_schema
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


@pytest.mark.parametrize(
    ("builder", "schema_name"),
    [
        (
            build_review_oracle_validate_finding_advocate_parameter,
            "validate_finding_advocate.json",
        ),
        (
            build_review_oracle_validate_finding_challenger_parameter,
            "validate_finding_challenger.json",
        ),
    ],
)
def test_review_oracle_validate_finding_schema_matches_oracle_source(
    builder: Callable[[str, str, str], AgentCallParameter], schema_name: str
) -> None:
    parameter = builder("finding", "known advocate", "known challenger")
    assert parameter.model_class == ModelClass.EFFICIENCY
    assert parameter.reasoning_effort == ReasoningEffort.MEDIUM
    assert parameter.file_access_mode == FileAccessMode.PURE_ORACLE_READ
    assert "finding" in parameter.prompt
    assert "known advocate" in parameter.prompt
    assert "known challenger" in parameter.prompt
    assert "<oracle_root>" not in parameter.prompt
    assert "<oracle-root>" in parameter.prompt
    assert "- <oracle-root> =" in parameter.prompt
    assert parameter.structured_output_schema_path is not None
    schema = json.loads(parameter.structured_output_schema_path.read_text())
    oracle_schema = json.loads(
        (
            Path(__file__).parents[1]
            / "oracle"
            / "src"
            / "oracle"
            / "acp_builder"
            / "review"
            / "oracle"
            / schema_name
        ).read_text()
    )

    assert parameter.structured_output_schema_path.name == schema_name
    assert schema == oracle_schema
    validate({"reasons": []}, schema)
    validate({"reasons": ["oracle file の記述に基づく理由"]}, schema)


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
