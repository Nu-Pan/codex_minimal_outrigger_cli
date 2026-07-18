from contextlib import chdir
from pathlib import Path

from _cli_support import runner
from typer.testing import Result

# {{work-root}}/oracle/doc/dev_rule/test_rule.md
# {{work-root}}/oracle/doc/app_spec/cmoc_managed_ollama.md
# テストは production の per-user service を使い、fake service lifecycle はテスト境界に
# 含めない。

TEST_SLM_MODEL = "qwen3:4b-instruct-2507-q4_K_M"


def run_doctor(root: Path) -> Result:
    """production と共有する managed Ollama service に対して root で doctor を実行する。"""
    from main import app

    # {{work-root}}/oracle/doc/app_spec/cmoc_managed_ollama.md
    # production の HOME、PATH、固定 endpoint 127.0.0.1:11434 を維持する。
    # {{work-root}}/oracle/doc/app_spec/sub_command/doctor.md
    # doctor に root option はないため、cwd で対象 worktree を指定する。
    with chdir(root):
        result = runner.invoke(app, ["doctor"], catch_exceptions=False)
    assert result.exit_code == 0, result.output
    return result
