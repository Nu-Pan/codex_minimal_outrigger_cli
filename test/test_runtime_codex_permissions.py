"""Codex sandbox argv が permission profile に依存しないことを検証する。

根拠: {{work-root}}/oracle/doc/app_spec/codex_exec_rule.md
"""

import inspect
import shutil
import subprocess
from pathlib import Path

import pytest
from _codex_support import codex_arg_value, codex_override_config

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
        ModelClass.EFFICIENCY,
        ReasoningEffort.LOW,
        mode,
        "prompt",
        None,
    )


@pytest.mark.parametrize("mode", list(FileAccessMode))
def test_codex_overrides_do_not_inject_permission_profile(
    mode: FileAccessMode,
) -> None:
    """profile の生成・選択・config 注入を全 mode で禁止する。"""
    args = build_codex_override_args(_parameter(mode), CmocConfig())
    config_values = [
        args[index + 1] for index, arg in enumerate(args[:-1]) if arg == "--config"
    ]

    assert codex_arg_value(args, "--sandbox") in {"read-only", "workspace-write"}
    assert "--profile" not in args
    assert "-p" not in args
    assert all(
        not value.startswith(
            (
                "default_permissions=",
                "permissions.",
                "sandbox_workspace_write=",
            )
        )
        for value in config_values
    )
    parsed = codex_override_config(args)
    assert "permissions" not in parsed
    assert "default_permissions" not in parsed
    assert "sandbox_workspace_write" not in parsed
    assert "features" not in parsed


def test_path_based_permission_inputs_are_absent_from_builder_api() -> None:
    """path 別の read/write 例外を argv builder へ渡す入口を残さない。"""
    build_parameters = inspect.signature(build_codex_override_args).parameters
    prepare_parameters = inspect.signature(prepare_codex_override_args).parameters

    assert tuple(build_parameters) == ("parameter", "config")
    assert tuple(prepare_parameters) == ("parameter", "config")
    for name in (
        "extra_read_paths",
        "extra_writable_paths",
        "extra_read_root",
        "allow_oracle_conflict_writes",
    ):
        assert name not in prepare_parameters


@pytest.mark.parametrize(
    "mode",
    [
        FileAccessMode.READONLY,
        FileAccessMode.PURE_ORACLE_READ,
        FileAccessMode.REALIZATION_WRITE,
        FileAccessMode.PURE_ORACLE_WRITE,
        FileAccessMode.REPO_WRITE,
        FileAccessMode.NO_RULE,
    ],
)
@pytest.mark.skipif(_CODEX_CLI is None, reason="codex CLI is not installed")
def test_sandbox_argument_is_accepted_by_codex_cli(
    tmp_path: Path, mode: FileAccessMode
) -> None:
    """生成 argv の専用 sandbox 引数を実 Codex CLI parser に通す。"""
    assert _CODEX_CLI is not None
    codex = _CODEX_CLI

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
    assert "permission" not in output.lower()
