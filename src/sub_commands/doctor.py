from pathlib import Path

import typer

from cmoc_runtime import (
    run_cli_subcommand,
    run_doctor_preprocess,
    run_git,
    repo_root,
    sync_config,
    work_root,
)


def cmoc_init_impl() -> None:
    """初回 setup と config 同期を CLI runtime から実行する。"""
    _run_preprocess_command("init", sync_config_after_preprocess=True)


def cmoc_doctor_impl() -> None:
    """CLI runtime を通して doctor preprocess を明示実行する。"""
    _run_preprocess_command("doctor")


def _run_preprocess_command(
    command_name: str, *, sync_config_after_preprocess: bool = False
) -> None:
    run_cli_subcommand(
        _cmoc_preprocess_body,
        command_name=command_name,
        command_argv=["cmoc", command_name],
        doctor_preprocess=False,
        command_heading=command_name,
        sync_config_after_preprocess=sync_config_after_preprocess,
    )


def _cmoc_preprocess_body(
    command_heading: str, sync_config_after_preprocess: bool
) -> None:
    """現在の work root を cmoc 実行可能状態へ修復する。"""
    current_root = work_root()
    root = repo_root()
    # <work-root>/oracle/doc/app_spec/doctor_preprocess.md
    run_doctor_preprocess(current_root)
    if sync_config_after_preprocess:
        # <work-root>/oracle/src/oracle/other/cmoc_config.py
        # config は人間編集対象なので、生成・同期入口を init に限定する。
        sync_config(root)
        _commit_init_config(root)
    typer.echo(f"# cmoc {command_heading}\n- repo_root: `{root}`")


def _commit_init_config(root: Path) -> None:
    run_git(["add", ".cmoc/config.json"], root)
    has_config_diff = (
        run_git(
            ["diff", "--cached", "--quiet", "--", ".cmoc/config.json"],
            root,
            check=False,
        ).returncode
        != 0
    )
    if has_config_diff:
        run_git(["commit", "-m", "cmoc init config", "--", ".cmoc/config.json"], root)
