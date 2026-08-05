"""Codex sandbox argv が permission profile に依存しないことを検証する。

根拠: {{work-root}}/oracle/doc/app_spec/codex_exec_rule.md
"""

import shutil
import subprocess
from pathlib import Path

import pytest
from _codex_support import setup_codex_home

from basic.acp import AgentCallParameter, FileAccessMode, ModelClass, ReasoningEffort
from commons.runtime_codex_profile import (
    build_codex_override_args,
    prepare_codex_override_args,
)
from config.cmoc_config import CmocConfig

_CODEX_CLI = shutil.which("codex")


def _parameter(mode: FileAccessMode) -> AgentCallParameter:
    """指定modeの最小AgentCallParameterを作る。"""
    return AgentCallParameter(
        model_class=ModelClass.EFFICIENCY,
        reasoning_effort=ReasoningEffort.LOW,
        file_access_mode=mode,
        prompt="prompt",
        structured_output_schema_path=None,
        agent_call_cwd=Path.cwd(),
    )


def test_path_based_permission_inputs_are_absent_from_builder_api() -> None:
    """path 別の read/write 例外を argv builder へ渡す入口を残さない。"""
    parameter = _parameter(FileAccessMode.READONLY)
    config = CmocConfig()
    for builder in (build_codex_override_args, prepare_codex_override_args):
        for name in (
            "extra_read_paths",
            "extra_writable_paths",
            "extra_read_root",
            "allow_oracle_conflict_writes",
        ):
            with pytest.raises(TypeError, match=name):
                builder(
                    parameter,
                    config,
                    **{name: Path("path")},
                )


@pytest.mark.parametrize("mode", list(FileAccessMode))
@pytest.mark.skipif(_CODEX_CLI is None, reason="codex CLI is not installed")
def test_sandbox_argument_is_accepted_by_codex_cli(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, mode: FileAccessMode
) -> None:
    """生成 argv の専用 sandbox 引数を実 Codex CLI parser に通す。"""
    assert _CODEX_CLI is not None
    codex = _CODEX_CLI

    setup_codex_home(tmp_path, monkeypatch)
    root = tmp_path / "repo"
    root.mkdir()
    args = build_codex_override_args(_parameter(mode), CmocConfig())
    result = subprocess.run(
        [
            codex,
            *args,
            "exec",
            "--ignore-user-config",
            "--ignore-rules",
            "--ephemeral",
            "--skip-git-repo-check",
            "--output-schema",
            str(tmp_path / "missing-schema.json"),
            "--json",
            "-",
        ],
        cwd=root,
        input="probe\n",
        text=True,
        capture_output=True,
        timeout=10,
        check=False,
    )

    output = result.stdout + result.stderr
    assert result.returncode == 1
    assert "Failed to read output schema file" in output
