# {{work-root}}/oracle/doc/app_spec/sub_command/session_join.md
import hashlib
import json
from functools import lru_cache
from pathlib import Path
from typing import Callable

from acp.builder.session.join.conflict_resolution import (
    build_session_join_conflict_resolution_parameter,
)
from cmoc_runtime import (
    CmocError,
    CommandResult,
    TerminalResult,
    current_branch,
    head_commit,
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
from commons.runtime_git import literal_pathspec, status_path_statuses
from commons.runtime_primary_report import update_primary_report_fields
from commons.runtime_results import CodexExecCallable

_CodexExec = CodexExecCallable
_GitRun = Callable[..., CommandResult]


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


def _cmoc_session_join_body(
    codex_exec: _CodexExec, git: _GitRun = run_git
) -> TerminalResult:
    """active session branch を session home branch へ merge する。"""
    root = repo_root()
    work = work_root()
    branch = current_branch(work)
    update_primary_report_fields(
        session_branch=branch,
        session_state_before=None,
        session_state_after=None,
    )
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
    update_primary_report_fields(
        home_branch=home,
        session_state_before=state.session.state,
    )
    if not home:
        raise CmocError("session home branch を特定できません。", [], str(path))
    session_head_before_merge = head_commit(work)
    update_primary_report_fields(
        session_branch_head_before_merge=session_head_before_merge,
    )
    start_subcommand_step(3, "session branch を merge", "merge session branch")
    # {{work-root}}/oracle/doc/app_spec/session_state.md:
    # session_home_branch は local branch なので、同名 remote-tracking branch を
    # Git に推測させて別の merge target を作らない。
    run_git(["switch", "--no-guess", home], work)
    home_head_before_merge = head_commit(work)
    update_primary_report_fields(home_branch_head_before_merge=home_head_before_merge)
    merge = git(["merge", "--no-ff", branch], work, check=False)
    if merge.returncode != 0:
        resolve_session_join_conflict(work, codex_exec, git)
    head_after_merge = head_commit(work)
    merge_commit = (
        head_after_merge if head_after_merge != home_head_before_merge else None
    )
    update_primary_report_fields(merge_commit=merge_commit)
    state.session.state = "joined"
    start_subcommand_step(4, "後始末と terminal result を確定", "finish session join")
    write_state(path, state)
    update_primary_report_fields(session_state_after="joined")
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
        delete_result = CommandResult(1, "", f"session branch is not merged: {branch}")
    warnings: list[str] = []
    if delete_result.returncode != 0:
        warnings.append(f"session branch was not deleted: {branch}")
    return TerminalResult(
        details=(
            ("session_id", session_id),
            ("joined_to", home),
            ("deleted_session_branch", delete_result.returncode == 0),
        ),
        warnings=tuple(warnings),
    )


def resolve_session_join_conflict(
    root: Path,
    codex_exec: _CodexExec,
    git: _GitRun = run_git,
) -> None:
    """session join の merge conflict を Codex CLI へ依頼して解消する。"""
    start_subcommand_step("3/4, 1/5", "conflict 対象を列挙", "enumerate conflicts")
    conflicted_paths = _unmerged_paths(root, git)
    update_primary_report_fields(
        conflict_paths=[str(_absolute_path(path)) for path in conflicted_paths],
        conflict_resolution_status="not_started",
    )
    if not conflicted_paths:
        raise CmocError(
            "merge に失敗しましたが conflict 対象ファイルを特定できません。",
            ["git status を確認し、手動解決後に再実行してください。"],
            git(["status", "--short"], root).stdout,
        )
    before_codex = _changed_path_snapshot(root, git)
    before_conflict_contents = _conflict_file_contents(conflicted_paths)
    start_subcommand_step("3/4, 2/5", "conflict marker 解消を依頼", "resolve conflicts")
    update_primary_report_fields(conflict_resolution_status="started")
    codex_exec(
        build_session_join_conflict_resolution_parameter(conflicted_paths),
        # {{work-root}}/oracle/doc/app_spec/codex_exec_rule.md:
        # Codex がこの worktree を編集しても config/log は repo-root に残す。
        root=repo_root(root),
        purpose="session join conflict resolution",
    )
    update_primary_report_fields(conflict_resolution_status="completed")
    _reject_non_conflict_changes(root, git, before_codex, conflicted_paths)
    _reject_conflict_context_changes(before_conflict_contents)
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
        git(["add", "--", literal_pathspec(str(path.relative_to(root)))], root)
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


def _unmerged_paths(root: Path, git: _GitRun) -> list[Path]:
    """Gitのunmerged pathをNUL framingで安全に読み取る。"""
    # {{work-root}}/oracle/doc/app_spec/sub_command/session_join.md:
    # Git path には改行が含まれ得るため、conflict target は NUL framing を使う。
    fields = git(["diff", "--name-only", "-z", "--diff-filter=U"], root).stdout.split(
        "\0"
    )
    return [root / field for field in fields if field]


def _reject_non_conflict_changes(
    root: Path,
    git: _GitRun,
    before_codex: dict[Path, tuple[str, tuple[str, int, int, str | None] | None]],
    conflicted_paths: list[Path],
) -> None:
    """Codex 呼び出し後に許可範囲外の差分が変化していないか検査する。"""
    # {{work-root}}/oracle/doc/app_spec/sub_command/session_join.md の
    # 「oracle file 規定と conflict 解消の優先順位」:
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
    # conflict 対象でも file type と mode は marker 解消の対象外なので、変更を許可しない。
    for path in sorted(allowed, key=str):
        before_entry = before_codex.get(path)
        after_entry = after_codex.get(path)
        if before_entry is None or after_entry is None:
            continue
        before_fingerprint = before_entry[1]
        after_fingerprint = after_entry[1]
        if before_fingerprint is None or after_fingerprint is None:
            continue
        if before_fingerprint[:2] != after_fingerprint[:2]:
            changed.append(path)
    changed.sort(key=str)
    if changed:
        raise CmocError(
            "conflict 解消以外の差分が残っています。",
            ["差分を確認し、不要な変更を戻してから手動で merge を完了してください。"],
            "\n".join(str(path) for path in changed),
        )


def _conflict_file_contents(paths: list[Path]) -> dict[Path, bytes]:
    """conflict marker 外の内容を比較するため、対象 file の事前内容を保存する。"""
    contents: dict[Path, bytes] = {}
    for path in paths:
        absolute = _absolute_path(path)
        content = _read_regular_file(absolute)
        if content is not None and _conflict_context_segments(content) is not None:
            contents[absolute] = content
    return contents


def _reject_conflict_context_changes(before_contents: dict[Path, bytes]) -> None:
    """conflict marker の外側へ agent が差分を加えた場合は merge を拒否する。"""
    # {{work-root}}/oracle/doc/app_spec/sub_command/session_join.md の
    # 「oracle file 規定と conflict 解消の優先順位」:
    # conflict marker の置換範囲外の仕様変更、実装改善、整形を merge commit に持ち込まない。
    changed: list[Path] = []
    for path, before in before_contents.items():
        after = _read_regular_file(path)
        if after is None:
            changed.append(path)
            continue
        if not _preserves_conflict_context(before, after):
            changed.append(path)
    if changed:
        raise CmocError(
            "conflict 対象 file の不要な差分が残っています。",
            [
                "差分を確認し、marker 外の変更を戻してから手動で merge を完了してください。"
            ],
            "\n".join(str(path) for path in changed),
        )


def _read_regular_file(path: Path) -> bytes | None:
    """symlink や directory をたどらず、通常 file の bytes だけを読む。"""
    try:
        if path.is_symlink() or not path.is_file():
            return None
        return path.read_bytes()
    except OSError:
        return None


def _conflict_context_segments(content: bytes) -> list[tuple[bytes, ...]] | None:
    """conflict block を除いた、変更禁止の line segment を返す。"""
    lines = tuple(content.splitlines(keepends=True))
    ranges: list[tuple[int, int]] = []
    opening: int | None = None
    for index, line in enumerate(lines):
        if opening is None:
            if line.startswith(b"<<<<<<<"):
                opening = index
        elif line.startswith(b">>>>>>>"):
            ranges.append((opening, index + 1))
            opening = None
    if opening is not None:
        ranges.append((opening, len(lines)))
    if not ranges:
        return None

    segments: list[tuple[bytes, ...]] = []
    cursor = 0
    for start, end in ranges:
        segments.append(lines[cursor:start])
        cursor = end
    segments.append(lines[cursor:])
    return segments


def _preserves_conflict_context(before: bytes, after: bytes) -> bool:
    """解消後も conflict block 外の line segment が順序・内容を保つか判定する。"""
    segments = _conflict_context_segments(before)
    if segments is None:
        # binary conflict や marker を持たない conflict は、marker 外の境界を決められない。
        return True
    after_lines = tuple(after.splitlines(keepends=True))

    @lru_cache(maxsize=None)
    def matches(segment_index: int, position: int) -> bool:
        """指定位置から残りの conflict context segment を順序どおり探す。"""
        if segment_index == len(segments):
            # 最後の conflict block の置換本文は任意の line を含み得る。
            return True
        segment = segments[segment_index]
        if not segment:
            return matches(segment_index + 1, position)
        if segment_index == 0:
            end = position + len(segment)
            return after_lines[position:end] == segment and matches(
                segment_index + 1, end
            )

        for start in range(position, len(after_lines) - len(segment) + 1):
            end = start + len(segment)
            if after_lines[start:end] != segment:
                continue
            if segment_index == len(segments) - 1 and end != len(after_lines):
                continue
            if matches(segment_index + 1, end):
                return True
        return False

    return matches(0, 0)


def _changed_path_snapshot(
    root: Path,
    git: _GitRun,
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
