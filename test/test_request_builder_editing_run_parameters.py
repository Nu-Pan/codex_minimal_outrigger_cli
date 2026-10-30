"""editing run workload の正本 builder と残る adapter を検証する。

対応する oracle file:
- `{{work-root}}/reference/src/oracle/request_builder/decision/apply/launch_exec.py`
- `{{work-root}}/reference/src/oracle/request_builder/realization/refactor/file_review_and_fix.py`
- `{{work-root}}/reference/src/oracle/request_builder/realization/refactor/file_review_and_fix.json`
"""

import json
from pathlib import Path

import oracle.other.path_model as path_model_module
import pytest
from _request_builder_support import oracle_schema_path
from oracle.request_builder.decision.apply.launch_exec import (
    build_decision_apply_realization_request,
)
from oracle.request_builder.realization.refactor.file_review_and_fix import (
    build_realization_refactor_request as build_canonical_review_parameter,
)

from acp.builder.realization.refactor.fork.file_review_and_fix import (
    build_realization_refactor_request,
)
from basic.acp import FileAccessMode


def _objective_section(prompt: str) -> str:
    """完全 prompt から caller 固有 objective block の本文を取り出す。"""
    return prompt.split('<cmoc_block id="objective">', 1)[1].split("</cmoc_block>", 1)[
        0
    ]


@pytest.fixture
def editing_run_paths(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> tuple[Path, Path]:
    """builder の cwd と root の受け渡しを、Git 探索結果だけ置換して検証する。"""
    # Git metadata の解決は test_basic_runtime.py と fork 統合 test に残す。
    root = tmp_path / "repo"
    run_worktree = tmp_path / "run"
    root.mkdir()
    run_worktree.mkdir()

    def _resolve_worktree_roots(agent_call_cwd: Path) -> tuple[Path, Path]:
        # process cwd ではなく、builder が指定した run cwd の探索を検査する。
        assert agent_call_cwd == run_worktree.resolve()
        return run_worktree.resolve(), root.resolve()

    monkeypatch.setattr(
        path_model_module, "_resolve_git_worktree_roots", _resolve_worktree_roots
    )
    monkeypatch.chdir(root)
    return root, run_worktree


def test_refactor_compatibility_builder_reexports_canonical_function() -> None:
    """互換 import 経路が prompt を加工せず正本 builder を再公開する。"""
    assert build_realization_refactor_request is build_canonical_review_parameter


def test_decision_apply_builder_passes_commit_references(
    editing_run_paths: tuple[Path, Path],
) -> None:
    """apply builder が commit 参照と取得条件を prompt に含める。"""
    root, run_worktree = editing_run_paths
    parameter = build_decision_apply_realization_request(
        "base-commit",
        "fork-commit",
        run_worktree,
    )

    assert parameter.file_access_mode == FileAccessMode.REALIZATION_WRITE
    assert parameter.structured_output_schema_path is None
    assert parameter.enable_document_search_mcp is True
    assert parameter.agent_call_cwd == run_worktree.resolve()
    assert f"- {{{{repo-root}}}} = {root.resolve()}" in parameter.prompt
    assert f"- {{{{work-root}}}} = {run_worktree.resolve()}" in parameter.prompt
    assert "base-commit" in parameter.prompt
    assert "fork-commit" in parameter.prompt
    assert "diff --git" not in parameter.prompt
    assert (
        "始点・終点のいずれかで decision, reference, spec だったファイル"
        in parameter.prompt
    )
    assert "差分を取得できない場合は失敗として報告" in parameter.prompt
    objective = _objective_section(parameter.prompt)
    assert "# task" in objective
    assert "decision, reference, spec の変更を realization に反映" in objective
    assert "# scope" in objective
    assert "修正対象は `{{work-root}}` ツリー内の realization すべて" in objective
    assert "# completion criteria" in objective
    assert (
        "終点の decision, reference, spec と作業結果の realization との間に齟齬がない"
        in objective
    )
    for heading in ("# realization policy", "# realization findings policy"):
        assert heading in parameter.prompt
    assert "# oracle policy" not in parameter.prompt
    assert "# conflict resolution policy" not in parameter.prompt
    assert "# realization oracle reference policy" not in parameter.prompt
    assert "# routing policy" in parameter.prompt


def test_refactor_builders_use_canonical_structured_output_schemas(
    editing_run_paths: tuple[Path, Path],
) -> None:
    """refactor builder が canonical schema と要求された実行設定を使うことを確認する。"""
    root, run_worktree = editing_run_paths
    target_path = run_worktree / "README.md"
    review = build_realization_refactor_request(target_path, run_worktree)

    assert review.file_access_mode == FileAccessMode.REALIZATION_WRITE
    assert review.structured_output_schema_path is not None
    review_schema_path = oracle_schema_path(
        "realization", "refactor", "file_review_and_fix.json"
    )
    assert (
        review.structured_output_schema_path.resolve() == review_schema_path.resolve()
    )
    assert review.enable_document_search_mcp is True
    assert review.agent_call_cwd == run_worktree.resolve()
    assert f"- {{{{repo-root}}}} = {root.resolve()}" in review.prompt
    assert f"- {{{{work-root}}}} = {run_worktree.resolve()}" in review.prompt
    assert str(target_path.resolve()) in review.prompt
    assert "調査開始時点ですでに解消されている問題" in review.prompt
    assert "# Structured Output の決定論的事後条件" in review.prompt
    assert "全所見の `changed_paths` の和集合" in review.prompt
    assert (
        "`evidences[].path` は変更 path の申告または照合に使用しない" in review.prompt
    )
    review_objective = _objective_section(review.prompt)
    assert "# task" in review_objective
    assert "# scope" in review_objective
    assert "# completion criteria" in review_objective
    assert "この agent call 内で修正後の再調査と所定の検証を終えている" in (
        review_objective
    )
    assert "# realization oracle reference policy" not in review.prompt
    for heading in (
        "# oracle and realization basic",
        "# realization policy",
        "# realization findings policy",
        "# routing policy",
    ):
        assert heading in review.prompt
    assert "# oracle policy" not in review.prompt
    review_schema = json.loads(review.structured_output_schema_path.read_text())
    finding_schema = review_schema["properties"]["findings"]["items"]
    assert "changed_paths" in finding_schema["required"]
    assert finding_schema["properties"]["changed_paths"]["type"] == "array"
    assert "verification" in review_schema["required"]
    assert review_schema["properties"]["verification"]["properties"]["status"][
        "enum"
    ] == [
        "passed",
        "not_required",
        "failed",
        "incomplete",
    ]
    assert "テストと実装のムダ" in review_objective
    assert "必要な回帰検出能力" in review_objective
    assert "focused test だけで済ませたり" in review.prompt
    assert "Real Codex CLI を使う test" in review.prompt
