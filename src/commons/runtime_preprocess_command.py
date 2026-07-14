import typer

from commons.runtime_cli import run_cli_subcommand, start_subcommand_step
from commons.runtime_doctor import run_doctor_preprocess
from commons.runtime_paths import repo_root, work_root


def run_preprocess_command(command_name: str) -> None:
    run_cli_subcommand(
        _preprocess_body,
        command_name=command_name,
        command_argv=["cmoc", command_name],
        doctor_preprocess=False,
        command_heading=command_name,
        total_steps=1,
    )


def _preprocess_body(command_heading: str) -> None:
    current_work_root = work_root()
    current_repo_root = repo_root()
    # {{work-root}}/oracle/doc/app_spec/doctor_preprocess.md
    start_subcommand_step(1, "doctor preprocess", "doctor preprocess")
    run_doctor_preprocess(current_work_root)
    typer.echo(f"# cmoc {command_heading}\n- repo_root: `{current_repo_root}`")
