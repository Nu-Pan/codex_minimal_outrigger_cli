"""editing run workload の canonical builder adapter を検証する。"""

import json
from pathlib import Path

from acp.builder.realization.apply.fork.launch_exec import (
    build_realization_apply_fork_launch_exec_parameter,
)
from acp.builder.realization.refactor.fork.change_summary import (
    build_realization_refactor_fork_change_summary_parameter,
)
from acp.builder.realization.refactor.fork.file_review_and_fix import (
    build_realization_refactor_fork_file_review_and_fix_parameter,
)
from basic.acp import FileAccessMode, ModelClass, ReasoningEffort


def test_realization_apply_builder_embeds_commit_range_and_raw_diff() -> None:
    """apply builder が commit 範囲と oracle raw diff を prompt に含めることを確認する。"""
    parameter = build_realization_apply_fork_launch_exec_parameter(
        "base-commit",
        "fork-commit",
        "diff --git a/oracle/a.md b/oracle/a.md\n",
        Path.cwd(),
    )

    assert parameter.file_access_mode == FileAccessMode.REALIZATION_WRITE
    assert parameter.structured_output_schema_path is None
    assert "base-commit" in parameter.prompt
    assert "fork-commit" in parameter.prompt
    assert "diff --git a/oracle/a.md b/oracle/a.md" in parameter.prompt


def test_refactor_builders_use_canonical_structured_output_schemas() -> None:
    """refactor builder が canonical schema と要求された実行設定を使うことを確認する。"""
    review = build_realization_refactor_fork_file_review_and_fix_parameter(
        Path(__file__)
    )
    summary = build_realization_refactor_fork_change_summary_parameter(
        "diff --git a/src/a.py b/src/a.py\n"
    )

    assert review.model_class == ModelClass.EFFICIENCY
    assert review.reasoning_effort == ReasoningEffort.MAX
    assert review.file_access_mode == FileAccessMode.REALIZATION_WRITE
    assert review.structured_output_schema_path is not None
    assert review.structured_output_schema_path.name == "file_review_and_fix.json"
    assert str(Path(__file__).resolve()) in review.prompt
    assert "調査開始時点の既存実装ですでに解消されている問題" in review.prompt
    assert "`resolution.status=fixed` は、この agent call 内で" in review.prompt
    review_schema = json.loads(review.structured_output_schema_path.read_text())
    findings_schema = review_schema["properties"]["findings"]
    status_schema = findings_schema["items"]["properties"]["resolution"]["properties"][
        "status"
    ]
    assert "調査開始時点で存在した" in findings_schema["description"]
    assert "実際に変更" in status_schema["description"]
    assert summary.file_access_mode == FileAccessMode.READONLY
    assert summary.structured_output_schema_path is not None
    assert summary.structured_output_schema_path.name == "change_summary.json"
