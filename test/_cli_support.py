from pathlib import Path

from typer.testing import CliRunner, Result

from commons.runtime_paths import pushd

runner = CliRunner()


def run_doctor(root: Path) -> Result:
    """doctor CLI を対象 worktree の cwd で実行する。"""
    from main import app

    # {{work-root}}/oracle/doc/app_spec/sub_command/doctor.md
    # {{work-root}}/oracle/doc/app_spec/doctor_preprocess.md
    # os.chdir と CliRunner の isolation は process-global なので共有 lock 内で実行する。
    with pushd(root):
        result = runner.invoke(app, ["doctor"], catch_exceptions=False)
    assert result.exit_code == 0, result.output
    return result


def terminal_primary_report(result: Result) -> Path:
    """terminal result の primary report フルパスを取り出す。"""
    # {{work-root}}/oracle/doc/app_spec/console_and_file_log.md
    prefix = "- primary report ("
    for line in result.output.splitlines():
        if line.startswith(prefix) and "): `" in line and line.endswith("`"):
            return Path(line.split("): `", 1)[1][:-1])
    raise AssertionError(
        f"primary report is missing from terminal result:\n{result.output}"
    )
