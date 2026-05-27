"""`cmoc apply join` の本体処理。"""

import json
import os
from pathlib import Path

from commons.command_runner import run_command
from commons.errors import CmocError
from commons.repo import (
    apply_worktree_path_from_branch,
    assert_no_uncommitted_changes,
    current_branch,
    is_apply_branch,
    is_implementation_path,
    is_session_branch,
    read_session_state,
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
    if merge_result.returncode != 0:
        unmerged = _unmerged_paths(cmoc_root)
        detail = merge_result.stderr.strip()
        if unmerged:
            detail = "\n".join(["unmerged paths:", *unmerged, detail]).strip()
        raise CmocError(
            "apply branch の merge で conflict が発生しました。",
            [
                "cmoc は apply join の conflict を自動解消しません。",
                "git status を確認し、手動で merge 状態を解消してください。",
            ],
            detail,
        )

    start_step(timer, 5, 5, "record ready apply state")
    cleanup_evidence = _snapshot_cleanup_evidence(cmoc_root, join_state)
    _mark_apply_ready(cmoc_root, session_id, state)
    warnings = _cleanup_apply_artifacts(
        cmoc_root,
        join_state,
        state,
        cleanup_evidence,
    )
    print(f"joined apply branch: {join_state.apply_branch}")
    print(f"session branch: {join_state.session_branch}")
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
        result_saved: bool,
        warnings: list[str],
    ) -> None:
        self.report_saved = report_saved
        self.result_saved = result_saved
        self.warnings = warnings


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
            ["state JSON の session/apply セクションを確認してください。"],
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
    if apply.get("state") != "completed":
        raise CmocError(
            "join 可能な apply run ではありません。",
            [
                "`cmoc apply fork` が完了してから `cmoc apply join` を実行してください。",
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
    apply_paths = _changed_paths_between(
        repo_root,
        join_state.oracle_snapshot_commit,
        join_state.apply_branch,
    )
    for path in apply_paths:
        if not is_implementation_path(repo_root, path):
            unexpected.append(f"{join_state.apply_branch}: {path}")

    session_paths = _changed_paths_between(
        repo_root,
        join_state.oracle_snapshot_commit,
        join_state.session_branch,
    )
    for path in session_paths:
        if not _is_oracle_path(path):
            unexpected.append(f"{join_state.session_branch}: {path}")
    return unexpected


def _changed_paths_between(
    repo_root: Path,
    base_commit: str,
    branch_name: str,
) -> list[str]:
    """base..branch の変更後 path を返す。"""
    result = run_git(
        repo_root,
        ["diff", "--name-status", "-M", f"{base_commit}..{branch_name}", "--"],
    )
    paths: list[str] = []
    for line in result.stdout.splitlines():
        parts = line.split("\t")
        if not parts:
            continue
        status = parts[0]
        if status.startswith(("R", "C")) and len(parts) >= 3:
            paths.append(parts[2])
        elif len(parts) >= 2:
            paths.append(parts[1])
    return paths


def _is_oracle_path(path: str) -> bool:
    """oracle ファイル側の変更とみなす path か判定する。"""
    return path == "oracles" or path.startswith("oracles/")


def _force_resolve_unexpected_diffs(
    repo_root: Path,
    join_state: _JoinState,
) -> None:
    """想定外差分を snapshot の内容へ戻す。"""
    _revert_branch_paths(
        repo_root,
        join_state.apply_branch,
        join_state.oracle_snapshot_commit,
        [
            path
            for path in _changed_paths_between(
                repo_root,
                join_state.oracle_snapshot_commit,
                join_state.apply_branch,
            )
            if not is_implementation_path(repo_root, path)
        ],
        join_state.apply_worktree,
    )
    _revert_branch_paths(
        repo_root,
        join_state.session_branch,
        join_state.oracle_snapshot_commit,
        [
            path
            for path in _changed_paths_between(
                repo_root,
                join_state.oracle_snapshot_commit,
                join_state.session_branch,
            )
            if not _is_oracle_path(path)
        ],
        repo_root,
    )


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
    worktree = branch_worktree or repo_root
    if current_branch(worktree) != branch_name:
        run_git(worktree, ["switch", branch_name])
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
    if run_git(worktree, ["diff", "--cached", "--quiet"], check=False).returncode == 1:
        run_git(
            worktree,
            [
                "commit",
                "-m",
                f"Revert unexpected apply join changes on {branch_name}",
            ],
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
    result = run_git(repo_root, ["diff", "--name-only", "--diff-filter=U"])
    return [line for line in result.stdout.splitlines() if line]


def _mark_apply_ready(
    repo_root: Path,
    session_id: str,
    state: dict[str, object],
) -> None:
    """apply セクションを ready に戻し、固定 field を null 初期化する。"""
    apply = state.get("apply")
    if not isinstance(apply, dict):
        raise CmocError(
            "session state ファイルの形式が不正です。",
            ["state JSON の apply セクションを確認してください。"],
        )
    state["apply"] = {
        "state": "ready",
        "apply_branch": None,
        "oracle_snapshot_commit": None,
    }
    write_session_state(repo_root, session_id, state)


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
            result_saved=False,
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
        result_saved=result_saved,
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
    join_state: _JoinState,
    state: dict[str, object],
    cleanup_evidence: _CleanupEvidence,
) -> list[str]:
    """安全条件を満たす場合だけ apply worktree と branch を削除する。"""
    warnings: list[str] = [*cleanup_evidence.warnings]
    if not _cleanup_preconditions_hold(repo_root, join_state, state, cleanup_evidence):
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
        else:
            warnings.append(
                "apply worktree path is outside .cmoc/worktrees: "
                f"{join_state.apply_worktree}"
            )

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
    join_state: _JoinState,
    state: dict[str, object],
    cleanup_evidence: _CleanupEvidence,
) -> bool:
    """apply artifact 削除の安全条件を検証する。"""
    apply = state.get("apply")
    if not isinstance(apply, dict) or apply.get("state") != "ready":
        return False
    if not cleanup_evidence.report_saved or not cleanup_evidence.result_saved:
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
