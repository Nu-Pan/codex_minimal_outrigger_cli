from contextlib import chdir
from pathlib import Path

from typer.testing import CliRunner, Result

runner = CliRunner()


def run_doctor(root: Path) -> Result:
    """doctor CLI を対象 worktree の cwd で実行する。"""
    from main import app

    with chdir(root):
        result = runner.invoke(app, ["doctor"], catch_exceptions=False)
    assert result.exit_code == 0, result.output
    return result
