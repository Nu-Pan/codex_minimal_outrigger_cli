"""`cmoc oracle edit` の main-worktree exec workload。"""

from pathlib import Path

from acp.builder.oracle.edit.launch_exec import (
    build_oracle_edit_main_launch_exec_parameter,
    build_oracle_edit_reduction_launch_exec_parameter,
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
from commons.indexing import enable_indexing_preflight
from commons.prompt_editor_input import (
    ORIGINAL_PROMPT_PLACEHOLDER,
    collect_prompt_editor_input,
    ensure_prompt_editor_roots_ignored,
    finalize_complete_prompt,
    reserve_prompt_editor_input,
)
from commons.runtime_git import current_branch
from commons.runtime_state import load_session_part_for_branch


def cmoc_oracle_edit_impl() -> None:
    """CLI runtime を通して 2 回の oracle edit agent call を実行する。"""
    enable_indexing_preflight()
    run_cli_subcommand(
        _cmoc_oracle_edit_body,
        pre_log_check=ensure_prompt_editor_roots_ignored,
        command_name="oracle edit",
        command_argv=["cmoc", "oracle", "edit"],
        total_steps=9,
    )


def _cmoc_oracle_edit_body() -> None:
    """入力された oracle 編集指示から 2 回の Codex exec を起動する。"""
    repository = repo_root()
    current_root = work_root()

    # oracle 編集契約を含む完全 prompt の skeleton とパラメータを先に固定する。
    # {{work-root}}/oracle/doc/app_spec/sub_command/oracle_edit.md
    start_subcommand_step(2, "本命起動パラメータを構築", "build main parameter")
    time_stamp, editor_work_path, input_copy_path, complete_path = (
        reserve_prompt_editor_input(repository)
    )
    main_parameter = build_oracle_edit_main_launch_exec_parameter(
        time_stamp,
        ORIGINAL_PROMPT_PLACEHOLDER,
    )
    complete_prompt_skeleton = complete_path.read_text(encoding="utf-8")

    start_subcommand_step(3, "oracle 最終状態の指示を入力", "edit instruction")
    instruction = collect_prompt_editor_input(
        repository,
        editor_work_path,
        input_copy_path,
        complete_prompt_skeleton,
    )

    start_subcommand_step(4, "完全プロンプトを確定", "finalize complete prompt")
    finalize_complete_prompt(
        editor_work_path,
        complete_path,
        complete_prompt_skeleton,
        instruction,
    )
    start_subcommand_step(5, "本命起動前 indexing", "indexing preflight")

    def _validate_and_start_main_step() -> None:
        """indexing 後に起動前提を検証し、本命 agent call を開始する。"""
        start_subcommand_step(6, "本命起動の事前条件を確認", "validate main launch")
        _require_oracle_edit_launch_preconditions(repository, current_root)
        start_subcommand_step(7, "本命 agent call を実行", "run main agent call")

    # 本命 parameter の indexing flag により、callback は preflight 後かつ
    # subprocess 起動直前に呼ばれる。
    config = load_config(current_root)
    run_codex_exec(
        main_parameter,
        root=repository,
        config=config,
        purpose="oracle edit main",
        before_agent_call=_validate_and_start_main_step,
    )

    # 本命の正常終了後だけ、独立した新規 exec session で仕様削減を行う。
    start_subcommand_step(8, "仕様削減 agent call を実行", "run reduction agent call")
    reduction_parameter = build_oracle_edit_reduction_launch_exec_parameter(instruction)
    run_codex_exec(
        reduction_parameter,
        root=repository,
        config=config,
        purpose="oracle edit reduction",
    )
    start_subcommand_step(9, "終了状態を確定", "finalize oracle edit")


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
