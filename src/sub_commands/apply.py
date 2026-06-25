import json
import os
import signal
import time
from pathlib import Path

import typer

from cmoc_runtime import (
    ApplyPart,
    CmocError,
    SessionState,
    branch_exists,
    current_branch,
    delete_branch,
    ensure_cmoc_ignored,
    is_git_ignored,
    load_state_for_branch,
    remove_worktree,
    repo_root,
    reports_dir,
    require_clean_worktree,
    run_git,
    timestamp,
    work_root,
    write_state,
)


def cmoc_apply_join_impl(force_resolve: bool) -> None:
    """apply branch を session branch へ merge し、apply state を ready に戻す。"""
    repo = repo_root()
    current_root = work_root()
    branch = current_branch(current_root)
    if branch.startswith("cmoc/apply/"):
        require_clean_worktree(current_root)
        parts = branch.split("/")
        session_id = parts[2] if len(parts) >= 4 else ""
        session_branch = f"cmoc/session/{session_id}"
        root = worktree_for_branch(repo, session_branch)
        os.chdir(root)
    else:
        root = repo
        session_branch = branch
    _session_id, path, state = load_state_for_branch(root, branch)
    if not (branch.startswith("cmoc/session/") or branch.startswith("cmoc/apply/")):
        raise CmocError("apply join は session branch または apply branch 上で実行してください。", [], branch)
    if state.session.state != "active" or state.apply.state not in {"completed", "error"}:
        raise CmocError("join 可能な apply run がありません。", [], str(path))
    require_clean_worktree(root)
    ensure_cmoc_ignored(root)
    apply_branch = state.apply.apply_branch
    if not apply_branch:
        raise CmocError("apply branch を特定できません。", [], str(path))
    apply_worktree = worktree_for_branch_optional(root, apply_branch)
    if apply_worktree:
        require_clean_worktree(apply_worktree)
    unexpected = collect_apply_join_unexpected_changes(root, state, apply_branch, session_branch)
    if unexpected and not force_resolve:
        raise CmocError(
            "apply join の想定外差分があります。",
            ["--force-resolve で想定外差分を revert するか、手動で内容を確認してください。"],
            json.dumps(unexpected, ensure_ascii=False, indent=2),
        )
    if unexpected and force_resolve:
        revert_unexpected_changes(root, unexpected, state)
    merge = run_git(["merge", "--no-ff", apply_branch], root, check=False)
    if merge.returncode != 0 and not resolve_index_conflicts(root) and not force_resolve:
        raise CmocError(
            "apply branch の merge に失敗しました。",
            ["必要なら手動で解決するか、--force-resolve を検討してください。"],
            merge.stderr,
        )
    if merge.returncode != 0 and run_git(["diff", "--name-only", "--diff-filter=U"], root).stdout.strip():
        raise CmocError(
            "apply branch の merge conflict が残っています。",
            ["git status を確認し、手動で解決してください。"],
            run_git(["diff", "--name-only", "--diff-filter=U"], root).stdout,
        )
    joined_apply_oracle_snapshot_commit = state.apply.oracle_snapshot_commit
    state.session.last_joined_apply_oracle_snapshot_commit = (
        joined_apply_oracle_snapshot_commit
    )
    state.apply = ApplyPart()
    write_state(path, state)
    warnings: list[str] = []
    merged_reachable = run_git(["merge-base", "--is-ancestor", apply_branch, "HEAD"], root, check=False).returncode == 0
    report_path = write_apply_join_report(
        root,
        session_branch,
        state,
        apply_branch,
        apply_worktree,
        force_resolve,
        unexpected,
        merged_reachable,
    )
    if merged_reachable:
        if apply_worktree:
            remove_worktree(root, apply_worktree)
        delete_result = delete_branch(root, apply_branch, force=False)
        if delete_result.returncode != 0:
            warnings.append(f"apply branch was not deleted: {apply_branch}")
    else:
        warnings.append(f"apply branch is not reachable from session HEAD: {apply_branch}")
    if apply_worktree and apply_worktree.exists():
        warnings.append(f"apply worktree remains: {apply_worktree}")
    warning_lines = [f"  - {warning}" for warning in warnings] if warnings else ["  - none"]
    typer.echo(
        "\n".join(
            [
                "# cmoc apply join",
                f"- joined_apply_branch: `{apply_branch}`",
                f"- removed_apply_worktree: `{apply_worktree}`",
                f"- force_resolve: `{force_resolve}`",
                f"- cleanup_reachable: `{merged_reachable}`",
                f"- report: `{report_path}`",
                "- warnings:",
                *warning_lines,
            ]
        )
    )


def write_apply_join_report(
    root: Path,
    session_branch: str,
    state: SessionState,
    apply_branch: str,
    apply_worktree: Path | None,
    force_resolve: bool,
    unexpected: dict[str, list[str]],
    cleanup_reachable: bool,
) -> Path:
    report_dir = reports_dir(root, "apply/join")
    report_dir.mkdir(parents=True, exist_ok=True)
    path = report_dir / f"{timestamp()}.md"
    path.write_text(
        render_apply_join_report(
            session_branch,
            state,
            apply_branch,
            apply_worktree,
            force_resolve,
            unexpected,
            cleanup_reachable,
        )
    )
    return path


def render_apply_join_report(
    session_branch: str,
    state: SessionState,
    apply_branch: str,
    apply_worktree: Path | None,
    force_resolve: bool,
    unexpected: dict[str, list[str]],
    cleanup_reachable: bool,
) -> str:
    unexpected_lines = [
        f"- {kind}: {', '.join(paths)}"
        for kind, paths in unexpected.items()
    ] or ["- none"]
    return "\n".join(
        [
            "---",
            f"cmoc_session_branch: {session_branch}",
            f"cmoc_apply_branch: {apply_branch}",
            f"cmoc_apply_worktree: {apply_worktree}",
            "joined_apply_oracle_snapshot_commit: "
            f"{state.session.last_joined_apply_oracle_snapshot_commit}",
            f"force_resolve: {force_resolve}",
            f"cleanup_reachable: {cleanup_reachable}",
            "---",
            "# cmoc apply join report",
            "## Result",
            "apply branch を session branch へ join しました。",
            "## Unexpected Changes",
            *unexpected_lines,
            "",
        ]
    )


def collect_apply_join_unexpected_changes(root: Path, state: SessionState, apply_branch: str, session_branch: str) -> dict[str, list[str]]:
    """apply/session branch 上の想定外差分を分類して返す。"""
    base = state.apply.oracle_snapshot_commit or state.session.session_start_commit or "HEAD"
    apply_paths = run_git(["diff", "--name-only", base, apply_branch], root).stdout.splitlines()
    session_paths = run_git(["diff", "--name-only", base, session_branch], root).stdout.splitlines()
    unexpected_apply = [path for path in apply_paths if not is_expected_apply_change(root, path)]
    unexpected_session = [path for path in session_paths if not is_expected_session_change(path)]
    result: dict[str, list[str]] = {}
    if unexpected_apply:
        result["apply"] = unexpected_apply
    if unexpected_session:
        result["session"] = unexpected_session
    return result


def is_expected_apply_change(root: Path, path: str) -> bool:
    """apply branch 上で許可される差分かどうかを判定する。"""
    p = Path(path)
    if p.name == "INDEX.md":
        return True
    if path == ".gitignore" or path.startswith(".git/"):
        return False
    if path.startswith(("oracle/", "memo/", ".agents/")):
        return False
    return not is_git_ignored(root, root / path)


def is_expected_session_change(path: str) -> bool:
    """session branch 上で apply 実行中に許可される差分かどうかを判定する。"""
    p = Path(path)
    return p.name == "INDEX.md" or path.startswith("oracle/") or path.startswith("memo/")


def revert_unexpected_changes(root: Path, unexpected: dict[str, list[str]], state: SessionState) -> None:
    """force-resolve 時に想定外差分を apply fork 基準へ戻す。"""
    base = state.apply.oracle_snapshot_commit or state.session.session_start_commit
    if not base:
        raise CmocError(
            "想定外差分を revert する基準 commit を特定できません。",
            ["session state file を確認してください。"],
            json.dumps(state.to_dict(), ensure_ascii=False, indent=2),
        )
    for path in unexpected.get("session", []):
        restore_path_from_commit(root, base, path)
    session_changed = run_git(["status", "--short"], root).stdout.strip()
    if session_changed:
        run_git(["add", "."], root)
        run_git(["commit", "-m", "cmoc apply join force-resolve session changes"], root)
    apply_branch = state.apply.apply_branch
    if apply_branch and unexpected.get("apply"):
        apply_root = worktree_for_branch_optional(root, apply_branch)
        if apply_root is None:
            raise CmocError(
                "apply worktree を特定できません。",
                ["git worktree list を確認してから再実行してください。"],
                f"apply_branch: {apply_branch}",
            )
        for path in unexpected["apply"]:
            restore_path_from_commit(apply_root, base, path)
        apply_changed = run_git(["status", "--short"], apply_root).stdout.strip()
        if apply_changed:
            run_git(["add", "."], apply_root)
            run_git(["commit", "-m", "cmoc apply join force-resolve apply changes"], apply_root)


def restore_path_from_commit(root: Path, commit: str, path: str) -> None:
    """path を指定 commit の内容へ戻し、存在しない場合は削除する。"""
    exists = run_git(["cat-file", "-e", f"{commit}:{path}"], root, check=False).returncode == 0
    if exists:
        run_git(["checkout", commit, "--", path], root)
    else:
        target = root / path
        if target.exists():
            run_git(["rm", "-f", path], root)


def resolve_index_conflicts(root: Path) -> bool:
    """INDEX.md だけの merge conflict を削除 commit で機械解決する。"""
    conflicted = run_git(["diff", "--name-only", "--diff-filter=U"], root).stdout.splitlines()
    if not conflicted:
        return False
    if any(Path(path).name != "INDEX.md" for path in conflicted):
        return False
    for path in conflicted:
        run_git(["rm", "-f", path], root)
    run_git(["commit", "--no-edit"], root)
    return True


def cmoc_apply_abandon_impl() -> None:
    """未 join の apply run を破棄して apply state を ready に戻す。"""
    repo = repo_root()
    current_root = work_root()
    branch = current_branch(current_root)
    if not (branch.startswith("cmoc/session/") or branch.startswith("cmoc/apply/")):
        raise CmocError("apply abandon は session branch または apply branch 上で実行してください。", [], branch)
    if branch.startswith("cmoc/apply/"):
        session_id = branch.split("/")[2]
        session_branch = f"cmoc/session/{session_id}"
        root = worktree_for_branch(repo, session_branch)
    else:
        root = repo
    _session_id, path, state = load_state_for_branch(root, branch)
    if state.session.state != "active" or state.apply.state == "ready":
        raise CmocError("破棄対象の active apply run がありません。", [], str(path))
    require_clean_worktree(root)
    previous = state.apply.state
    apply_branch = state.apply.apply_branch
    apply_worktree = worktree_for_branch_optional(root, apply_branch) if apply_branch else None
    if not apply_branch:
        raise CmocError(
            "破棄対象 apply run の補助情報を特定できません。",
            ["session state file の apply.apply_branch を確認してください。"],
            str(path),
        )
    warnings: list[str] = []
    if previous == "running":
        process_id = state.apply.apply_process_id
        if process_id is None:
            raise CmocError(
                "実行中 apply process を特定できません。",
                ["session state file の apply.apply_process_id を確認してください。"],
                str(path),
            )
        stopped_warning = stop_apply_process(process_id)
        if stopped_warning:
            warnings.append(stopped_warning)
    if branch == apply_branch:
        os.chdir(root)
    if apply_worktree:
        remove_worktree(root, apply_worktree)
    else:
        warnings.append(f"apply worktree already missing for branch: {apply_branch}")
    if not branch_exists(root, apply_branch):
        warnings.append(f"apply branch already missing: {apply_branch}")
    else:
        delete_branch(root, apply_branch, force=True)
    if apply_worktree and apply_worktree.exists():
        warnings.append(f"orphan apply worktree remains: {apply_worktree}")
    if branch_exists(root, apply_branch):
        warnings.append(f"orphan apply branch remains: {apply_branch}")
    state.apply = ApplyPart()
    write_state(path, state)
    warning_lines = [f"  - {warning}" for warning in warnings] if warnings else ["  - none"]
    typer.echo(
        "\n".join(
            [
                "# cmoc apply abandon",
                f"- apply_branch: `{apply_branch}`",
                f"- apply_worktree: `{apply_worktree}`",
                f"- before: `{previous}`",
                "- after: `ready`",
                "- warnings:",
                *warning_lines,
            ]
        )
    )


def worktree_for_branch(root: Path, branch: str) -> Path:
    """branch が checkout されている linked worktree を返す。"""
    path = worktree_for_branch_optional(root, branch)
    if path is not None:
        return path
    raise CmocError(
        "session branch の worktree を特定できません。",
        ["git worktree list を確認し、session branch の worktree から再実行してください。"],
        f"branch: {branch}",
    )


def worktree_for_branch_optional(root: Path, branch: str) -> Path | None:
    """branch が checkout されている linked worktree を返し、無ければ None を返す。"""
    output = run_git(["worktree", "list", "--porcelain"], root).stdout
    current_path: Path | None = None
    for line in output.splitlines():
        if line.startswith("worktree "):
            current_path = Path(line.removeprefix("worktree ")).resolve()
        elif line == f"branch refs/heads/{branch}" and current_path is not None:
            return current_path
    return None


def stop_apply_process(process_id: int) -> str | None:
    """running abandon では cleanup 前に apply process が消えたことを確認する。"""
    if process_id == os.getpid():
        raise CmocError(
            "現在の apply abandon process は停止対象にできません。",
            ["別 process から cmoc apply abandon を実行してください。"],
            f"pid: {process_id}",
        )
    if not process_exists(process_id):
        return f"apply process already stopped: {process_id}"
    os.kill(process_id, signal.SIGTERM)
    if wait_process_exit(process_id, 5.0):
        return None
    os.kill(process_id, signal.SIGKILL)
    if wait_process_exit(process_id, 5.0):
        return None
    raise CmocError(
        "実行中 apply process を停止できません。",
        ["apply process を確認して停止後に再実行してください。"],
        f"pid: {process_id}",
    )


def wait_process_exit(process_id: int, timeout_sec: float) -> bool:
    deadline = time.monotonic() + timeout_sec
    while time.monotonic() < deadline:
        if not process_exists(process_id):
            return True
        time.sleep(0.1)
    return not process_exists(process_id)


def process_exists(process_id: int) -> bool:
    if process_id <= 0:
        return False
    try:
        os.kill(process_id, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    return True
