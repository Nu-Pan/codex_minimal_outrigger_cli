"""`cmoc apply abandon` の本体処理。"""

import os
import signal
from pathlib import Path
from time import sleep

from commons.command_runner import run_command
from commons.errors import CmocError
from commons.repo import (
    apply_worktree_path_from_branch,
    assert_no_uncommitted_changes,
    clear_apply_process_id,
    current_branch,
    is_apply_branch,
    is_session_branch,
    process_cmdline,
    process_start_time,
    read_apply_process_record,
    read_session_state,
    run_git,
    session_id_from_branch,
    session_state_repo_root,
    worktree_path_for_branch,
    write_session_state,
)
from commons.timing import StepTimer, start_step


def cmoc_apply_abandon_impl(repo_root: Path | None = None) -> None:
    """現在の session に紐づく未 join apply run を破棄する。"""
    # 直接呼び出し時は共通 runner で repo root 解決とエラー整形を行う。
    if repo_root is None:
        run_command(cmoc_apply_abandon_impl)
        return

    timer = StepTimer("apply abandon")
    start_step(timer, 1, 4, "validate apply state")
    branch_name = current_branch(repo_root)
    session_id = session_id_from_branch(branch_name)
    cmoc_root = session_state_repo_root(repo_root, session_id)
    os.chdir(cmoc_root)
    state = read_session_state(cmoc_root, session_id)
    abandon_state = _validate_abandonable_state(
        cmoc_root,
        state,
        branch_name,
        session_id,
    )
    session_worktree = worktree_path_for_branch(
        cmoc_root,
        abandon_state.session_branch,
    )
    if session_worktree is not None:
        assert_no_uncommitted_changes(session_worktree)

    start_step(timer, 2, 4, "stop running apply")
    warnings = _stop_running_apply(abandon_state)

    start_step(timer, 3, 4, "cleanup apply artifacts")
    _relocate_from_apply_branch(
        cmoc_root,
        branch_name,
        abandon_state,
        session_worktree,
    )
    warnings.extend(_cleanup_apply_artifacts(cmoc_root, abandon_state))

    start_step(timer, 4, 4, "record ready apply state")
    _mark_apply_ready(cmoc_root, session_id, state)

    print(f"abandoned apply branch: {abandon_state.apply_branch}")
    print(f"abandoned apply worktree: {abandon_state.apply_worktree}")
    print(f"previous apply.state: {abandon_state.previous_apply_state}")
    print("current apply.state: ready")
    for warning in warnings:
        print(f"warning: {warning}")
    timer.report()


class _AbandonState:
    """apply abandon に必要な state 値。"""

    def __init__(
        self,
        *,
        apply_branch: str,
        session_branch: str,
        apply_worktree: Path,
        previous_apply_state: str,
        repo_root: Path,
        session_id: str,
        process_record: dict[str, object] | None,
    ) -> None:
        self.apply_branch = apply_branch
        self.session_branch = session_branch
        self.apply_worktree = apply_worktree
        self.previous_apply_state = previous_apply_state
        self.repo_root = repo_root
        self.session_id = session_id
        self.process_record = process_record


def _validate_abandonable_state(
    repo_root: Path,
    state: dict[str, object],
    current_branch_name: str,
    session_id: str,
) -> _AbandonState:
    """apply abandon の state 前提条件を検証する。"""
    session = state.get("session")
    apply = state.get("apply")
    if not isinstance(session, dict) or not isinstance(apply, dict):
        raise CmocError(
            "session state ファイルの形式が不正です。",
            [
                "state JSON の session/apply セクションを確認して復旧してください。",
                "復旧できない場合は、対象 session を使わず新しい session を開始してください。",
            ],
            f"現在の branch: {current_branch_name}",
        )
    session_branch = f"cmoc/session/{session_id}"
    if session.get("state") != "active":
        raise CmocError(
            "active な session ではありません。",
            [
                "対象 session の state を確認してください。",
                "既に join または abandon 済みの場合は、新しい session を開始してください。",
            ],
            f"session.state: {session.get('state')}",
        )
    apply_state = apply.get("state")
    if apply_state == "ready":
        raise CmocError(
            "破棄対象の apply run がありません。",
            [
                "`cmoc apply fork` で apply run を開始してから実行してください。",
                "session state の apply.state を確認してください。",
            ],
            f"apply.state: {apply_state}",
        )
    if not isinstance(apply_state, str) or not apply_state:
        raise CmocError(
            "apply state を session state から特定できませんでした。",
            [
                "session state の apply.state を確認して復旧してください。",
                "復旧できない場合は、対象 session を使わず新しい session を開始してください。",
            ],
            f"apply.state: {apply_state}",
        )
    if apply_state not in {"running", "completed", "error"}:
        raise CmocError(
            "session state ファイルの apply.state が不正です。",
            [
                "apply.state は ready/running/completed/error のいずれかである必要があります。",
                "破損した session state を復旧してから再実行してください。",
            ],
            f"apply.state: {apply_state}",
        )
    apply_branch = apply.get("apply_branch")
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
                "別 session の apply branch を破棄対象にしないでください。",
            ],
            "\n".join(
                [
                    f"session id: {session_id}",
                    f"apply branch session id: {apply_branch_session_id}",
                    f"apply.apply_branch: {apply_branch}",
                ]
            ),
        )
    apply_worktree = apply_worktree_path_from_branch(repo_root, apply_branch)
    if current_branch_name not in {session_branch, apply_branch}:
        raise CmocError(
            "`cmoc apply abandon` は session branch または apply branch 上で実行してください。",
            [
                "対象 session の session branch か、対応する apply branch へ移動してください。",
                "通常 branch の削除は `git branch -D` を直接実行してください。",
            ],
            f"現在の branch: {current_branch_name or '(detached HEAD)'}",
        )
    if not is_session_branch(session_branch):
        raise CmocError(
            "session branch 名が不正です。",
            [
                "session state ファイル名と branch 名を確認してください。",
                "正しい session branch 上で `cmoc apply abandon` を再実行してください。",
            ],
            f"session branch: {session_branch}",
        )
    process_record = None
    if apply_state == "running":
        process_record = read_apply_process_record(repo_root, session_id)
    return _AbandonState(
        apply_branch=apply_branch,
        session_branch=session_branch,
        apply_worktree=apply_worktree,
        previous_apply_state=apply_state,
        repo_root=repo_root,
        session_id=session_id,
        process_record=process_record,
    )


def _stop_running_apply(abandon_state: _AbandonState) -> list[str]:
    """running apply のプロセスを停止し、終了済みであることを確認する。"""
    if abandon_state.previous_apply_state != "running":
        return []
    process_record = abandon_state.process_record
    if process_record is None:
        raise CmocError(
            "running apply process id が記録されていません。",
            [
                ".cmoc/runtime/apply 配下の pid ファイルを確認してください。",
                "実行中の apply process を特定できないため、手動で状態を確認してから再実行してください。",
            ],
            "apply.state: running",
        )
    process_id = _process_id_from_record(process_record)
    if process_id == os.getpid():
        raise CmocError(
            "停止対象の apply process が現在の abandon process と一致します。",
            [
                "runtime の apply process id ファイルを確認してください。",
                "誤った process id が記録されている場合は、state を復旧してから再実行してください。",
            ],
            f"apply process id: {process_id}",
        )
    if not _process_exists(process_id):
        return [f"running apply process was already gone: pid {process_id}"]
    _assert_apply_process_identity(abandon_state, process_record, process_id)

    target_process_ids = [*reversed(_descendant_process_ids(process_id)), process_id]
    for target_process_id in target_process_ids:
        if _process_exists(target_process_id):
            os.kill(target_process_id, signal.SIGTERM)
    for _ in range(50):
        if not any(_process_exists(pid) for pid in target_process_ids):
            return []
        sleep(0.1)

    raise CmocError(
        "running apply process を停止できませんでした。",
        [
            "対象 process の状態を確認してください。",
            "`cmoc apply abandon` を再実行する前に、手動で process を停止してください。",
        ],
        f"apply process id: {process_id}",
    )


def _process_id_from_record(process_record: dict[str, object]) -> int:
    """runtime record から正の process id を取り出す。"""
    process_id = process_record.get("process_id")
    if isinstance(process_id, int) and process_id > 0:
        return process_id
    raise CmocError(
        "running apply process id が不正です。",
        [
            ".cmoc/runtime/apply 配下の pid ファイルを確認してください。",
            "実行中の apply process を特定できないため、手動で状態を確認してから再実行してください。",
        ],
        f"apply process id: {process_id}",
    )


def _assert_apply_process_identity(
    abandon_state: _AbandonState,
    process_record: dict[str, object],
    process_id: int,
) -> None:
    """PID 再利用を検出し、現在の apply process と確認できる場合だけ許可する。"""
    expected_repo_root = str(abandon_state.repo_root.resolve())
    recorded_start_time = process_record.get("proc_start_time")
    current_start_time = process_start_time(process_id)
    recorded_cmdline = process_record.get("cmdline")
    current_cmdline = process_cmdline(process_id)
    checks = [
        ("format", process_record.get("format"), "cmoc-apply-process-v1"),
        ("repo_root", process_record.get("repo_root"), expected_repo_root),
        ("session_id", process_record.get("session_id"), abandon_state.session_id),
        (
            "apply_branch",
            process_record.get("apply_branch"),
            abandon_state.apply_branch,
        ),
        (
            "proc_start_time",
            recorded_start_time,
            current_start_time,
        ),
        ("cmdline", recorded_cmdline, current_cmdline),
    ]
    mismatches = [
        f"{name}: recorded={recorded!r}, current={current!r}"
        for name, recorded, current in checks
        if recorded != current
    ]
    if not isinstance(recorded_start_time, int):
        mismatches.append(
            f"recorded proc_start_time is invalid: {recorded_start_time!r}"
        )
    if not isinstance(current_start_time, int):
        mismatches.append(
            f"current proc_start_time is unavailable: {current_start_time!r}"
        )
    if not isinstance(recorded_cmdline, list) or not recorded_cmdline:
        mismatches.append(f"recorded cmdline is invalid: {recorded_cmdline!r}")
    if not isinstance(current_cmdline, list) or not current_cmdline:
        mismatches.append(f"current cmdline is unavailable: {current_cmdline!r}")
    if not mismatches:
        return
    raise CmocError(
        "running apply process を安全に特定できませんでした。",
        [
            ".cmoc/runtime/apply 配下の pid ファイルと実行中 process を確認してください。",
            "対象が現在の apply process であると確認できるまで、手動で process を停止しないでください。",
        ],
        "\n".join([f"apply process id: {process_id}", *mismatches]),
    )


def _process_exists(process_id: int) -> bool:
    """process id が現在存在するかを OS に問い合わせる。"""
    proc_stat = Path(f"/proc/{process_id}/stat")
    if proc_stat.exists():
        try:
            fields = proc_stat.read_text(encoding="utf-8").split()
        except OSError:
            fields = []
        if len(fields) >= 3 and fields[2] == "Z":
            return False
    try:
        os.kill(process_id, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    return True


def _descendant_process_ids(process_id: int) -> list[int]:
    """Linux procfs から対象 process の子孫 process id を返す。"""
    children: list[int] = []
    for child_id in _child_process_ids(process_id):
        children.append(child_id)
        children.extend(_descendant_process_ids(child_id))
    return children


def _child_process_ids(process_id: int) -> list[int]:
    """Linux procfs から対象 process の直接の子 process id を返す。"""
    children_path = Path(f"/proc/{process_id}/task/{process_id}/children")
    try:
        content = children_path.read_text(encoding="utf-8")
    except OSError:
        return []
    return [int(value) for value in content.split() if value.isdigit()]


def _relocate_from_apply_branch(
    repo_root: Path,
    current_branch_name: str,
    abandon_state: _AbandonState,
    session_worktree: Path | None,
) -> None:
    """apply branch 上からの実行時に cleanup 基点を session branch へ移す。"""
    if current_branch_name != abandon_state.apply_branch:
        return
    if session_worktree is not None:
        os.chdir(session_worktree)
        return
    assert_no_uncommitted_changes(repo_root)
    switch_result = run_git(
        repo_root,
        ["switch", abandon_state.session_branch],
        check=False,
    )
    if switch_result.returncode == 0:
        assert_no_uncommitted_changes(repo_root)
        return
    detail = switch_result.stderr.strip()
    raise CmocError(
        "apply cleanup のため session branch へ移動できませんでした。",
        [
            "session branch の worktree 状態を確認してください。",
            "問題を解消してから `cmoc apply abandon` を再実行してください。",
        ],
        detail or f"session branch: {abandon_state.session_branch}",
    )


def _cleanup_apply_artifacts(
    repo_root: Path,
    abandon_state: _AbandonState,
) -> list[str]:
    """apply worktree と apply branch を強制削除する。"""
    warnings: list[str] = []
    if abandon_state.apply_worktree.exists():
        worktree_result = run_git(
            repo_root,
            ["worktree", "remove", "--force", str(abandon_state.apply_worktree)],
            check=False,
        )
        if worktree_result.returncode != 0:
            warnings.append(
                "apply worktree was not deleted: "
                f"{abandon_state.apply_worktree}"
            )
            detail = worktree_result.stderr.strip()
            if detail:
                warnings.append(detail)
    else:
        warnings.append(
            f"apply worktree was already missing: {abandon_state.apply_worktree}"
        )

    branch_exists = run_git(
        repo_root,
        ["show-ref", "--verify", f"refs/heads/{abandon_state.apply_branch}"],
        check=False,
    )
    if branch_exists.returncode == 0:
        branch_result = run_git(
            repo_root,
            ["branch", "-D", abandon_state.apply_branch],
            check=False,
        )
        if branch_result.returncode != 0:
            warnings.append(
                f"apply branch was not deleted: {abandon_state.apply_branch}"
            )
            detail = branch_result.stderr.strip()
            if detail:
                warnings.append(detail)
    else:
        warnings.append(
            f"apply branch was already missing: {abandon_state.apply_branch}"
        )
    return warnings


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
            [
                "state JSON の apply セクションを確認して復旧してください。",
                "復旧できない場合は、対象 session を使わず新しい session を開始してください。",
            ],
        )
    state["apply"] = {
        "state": "ready",
        "apply_branch": None,
        "oracle_snapshot_commit": None,
    }
    write_session_state(repo_root, session_id, state)
    clear_apply_process_id(repo_root, session_id)
