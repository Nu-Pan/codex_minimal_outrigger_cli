"""apply join の差分判定、merge、report、後始末を一つの実行単位として扱う。

このファイルは 16,000 文字を超えるが、各処理は同じ apply/session state、
worktree、branch の失敗時文脈を共有するため、分割せず一箇所で追える凝集した責務である。
根拠: {{work-root}}/oracle/src/oracle/prompt_builder/parts/realization_standard.py
"""

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
    load_state_for_branch,
    remove_worktree,
    repo_root,
    reports_dir,
    require_clean_worktree,
    run_cli_subcommand,
    run_git,
    start_subcommand_step,
    timestamp,
    work_root,
    write_state,
)
from commons.runtime_apply import (
    apply_process_id_path,
    apply_run_lock,
    delete_apply_process_id,
    read_apply_process_id,
    stop_apply_process,
    worktree_for_branch,
    worktree_for_branch_optional,
)
from commons.runtime_git import is_realization_file_path


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
        total_steps=8,
    )


def _cmoc_apply_join_body(force_resolve: bool) -> None:
    """apply branch を session branch へ merge し、apply state を ready に戻す。"""
    repo = repo_root()
    current_root = work_root()
    start_subcommand_step(2, "事前条件を確認", "validate preconditions")
    branch = current_branch(current_root)
    if branch.startswith("cmoc/apply/"):
        session_id = apply_branch_session_id(branch)
    else:
        session_id, _, _ = load_state_for_branch(repo, branch)
    with apply_run_lock(repo, session_id):
        _cmoc_apply_join_locked(repo, current_root, branch, force_resolve, session_id)


def _cmoc_apply_join_locked(
    repo: Path,
    current_root: Path,
    branch: str,
    force_resolve: bool,
    session_id: str,
) -> None:
    """lock 内で state の再読込から merge・report・cleanup までを直列化する。

    根拠: {{work-root}}/oracle/doc/app_spec/sub_command/apply_join.md
    """
    start_subcommand_step(3, "apply branch の前準備", "prepare apply branch")
    if branch.startswith("cmoc/apply/"):
        session_branch = f"cmoc/session/{session_id}"
        root = worktree_for_branch(repo, session_branch)
    else:
        root = current_root
        session_branch = branch
    session_id, path, state = load_state_for_branch(repo, branch)
    start_subcommand_step(4, "session branch の前準備", "prepare session branch")
    if state.session.state != "active" or state.apply.state not in {
        "completed",
        "error",
    }:
        raise CmocError("join 可能な apply run がありません。", [], str(path))
    apply_branch = state.apply.apply_branch
    if not apply_branch:
        raise CmocError("apply branch を特定できません。", [], str(path))
    if apply_branch_session_id(apply_branch) != session_id:
        raise CmocError(
            "apply branch が現在の session に属していません。",
            ["session state file の apply.apply_branch を確認してください。"],
            f"session_id: {session_id}\napply_branch: {apply_branch}",
        )
    if branch.startswith("cmoc/apply/") and branch != apply_branch:
        raise CmocError(
            "現在の apply branch は join 対象の active apply run ではありません。",
            [
                "session state file が指す apply branch 上、または session branch 上から再実行してください。"
            ],
            f"current_branch: {branch}\napply_branch: {apply_branch}",
        )
    apply_oracle_snapshot_commit = state.apply.oracle_snapshot_commit
    if not apply_oracle_snapshot_commit:
        raise CmocError(
            "apply の oracle snapshot commit を特定できません。",
            ["session state file を確認してください。"],
            str(path),
        )
    warnings: list[str] = []
    if state.apply.state == "error":
        warning = _stop_error_apply_process(repo, session_id)
        if warning:
            warnings.append(warning)
    require_clean_worktree(root)
    ensure_cmoc_ignored(root)
    apply_worktree = worktree_for_branch_optional(root, apply_branch)
    if apply_worktree:
        require_clean_worktree(apply_worktree)
    start_subcommand_step(5, "apply branch の差分を確認", "check unexpected changes")
    unexpected = collect_apply_join_unexpected_changes(
        root, state, apply_branch, session_branch, apply_worktree
    )
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
    start_subcommand_step(6, "apply branch を merge", "merge apply branch")
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
    start_subcommand_step(7, "apply state を更新", "update apply state")
    state.session.last_joined_apply_oracle_snapshot_commit = (
        apply_oracle_snapshot_commit
    )
    state.apply = ApplyPart()
    write_state(path, state)
    merged_reachable = (
        run_git(
            ["merge-base", "--is-ancestor", apply_branch, "HEAD"],
            root,
            check=False,
        ).returncode
        == 0
    )
    start_subcommand_step(8, "結果をレポートして後始末", "report and cleanup")
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
                # {{work-root}}/oracle/doc/app_spec/misc_spec.md は呼び出し元 worktree
                # の cwd を固定するため、削除のために chdir してはならない。
                kept_current_worktree = True
                warnings.append(
                    "apply worktree remains because it is current cwd: "
                    f"{apply_worktree}"
                )
            else:
                remove_worktree(repo, apply_worktree)
        if not (apply_worktree and apply_worktree.exists()):
            delete_result = delete_branch(repo, apply_branch, force=False)
            if delete_result.returncode != 0:
                warnings.append(f"apply branch was not deleted: {apply_branch}")
    else:
        warnings.append(
            f"apply branch is not reachable from session HEAD: {apply_branch}"
        )
    if apply_worktree and apply_worktree.exists() and not kept_current_worktree:
        warnings.append(f"apply worktree remains: {apply_worktree}")
    warning_lines = (
        [f"  - {warning}" for warning in warnings] if warnings else ["  - none"]
    )
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


def _stop_error_apply_process(repo: Path, session_id: str) -> str | None:
    """error state の apply process と Codex child を停止して pid file を消す。

    error state では fork が残した child process が apply worktree を変更し得る。
    そのため、clean 検査より先に停止し、停止対象を読めない pid file は安全側で
    join を中止する。根拠: {{work-root}}/oracle/doc/app_spec/sub_command/apply_join.md
    """
    tracking_path = apply_process_id_path(repo, session_id)
    process = read_apply_process_id(repo, session_id)
    if process is None:
        if tracking_path.exists():
            raise CmocError(
                "apply process tracking を読み取れません。",
                [
                    "apply process を確認し、tracking file を修復してから再実行してください。"
                ],
                str(tracking_path),
            )
        return None
    warning = stop_apply_process(
        process,
        lambda: read_apply_process_id(repo, session_id),
    )
    delete_apply_process_id(repo, session_id)
    return warning


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
    """apply join の結果を timestamp 付き Markdown report として保存する。

    根拠: {{work-root}}/oracle/doc/app_spec/sub_command/apply_join.md
    """
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
    """apply join の state・差分・conflict を Markdown report 本文へ描画する。

    根拠: {{work-root}}/oracle/doc/app_spec/sub_command/apply_join.md
    """
    unexpected_lines = [
        f"- {kind}: {', '.join(paths)}" for kind, paths in unexpected.items()
    ] or ["- なし"]
    conflict_lines = [f"- 未解決: {path}" for path in merge_conflicts] or ["- なし"]
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
    apply_worktree: Path | None = None,
) -> dict[str, list[str]]:
    """apply/session branch 上の想定外差分を分類して返す。

    根拠: {{work-root}}/oracle/doc/app_spec/sub_command/apply_join.md
    """
    base = (
        state.apply.oracle_snapshot_commit
        or state.session.session_start_commit
        or "HEAD"
    )
    apply_paths = changed_paths_on_managed_branch(root, base, apply_branch)
    session_paths = changed_paths_on_managed_branch(root, base, session_branch)
    unexpected_apply = [
        path
        for path in apply_paths
        if not is_expected_apply_change(
            root, path, apply_branch=apply_branch, apply_worktree=apply_worktree
        )
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
    """managed branch の差分を削除 path 除外・rename 先優先で列挙する。

    根拠: {{work-root}}/oracle/doc/app_spec/misc_spec.md
    """
    lines = managed_branch_name_status_lines(root, base, branch)
    paths: list[str] = []
    for line in lines:
        columns = line.split("\t")
        if columns[0].startswith(("C", "R")):
            paths.append(columns[2])
        else:
            paths.append(columns[1])
    return paths


def rename_sources_on_managed_branch(
    root: Path, base: str, branch: str
) -> dict[str, str]:
    """managed branch の rename 先から、復元すべき rename 元を引く。

    根拠: {{work-root}}/oracle/doc/app_spec/misc_spec.md
    """
    lines = managed_branch_name_status_lines(root, base, branch)
    sources: dict[str, str] = {}
    for line in lines:
        columns = line.split("\t")
        if columns[0].startswith("R"):
            sources[columns[2]] = columns[1]
    return sources


def managed_branch_name_status_lines(root: Path, base: str, branch: str) -> list[str]:
    """managed branch 間の name-status diff を Git の出力行として返す。

    根拠: {{work-root}}/oracle/doc/app_spec/misc_spec.md
    """
    return run_git(
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


def is_expected_apply_change(
    root: Path,
    path: str,
    *,
    apply_branch: str | None = None,
    apply_worktree: Path | None = None,
) -> bool:
    """apply branch 上で許可される差分かどうかを判定する。"""
    if Path(path).name == "INDEX.md":
        return True
    if apply_worktree is not None:
        return is_realization_file_path(apply_worktree, apply_worktree / path)
    return is_realization_file_path(
        root,
        root / path,
        branch=apply_branch,
    )


def is_expected_session_change(root: Path, path: str) -> bool:
    """session branch 上で apply 実行中に許可される差分かどうかを判定する。"""
    p = Path(path)
    if p.name == "INDEX.md" or is_root_memo_path(path):
        return True
    return is_oracle_file_path(root, root / path)


def is_root_memo_path(path: str) -> bool:
    """path が root memo またはその配下かどうかを判定する。

    根拠: {{work-root}}/oracle/doc/app_spec/sub_command/apply_join.md
    """
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
    if unexpected.get("session"):
        session_rename_sources = rename_sources_on_managed_branch(root, base, "HEAD")
        for path in unexpected["session"]:
            restore_managed_branch_path(root, base, path, session_rename_sources)
    session_changed = run_git(["status", "--short"], root).stdout.strip()
    if session_changed:
        run_git(["add", "."], root)
        run_git(["commit", "-m", "cmoc apply join force-resolve session changes"], root)
    apply_branch = state.apply.apply_branch
    if apply_branch and unexpected.get("apply"):
        apply_rename_sources = rename_sources_on_managed_branch(
            root, base, apply_branch
        )
        apply_root = worktree_for_branch_optional(root, apply_branch)
        if apply_root is None:
            raise CmocError(
                "apply worktree を特定できません。",
                ["git worktree list を確認してから再実行してください。"],
                f"apply_branch: {apply_branch}",
            )
        for path in unexpected["apply"]:
            restore_managed_branch_path(apply_root, base, path, apply_rename_sources)
        apply_changed = run_git(["status", "--short"], apply_root).stdout.strip()
        if apply_changed:
            run_git(["add", "."], apply_root)
            run_git(
                ["commit", "-m", "cmoc apply join force-resolve apply changes"],
                apply_root,
            )


def restore_managed_branch_path(
    root: Path, commit: str, path: str, rename_sources: dict[str, str]
) -> None:
    """managed branch の差分 path と rename 元を指定 commit へ戻す。

    根拠: {{work-root}}/oracle/doc/app_spec/sub_command/apply_join.md
    """
    restore_path_from_commit(root, commit, path)
    source = rename_sources.get(path)
    if source:
        # {{work-root}}/oracle/doc/app_spec/sub_command/apply_join.md に従い、想定外
        # 差分は force-resolve で戻す。managed branch の分類は rename 先だけを
        # 報告するため、rename 元の復元もこの経路で行う。
        restore_path_from_commit(root, commit, source)


def restore_path_from_commit(root: Path, commit: str, path: str) -> None:
    """path を指定 commit の内容へ戻し、存在しない場合は削除する。"""
    exists = (
        run_git(
            ["cat-file", "-e", f"{commit}:{path}"],
            root,
            check=False,
        ).returncode
        == 0
    )
    if exists:
        run_git(["checkout", commit, "--", path], root)
    else:
        target = root / path
        # {{work-root}}/oracle/doc/app_spec/sub_command/apply_join.md に従い、追加
        # path は force-resolve で戻す。broken symlink は Path.exists() が false
        # でも Git path なので is_symlink() も確認する。
        if target.exists() or target.is_symlink():
            run_git(["rm", "-f", "--", path], root)


def resolve_index_conflicts(root: Path) -> bool:
    """INDEX.md だけの merge conflict を削除 commit で機械解決する。"""
    conflicted = run_git(
        ["diff", "--name-only", "--diff-filter=U"], root
    ).stdout.splitlines()
    if not conflicted:
        return False
    if any(Path(path).name != "INDEX.md" for path in conflicted):
        return False
    for path in conflicted:
        run_git(["rm", "-f", path], root)
    run_git(["commit", "--no-edit"], root)
    return True
