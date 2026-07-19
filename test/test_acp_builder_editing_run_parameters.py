"""新しい editing workload の canonical builder adapter を検証する。"""

from pathlib import Path

from acp.builder.oracle.edit.fork.launch_exec import (
    build_oracle_edit_fork_launch_exec_parameter,
)
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


def test_oracle_edit_fork_builder_returns_complete_exec_prompt() -> None:
    worktree = Path.cwd()

    parameter = build_oracle_edit_fork_launch_exec_parameter(
        "oracle の最終状態を更新する",
        worktree,
    )

    assert parameter.model_class == ModelClass.FLAGSHIP
    assert parameter.reasoning_effort == ReasoningEffort.MAX
    assert parameter.file_access_mode == FileAccessMode.PURE_ORACLE_WRITE
    assert parameter.structured_output_schema_path is None
    assert parameter.cwd == worktree.resolve()
    assert "oracle の最終状態を更新する" in parameter.prompt


def test_realization_apply_builder_embeds_commit_range_and_raw_diff() -> None:
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
    assert summary.file_access_mode == FileAccessMode.READONLY
    assert summary.structured_output_schema_path is not None
    assert summary.structured_output_schema_path.name == "change_summary.json"
