from pathlib import Path

import typer

from commons.runtime_cli import run_cli_subcommand
from commons.runtime_config import sync_config
from commons.runtime_doctor import run_doctor_preprocess
from commons.runtime_git import run_git
from commons.runtime_paths import repo_root, work_root


def run_preprocess_command(command_name: str) -> None:
    run_cli_subcommand(
        _preprocess_body,
        command_name=command_name,
        command_argv=["cmoc", command_name],
        doctor_preprocess=False,
        command_heading=command_name,
    )


def _preprocess_body(command_heading: str) -> None:
    current_work_root = work_root()
    current_repo_root = repo_root()
    # <work-root>/oracle/doc/app_spec/doctor_preprocess.md
    run_doctor_preprocess(current_work_root)
    # <work-root>/oracle/src/oracle/other/cmoc_config.py
    # config は人間編集対象だが、生成・同期は doctor が現在形へ戻す。
    sync_config(current_repo_root)
    _commit_config(current_repo_root)
    typer.echo(f"# cmoc {command_heading}\n- repo_root: `{current_repo_root}`")


def _commit_config(root: Path) -> None:
    # <work-root>/oracle/src/oracle/other/cmoc_config.py
    # config は .cmoc/local と違って repo の tracked 正本なので、広域の
    # .cmoc/ ignore があっても明示的に index へ追加する。
    run_git(["add", "-f", ".cmoc/config.json"], root)
    has_config_diff = (
        run_git(
            ["diff", "--cached", "--quiet", "--", ".cmoc/config.json"],
            root,
            check=False,
        ).returncode
        != 0
    )
    if has_config_diff:
        run_git(["commit", "-m", "cmoc config", "--", ".cmoc/config.json"], root)
