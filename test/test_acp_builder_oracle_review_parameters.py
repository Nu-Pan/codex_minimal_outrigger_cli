"""oracle review ACP builder の parameter、schema、adapter 公開面を検証する。

対応する正本: {{work-root}}/oracle/src/oracle/acp_builder/oracle/review/
"""

import json
from pathlib import Path
from typing import Callable

import pytest
from _acp_builder_support import oracle_schema_path
from jsonschema import validate
from oracle.acp_builder.oracle.review.enumerate_finding import (
    build_oracle_review_enumerate_finding_parameter as _build_oracle_enumerate_parameter,
)

import acp.builder.oracle.review.judge_finding as review_judge_finding_module
import acp.builder.oracle.review.merge_finding as review_merge_finding_module
import acp.builder.oracle.review.validate_finding_advocate as review_validate_advocate_module
import acp.builder.oracle.review.validate_finding_challenger as review_validate_challenger_module
from acp.builder.oracle.review.enumerate_finding import (
    build_oracle_review_enumerate_finding_parameter,
)
from acp.builder.oracle.review.judge_finding import (
    build_oracle_review_judge_finding_parameter,
)
from acp.builder.oracle.review.merge_finding import (
    build_oracle_review_merge_finding_parameter,
)
from acp.builder.oracle.review.validate_finding_advocate import (
    build_oracle_review_validate_finding_advocate_parameter,
)
from acp.builder.oracle.review.validate_finding_challenger import (
    build_oracle_review_validate_finding_challenger_parameter,
)
from basic.acp import AgentCallParameter, FileAccessMode, ModelClass, ReasoningEffort


@pytest.mark.parametrize(
    ("module", "exported_name"),
    [
        (
            review_judge_finding_module,
            "build_oracle_review_judge_finding_parameter",
        ),
        (
            review_merge_finding_module,
            "build_oracle_review_merge_finding_parameter",
        ),
        (
            review_validate_advocate_module,
            "build_oracle_review_validate_finding_advocate_parameter",
        ),
        (
            review_validate_challenger_module,
            "build_oracle_review_validate_finding_challenger_parameter",
        ),
    ],
)
def test_review_compatibility_modules_export_only_builders(
    module: object, exported_name: str
) -> None:
    """review互換moduleが指定されたbuilderだけを公開することを検証する。"""
    assert module.__all__ == [exported_name]
    for internal_name in [
        "Path",
        "StructDoc",
        "StructCodeBlock",
        "render_as_markdown",
        "resolve_real_path",
        "build_complete_prompt",
        "AgentCallParameter",
    ]:
        assert not hasattr(module, internal_name)


def test_oracle_review_merge_finding_uses_efficiency_model() -> None:
    """merge finding builderがefficiency modelとmax reasoningを選ぶことを検証する。"""
    parameter = build_oracle_review_merge_finding_parameter("[]")

    assert parameter.model_class == ModelClass.EFFICIENCY
    assert parameter.reasoning_effort == ReasoningEffort.MAX
    assert parameter.file_access_mode == FileAccessMode.PURE_ORACLE_READ
    assert parameter.run_indexing_preflight is True


def test_oracle_review_judge_finding_uses_max_reasoning() -> None:
    """judge finding builderがefficiency modelとmax reasoningを選ぶことを検証する。"""
    parameter = build_oracle_review_judge_finding_parameter(
        "finding", "advocate", "challenger"
    )

    assert parameter.model_class == ModelClass.EFFICIENCY
    assert parameter.reasoning_effort == ReasoningEffort.MAX
    assert parameter.file_access_mode == FileAccessMode.PURE_ORACLE_READ


def test_oracle_review_enumerate_finding_schema_matches_oracle_source() -> None:
    """enumerate finding builderのschemaがoracle sourceと一致することを検証する。"""
    parameter = build_oracle_review_enumerate_finding_parameter(
        Path("{{work-root}}/oracle/spec.md"),
        "[]",
    )
    assert parameter.model_class == ModelClass.EFFICIENCY
    assert parameter.reasoning_effort == ReasoningEffort.MAX
    assert parameter.structured_output_schema_path is not None
    schema = json.loads(parameter.structured_output_schema_path.read_text())
    oracle_schema = json.loads(
        oracle_schema_path("oracle", "review", "enumerate_finding.json").read_text()
    )

    assert schema == oracle_schema
    validate({"findings": []}, schema)
    validate(
        {
            "findings": [
                {
                    "severity": "fatal",
                    "title": "missing requirement",
                    "oracle_path": "{{oracle-root}}/spec.md",
                    "reason": "仕様断片として致命的な欠落がある。",
                },
                {
                    "severity": "minor",
                    "title": "ambiguous wording",
                    "oracle_path": "{{oracle-root}}/spec.md",
                    "reason": "軽微な曖昧さとして改善余地がある。",
                },
            ]
        },
        schema,
    )


def test_oracle_review_enumerate_parameter_matches_oracle_builder() -> None:
    """enumerate finding互換builderがcanonical builderと同じparameterを返すことを検証する。"""
    oracle_path = Path("{{work-root}}/oracle/doc/sample.md")
    related_findings = "[]"

    parameter = build_oracle_review_enumerate_finding_parameter(
        oracle_path,
        related_findings,
    )
    oracle_parameter = _build_oracle_enumerate_parameter(
        oracle_path,
        related_findings,
    )

    assert parameter == oracle_parameter


def test_oracle_review_enumerate_parameter_keeps_symlink_entry_path(
    tmp_path: Path,
) -> None:
    """enumerate prompt の `{{oracle-path}}` が symlink entry を指す。"""
    (tmp_path / "oracle").mkdir()
    target = tmp_path / "memo.md"
    target.write_text("# memo\n")
    link = tmp_path / "oracle" / "memo-link.md"
    link.symlink_to("../memo.md")

    parameter = build_oracle_review_enumerate_finding_parameter(link, "[]")

    assert f"- {{{{oracle-path}}}} = {link}" in parameter.prompt
    assert f"- {{{{oracle-path}}}} = {link.resolve()}" not in parameter.prompt


def test_oracle_review_enumerate_parameter_preserves_related_findings_text(
    tmp_path: Path,
) -> None:
    """symlink補正が動的な既知所見を書き換えないことを検証する。"""
    (tmp_path / "oracle").mkdir()
    target = tmp_path / "memo.md"
    target.write_text("# memo\n")
    link = tmp_path / "oracle" / "memo-link.md"
    link.symlink_to("../memo.md")
    related_findings = f"- {{{{oracle-path}}}} = {link.resolve()}"

    parameter = build_oracle_review_enumerate_finding_parameter(
        link,
        related_findings,
    )

    assert related_findings in parameter.prompt
    assert f"- {{{{oracle-path}}}} = {link}" in parameter.prompt


def test_oracle_review_merge_finding_schema_matches_oracle_source() -> None:
    """merge finding builderのschemaとplaceholder補正を検証する。"""
    parameter = build_oracle_review_merge_finding_parameter("[]")
    assert "<{{oracle-root}}>" not in parameter.prompt
    assert "{{oracle-root}}" in parameter.prompt
    assert "- {{oracle-root}} =" in parameter.prompt
    assert parameter.structured_output_schema_path is not None
    schema = json.loads(parameter.structured_output_schema_path.read_text())
    oracle_schema = json.loads(
        oracle_schema_path("oracle", "review", "merge_finding.json").read_text()
    )
    finding = {
        "severity": "fatal",
        "title": "merged",
        "oracle_path": "{{oracle-root}}/spec.md",
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


def test_oracle_review_merge_finding_preserves_known_findings_text() -> None:
    """merge finding builderが既知findingの動的文字列を保持することを検証する。"""
    known_findings = (
        '[{"finding_id":"finding-0001","reason":"literal <{{oracle-root}}>"}]'
        "\n- <{{oracle-root}}> = literal"
    )
    parameter = build_oracle_review_merge_finding_parameter(known_findings)
    assert known_findings in parameter.prompt
    assert "- {{oracle-root}} =" in parameter.prompt


@pytest.mark.parametrize(
    ("builder", "schema_name"),
    [
        (
            build_oracle_review_validate_finding_advocate_parameter,
            "validate_finding_advocate.json",
        ),
        (
            build_oracle_review_validate_finding_challenger_parameter,
            "validate_finding_challenger.json",
        ),
    ],
)
def test_oracle_review_validate_finding_schema_matches_oracle_source(
    builder: Callable[[str, str, str], AgentCallParameter], schema_name: str
) -> None:
    """validate finding builderのschemaと動的入力保持を検証する。"""
    parameter = builder("finding", "known advocate", "known challenger")
    assert parameter.model_class == ModelClass.EFFICIENCY
    assert parameter.reasoning_effort == ReasoningEffort.MAX
    assert parameter.file_access_mode == FileAccessMode.PURE_ORACLE_READ
    assert "finding" in parameter.prompt
    assert "known advocate" in parameter.prompt
    assert "known challenger" in parameter.prompt
    assert "{{oracle_root}}" not in parameter.prompt
    assert "{{oracle-root}}" in parameter.prompt
    assert "- {{oracle-root}} =" in parameter.prompt
    assert parameter.structured_output_schema_path is not None
    schema = json.loads(parameter.structured_output_schema_path.read_text())
    oracle_schema = json.loads(
        oracle_schema_path("oracle", "review", schema_name).read_text()
    )

    assert parameter.structured_output_schema_path.name == schema_name
    assert schema == oracle_schema
    validate({"reasons": []}, schema)
    validate({"reasons": ["oracle file の記述に基づく理由"]}, schema)


def test_oracle_review_validate_finding_advocate_preserves_dynamic_text() -> None:
    """advocate builderが動的入力内のplaceholderを補正せず保持することを検証する。"""
    finding = "finding literal `{{oracle_root}}` ツリー内 should stay"
    known_advocate = "known advocate literal `{{oracle_root}}` ツリー内 should stay"
    known_challenger = "known challenger literal `{{oracle_root}}` ツリー内 should stay"

    parameter = build_oracle_review_validate_finding_advocate_parameter(
        finding,
        known_advocate,
        known_challenger,
    )

    assert finding in parameter.prompt
    assert known_advocate in parameter.prompt
    assert known_challenger in parameter.prompt
    assert parameter.prompt.count("`{{oracle_root}}` ツリー内") == 3
    assert "`{{oracle-root}}` ツリー内" in parameter.prompt
