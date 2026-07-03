import json
from pathlib import Path

import typer

from cmoc_runtime import (
    ApplyPart,
    CmocError,
    SessionState,
    apply_branch_session_id,
    current_branch,
    delete_branch,
    ensure_cmoc_ignored,
    is_oracle_file_path,
    is_untracked_git_ignored,
    load_state_for_branch,
    remove_worktree,
    repo_root,
    reports_dir,
    require_clean_worktree,
    run_cli_subcommand,
    run_git,
    timestamp,
    work_root,
    write_state,
)
from commons.runtime_apply import worktree_for_branch, worktree_for_branch_optional


def cmoc_apply_join_impl(force_resolve: bool) -> None:
    """CLI runtime を通して apply join を実行する。"""
    run_cli_subcommand(
        _cmoc_apply_join_body,
        force_resolve,
        command_name="apply join",
        command_argv=[
            "cmoc",
            "apply",
            "join",
            *(["--force-resolve"] if force_resolve else []),
        ],
    )


def _cmoc_apply_join_body(force_resolve: bool) -> None:
    """apply branch を session branch へ merge し、apply state を ready に戻す。"""
    repo = repo_root()
    current_root = work_root()
    branch = current_branch(current_root)
    if branch.startswith("cmoc/apply/"):
        require_clean_worktree(current_root)
        session_id = apply_branch_session_id(branch)
        session_branch = f"cmoc/session/{session_id}"
        root = worktree_for_branch(repo, session_branch)
    else:
        root = current_root
        session_branch = branch
    _session_id, path, state = load_state_for_branch(repo, branch)
    if not (branch.startswith("cmoc/session/") or branch.startswith("cmoc/apply/")):
        raise CmocError("apply join は session branch または apply branch 上で実行してください。", [], branch)
    if state.session.state != "active" or state.apply.state not in {"completed", "error"}:
        raise CmocError("join 可能な apply run がありません。", [], str(path))
    require_clean_worktree(root)
    ensure_cmoc_ignored(root)
    apply_branch = state.apply.apply_branch
    if not apply_branch:
        raise CmocError("apply branch を特定できません。", [], str(path))
    if branch.startswith("cmoc/apply/") and branch != apply_branch:
        raise CmocError(
            "現在の apply branch は join 対象の active apply run ではありません。",
            ["session state file が指す apply branch 上、または session branch 上から再実行してください。"],
            f"current_branch: {branch}\napply_branch: {apply_branch}",
        )
    apply_oracle_snapshot_commit = state.apply.oracle_snapshot_commit
    if not apply_oracle_snapshot_commit:
        raise CmocError(
            "apply の oracle snapshot commit を特定できません。",
            ["session state file を確認してください。"],
            str(path),
        )
    apply_worktree = worktree_for_branch_optional(root, apply_branch)
    if apply_worktree:
        require_clean_worktree(apply_worktree)
    unexpected = collect_apply_join_unexpected_changes(root, state, apply_branch, session_branch)
    if unexpected and not force_resolve:
        report_path = write_apply_join_report(
            repo,
            session_branch,
            state,
            apply_branch,
            apply_worktree,
            force_resolve,
            unexpected,
            False,
            [],
        )
        raise CmocError(
            "apply join の想定外差分があります。",
            [
                "--force-resolve で想定外差分を revert するか、手動で内容を確認してください。",
                f"保存済み report を確認してください: {report_path}",
            ],
            json.dumps(unexpected, ensure_ascii=False, indent=2),
        )
    if unexpected and force_resolve:
        revert_unexpected_changes(root, unexpected, state)
    merge = run_git(["merge", "--no-ff", apply_branch], root, check=False)
    if merge.returncode != 0:
        index_conflicts_resolved = resolve_index_conflicts(root)
        merge_conflicts = run_git(
            ["diff", "--name-only", "--diff-filter=U"], root
        ).stdout.splitlines()
        if merge_conflicts:
            report_path = write_apply_join_report(
                repo,
                session_branch,
                state,
                apply_branch,
                apply_worktree,
                force_resolve,
                unexpected,
                False,
                merge_conflicts,
            )
            raise CmocError(
                "apply branch の merge conflict が残っています。",
                [
                    "git status を確認し、手動で解決してください。",
                    f"保存済み report を確認してください: {report_path}",
                ],
                "\n".join(merge_conflicts),
            )
        if not index_conflicts_resolved:
            raise CmocError(
                "apply branch の merge に失敗しました。",
                ["必要なら手動で解決するか、--force-resolve を検討してください。"],
                merge.stderr,
            )
    state.session.last_joined_apply_oracle_snapshot_commit = apply_oracle_snapshot_commit
    state.apply = ApplyPart()
    write_state(path, state)
    warnings: list[str] = []
    merged_reachable = (
        run_git(
            ["merge-base", "--is-ancestor", apply_branch, "HEAD"],
            root,
            check=False,
        ).returncode
        == 0
    )
    report_path = write_apply_join_report(
        repo,
        session_branch,
        state,
        apply_branch,
        apply_worktree,
        force_resolve,
        unexpected,
        merged_reachable,
        [],
    )
    kept_current_worktree = False
    if merged_reachable:
        if apply_worktree:
            if apply_worktree == current_root:
                # <work-root>/oracle/doc/app_spec/misc_spec.md keeps cmoc pwd fixed
                # to the caller's worktree, so join must not chdir away to delete it.
                kept_current_worktree = True
                warnings.append(
                    f"apply worktree remains because it is current cwd: {apply_worktree}"
                )
            else:
                remove_worktree(repo, apply_worktree)
        if not (apply_worktree and apply_worktree.exists()):
            delete_result = delete_branch(repo, apply_branch, force=False)
            if delete_result.returncode != 0:
                warnings.append(f"apply branch was not deleted: {apply_branch}")
    else:
        warnings.append(f"apply branch is not reachable from session HEAD: {apply_branch}")
    if apply_worktree and apply_worktree.exists() and not kept_current_worktree:
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
    merge_conflicts: list[str],
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
            merge_conflicts,
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
    merge_conflicts: list[str],
) -> str:
    unexpected_lines = [
        f"- {kind}: {', '.join(paths)}"
        for kind, paths in unexpected.items()
    ] or ["- なし"]
    conflict_lines = [
        f"- 未解決: {path}" for path in merge_conflicts
    ] or ["- なし"]
    if merge_conflicts:
        result = "apply branch の merge conflict が残っています。cmoc は自動解決しませんでした。"
    elif unexpected and not force_resolve:
        result = "apply join の想定外差分を検出したため、join を中止しました。"
    else:
        result = "apply branch を session branch へ join しました。"
    return "\n".join(
        [
            "---",
            f"cmoc_session_branch: {session_branch}",
            f"cmoc_apply_branch: {apply_branch}",
            f"cmoc_apply_worktree: {apply_worktree}",
            "last_joined_apply_oracle_snapshot_commit: "
            f"{state.session.last_joined_apply_oracle_snapshot_commit}",
            f"force_resolve: {force_resolve}",
            f"cleanup_reachable: {cleanup_reachable}",
            "---",
            "# cmoc apply join 結果レポート",
            "## 結果",
            result,
            "## 想定外差分",
            *unexpected_lines,
            "## マージコンフリクト",
            *conflict_lines,
            "",
        ]
    )


def collect_apply_join_unexpected_changes(
    root: Path,
    state: SessionState,
    apply_branch: str,
    session_branch: str,
) -> dict[str, list[str]]:
    """apply/session branch 上の想定外差分を分類して返す。"""
    base = (
        state.apply.oracle_snapshot_commit
        or state.session.session_start_commit
        or "HEAD"
    )
    apply_paths = changed_paths_on_managed_branch(root, base, apply_branch)
    session_paths = changed_paths_on_managed_branch(root, base, session_branch)
    unexpected_apply = [
        path for path in apply_paths if not is_expected_apply_change(root, path)
    ]
    unexpected_session = [
        path for path in session_paths if not is_expected_session_change(root, path)
    ]
    result: dict[str, list[str]] = {}
    if unexpected_apply:
        result["apply"] = unexpected_apply
    if unexpected_session:
        result["session"] = unexpected_session
    return result


def changed_paths_on_managed_branch(root: Path, base: str, branch: str) -> list[str]:
    # <work-root>/oracle/doc/app_spec/misc_spec.md requires deleted paths to be
    # outside managed-branch change scope, and renames to be classified by new path.
    lines = run_git(
        [
            "diff",
            "--name-status",
            "--find-renames",
            "--diff-filter=ACMRT",
            base,
            branch,
        ],
        root,
    ).stdout.splitlines()
    paths: list[str] = []
    for line in lines:
        columns = line.split("\t")
        if columns[0].startswith(("C", "R")):
            paths.append(columns[2])
        else:
            paths.append(columns[1])
    return paths


def is_expected_apply_change(root: Path, path: str) -> bool:
    """apply branch 上で許可される差分かどうかを判定する。"""
    p = Path(path)
    if p.name == "INDEX.md":
        return True
    if p.name == "AGENTS.md":
        return False
    if path.startswith((".git/", ".codex/")):
        return False
    if path.startswith(("oracle/", ".agents/")) or is_root_memo_path(path):
        return False
    return not is_untracked_git_ignored(root, root / path)


def is_expected_session_change(root: Path, path: str) -> bool:
    """session branch 上で apply 実行中に許可される差分かどうかを判定する。"""
    p = Path(path)
    if p.name == "INDEX.md" or is_root_memo_path(path):
        return True
    return is_oracle_file_path(root, root / path)


def is_root_memo_path(path: str) -> bool:
    # <work-root>/oracle/doc/app_spec/sub_command/apply_join.md treats root memo
    # and paths below it as session-side changes, not apply-side products.
    return path == "memo" or path.startswith("memo/")


def revert_unexpected_changes(
    root: Path,
    unexpected: dict[str, list[str]],
    state: SessionState,
) -> None:
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
