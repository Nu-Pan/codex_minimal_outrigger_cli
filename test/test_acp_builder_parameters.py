"""ACP builder の parameter と structured output schema 参照を検証する。

分割根拠: <work-root>/oracle/src/oracle/prompt_builder/parts/realization_standard.py
"""

import json
from pathlib import Path
from typing import Callable

import pytest
from jsonschema import validate

import acp.builder.tui.resolve_parameter as tui_resolve_parameter_module
from acp.builder.apply.fork.change_summary import (
    build_apply_fork_change_summary_parameter,
)
from acp.builder.apply.fork.file_finding_enumeration import (
    build_apply_fork_file_finding_enumeration_parameter,
)
from acp.builder.apply.fork.finding_application import (
    build_apply_fork_finding_application_parameter,
)
from acp.builder.common.file_access_rule_vaolation_recovery import (
    build_file_access_rule_vaolation_recovery_parameter,
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
from acp.builder.tui.resolve_parameter import TUI_FILE_ACCESS_MODES
from acp.builder.tui.resolve_parameter import build_tui_resolve_parameter_parameter
from basic.acp import AgentCallParameter, FileAccessMode, ModelClass, ReasoningEffort
from oracle.acp_builder.review.oracle.enumerate_finding import (
    build_review_oracle_enumerate_finding_parameter as _build_oracle_enumerate_parameter,
)


def oracle_schema_path(*parts: str) -> Path:
    return Path(__file__).parents[1].joinpath(
        "oracle", "src", "oracle", "acp_builder", *parts
    )


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
    expected_path = oracle_schema_path("apply", "fork", "change_summary.json")

    assert parameter.structured_output_schema_path == expected_path

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


def test_file_access_rule_violation_recovery_uses_dedicated_parameter() -> None:
    call_log = Path(".cmoc/log/codex/20260102_030405_call.json")
    parameter = build_file_access_rule_vaolation_recovery_parameter(
        call_log,
        [Path("oracle/spec.md")],
        FileAccessMode.REALIZATION_WRITE,
    )

    assert parameter.model_class == ModelClass.FLAGSHIP
    assert parameter.reasoning_effort == ReasoningEffort.MEDIUM
    assert parameter.file_access_mode == FileAccessMode.NO_RULE
    assert parameter.structured_output_schema_path is None
    assert "ファイルアクセス規則違反のリカバリー担当" in parameter.prompt
    assert "# <violated-file-access-rule>" in parameter.prompt
    assert "# <violated-file-list>" in parameter.prompt
    assert "- `oracle/spec.md`" in parameter.prompt
    assert "20260102_030405_call" in parameter.prompt
    assert "FINDING-00" not in parameter.prompt


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
        "goal",
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


def test_tui_resolve_parameter_module_exports_only_required_names() -> None:
    assert tui_resolve_parameter_module.__all__ == [
        "build_tui_resolve_parameter_parameter",
        "TUI_FILE_ACCESS_MODES",
    ]
    assert not hasattr(tui_resolve_parameter_module, "render_as_markdown")


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
        oracle_schema_path("review", "oracle", "enumerate_finding.json").read_text()
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


def test_review_oracle_enumerate_parameter_matches_oracle_builder() -> None:
    oracle_path = Path("<work-root>/oracle/doc/sample.md")
    related_findings = "[]"

    parameter = build_review_oracle_enumerate_finding_parameter(
        oracle_path,
        related_findings,
    )
    oracle_parameter = _build_oracle_enumerate_parameter(
        oracle_path,
        related_findings,
    )

    assert parameter == oracle_parameter


def test_review_oracle_merge_finding_schema_matches_oracle_source() -> None:
    parameter = build_review_oracle_merge_finding_parameter("[]")
    assert "<<oracle-root>>" not in parameter.prompt
    assert "<oracle-root>" in parameter.prompt
    assert "- <oracle-root> =" in parameter.prompt
    assert parameter.structured_output_schema_path is not None
    schema = json.loads(parameter.structured_output_schema_path.read_text())
    oracle_schema = json.loads(
        oracle_schema_path("review", "oracle", "merge_finding.json").read_text()
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


def test_review_oracle_merge_finding_preserves_known_findings_text() -> None:
    known_findings = (
        '[{"finding_id":"finding-0001","reason":"literal <<oracle-root>>"}]'
        "\n- <<oracle-root>> = literal"
    )
    parameter = build_review_oracle_merge_finding_parameter(known_findings)
    assert known_findings in parameter.prompt
    assert "- <oracle-root> =" in parameter.prompt


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
        oracle_schema_path("review", "oracle", schema_name).read_text()
    )

    assert parameter.structured_output_schema_path.name == schema_name
    assert schema == oracle_schema
    validate({"reasons": []}, schema)
    validate({"reasons": ["oracle file の記述に基づく理由"]}, schema)


def test_review_oracle_validate_finding_advocate_preserves_dynamic_text() -> None:
    finding = "finding literal `<oracle_root>` ツリー内 should stay"
    known_advocate = "known advocate literal `<oracle_root>` ツリー内 should stay"
    known_challenger = "known challenger literal `<oracle_root>` ツリー内 should stay"

    parameter = build_review_oracle_validate_finding_advocate_parameter(
        finding,
        known_advocate,
        known_challenger,
    )

    assert finding in parameter.prompt
    assert known_advocate in parameter.prompt
    assert known_challenger in parameter.prompt
    assert parameter.prompt.count("`<oracle_root>` ツリー内") == 3
    assert "`<oracle-root>` ツリー内" in parameter.prompt


def test_session_join_conflict_resolution_uses_repo_write_mode() -> None:
    parameter = build_session_join_conflict_resolution_parameter([__file__])

    assert parameter.model_class == ModelClass.MAINSTREAM
    assert parameter.reasoning_effort == ReasoningEffort.MEDIUM
    assert parameter.file_access_mode == FileAccessMode.REPO_WRITE
    assert "conflict 対象ファイル" in parameter.prompt
