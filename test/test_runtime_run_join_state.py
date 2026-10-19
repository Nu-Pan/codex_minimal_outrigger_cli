"""join の Git 照合を、worktree 作成や CLI 前処理を重ねずに検証する。"""

from dataclasses import replace
from unittest.mock import Mock

import pytest
from _git_support import RUN_BRANCH, SESSION_BRANCH, SESSION_ID, run_git

import commons.runtime_git as git_module
import commons.runtime_run_join as run_join
import commons.runtime_run_join_state as join_state
from commons.runtime_errors import CmocError
from commons.runtime_git import head_commit
from commons.runtime_run_lifecycle import EditingRunContext, commit_work_unit


@pytest.fixture
def imported_record(committed_repository):
    root = committed_repository
    baseline = head_commit(root)
    (root / "result.txt").write_text("prepared result\n")
    prepared = commit_work_unit(root, "prepared result")
    tree = join_state.tree_id(root, prepared)
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
        kind="realization_apply",
        run_branch=RUN_BRANCH,
        run_fork_commit=baseline,
        run_worktree=root / "removed-run",
    )
    return join_state.JoinRecord(
        context,
        prepared,
        session_head=baseline,
        prepared_run_head=prepared,
        imported=True,
        join_commit=imported,
        session_commit=imported,
        session_tree=tree,
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
            session_commit=record.prepared_run_head,
            session_head=record.prepared_run_head,
            join_commit=None,
        ),
    )
    queries = Mock(wraps=join_state.run_git)
    monkeypatch.setattr(join_state, "run_git", queries)

    for receipt in records:
        queries.reset_mock()
        assert join_state.confirm_import(receipt)
        assert 0 < queries.call_count <= 2
    # 成功済みの判定を持ち越さず、session ref の変更を次回の照合で拒否する。
    run_git(root, "update-ref", SESSION_BRANCH, record.context.run_fork_commit)
    for receipt in records:
        with pytest.raises(CmocError, match="取り込み成果を確認できません"):
            join_state.confirm_import(receipt)


def test_import_confirmation_rejects_inconsistent_receipt(imported_record):
    record = imported_record
    baseline = record.context.run_fork_commit
    mismatches = [
        {"session_tree": join_state.tree_id(record.context.repo, baseline)},
        {"prepared_run_head": baseline},
        {"session_head": record.prepared_run_head},
        {"join_commit": baseline},
        {"join_commit": None},
        {"session_commit": None},
        {"session_commit": record.session_tree},
        {"prepared_run_head": record.session_tree},
    ]
    for mismatch in mismatches:
        with pytest.raises(CmocError):
            join_state.confirm_import(replace(record, **mismatch))


def test_missing_receipt_checks_candidate_tree_and_parents(
    imported_record, monkeypatch
):
    root = imported_record.context.repo
    imported = imported_record.join_commit
    queries = Mock(wraps=join_state.run_git)
    monkeypatch.setattr(join_state, "run_git", queries)

    # 各候補は同じ基準から分岐させ、復旧で書き換わる記録は毎回作り直す。
    for mismatch in (None, "tree", "parent_order"):
        if mismatch is not None:
            tree = imported_record.session_tree
            parents = [imported_record.session_head, imported_record.prepared_run_head]
            if mismatch == "tree":
                tree = join_state.tree_id(root, imported_record.session_head)
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
            session_commit=None,
            session_tree=None,
        )
        # durable 保存と CLI の復旧は test_editing_run_cli.py に残す。
        save = Mock()
        monkeypatch.setattr(record, "save", save)
        queries.reset_mock()

        assert join_state.confirm_import(record) is (mismatch is None), mismatch
        assert 0 < queries.call_count <= 2, mismatch
        if mismatch is None:
            assert record.imported
            assert record.join_commit == record.session_commit == imported
            assert record.session_tree == imported_record.session_tree
            save.assert_called_once_with()
        else:
            assert not record.imported
            assert (
                record.join_commit
                is record.session_commit
                is record.session_tree
                is None
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
    run_git(root, "branch", context.run_branch, record.prepared_run_head)
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
    run_git(root, "update-ref", branch_ref, record.prepared_run_head)
    inspect(True)

    # branch が一致しても、残存 worktree の別 HEAD・未確定差分は削除しない。
    run_git(root, "switch", "--detach", context.run_fork_commit)
    inspect(False)
    run_git(root, "switch", "--detach", record.prepared_run_head)
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
