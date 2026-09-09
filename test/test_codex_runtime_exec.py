import json
import os
from pathlib import Path

import pytest
from _codex_support import (
    codex_arg_value,
    codex_override_config,
    codex_parameter,
    setup_codex_home,
    stub_codex_overrides,
)
from _command_support import write_python_executable
from _git_support import make_repo
from oracle.other.cmoc_config import CodexCallConfig, CodexModelProviderConfig

from basic.acp import AgentCallParameter, FileAccessMode
from commons.runtime_codex import run_codex_exec
from commons.runtime_codex_profile import prepare_codex_override_args
from config.cmoc_config import CmocConfig


def test_setup_codex_home_isolates_home_and_codex_home(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """共通 Codex 環境 helper が両方の home を test-root 内へ置く。"""
    codex_home = setup_codex_home(tmp_path, monkeypatch)

    assert Path(os.environ["HOME"]) == tmp_path / "home"
    assert Path(os.environ["CODEX_HOME"]) == codex_home


# {{work-root}}/oracle/doc/app_spec/codex_exec_rule.md
def _assert_codex_exec_contract(args: list[str], prompt: str) -> None:
    """Codex exec の必須 argv と prompt の stdin 渡しを検証する。"""
    assert "--json" in args
    assert "--output-last-message" in args
    assert args[-1] == "-"
    assert prompt not in args
    assert "--profile" not in args
    assert "-p" not in args
    assert codex_arg_value(args, "--sandbox") in {"read-only", "workspace-write"}
    assert codex_arg_value(args, "--ask-for-approval") == "on-request"
    assert "--approve-for-me" not in args
    override = codex_override_config(args)
    assert "approval_policy" not in override
    assert override["approvals_reviewer"] == "auto_review"
    assert "sandbox_workspace_write" not in override
    assert "features" not in override


def _assert_no_codex_home_config(codex_home: Path) -> None:
    """CODEX_HOME に利用者設定を生成していないことを検証する。"""
    assert not (codex_home / "config.toml").exists()
    assert not list(codex_home.glob("*.config.toml"))


def test_run_codex_exec_injects_overrides_and_starts_codex(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Codex CLI の override とリポジトリ書き込み結果を検証する。"""
    root = make_repo(tmp_path)
    codex_home = setup_codex_home(tmp_path, monkeypatch)
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    recorder = tmp_path / "record.json"
    write_python_executable(
        bin_dir / "codex",
        [
            "import json, os, pathlib, sys",
            "args = sys.argv[1:]",
            "output = pathlib.Path(args[args.index('--output-last-message') + 1])",
            "output.write_text('done\\n')",
            "pathlib.Path('oracle/created.md').write_text('created\\n')",
            "pathlib.Path('src').mkdir(exist_ok=True)",
            "pathlib.Path('src/created.py').write_text('created\\n')",
            "pathlib.Path('.gitignore').write_text('memo\\n')",
            f"pathlib.Path({str(recorder)!r}).write_text(json.dumps({{",
            "    'args': args,",
            "    'cwd': os.getcwd(),",
            "    'stdin': sys.stdin.read(),",
            "    'stdin_fd': os.readlink('/proc/self/fd/0'),",
            "}))",
            "print(json.dumps({'type': 'turn.completed'}))",
        ],
    )
    monkeypatch.setenv("PATH", f"{bin_dir}:{Path('/usr/bin')}")
    config = CmocConfig()
    parameter = codex_parameter(FileAccessMode.REPO_WRITE, agent_call_cwd=root)
    call_config = config.codex.agent_calls[parameter.agent_call_kind]

    result = run_codex_exec(
        parameter,
        root=root,
        capacity_initial_sleep_sec=0,
        config=config,
    )

    record = json.loads(recorder.read_text())
    _assert_codex_exec_contract(record["args"], "prompt")
    assert record["args"][:4] == [
        "--ask-for-approval",
        "on-request",
        "--model",
        call_config.model,
    ]
    assert record["args"][record["args"].index("exec") + 1] == "--skip-git-repo-check"
    assert record["args"][record["args"].index("--cd") + 1] == str(root.resolve())
    assert record["cwd"] == str(root.resolve())
    assert record["stdin"] == "prompt"
    assert Path(record["stdin_fd"]).resolve() == result.prompt_log_path.resolve()
    assert result.prompt_log_path.name.endswith("_prompt.md")
    assert codex_arg_value(record["args"], "--sandbox") == "workspace-write"
    override_config = codex_override_config(record["args"])
    assert override_config["model_reasoning_effort"] == call_config.reasoning_effort
    assert "default_permissions" not in override_config
    assert "permissions" not in override_config
    assert (root / "oracle" / "created.md").read_text() == "created\n"
    assert (root / "src" / "created.py").read_text() == "created\n"
    assert (root / ".gitignore").read_text() == "memo\n"
    _assert_no_codex_home_config(codex_home)
    assert result.output_text == "done\n"


def test_run_codex_exec_keeps_invalid_utf8_output_as_unparsed_text(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """schema-less output の不正 UTF-8 で結果構築を中断しない。"""
    root = make_repo(tmp_path)
    setup_codex_home(tmp_path, monkeypatch)
    stub_codex_overrides(monkeypatch)
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    write_python_executable(
        bin_dir / "codex",
        [
            "import pathlib, sys",
            "args = sys.argv[1:]",
            "output = pathlib.Path(args[args.index('--output-last-message') + 1])",
            "output.write_bytes(b'\\xff')",
            'print(\'{"type": "turn.completed"}\')',
        ],
    )
    monkeypatch.setenv("PATH", f"{bin_dir}:{Path('/usr/bin')}")

    result = run_codex_exec(
        codex_parameter(agent_call_cwd=root),
        root=root,
        capacity_initial_sleep_sec=0,
        config=CmocConfig(),
    )

    assert result.output_json is None
    assert result.output_text == "\ufffd"


# {{work-root}}/oracle/doc/app_spec/codex_model_provider.md
def test_run_codex_exec_uses_generic_provider_without_builtin_local_flags(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """汎用 provider override と組み込み local provider フラグ不使用を検証する。"""
    root = make_repo(tmp_path)
    codex_home = setup_codex_home(tmp_path, monkeypatch)
    config = CmocConfig()
    config.codex.model_providers["local.provider"] = CodexModelProviderConfig(
        {
            "name": "local provider",
            "base_url": "http://127.0.0.1:43123/v1",
            "wire_api": "responses",
        }
    )
    config.codex.agent_calls["test_agent_call"] = CodexCallConfig(
        "local.provider", "local-model", "low"
    )
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    recorder = tmp_path / "record.json"
    write_python_executable(
        bin_dir / "codex",
        [
            "import json, os, pathlib, sys",
            "args = sys.argv[1:]",
            "output = pathlib.Path(args[args.index('--output-last-message') + 1])",
            "output.write_text('done\\n')",
            f"pathlib.Path({str(recorder)!r}).write_text(json.dumps({{",
            "    'args': args,",
            "}))",
            "print(json.dumps({'type': 'turn.completed'}))",
        ],
    )
    monkeypatch.setenv("PATH", f"{bin_dir}:{os.environ.get('PATH', '')}")

    run_codex_exec(
        AgentCallParameter(
            agent_call_kind="test_agent_call",
            file_access_mode=FileAccessMode.READONLY,
            prompt="prompt",
            structured_output_schema_path=None,
            agent_call_cwd=root,
        ),
        root=root,
        capacity_initial_sleep_sec=0,
        config=config,
    )

    record = json.loads(recorder.read_text())
    _assert_codex_exec_contract(record["args"], "prompt")
    override_config = codex_override_config(record["args"])
    assert "--oss" not in record["args"]
    assert "--local-provider" not in record["args"]
    assert "--disable" not in record["args"]
    assert codex_arg_value(record["args"], "--model") == "local-model"
    assert override_config["model_provider"] == "local.provider"
    providers = override_config["model_providers"]
    assert isinstance(providers, dict)
    assert providers["local.provider"] == {
        "name": "local provider",
        "base_url": "http://127.0.0.1:43123/v1",
        "wire_api": "responses",
    }
    _assert_no_codex_home_config(codex_home)


# {{work-root}}/oracle/doc/app_spec/codex_exec_rule.md
def test_prepare_codex_override_args_does_not_create_codex_home_config(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Codex override の構築時に CODEX_HOME の設定ファイルを作成しないことを検証する。"""
    codex_home = setup_codex_home(tmp_path, monkeypatch)

    override_args = prepare_codex_override_args(
        codex_parameter(agent_call_cwd=tmp_path), CmocConfig()
    )

    assert "--profile" not in override_args
    assert "-p" not in override_args
    _assert_no_codex_home_config(codex_home)
