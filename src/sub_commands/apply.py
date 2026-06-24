import json
import os
from pathlib import Path
from typing import Callable

import typer

from acp.builder.apply.fork.finding_application import (
    build_apply_fork_finding_application_parameter,
)
from acp.builder.apply.fork.refine_finding import (
    build_apply_fork_refine_finding_parameter,
)
from cmoc_runtime import (
    ApplyPart,
    CmocError,
    SessionState,
    branch_exists,
    create_run_worktree,
    current_branch,
    delete_branch,
    ensure_cmoc_ignored,
    head_commit,
    is_git_ignored,
    load_config,
    load_state_for_branch,
    pushd,
    remove_worktree,
    repo_root,
    require_clean_worktree,
    run_git,
    timestamp,
    work_root,
    worktrees_dir,
    write_state,
)
from config.cmoc_config import CmocConfig


CodexExec = Callable[..., object]
EnumerateApplyTargets = Callable[[Path, str, SessionState | None], list[Path]]
EnumerateApplyFindings = Callable[[Path, list[Path], CmocConfig], list[dict]]


def cmoc_apply_fork_impl(
    scope: str,
    codex_exec: CodexExec,
    enumerate_targets: Callable[..., list[Path]],
    enumerate_findings_for_targets: Callable[..., list[dict]],
    related_paths: Callable[[Path, list[dict]], list[Path]],
    ensure_no_forbidden_diff: Callable[[Path], None],
    changed_paths: Callable[[Path], list[Path]],
    generate_commit_message: Callable[[Path, Path, dict, CmocConfig], str],
    normalize_targets: Callable[[Path, set[Path]], list[Path]],
    write_report: Callable[[Path, Path, str, SessionState, list[int], str, CmocConfig], Path],
    write_error_report: Callable[[Path, str, SessionState, list[int], Path], Path],
) -> int:
    """Codex CLI による apply loop を isolated apply worktree 上で実行する。"""
    if scope not in {"rolling", "session", "full"}:
        raise CmocError("scope が不正です。", ["rolling, session, full のいずれかを指定してください。"], scope)
    root = repo_root()
    branch = current_branch(root)
    session_id, path, state = load_state_for_branch(root, branch)
    if not branch.startswith("cmoc/session/"):
        raise CmocError("apply fork は session branch 上で実行してください。", [], branch)
    if state.session.state != "active" or state.apply.state != "ready":
        raise CmocError("apply fork の事前条件を満たしていません。", [], str(path))
    require_clean_worktree(root)
    ensure_cmoc_ignored(root)
    run_id = timestamp()
    apply_branch = f"cmoc/apply/{session_id}/{run_id}"
    oracle_snapshot_commit = head_commit(root)
    apply_worktree = worktrees_dir(root) / session_id / run_id
    create_run_worktree(root, apply_branch, apply_worktree, "HEAD")
    state.apply = ApplyPart(
        state="running",
        apply_branch=apply_branch,
        oracle_snapshot_commit=oracle_snapshot_commit,
    )
    write_state(path, state)
    config = load_config(root)
    finding_counts: list[int] = []
    result_label = "error"
    report_path: Path | None = None
    try:
        with pushd(apply_worktree):
            findings: list[dict] = []
            dirty_targets = enumerate_targets(apply_worktree, scope, state)
            for _apply_loop in range(config.apply_fork.num_apply_loop):
                if not dirty_targets:
                    result_label = "unconverged" if findings else "converged"
                    break
                findings = enumerate_findings_for_targets(
                    apply_worktree,
                    dirty_targets,
                    config,
                    log_root=root,
                )
                for _ in range(config.apply_fork.num_improve_findings_loop):
                    refined = codex_exec(
                        build_apply_fork_refine_finding_parameter({"findings": findings}),
                        root=root,
                        cwd=apply_worktree,
                        config=config,
                        purpose="apply fork refine findings",
                    ).output_json
                    next_findings = list((refined or {}).get("findings", []))
                    if next_findings == findings:
                        break
                    findings = next_findings
                finding_counts.append(len(findings))
                if not findings:
                    result_label = "converged"
                    break
                next_dirty = set(related_paths(apply_worktree, findings))
                for finding in findings:
                    codex_exec(
                        build_apply_fork_finding_application_parameter(
                            json.dumps(finding, ensure_ascii=False, indent=2)
                        ),
                        root=root,
                        cwd=apply_worktree,
                        config=config,
                        purpose="apply fork finding application",
                    )
                    ensure_no_forbidden_diff(apply_worktree)
                    changed = changed_paths(apply_worktree)
                    next_dirty.update(changed)
                    if changed:
                        commit_message = generate_commit_message(
                            root,
                            apply_worktree,
                            finding,
                            config,
                        )
                        run_git(["add", "."], apply_worktree)
                        run_git(["commit", "-m", commit_message], apply_worktree)
                dirty_targets = normalize_targets(apply_worktree, next_dirty)
            else:
                result_label = "unconverged"
            report_path = write_report(
                root,
                apply_worktree,
                branch,
                state,
                finding_counts,
                result_label,
                config,
            )
        state.apply.state = "completed"
        write_state(path, state)
    except BaseException:
        state.apply.state = "error"
        write_state(path, state)
        if report_path is None:
            write_error_report(root, branch, state, finding_counts, apply_worktree)
        raise
    typer.echo(
        "\n".join(
            [
                "# cmoc apply fork",
                f"- scope: `{scope}`",
                f"- apply_branch: `{apply_branch}`",
                f"- apply_worktree: `{apply_worktree}`",
                f"- oracle_snapshot_commit: `{oracle_snapshot_commit}`",
                f"- findings: `{len(findings)}`",
                f"- result: `{state.apply.state}`",
                f"- result_label: `{result_label}`",
                f"- report: `{report_path}`",
            ]
        )
    )
    return 2 if result_label == "unconverged" else 0


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
    state.session.last_joined_apply_commit = head_commit(root)
    apply_worktree = worktree_for_branch_optional(root, apply_branch)
    state.apply = ApplyPart()
    write_state(path, state)
    warnings: list[str] = []
    merged_reachable = run_git(["merge-base", "--is-ancestor", apply_branch, "HEAD"], root, check=False).returncode == 0
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
                "- warnings:",
                *warning_lines,
            ]
        )
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
