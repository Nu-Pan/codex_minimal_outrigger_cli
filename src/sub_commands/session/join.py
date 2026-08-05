# {{work-root}}/oracle/doc/app_spec/sub_command/session_join.md
import hashlib
import json
from pathlib import Path
from typing import Callable

import typer

from acp.builder.session.join.conflict_resolution import (
    build_session_join_conflict_resolution_parameter,
)
from cmoc_runtime import (
    CmocError,
    CommandResult,
    current_branch,
    load_state_for_branch,
    repo_root,
    require_clean_worktree,
    run_cli_subcommand,
    run_codex_exec,
    run_git,
    start_subcommand_step,
    work_root,
    write_state,
)
from commons.indexing import enable_indexing_preflight
from commons.runtime_git import status_path_statuses
from commons.runtime_results import CodexExecCallable

CodexExec = CodexExecCallable
GitRun = Callable[..., CommandResult]


def cmoc_session_join_impl() -> None:
    """CLI runtime を通して session join を実行する。"""
    enable_indexing_preflight()
    run_cli_subcommand(
        _cmoc_session_join_body,
        run_codex_exec,
        run_git,
        command_name="session join",
        command_argv=["cmoc", "session", "join"],
        total_steps=4,
        use_work_root_runtime=True,
    )


def _cmoc_session_join_body(codex_exec: CodexExec, git: GitRun = run_git) -> None:
    """active session branch を session home branch へ merge する。"""
    root = repo_root()
    work = work_root()
    branch = current_branch(work)
    start_subcommand_step(2, "事前条件を確認", "validate preconditions")
    session_id, path, state = load_state_for_branch(root, branch)
    if not branch.startswith("cmoc/session/"):
        raise CmocError(
            "session join は session branch 上で実行してください。", [], branch
        )
    if state.session.state != "active" or state.run.state != "ready":
        raise CmocError(
            "session join の事前条件を満たしていません。",
            ["session.state と run.state を確認してください。"],
            json.dumps(state.to_dict(), ensure_ascii=False, indent=2),
        )
    require_clean_worktree(work)
    home = state.session.session_home_branch
    if not home:
        raise CmocError("session home branch を特定できません。", [], str(path))
    start_subcommand_step(3, "session branch を merge", "merge session branch")
    try:
        run_git(["switch", home], work)
        merge = git(["merge", "--no-ff", branch], work, check=False)
        if merge.returncode != 0:
            resolve_session_join_conflict(work, codex_exec, git)
        state.session.state = "joined"
        start_subcommand_step(4, "後始末と結果を表示", "finish session join")
        write_state(path, state)
        # {{work-root}}/oracle/doc/app_spec/sub_command/session_join.md:
        # 削除するのは local session branch 自体が merge target HEAD から到達可能な場合だけ。
        # remote-tracking ref で安全性を証明してはならない。
        reachable = (
            git(
                ["merge-base", "--is-ancestor", branch, "HEAD"],
                work,
                check=False,
            ).returncode
            == 0
        )
        if reachable:
            delete_result = git(["branch", "-d", branch], work, check=False)
        else:
            delete_result = CommandResult(
                1, "", f"session branch is not merged: {branch}"
            )
    except BaseException as exc:
        # {{work-root}}/oracle/doc/app_spec/sub_command/session_join.md:
        # precondition 後の failure では手動の git resolution が必要になり得るため、
        # error report は既定の stdout path ではなく stderr に出す。
        setattr(exc, "cmoc_error_to_stderr", True)
        raise
    warnings: list[str] = []
    if delete_result.returncode != 0:
        warnings.append(f"session branch was not deleted: {branch}")
    warning_lines = (
        [f"  - {warning}" for warning in warnings] if warnings else ["  - none"]
    )
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
    start_subcommand_step("3/4, 1/5", "conflict 対象を列挙", "enumerate conflicts")
    conflicted_paths = _unmerged_paths(root, git)
    if not conflicted_paths:
        raise CmocError(
            "merge に失敗しましたが conflict 対象ファイルを特定できません。",
            ["git status を確認し、手動解決後に再実行してください。"],
            git(["status", "--short"], root).stdout,
        )
    before_codex = _changed_path_snapshot(root, git)
    start_subcommand_step("3/4, 2/5", "conflict marker 解消を依頼", "resolve conflicts")
    codex_exec(
        build_session_join_conflict_resolution_parameter(conflicted_paths),
        # {{work-root}}/oracle/doc/app_spec/codex_exec_rule.md:
        # Codex がこの worktree を編集しても config/log は repo-root に残す。
        root=repo_root(root),
        purpose="session join conflict resolution",
    )
    _reject_non_conflict_changes(root, git, before_codex, conflicted_paths)
    start_subcommand_step(
        "3/4, 3/5", "conflict marker の残存を確認", "check conflict markers"
    )
    remaining_markers = [
        path
        for path in conflicted_paths
        if path.exists() and _has_conflict_marker_block(path.read_text(errors="ignore"))
    ]
    if remaining_markers:
        raise CmocError(
            "conflict marker が残っています。",
            ["conflict marker を手動で解消してから git commit してください。"],
            "\n".join(str(_absolute_path(path)) for path in remaining_markers),
        )
    start_subcommand_step("3/4, 4/5", "conflict 対象を stage", "stage conflicts")
    for path in conflicted_paths:
        git(["add", "--", str(path.relative_to(root))], root)
    unmerged_paths = _unmerged_paths(root, git)
    start_subcommand_step(
        "3/4, 5/5", "unmerged path と merge 完了を確認", "finish conflict merge"
    )
    unmerged = "\n".join(str(_absolute_path(path)) for path in unmerged_paths)
    if unmerged:
        raise CmocError(
            "unmerged path が残っています。",
            ["git status を確認し、手動で merge を完了してください。"],
            unmerged,
        )
    git(["commit", "--no-edit"], root)


def _unmerged_paths(root: Path, git: GitRun) -> list[Path]:
    """Gitのunmerged pathをNUL framingで安全に読み取る。"""
    # {{work-root}}/oracle/doc/app_spec/sub_command/session_join.md:
    # Git path には改行が含まれ得るため、conflict target は NUL framing を使う。
    fields = git(["diff", "--name-only", "-z", "--diff-filter=U"], root).stdout.split(
        "\0"
    )
    return [root / field for field in fields if field]


def _reject_non_conflict_changes(
    root: Path,
    git: GitRun,
    before_codex: dict[Path, tuple[str, tuple[str, int, int, str | None] | None]],
    conflicted_paths: list[Path],
) -> None:
    """Codex 呼び出し後に conflict 対象外の差分が変化していないか検査する。"""
    # {{work-root}}/oracle/src/oracle/prompt_builder/parts/conflict_resolution_standard.py:
    # conflict marker 解消に不要な別 file の変更を merge commit へ持ち込まない。
    allowed = {_absolute_path(path) for path in conflicted_paths}
    after_codex = _changed_path_snapshot(root, git)
    changed = sorted(
        (
            path
            for path in before_codex.keys() | after_codex.keys()
            if path not in allowed and before_codex.get(path) != after_codex.get(path)
        ),
        key=str,
    )
    if changed:
        raise CmocError(
            "conflict 解消以外の差分が残っています。",
            ["差分を確認し、不要な変更を戻してから手動で merge を完了してください。"],
            "\n".join(str(path) for path in changed),
        )


def _changed_path_snapshot(
    root: Path,
    git: GitRun,
) -> dict[Path, tuple[str, tuple[str, int, int, str | None] | None]]:
    """Codex 呼び出し前後の比較用に Git の変更 path と内容を記録する。"""
    snapshot: dict[Path, tuple[str, tuple[str, int, int, str | None] | None]] = {}
    for status, path in status_path_statuses(
        root,
        untracked_all=True,
        include_rename_sources=True,
        git=git,
    ):
        absolute = _absolute_path(path)
        snapshot[absolute] = (status, _path_fingerprint(absolute))
    return snapshot


def _absolute_path(path: Path) -> Path:
    """相対Git pathを現在のworktree基準の絶対pathへ変換する。"""
    return path if path.is_absolute() else path.absolute()


def _path_fingerprint(path: Path) -> tuple[str, int, int, str | None] | None:
    """変更 path の種類と内容を比較可能な fingerprint へ変換する。"""
    try:
        stat = path.lstat()
    except FileNotFoundError:
        return None
    if path.is_symlink():
        link_digest = hashlib.sha256(path.readlink().as_posix().encode()).hexdigest()
        return ("symlink", stat.st_mode, stat.st_size, link_digest)
    if path.is_dir():
        return ("dir", stat.st_mode, stat.st_size, None)
    file_digest: str | None = None
    if path.is_file():
        file_digest = hashlib.sha256(path.read_bytes()).hexdigest()
    return ("file", stat.st_mode, stat.st_size, file_digest)


def _has_conflict_marker_block(text: str) -> bool:
    """text内に未解決conflict marker blockが残っているか判定する。"""
    state = 0
    for line in text.splitlines():
        # {{work-root}}/oracle/doc/app_spec/sub_command/session_join.md:
        # 残った conflict fragment はすべて拒否する。ただし bare `=======` は opening
        # marker が active でない限り有効な Markdown として扱う。
        if line.startswith("<<<<<<<"):
            state = 1
        elif line.startswith(("|||||||", ">>>>>>>")):
            return True
        # Git は conflict-marker-size が既定の 7 文字を超えることを許可する。
        elif state == 1 and len(line) >= 7 and set(line) == {"="}:
            state = 2
    return state != 0
