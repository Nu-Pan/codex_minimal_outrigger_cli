import typer

from cmoc_runtime import run_cli_subcommand, run_doctor_preprocess, repo_root, sync_config


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
    """現在の repo root を cmoc 実行可能状態へ修復する。"""
    root = repo_root()
    run_doctor_preprocess(root)
    if sync_config_after_preprocess:
        # <work-root>/oracle/src/oracle/other/cmoc_config.py
        # config は人間編集対象なので、生成・同期入口を init に限定する。
        sync_config(root)
    typer.echo(f"# cmoc {command_heading}\n- repo_root: `{root}`")
