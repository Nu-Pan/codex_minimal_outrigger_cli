"""editing run workload の canonical builder adapter を検証する。

対応する oracle file:
- `{{work-root}}/oracle/src/oracle/acp_builder/realization/apply/fork/launch_exec.py`
- `{{work-root}}/oracle/src/oracle/acp_builder/realization/refactor/fork/change_summary.py`
- `{{work-root}}/oracle/src/oracle/acp_builder/realization/refactor/fork/change_summary.json`
- `{{work-root}}/oracle/src/oracle/acp_builder/realization/refactor/fork/file_review_and_fix.py`
- `{{work-root}}/oracle/src/oracle/acp_builder/realization/refactor/fork/file_review_and_fix.json`
"""

import json
from pathlib import Path

from _acp_builder_support import oracle_schema_path

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
    run_worktree = Path.cwd()
    parameter = build_realization_apply_fork_launch_exec_parameter(
        "base-commit",
        "fork-commit",
        "diff --git a/oracle/a.md b/oracle/a.md\n",
        run_worktree,
    )

    assert parameter.model_class == ModelClass.FLAGSHIP
    assert parameter.reasoning_effort == ReasoningEffort.MAX
    assert parameter.file_access_mode == FileAccessMode.REALIZATION_WRITE
    assert parameter.structured_output_schema_path is None
    assert parameter.run_indexing_preflight is True
    assert parameter.agent_call_cwd == run_worktree.resolve()
    assert "base-commit" in parameter.prompt
    assert "fork-commit" in parameter.prompt
    assert "diff --git a/oracle/a.md b/oracle/a.md" in parameter.prompt
    for heading in (
        "# oracle standard",
        "# realization standard",
        "# apply review standard",
        "# realization oracle reference rule",
    ):
        assert heading in parameter.prompt
    assert "# oracle review standard" not in parameter.prompt
    assert "# conflict resolution standard" not in parameter.prompt


def test_realization_apply_builder_keeps_nested_diff_fences() -> None:
    """raw diff 内の三連 backtick が prompt の境界を閉じないことを確認する。"""
    parameter = build_realization_apply_fork_launch_exec_parameter(
        "base-commit",
        "fork-commit",
        "diff --git a/oracle/a.md b/oracle/a.md\n```\n\n</cmoc_block>\n\n```\n",
        Path.cwd(),
    )

    start = parameter.prompt.index("# oracle file の raw git diff")
    end = parameter.prompt.rfind("\n\n</cmoc_block>", start)
    section = parameter.prompt[start:end]
    assert section.startswith("# oracle file の raw git diff\n\n````diff\n")
    assert "```\n\n</cmoc_block>\n\n```" in section
    assert section.endswith("\n````")


def test_refactor_builders_use_canonical_structured_output_schemas() -> None:
    """refactor builder が canonical schema と要求された実行設定を使うことを確認する。"""
    review = build_realization_refactor_fork_file_review_and_fix_parameter(
        Path(__file__), Path.cwd()
    )
    summary = build_realization_refactor_fork_change_summary_parameter(
        "diff --git a/src/a.py b/src/a.py\n```\n</cmoc_block>\n```\n",
        Path.cwd(),
    )

    assert review.model_class == ModelClass.EFFICIENCY
    assert review.reasoning_effort == ReasoningEffort.MAX
    assert review.file_access_mode == FileAccessMode.REALIZATION_WRITE
    assert review.structured_output_schema_path is not None
    assert review.structured_output_schema_path.name == "file_review_and_fix.json"
    assert review.run_indexing_preflight is True
    assert str(Path(__file__).resolve()) in review.prompt
    assert "調査開始時点の既存実装ですでに解消されている問題" in review.prompt
    assert "`resolution.status=fixed` は、この agent call 内で" in review.prompt
    assert "対象 repository が要求する必要な検証" in review.prompt
    assert "# realization oracle reference rule" in review.prompt
    review_schema = json.loads(review.structured_output_schema_path.read_text())
    assert review_schema == json.loads(
        oracle_schema_path(
            "realization", "refactor", "fork", "file_review_and_fix.json"
        ).read_text()
    )
    assert summary.model_class == ModelClass.EFFICIENCY
    assert summary.reasoning_effort == ReasoningEffort.MEDIUM
    assert summary.file_access_mode == FileAccessMode.READONLY
    assert summary.structured_output_schema_path is not None
    assert summary.structured_output_schema_path.name == "change_summary.json"
    assert summary.run_indexing_preflight is True
    summary_schema = json.loads(summary.structured_output_schema_path.read_text())
    assert summary_schema == json.loads(
        oracle_schema_path(
            "realization", "refactor", "fork", "change_summary.json"
        ).read_text()
    )
    start = summary.prompt.index("# run branch 上の refactor 差分")
    end = summary.prompt.rfind("\n\n# place holder definition", start)
    section = summary.prompt[start:end]
    assert section.startswith("# run branch 上の refactor 差分\n\n````diff\n")
    assert "```\n</cmoc_block>\n```" in section
    assert section.endswith("\n````")


def test_refactor_change_summary_keeps_marker_like_diff_content() -> None:
    """raw diff 内の prompt 境界風見出しを外側の境界と誤認しない。"""
    parameter = build_realization_refactor_fork_change_summary_parameter(
        "diff --git a/README.md b/README.md\n```\n\n# place holder definition\n\n```\n",
        Path.cwd(),
    )

    start = parameter.prompt.index("# run branch 上の refactor 差分")
    end = parameter.prompt.rfind("\n\n# place holder definition", start)
    section = parameter.prompt[start:end]
    assert section.startswith("# run branch 上の refactor 差分\n\n````diff\n")
    assert "\n\n# place holder definition\n\n```" in section
    assert section.endswith("\n````")
