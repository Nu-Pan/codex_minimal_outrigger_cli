import hashlib
import json
from dataclasses import replace
from pathlib import Path
from typing import Callable

import typer

from acp.builder.session.join.conflict_resolution import (
    build_session_join_conflict_resolution_parameter,
)
from commons.indexing import enable_indexing_preflight
from commons.runtime_git import status_path_statuses
from cmoc_runtime import (
    CmocError,
    CommandResult,
    current_branch,
    ensure_cmoc_ignored,
    load_state_for_branch,
    repo_root,
    require_clean_worktree,
    run_cli_subcommand,
    run_codex_exec,
    run_git,
    work_root,
    write_state,
)


CodexExec = Callable[..., object]
GitRun = Callable[..., object]


def cmoc_session_join_impl() -> None:
    """CLI runtime を通して session join を実行する。"""
    enable_indexing_preflight()
    run_cli_subcommand(
        _cmoc_session_join_body,
        run_codex_exec,
        run_git,
        command_name="session join",
        command_argv=["cmoc", "session", "join"],
        use_work_root_runtime=True,
    )


def _cmoc_session_join_body(codex_exec: CodexExec, git: GitRun = run_git) -> None:
    """active session branch を session home branch へ merge する。"""
    root = repo_root()
    work = work_root()
    branch = current_branch(work)
    session_id, path, state = load_state_for_branch(root, branch)
    if not branch.startswith("cmoc/session/"):
        raise CmocError("session join は session branch 上で実行してください。", [], branch)
    if state.session.state != "active" or state.apply.state != "ready":
        raise CmocError(
            "session join の事前条件を満たしていません。",
            ["session.state と apply.state を確認してください。"],
            json.dumps(state.to_dict(), ensure_ascii=False, indent=2),
        )
    require_clean_worktree(work)
    ensure_cmoc_ignored(work)
    home = state.session.session_home_branch
    if not home:
        raise CmocError("session home branch を特定できません。", [], str(path))
    try:
        run_git(["switch", home], work)
        merge = git(["merge", "--no-ff", branch], work, check=False)
        if merge.returncode != 0:
            resolve_session_join_conflict(work, codex_exec, git)
        state.session.state = "joined"
        write_state(path, state)
        # <work-root>/oracle/doc/app_spec/sub_command/session_join.md:
        # delete only when the local session branch itself is reachable from
        # the merge target HEAD; remote-tracking refs must not prove safety.
        reachable = git(
            ["merge-base", "--is-ancestor", branch, "HEAD"],
            work,
            check=False,
        ).returncode == 0
        if reachable:
            delete_result = git(["branch", "-d", branch], work, check=False)
        else:
            delete_result = CommandResult(
                1, "", f"session branch is not merged: {branch}"
            )
    except BaseException as exc:
        # <work-root>/oracle/doc/app_spec/sub_command/session_join.md:
        # post-precondition failures can require manual git resolution, so their
        # error report must go to stderr instead of the default stdout path.
        setattr(exc, "cmoc_error_to_stderr", True)
        raise
    warnings: list[str] = []
    if delete_result.returncode != 0:
        warnings.append(f"session branch was not deleted: {branch}")
    warning_lines = [f"  - {warning}" for warning in warnings] if warnings else ["  - none"]
    typer.echo(
        "\n".join(
            [
                "# cmoc session join",
                f"- session_id: `{session_id}`",
                f"- joined_to: `{home}`",
                f"- deleted_session_branch: `{delete_result.returncode == 0}`",
                "- warnings:",
                *warning_lines,
            ]
        )
    )

def resolve_session_join_conflict(
    root: Path,
    codex_exec: CodexExec,
    git: GitRun = run_git,
) -> None:
    """session join の merge conflict を Codex CLI へ依頼して解消する。"""
    conflicted_paths = _unmerged_paths(root, git)
    if not conflicted_paths:
        raise CmocError(
            "merge に失敗しましたが conflict 対象ファイルを特定できません。",
            ["git status を確認し、手動解決後に再実行してください。"],
            git(["status", "--short"], root).stdout,
        )
    before_codex = _changed_path_snapshot(root, git)
    codex_exec(
        replace(
            build_session_join_conflict_resolution_parameter(conflicted_paths),
            cwd=root,
        ),
        root=root,
        purpose="session join conflict resolution",
        # <work-root>/oracle/doc/app_spec/sub_command/session_join.md
        # oracle conflict の例外は prompt だけでは sandbox に効かないため、
        # conflict 対象だけを profile の writable root にも反映する。
        extra_writable_paths=conflicted_paths,
        allow_oracle_conflict_writes=True,
    )
    _reject_non_conflict_changes(root, git, before_codex, conflicted_paths)
    remaining_markers = [
        path
        for path in conflicted_paths
        if path.exists() and _has_conflict_marker_block(path.read_text(errors="ignore"))
    ]
    if remaining_markers:
        raise CmocError(
            "conflict marker が残っています。",
            ["conflict marker を手動で解消してから git commit してください。"],
            "\n".join(str(path) for path in remaining_markers),
        )
    for path in conflicted_paths:
        git(["add", "--", str(path.relative_to(root))], root)
    unmerged_paths = _unmerged_paths(root, git)
    unmerged = "\n".join(str(path.relative_to(root)) for path in unmerged_paths)
    if unmerged:
        raise CmocError(
            "unmerged path が残っています。",
            ["git status を確認し、手動で merge を完了してください。"],
            unmerged,
        )
    git(["commit", "--no-edit"], root)


def _unmerged_paths(root: Path, git: GitRun) -> list[Path]:
    # <work-root>/oracle/doc/app_spec/sub_command/session_join.md:
    # Git paths can contain newlines, so conflict targets must use NUL framing.
    fields = git(["diff", "--name-only", "-z", "--diff-filter=U"], root).stdout.split("\0")
    return [root / field for field in fields if field]


def _reject_non_conflict_changes(
    root: Path,
    git: GitRun,
    before_codex: dict[Path, tuple[str, tuple[str, int, int, str | None] | None]],
    conflicted_paths: list[Path],
) -> None:
    # <work-root>/oracle/src/oracle/acp_builder/session/join/conflict_resolution.py:
    # REPO_WRITE is needed for oracle conflicts, so this command enforces the
    # narrower "conflict targets only" boundary after the agent returns.
    allowed = {_absolute_path(path) for path in conflicted_paths}
    after_codex = _changed_path_snapshot(root, git)
    changed = [
        path
        for path in before_codex.keys() | after_codex.keys()
        if _absolute_path(path) not in allowed
        and before_codex.get(path) != after_codex.get(path)
    ]
    if changed:
        raise CmocError(
            "conflict 解消以外の差分が残っています。",
            ["差分を確認し、不要な変更を戻してから手動で merge を完了してください。"],
            "\n".join(str(path.relative_to(root)) for path in changed),
        )


def _changed_path_snapshot(
    root: Path, git: GitRun
) -> dict[Path, tuple[str, tuple[str, int, int, str | None] | None]]:
    snapshot: dict[Path, tuple[str, tuple[str, int, int, str | None] | None]] = {}
    for status, path in status_path_statuses(root, untracked_all=True, git=git):
        absolute = _absolute_path(path)
        snapshot[absolute] = (status, _path_fingerprint(absolute))
    return snapshot


def _absolute_path(path: Path) -> Path:
    return path if path.is_absolute() else path.absolute()


def _path_fingerprint(path: Path) -> tuple[str, int, int, str | None] | None:
    try:
        stat = path.lstat()
    except FileNotFoundError:
        return None
    if path.is_symlink():
        digest = hashlib.sha256(path.readlink().as_posix().encode()).hexdigest()
        return ("symlink", stat.st_mode, stat.st_size, digest)
    if path.is_dir():
        return ("dir", stat.st_mode, stat.st_size, None)
    digest: str | None = None
    if path.is_file():
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
    return ("file", stat.st_mode, stat.st_size, digest)


def _has_conflict_marker_block(text: str) -> bool:
    state = 0
    for line in text.splitlines():
        if state == 0 and line.startswith("<<<<<<<"):
            state = 1
        # <work-root>/oracle/doc/app_spec/sub_command/session_join.md:
        # Git allows conflict-marker-size to exceed the default seven chars.
        elif state == 1 and len(line) >= 7 and set(line) == {"="}:
            state = 2
        elif state == 2 and line.startswith(">>>>>>>"):
            return True
    return False
