"""両 join の統合対象と共通の競合解消 call の契約を検証する。

対応する正本:
- {{work-root}}/reference/src/oracle/request_builder/common/conflict_resolution.py
- {{work-root}}/spec/app_spec/codex_common_rule.md
- {{work-root}}/spec/app_spec/merge_conflict_resolution.md
"""

from dataclasses import replace
from pathlib import Path

import oracle.other.path_model as path_model_module
import pytest
from _codex_support import codex_arg_value, codex_override_config
from oracle.request_builder.basic import FileAccessMode
from oracle.request_builder.run.join.conflict_resolution import (
    build_run_join_conflict_resolution_request,
)
from oracle.request_builder.session.join.conflict_resolution import (
    build_session_join_conflict_resolution_request,
)

from commons.runtime_codex_profile import build_codex_override_args
from config.cmoc_config import CmocConfig


@pytest.fixture
def merge_worktree(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """process cwd と異なる merge worktree から context を構築させる。"""
    # 実 Git の root 解決は test_basic_runtime.py と session join 結合 test に残す。
    worktree = tmp_path / "merge"
    worktree.mkdir()

    def _resolve_worktree_roots(agent_call_cwd: Path) -> tuple[Path, Path]:
        assert agent_call_cwd == worktree.resolve()
        return worktree.resolve(), tmp_path.resolve()

    monkeypatch.setattr(
        path_model_module, "_resolve_git_worktree_roots", _resolve_worktree_roots
    )
    monkeypatch.chdir(tmp_path)
    return worktree


@pytest.mark.parametrize("join_kind", ["run", "session"])
def test_join_conflict_resolution_passes_inputs_and_shared_launch_parameters(
    merge_worktree: Path,
    join_kind: str,
) -> None:
    """コマンド別の引数を対応付け、共通の規定・編集範囲・設定を渡す。"""

    source, target = "c" * 40, "d" * 40
    if join_kind == "run":
        parameter = build_run_join_conflict_resolution_request(
            target, source, merge_worktree
        )
    else:
        parameter = build_session_join_conflict_resolution_request(
            target, source, merge_worktree
        )

    assert parameter.agent_call_kind == "build_merge_conflict_resolution_request"
    assert parameter.file_access_mode == FileAccessMode.SPEC_AND_REALIZATION_WRITE
    assert parameter.structured_output_schema_path is None
    assert parameter.agent_call_cwd == merge_worktree.resolve()
    assert (
        f"- {{{{repo-root}}}} = {merge_worktree.parent.resolve()}" in parameter.prompt
    )
    assert f"- {{{{work-root}}}} = {merge_worktree.resolve()}" in parameter.prompt
    assert f"- source（取り込む側）: `{source}`" in parameter.prompt
    assert f"- target（取り込み先の merge 前）: `{target}`" in parameter.prompt
    assert "共通祖先" in parameter.prompt
    assert "進行中の merge の Git index" in parameter.prompt
    assert "conflict 対象ファイル" not in parameter.prompt
    objective = parameter.prompt.split('<cmoc_block id="objective">', 1)[1].split(
        "</cmoc_block>", 1
    )[0]
    assert "# task" in objective
    assert "進行中の merge" in objective
    assert parameter.enable_document_search_mcp is True
    policy_heading = "# conflict resolution policy\n"
    assert parameter.prompt.count(policy_heading) == 1
    policy = parameter.prompt.split(policy_heading, 1)[1].split("\n# ", 1)[0]
    assert [
        line
        for line in policy.splitlines()
        if line in {"**必須**", "**禁止**", "**許容**", "**例外**", "**補足情報**"}
    ] == ["**必須**", "**禁止**", "**許容**"]
    assert "両 branch の両立可能な変更" in policy
    assert "妥当な解決方法が複数ある場合" in policy
    assert "規定に違反する解消結果" in policy
    assert "初期の競合一覧にないファイル" in policy
    assert "解決不能な場合、未解消のままで良い" in policy
    assert "merge_resolution:" not in policy
    assert (
        parameter.prompt.index("# realization policy\n")
        < parameter.prompt.index(policy_heading)
        < parameter.prompt.index("# 管理操作との境界\n")
    )
    assert "# routing policy" in parameter.prompt
    for heading in ("# spec policy", "# realization policy"):
        assert heading in parameter.prompt
    assert "# realization findings policy" not in parameter.prompt
    assert "merge_resolution: resolved" in parameter.prompt
    assert "merge_resolution: unresolved" in parameter.prompt
    assert "新しい人間意図の選択が必要な場合" in parameter.prompt
    assert (
        "未解消の場合も merge の中止や作業状態の復旧を自分で行わず" in parameter.prompt
    )
    assert 'target="sealed_feedback_result"' not in parameter.prompt
    # source/target の対応は上で検査済み。argv の prompt 非依存性には
    # prompt の参照入力だけを変え、完全 prompt を再構築しない。
    changed_input_parameter = replace(
        parameter,
        prompt=parameter.prompt.replace(source, "e" * 40).replace(target, "f" * 40),
    )
    config = CmocConfig()
    args = build_codex_override_args(parameter, config)
    changed_input_args = build_codex_override_args(changed_input_parameter, config)

    assert args == changed_input_args
    assert codex_arg_value(args, "--sandbox") == "workspace-write"
    assert all(source not in arg and target not in arg for arg in args)
    parsed = codex_override_config(args)
    assert "permissions" not in parsed
    assert "default_permissions" not in parsed


def test_join_builders_produce_the_same_request_for_the_same_merge(
    merge_worktree: Path,
) -> None:
    """コマンドの違いだけで、文面・起動設定・編集範囲を変えない。"""
    run = build_run_join_conflict_resolution_request("target", "source", merge_worktree)
    session = build_session_join_conflict_resolution_request(
        "target", "source", merge_worktree
    )

    assert run == session


def test_feedback_join_adds_sealed_result_input_without_changing_launch_settings(
    merge_worktree: Path,
) -> None:
    """封印済み結果を参照入力に加え、通常 join と同じ受理・権限で検証する。"""
    plain = build_run_join_conflict_resolution_request("run", "session", merge_worktree)
    sealed = build_run_join_conflict_resolution_request(
        "run",
        "session",
        merge_worktree,
        feedback_report_cut_path=Path("{{work-root}}/sealed/report-cut.json"),
    )

    assert replace(sealed, prompt=plain.prompt) == plain
    assert sealed.prompt.count("# conflict resolution policy\n") == 1
    assert (
        sealed.prompt.split("# 管理操作との境界\n", 1)[0]
        == plain.prompt.split("# 管理操作との境界\n", 1)[0]
    )
    assert str(merge_worktree / "sealed/report-cut.json") in sealed.prompt
    assert sealed.prompt.count('<cmoc_block id="sealed_feedback_result">') == 1
    assert "読み取り専用で確認すること" in sealed.prompt
    assert "結果分類そのものの変更が必要な場合" in sealed.prompt
    assert "未解消として具体的な理由を報告すること" in sealed.prompt
    assert "issue 処理のやり直しや対象外 issue の探索を行わないこと" in sealed.prompt
