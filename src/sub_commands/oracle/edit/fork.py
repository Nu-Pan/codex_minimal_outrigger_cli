"""`cmoc oracle edit fork` の isolated editing workload。"""

from pathlib import Path

import typer

from acp.builder.oracle.edit.fork.launch_exec import (
    build_oracle_edit_fork_launch_exec_parameter,
)
from cmoc_runtime import (
    CmocError,
    load_config,
    pushd,
    run_cli_subcommand,
    run_codex_exec,
    start_subcommand_step,
)
from commons.indexing import enable_indexing_preflight
from commons.prompt_editor_input import (
    collect_prompt_editor_input,
    ensure_prompt_editor_roots_ignored,
)
from commons.runtime_run import run_process_tracking
from sub_commands.run.lifecycle import (
    EditingRunContext,
    commit_work_unit,
    flattened_change_paths,
    refresh_indexes,
    require_ready_session,
    rollback_work_unit,
    set_run_state,
    start_editing_run,
    tree_changes,
    unexpected_agent_paths,
    unexpected_run_paths,
    worktree_change_paths,
)
from sub_commands.run.report import write_fork_report

# {{work-root}}/oracle/doc/app_spec/sub_command/oracle_edit.md
ORACLE_EDIT_FORK_TEMPLATE = """<!--
以下の指示は cmoc が自動注入するため、この file に書いてはいけない。

- realization file の読み書き禁止
- oracle file の規約・規範
- TODO
-->"""


def cmoc_oracle_edit_fork_impl() -> None:
    """CLI runtime を通して oracle edit fork を実行する。"""
    enable_indexing_preflight()
    run_cli_subcommand(
        _cmoc_oracle_edit_fork_body,
        pre_log_check=ensure_prompt_editor_roots_ignored,
        command_name="oracle edit fork",
        command_argv=["cmoc", "oracle", "edit", "fork"],
        total_steps=8,
    )


def _cmoc_oracle_edit_fork_body() -> None:
    """ユーザー指示を 1 回の Codex exec で oracle file へ反映する。"""
    start_subcommand_step(2, "editing run の事前条件を確認", "validate run")
    repository, *_ = require_ready_session()
    start_subcommand_step(3, "oracle 最終状態の指示を入力", "edit instruction")
    _, instruction = collect_prompt_editor_input(
        repository,
        ORACLE_EDIT_FORK_TEMPLATE,
    )
    context: EditingRunContext | None = None
    codex_returncode: int | None = None
    try:
        start_subcommand_step(4, "oracle edit run を作成", "create editing run")
        context = start_editing_run("oracle_edit")
        parameter = build_oracle_edit_fork_launch_exec_parameter(
            instruction,
            context.run_worktree,
        )
        start_subcommand_step(5, "oracle 編集 agent を実行", "run oracle editor")
        with (
            run_process_tracking(context.repo, context.session_id),
            pushd(context.run_worktree),
        ):
            result = run_codex_exec(
                parameter,
                root=context.repo,
                cwd=context.run_worktree,
                config=load_config(context.run_worktree),
                purpose="oracle edit fork",
            )
        codex_returncode = result.returncode
        if result.returncode != 0:
            raise CmocError(
                "oracle edit agent が正常終了しませんでした。",
                ["run report と Codex call log を確認してください。"],
                f"returncode: {result.returncode}",
            )
        start_subcommand_step(6, "oracle 差分を検査して commit", "commit changes")
        _validate_agent_changes(context)
        refresh_indexes(context.run_worktree, commit=True)
        commit_work_unit(
            context.run_worktree,
            "cmoc oracle edit fork",
            allow_empty=True,
        )
        changes = tree_changes(
            context.run_worktree,
            context.run_fork_commit,
        )
        unexpected = unexpected_run_paths(context, changes)
        if unexpected:
            raise _unexpected_change_error(unexpected)
        start_subcommand_step(7, "run を joinable に更新", "publish joinable")
        set_run_state(context, "joinable")
        start_subcommand_step(8, "fork report を保存", "write fork report")
        report = write_fork_report(
            context,
            "oracle/edit/fork",
            state_after="joinable",
            completion_reason="completed",
            changed_paths=flattened_change_paths(changes),
            codex_returncode=codex_returncode,
        )
    except BaseException as exc:
        if context is None:
            raise
        report = _record_error(context, codex_returncode, exc)
        error = CmocError(
            "oracle edit fork は error state で停止しました。",
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
    paths = worktree_change_paths(context.run_worktree)
    unexpected = unexpected_agent_paths(context, paths)
    if unexpected:
        raise _unexpected_change_error(unexpected)


def _unexpected_change_error(paths: list[str]) -> CmocError:
    return CmocError(
        "oracle edit run に想定外差分があります。",
        ["run report を確認し、run を join または abandon してください。"],
        "\n".join(paths),
    )


def _record_error(
    context: EditingRunContext,
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
        "oracle/edit/fork",
        state_after="error",
        completion_reason="error",
        changed_paths=flattened_change_paths(changes),
        codex_returncode=codex_returncode,
        body_lines=[
            "## Error",
            repr(exc),
            "## Cleanup warnings",
            *([f"- {item}" for item in cleanup_errors] or ["- none"]),
        ],
    )
