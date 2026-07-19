"""Codex argv の model、sandbox、provider 上書き契約を検証する。

根拠:
- {{work-root}}/oracle/doc/app_spec/codex_exec_rule.md
- {{work-root}}/oracle/doc/app_spec/cmoc_managed_ollama.md
"""

from dataclasses import replace
from pathlib import Path
from typing import cast

import pytest
from _codex_support import codex_arg_value, codex_override_config
from _ollama_support import TEST_SLM_MODEL
from oracle.other.cmoc_config import CodexModelSpec

from basic.acp import AgentCallParameter, FileAccessMode, ModelClass, ReasoningEffort
from cmoc_runtime import CmocError
from commons.runtime_codex_profile import (
    build_codex_override_args,
    prepare_codex_override_args,
)
from config.cmoc_config import CmocConfig

_SANDBOX_BY_MODE = {
    FileAccessMode.READONLY: "read-only",
    FileAccessMode.PURE_ORACLE_READ: "read-only",
    FileAccessMode.REPO_WRITE: "workspace-write",
    FileAccessMode.PURE_ORACLE_WRITE: "workspace-write",
    FileAccessMode.REALIZATION_WRITE: "workspace-write",
    FileAccessMode.NO_RULE: "workspace-write",
}


def _parameter(mode: FileAccessMode) -> AgentCallParameter:
    """指定modeの最小AgentCallParameterを作る。"""
    return AgentCallParameter(
        ModelClass.EFFICIENCY,
        ReasoningEffort.LOW,
        mode,
        "prompt",
        None,
    )


@pytest.mark.parametrize(("mode", "sandbox"), _SANDBOX_BY_MODE.items())
def test_codex_overrides_use_dedicated_sandbox_argument(
    mode: FileAccessMode, sandbox: str
) -> None:
    """全 file access mode を専用 --sandbox 引数へ欠落なく変換する。"""
    config = CmocConfig()
    args = build_codex_override_args(_parameter(mode), config)

    assert args.count("--sandbox") == 1
    assert codex_arg_value(args, "--sandbox") == sandbox
    assert args.count("--ask-for-approval") == 1
    assert codex_arg_value(args, "--ask-for-approval") == "on-request"
    assert codex_arg_value(args, "--model") == (
        config.codex.model[ModelClass.EFFICIENCY].model
    )
    parsed = codex_override_config(args)
    assert parsed["approvals_reviewer"] == "auto_review"
    assert "approval_policy" not in parsed
    assert (
        parsed["model_reasoning_effort"]
        == (config.codex.reasoning_effort[ReasoningEffort.LOW])
    )
    assert "permissions" not in parsed
    assert "default_permissions" not in parsed
    assert parsed["sandbox_workspace_write"] == {"network_access": True}
    assert parsed["features"] == {
        "network_proxy": {
            "enabled": True,
            "domains": {"127.0.0.1": "allow"},
        }
    }
    assert "--profile" not in args
    assert "-p" not in args


def test_codex_overrides_reject_unknown_file_access_mode() -> None:
    """未知 mode では sandbox を推測せず、Codex 起動前の構築段階で失敗する。"""
    parameter = replace(
        _parameter(FileAccessMode.READONLY),
        file_access_mode=cast(FileAccessMode, "future_mode"),
    )

    with pytest.raises(CmocError, match="不明な FileAccessMode"):
        build_codex_override_args(parameter, CmocConfig())


def test_prepare_codex_overrides_does_not_scan_worktree(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """通常 provider の argv は root の実在 path や内容を入力にしない。"""
    root = tmp_path / "repo"
    root.mkdir()

    def fail_scan(*_args: object, **_kwargs: object) -> object:
        """worktree走査が呼ばれた場合にテストを失敗させる。"""
        raise AssertionError("worktree scan must not be used to build Codex argv")

    monkeypatch.setattr(Path, "iterdir", fail_scan)
    monkeypatch.setattr(Path, "rglob", fail_scan)

    parameter = _parameter(FileAccessMode.REALIZATION_WRITE)
    config = CmocConfig()
    assert prepare_codex_override_args(parameter, config, root) == (
        build_codex_override_args(parameter, config)
    )


def test_codex_overrides_use_cmoc_ollama_provider_for_local_slm() -> None:
    """minimum modelがcmoc managed Ollama providerへ変換されることを検証する。"""
    config = CmocConfig()
    config.codex.model[ModelClass.MINIMUM] = CodexModelSpec("cmoc", TEST_SLM_MODEL)

    args = build_codex_override_args(
        AgentCallParameter(
            ModelClass.MINIMUM,
            ReasoningEffort.LOW,
            FileAccessMode.READONLY,
            "prompt",
            None,
        ),
        config,
    )

    parsed = codex_override_config(args)
    assert codex_arg_value(args, "--sandbox") == "read-only"
    assert codex_arg_value(args, "--model") == TEST_SLM_MODEL
    assert codex_arg_value(args, "--disable") == "multi_agent"
    assert parsed["web_search"] == "disabled"
    assert parsed["model_provider"] == "cmoc_managed_ollama"
    assert parsed["model_providers"]["cmoc_managed_ollama"] == {
        "name": "cmoc managed ollama",
        "base_url": "http://127.0.0.1:11434/v1",
        "wire_api": "responses",
    }
    assert "permissions" not in parsed
