"""`cmoc session join` の本体処理。"""

import subprocess
import sys
from pathlib import Path

from commons.codex import run_codex_exec
from commons.command_runner import run_command
from commons.errors import CmocError
from commons.repo import (
    assert_no_uncommitted_changes,
    assert_no_uncommitted_changes_outside_cmoc,
    current_branch,
    ensure_cmoc_ignored_and_committed,
    git_name_only_paths,
    git_status_paths,
    is_session_branch,
    read_session_state,
    resolve_session_home_branch,
    run_git,
    session_id_from_branch,
    session_state_root,
    write_session_state,
)
from commons.timing import StepTimer, start_step

_MANUAL_RESOLUTION_MESSAGE: str = (
    "手動解消が必要です。cmoc は repository 状態をロールバックしていません。"
)

_ProtectedConflictSnapshot = dict[str, tuple[str, bytes | None, str]]


def cmoc_session_join_impl(repo_root: Path | None = None) -> None:
    """現在の session branch を記録済み home branch へ merge する。"""
    # 直接呼び出し時は共通 runner で repo root 解決とエラー整形を行う。
    if repo_root is None:
        run_command(cmoc_session_join_impl, command_path="cmoc session join")
        return

    timer = StepTimer("session join")
    manual_resolution_required = False
    try:
        start_step(timer, 1, 5, "session 状態検証")
        session_branch = _current_session_branch(repo_root)
        session_id = session_id_from_branch(session_branch)
        state_root = session_state_root(repo_root)
        state = read_session_state(state_root, session_id)
        _validate_joinable_state(state, session_branch)
        home_branch = resolve_session_home_branch(
            repo_root,
            state,
            session_branch,
        )
        _assert_local_branch_exists(repo_root, home_branch)
        assert_no_uncommitted_changes_outside_cmoc(repo_root)

        start_step(timer, 2, 5, ".cmoc ignore 確認")
        manual_resolution_required = True
        ensure_cmoc_ignored_and_committed(repo_root)
        assert_no_uncommitted_changes(repo_root)
        _record_session_home_branch(state_root, session_id, state, home_branch)

        start_step(timer, 3, 5, "session home branch 切替")
        run_git(repo_root, ["switch", home_branch])

        start_step(timer, 4, 5, "session branch merge")
        ensure_cmoc_ignored_and_committed(repo_root)
        assert_no_uncommitted_changes(repo_root)
        result = run_git(
            repo_root,
            ["merge", "--no-ff", session_branch],
            check=False,
        )
        if result.returncode != 0:
            if _unmerged_paths(repo_root):
                _resolve_conflicts(repo_root)
            else:
                _raise_unexpected_merge_failure(result)

        start_step(timer, 5, 5, "session join 記録")
        _mark_session_joined(state_root, session_id, state)
        _delete_branch_if_safe(repo_root, session_branch)
        print(f"joined session branch: {session_branch}")
        print(f"session home branch: {home_branch}")
        timer.report()
    except Exception:
        # 副作用段階に入った後は rollback せず、手動解決を案内する。
        if manual_resolution_required:
            print(_MANUAL_RESOLUTION_MESSAGE, file=sys.stderr)
        raise


def _current_session_branch(repo_root: Path) -> str:
    """現在 checkout している session branch 名を返す。"""
    branch_name = current_branch(repo_root)
    if not is_session_branch(branch_name):
        raise CmocError(
            "`cmoc session join` は session branch 上で実行してください。",
            [
                "`cmoc session fork` で作成した branch へ移動してから再実行してください。",
                "通常 branch 同士の merge は `git merge` を直接実行してください。",
            ],
            f"現在の branch: {branch_name or '(detached HEAD)'}",
        )
    return branch_name


def _validate_joinable_state(
    state: dict[str, object],
    session_branch: str,
) -> None:
    """session join の state 前提条件を検証する。"""
    session = state.get("session")
    apply = state.get("apply")
    if not isinstance(session, dict) or not isinstance(apply, dict):
        raise CmocError(
            "session state ファイルの形式が不正です。",
            [
                "state JSON の session/apply セクションを確認して復旧してください。",
                "復旧できない場合は、現在の session を abandon して新しい session を開始してください。",
            ],
            f"現在の branch: {session_branch}",
        )
    if session.get("state") != "active":
        raise CmocError(
            "active な session ではありません。",
            [
                "対象 session の state を確認してください。",
                "既に join または abandon 済みの場合は、追加の join は実行できません。",
            ],
            f"session.state: {session.get('state')}",
        )
    if apply.get("state") != "ready":
        raise CmocError(
            "apply run が完了または整理されていません。",
            [
                "`cmoc apply join` または `cmoc apply abandon` を完了してから再実行してください。",
                "session state の apply.state を確認してください。",
            ],
            f"apply.state: {apply.get('state')}",
        )


def _record_session_home_branch(
    repo_root: Path,
    session_id: str,
    state: dict[str, object],
    home_branch: str,
) -> None:
    """復元済み session home branch を state に保存する。"""
    session = state.get("session")
    if not isinstance(session, dict):
        raise CmocError(
            "session state ファイルの形式が不正です。",
            [
                "state JSON の session セクションを確認して復旧してください。",
                "復旧できない場合は、現在の session を使わず新しい session を開始してください。",
            ],
        )
    if session.get("session_home_branch") == home_branch:
        return
    session["session_home_branch"] = home_branch
    write_session_state(repo_root, session_id, state)


def _assert_local_branch_exists(repo_root: Path, branch_name: str) -> None:
    """記録済み home branch が local branch として存在することを確認する。"""
    result = run_git(
        repo_root,
        ["show-ref", "--verify", f"refs/heads/{branch_name}"],
        check=False,
    )
    if result.returncode != 0:
        raise CmocError(
            "session home branch が見つかりませんでした。",
            [
                "session state に記録された branch 名を確認してください。",
                "削除済みの場合は、手動で復元または merge 先を判断してください。",
            ],
            f"session home branch: {branch_name}",
        )


def _mark_session_joined(
    repo_root: Path,
    session_id: str,
    state: dict[str, object],
) -> None:
    """session state を joined として保存する。"""
    session = state.get("session")
    if not isinstance(session, dict):
        raise CmocError(
            "session state ファイルの形式が不正です。",
            [
                "state JSON の session セクションを確認して復旧してください。",
                "復旧できない場合は、現在の session を使わず新しい session を開始してください。",
            ],
        )
    session["state"] = "joined"
    write_session_state(repo_root, session_id, state)


def _resolve_conflicts(repo_root: Path) -> None:
    """Codex CLI へ conflict marker 解消を依頼し、merge commit を作成する。"""
    # merge 直後の conflict 対象を固定し、後続確認でも同じ一覧を使う。
    unmerged = _unmerged_paths(repo_root)
    if not unmerged:
        raise CmocError(
            "git merge が失敗しましたが、unmerged path がありません。",
            [
                "git status を手動で確認してください。",
                "merge 状態を解消してから cmoc を再実行してください。",
            ],
        )
    _assert_no_forbidden_conflict_paths(unmerged)
    merge_state = _merge_state_snapshot(repo_root)
    protected_snapshot = _protected_conflict_snapshot(repo_root, unmerged)

    # conflict 解消用 Codex 呼び出しは INDEX メンテナンス例外として実行する。
    run_codex_exec(
        repo_root,
        _conflict_prompt(repo_root, unmerged),
        purpose="session join conflict 解消",
        read_only=False,
        expect_json=False,
        skip_index_maintenance=True,
        allowed_uncommitted_oracle_paths=_oracle_conflict_paths(unmerged),
    )

    _assert_merge_state_unchanged(repo_root, merge_state)

    # conflict 対象外の差分は Codex 呼び出し前と同一でなければならない。
    _assert_protected_conflict_snapshot_unchanged(
        repo_root,
        unmerged,
        protected_snapshot,
    )

    # conflict 対象に marker が残っていないことを add 前に検出する。
    marker_files = _files_with_conflict_markers(repo_root, unmerged)
    if marker_files:
        raise CmocError(
            "Codex CLI による解消後も conflict marker が残っています。",
            [
                "残っている conflict marker を手動で解消してください。",
                "merge commit を手動で作成してください。",
            ],
            "\n".join(marker_files),
        )

    # cmoc の責任で conflict 対象を add し、unmerged path が残らないことを確認する。
    for path in unmerged:
        run_git(repo_root, ["add", "--", path])
    if _unmerged_paths(repo_root):
        raise CmocError(
            "conflict 解消後も unmerged path が残っています。",
            [
                "git status を手動で確認してください。",
                "merge を手動で解消して commit してください。",
            ],
            "\n".join(_unmerged_paths(repo_root)),
        )

    # marker 確認と git add が完了してから merge commit を作成する。
    run_git(repo_root, ["commit", "--no-edit"])


def _merge_state_snapshot(repo_root: Path) -> dict[str, str]:
    """Codex 呼び出し前の merge state を保存する。"""
    return {
        "branch": current_branch(repo_root),
        "head": _rev_parse(repo_root, "HEAD"),
        "merge_head": _rev_parse(repo_root, "MERGE_HEAD"),
        "unmerged_index": _unmerged_index_snapshot(repo_root),
    }


def _assert_merge_state_unchanged(
    repo_root: Path,
    before: dict[str, str],
) -> None:
    """Codex が merge state を完了・中止・移動していないことを確認する。"""
    after = _merge_state_snapshot(repo_root)
    if after == before and after["merge_head"]:
        return

    details = []
    for key in ("branch", "head", "merge_head", "unmerged_index"):
        if after.get(key) == before.get(key):
            continue
        if key == "unmerged_index":
            details.append("unmerged_index: changed")
            continue
        details.append(
            f"{key}: {before.get(key) or '(none)'}"
            f" -> {after.get(key) or '(none)'}"
        )
    if not after["merge_head"] and "merge_head" not in {
        detail.split(":", 1)[0] for detail in details
    }:
        details.append("merge_head: merge state is missing")

    raise CmocError(
        "Codex CLI が session join の merge state を変更しました。",
        [
            "merge commit は作成していません。",
            "git status と git log を確認し、merge を手動で復旧または解消してください。",
        ],
        "\n".join(details),
    )


def _rev_parse(repo_root: Path, revision: str) -> str:
    """存在する revision を full hash に解決し、存在しない場合は空文字を返す。"""
    result = run_git(
        repo_root,
        ["rev-parse", "-q", "--verify", revision],
        check=False,
    )
    if result.returncode != 0:
        return ""
    return result.stdout.strip()


def _unmerged_index_snapshot(repo_root: Path) -> str:
    """unmerged index stage 情報を Codex の git add 検出用に保存する。"""
    result = run_git(repo_root, ["ls-files", "-u", "-z"])
    return result.stdout


def _raise_unexpected_merge_failure(
    result: subprocess.CompletedProcess[str],
) -> None:
    """conflict ではない merge 失敗をユーザー向けエラーにする。"""
    stdout = getattr(result, "stdout", "")
    stderr = getattr(result, "stderr", "")
    detail = "\n".join(
        [
            f"git merge return code: {result.returncode}",
            "STDOUT:",
            stdout.strip(),
            "STDERR:",
            stderr.strip(),
        ]
    ).strip()
    raise CmocError(
        "git merge が失敗しましたが、merge conflict は検出されませんでした。",
        [
            "git status と git merge の出力を確認し、手動で原因を解消してください。",
            "リポジトリ状態を整理してから `cmoc session join` を再実行してください。",
        ],
        detail,
    )


def _delete_branch_if_safe(repo_root: Path, branch_name: str) -> None:
    """git に安全判定を任せて session branch 削除を試みる。"""
    # `git branch -d` が拒否した場合は warning に留める。
    result = run_git(repo_root, ["branch", "-d", branch_name], check=False)
    if result.returncode != 0:
        print(f"warning: session branch was not deleted: {branch_name}")


def _files_with_conflict_markers(
    repo_root: Path,
    paths: list[str] | None = None,
) -> list[str]:
    """conflict marker が残るファイルを列挙する。"""
    matches: list[str] = []
    if paths is None:
        result = run_git(repo_root, ["ls-files", "-z"])
        target_paths = {
            relative
            for relative in result.stdout.split("\0")
            if relative
        }
    else:
        target_paths = {relative for relative in paths if relative}

    for relative in sorted(target_paths):
        path = repo_root / relative
        if not path.exists() or not path.is_file():
            continue
        for line in path.read_text(
            encoding="utf-8",
            errors="ignore",
        ).splitlines():
            if (
                line.startswith("<<<<<<<")
                or line.startswith("|||||||")
                or line == "======="
                or line.startswith(">>>>>>>")
            ):
                matches.append(relative)
                break
    return matches


def _assert_no_forbidden_conflict_paths(unmerged: list[str]) -> None:
    """Codex に渡せない禁止領域が conflict 対象に含まれないことを確認する。"""
    forbidden = [
        path
        for path in unmerged
        if _is_forbidden_conflict_path(path)
    ]
    if forbidden:
        raise CmocError(
            "Codex CLI に依頼できない禁止領域で conflict が発生しました。",
            [
                "表示された path を手動で確認してください。",
                "禁止領域の扱いを判断したうえで、merge を手動で解消してください。",
            ],
            "\n".join(forbidden),
        )


def _is_forbidden_conflict_path(path: str) -> bool:
    """session join の自動 conflict 解消で編集禁止の path か判定する。"""
    return (
        path == ".agents"
        or path.startswith(".agents/")
        or path == "memo"
        or path.startswith("memo/")
    )


def _oracle_conflict_paths(unmerged: list[str]) -> list[str]:
    """conflict marker 解消だけを許可する oracle path を抽出する。"""
    return [
        path
        for path in unmerged
        if path == "oracles" or path.startswith("oracles/")
    ]


def _protected_conflict_snapshot(
    repo_root: Path,
    unmerged: list[str],
) -> _ProtectedConflictSnapshot:
    """conflict 対象外の未コミット状態と作業ツリー内容を保存する。"""
    unmerged_set = set(unmerged)
    snapshot: _ProtectedConflictSnapshot = {}
    for status, path in _porcelain_status_entries(repo_root):
        if path in unmerged_set:
            continue
        snapshot[path] = (
            status,
            _read_snapshot_bytes(repo_root, path),
            _index_snapshot_entry(repo_root, path),
        )
    return snapshot


def _assert_protected_conflict_snapshot_unchanged(
    repo_root: Path,
    unmerged: list[str],
    before: _ProtectedConflictSnapshot,
) -> None:
    """Codex が conflict 対象外 path を変更していないことを確認する。"""
    after = _protected_conflict_snapshot(repo_root, unmerged)
    if after == before:
        return

    changed_paths = sorted(set(before) | set(after))
    details = []
    for path in changed_paths:
        if before.get(path) == after.get(path):
            continue
        details.append(path)

    raise CmocError(
        "Codex CLI が conflict 対象外の path を変更しました。",
        [
            "merge commit は作成していません。",
            "表示された path の変更を手動で確認し、merge を手動で解消してください。",
        ],
        "\n".join(details),
    )


def _porcelain_status_entries(repo_root: Path) -> list[tuple[str, str]]:
    """git status porcelain から status と変更後 path を取得する。"""
    result = run_git(
        repo_root,
        ["status", "--porcelain=v1", "-z", "--untracked-files=all"],
    )
    return git_status_paths(result.stdout)


def _read_snapshot_bytes(repo_root: Path, relative_path: str) -> bytes | None:
    """存在する通常ファイルの内容を snapshot 用に読む。"""
    if relative_path == "memo" or relative_path.startswith("memo/"):
        return None
    path = repo_root / relative_path
    if not path.exists() or not path.is_file():
        return None
    return path.read_bytes()


def _index_snapshot_entry(repo_root: Path, relative_path: str) -> str:
    """path の index stage/blob 情報を snapshot 用に保存する。"""
    result = run_git(repo_root, ["ls-files", "-s", "-z", "--", relative_path])
    return result.stdout


def _unmerged_paths(repo_root: Path) -> list[str]:
    """unmerged path を git から取得する。"""
    # git diff の unmerged filter で現在残っている conflict path を読む。
    result = run_git(repo_root, ["diff", "--name-only", "-z", "--diff-filter=U"])
    return git_name_only_paths(result.stdout)


def _conflict_prompt(repo_root: Path, unmerged: list[str]) -> str:
    """session join conflict 解消用 prompt を組み立てる。"""
    # Codex CLI には conflict 対象を git 相対パスではなく絶対パスで渡す。
    concrete_repo_root = repo_root.resolve()
    concrete_unmerged = [
        str((concrete_repo_root / relative_path).resolve())
        for relative_path in unmerged
    ]
    oracle_conflicts = [
        path
        for path in unmerged
        if path == "oracles" or path.startswith("oracles/")
    ]
    root_doc_conflicts = [
        path
        for path in unmerged
        if path in {"README.md", "AGENTS.md"}
    ]
    root_doc_conflict_set = set(root_doc_conflicts)

    lines = [
        "あなたは merge conflict 解消担当です。",
        f"`{concrete_repo_root}` の以下の conflict 対象ファイルだけを編集してください:",
        str(concrete_unmerged),
        "完了条件は、conflict marker を削除し、解決内容と未解決ファイルの有無を報告することです。",
        "`git add` と `git commit` は実行禁止です。",
        "conflict 対象外のファイルは編集禁止です。",
        f"`{concrete_repo_root / '.agents'}` は編集禁止です。",
        f"`{concrete_repo_root / 'memo'}` は読み書き禁止です。",
    ]
    for root_doc in ("README.md", "AGENTS.md"):
        concrete_root_doc = concrete_repo_root / root_doc
        if root_doc in root_doc_conflict_set:
            lines.append(
                f"`{concrete_root_doc}` は conflict marker 解消に限って編集できます。"
            )
        else:
            lines.append(f"`{concrete_root_doc}` は編集禁止です。")
    if oracle_conflicts:
        concrete_oracle_conflicts = [
            str((concrete_repo_root / relative_path).resolve())
            for relative_path in oracle_conflicts
        ]
        lines.extend(
            [
                "以下の oracle file は conflict marker 解消に限って編集できます:",
                str(concrete_oracle_conflicts),
                "oracle file の意味的な仕様改訂、conflict 対象外 oracle file の編集は禁止です。",
            ]
        )
    else:
        lines.append(f"`{concrete_repo_root / 'oracles'}` は編集禁止です。")
    return "\n".join(lines)
