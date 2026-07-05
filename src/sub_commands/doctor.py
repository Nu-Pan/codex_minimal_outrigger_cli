import typer

from cmoc_runtime import run_cli_subcommand, run_doctor_preprocess, repo_root


def cmoc_init_impl() -> None:
    """初回 setup と config 同期を CLI runtime から実行する。"""
    # <work-root>/oracle/src/oracle/other/cmoc_config.py
    # init は config 同期入口だが、.cmoc ignore も同じ初期 setup で保証する。
    _run_preprocess_command("init")


def cmoc_doctor_impl() -> None:
    """CLI runtime を通して doctor preprocess を明示実行する。"""
    _run_preprocess_command("doctor")


def _run_preprocess_command(command_name: str) -> None:
    run_cli_subcommand(
        _cmoc_preprocess_body,
        command_name=command_name,
        command_argv=["cmoc", command_name],
        doctor_preprocess=False,
        command_heading=command_name,
    )


def _cmoc_preprocess_body(command_heading: str) -> None:
    """現在の repo root を cmoc 実行可能状態へ修復する。"""
    root = repo_root()
    run_doctor_preprocess(root)
    typer.echo(f"# cmoc {command_heading}\n- repo_root: `{root}`")
