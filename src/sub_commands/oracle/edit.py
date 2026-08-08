"""`cmoc oracle edit` の main-worktree TUI workload。"""

from pathlib import Path

from acp.builder.oracle.edit.launch_tui import (
    build_oracle_edit_launch_tui_parameter,
)
from cmoc_runtime import (
    CmocError,
    load_config,
    repo_root,
    run_cli_subcommand,
    run_codex_tui,
    start_subcommand_step,
    work_root,
)
from commons.indexing import enable_indexing_preflight
from commons.prompt_editor_input import (
    ORIGINAL_PROMPT_PLACEHOLDER,
    collect_prompt_editor_input,
    ensure_prompt_editor_roots_ignored,
    finalize_complete_prompt,
    reserve_prompt_editor_input,
)
from commons.runtime_git import current_branch, require_clean_worktree
from commons.runtime_state import load_session_part_for_branch


def cmoc_oracle_edit_impl() -> None:
    """CLI runtime を通して oracle edit TUI を起動する。"""
    enable_indexing_preflight()
    run_cli_subcommand(
        _cmoc_oracle_edit_body,
        pre_log_check=ensure_prompt_editor_roots_ignored,
        command_name="oracle edit",
        command_argv=["cmoc", "oracle", "edit"],
        tui_process=True,
        total_steps=7,
    )


def _cmoc_oracle_edit_body() -> None:
    """入力された oracle 編集指示から Codex TUI を起動する。"""
    repository = repo_root()
    current_root = work_root()

    # oracle 編集契約を含む完全 prompt の skeleton とパラメータを先に固定する。
    # {{work-root}}/oracle/doc/app_spec/sub_command/oracle_edit.md
    start_subcommand_step(2, "TUI 起動パラメータを構築", "build TUI parameter")
    time_stamp, original_path, complete_path = reserve_prompt_editor_input(repository)
    parameter = build_oracle_edit_launch_tui_parameter(
        time_stamp,
        ORIGINAL_PROMPT_PLACEHOLDER,
    )
    complete_prompt_skeleton = complete_path.read_text(encoding="utf-8")

    start_subcommand_step(3, "oracle 最終状態の指示を入力", "edit instruction")
    instruction = collect_prompt_editor_input(
        original_path,
        complete_prompt_skeleton,
    )

    start_subcommand_step(4, "完全プロンプトを確定", "finalize complete prompt")
    finalize_complete_prompt(
        complete_path,
        complete_prompt_skeleton,
        instruction,
    )
    start_subcommand_step(5, "TUI 起動前 indexing", "indexing preflight")

    def _validate_and_start_launch_step() -> None:
        """oracle edit TUI の起動前提を検証し、最後の step を開始する。"""
        start_subcommand_step(6, "TUI 起動の事前条件を確認", "validate TUI launch")
        _require_oracle_edit_launch_preconditions(repository, current_root)
        start_subcommand_step(7, "Codex TUI を起動", "launch Codex TUI")

    run_codex_tui(
        parameter,
        root=repository,
        config=load_config(current_root),
        purpose="oracle edit",
        pre_launch_check=_validate_and_start_launch_step,
        notification_command_name="oracle edit",
    )


def _require_oracle_edit_launch_preconditions(
    repository: Path,
    current_root: Path,
) -> None:
    """main worktree の active session branch と clean 状態を要求する。"""
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
    require_clean_worktree(current_root)
