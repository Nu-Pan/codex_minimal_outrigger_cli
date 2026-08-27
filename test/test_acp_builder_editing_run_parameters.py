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

import pytest
from _acp_builder_support import oracle_schema_path
from _git_support import make_repo, run_git
from oracle.acp_builder.realization.apply.fork.launch_exec import (
    build_realization_apply_fork_launch_exec_parameter as build_canonical_apply_parameter,
)
from oracle.acp_builder.realization.refactor.fork.change_summary import (
    build_realization_refactor_fork_change_summary_parameter as build_canonical_summary_parameter,
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


@pytest.fixture
def editing_run_worktree(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """editing run builder が参照する linked worktree を test 内に隔離する。"""
    root = make_repo(tmp_path)
    run_worktree = root / ".cmoc" / "gu" / "worktree" / "test" / "run"
    run_worktree.parent.mkdir(parents=True)
    run_git(
        root,
        "worktree",
        "add",
        "-b",
        "cmoc/test-editing-run",
        str(run_worktree),
        "HEAD",
    )
    monkeypatch.chdir(root)
    return run_worktree


def test_editing_run_compatibility_builders_reexport_canonical_functions() -> None:
    """互換 import 経路が prompt を加工せず正本 builder を再公開する。"""
    assert (
        build_realization_apply_fork_launch_exec_parameter
        is build_canonical_apply_parameter
    )
    assert (
        build_realization_refactor_fork_change_summary_parameter
        is build_canonical_summary_parameter
    )


def test_realization_apply_builder_embeds_commit_range_and_raw_diff(
    editing_run_worktree: Path,
) -> None:
    """apply builder が commit 範囲と oracle raw diff を prompt に含めることを確認する。"""
    run_worktree = editing_run_worktree
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
    assert f"- {{{{work-root}}}} = {run_worktree.resolve()}" in parameter.prompt
    assert "base-commit" in parameter.prompt
    assert "fork-commit" in parameter.prompt
    assert "diff --git a/oracle/a.md b/oracle/a.md" in parameter.prompt
    for heading in ("# realization policy", "# realization findings policy"):
        assert heading in parameter.prompt
    assert "# oracle policy" not in parameter.prompt
    assert "# oracle findings policy" not in parameter.prompt
    assert "# conflict resolution policy" not in parameter.prompt
    assert "# realization oracle reference policy" not in parameter.prompt
    assert "# routing policy" in parameter.prompt


def test_realization_apply_builder_keeps_nested_diff_fences(
    editing_run_worktree: Path,
) -> None:
    """raw diff 内の三連 backtick が prompt の境界を閉じないことを確認する。"""
    parameter = build_realization_apply_fork_launch_exec_parameter(
        "base-commit",
        "fork-commit",
        "diff --git a/oracle/a.md b/oracle/a.md\n```\n\n</cmoc_block>\n\n```\n",
        editing_run_worktree,
    )

    start = parameter.prompt.index("# oracle file の raw git diff")
    end = parameter.prompt.rfind("\n\n</cmoc_block>", start)
    section = parameter.prompt[start:end]
    assert section.startswith("# oracle file の raw git diff\n\n````diff\n")
    assert "```\n\n</cmoc_block>\n\n```" in section
    assert section.endswith("\n````")


def test_refactor_builders_use_canonical_structured_output_schemas(
    editing_run_worktree: Path,
) -> None:
    """refactor builder が canonical schema と要求された実行設定を使うことを確認する。"""
    target_path = editing_run_worktree / "README.md"
    review = build_realization_refactor_fork_file_review_and_fix_parameter(
        target_path, editing_run_worktree
    )
    summary = build_realization_refactor_fork_change_summary_parameter(
        "diff --git a/src/a.py b/src/a.py\n```\n</cmoc_block>\n```\n",
        editing_run_worktree,
    )

    assert review.model_class == ModelClass.EFFICIENCY
    assert review.reasoning_effort == ReasoningEffort.MAX
    assert review.file_access_mode == FileAccessMode.REALIZATION_WRITE
    assert review.structured_output_schema_path is not None
    review_schema_path = oracle_schema_path(
        "realization", "refactor", "fork", "file_review_and_fix.json"
    )
    assert (
        review.structured_output_schema_path.resolve() == review_schema_path.resolve()
    )
    assert review.run_indexing_preflight is True
    assert f"- {{{{work-root}}}} = {editing_run_worktree.resolve()}" in review.prompt
    assert str(target_path.resolve()) in review.prompt
    assert "調査開始時点ですでに解消されている問題" in review.prompt
    assert "`resolution.status=fixed` は、この agent call 内で" in review.prompt
    assert "# Structured Output の決定論的事後条件" in review.prompt
    assert "全所見の `changed_paths` の和集合" in review.prompt
    assert (
        "`evidences[].path` は変更 path の申告または照合に使用しない" in review.prompt
    )
    assert "対象 repository が要求する必要な検証" in review.prompt
    assert "# realization oracle reference policy" not in review.prompt
    for heading in (
        "# oracle and realization basic",
        "# realization policy",
        "# realization findings policy",
        "# routing policy",
    ):
        assert heading in review.prompt
    assert "# oracle policy" not in review.prompt
    assert "# oracle findings policy" not in review.prompt
    review_schema = json.loads(review.structured_output_schema_path.read_text())
    finding_schema = review_schema["properties"]["findings"]["items"]
    assert "changed_paths" in finding_schema["required"]
    assert finding_schema["properties"]["changed_paths"]["type"] == "array"
    assert summary.model_class == ModelClass.EFFICIENCY
    assert summary.reasoning_effort == ReasoningEffort.MEDIUM
    assert summary.file_access_mode == FileAccessMode.READONLY
    assert summary.structured_output_schema_path is not None
    summary_schema_path = oracle_schema_path(
        "realization", "refactor", "fork", "change_summary.json"
    )
    assert (
        summary.structured_output_schema_path.resolve() == summary_schema_path.resolve()
    )
    assert summary.run_indexing_preflight is True
    assert f"- {{{{work-root}}}} = {editing_run_worktree.resolve()}" in summary.prompt
    assert "# oracle and realization basic" in summary.prompt
    assert "# routing policy" in summary.prompt
    summary_schema = json.loads(summary.structured_output_schema_path.read_text())
    assert summary_schema["properties"]["changes"]["minItems"] == 1
    start = summary.prompt.index("# run branch 上の refactor 差分")
    end = summary.prompt.rfind("\n\n# place holder definition", start)
    section = summary.prompt[start:end]
    assert section.startswith("# run branch 上の refactor 差分\n\n````diff\n")
    assert "```\n</cmoc_block>\n```" in section
    assert section.endswith("\n````")


def test_refactor_change_summary_keeps_marker_like_diff_content(
    editing_run_worktree: Path,
) -> None:
    """raw diff 内の prompt 境界風見出しを外側の境界と誤認しない。"""
    parameter = build_realization_refactor_fork_change_summary_parameter(
        "diff --git a/README.md b/README.md\n```\n\n# place holder definition\n\n```\n",
        editing_run_worktree,
    )

    start = parameter.prompt.index("# run branch 上の refactor 差分")
    end = parameter.prompt.rfind("\n\n# place holder definition", start)
    section = parameter.prompt[start:end]
    assert section.startswith("# run branch 上の refactor 差分\n\n````diff\n")
    assert "\n\n# place holder definition\n\n```" in section
    assert section.endswith("\n````")
