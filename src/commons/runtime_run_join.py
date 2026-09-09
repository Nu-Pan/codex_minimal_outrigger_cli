"""editing run の join と cleanup で共有する runtime 処理。"""

import os
from collections.abc import Callable, Collection
from pathlib import Path

from .runtime_cli import start_subcommand_step
from .runtime_doctor import run_doctor_preprocess
from .runtime_errors import CmocError
from .runtime_git import (
    branch_exists,
    current_branch,
    delete_branch,
    head_commit,
    literal_pathspec,
    remove_worktree,
    require_clean_worktree,
    run_git,
)
from .runtime_paths import refactor_state_path, repo_root, work_root
from .runtime_primary_report import update_primary_report_fields
from .runtime_refactor import sync_refactor_state
from .runtime_results import TerminalResult
from .runtime_run import (
    delete_run_process_id,
    run_process_tracking,
    stop_tracked_codex_children,
    write_run_process_id,
)
from .runtime_run_lifecycle import (
    EditingRunContext,
    GitChange,
    commit_work_unit,
    is_generated_index_path,
    refresh_indexes,
    tree_changes,
    unexpected_run_paths,
    unexpected_session_paths,
)
from .runtime_run_report import write_lifecycle_report
from .runtime_state import SessionState, load_state_for_branch, write_state


def doctor_preprocess_for_join() -> set[str]:
    """join 前の refactor state 同期を active run kind に合わせる。"""
    # join 前の state を確認し、workload が更新する state の二重同期を避ける。
    root = work_root()
    before = head_commit(root)
    sync_refactor_entries = True
    try:
        branch = current_branch(root)
        _, _, state = load_state_for_branch(repo_root(root), branch)
    except CmocError:
        # active run の詳細な事前条件は doctor 後の resolve_active_run で報告する。
        pass
    else:
        # merge 前の entry 同期は refactor state を更新する run で遅延する。
        sync_refactor_entries = state.run.kind not in {
            "realization_refactor",
            "feedback_report",
        }
    run_doctor_preprocess(root, sync_refactor_entries=sync_refactor_entries)
    after = head_commit(root)
    if before == after:
        return set()
    # doctor 自身が merge 前に同期した refactor state だけを session の差分から除外する。
    refactor_state = refactor_state_path(root).relative_to(root)
    return {
        path
        for change in tree_changes(root, before, after)
        for path in change.paths
        if Path(path) == refactor_state
    }


def validate_run_join(
    context: EditingRunContext,
    warnings: list[str],
    *,
    force_resolve: bool = False,
    session_ignored_paths: Collection[str] = (),
    run_ignored_paths: Collection[str] = (),
) -> None:
    """明示 join と self-joining workload が共有する clean・差分検査を行う。"""
    # session と run の両 worktree を clean にし、fork 以後の差分を分類する。
    require_clean_worktree(context.session_worktree)
    require_clean_worktree(context.run_worktree)
    run_changes = tree_changes(
        context.run_worktree,
        context.run_fork_commit,
    )
    session_changes = tree_changes(
        context.session_worktree,
        context.run_fork_commit,
    )
    session_unexpected = unexpected_session_paths(
        context.session_worktree,
        session_changes,
        base=context.run_fork_commit,
        ignored_paths=session_ignored_paths,
    )
    if session_unexpected:
        _raise_unexpected(
            context,
            "session branch に想定外差分があります。",
            session_unexpected,
            warnings,
        )
    run_unexpected = unexpected_run_paths(
        context,
        run_changes,
        ignored_paths=run_ignored_paths,
    )
    if run_unexpected and not force_resolve:
        _raise_unexpected(
            context,
            "run branch に想定外差分があります。",
            run_unexpected,
            warnings,
        )
    if run_unexpected:
        # force-resolve は run branch の想定外差分だけを fork commit へ戻す。
        _revert_unexpected_run_paths(context, run_changes, run_unexpected)
        warnings.append(
            "--force-resolve reverted unexpected run paths: "
            + ", ".join(run_unexpected)
        )
        run_changes = tree_changes(
            context.run_worktree,
            context.run_fork_commit,
        )
        remaining = unexpected_run_paths(
            context,
            run_changes,
            ignored_paths=run_ignored_paths,
        )
        if remaining:
            _raise_unexpected(
                context,
                "run branch の想定外差分を解消できませんでした。",
                remaining,
                warnings,
            )


def merge_run(
    context: EditingRunContext,
    state: SessionState,
    warnings: list[str],
    session_head_before_join: str,
    *,
    on_merged: Callable[[str | None], None] | None = None,
) -> tuple[str | None, str, str | None, str | None]:
    """共通 merge と post-join を行い、state 初期化と資源 cleanup は呼出元に残す。"""
    # merge の結果を確定し、workload 固有の state 初期化は呼出元へ返す。
    run_join_commit: str | None
    index_conflict = False
    start_subcommand_step(3, "run branch を session へ merge", "merge run")
    merge = run_git(
        ["merge", "--no-ff", context.run_branch],
        context.session_worktree,
        check=False,
    )
    if merge.returncode != 0:
        index_conflict = True
        run_join_commit = _resolve_index_only_conflict_or_fail(
            context,
            state,
            warnings,
            session_head_before_join,
        )
    else:
        merged_head = head_commit(context.session_worktree)
        run_join_commit = (
            merged_head if merged_head != session_head_before_join else None
        )
    if on_merged is not None:
        on_merged(run_join_commit)
    # merge 後の共通 hook と state 同期を実行する。
    start_subcommand_step(4, "post-join hook と state 同期", "run post-join")
    hook_result = "none"
    # post-join 処理の失敗時は merge を戻して error state にするため、成功確定まで
    # last_joined_apply_fork_commit を state object へ書き戻さない。
    last_joined_apply_fork_commit = state.session.last_joined_apply_fork_commit
    if context.kind == "realization_apply":
        # lock 内で対象 run を確定した時点の state を使い、error run の比較始点を保つ。
        hook_result = "session.last_joined_apply_fork_commit preserved"
        if context.state_before == "joinable":
            last_joined_apply_fork_commit = context.run_fork_commit
            hook_result = "session.last_joined_apply_fork_commit updated"
    _refresh_join_indexes(context, warnings)
    if index_conflict:
        warnings.append("INDEX.md conflicts were regenerated")
    sync_refactor_state(context.session_worktree)
    state_sync_commit = commit_work_unit(
        context.session_worktree,
        "cmoc refactor state sync after run join",
    )
    return (
        run_join_commit,
        hook_result,
        state_sync_commit,
        last_joined_apply_fork_commit,
    )


def _refresh_join_indexes(
    context: EditingRunContext,
    warnings: list[str],
) -> None:
    """post-merge の INDEX 生成を追跡し、INDEX 外の副作用を拒否する。"""
    # join 自身が起動する Codex を run process tracking に登録する。
    with run_process_tracking(context.repo, context.session_id):
        write_run_process_id(context.repo, context.session_id, os.getpid())
        try:
            refresh_indexes(context.session_worktree, commit=True)
        finally:
            try:
                warnings.extend(
                    stop_tracked_codex_children(context.repo, context.session_id) or []
                )
            finally:
                delete_run_process_id(context.repo, context.session_id)
    # INDEX commit が拾わない Codex の副作用を state sync commit へ混入させない。
    require_clean_worktree(context.session_worktree)


def _revert_unexpected_run_paths(
    context: EditingRunContext,
    changes: list[GitChange],
    unexpected_paths: list[str],
) -> None:
    """force-resolve 対象の変更を fork commit へ戻して commit する。"""
    # 検出済み repository path を literal として指定し、rename の両端を一緒に戻す。
    unexpected = set(unexpected_paths)
    paths = sorted(
        {
            path
            for change in changes
            if unexpected.intersection(change.paths)
            for path in change.paths
        }
    )
    run_git(
        [
            "restore",
            "--source",
            context.run_fork_commit,
            "--staged",
            "--worktree",
            "--",
            *[literal_pathspec(path) for path in paths],
        ],
        context.run_worktree,
    )
    commit_work_unit(context.run_worktree, "cmoc run force resolve")


def _resolve_index_only_conflict_or_fail(
    context: EditingRunContext,
    state: SessionState,
    warnings: list[str],
    session_head_before_join: str,
) -> str:
    """INDEX.md だけの conflict を再生成し、それ以外は error report へ移す。"""
    # unmerged path を調べ、INDEX.md だけなら再生成へ進める。
    fields = run_git(
        ["diff", "--name-only", "-z", "--diff-filter=U"],
        context.session_worktree,
    ).stdout.split("\0")
    conflicts = [path for path in fields if path]
    if conflicts and all(
        is_generated_index_path(
            context.session_worktree,
            path,
            base=context.run_fork_commit,
        )
        for path in conflicts
    ):
        for path in conflicts:
            if _has_ours_conflict_stage(context.session_worktree, path):
                run_git(
                    ["checkout", "--ours", "--", literal_pathspec(path)],
                    context.session_worktree,
                )
                run_git(
                    ["add", "--", literal_pathspec(path)],
                    context.session_worktree,
                )
            else:
                # session 側で削除された INDEX.md には ours stage がないため、削除を
                # stage してから再生成処理へ渡す。
                run_git(
                    ["rm", "-f", "--", literal_pathspec(path)],
                    context.session_worktree,
                )
        run_git(["commit", "--no-edit"], context.session_worktree)
        merge_commit = head_commit(context.session_worktree)
        return merge_commit
    # INDEX.md 以外の conflict は join 開始前の clean tree へ戻して report する。
    restore_session_after_join_failure(context, session_head_before_join)
    state.run.state = "error"
    write_state(context.state_path, state)
    report = write_lifecycle_report(
        context,
        "join",
        state_after="error",
        warnings=warnings,
        details={
            "run_join_commit": None,
            "post_join_hook": "not_run",
            "refactor_state_sync_commit": None,
            "cleanup": "not_run",
            "conflict_paths": ", ".join(conflicts),
        },
        terminal_classification="error",
        exit_code=1,
    )
    error = CmocError(
        "INDEX.md 以外の merge conflict が発生しました。",
        ["run report を確認し、run を join または abandon してください。"],
        "\n".join(conflicts) or "merge failed without unmerged paths",
        terminal_result=TerminalResult(
            primary_report=report,
            primary_report_role="run join report",
            warnings=tuple(warnings),
        ),
    )
    raise error


def restore_session_after_join_failure(
    context: EditingRunContext,
    session_head_before_join: str,
) -> None:
    """merge/post-join 失敗後に session worktree を開始時点へ戻す。"""
    # merge --abort が失敗しても、開始前の clean tree へ戻す。
    merge_head = run_git(
        ["rev-parse", "-q", "--verify", "MERGE_HEAD"],
        context.session_worktree,
        check=False,
    )
    if merge_head.returncode == 0:
        run_git(["merge", "--abort"], context.session_worktree, check=False)
    run_git(["reset", "--hard", session_head_before_join], context.session_worktree)
    run_git(["clean", "-fd"], context.session_worktree)


def _has_ours_conflict_stage(root: Path, path: str) -> bool:
    """unmerged path に session 側の stage 2 が存在するか判定する。"""
    # stage 2 があれば session 側の内容を残してから index を再生成する。
    fields = run_git(
        ["ls-files", "-u", "-z", "--", literal_pathspec(path)], root
    ).stdout.split("\0")
    for field in fields:
        metadata, separator, _path = field.partition("\t")
        if separator and len(metadata.split()) >= 3 and metadata.split()[2] == "2":
            return True
    return False


def cleanup_joined_run(
    context: EditingRunContext,
    warnings: list[str],
) -> str:
    """merge 済み run の worktree と branch を安全条件付きで削除する。"""
    # run branch が session branch へ到達可能なことを先に確認する。
    try:
        reachable = (
            run_git(
                [
                    "merge-base",
                    "--is-ancestor",
                    context.run_branch,
                    context.session_branch,
                ],
                context.session_worktree,
                check=False,
            ).returncode
            == 0
        )
    except Exception:
        warnings.append("run branch reachability check failed")
        return "preserved"
    if not reachable:
        warnings.append("run branch is not reachable from session branch")
        return "preserved"
    # 削除対象 worktree が cwd の場合は、session worktree へ退避する。
    if Path.cwd().resolve() == context.run_worktree.resolve():
        try:
            os.chdir(context.session_worktree)
        except Exception:
            warnings.append("run worktree cleanup failed")
            return "preserved"
    try:
        removal = remove_worktree(context.repo, context.run_worktree)
    except Exception:
        warnings.append("run worktree cleanup failed")
        return "preserved"
    if (
        removal.returncode != 0
        or context.run_worktree.exists()
        or context.run_worktree.is_symlink()
    ):
        warnings.append("run worktree cleanup failed")
        return "preserved"
    # worktree の削除成功後だけ branch を削除する。
    try:
        branch_present = branch_exists(context.repo, context.run_branch)
    except Exception:
        warnings.append("run branch cleanup failed")
        return "branch_preserved"
    if branch_present:
        try:
            deletion = delete_branch(context.repo, context.run_branch)
            branch_present = deletion.returncode != 0 or branch_exists(
                context.repo, context.run_branch
            )
        except Exception:
            warnings.append("run branch cleanup failed")
            return "branch_preserved"
        if branch_present:
            warnings.append("run branch cleanup failed")
            return "branch_preserved"
    return "completed"


def _raise_unexpected(
    context: EditingRunContext,
    summary: str,
    paths: list[str],
    warnings: list[str],
) -> None:
    """想定外差分を report に記録して join failure として送出する。"""
    # 差分を report に保存してから、join を中断する。
    update_primary_report_fields(
        state_after=context.state_before,
        run_join_commit=None,
        post_join_hook="not_run",
        cleanup="not_run",
        unexpected_paths=paths,
    )
    report = write_lifecycle_report(
        context,
        "join",
        state_after=context.state_before,
        warnings=warnings,
        details={
            "run_join_commit": None,
            "post_join_hook": "not_run",
            "refactor_state_sync_commit": None,
            "cleanup": "not_run",
            "unexpected_paths": ", ".join(paths),
        },
        terminal_classification="error",
        exit_code=1,
    )
    error = CmocError(
        summary,
        [
            "run branch のみを自動修復する場合は cmoc run join --force-resolve を実行してください。",
            "session branch の成果物は手動で確認してください。",
        ],
        "\n".join(paths),
        terminal_result=TerminalResult(
            primary_report=report,
            primary_report_role="run join report",
            warnings=tuple(warnings),
        ),
    )
    raise error
