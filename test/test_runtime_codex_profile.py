"""Codex argv の model、sandbox、provider 上書き契約を検証する。

根拠:
- {{work-root}}/oracle/doc/app_spec/codex_exec_rule.md
- {{work-root}}/oracle/doc/app_spec/codex_model_provider.md
- {{work-root}}/oracle/doc/app_spec/windows_toast_notification.md
"""

import hashlib
import shlex
import subprocess
import sys
from dataclasses import replace
from pathlib import Path
from typing import cast

import pytest
from _codex_support import codex_arg_value, codex_override_config, codex_parameter
from oracle.other.cmoc_config import CodexCallConfig, CodexModelProviderConfig

import commons.runtime_codex_profile as runtime_codex_profile
from basic.acp import AgentCallParameter, FileAccessMode
from cmoc_runtime import CmocError
from commons.runtime_codex_profile import (
    build_codex_override_args,
    codex_subprocess_env,
    prepare_codex_override_args,
    prepare_schema,
    read_output_json,
)
from commons.runtime_editor_input_handoff_protocol import EDITOR_INPUT_REPOSITORY_ENV
from commons.runtime_feedback import (
    FEEDBACK_CAPABILITY_ENV,
    FEEDBACK_COLLECTOR_ENV,
    FEEDBACK_PROTOCOL_ENV,
)
from config.cmoc_config import CmocConfig

_SANDBOX_BY_MODE = {
    FileAccessMode.READONLY: "read-only",
    FileAccessMode.PURE_ORACLE_READ: "read-only",
    FileAccessMode.REPO_WRITE: "workspace-write",
    FileAccessMode.PURE_ORACLE_WRITE: "workspace-write",
    FileAccessMode.REALIZATION_WRITE: "workspace-write",
    FileAccessMode.NO_POLICY: "workspace-write",
}


@pytest.mark.parametrize(("mode", "sandbox"), _SANDBOX_BY_MODE.items())
def test_codex_overrides_use_dedicated_sandbox_argument(
    mode: FileAccessMode, sandbox: str
) -> None:
    """全 file access mode を専用 --sandbox 引数へ欠落なく変換する。"""
    config = CmocConfig()
    parameter = codex_parameter(mode, agent_call_cwd=Path.cwd())
    call_config = config.codex.agent_calls[parameter.agent_call_kind]
    args = build_codex_override_args(parameter, config)

    assert args.count("--sandbox") == 1
    assert codex_arg_value(args, "--sandbox") == sandbox
    assert codex_arg_value(args, "--ask-for-approval") == "on-request"
    assert "--approve-for-me" not in args
    assert codex_arg_value(args, "--model") == call_config.model
    parsed = codex_override_config(args)
    assert "approval_policy" not in parsed
    assert parsed["approvals_reviewer"] == "auto_review"
    assert parsed["model_reasoning_effort"] == call_config.reasoning_effort
    assert "permissions" not in parsed
    assert "default_permissions" not in parsed
    assert "sandbox_workspace_write" not in parsed
    assert "features" not in parsed
    assert parsed["model_provider"] == call_config.model_provider
    assert "model_providers" not in parsed
    assert parsed["notify"] == []
    assert parsed["tui"] == {"notifications": False}
    assert "hooks" not in parsed
    assert parsed["mcp_servers"] == {
        "cmoc_feedback": {
            "command": sys.executable,
            "args": ["-m", "commons.runtime_feedback_reporter"],
            "env_vars": [
                FEEDBACK_CAPABILITY_ENV,
                FEEDBACK_COLLECTOR_ENV,
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
    }
    assert parsed["shell_environment_policy"]["filters"] == {
        FEEDBACK_CAPABILITY_ENV: "exclude",
        FEEDBACK_COLLECTOR_ENV: "exclude",
        FEEDBACK_PROTOCOL_ENV: "exclude",
    }
    assert "--profile" not in args
    assert "-p" not in args


def test_codex_overrides_reject_unknown_file_access_mode() -> None:
    """未知 mode では sandbox を推測せず、Codex 起動前の構築段階で失敗する。"""
    parameter = replace(
        codex_parameter(FileAccessMode.READONLY, agent_call_cwd=Path.cwd()),
        file_access_mode=cast(FileAccessMode, "future_mode"),
    )

    with pytest.raises(CmocError, match="不明な FileAccessMode"):
        build_codex_override_args(parameter, CmocConfig())


def test_feedback_capability_values_are_not_written_to_codex_argv(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """MCP 起動情報は環境変数名だけを含み、call secret を argv に載せない。"""
    secret_values = (
        "capability-secret-value",
        "/tmp/private-collector.sock",
        "private-protocol-value",
    )
    for name, value in zip(
        (FEEDBACK_CAPABILITY_ENV, FEEDBACK_COLLECTOR_ENV, FEEDBACK_PROTOCOL_ENV),
        secret_values,
        strict=True,
    ):
        monkeypatch.setenv(name, value)

    args = build_codex_override_args(
        codex_parameter(FileAccessMode.READONLY, agent_call_cwd=Path.cwd()),
        CmocConfig(),
    )
    rendered = "\n".join(args)

    for value in secret_values:
        assert value not in rendered


def test_codex_overrides_enable_editor_input_handoff_only_when_selected() -> None:
    """選択済み call だけに overwrite 一つの optional MCP を注入する。"""
    parameter = replace(
        codex_parameter(FileAccessMode.REPO_WRITE, agent_call_cwd=Path.cwd()),
        enable_editor_input_handoff_mcp=True,
    )

    parsed = codex_override_config(build_codex_override_args(parameter, CmocConfig()))

    editor_server = parsed["mcp_servers"]["cmoc_editor_input"]
    assert editor_server == {
        "command": sys.executable,
        "args": ["-m", "commons.runtime_editor_input_handoff_mcp"],
        "env_vars": [EDITOR_INPUT_REPOSITORY_ENV],
        "enabled": True,
        "required": False,
        "enabled_tools": ["overwrite"],
        "disabled_tools": [],
        "startup_timeout_sec": 5,
        "tool_timeout_sec": 15,
        "default_tools_approval_mode": "approve",
        "tools": {"overwrite": {"approval_mode": "approve"}},
    }
    assert (
        parsed["shell_environment_policy"]["filters"][EDITOR_INPUT_REPOSITORY_ENV]
        == "exclude"
    )


def test_codex_subprocess_env_does_not_inherit_stale_call_context(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """親 process の別 call 用 MCP context を Codex env へ継承しない。"""
    for name, value in (
        (FEEDBACK_CAPABILITY_ENV, "stale-capability"),
        (FEEDBACK_COLLECTOR_ENV, "/tmp/stale-collector.sock"),
        (FEEDBACK_PROTOCOL_ENV, "stale-protocol"),
        (EDITOR_INPUT_REPOSITORY_ENV, "/tmp/stale-repository"),
    ):
        monkeypatch.setenv(name, value)

    environment = codex_subprocess_env(tmp_path / ".codex")

    assert all(
        name not in environment
        for name in (
            FEEDBACK_CAPABILITY_ENV,
            FEEDBACK_COLLECTOR_ENV,
            FEEDBACK_PROTOCOL_ENV,
            EDITOR_INPUT_REPOSITORY_ENV,
        )
    )


def test_prepare_codex_overrides_matches_builder_defaults() -> None:
    """callback 未指定の prepare 境界は builder の既定 argv と一致する。"""
    parameter = codex_parameter(
        FileAccessMode.REALIZATION_WRITE, agent_call_cwd=Path.cwd()
    )
    config = CmocConfig()
    assert prepare_codex_override_args(parameter, config) == (
        build_codex_override_args(parameter, config)
    )


def test_codex_overrides_pair_root_capture_with_legacy_notification() -> None:
    """root SessionStart 記録と最終 legacy callback を対で設定する。"""
    notification_command = [
        "/notify python",
        "/callback.py",
        "codex-tui-callback",
        "/state",
        "repository '; Write-Error injected",
    ]
    session_start_command = [
        "/python with space",
        "/callback.py",
        "codex-tui-session-start-hook",
        "/state",
    ]

    args = build_codex_override_args(
        codex_parameter(FileAccessMode.READONLY, agent_call_cwd=Path.cwd()),
        CmocConfig(),
        notification_command=notification_command,
        session_start_command=session_start_command,
    )

    parsed = codex_override_config(args)
    assert parsed["notify"] == notification_command
    assert parsed["tui"] == {"notifications": False}
    assert "features" not in parsed
    hook_command = shlex.join(session_start_command)
    hooks = parsed["hooks"]
    assert isinstance(hooks, dict)
    assert hooks["SessionStart"] == [
        {
            "hooks": [
                {
                    "type": "command",
                    "command": hook_command,
                    "timeout": 10,
                    "async": False,
                }
            ]
        }
    ]
    assert "Stop" not in hooks
    assert "SubagentStart" not in hooks
    assert "SubagentStop" not in hooks
    assert hooks["state"] == {
        "/<session-flags>/config.toml:session_start:0:0": {
            "enabled": True,
            "trusted_hash": (
                runtime_codex_profile._codex_session_start_hook_trusted_hash(
                    hook_command
                )
            ),
        }
    }
    assert "--dangerously-bypass-hook-trust" not in args
    assert (
        runtime_codex_profile._codex_session_start_hook_trusted_hash("echo hello")
        == "sha256:863a01826297cdbe63da6b232502523983ae7bb9376872bf40eae001e6e226d4"
    )


def test_codex_overrides_disable_unpaired_notification_callback() -> None:
    """root capture が欠ける場合は legacy callback を有効にしない。"""
    args = build_codex_override_args(
        codex_parameter(FileAccessMode.READONLY, agent_call_cwd=Path.cwd()),
        CmocConfig(),
        notification_command=["/callback.py"],
    )

    parsed = codex_override_config(args)
    assert parsed["notify"] == []
    assert "hooks" not in parsed


@pytest.mark.parametrize(
    ("version_output", "returncode", "expected"),
    [
        (b"codex-cli 0.151.0\n", 0, True),
        (b"codex-cli 0.152.0\n", 0, False),
        (b"codex-cli 0.151.0\n", 1, False),
    ],
)
def test_tui_notification_requires_exact_verified_codex_version(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    version_output: bytes,
    returncode: int,
    expected: bool,
) -> None:
    """未検証版では無絞り込み callback へ戻さず fail-closed にする。"""
    calls: list[tuple[list[str], dict[str, object]]] = []

    def fake_run(
        args: list[str], **kwargs: object
    ) -> subprocess.CompletedProcess[bytes]:
        """version probe の有限・非対話 subprocess 境界を記録する。"""
        calls.append((args, kwargs))
        return subprocess.CompletedProcess(args, returncode, stdout=version_output)

    monkeypatch.setattr(runtime_codex_profile.subprocess, "run", fake_run)
    environment = {"PATH": "/test/bin"}

    assert (
        runtime_codex_profile.codex_cli_supports_tui_notification_hooks(
            tmp_path,
            environment,
        )
        is expected
    )
    assert calls == [
        (
            ["codex", "--version"],
            {
                "cwd": tmp_path,
                "env": environment,
                "stdin": subprocess.DEVNULL,
                "stdout": subprocess.PIPE,
                "stderr": subprocess.DEVNULL,
                "timeout": 2.0,
                "check": False,
            },
        )
    ]


def test_tui_notification_version_probe_failure_is_nonfatal(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """version probe の起動失敗や timeout は callback 無効化だけに閉じる。"""

    def fail_run(*_args: object, **_kwargs: object) -> object:
        """有限時間を超えた version probe を再現する。"""
        raise subprocess.TimeoutExpired(["codex", "--version"], 2)

    monkeypatch.setattr(runtime_codex_profile.subprocess, "run", fail_run)

    assert not runtime_codex_profile.codex_cli_supports_tui_notification_hooks(
        tmp_path,
        {"PATH": "/test/bin"},
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
    assert codex_arg_value(args, "--sandbox") == "read-only"
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
        }
    }
    # {{work-root}}/oracle/doc/app_spec/codex_exec_rule.md
    # dotted override path の quoted segment は Codex CLI parser が受理しないため、
    # selected provider を inline TOML table として一度に渡す。
    assert any(
        argument.startswith('model_providers={"provider.with dot" = {')
        for argument in args
    )
    assert "permissions" not in parsed


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
    """schema の改行を変えず、source 本文の SHA256 path に保存する。"""
    source = tmp_path / "schema.json"
    source_bytes = b'{\r\n  "type": "object"\r\n}\r\n'
    source.write_bytes(source_bytes)

    stored = prepare_schema(tmp_path / "repo", source)

    assert stored is not None
    assert stored.name == f"{hashlib.sha256(source_bytes).hexdigest()}.json"
    assert stored.read_bytes() == source_bytes


def test_read_output_json_returns_none_for_invalid_utf8(
    tmp_path: Path,
) -> None:
    """不正 encoding の schema-less output を JSON failure として扱う。"""
    output = tmp_path / "output.json"
    output.write_bytes(b"\xff")

    assert read_output_json(output) is None
