from contextlib import chdir
from dataclasses import replace
from pathlib import Path

from _cli_support import runner
from typer.testing import Result

from commons.runtime_config import load_config, write_config
from config.cmoc_config import CmocConfig

# {{work-root}}/oracle/doc/dev_rule/test_rule.md
# {{work-root}}/oracle/doc/app_spec/cmoc_managed_ollama.md
# テストは production の per-user service を使い、fake service lifecycle はテスト境界に
# 含めない。

TEST_SLM_MODEL = "qwen3:4b-instruct-2507-q4_K_M"


def bypass_managed_ollama_launch(config: CmocConfig) -> CmocConfig:
    """被テスト cmoc が外側の managed Ollama 起動保証を再実行しない設定にする。"""
    # {{work-root}}/oracle/doc/dev_rule/test_rule.md
    return replace(config, cmoc_managed_ollama_service_launch_behavior="bypass")


def run_doctor(root: Path, *, bypass_managed_ollama: bool = True) -> Result:
    """production と共有する managed Ollama service に対して root で doctor を実行する。"""
    from main import app

    if bypass_managed_ollama:
        path = root / ".cmoc" / "gt" / "ar" / "config.json"
        config = load_config(root) if path.exists() else CmocConfig()
        write_config(path, bypass_managed_ollama_launch(config))

    # {{work-root}}/oracle/doc/app_spec/cmoc_managed_ollama.md
    # production の HOME、PATH、固定 endpoint 127.0.0.1:11434 を維持する。
    # {{work-root}}/oracle/doc/app_spec/sub_command/doctor.md
    # doctor に root option はないため、cwd で対象 worktree を指定する。
    with chdir(root):
        result = runner.invoke(app, ["doctor"], catch_exceptions=False)
    assert result.exit_code == 0, result.output
    return result
