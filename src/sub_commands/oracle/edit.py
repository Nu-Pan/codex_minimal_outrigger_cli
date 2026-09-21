"""`cmoc oracle edit` の main-worktree exec workload。"""

from pathlib import Path

from acp.builder.oracle.edit.launch_exec import (
    build_oracle_edit_main_launch_exec_parameter,
)
from cmoc_runtime import (
    CmocError,
    load_config,
    repo_root,
    run_cli_subcommand,
    run_codex_exec,
    start_subcommand_step,
    work_root,
)
from commons.indexing import run_indexing_preflight
from commons.prompt_editor_input import (
    ORIGINAL_PROMPT_PLACEHOLDER,
    collect_prompt_editor_input,
    edit_prompt_editor_input,
    ensure_prompt_editor_roots_ignored,
    finalize_prompt_editor_input,
    reserve_prompt_editor_input,
)
from commons.runtime_git import current_branch
from commons.runtime_primary_report import update_primary_report_fields
from commons.runtime_state import load_session_part_for_branch


def cmoc_oracle_edit_impl() -> None:
    """CLI runtime を通して 2 回の oracle edit agent call を実行する。"""
    run_cli_subcommand(
        _cmoc_oracle_edit_body,
        pre_log_check=ensure_prompt_editor_roots_ignored,
        command_name="oracle edit",
        command_argv=["cmoc", "oracle", "edit"],
        total_steps=10,
    )


def _cmoc_oracle_edit_body() -> None:
    """入力された oracle 編集指示から 2 回の Codex exec を起動する。"""
    repository = repo_root()
    current_root = work_root()

    # oracle 編集契約を含む完全 prompt の skeleton を handoff ガイドに使う。
    # {{work-root}}/oracle/doc/app_spec/sub_command/oracle_edit.md
    start_subcommand_step(2, "編集 prompt の skeleton を構築", "build edit skeleton")
    complete_prompt_skeleton = build_oracle_edit_main_launch_exec_parameter(
        ORIGINAL_PROMPT_PLACEHOLDER
    ).prompt
    # skeleton の構築に成功した後でだけ editor work file を予約する。
    editor_work_path, input_copy_path = reserve_prompt_editor_input(repository)

    start_subcommand_step(3, "oracle 最終状態の指示を入力", "edit instruction")
    edit_prompt_editor_input(
        repository,
        editor_work_path,
        complete_prompt_skeleton,
    )

    start_subcommand_step(4, "入力結果を保存・抽出", "save and extract input")
    instruction = collect_prompt_editor_input(
        repository,
        editor_work_path,
        input_copy_path,
    )

    start_subcommand_step(5, "共用する入力と設定を確定", "prepare edit calls")
    parameter = build_oracle_edit_main_launch_exec_parameter(instruction)
    # JSON から復元した設定を両回で共用し、自己編集後の定義・設定を再取得しない。
    config = load_config(current_root)
    finalize_prompt_editor_input(repository, editor_work_path)
    start_subcommand_step(6, "編集前 indexing", "indexing before edits")
    run_indexing_preflight(repository, run_codex_exec)
    start_subcommand_step(7, "編集起動の事前条件を確認", "validate edit launch")
    _require_oracle_edit_launch_preconditions(repository, current_root)

    for pass_number, pass_name in enumerate(("first", "second"), start=1):
        start_subcommand_step(
            7 + pass_number,
            f"{pass_number} 回目の編集 agent call を実行",
            f"run edit agent call {pass_number}",
        )
        status_field = f"{pass_name}_agent_call_status"
        update_primary_report_fields(**{status_field: "started"})
        try:
            run_codex_exec(
                parameter,
                root=repository,
                config=config,
                purpose=f"oracle edit {pass_name}",
            )
        except BaseException:
            update_primary_report_fields(**{status_field: "failed"})
            raise
        update_primary_report_fields(**{status_field: "succeeded"})
    start_subcommand_step(10, "終了状態を確定", "finalize oracle edit")


# {{work-root}}/oracle/doc/app_spec/sub_command/oracle_edit.md
def _require_oracle_edit_launch_preconditions(
    repository: Path,
    current_root: Path,
) -> None:
    """main worktree の active session branch を要求する。"""
    if current_root.resolve() != repository.resolve():
        raise CmocError(
            "cmoc oracle edit は main worktree から実行してください。",
            ["main worktree の active session branch へ移動して再実行してください。"],
            f"work_root: {current_root.resolve()}\nrepo_root: {repository.resolve()}",
        )
    branch = current_branch(current_root)
    if not branch.startswith("cmoc/session/"):
        raise CmocError(
            "cmoc oracle edit は session branch 上で実行してください。",
            ["active な cmoc session branch へ checkout して再実行してください。"],
            f"current branch: {branch}",
        )
    _, state_file, session = load_session_part_for_branch(repository, branch)
    if session.state != "active":
        raise CmocError(
            "active な session ではありません。",
            ["active な cmoc session branch で再実行してください。"],
            f"session.state: {session.state}\nstate: {state_file}",
        )
