"""Codex argv の model、sandbox、provider 上書き契約を検証する。

根拠:
- {{work-root}}/oracle/doc/app_spec/codex_exec_rule.md
- {{work-root}}/oracle/doc/app_spec/codex_model_provider.md
"""

from dataclasses import replace
from typing import cast

import pytest
from _codex_support import codex_arg_value, codex_override_config
from oracle.other.cmoc_config import CodexModelProviderConfig, CodexModelSpec

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
    assert "sandbox_workspace_write" not in parsed
    assert "features" not in parsed
    assert "model_provider" not in parsed
    assert "model_providers" not in parsed
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


def test_prepare_codex_overrides_is_config_only() -> None:
    """prepare 境界も path や provider lifecycle を入力に持たない。"""
    parameter = _parameter(FileAccessMode.REALIZATION_WRITE)
    config = CmocConfig()
    assert prepare_codex_override_args(parameter, config) == (
        build_codex_override_args(parameter, config)
    )


def test_codex_overrides_encode_selected_generic_provider() -> None:
    """任意 ID/key と再帰値を意味を変えない TOML argv にする。"""
    config = CmocConfig()
    provider_id = "provider.with dot"
    config.codex.model_providers[provider_id] = CodexModelProviderConfig(
        {
            "base.url": "http://127.0.0.1:43123/v1",
            "enabled": True,
            "count": 2,
            "ratio": 0.5,
            "nested": ["value", {"answer": 42}],
        }
    )
    config.codex.model_providers["unused"] = CodexModelProviderConfig(
        {"secret": "must-not-be-forwarded"}
    )
    config.codex.model[ModelClass.MINIMUM] = CodexModelSpec(provider_id, "local-model")

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
    assert codex_arg_value(args, "--model") == "local-model"
    assert parsed["model_provider"] == provider_id
    assert parsed["model_providers"] == {
        provider_id: {
            "base.url": "http://127.0.0.1:43123/v1",
            "enabled": True,
            "count": 2,
            "ratio": 0.5,
            "nested": ["value", {"answer": 42}],
        }
    }
    assert "permissions" not in parsed


def test_codex_overrides_leave_bare_toml_key_segments_unquoted() -> None:
    """Codex CLI の dotted path parser が読む bare provider key を検証する。"""
    config = CmocConfig()
    provider_id = "test-local_provider"
    config.codex.model_providers[provider_id] = CodexModelProviderConfig(
        {"name": "local provider"}
    )
    config.codex.model[ModelClass.MINIMUM] = CodexModelSpec(provider_id, "local-model")

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

    assert 'model_providers.test-local_provider.name="local provider"' in args


def test_codex_overrides_reject_undefined_selected_provider() -> None:
    """選択 provider の定義欠落を Codex 起動前の argv 構築で失敗させる。"""
    config = CmocConfig()
    config.codex.model[ModelClass.MINIMUM] = CodexModelSpec(
        "missing-provider", "local-model"
    )

    with pytest.raises(CmocError, match="Codex model provider が未定義"):
        build_codex_override_args(
            AgentCallParameter(
                ModelClass.MINIMUM,
                ReasoningEffort.LOW,
                FileAccessMode.READONLY,
                "prompt",
                None,
            ),
            config,
        )
