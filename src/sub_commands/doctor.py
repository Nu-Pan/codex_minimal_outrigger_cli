"""doctor preprocess を明示実行する cmoc doctor の CLI 入口を提供する。"""

# {{work-root}}/oracle/doc/app_spec/sub_command/doctor.md
# {{work-root}}/oracle/doc/dev_rule/design_rule.md

from cmoc_runtime import (
    TerminalResult,
    repo_root,
    run_cli_subcommand,
    run_doctor_preprocess,
    start_subcommand_step,
    work_root,
)


def cmoc_doctor_impl() -> None:
    """CLI runtime を通して doctor preprocess を明示実行する。"""
    run_cli_subcommand(
        _doctor_body,
        command_name="doctor",
        command_argv=["cmoc", "doctor"],
        doctor_preprocess=False,
        total_steps=1,
    )


def _doctor_body() -> TerminalResult:
    """doctor preprocess を実行し、terminal result の固有情報を返す。"""
    current_work_root = work_root()
    current_repo_root = repo_root()
    # {{work-root}}/oracle/doc/app_spec/doctor_preprocess.md
    start_subcommand_step(1, "doctor preprocess", "doctor preprocess")
    run_doctor_preprocess(current_work_root)
    return TerminalResult(details=(("repo_root", current_repo_root),))
