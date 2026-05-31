"""`cmoc apply join` の本体処理。"""

import json
import os
import tempfile
from collections.abc import Callable
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

from commons.command_runner import run_command
from commons.errors import CmocError
from commons.repo import (
    apply_worktree_path_from_branch,
    assert_no_uncommitted_changes,
    clear_apply_process_id,
    current_branch,
    filter_apply_implementation_file_paths_at_commit,
    filter_oracle_file_paths_at_commit,
    git_name_only_paths,
    git_name_status_entries,
    is_apply_branch,
    is_session_branch,
    read_session_state,
    resolve_session_home_branch,
    root_gitignored_paths_at_commit,
    run_git,
    session_id_from_branch,
    session_state_repo_root,
    write_session_state,
)
from commons.timing import StepTimer, start_step


def cmoc_apply_join_impl(
    repo_root: Path | None = None,
    *,
    force_resolve: bool = False,
) -> None:
    """完了済み apply branch を session branch へ merge する。"""
    # 直接呼び出し時は共通 runner で repo root 解決とエラー整形を行う。
    if repo_root is None:
        run_command(
            lambda resolved_repo_root: cmoc_apply_join_impl(
                resolved_repo_root,
                force_resolve=force_resolve,
            )
        )
        return

    timer = StepTimer("apply join")
    start_step(timer, 1, 5, "validate apply state")
    branch_name = current_branch(repo_root)
    session_id = session_id_from_branch(branch_name)
    cmoc_root = session_state_repo_root(repo_root, session_id)
    os.chdir(cmoc_root)
    state = read_session_state(cmoc_root, session_id)
    join_state = _validate_joinable_state(
        cmoc_root,
        state,
        branch_name,
        session_id,
    )
    _assert_local_branch_exists(cmoc_root, join_state.session_branch)
    _assert_local_branch_exists(cmoc_root, join_state.apply_branch)
    assert_no_uncommitted_changes(repo_root)
    if cmoc_root != repo_root:
        assert_no_uncommitted_changes(cmoc_root)
    if join_state.apply_worktree is not None and join_state.apply_worktree.exists():
        assert_no_uncommitted_changes(join_state.apply_worktree)

    start_step(timer, 2, 5, "inspect unexpected diffs")
    unexpected = _unexpected_diffs(cmoc_root, join_state)
    if unexpected and not force_resolve:
        raise CmocError(
            "apply join を中止しました。想定外の差分があります。",
            [
                "`--force-resolve` を付けて再実行すると、想定外差分を revert してから merge を試みます。",
                "意図した変更の場合は、対象 branch の内容を手動で確認してください。",
            ],
            "\n".join(unexpected),
        )

    start_step(timer, 3, 5, "resolve unexpected diffs")
    if unexpected:
        _force_resolve_unexpected_diffs(cmoc_root, join_state)
        print("force-resolved unexpected diffs:")
        for line in unexpected:
            print(f"- {line}")

    start_step(timer, 4, 5, "merge apply branch")
    run_git(cmoc_root, ["switch", join_state.session_branch])
    merge_result = run_git(
        cmoc_root,
        ["merge", "--no-ff", join_state.apply_branch],
        check=False,
    )
    auto_resolved_index_conflicts: list[str] = []
    if merge_result.returncode != 0:
        unmerged = _unmerged_paths(cmoc_root)
        index_conflicts = [path for path in unmerged if _is_index_path(path)]
        non_index_conflicts = [
            path for path in unmerged if not _is_index_path(path)
        ]
        if index_conflicts:
            auto_resolved_index_conflicts = _resolve_index_conflicts(
                cmoc_root,
                index_conflicts,
                merge_result.stderr.strip(),
                commit_merge=not non_index_conflicts,
            )
            unmerged = _unmerged_paths(cmoc_root)
            non_index_conflicts = [
                path for path in unmerged if not _is_index_path(path)
            ]
        if non_index_conflicts or not index_conflicts:
            if auto_resolved_index_conflicts and unmerged:
                detail = "\n".join(["unmerged paths:", *unmerged]).strip()
            else:
                detail = merge_result.stderr.strip()
            if unmerged and not detail.startswith("unmerged paths:"):
                detail = "\n".join(["unmerged paths:", *unmerged, detail]).strip()
            raise CmocError(
                "apply branch の merge で conflict が発生しました。",
                [
                    "cmoc は INDEX.md 以外の apply join conflict を自動解消しません。",
                    "git status を確認し、手動で merge 状態を解消してください。",
                ],
                detail,
            )

    start_step(timer, 5, 5, "record ready apply state")
    cleanup_evidence = _snapshot_cleanup_evidence(cmoc_root, join_state)
    _mark_apply_ready(
        cmoc_root,
        session_id,
        state,
        join_state.oracle_snapshot_commit,
        resolve_session_home_branch(
            cmoc_root,
            state,
            join_state.session_branch,
        ),
        cleanup_evidence.apply_result,
    )
    warnings = _cleanup_apply_artifacts(
        cmoc_root,
        session_id,
        join_state,
        cleanup_evidence,
    )
    print(f"joined apply branch: {join_state.apply_branch}")
    print(f"session branch: {join_state.session_branch}")
    if auto_resolved_index_conflicts:
        print("auto-resolved INDEX.md conflicts:")
        for path in auto_resolved_index_conflicts:
            print(f"- {path}")
    for warning in warnings:
        print(f"warning: {warning}")
    timer.report()


class _JoinState:
    """apply join に必要な state 値。"""

    def __init__(
        self,
        *,
        session_branch: str,
        apply_branch: str,
        apply_worktree: Path | None,
        oracle_snapshot_commit: str,
    ) -> None:
        self.session_branch = session_branch
        self.apply_branch = apply_branch
        self.apply_worktree = apply_worktree
        self.oracle_snapshot_commit = oracle_snapshot_commit


class _CleanupEvidence:
    """ready 遷移前に確認した cleanup 用証跡。"""

    def __init__(
        self,
        *,
        report_saved: bool,
        apply_result: str | None,
        warnings: list[str],
    ) -> None:
        self.report_saved = report_saved
        self.apply_result = apply_result
        self.warnings = warnings


class _ChangedPathEntry:
    """1 つの git diff entry が触る path 群。"""

    def __init__(self, paths: list[str]) -> None:
        self.paths = paths


def _validate_joinable_state(
    repo_root: Path,
    state: dict[str, object],
    current_branch_name: str,
    session_id: str,
) -> _JoinState:
    """apply join の state 前提条件を検証する。"""
    session = state.get("session")
    apply = state.get("apply")
    if not isinstance(session, dict) or not isinstance(apply, dict):
        raise CmocError(
            "session state ファイルの形式が不正です。",
            [
                "state JSON の session/apply セクションを確認して復旧してください。",
                "復旧できない場合は、対象 apply run を破棄して新しい session でやり直してください。",
            ],
            f"現在の branch: {current_branch_name}",
    )
    session_branch = f"cmoc/session/{session_id}"
    apply_branch = apply.get("apply_branch")
    oracle_snapshot_commit = apply.get("oracle_snapshot_commit")
    if session.get("state") != "active":
        raise CmocError(
            "active な session ではありません。",
            [
                "対象 session の state を確認してください。",
                "既に join または abandon 済みの場合は、新しい session を開始してください。",
            ],
            f"session.state: {session.get('state')}",
        )
    if apply.get("state") not in {"completed", "error"}:
        raise CmocError(
            "join 可能な apply run ではありません。",
            [
                "`cmoc apply fork` が completed または error になってから `cmoc apply join` を実行してください。",
                "session state の apply.state を確認してください。",
            ],
            f"apply.state: {apply.get('state')}",
        )
    if not isinstance(apply_branch, str) or not is_apply_branch(apply_branch):
        raise CmocError(
            "apply branch を session state から特定できませんでした。",
            [
                "session state の apply.apply_branch を確認してください。",
                "state が壊れている場合は、手動で apply branch を確認してください。",
            ],
            f"apply.apply_branch: {apply_branch}",
        )
    apply_branch_session_id = session_id_from_branch(apply_branch)
    if apply_branch_session_id != session_id:
        raise CmocError(
            "session state ファイルの apply branch が現在の session と一致しません。",
            [
                "session state の apply.apply_branch を確認して復旧してください。",
                "別 session の apply branch を join 対象にしないでください。",
            ],
            "\n".join(
                [
                    f"session id: {session_id}",
                    f"apply branch session id: {apply_branch_session_id}",
                    f"apply.apply_branch: {apply_branch}",
                ]
            ),
        )
    if current_branch_name not in {session_branch, apply_branch}:
        raise CmocError(
            "`cmoc apply join` は session branch または apply branch 上で実行してください。",
            [
                "対象 session の session branch か、対応する apply branch へ移動してください。",
                "通常 branch 同士の merge は `git merge` を直接実行してください。",
            ],
            f"現在の branch: {current_branch_name or '(detached HEAD)'}",
        )
    if not isinstance(oracle_snapshot_commit, str) or not oracle_snapshot_commit:
        raise CmocError(
            "oracle snapshot commit を session state から特定できませんでした。",
            [
                "session state の apply.oracle_snapshot_commit を確認してください。",
                "state が壊れている場合は、手動で merge 元の基準 commit を確認してください。",
            ],
        )
    if not is_session_branch(session_branch):
        raise CmocError(
            "session branch 名が不正です。",
            [
                "session state ファイル名と branch 名を確認してください。",
                "正しい session branch 上で `cmoc apply join` を再実行してください。",
            ],
            f"session branch: {session_branch}",
        )
    apply_worktree = apply_worktree_path_from_branch(repo_root, apply_branch)
    return _JoinState(
        session_branch=session_branch,
        apply_branch=apply_branch,
        apply_worktree=apply_worktree,
        oracle_snapshot_commit=oracle_snapshot_commit,
    )


def _assert_local_branch_exists(repo_root: Path, branch_name: str) -> None:
    """local branch が存在することを確認する。"""
    result = run_git(
        repo_root,
        ["show-ref", "--verify", f"refs/heads/{branch_name}"],
        check=False,
    )
    if result.returncode != 0:
        raise CmocError(
            "必要な local branch が見つかりませんでした。",
            [
                "session state に記録された branch 名を確認してください。",
                "削除済みの場合は、手動で branch を復元してから再実行してください。",
            ],
            f"branch: {branch_name}",
        )


def _unexpected_diffs(repo_root: Path, join_state: _JoinState) -> list[str]:
    """通常モードで停止対象にする想定外差分を列挙する。"""
    unexpected: list[str] = []
    apply_entries = _changed_path_entries_between(
        repo_root,
        join_state.oracle_snapshot_commit,
        join_state.apply_branch,
    )
    for entry in apply_entries:
        invalid_paths = [
            path
            for path in entry.paths
            if not _is_apply_branch_expected_path(
                repo_root,
                join_state.oracle_snapshot_commit,
                path,
            )
        ]
        for path in invalid_paths:
            unexpected.append(f"{join_state.apply_branch}: {path}")

    session_entries = _changed_path_entries_between(
        repo_root,
        join_state.oracle_snapshot_commit,
        join_state.session_branch,
    )
    for entry in session_entries:
        invalid_paths = [
            path
            for path in entry.paths
            if not _is_session_branch_expected_path(
                repo_root,
                join_state.oracle_snapshot_commit,
                path,
            )
        ]
        for path in invalid_paths:
            unexpected.append(f"{join_state.session_branch}: {path}")
    return unexpected


def _changed_path_entries_between(
    repo_root: Path,
    base_commit: str,
    branch_name: str,
) -> list[_ChangedPathEntry]:
    """base..branch の変更 entry が触る path 群を返す。"""
    result = run_git(
        repo_root,
        [
            "diff",
            "--name-status",
            "-z",
            "-M",
            "-C",
            "--find-copies-harder",
            f"{base_commit}..{branch_name}",
            "--",
        ],
    )
    entries: list[_ChangedPathEntry] = []
    for status, paths in git_name_status_entries(result.stdout):
        if paths:
            if status.startswith("R"):
                entries.append(_ChangedPathEntry(paths))
            else:
                # copy は source を変更しないため、変更後 path を対象にする。
                entries.append(_ChangedPathEntry([paths[-1]]))
    return entries


def _is_oracle_path(path: str) -> bool:
    """oracle ファイル側の変更とみなす path か判定する。"""
    return path == "oracles" or path.startswith("oracles/")


def _is_apply_branch_expected_path(
    repo_root: Path,
    oracle_snapshot_commit: str,
    path: str,
) -> bool:
    """apply branch 側で cmoc が積み得る想定内 path か判定する。"""
    if _is_apply_branch_forbidden_path(path):
        return False
    if _is_snapshot_index_path(repo_root, oracle_snapshot_commit, path):
        return True
    return (
        filter_apply_implementation_file_paths_at_commit(
            repo_root,
            oracle_snapshot_commit,
            [path],
        )
        == [path]
    )


def _is_apply_branch_forbidden_path(path: str) -> bool:
    """apply branch 側の正規成果物として扱わない path か判定する。"""
    return (
        _is_oracle_path(path)
        or path == "README.md"
        or path == "AGENTS.md"
        or path == ".cmoc"
        or path.startswith(".cmoc/")
        or path == ".agents"
        or path.startswith(".agents/")
        or _is_memo_path(path)
    )


def _is_session_branch_expected_path(
    repo_root: Path,
    oracle_snapshot_commit: str,
    path: str,
) -> bool:
    """session branch 側で利用者が編集し得る想定内 path か判定する。"""
    return (
        filter_oracle_file_paths_at_commit(
            repo_root,
            oracle_snapshot_commit,
            [path],
        )
        == [path]
        or _is_memo_path(path)
        or _is_index_path(path)
    )


def _is_memo_path(path: str) -> bool:
    """root memo 側の変更とみなす path か判定する。"""
    return path == "memo" or path.startswith("memo/")


def _is_index_path(path: str) -> bool:
    """cmoc が再生成可能な INDEX.md path か判定する。"""
    return Path(path).name == "INDEX.md"


def _is_snapshot_index_path(
    repo_root: Path,
    oracle_snapshot_commit: str,
    path: str,
) -> bool:
    """snapshot の root `.gitignore` で除外されない INDEX.md か判定する。"""
    index_path = Path(path)
    if index_path.is_absolute() or index_path.name != "INDEX.md":
        return False
    if any(part in {"", ".", ".."} for part in index_path.parts):
        return False
    directory = index_path.parent.as_posix()
    candidates = [path]
    if directory != ".":
        candidates.append(directory)
    ignored = root_gitignored_paths_at_commit(
        repo_root,
        oracle_snapshot_commit,
        candidates,
    )
    return path not in ignored and directory not in ignored


def _force_resolve_unexpected_diffs(
    repo_root: Path,
    join_state: _JoinState,
) -> None:
    """想定外差分を snapshot の内容へ戻す。"""
    _revert_branch_paths(
        repo_root,
        join_state.apply_branch,
        join_state.oracle_snapshot_commit,
        _unexpected_entry_paths(
            _changed_path_entries_between(
                repo_root,
                join_state.oracle_snapshot_commit,
                join_state.apply_branch,
            ),
            lambda path: _is_apply_branch_expected_path(
                repo_root,
                join_state.oracle_snapshot_commit,
                path,
            ),
        ),
        join_state.apply_worktree,
    )
    _revert_branch_paths(
        repo_root,
        join_state.session_branch,
        join_state.oracle_snapshot_commit,
        _unexpected_entry_paths(
            _changed_path_entries_between(
                repo_root,
                join_state.oracle_snapshot_commit,
                join_state.session_branch,
            ),
            lambda path: _is_session_branch_expected_path(
                repo_root,
                join_state.oracle_snapshot_commit,
                path,
            ),
        ),
        repo_root,
    )


def _unexpected_entry_paths(
    entries: list[_ChangedPathEntry],
    is_expected_path: Callable[[str], bool],
) -> list[str]:
    """想定外 path を含む entry の全 path を revert 対象として返す。"""
    paths: set[str] = set()
    for entry in entries:
        if any(not is_expected_path(path) for path in entry.paths):
            paths.update(entry.paths)
    return sorted(paths)


def _revert_branch_paths(
    repo_root: Path,
    branch_name: str,
    source_commit: str,
    paths: list[str],
    branch_worktree: Path | None,
) -> None:
    """指定 branch 上の path を source commit へ戻して commit する。"""
    if not paths:
        return
    with _revert_worktree(repo_root, branch_name, branch_worktree) as worktree:
        existing_at_source = _paths_existing_at_commit(worktree, source_commit, paths)
        missing_at_source = sorted(set(paths) - set(existing_at_source))
        if existing_at_source:
            run_git(
                worktree,
                ["restore", "--source", source_commit, "--", *existing_at_source],
            )
        if missing_at_source:
            run_git(worktree, ["rm", "-r", "--ignore-unmatch", "--", *missing_at_source])
        if existing_at_source:
            run_git(worktree, ["add", "--", *existing_at_source])
        if (
            run_git(worktree, ["diff", "--cached", "--quiet"], check=False).returncode
            == 1
        ):
            run_git(
                worktree,
                [
                    "commit",
                    "-m",
                    f"Revert unexpected apply join changes on {branch_name}",
                ],
            )


@contextmanager
def _revert_worktree(
    repo_root: Path,
    branch_name: str,
    branch_worktree: Path | None,
) -> Iterator[Path]:
    """revert に使える worktree を返す。必要なら一時 worktree を作る。"""
    if branch_worktree is None:
        if current_branch(repo_root) != branch_name:
            run_git(repo_root, ["switch", branch_name])
        yield repo_root
        return

    if branch_worktree.exists():
        if current_branch(branch_worktree) != branch_name:
            run_git(branch_worktree, ["switch", branch_name])
        yield branch_worktree
        return

    if current_branch(repo_root) == branch_name:
        yield repo_root
        return

    temporary_root = repo_root / ".cmoc" / "worktrees" / "tmp"
    temporary_root.mkdir(parents=True, exist_ok=True)
    run_git(repo_root, ["worktree", "prune"])
    temporary_worktree = Path(
        tempfile.mkdtemp(
            prefix="apply-join-force-resolve-",
            dir=temporary_root,
        )
    )
    temporary_worktree.rmdir()
    result = run_git(
        repo_root,
        ["worktree", "add", str(temporary_worktree), branch_name],
        check=False,
    )
    if result.returncode != 0:
        detail = result.stderr.strip()
        if detail:
            detail = f"{branch_worktree}\n{detail}"
        else:
            detail = str(branch_worktree)
        raise CmocError(
            "apply worktree が見つからず、一時 worktree の作成にも失敗しました。",
            [
                "session state に記録された apply branch と worktree を確認してください。",
                "stale な worktree 登録が残っている場合は `git worktree prune` 後に再実行してください。",
                "手動復旧する場合は apply branch を checkout して想定外差分を revert してください。",
            ],
            detail,
        )
    try:
        yield temporary_worktree
    finally:
        run_git(
            repo_root,
            ["worktree", "remove", "--force", str(temporary_worktree)],
            check=False,
        )


def _paths_existing_at_commit(
    repo_root: Path,
    commit_hash: str,
    paths: list[str],
) -> list[str]:
    """指定 commit に存在する path だけを返す。"""
    existing: list[str] = []
    for path in paths:
        result = run_git(
            repo_root,
            ["cat-file", "-e", f"{commit_hash}:{path}"],
            check=False,
        )
        if result.returncode == 0:
            existing.append(path)
    return existing


def _unmerged_paths(repo_root: Path) -> list[str]:
    """unmerged path を git から取得する。"""
    result = run_git(repo_root, ["diff", "--name-only", "-z", "--diff-filter=U"])
    return git_name_only_paths(result.stdout)


def _resolve_index_conflicts(
    repo_root: Path,
    paths: list[str],
    merge_stderr: str,
    *,
    commit_merge: bool,
) -> list[str]:
    """INDEX.md conflict を削除で解消し、必要なら merge commit を完了する。"""
    resolved_paths = sorted(paths)
    run_git(repo_root, ["rm", "--ignore-unmatch", "--", *resolved_paths])
    remaining = _unmerged_paths(repo_root)
    remaining_index_conflicts = [
        path for path in remaining if _is_index_path(path)
    ]
    if remaining_index_conflicts or (commit_merge and remaining):
        detail = "\n".join(
            [
                "unmerged paths:",
                *remaining,
                merge_stderr,
            ]
        ).strip()
        raise CmocError(
            "INDEX.md conflict の自動解消に失敗しました。",
            [
                "git status を確認し、残っている conflict を手動で解消してください。",
                "不要な merge 状態であれば `git merge --abort` で戻してください。",
            ],
            detail,
        )
    if not commit_merge:
        return resolved_paths

    commit_result = run_git(repo_root, ["commit", "--no-edit"], check=False)
    if commit_result.returncode != 0:
        detail = "\n".join(
            [
                merge_stderr,
                commit_result.stderr.strip(),
            ]
        ).strip()
        raise CmocError(
            "INDEX.md conflict 解消後の merge commit に失敗しました。",
            [
                "git status を確認し、merge 状態を手動で完了してください。",
                "不要な merge 状態であれば `git merge --abort` で戻してください。",
            ],
            detail,
        )
    return resolved_paths


def _mark_apply_ready(
    repo_root: Path,
    session_id: str,
    state: dict[str, object],
    oracle_snapshot_commit: str,
    session_home_branch: str,
    apply_result: str | None,
) -> None:
    """最後に join した snapshot を記録し、apply セクションを ready に戻す。"""
    session = state.get("session")
    apply = state.get("apply")
    if not isinstance(session, dict) or not isinstance(apply, dict):
        raise CmocError(
            "session state ファイルの形式が不正です。",
            [
                "state JSON の session/apply セクションを確認して復旧してください。",
                "復旧できない場合は、対象 apply run を破棄して新しい session でやり直してください。",
            ],
        )
    session["session_home_branch"] = session_home_branch
    session["last_joined_apply_oracle_snapshot_commit"] = oracle_snapshot_commit
    if apply_result is not None and apply_result.strip() != "":
        session["last_joined_apply_result"] = apply_result
    else:
        session.pop("last_joined_apply_result", None)
    state["apply"] = {
        "state": "ready",
        "apply_branch": None,
        "oracle_snapshot_commit": None,
    }
    write_session_state(repo_root, session_id, state)
    clear_apply_process_id(repo_root, session_id)


def _snapshot_cleanup_evidence(
    repo_root: Path,
    join_state: _JoinState,
) -> _CleanupEvidence:
    """apply artifact 削除前に report/result 保存済み証跡を取得する。"""
    report_path, metadata = _find_apply_report(repo_root, join_state.apply_branch)
    warnings: list[str] = []
    if report_path is None:
        warnings.append(
            "apply cleanup skipped: saved apply report was not found for "
            f"{join_state.apply_branch}"
        )
        return _CleanupEvidence(
            report_saved=False,
            apply_result=None,
            warnings=warnings,
        )

    result = metadata.get("result")
    result_saved = isinstance(result, str) and result.strip() != ""
    if not result_saved:
        warnings.append(
            "apply cleanup skipped: saved apply report does not contain result "
            f"metadata: {report_path}"
        )
    return _CleanupEvidence(
        report_saved=True,
        apply_result=result if result_saved else None,
        warnings=warnings,
    )


def _find_apply_report(
    repo_root: Path,
    apply_branch: str,
) -> tuple[Path | None, dict[str, str]]:
    """該当 apply branch の保存済み report と metadata を探す。"""
    report_dir = repo_root / ".cmoc" / "reports" / "apply" / "fork"
    if not report_dir.exists():
        return None, {}

    candidates = sorted(report_dir.glob("*.md"), reverse=True)
    for path in candidates:
        try:
            report = path.read_text(encoding="utf-8")
        except OSError:
            continue
        metadata = _split_yaml_front_matter(report)
        if metadata.get("cmoc_apply_branch") == apply_branch:
            return path, metadata
    return None, {}


def _split_yaml_front_matter(report: str) -> dict[str, str]:
    """apply report の YAML Front Matter を軽量に取り出す。"""
    if not report.startswith("---\n"):
        return {}
    front_matter_end = report.find("\n---\n", 4)
    if front_matter_end == -1:
        return {}

    front_matter: dict[str, str] = {}
    for line in report[4:front_matter_end].splitlines():
        if ":" not in line:
            continue
        key, raw_value = line.split(":", 1)
        value = raw_value.strip()
        if value.startswith('"') and value.endswith('"'):
            try:
                loaded = json.loads(value)
            except json.JSONDecodeError:
                loaded = value[1:-1]
            if isinstance(loaded, str):
                front_matter[key.strip()] = loaded
                continue
        front_matter[key.strip()] = value
    return front_matter


def _cleanup_apply_artifacts(
    repo_root: Path,
    session_id: str,
    join_state: _JoinState,
    cleanup_evidence: _CleanupEvidence,
) -> list[str]:
    """安全条件を満たす場合だけ apply worktree と branch を削除する。"""
    warnings: list[str] = [*cleanup_evidence.warnings]
    if not _cleanup_preconditions_hold(
        repo_root,
        session_id,
        join_state,
        cleanup_evidence,
        warnings,
    ):
        if not warnings:
            warnings.append(
                "apply artifacts were kept because cleanup preconditions failed"
            )
        return warnings

    if join_state.apply_worktree is not None and join_state.apply_worktree.exists():
        if _is_safe_apply_worktree(repo_root, join_state.apply_worktree):
            result = run_git(
                repo_root,
                ["worktree", "remove", str(join_state.apply_worktree)],
                check=False,
            )
            if result.returncode != 0:
                warnings.append(
                    f"apply worktree was not deleted: {join_state.apply_worktree}"
                )
                return warnings
        else:
            warnings.append(
                "apply worktree path is outside .cmoc/worktrees: "
                f"{join_state.apply_worktree}"
            )
            return warnings

    result = run_git(
        repo_root,
        ["branch", "-d", join_state.apply_branch],
        check=False,
    )
    if result.returncode != 0:
        warnings.append(f"apply branch was not deleted: {join_state.apply_branch}")
    return warnings


def _cleanup_preconditions_hold(
    repo_root: Path,
    session_id: str,
    join_state: _JoinState,
    cleanup_evidence: _CleanupEvidence,
    warnings: list[str],
) -> bool:
    """apply artifact 削除の安全条件を検証する。"""
    try:
        saved_state = read_session_state(repo_root, session_id)
    except CmocError as error:
        warnings.append(
            "apply cleanup skipped: session state could not be reloaded after "
            f"recording ready state: {error.message}"
        )
        return False

    apply = saved_state.get("apply")
    if not isinstance(apply, dict) or apply.get("state") != "ready":
        return False
    session = saved_state.get("session")
    if not isinstance(session, dict):
        return False
    if not cleanup_evidence.report_saved:
        return False
    result = session.get("last_joined_apply_result")
    if not isinstance(result, str) or result.strip() == "":
        warnings.append(
            "apply cleanup skipped: apply result was not saved in session state"
        )
        return False
    ancestor = run_git(
        repo_root,
        [
            "merge-base",
            "--is-ancestor",
            join_state.apply_branch,
            join_state.session_branch,
        ],
        check=False,
    )
    if ancestor.returncode != 0:
        return False
    return True


def _is_safe_apply_worktree(repo_root: Path, path: Path) -> bool:
    """削除してよい cmoc 管理 apply worktree path か判定する。"""
    try:
        path.resolve().relative_to((repo_root / ".cmoc" / "worktrees").resolve())
    except ValueError:
        return False
    return True
