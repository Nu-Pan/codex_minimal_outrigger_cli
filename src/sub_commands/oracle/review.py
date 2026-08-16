"""oracle review の CLI と isolated run lifecycle を統括する。

この file は 16,000 文字を超えるが、次の処理は同じ resource ownership と例外処理を
共有する一つの責務である。

- review run の target 作成
- review loop の呼び出し
- INDEX 差分の merge
- 中断・失敗時の cleanup と report

これらを分割すると、中断・部分作成・cleanup failure の状態遷移を複数 file で追う必要
があるため、現状は oracle review lifecycle として一箇所に保つ。

根拠:
- {{work-root}}/oracle/doc/app_spec/sub_command/oracle_review.md
- {{work-root}}/oracle/doc/app_spec/run_isolation.md
- {{work-root}}/oracle/doc/app_spec/subcommand_interruption.md
- {{work-root}}/oracle/src/oracle/prompt_builder/policy/realization.py
"""

# {{work-root}}/oracle/doc/app_spec/sub_command/oracle_review.md
from pathlib import Path

from cmoc_runtime import (
    CmocError,
    SessionState,
    TerminalResult,
    branch_exists,
    create_run_worktree,
    current_branch,
    current_subcommand_logger,
    delete_branch,
    head_commit,
    load_config,
    load_state_for_branch,
    mark_current_subcommand_interrupted,
    remove_worktree,
    repo_root,
    run_cli_subcommand,
    run_codex_exec,
    run_doctor_preprocess,
    start_subcommand_step,
    work_root,
)
from commons.indexing import enable_indexing_preflight
from commons.runtime_git import status_path_statuses
from commons.runtime_results import CodexExecCallable
from commons.runtime_run import run_lifecycle_lock
from commons.runtime_run_lifecycle import new_run_target

from .review_index import (
    commit_review_index_changes,
    merge_review_branch,
    resolve_review_index_conflicts,
    review_branch_has_index_changes,
    review_worktree_status_paths,
)
from .review_loop import (
    OracleReviewInterrupted,
    apply_finding_merge_operations,
    run_oracle_review_loop,
)
from .review_report import (
    oracle_review_result,
    path_display,
    render_finding_section,
    render_oracle_review_report,
    write_oracle_review_report,
)
from .review_targets import (
    enumerate_oracle_review_targets,
    enumerate_review_all_oracle_files,
)

CodexExec = CodexExecCallable

__all__ = [
    "CodexExec",
    "apply_finding_merge_operations",
    "cmoc_oracle_review_impl",
    "commit_review_index_changes",
    "enumerate_review_all_oracle_files",
    "enumerate_oracle_review_targets",
    "merge_review_branch",
    "path_display",
    "render_finding_section",
    "render_oracle_review_report",
    "resolve_review_index_conflicts",
    "review_worktree_status_paths",
    "run_oracle_review_loop",
    "write_oracle_review_report",
]


def cmoc_oracle_review_impl(scope: str) -> None:
    """CLI runtime を通して oracle review を実行する。"""
    enable_indexing_preflight()
    run_cli_subcommand(
        _cmoc_oracle_review_body,
        scope,
        run_codex_exec,
        command_name="oracle review",
        command_argv=["cmoc", "oracle", "review", "--scope", scope],
        # {{work-root}}/oracle/doc/app_spec/subcommand_interruption.md
        interruptible=True,
        total_steps=8,
        # oracle review は doctor 中断でも固有の interrupted report を保存する。
        doctor_preprocess=False,
    )


def _cmoc_oracle_review_body(
    scope: str,
    codex_exec: CodexExec,
) -> TerminalResult:
    """現在の session branch の oracle を isolated review worktree 上でレビューする。"""
    root = repo_root()
    current_root = work_root()
    branch = ""
    session_id = ""
    state = SessionState()
    run_branch: str | None = None
    review_worktree = root
    run_fork_commit: str | None = None
    run_join_commit: str | None = None
    all_oracle_files: list[Path] = []
    oracle_files: list[Path] = []
    evaluated_oracle_files: list[Path] = []
    findings: list[dict] = []
    review_worktree_created = False
    run_branch_created = False
    interrupted = False
    cleanup_error: CmocError | None = None

    try:
        # {{work-root}}/oracle/doc/app_spec/sub_command/oracle_review.md
        # 共通 runner の impl 前中断経路を迂回し、doctor 中断も review report へ到達させる。
        start_subcommand_step(1, "doctor preprocess", "doctor preprocess")
        run_doctor_preprocess(current_root)
        branch = current_branch(current_root)
        session_id, _state_path, state = load_state_for_branch(root, branch)
        if not branch.startswith("cmoc/session/") or state.session.state != "active":
            raise CmocError(
                "oracle review は active session branch 上で実行してください。",
                [],
                branch,
            )
        _require_clean_worktree(current_root)
        config = load_config(current_root)
        run_fork_commit = head_commit(current_root)
    except KeyboardInterrupt:
        # {{work-root}}/oracle/doc/app_spec/sub_command/oracle_review.md
        # run resource を作る前の中断でも、空の確定結果を interrupted report として残す。
        _record_oracle_review_interruption()
        report_path = write_oracle_review_report(
            root,
            scope,
            branch,
            state,
            0,
            [],
            [],
            None,
            run_fork_commit,
            None,
            interrupted=True,
        )
        return _oracle_review_terminal_result(report_path, "interrupted")

    def _cleanup_created_resources() -> CmocError | None:
        """今回作成した review resource だけを cleanup して所有権を破棄する。

        根拠: {{work-root}}/oracle/doc/app_spec/subcommand_interruption.md
        """
        nonlocal review_worktree_created, run_branch_created
        if not (review_worktree_created or run_branch_created):
            return None
        if run_branch is None:
            return CmocError(
                "oracle review の隔離 run の cleanup に失敗しました。",
                [
                    "review worktree と run branch の状態を確認してください。",
                    "残った隔離 run の資源を整理してから再実行してください。",
                ],
                "run branch was not resolved before cleanup",
            )
        try:
            # {{work-root}}/oracle/doc/branch_model.md
            # worktree を先に削除してから branch を削除するため、cleanup 中に同じ
            # run-id が再利用されると別 invocation の branch を誤って検査する。
            # target の再確保と resource cleanup を同じ lock で直列化する。
            try:
                with run_lifecycle_lock(root, session_id):
                    return _cleanup_review_run(
                        current_root,
                        review_worktree,
                        run_branch,
                        worktree_created=review_worktree_created,
                        branch_created=run_branch_created,
                    )
            except BaseException as exc:
                # lock 待機中の Ctrl+C でも resource ownership を成功扱いで捨てず、
                # 通常の cleanup failure として report する。
                return CmocError(
                    "oracle review の隔離 run の cleanup に失敗しました。",
                    [
                        "review worktree と run branch の状態を確認してください。",
                        "残った隔離 run の資源を整理してから再実行してください。",
                    ],
                    f"run lifecycle lock acquisition failed: {exc!r}",
                )
        finally:
            review_worktree_created = False
            run_branch_created = False

    try:
        assert run_fork_commit is not None
        start_subcommand_step(2, "run の隔離実行を開始", "start isolated review")
        # {{work-root}}/oracle/doc/app_spec/run_isolation.md
        # editing run と review run が同じ branch/worktree namespace を共有するため、
        # target の選択から linked worktree 作成までを共通 lock 下で行う。
        with run_lifecycle_lock(root, session_id):
            run_branch, review_worktree = new_run_target(root, session_id)
            run_fork_commit = head_commit(current_root)
            worktree_present_before_create = (
                review_worktree.exists() or review_worktree.is_symlink()
            )
            branch_present_before_create = branch_exists(root, run_branch)
            create_succeeded = False
            try:
                create_run_worktree(
                    current_root, run_branch, review_worktree, run_fork_commit
                )
                create_succeeded = True
            finally:
                # {{work-root}}/oracle/doc/app_spec/subcommand_interruption.md
                # worktree add が作成直後に中断されても、今回の作成物だけを cleanup 対象として
                # 後続の終了処理へ渡す。target 選択と作成は lock 下なので、検出された resource
                # はこの invocation の部分作成である。
                # create_run_worktree の成功後は branch/worktree とも今回の所有物なので、
                # probe の False で ownership を失わせない。
                if create_succeeded:
                    review_worktree_created = True
                    run_branch_created = True
                try:
                    worktree_present = (
                        review_worktree.exists() or review_worktree.is_symlink()
                    )
                except BaseException:
                    # 検出自体が中断されても、作成を開始した target はこの invocation の
                    # 所有物として扱う。ただし、作成前から存在した resource は別 invocation
                    # の所有物なので cleanup 対象にしない。
                    review_worktree_created = not worktree_present_before_create
                    run_branch_created = not branch_present_before_create
                    raise
                if not create_succeeded:
                    review_worktree_created = (
                        not worktree_present_before_create and worktree_present
                    )
                try:
                    branch_present = branch_exists(root, run_branch)
                except BaseException:
                    # branch probe 中の Ctrl+C でも、create_run_worktree が確保した branch を
                    # cleanup 対象として保持する。作成前から存在した branch は別 invocation
                    # の所有物なので cleanup しない。
                    run_branch_created = not branch_present_before_create
                    raise
                if not create_succeeded:
                    run_branch_created = (
                        not branch_present_before_create and branch_present
                    )
        try:
            start_subcommand_step(3, "所見リストを初期化", "initialize findings")
            all_oracle_files = enumerate_review_all_oracle_files(review_worktree)
            oracle_files = enumerate_oracle_review_targets(
                review_worktree, scope, state, run_fork_commit
            )
            try:
                findings = run_oracle_review_loop(
                    root,
                    review_worktree,
                    oracle_files,
                    config,
                    codex_exec,
                    step_callback=start_subcommand_step,
                    evaluated_files=evaluated_oracle_files,
                )
            except OracleReviewInterrupted as interruption:
                interrupted = True
                findings = interruption.findings
                evaluated_oracle_files = interruption.evaluated_files
                _record_oracle_review_interruption()
            start_subcommand_step(7, "run の隔離実行を終了", "finish isolated review")
            commit_review_index_changes(review_worktree)
            review_has_index_changes = review_branch_has_index_changes(
                review_worktree, run_fork_commit
            )
            if review_has_index_changes:
                # {{work-root}}/oracle/doc/app_spec/run_isolation.md
                # review run の自動 merge は editing run の join と同じ session branch
                # を更新するため、別 run の lifecycle 操作と直列化する。
                with run_lifecycle_lock(root, session_id):
                    run_join_commit = merge_review_branch(current_root, run_branch)
        finally:
            cleanup_error = _cleanup_created_resources()
        if cleanup_error is not None:
            raise cleanup_error
        start_subcommand_step(8, "所見リストをレポート", "write review report")
        report_path = write_oracle_review_report(
            root,
            scope,
            branch,
            state,
            len(all_oracle_files),
            evaluated_oracle_files,
            findings,
            run_branch,
            run_fork_commit,
            run_join_commit,
            interrupted=interrupted,
        )
    except KeyboardInterrupt:
        # loop 外の中断も、確定済みとして記録済みの範囲だけで正常完了する。
        cleanup_result = _cleanup_created_resources()
        if cleanup_result is not None:
            cleanup_error = cleanup_result
        if cleanup_error is not None:
            report_path = write_oracle_review_report(
                root,
                scope,
                branch,
                state,
                len(all_oracle_files),
                evaluated_oracle_files,
                findings,
                run_branch,
                run_fork_commit,
                run_join_commit,
                error_message=cleanup_error.detail,
            )
            cleanup_error.terminal_result = _oracle_review_terminal_result(
                report_path, "error"
            )
            raise cleanup_error
        if not interrupted:
            interrupted = True
            _record_oracle_review_interruption()
        report_path = write_oracle_review_report(
            root,
            scope,
            branch,
            state,
            len(all_oracle_files),
            evaluated_oracle_files,
            findings,
            run_branch,
            run_fork_commit,
            run_join_commit,
            interrupted=True,
        )
        return _oracle_review_terminal_result(report_path, "interrupted")
    except BaseException as exc:
        # {{work-root}}/oracle/doc/app_spec/run_isolation.md
        # create_run_worktree が部分作成後に失敗した場合も、隔離 run を残さない。
        cleanup_result = _cleanup_created_resources()
        if cleanup_result is not None:
            cleanup_error = cleanup_result
        if isinstance(exc, CmocError):
            error_message = f"{exc.summary}\n{exc.detail}"
        else:
            error_message = str(exc) or exc.__class__.__name__
        if cleanup_error is not None and cleanup_error is not exc:
            error_message = f"{error_message}\ncleanup: {cleanup_error.detail}"
        report_path = write_oracle_review_report(
            root,
            scope,
            branch,
            state,
            len(all_oracle_files),
            evaluated_oracle_files,
            findings,
            run_branch,
            run_fork_commit,
            run_join_commit,
            error_message=error_message,
        )
        terminal_result = _oracle_review_terminal_result(report_path, "error")
        if isinstance(exc, CmocError):
            exc.terminal_result = terminal_result
        else:
            setattr(exc, "cmoc_terminal_result", terminal_result)
        raise
    return _oracle_review_terminal_result(
        report_path,
        oracle_review_result(
            evaluated_oracle_files,
            findings,
            interrupted=interrupted,
        ),
    )


def _record_oracle_review_interruption() -> None:
    """review 中断要求を subcommand log へ記録する。"""
    # {{work-root}}/oracle/doc/app_spec/windows_toast_notification.md
    mark_current_subcommand_interrupted()
    logger = current_subcommand_logger()
    if logger is not None:
        logger.event(
            "user_interruption",
            command="oracle review",
            result="interrupted",
        )


def _oracle_review_terminal_result(report_path: Path, result: str) -> TerminalResult:
    """保存済み review report を一意な primary report として返す。"""
    return TerminalResult(
        primary_report=report_path,
        primary_report_role="oracle review report",
        result=result,
    )


def _cleanup_review_run(
    root: Path,
    review_worktree: Path,
    run_branch: str,
    *,
    worktree_created: bool,
    branch_created: bool,
) -> CmocError | None:
    """review run の worktree と branch を削除し、失敗を report 可能にする。

    `remove_worktree` と `delete_branch` は失敗を returncode で返すため、結果を
    無視すると隔離 run が残ったまま成功扱いになる。

    根拠: {{work-root}}/oracle/doc/app_spec/sub_command/oracle_review.md
    """
    errors: list[str] = []
    if worktree_created:
        try:
            removal = remove_worktree(root, review_worktree)
            if (
                removal.returncode != 0
                or review_worktree.exists()
                or review_worktree.is_symlink()
            ):
                errors.append(
                    "worktree removal failed: "
                    + (
                        removal.stderr.strip()
                        or (
                            f"returncode: {removal.returncode}"
                            if removal.returncode != 0
                            else "path still exists"
                        )
                    )
                )
        except BaseException as exc:
            errors.append(f"worktree removal failed: {exc!r}")
    if branch_created:
        try:
            deletion = delete_branch(root, run_branch, force=True)
            if deletion.returncode != 0:
                errors.append(
                    "run branch deletion failed: "
                    + (deletion.stderr.strip() or f"returncode: {deletion.returncode}")
                )
            elif branch_exists(root, run_branch):
                errors.append("run branch deletion failed: branch still exists")
        except BaseException as exc:
            errors.append(f"run branch deletion failed: {exc!r}")
    if not errors:
        return None
    return CmocError(
        "oracle review の隔離 run の cleanup に失敗しました。",
        [
            "review worktree と run branch の状態を確認してください。",
            "残った隔離 run の資源を整理してから再実行してください。",
        ],
        "\n".join(errors),
    )


def _require_clean_worktree(root: Path) -> None:
    """git status を検査し、未コミット差分があれば CmocError を送出する。"""
    statuses = status_path_statuses(
        root, untracked_all=True, include_rename_sources=True
    )
    if statuses:
        raise CmocError(
            "oracle review は git 未コミット差分がある状態では実行できません。",
            ["差分を commit または退避してから再実行してください。"],
            "\n".join(str(path) for _status, path in statuses),
        )
