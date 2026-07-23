"""明示的な join を必要とする editing run の共通処理。"""

from __future__ import annotations

import os
from collections.abc import Collection
from dataclasses import dataclass
from pathlib import Path

from commons.indexing import commit_index_updates, indexing_lock, update_indexes
from commons.runtime_codex import run_codex_exec as run_indexing_codex_exec
from commons.runtime_errors import CmocError
from commons.runtime_git import (
    branch_exists,
    create_run_worktree,
    current_branch,
    delete_branch,
    head_commit,
    is_realization_file_path,
    remove_worktree,
    require_clean_worktree,
    run_git,
    status_path_statuses,
)
from commons.runtime_paths import (
    is_root_memo,
    refactor_state_path,
    repo_root,
    timestamp,
    work_root,
)
from commons.runtime_run import (
    delete_run_process_id,
    expected_run_worktree,
    run_lifecycle_lock,
    worktree_for_branch,
    worktree_for_branch_optional,
    write_run_process_id,
)
from commons.runtime_state import (
    RunPart,
    SessionState,
    load_state_for_branch,
    write_state,
)

MAX_RUN_ID_ATTEMPTS = 32


@dataclass(frozen=True)
class EditingRunContext:
    """workload が共有する active editing run の確定情報。"""

    repo: Path
    session_worktree: Path
    session_id: str
    state_path: Path
    session_branch: str
    session_fork_commit: str
    kind: str
    run_branch: str
    run_fork_commit: str
    run_worktree: Path
    state_before: str = "ready"


@dataclass(frozen=True)
class GitChange:
    """rename/copy の両端を失わない Git tree change。"""

    status: str
    paths: tuple[str, ...]


def require_ready_session() -> tuple[Path, Path, str, Path, SessionState, str]:
    """fork の共通事前条件を検査し、session 情報を返す。"""
    repository = repo_root()
    session_worktree = work_root()
    branch = current_branch(session_worktree)
    if not branch.startswith("cmoc/session/"):
        raise CmocError(
            "editing run は session branch 上で開始してください。",
            ["active な cmoc session branch へ checkout して再実行してください。"],
            f"current branch: {branch}",
        )
    session_id, path, state = load_state_for_branch(repository, branch)
    if state.session.state != "active" or state.run.state != "ready":
        raise CmocError(
            "editing run を開始できる session state ではありません。",
            ["既存 run を join または abandon してから再実行してください。"],
            f"session.state: {state.session.state}\nrun.state: {state.run.state}",
        )
    require_clean_worktree(session_worktree)
    session_fork_commit = state.session.session_fork_commit
    if session_fork_commit is None:
        raise CmocError(
            "session fork commit を特定できません。",
            ["session state file を確認してください。"],
            str(path),
        )
    return (
        repository,
        session_worktree,
        session_id,
        path,
        state,
        session_fork_commit,
    )


def start_editing_run(kind: str) -> EditingRunContext:
    """session HEAD から isolated run branch/worktree を作り state を公開する。"""
    (
        repository,
        session_worktree,
        session_id,
        path,
        _state,
        session_fork_commit,
    ) = require_ready_session()
    session_branch = current_branch(session_worktree)
    with run_lifecycle_lock(repository, session_id):
        # {{work-root}}/oracle/doc/app_spec/sub_command/editing_run.md
        # editor 入力中や並行 process の間に状態が変わり得るため lock 内で再検査する。
        _, _, state = load_state_for_branch(repository, session_branch)
        if state.session.state != "active" or state.run.state != "ready":
            raise CmocError(
                "別の editing run が先に開始されました。",
                ["session state を確認し、active run を先に終了してください。"],
                f"session.state: {state.session.state}\nrun.state: {state.run.state}",
            )
        require_clean_worktree(session_worktree)
        fork_commit = head_commit(session_worktree)
        run_branch, run_worktree = _new_run_target(repository, session_id)
        created = False
        published = False
        try:
            create_run_worktree(
                repository,
                run_branch,
                run_worktree,
                start_point=fork_commit,
            )
            created = True
            state.run = RunPart(
                state="running",
                kind=kind,
                branch=run_branch,
                fork_commit=fork_commit,
            )
            write_state(path, state)
            published = True
            write_run_process_id(repository, session_id, os.getpid())
        except BaseException:
            if published:
                state.run.state = "error"
                write_state(path, state)
            elif created:
                remove_worktree(repository, run_worktree)
                if branch_exists(repository, run_branch):
                    delete_branch(repository, run_branch, force=True)
            raise
    return EditingRunContext(
        repo=repository,
        session_worktree=session_worktree,
        session_id=session_id,
        state_path=path,
        session_branch=session_branch,
        session_fork_commit=session_fork_commit,
        kind=kind,
        run_branch=run_branch,
        run_fork_commit=fork_commit,
        run_worktree=run_worktree,
    )


def resolve_active_run(
    allowed_states: set[str],
    *,
    allow_missing_run_worktree: bool = False,
) -> tuple[EditingRunContext, SessionState]:
    """現在の branch と state から active run および session worktree を解決する。"""
    repository = repo_root()
    current_worktree = work_root()
    branch = current_branch(current_worktree)
    session_id, path, state = load_state_for_branch(repository, branch)
    if state.session.state != "active" or state.run.state not in allowed_states:
        raise CmocError(
            "active editing run の lifecycle 事前条件を満たしていません。",
            ["session state の session.state と run.state を確認してください。"],
            f"session.state: {state.session.state}\nrun.state: {state.run.state}",
        )
    kind = state.run.kind
    run_branch = state.run.branch
    fork_commit = state.run.fork_commit
    session_fork_commit = state.session.session_fork_commit
    if None in {kind, run_branch, fork_commit, session_fork_commit}:
        raise CmocError(
            "active editing run の情報を特定できません。",
            ["session state file を確認してください。"],
            str(path),
        )
    assert kind is not None
    assert run_branch is not None
    assert fork_commit is not None
    assert session_fork_commit is not None
    session_branch = f"cmoc/session/{session_id}"
    if branch not in {session_branch, run_branch}:
        raise CmocError(
            "現在の branch は active run の lifecycle 対象ではありません。",
            ["session branch または active run branch から再実行してください。"],
            f"current: {branch}\nsession: {session_branch}\nrun: {run_branch}",
        )
    session_worktree = worktree_for_branch(repository, session_branch)
    expected = expected_run_worktree(repository, run_branch)
    run_worktree = worktree_for_branch_optional(repository, run_branch)
    if run_worktree is None and allow_missing_run_worktree:
        run_worktree = expected
    if run_worktree is None or run_worktree.resolve() != expected.resolve():
        raise CmocError(
            "active run worktree が管理 path と一致しません。",
            ["git worktree list と session state file を確認してください。"],
            f"actual: {run_worktree}\nexpected: {expected}",
        )
    return (
        EditingRunContext(
            repo=repository,
            session_worktree=session_worktree,
            session_id=session_id,
            state_path=path,
            session_branch=session_branch,
            session_fork_commit=session_fork_commit,
            kind=kind,
            run_branch=run_branch,
            run_fork_commit=fork_commit,
            run_worktree=run_worktree,
            state_before=state.run.state,
        ),
        state,
    )


def set_run_state(context: EditingRunContext, run_state: str) -> SessionState:
    """同じ active run であることを確認して joinable/error を保存する。"""
    if run_state not in {"joinable", "error"}:
        raise ValueError(f"unsupported terminal run state: {run_state}")
    with run_lifecycle_lock(context.repo, context.session_id):
        _, _, state = load_state_for_branch(context.repo, context.session_branch)
        if (
            state.session.state != "active"
            or state.run.kind != context.kind
            or state.run.branch != context.run_branch
            or state.run.fork_commit != context.run_fork_commit
        ):
            raise CmocError(
                "editing run の state が実行中に変更されました。",
                ["session state と run branch を確認してください。"],
                str(context.state_path),
            )
        state.run.state = run_state
        write_state(context.state_path, state)
        delete_run_process_id(context.repo, context.session_id)
        return state


def rollback_work_unit(worktree: Path) -> None:
    """未確定の workload 差分を直近 commit へ戻す。"""
    run_git(["reset", "--hard", "HEAD"], worktree)
    run_git(["clean", "-fd"], worktree)


def commit_work_unit(
    worktree: Path,
    message: str,
    *,
    allow_empty: bool = False,
) -> str | None:
    """worktree の全差分を一つの整合した commit として確定する。"""
    run_git(["add", "-A"], worktree)
    diff = run_git(["diff", "--cached", "--quiet"], worktree, check=False)
    if diff.returncode == 0:
        if allow_empty:
            run_git(["commit", "--allow-empty", "-m", message], worktree)
            return head_commit(worktree)
        return None
    if diff.returncode != 1:
        raise CmocError(
            "commit 対象差分を確認できません。",
            ["run worktree の git index を確認してください。"],
            diff.stderr,
        )
    run_git(["commit", "-m", message], worktree)
    return head_commit(worktree)


def refresh_indexes(worktree: Path, *, commit: bool) -> list[Path]:
    """run worktree の INDEX.md を再生成し、必要なら独立 commit にする。"""
    with indexing_lock(worktree):
        updated = update_indexes(worktree, run_indexing_codex_exec)
        if commit:
            commit_index_updates(worktree, updated)
        return updated


def worktree_change_paths(
    worktree: Path,
    *,
    include_rename_sources: bool = False,
) -> list[str]:
    """未 commit 差分の変更対象を repository 相対 path で返す。"""
    # {{work-root}}/oracle/doc/app_spec/misc_spec.md
    # report 用の既定値は rename 後の path だけを返し、agent 権限検査だけが
    # rename 元も明示的に含める。
    paths = status_path_statuses(
        worktree,
        untracked_all=True,
        include_rename_sources=include_rename_sources,
    )
    return sorted(
        {str(path.absolute().relative_to(worktree.absolute())) for _, path in paths}
    )


def tree_changes(worktree: Path, base: str, end: str = "HEAD") -> list[GitChange]:
    """2 tree 間の変更を NUL framing で安全に列挙する。"""
    fields = run_git(
        ["diff", "--name-status", "-z", "--find-renames", base, end],
        worktree,
    ).stdout.split("\0")
    changes: list[GitChange] = []
    index = 0
    while index < len(fields):
        status = fields[index]
        index += 1
        if not status:
            continue
        path_count = 2 if status[0] in {"R", "C"} else 1
        paths = tuple(fields[index : index + path_count])
        if len(paths) != path_count or any(not path for path in paths):
            raise CmocError(
                "git diff の path 一覧を解釈できません。",
                ["run branch の git tree を確認してください。"],
                repr(fields),
            )
        changes.append(GitChange(status, paths))
        index += path_count
    return changes


def flattened_change_paths(changes: list[GitChange]) -> list[str]:
    """managed branch の変更 file path を重複なしで返す。"""
    # {{work-root}}/oracle/doc/app_spec/misc_spec.md
    # 削除 path と rename 元 path は変更対象の集合に含めず、rename 後だけを残す。
    paths: set[str] = set()
    for change in changes:
        if not change.paths or change.status.startswith("D"):
            continue
        paths.add(
            change.paths[-1]
            if change.status.startswith(("R", "C"))
            else change.paths[0]
        )
    return sorted(paths)


def unexpected_agent_paths(
    context: EditingRunContext,
    paths: list[str],
) -> list[str]:
    """workload agent が変更を許可されていない path を返す。"""
    return sorted(
        path
        for path in paths
        if not _is_agent_expected_path(
            context.run_worktree,
            context.kind,
            path,
            context.run_branch,
        )
    )


def unexpected_run_paths(
    context: EditingRunContext,
    changes: list[GitChange],
    *,
    ignored_paths: Collection[str] = (),
) -> list[str]:
    """run branch の workload 想定外 path を返す。"""
    ignored = set(ignored_paths)
    return sorted(
        {
            path
            for change in changes
            for path in change.paths
            if path not in ignored
            and not _is_run_expected_path(
                context.run_worktree,
                context.kind,
                path,
                context.run_branch,
            )
        }
    )


def unexpected_session_paths(
    session_worktree: Path,
    changes: list[GitChange],
    *,
    ignored_paths: Collection[str] = (),
) -> list[str]:
    """run 開始後の session branch にある想定外 path を返す。"""
    ignored = set(ignored_paths)
    return sorted(
        {
            path
            for change in changes
            for path in change.paths
            if path not in ignored
            and not (
                _is_oracle_path(path)
                or _is_index_path(path)
                or is_root_memo(session_worktree, session_worktree / path)
            )
        }
    )


def raw_oracle_diff(worktree: Path, base: str, end: str) -> str:
    """両端のいずれかが oracle file である rename 対応 raw diff を返す。"""
    candidates = sorted(
        {
            path
            for change in tree_changes(worktree, base, end)
            if any(_is_oracle_path(path) for path in change.paths)
            for path in change.paths
        }
    )
    if not candidates:
        return ""
    return run_git(
        ["diff", "--binary", "--find-renames", base, end, "--", *candidates],
        worktree,
    ).stdout


def _new_run_target(repository: Path, session_id: str) -> tuple[str, Path]:
    for _ in range(MAX_RUN_ID_ATTEMPTS):
        run_id = timestamp()
        branch = f"cmoc/run/{session_id}/{run_id}"
        worktree = expected_run_worktree(repository, branch)
        if not branch_exists(repository, branch) and not worktree.exists():
            return branch, worktree
    raise CmocError(
        "一意な run-id を生成できませんでした。",
        ["時間を置いてから editing run を再実行してください。"],
        f"attempts: {MAX_RUN_ID_ATTEMPTS}",
    )


def _is_agent_expected_path(
    root: Path,
    kind: str,
    path: str,
    branch: str,
) -> bool:
    if kind in {"realization_apply", "realization_refactor"}:
        return is_realization_file_path(root, root / path, branch=branch)
    return False


def _is_run_expected_path(
    root: Path,
    kind: str,
    path: str,
    branch: str,
) -> bool:
    if _is_index_path(path):
        return True
    if kind == "realization_refactor" and _is_refactor_state_path(root, path):
        return True
    return _is_agent_expected_path(root, kind, path, branch)


def _is_oracle_path(path: str) -> bool:
    parts = Path(path).parts
    return (
        bool(parts)
        and parts[0] == "oracle"
        and Path(path).name
        not in {
            "AGENTS.md",
            "INDEX.md",
        }
    )


def _is_index_path(path: str) -> bool:
    return Path(path).name == "INDEX.md"


def _is_refactor_state_path(root: Path, path: str) -> bool:
    return Path(path) == refactor_state_path(root).relative_to(root)
