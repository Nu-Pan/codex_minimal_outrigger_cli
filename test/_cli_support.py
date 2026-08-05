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
