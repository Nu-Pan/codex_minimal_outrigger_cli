"""`cmoc realization apply fork` の差分追従 workload。"""

from pathlib import Path

import typer

from acp.builder.realization.apply.fork.launch_exec import (
    build_realization_apply_fork_launch_exec_parameter,
)
from cmoc_runtime import (
    CmocError,
    load_config,
    load_state_for_branch,
    pushd,
    run_cli_subcommand,
    run_codex_exec,
    start_subcommand_step,
)
from commons.indexing import enable_indexing_preflight
from commons.runtime_run import run_process_tracking
from sub_commands.run.lifecycle import (
    EditingRunContext,
    commit_work_unit,
    flattened_change_paths,
    raw_oracle_diff,
    refresh_indexes,
    rollback_work_unit,
    set_run_state,
    start_editing_run,
    tree_changes,
    unexpected_agent_paths,
    unexpected_run_paths,
    worktree_change_paths,
)
from sub_commands.run.report import write_fork_report


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
    context: EditingRunContext | None = None
    codex_returncode: int | None = None
    diff_base_commit: str | None = None
    try:
        start_subcommand_step(2, "realization apply run を作成", "create editing run")
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
        with (
            run_process_tracking(context.repo, context.session_id),
            pushd(context.run_worktree),
        ):
            result = run_codex_exec(
                parameter,
                root=context.repo,
                cwd=context.run_worktree,
                config=load_config(context.run_worktree),
                purpose="realization apply fork",
            )
        codex_returncode = result.returncode
        if result.returncode != 0:
            raise CmocError(
                "realization apply agent が正常終了しませんでした。",
                ["run report と Codex call log を確認してください。"],
                f"returncode: {result.returncode}",
            )
        start_subcommand_step(5, "realization 差分を検査して commit", "commit changes")
        _validate_agent_changes(context)
        # {{work-root}}/oracle/doc/app_spec/sub_command/realization_apply.md
        # agent の realization 差分と cmoc が生成する INDEX.md を同じ処理単位に
        # 含め、後続の commit/rollback が両方へ同じように適用されるようにする。
        refresh_indexes(context.run_worktree, commit=False)
        commit_work_unit(
            context.run_worktree,
            "cmoc realization apply fork",
            allow_empty=True,
        )
        changes = tree_changes(context.run_worktree, context.run_fork_commit)
        unexpected = unexpected_run_paths(context, changes)
        if unexpected:
            raise _unexpected_change_error(unexpected)
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
            extra_fields={"diff_base_commit": diff_base_commit},
        )
    except BaseException as exc:
        if context is None:
            raise
        report = _record_error(
            context,
            diff_base_commit,
            codex_returncode,
            exc,
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


def _validate_agent_changes(context: EditingRunContext) -> None:
    unexpected = unexpected_agent_paths(
        context,
        worktree_change_paths(
            context.run_worktree,
            include_rename_sources=True,
        ),
    )
    if unexpected:
        raise _unexpected_change_error(unexpected)


def _unexpected_change_error(paths: list[str]) -> CmocError:
    return CmocError(
        "realization apply run に想定外差分があります。",
        ["run report を確認し、run を join または abandon してください。"],
        "\n".join(paths),
    )


def _record_error(
    context: EditingRunContext,
    diff_base_commit: str | None,
    codex_returncode: int | None,
    exc: BaseException,
) -> Path:
    cleanup_errors: list[str] = []
    try:
        rollback_work_unit(context.run_worktree)
    except BaseException as cleanup_error:
        cleanup_errors.append(f"rollback failed: {cleanup_error!r}")
    try:
        set_run_state(context, "error")
    except BaseException as state_error:
        cleanup_errors.append(f"state update failed: {state_error!r}")
    changes = tree_changes(context.run_worktree, context.run_fork_commit)
    return write_fork_report(
        context,
        "realization/apply/fork",
        state_after="error",
        completion_reason="error",
        changed_paths=flattened_change_paths(changes),
        codex_returncode=codex_returncode,
        extra_fields={"diff_base_commit": diff_base_commit},
        body_lines=[
            "## Error",
            repr(exc),
            "## Cleanup warnings",
            *([f"- {item}" for item in cleanup_errors] or ["- none"]),
        ],
    )
