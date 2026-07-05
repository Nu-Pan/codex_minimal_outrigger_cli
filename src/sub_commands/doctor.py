import typer

from cmoc_runtime import run_cli_subcommand, run_doctor_preprocess, repo_root


def cmoc_doctor_impl() -> None:
    """CLI runtime を通して doctor preprocess を明示実行する。"""
    run_cli_subcommand(
        _cmoc_doctor_body,
        command_name="doctor",
        command_argv=["cmoc", "doctor"],
        doctor_preprocess=False,
    )


def _cmoc_doctor_body() -> None:
    """現在の repo root を cmoc 実行可能状態へ修復する。"""
    root = repo_root()
    run_doctor_preprocess(root)
    typer.echo(f"# cmoc doctor\n- repo_root: `{root}`")
