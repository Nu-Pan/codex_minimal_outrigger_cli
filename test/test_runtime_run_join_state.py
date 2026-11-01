"""join の Git 照合を、worktree 作成や CLI 前処理を重ねずに検証する。"""

from dataclasses import replace
from unittest.mock import Mock

import pytest
from _git_support import RUN_BRANCH, SESSION_BRANCH, SESSION_ID, run_git

import commons.runtime_git as git_module
import commons.runtime_join as merge_module
import commons.runtime_run_join as run_join
import commons.runtime_run_join_state as join_state
from commons.runtime_errors import CmocError
from commons.runtime_git import current_branch, head_commit
from commons.runtime_run_lifecycle import EditingRunContext, commit_work_unit


@pytest.fixture
def imported_record(committed_repository):
    root = committed_repository
    baseline = head_commit(root)
    (root / "result.txt").write_text("prepared result\n")
    prepared = commit_work_unit(root, "prepared result")
    tree = merge_module.tree_id(root, prepared)
    imported = run_git(
        root, "commit-tree", tree, "-p", baseline, "-p", prepared, "-m", "import"
    ).stdout.strip()
    run_git(root, "branch", SESSION_BRANCH, imported)
    # 照合は保存済み成果と session 履歴を使い、削除済み run 資源を必要としない。
    context = EditingRunContext(
        repo=root,
        session_worktree=root,
        session_id=SESSION_ID,
        state_path=root / "state.json",
        session_branch=SESSION_BRANCH,
        session_fork_commit=baseline,
        kind="decision_apply",
        run_branch=RUN_BRANCH,
        run_fork_commit=baseline,
        run_worktree=root / "removed-run",
    )
    return join_state.JoinRecord(
        context,
        original_source_head=prepared,
        target_head=baseline,
        prepared_head=prepared,
        imported=True,
        join_commit=imported,
        target_commit=imported,
        target_tree=tree,
    )


def test_import_confirmation_batches_metadata_and_rechecks_reachability(
    imported_record, monkeypatch
):
    record = imported_record
    root = record.context.repo
    # 同じ履歴で merge と no-op の記録を照合し、準備用 commit を重ねない。
    records = (
        record,
        replace(
            record,
            target_commit=record.prepared_head,
            target_head=record.prepared_head,
            join_commit=None,
        ),
    )
    queries = Mock(wraps=merge_module.run_git)
    monkeypatch.setattr(merge_module, "run_git", queries)

    for receipt in records:
        queries.reset_mock()
        assert merge_module.confirm_import(receipt)
        assert 0 < queries.call_count <= 2
    # 成功済みの判定を持ち越さず、session ref の変更を次回の照合で拒否する。
    run_git(root, "update-ref", SESSION_BRANCH, record.context.run_fork_commit)
    for receipt in records:
        with pytest.raises(CmocError, match="取り込み成果を確認できません"):
            merge_module.confirm_import(receipt)


def test_import_confirmation_rejects_inconsistent_receipt(imported_record, monkeypatch):
    record = imported_record
    baseline = record.context.run_fork_commit
    mismatches = [
        {"target_tree": merge_module.tree_id(record.context.repo, baseline)},
        {"prepared_head": baseline},
        {"target_head": record.prepared_head},
        {"join_commit": baseline},
        {"join_commit": None},
        {"target_commit": None},
        {"target_commit": record.target_tree},
        {"prepared_head": record.target_tree},
    ]
    queries = Mock(wraps=merge_module.run_git)
    monkeypatch.setattr(merge_module, "run_git", queries)
    for mismatch in mismatches:
        queries.reset_mock()
        with pytest.raises(CmocError):
            merge_module.confirm_import(replace(record, **mismatch))
        # 不完全な記録は即座に、履歴・tree の不整合は metadata の照会だけで拒否する。
        assert queries.call_count <= 1, mismatch


def test_missing_receipt_checks_candidate_tree_and_parents(
    imported_record, monkeypatch
):
    root = imported_record.context.repo
    imported = imported_record.join_commit
    queries = Mock(wraps=merge_module.run_git)
    monkeypatch.setattr(merge_module, "run_git", queries)

    # 各候補は同じ基準から分岐させ、復旧で書き換わる記録は毎回作り直す。
    for mismatch in (None, "tree", "parent_order"):
        if mismatch is not None:
            tree = imported_record.target_tree
            parents = [imported_record.target_head, imported_record.prepared_head]
            if mismatch == "tree":
                tree = merge_module.tree_id(root, imported_record.target_head)
            else:
                parents.reverse()
            candidate = run_git(
                root,
                "commit-tree",
                tree,
                "-p",
                parents[0],
                "-p",
                parents[1],
                "-m",
                "different import",
            ).stdout.strip()
            run_git(root, "update-ref", SESSION_BRANCH, candidate)
        record = replace(
            imported_record,
            imported=False,
            join_commit=None,
            target_commit=None,
            target_tree=None,
        )
        # durable 保存と CLI の復旧は test_editing_run_cli.py に残す。
        save = Mock()
        monkeypatch.setattr(record, "save", save)
        queries.reset_mock()

        assert merge_module.confirm_import(record) is (mismatch is None), mismatch
        assert 0 < queries.call_count <= 2, mismatch
        if mismatch is None:
            assert record.imported
            assert record.join_commit == record.target_commit == imported
            assert record.target_tree == imported_record.target_tree
            save.assert_called_once_with()
        else:
            assert not record.imported
            assert (
                record.join_commit is record.target_commit is record.target_tree is None
            )
            save.assert_not_called()


def test_cleanup_rechecks_resources_without_repeating_branch_query(
    imported_record, monkeypatch
):
    """削除前の成果照合を一度の branch 照会で行い、次回の変更も拒否する。"""
    record = imported_record
    root = record.context.repo
    context = replace(record.context, run_worktree=root)
    branch_ref = f"refs/heads/{context.run_branch}"
    run_git(root, "branch", context.run_branch, record.prepared_head)
    queries = Mock(wraps=git_module.subprocess.run)
    monkeypatch.setattr(git_module.subprocess, "run", queries)

    def inspect(expected, active=context):
        queries.reset_mock()
        assert run_join._cleanup_run_matches_prepared(active, record) is expected
        branch_queries = [
            call.args[0]
            for call in queries.call_args_list
            if {branch_ref, context.run_branch}.intersection(call.args[0])
        ]
        assert len(branch_queries) == 1, branch_queries

    inspect(True)
    run_git(root, "update-ref", branch_ref, context.run_fork_commit)
    inspect(False)
    run_git(root, "update-ref", branch_ref, record.prepared_head)
    inspect(True)

    # branch が一致しても、残存 worktree の別 HEAD・未確定差分は削除しない。
    run_git(root, "switch", "--detach", context.run_fork_commit)
    inspect(False)
    run_git(root, "switch", "--detach", record.prepared_head)
    dirty = root / "untracked.txt"
    dirty.write_text("keep this change\n")
    inspect(False)
    assert dirty.read_text() == "keep this change\n"
    dirty.unlink()
    inspect(True)

    # 部分回収済みの資源を許容し、同名 tag を run branch と取り違えない。
    run_git(root, "branch", "-D", context.run_branch)
    run_git(root, "tag", context.run_branch, context.run_fork_commit)
    inspect(True)
    inspect(True, record.context)
    # Git 自体の照会失敗は、branch 不在と区別して削除を止める。
    inspect(False, replace(record.context, repo=root.parent))


def test_rollback_does_not_restore_tracked_runtime_data(imported_record):
    """doctor が追跡を外した管理 file を reset で古い内容へ戻さない。"""
    root = imported_record.context.repo
    evidence = root / ".cmoc/gu/evidence.txt"
    evidence.parent.mkdir(parents=True)
    evidence.write_text("old tracked data\n")
    original = commit_work_unit(root, "incorrectly tracked runtime data")
    run_git(root, "rm", "--cached", ".cmoc/gu/evidence.txt")
    (root / ".gitignore").write_text("/.cmoc/gu/\n")
    prepared = commit_work_unit(root, "untrack runtime data")
    evidence.write_text("new diagnosis and recovery evidence\n")
    context = replace(
        imported_record.context,
        run_branch=current_branch(root),
        run_worktree=root,
        session_worktree=root,
    )
    record = join_state.JoinRecord(
        context,
        original_source_head=original,
        owned_source_head=prepared,
        preparation_started=True,
    )

    with pytest.raises(CmocError, match="管理領域を再追跡"):
        merge_module.rollback_join_preparation(record)

    assert head_commit(root) == prepared
    assert evidence.read_text() == "new diagnosis and recovery evidence\n"
    assert run_git(root, "ls-files", "--", ".cmoc/gu").stdout == ""
