"""oracle review ACP builder の parameter、schema、adapter 公開面を検証する。

対応する正本: {{work-root}}/oracle/src/oracle/acp_builder/oracle/review/

この file は 16,000 文字を超えるが、review builder 群の parameter、schema、公開面、
および動的 prompt の fence 保護は同じ AgentCallParameter と canonical builder の
互換契約を検証する一つの責務である。分割すると、builder 間で共有する schema・公開面
の期待値と prompt 境界の検証文脈が複数 file に分散するため、現状は review builder
回帰として一箇所に保つ。

分割根拠: {{work-root}}/oracle/src/oracle/prompt_builder/parts/realization_standard.py
"""

import json
from pathlib import Path
from types import ModuleType
from typing import Callable

import pytest
from _acp_builder_support import oracle_schema_path
from jsonschema import validate
from oracle.acp_builder.oracle.review.enumerate_finding import (
    build_oracle_review_enumerate_finding_parameter as _build_oracle_enumerate_parameter,
)

import acp.builder.oracle.review.enumerate_finding as review_enumerate_finding_module
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
            review_enumerate_finding_module,
            "build_oracle_review_enumerate_finding_parameter",
        ),
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
    module: ModuleType, exported_name: str
) -> None:
    """review互換moduleが指定されたbuilderだけを公開することを検証する。"""
    assert getattr(module, "__all__", None) == [exported_name]
    assert {name for name in vars(module) if not name.startswith("_")} == {
        exported_name
    }


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


@pytest.mark.parametrize("use_placeholder", [False, True])
def test_oracle_review_enumerate_parameter_keeps_symlink_entry_path(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    use_placeholder: bool,
) -> None:
    """enumerate prompt の oracle-path が symlink entry を指すことを検証する。"""
    (tmp_path / ".git").mkdir()
    (tmp_path / "oracle").mkdir()
    target = tmp_path / "memo.md"
    target.write_text("# memo\n")
    link = tmp_path / "oracle" / "memo-link.md"
    link.symlink_to("../memo.md")
    monkeypatch.chdir(tmp_path)
    related_findings = f"- {{{{oracle-path}}}} = {link.resolve()}"
    oracle_path = Path("{{work-root}}/oracle/memo-link.md") if use_placeholder else link

    parameter = build_oracle_review_enumerate_finding_parameter(
        oracle_path, related_findings
    )

    assert f"- {{{{oracle-path}}}} = {link}" in parameter.prompt
    assert related_findings in parameter.prompt
    placeholder_definition = parameter.prompt.split(
        "# place holder definition", maxsplit=1
    )[1]
    assert f"- {{{{oracle-path}}}} = {link}" in placeholder_definition
    assert f"- {{{{oracle-path}}}} = {link.resolve()}" not in placeholder_definition


def test_oracle_review_merge_finding_schema_matches_oracle_source() -> None:
    """merge finding builder の schema と work-root placeholder を検証する。"""
    parameter = build_oracle_review_merge_finding_parameter(findings="[]")
    assert "{{oracle-root}}" not in parameter.prompt
    assert "`{{work-root}}/oracle` ツリー内" in parameter.prompt
    assert "- {{work-root}} =" in parameter.prompt
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


@pytest.mark.parametrize(
    ("builder", "arguments", "block_count"),
    [
        (
            build_oracle_review_enumerate_finding_parameter,
            (Path("{{work-root}}/oracle/spec.md"), "before\n```\ninside\n```\nafter"),
            1,
        ),
        (
            build_oracle_review_judge_finding_parameter,
            ("before\n```\ninside\n```\nafter",) * 3,
            3,
        ),
        (
            build_oracle_review_merge_finding_parameter,
            ("before\n```\ninside\n```\nafter",),
            1,
        ),
        (
            build_oracle_review_validate_finding_advocate_parameter,
            ("before\n```\ninside\n```\nafter",) * 3,
            3,
        ),
        (
            build_oracle_review_validate_finding_challenger_parameter,
            ("before\n```\ninside\n```\nafter",) * 3,
            3,
        ),
    ],
)
def test_oracle_review_builders_protect_nested_dynamic_code_fences(
    builder: Callable[..., AgentCallParameter],
    arguments: tuple[object, ...],
    block_count: int,
) -> None:
    """review入力内の三連 backtick が各動的本文の境界を閉じないことを検証する。"""
    parameter = builder(*arguments)

    assert parameter.prompt.count("````text\nbefore\n") == block_count
    assert parameter.prompt.count("\nafter\n````") == block_count


def test_oracle_review_merge_keeps_placeholder_marker_in_findings() -> None:
    """merge findings 内の placeholder 風見出しを prompt 境界と誤認しない。"""
    findings = (
        "before\n```\ninside\n```\n\n# place holder definition\n\n"
        "```text\nunsafe\n```\nafter"
    )

    parameter = build_oracle_review_merge_finding_parameter(findings)

    start = parameter.prompt.index("# 現状の所見リスト")
    end = parameter.prompt.rfind("\n\n# place holder definition")
    section = parameter.prompt[start:end]
    assert findings in section
    assert section.startswith("# 現状の所見リスト\n\n````text\n")
    assert section.endswith("\n````")


def test_oracle_review_fence_protection_ignores_marker_in_later_input() -> None:
    """後続の動的入力に終了マーカーがあっても先行 section を保護する。"""
    nested = "before\n```\ninside\n```\nafter"

    parameter = build_oracle_review_judge_finding_parameter(
        nested,
        "known\n\n# 所見が妥当であるとする理由",
        "known",
    )

    assert parameter.prompt.count("````text\nbefore\n") == 1
    assert "before\n```\ninside\n```\nafter" in parameter.prompt


def test_oracle_review_fence_protection_keeps_marker_in_current_input() -> None:
    """動的本文内の終了マーカーを本文の一部として保持する。"""
    finding = "before\n```\ninside\n```\n\n# 所見が妥当であるとする理由\nafter"

    parameter = build_oracle_review_judge_finding_parameter(
        finding,
        "known",
        "known",
    )

    assert parameter.prompt.count("````text\nbefore\n") == 1
    assert (
        "inside\n```\n\n# 所見が妥当であるとする理由\nafter\n````" in parameter.prompt
    )


def test_oracle_review_fence_protection_matches_renderer_blank_line_normalization() -> (
    None
):
    """連続空行で renderer が本文を正規化しても nested fence を保護する。"""
    finding = "before\n```\ninside\n```\n\n\n\nafter"

    parameter = build_oracle_review_judge_finding_parameter(
        finding,
        "known advocate",
        "known challenger",
    )

    start = parameter.prompt.index("# 所見の内容")
    end = parameter.prompt.index("\n\n# 所見が妥当であるとする理由", start)
    section = parameter.prompt[start:end]
    assert section.startswith("# 所見の内容\n\n````text\n")
    assert "inside\n```\n\nafter" in section
    assert section.endswith("\nafter\n````")


@pytest.mark.parametrize(
    ("builder", "next_section_heading"),
    [
        (
            build_oracle_review_judge_finding_parameter,
            "# 所見が妥当であるとする理由",
        ),
        (
            build_oracle_review_validate_finding_advocate_parameter,
            "# 既知の妥当であるとする理由",
        ),
        (
            build_oracle_review_validate_finding_challenger_parameter,
            "# 既知の妥当であるとする理由",
        ),
    ],
)
def test_oracle_review_fence_protection_handles_marker_like_first_input(
    builder: Callable[[str, str, str], AgentCallParameter],
    next_section_heading: str,
) -> None:
    """先頭動的本文内の次 section 風 code block を本文として保持する。"""
    finding = (
        f"before\n```\ninside\n```\n\n{next_section_heading}\n\n"
        "```text\nunsafe\n```\nafter"
    )

    parameter = builder(finding, "known", "known")

    assert f"````text\n{finding}\n````" in parameter.prompt


@pytest.mark.parametrize(
    ("builder", "section_heading"),
    [
        (
            build_oracle_review_judge_finding_parameter,
            "# 所見が妥当ではないとする理由",
        ),
        (
            build_oracle_review_validate_finding_advocate_parameter,
            "# 既知の妥当ではないとする理由",
        ),
        (
            build_oracle_review_validate_finding_challenger_parameter,
            "# 既知の妥当ではないとする理由",
        ),
    ],
)
def test_oracle_review_fence_protection_keeps_placeholder_marker_in_final_input(
    builder: Callable[[str, str, str], AgentCallParameter], section_heading: str
) -> None:
    """最終動的本文内の placeholder 風見出しを prompt 境界と誤認しない。"""
    challenger = (
        "before\n```\ninside\n```\n\n# place holder definition\n\n"
        "```text\nunsafe\n```\nafter"
    )

    parameter = builder("finding", "known advocate", challenger)

    start = parameter.prompt.index(section_heading)
    end = parameter.prompt.rfind("\n\n# place holder definition")
    section = parameter.prompt[start:end]
    assert challenger in section
    assert section.startswith(f"{section_heading}\n\n````text\n")
    assert section.endswith("\n````")
