"""Codex argv の model、sandbox、provider 上書き契約を検証する。

根拠:
- {{work-root}}/spec/app_spec/codex_common_rule.md
- {{work-root}}/spec/app_spec/codex_exec_rule.md
- {{work-root}}/spec/app_spec/codex_model_provider.md
- {{work-root}}/spec/app_spec/windows_toast_notification.md
"""

import hashlib
import json
import os
import subprocess
import sys
from dataclasses import replace
from pathlib import Path
from typing import cast

import pytest
from _codex_support import (
    codex_arg_value,
    codex_override_config,
    codex_parameter,
    setup_codex_home,
)
from oracle.other import path_model as path_model_module
from oracle.other.cmoc_config import CodexCallConfig, CodexModelProviderConfig

import commons.runtime_codex_profile as runtime_codex_profile
from basic.acp import AgentCallParameter, FileAccessMode
from cmoc_runtime import CmocError
from commons.runtime_codex_profile import (
    build_codex_override_args,
    codex_subprocess_env,
    prepare_codex_override_args,
    prepare_schema,
)
from commons.runtime_editor_input_handoff_protocol import (
    EDITOR_INPUT_REPOSITORY_ENV,
    EDITOR_INPUT_SOURCE_ENV,
)
from commons.runtime_feedback_protocol import (
    FEEDBACK_CAPABILITY_ENV,
    FEEDBACK_COLLECTOR_PORT_ENV,
    FEEDBACK_PROTOCOL_ENV,
)
from config.cmoc_config import CmocConfig, JsonTomlValue


def test_codex_overrides_use_dedicated_sandbox_argument() -> None:
    """全 file access mode を専用 --sandbox 引数へ欠落なく変換する。"""
    config = CmocConfig()
    agent_call_cwd = Path.cwd()
    for mode in FileAccessMode:
        args = build_codex_override_args(
            codex_parameter(mode, agent_call_cwd=agent_call_cwd), config
        )
        assert args.count("--sandbox") == 1, mode
        assert codex_arg_value(args, "--sandbox") == "workspace-write", mode


def test_prepare_codex_overrides_use_call_defaults_without_home_config(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """既定設定を argv だけで渡し、CODEX_HOME に設定を生成しない。"""
    codex_home = setup_codex_home(tmp_path, monkeypatch)
    config = CmocConfig()
    parameter = codex_parameter(FileAccessMode.READONLY, agent_call_cwd=tmp_path)
    call_config = config.codex.agent_calls[parameter.agent_call_kind]
    args = prepare_codex_override_args(parameter, config)

    assert args.count("--sandbox") == 1
    assert codex_arg_value(args, "--sandbox") == "workspace-write"
    assert args.count("--no-daemon") == 1
    assert codex_arg_value(args, "--ask-for-approval") == "on-request"
    assert "--approve-for-me" not in args
    assert codex_arg_value(args, "--model") == call_config.model
    parsed = codex_override_config(args)
    assert "approval_policy" not in parsed
    assert parsed["approvals_reviewer"] == "auto_review"
    assert parsed["model_reasoning_effort"] == call_config.reasoning_effort
    assert "permissions" not in parsed
    assert "default_permissions" not in parsed
    assert parsed["sandbox_workspace_write"] == {"exclude_slash_tmp": False}
    assert "sandbox_mode" not in parsed
    assert "sandbox_workspace_write.exclude_slash_tmp=false" in args
    assert "features" not in parsed
    assert parsed["model_provider"] == call_config.model_provider
    assert "model_providers" not in parsed
    assert parsed["notify"] == []
    assert parsed["tui"] == {"notifications": False}
    assert "hooks" not in parsed
    assert "--enable" not in args
    assert parsed["mcp_servers"]["cmoc_feedback"] == {
        "command": sys.executable,
        "args": ["-m", "commons.runtime_feedback_reporter"],
        "env_vars": [
            FEEDBACK_CAPABILITY_ENV,
            FEEDBACK_COLLECTOR_PORT_ENV,
            FEEDBACK_PROTOCOL_ENV,
        ],
        "enabled": True,
        "required": False,
        "enabled_tools": ["submit_observation"],
        "disabled_tools": [],
        "startup_timeout_sec": 5,
        "tool_timeout_sec": 15,
        "default_tools_approval_mode": "approve",
        "tools": {"submit_observation": {"approval_mode": "approve"}},
    }
    assert parsed["mcp_servers"]["cmoc_document_search"] == {
        "command": sys.executable,
        "args": ["-m", "commons.runtime_document_search_mcp", "{}"],
        "enabled": False,
        "required": False,
        "enabled_tools": [],
        "disabled_tools": ["search"],
    }
    assert parsed["shell_environment_policy"]["filters"] == {
        FEEDBACK_CAPABILITY_ENV: "exclude",
        FEEDBACK_COLLECTOR_PORT_ENV: "exclude",
        FEEDBACK_PROTOCOL_ENV: "exclude",
        EDITOR_INPUT_REPOSITORY_ENV: "exclude",
        EDITOR_INPUT_SOURCE_ENV: "exclude",
    }
    assert "--profile" not in args
    assert "-p" not in args
    assert not (codex_home / "config.toml").exists()
    assert not list(codex_home.glob("*.config.toml"))


def test_codex_overrides_disable_feedback_reporter_for_selected_call() -> None:
    """無効な call では外部設定にかかわらず reporter namespace を閉じる。"""
    parameter = replace(
        codex_parameter(FileAccessMode.READONLY, agent_call_cwd=Path.cwd()),
        enable_feedback_reporting=False,
    )

    parsed = codex_override_config(build_codex_override_args(parameter, CmocConfig()))
    server = parsed["mcp_servers"]["cmoc_feedback"]

    assert server["enabled"] is False
    assert server["required"] is False
    assert server["enabled_tools"] == []
    assert server["disabled_tools"] == ["submit_observation"]
    assert parsed["shell_environment_policy"]["filters"] == {
        FEEDBACK_CAPABILITY_ENV: "exclude",
        FEEDBACK_COLLECTOR_PORT_ENV: "exclude",
        FEEDBACK_PROTOCOL_ENV: "exclude",
        EDITOR_INPUT_REPOSITORY_ENV: "exclude",
        EDITOR_INPUT_SOURCE_ENV: "exclude",
    }


def test_codex_overrides_reject_unknown_file_access_mode() -> None:
    """未知 mode では sandbox を推測せず、Codex 起動前の構築段階で失敗する。"""
    parameter = replace(
        codex_parameter(FileAccessMode.READONLY, agent_call_cwd=Path.cwd()),
        file_access_mode=cast(FileAccessMode, "future_mode"),
    )

    with pytest.raises(CmocError, match="不明な FileAccessMode"):
        build_codex_override_args(parameter, CmocConfig())


def test_search_mcp_rejects_external_transport_collision(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """user 設定の同名 URL が残った実効 MCP 設定を起動前に拒否する。"""
    # Git discovery は test_basic_runtime.py に残し、transport の拒否判定を検査する。
    monkeypatch.setattr(
        path_model_module,
        "_resolve_git_worktree_roots",
        lambda _cwd: (tmp_path, tmp_path),
    )
    parameter = replace(
        codex_parameter(FileAccessMode.READONLY, agent_call_cwd=tmp_path),
        enable_document_search_mcp=True,
    )
    argv = ["codex", *build_codex_override_args(parameter, CmocConfig())]
    server = codex_override_config(argv)["mcp_servers"]["cmoc_document_search"]
    assert server["env"]["PYTHONPATH"].split(os.pathsep) == [
        str(Path(__file__).resolve().parents[1] / "src"),
        str(Path(__file__).resolve().parents[1] / "referenece/src"),
    ]
    calls: list[list[str]] = []

    def fake_run(
        args: list[str], **_kwargs: object
    ) -> subprocess.CompletedProcess[str]:
        calls.append(args)
        return subprocess.CompletedProcess(
            [],
            0,
            json.dumps(
                {
                    "name": "cmoc_document_search",
                    "enabled": True,
                    "transport": {
                        "type": "streamable_http",
                        "url": "https://example.invalid/search",
                    },
                }
            ),
            "",
        )

    monkeypatch.setattr(runtime_codex_profile.subprocess, "run", fake_run)
    with pytest.raises(CmocError, match="実効設定が call 固定値と一致しません"):
        runtime_codex_profile._verify_document_search_server(argv, cwd=tmp_path, env={})
    assert len(calls) == 1
    assert calls[0][:2] == ["codex", "--no-daemon"]
    assert calls[0][-4:] == ["mcp", "get", "cmoc_document_search", "--json"]


def test_feedback_call_context_values_are_not_written_to_codex_argv(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """MCP 起動情報は環境変数名だけを含み、call context を argv に載せない。"""
    context_values = (
        "capability-secret-value",
        "43210",
        "private-protocol-value",
    )
    for name, value in zip(
        (
            FEEDBACK_CAPABILITY_ENV,
            FEEDBACK_COLLECTOR_PORT_ENV,
            FEEDBACK_PROTOCOL_ENV,
        ),
        context_values,
        strict=True,
    ):
        monkeypatch.setenv(name, value)

    args = build_codex_override_args(
        codex_parameter(FileAccessMode.READONLY, agent_call_cwd=Path.cwd()),
        CmocConfig(),
    )
    rendered = "\n".join(args)

    for value in context_values:
        assert value not in rendered


def test_codex_overrides_enable_editor_input_handoff_only_when_selected() -> None:
    """選択済み call だけに ガイド取得と上書きの optional MCP を注入する。"""
    parameter = replace(
        codex_parameter(FileAccessMode.REPO_WRITE, agent_call_cwd=Path.cwd()),
        enable_editor_input_handoff_mcp=True,
    )

    parsed = codex_override_config(build_codex_override_args(parameter, CmocConfig()))

    editor_server = parsed["mcp_servers"]["cmoc_editor_input"]
    assert editor_server == {
        "command": sys.executable,
        "args": ["-m", "commons.runtime_editor_input_handoff_mcp"],
        "env": {"PYTHONPATH": str(Path(__file__).resolve().parents[1] / "src")},
        "env_vars": [EDITOR_INPUT_REPOSITORY_ENV, EDITOR_INPUT_SOURCE_ENV],
        "enabled": True,
        "required": False,
        "enabled_tools": ["get_handoff_guide", "overwrite"],
        "disabled_tools": [],
        "startup_timeout_sec": 5,
        "tool_timeout_sec": 15,
        "default_tools_approval_mode": "approve",
        "tools": {
            "get_handoff_guide": {"approval_mode": "approve"},
            "overwrite": {"approval_mode": "approve"},
        },
    }
    assert (
        parsed["shell_environment_policy"]["filters"][EDITOR_INPUT_REPOSITORY_ENV]
        == "exclude"
    )


def test_codex_subprocess_env_does_not_inherit_stale_call_context(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """親 process の別 call 用 MCP context を Codex env へ継承しない。"""
    for name, value in (
        (FEEDBACK_CAPABILITY_ENV, "stale-capability"),
        (FEEDBACK_COLLECTOR_PORT_ENV, "43210"),
        (FEEDBACK_PROTOCOL_ENV, "stale-protocol"),
        (EDITOR_INPUT_REPOSITORY_ENV, "/tmp/stale-repository"),
        (EDITOR_INPUT_SOURCE_ENV, "stale-source"),
    ):
        monkeypatch.setenv(name, value)

    environment = codex_subprocess_env(Path("/test/codex-home"))

    assert all(
        name not in environment
        for name in (
            FEEDBACK_CAPABILITY_ENV,
            FEEDBACK_COLLECTOR_PORT_ENV,
            FEEDBACK_PROTOCOL_ENV,
            EDITOR_INPUT_REPOSITORY_ENV,
            EDITOR_INPUT_SOURCE_ENV,
        )
    )


def test_codex_overrides_configure_direct_notification_callback() -> None:
    """固定 ID と invocation context を持つ通知専用コマンドだけを渡す。"""
    notification_command = [
        "/notify python",
        "/callback.py",
        "codex-tui-callback",
        "/state",
        "tui",
        "repository",
        "session-id",
    ]
    args = build_codex_override_args(
        codex_parameter(FileAccessMode.READONLY, agent_call_cwd=Path.cwd()),
        CmocConfig(),
        notification_command=notification_command,
    )
    parsed = codex_override_config(args)
    assert parsed["notify"] == notification_command
    assert parsed["tui"] == {"notifications": False}
    assert "hooks" not in parsed
    assert "--enable" not in args


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
            'text."日本語': 'quote"\\\n\t\x7f日本語',
            "empty": {"array": [], "table": {}},
        }
    )
    config.codex.model_providers["unused"] = CodexModelProviderConfig(
        {"secret": "must-not-be-forwarded"}
    )
    config.codex.agent_calls["test_agent_call"] = CodexCallConfig(
        provider_id, "local-model", "provider-defined-effort"
    )

    args = build_codex_override_args(
        AgentCallParameter(
            agent_call_kind="test_agent_call",
            file_access_mode=FileAccessMode.READONLY,
            prompt="prompt",
            structured_output_schema_path=None,
            agent_call_cwd=Path.cwd(),
        ),
        config,
    )

    parsed = codex_override_config(args)
    assert codex_arg_value(args, "--sandbox") == "workspace-write"
    assert codex_arg_value(args, "--model") == "local-model"
    assert parsed["model_provider"] == provider_id
    assert parsed["model_reasoning_effort"] == "provider-defined-effort"
    assert parsed["model_providers"] == {
        provider_id: {
            "base.url": "http://127.0.0.1:43123/v1",
            "enabled": True,
            "count": 2,
            "ratio": 0.5,
            "nested": ["value", {"answer": 42}],
            'text."日本語': 'quote"\\\n\t\x7f日本語',
            "empty": {"array": [], "table": {}},
        }
    }
    # {{work-root}}/spec/app_spec/codex_common_rule.md
    # dotted override path の quoted segment は Codex CLI parser が受理しないため、
    # selected provider を inline TOML table として一度に渡す。
    assert any(
        argument.startswith('model_providers={"provider.with dot" = {')
        for argument in args
    )
    assert "permissions" not in parsed


@pytest.mark.parametrize(
    "setting",
    [[None], {"nested": float("nan")}, {"nested": 2**63}],
)
def test_codex_overrides_reject_invalid_in_memory_provider_settings(
    setting: object,
) -> None:
    """設定読み込みを経由しない値も、argv 構築時に検証して拒否する。"""
    config = CmocConfig()
    config.codex.model_providers["openai"] = CodexModelProviderConfig(
        {"setting": cast(JsonTomlValue, setting)}
    )
    parameter = codex_parameter(agent_call_cwd=Path.cwd())

    with pytest.raises(CmocError, match="Codex model provider 設定が不正"):
        build_codex_override_args(parameter, config)


def test_codex_overrides_leave_bare_toml_key_segments_unquoted() -> None:
    """Codex CLI の dotted path parser が読む bare provider key を検証する。"""
    config = CmocConfig()
    provider_id = "test-local_provider"
    config.codex.model_providers[provider_id] = CodexModelProviderConfig(
        {"name": "local provider"}
    )
    config.codex.agent_calls["test_agent_call"] = CodexCallConfig(
        provider_id, "local-model", "low"
    )

    args = build_codex_override_args(
        AgentCallParameter(
            agent_call_kind="test_agent_call",
            file_access_mode=FileAccessMode.READONLY,
            prompt="prompt",
            structured_output_schema_path=None,
            agent_call_cwd=Path.cwd(),
        ),
        config,
    )

    assert 'model_providers.test-local_provider.name="local provider"' in args


def test_codex_overrides_reject_undefined_selected_provider() -> None:
    """選択 provider の定義欠落を Codex 起動前の argv 構築で失敗させる。"""
    config = CmocConfig()
    config.codex.agent_calls["test_agent_call"] = CodexCallConfig(
        "missing-provider", "local-model", "low"
    )

    with pytest.raises(CmocError, match="Codex model provider が未定義"):
        build_codex_override_args(
            AgentCallParameter(
                agent_call_kind="test_agent_call",
                file_access_mode=FileAccessMode.READONLY,
                prompt="prompt",
                structured_output_schema_path=None,
                agent_call_cwd=Path.cwd(),
            ),
            config,
        )


def test_codex_overrides_reject_missing_agent_call_setting() -> None:
    """未設定の agent call 種別を値の推測なしで起動前に拒否する。"""
    parameter = replace(
        codex_parameter(agent_call_cwd=Path.cwd()),
        agent_call_kind="missing_agent_call",
    )

    with pytest.raises(CmocError, match="Codex agent call 設定が未定義"):
        build_codex_override_args(parameter, CmocConfig())


def test_prepare_schema_preserves_source_bytes_for_hash_store(tmp_path: Path) -> None:
    """保存・検証で使う UTF-8 本文と改行を保ち、SHA256 path に保存する。"""
    source = tmp_path / "schema.json"
    source_bytes = '{\r\n  "type": "object",\r\n  "title": "日本語"\r\n}\r\n'.encode(
        "utf-8"
    )
    source.write_bytes(source_bytes)

    stored, schema_text = prepare_schema(tmp_path / "repo", source)

    assert stored.name == f"{hashlib.sha256(source_bytes).hexdigest()}.json"
    assert stored.read_bytes() == source_bytes
    assert schema_text.encode("utf-8") == source_bytes
