"""`cmoc realization apply fork` の差分追従 workload。"""

from pathlib import Path

import typer

from acp.builder.realization.apply.fork.launch_exec import (
    build_realization_apply_fork_launch_exec_parameter,
)
from cmoc_runtime import (
    CmocError,
    head_commit,
    load_config,
    load_state_for_branch,
    run_cli_subcommand,
    run_codex_exec,
    run_git,
    start_subcommand_step,
)
from commons.indexing import enable_indexing_preflight
from commons.runtime_feedback import accepted_feedback_observations
from commons.runtime_run import run_process_tracking, stop_tracked_codex_children
from commons.runtime_run_lifecycle import (
    EditingRunContext,
    GitChange,
    commit_work_unit,
    flattened_change_paths,
    is_generated_index_path,
    raw_oracle_diff,
    recover_started_run,
    refresh_indexes,
    rollback_work_unit,
    session_run_was_ready,
    set_run_state,
    start_editing_run,
    tree_changes,
    unexpected_agent_paths,
    unexpected_run_paths,
    worktree_change_paths,
)
from commons.runtime_run_report import write_fork_report


def cmoc_realization_apply_fork_impl() -> None:
    """CLI runtime を通して realization apply fork を実行する。"""
    enable_indexing_preflight()
    run_cli_subcommand(
        _cmoc_realization_apply_fork_body,
        command_name="realization apply fork",
        command_argv=["cmoc", "realization", "apply", "fork"],
        total_steps=7,
    )


def _cmoc_realization_apply_fork_body() -> None:
    """realization apply agent を実行し、差分を joinable run として公開する。"""
    context: EditingRunContext | None = None
    codex_returncode: int | None = None
    diff_base_commit: str | None = None
    agent_head: str | None = None
    agent_commit_check_active = False
    cleanup_warnings: list[str] = []
    start_attempted = False
    start_was_ready = False
    try:
        start_subcommand_step(2, "realization apply run を作成", "create editing run")
        start_was_ready = session_run_was_ready()
        start_attempted = True
        context = start_editing_run("realization_apply")
        _, _, state = load_state_for_branch(context.repo, context.session_branch)
        diff_base_commit = (
            state.session.last_joined_apply_fork_commit
            or state.session.session_fork_commit
        )
        if diff_base_commit is None:
            raise CmocError(
                "apply 差分の始点 commit を特定できません。",
                ["session state file を確認してください。"],
                str(context.state_path),
            )
        start_subcommand_step(3, "oracle raw diff を構築", "build oracle diff")
        oracle_diff = raw_oracle_diff(
            context.run_worktree,
            diff_base_commit,
            context.run_fork_commit,
        )
        parameter = build_realization_apply_fork_launch_exec_parameter(
            diff_base_commit,
            context.run_fork_commit,
            oracle_diff,
            context.run_worktree,
        )
        start_subcommand_step(4, "realization 追従 agent を実行", "run apply agent")
        # {{work-root}}/oracle/doc/app_spec/sub_command/editing_run.md
        # INDEX 再生成も run 中の Codex call なので、abandon が停止できるよう
        # agent call から処理単位の commit 検査まで同じ tracking scope に含める。
        run_worktree = context.run_worktree
        with run_process_tracking(context.repo, context.session_id):
            preflight_head = head_commit(run_worktree)

            def record_agent_head() -> None:
                """本命 agent の直前の run branch HEAD を記録する。"""
                nonlocal agent_commit_check_active, agent_head
                agent_head = head_commit(run_worktree)
                agent_commit_check_active = True

            try:
                result = run_codex_exec(
                    parameter,
                    root=context.repo,
                    config=load_config(context.run_worktree),
                    purpose="realization apply fork",
                    before_agent_call=record_agent_head,
                )
            except BaseException:
                if agent_commit_check_active and agent_head is not None:
                    _ensure_agent_did_not_commit(run_worktree, agent_head)
                else:
                    # {{work-root}}/oracle/doc/app_spec/sub_command/realization_apply.md
                    # callback 前の indexing commit は本命 agent の処理単位に含めず、
                    # 元の失敗を保ったまま error cleanup へ渡す。
                    _rollback_preflight_commits(run_worktree, preflight_head)
                raise
            if agent_commit_check_active and agent_head is not None:
                _ensure_agent_did_not_commit(run_worktree, agent_head)
            codex_returncode = result.returncode
            if result.returncode != 0:
                raise CmocError(
                    "realization apply agent が正常終了しませんでした。",
                    ["run report と Codex call log を確認してください。"],
                    f"returncode: {result.returncode}",
                )
            changed_agent_paths = worktree_change_paths(
                context.run_worktree,
                include_rename_sources=True,
            )
            unexpected = unexpected_agent_paths(context, changed_agent_paths)
            if unexpected:
                raise _unexpected_change_error(unexpected)
            start_subcommand_step(
                5, "realization 差分を検査して commit", "commit changes"
            )
            # {{work-root}}/oracle/doc/app_spec/sub_command/realization_apply.md
            # agent の realization 差分と cmoc が生成する INDEX.md を同じ処理単位に
            # 含め、後続の commit/rollback が両方へ同じように適用されるようにする。
            # {{work-root}}/oracle/doc/app_spec/run_isolation.md
            # INDEX refresh 前に tracked Codex child を停止し、agent 終了後の遅延
            # 書き込みを cmoc の生成差分へ混ぜない。
            cleanup_warnings.extend(
                stop_tracked_codex_children(context.repo, context.session_id)
            )
            if agent_commit_check_active and agent_head is not None:
                _ensure_agent_did_not_commit(run_worktree, agent_head)
            post_agent_paths = worktree_change_paths(
                context.run_worktree,
                include_rename_sources=True,
            )
            unexpected = unexpected_agent_paths(context, post_agent_paths)
            unexpected.extend(
                path
                for path in post_agent_paths
                if path not in changed_agent_paths and path not in unexpected
            )
            unexpected.sort()
            if unexpected:
                raise _unexpected_change_error(unexpected)
            refresh_indexes(context.run_worktree, commit=False)
            # {{work-root}}/oracle/doc/app_spec/run_isolation.md
            # 後続 process の遅い書き込みを差分検査・commit に混ぜないよう、最終
            # snapshot の前に tracked Codex child を停止する。
            cleanup_warnings.extend(
                stop_tracked_codex_children(context.repo, context.session_id)
            )
            if agent_commit_check_active and agent_head is not None:
                _ensure_agent_did_not_commit(run_worktree, agent_head)
            # tree_changes は commit 済みの差分だけを返すため、commit 前は status
            # path を同じ path 分類へ渡してから処理単位を確定する。
            pending_paths = worktree_change_paths(
                context.run_worktree,
                include_rename_sources=True,
            )
            pending_changes = [GitChange("M", (path,)) for path in pending_paths]
            unexpected = unexpected_run_paths(context, pending_changes)
            # {{work-root}}/oracle/doc/app_spec/indexing.md
            # indexing は INDEX.md だけを生成するため、agent 検査後に増えた realization
            # 差分を agent の許可済み差分へ便乗させない。
            unexpected.extend(
                path
                for path in pending_paths
                if path not in changed_agent_paths
                and not is_generated_index_path(
                    context.run_worktree,
                    path,
                    base=context.run_fork_commit,
                )
                and path not in unexpected
            )
            unexpected.sort()
            if unexpected:
                raise _unexpected_change_error(unexpected)
            agent_commit_check_active = False
            commit_work_unit(
                context.run_worktree,
                "cmoc realization apply fork",
                allow_empty=True,
            )
            changes = tree_changes(context.run_worktree, context.run_fork_commit)
        start_subcommand_step(6, "run を joinable に更新", "publish joinable")
        set_run_state(context, "joinable")
        start_subcommand_step(7, "fork report を保存", "write fork report")
        report = write_fork_report(
            context,
            "realization/apply/fork",
            state_after="joinable",
            completion_reason="completed",
            changed_paths=flattened_change_paths(changes),
            codex_returncode=codex_returncode,
            extra_fields=_apply_report_fields(diff_base_commit),
            body_lines=_cleanup_warning_lines(cleanup_warnings),
        )
    except BaseException as exc:
        if context is None:
            # {{work-root}}/oracle/doc/app_spec/sub_command/editing_run.md
            # 共通事前条件の CmocError では、既存 run をこの fork の失敗として
            # 回収してはいけない。start が公開済み context を付加した例外、または
            # start 処理が context を呼び出し側へ返す前の非 CmocError だけを回収する。
            if start_attempted and start_was_ready:
                if isinstance(exc, CmocError):
                    published_context = getattr(
                        exc, "_published_editing_run_context", None
                    )
                    if isinstance(published_context, EditingRunContext):
                        context = published_context
                else:
                    context = recover_started_run("realization_apply")
            if context is None:
                raise
        if agent_commit_check_active and agent_head is not None:
            try:
                _ensure_agent_did_not_commit(context.run_worktree, agent_head)
            except BaseException as agent_commit_error:
                exc = agent_commit_error
        report = _record_error(
            context,
            diff_base_commit,
            codex_returncode,
            exc,
            cleanup_warnings,
        )
        error = CmocError(
            "realization apply fork は error state で停止しました。",
            [
                "確定済み成果物を取り込む場合は `cmoc run join` を実行してください。",
                "run 全体を破棄する場合は `cmoc run abandon` を実行してください。",
            ],
            f"report: {report}\nerror: {exc!r}",
        )
        setattr(error, "cmoc_stdout", f"- fork report: `{report}`")
        raise error from exc
    typer.echo(f"- fork report: `{report}`")


def _unexpected_change_error(paths: list[str]) -> CmocError:
    """想定外の apply 差分を共通の利用者向け例外へ変換する。"""
    return CmocError(
        "realization apply run に想定外差分があります。",
        ["run report を確認し、run を join または abandon してください。"],
        "\n".join(paths),
    )


def _ensure_agent_did_not_commit(worktree: Path, before_head: str) -> None:
    """本命 apply agent の commit を検出し、処理単位へ混入させない。"""
    after_head = head_commit(worktree)
    if after_head == before_head:
        return
    try:
        # {{work-root}}/oracle/doc/app_spec/sub_command/realization_apply.md
        # agent の変更は cmoc が差分検査後に処理単位として commit するため、agent
        # が先に履歴を進めた場合は本命 call 前の run tree へ戻して error cleanup へ渡す。
        run_git(["reset", "--hard", before_head], worktree)
    except BaseException as reset_error:
        raise CmocError(
            "realization apply agent が commit を作成し、差分を戻せませんでした。",
            ["run worktree の git history と Codex call log を確認してください。"],
            f"before HEAD: {before_head}\nafter HEAD: {after_head}\n"
            f"reset error: {reset_error!r}",
        ) from reset_error
    raise CmocError(
        "realization apply agent が git commit を実行しました。",
        [
            "agent の commit を取り除いてから realization apply fork を再実行してください。"
        ],
        f"before HEAD: {before_head}\nafter HEAD: {after_head}",
    )


def _rollback_preflight_commits(worktree: Path, before_head: str) -> None:
    """本命 agent 前の indexing commit を処理単位の開始 HEAD へ戻す。"""
    after_head = head_commit(worktree)
    if after_head == before_head:
        return
    try:
        # {{work-root}}/oracle/doc/app_spec/sub_command/realization_apply.md
        run_git(["reset", "--hard", before_head], worktree)
    except BaseException as reset_error:
        raise CmocError(
            "realization apply の preflight commit を差分へ戻せませんでした。",
            ["run worktree の git history と indexing の状態を確認してください。"],
            f"before HEAD: {before_head}\nafter HEAD: {after_head}\n"
            f"reset error: {reset_error!r}",
        ) from reset_error


def _record_error(
    context: EditingRunContext,
    diff_base_commit: str | None,
    codex_returncode: int | None,
    exc: BaseException,
    cleanup_warnings: list[str] | None = None,
) -> Path:
    """apply run の差分を戻し、error state と fork report を保存する。"""
    cleanup_errors = list(cleanup_warnings or [])
    try:
        cleanup_errors.extend(
            stop_tracked_codex_children(context.repo, context.session_id)
        )
    except BaseException as cleanup_error:
        cleanup_errors.append(f"Codex child stop failed: {cleanup_error!r}")
    try:
        rollback_work_unit(context.run_worktree)
    except BaseException as cleanup_error:
        cleanup_errors.append(f"rollback failed: {cleanup_error!r}")
    try:
        set_run_state(context, "error")
    except BaseException as state_error:
        cleanup_errors.append(f"state update failed: {state_error!r}")
    # 最終 git inspection が失敗しても error report を保存できるようにする。
    # 根拠: {{work-root}}/oracle/doc/app_spec/sub_command/realization_apply.md。
    try:
        changed_paths = flattened_change_paths(
            tree_changes(context.run_worktree, context.run_fork_commit)
        )
    except BaseException as change_error:
        cleanup_errors.append(f"change inspection failed: {change_error!r}")
        changed_paths = []
    return write_fork_report(
        context,
        "realization/apply/fork",
        state_after="error",
        completion_reason="error",
        changed_paths=changed_paths,
        codex_returncode=codex_returncode,
        extra_fields=_apply_report_fields(diff_base_commit),
        body_lines=[
            "## Error",
            repr(exc),
            *_cleanup_warning_lines(cleanup_errors),
        ],
    )


def _cleanup_warning_lines(warnings: list[str]) -> list[str]:
    """fork report 用の cleanup warning section を組み立てる。

    根拠: {{work-root}}/oracle/doc/app_spec/sub_command/editing_run.md
    """
    return [
        "## Cleanup warnings",
        *([f"- {warning}" for warning in warnings] or ["- none"]),
    ]


def _apply_report_fields(diff_base_commit: str | None) -> dict[str, object]:
    """apply 固有の diff 始点と accepted feedback 参照を返す。"""
    observations = accepted_feedback_observations()
    return {
        "diff_base_commit": diff_base_commit,
        "feedback_observation_count": len(observations),
        "feedback_observations": observations,
    }
