from contextlib import chdir
from pathlib import Path

from click.testing import Result

from _cli_support import runner

# {{work-root}}/oracle/doc/dev_rule/test_rule.md
# {{work-root}}/oracle/doc/app_spec/cmoc_managed_ollama.md
# Tests use the production per-user service; fake service lifecycle is not
# part of the test boundary.

TEST_SLM_MODEL = "qwen3:4b-instruct-2507-q4_K_M"


def run_doctor(root: Path) -> Result:
    """Run doctor in root against the managed Ollama service shared with production."""
    from main import app

    # {{work-root}}/oracle/doc/app_spec/cmoc_managed_ollama.md
    # Keep production HOME, PATH, and the fixed 127.0.0.1:11434 endpoint.
    # {{work-root}}/oracle/doc/app_spec/sub_command/doctor.md
    # doctor has no root option; its cwd must identify the requested worktree.
    with chdir(root):
        result = runner.invoke(app, ["doctor"], catch_exceptions=False)
    assert result.exit_code == 0, result.output
    return result
