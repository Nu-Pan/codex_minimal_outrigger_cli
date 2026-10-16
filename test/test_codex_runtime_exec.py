import json
import os
from dataclasses import replace
from pathlib import Path

import pytest
from _codex_support import (
    codex_arg_value,
    codex_override_config,
    codex_parameter,
    setup_codex_home,
)
from _command_support import write_python_executable
from oracle.other.cmoc_config import CodexCallConfig, CodexModelProviderConfig

import commons.runtime_codex_exec as exec_module
from basic.acp import FileAccessMode
from commons.runtime_codex import run_codex_exec
from commons.runtime_errors import CmocError
from config.cmoc_config import CmocConfig


def test_schema_less_output_preserves_text_and_optional_json(tmp_path):
    """省略可能な出力の境界値と本文・JSON の一貫性を CLI 起動なしで検証する。"""
    # 出力 file 以外の前提は共通なので、同じ通常 file の内容だけを差し替える。
    cases = [
        (None, "", None),
        (b"", "", None),
        (b" \r\n\r", " \n\n", None),
        (b"done\n", "done\n", None),
        (
            '{"text": "日本語\ufffd"}\r\n'.encode("utf-8"),
            '{"text": "日本語\ufffd"}\n',
            {"text": "日本語\ufffd"},
        ),
        (
            b'{"text": "\xff"}\r\n',
            '{"text": "\ufffd"}\n',
            None,
        ),
        (
            b"[" * 10_000 + b"0" + b"]" * 10_000,
            "[" * 10_000 + "0" + "]" * 10_000,
            None,
        ),
    ]
    output = tmp_path / "output.json"
    for output_bytes, expected_text, expected_json in cases:
        if output_bytes is None:
            output.unlink(missing_ok=True)
        else:
            output.write_bytes(output_bytes)
        assert exec_module._read_optional_output(output) == (
            expected_text,
            expected_json,
        )


def test_setup_codex_home_isolates_home_and_codex_home(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """共通 Codex 環境 helper が両方の home を test-root 内へ置く。"""
    codex_home = setup_codex_home(tmp_path, monkeypatch)

    assert Path(os.environ["HOME"]) == tmp_path / "home"
    assert Path(os.environ["CODEX_HOME"]) == codex_home


def test_interactive_resume_is_rejected_before_exec_preparation(tmp_path):
    """対話再開を非対話 exec や補正用 prompt に変換しない。"""
    parameter = replace(
        codex_parameter(agent_call_cwd=tmp_path),
        prompt=None,
        tui_resume_session_id="saved-session-id",
    )

    with pytest.raises(CmocError, match="対話 TUI の再開パラメータ"):
        run_codex_exec(parameter, root=tmp_path)

    assert list(tmp_path.iterdir()) == []


# {{work-root}}/oracle/doc/app_spec/codex_exec_rule.md
def _assert_codex_exec_contract(args: list[str], prompt: str) -> None:
    """Codex exec の必須 argv と prompt の stdin 渡しを検証する。"""
    assert "--json" in args
    assert "--output-last-message" in args
    assert args[-1] == "-"
    assert prompt not in args
    assert "--profile" not in args
    assert "-p" not in args
    assert args.count("--no-daemon") == 1
    assert codex_arg_value(args, "--sandbox") == "workspace-write"
    assert codex_arg_value(args, "--ask-for-approval") == "on-request"
    assert "--approve-for-me" not in args
    override = codex_override_config(args)
    assert "approval_policy" not in override
    assert override["approvals_reviewer"] == "auto_review"
    assert override["sandbox_workspace_write"] == {"exclude_slash_tmp": False}
    assert "features" not in override


def _assert_no_codex_home_config(codex_home: Path) -> None:
    """CODEX_HOME に利用者設定を生成していないことを検証する。"""
    assert not (codex_home / "config.toml").exists()
    assert not list(codex_home.glob("*.config.toml"))


# {{work-root}}/oracle/doc/app_spec/codex_model_provider.md
def test_run_codex_exec_injects_provider_overrides_and_keeps_invalid_utf8_output(
    cli_repository: Path,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capfd: pytest.CaptureFixture[str],
    nonpersistent_codex_ids: None,
) -> None:
    """provider・path policy の受け渡しと schema-less 出力の読み取りを検証する。"""
    # schema-less exec は履歴を参照しない。root 探索と Fake CLI の書き込み先だけ用意する。
    root = cli_repository
    (root / "oracle").mkdir()
    # .agents の実在 path を権限設定へ注入しない検証も同じ REPO_WRITE の起動で行う。
    agents_file = root / ".agents" / "nested" / "instructions.md"
    agents_file.parent.mkdir(parents=True)
    agents_file.write_text("agent instructions\n")
    # 既定 home の生成・子への受け渡しもこの起動で検査する。
    home = tmp_path / "home"
    codex_home = home / ".codex"
    codex_home.mkdir(parents=True)
    monkeypatch.setenv("HOME", str(home))
    monkeypatch.delenv("CODEX_HOME", raising=False)
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    recorder = tmp_path / "record.json"
    # 同じ起動で不正 UTF-8 の保存・未解析・置換文字も検査し、別の Git・log 準備を省く。
    output_bytes = b"done\n\xff"
    write_python_executable(
        bin_dir / "codex",
        [
            "import json, os, pathlib, sys",
            "args = sys.argv[1:]",
            "output = pathlib.Path(args[args.index('--output-last-message') + 1])",
            f"output.write_bytes({output_bytes!r})",
            "pathlib.Path('oracle/created.md').write_text('created\\n')",
            "pathlib.Path('src').mkdir(exist_ok=True)",
            "pathlib.Path('src/created.py').write_text('created\\n')",
            "pathlib.Path('.gitignore').write_text('memo\\n')",
            f"pathlib.Path({str(recorder)!r}).write_text(json.dumps({{",
            "    'args': args,",
            "    'cwd': os.getcwd(),",
            "    'codex_home': os.environ.get('CODEX_HOME'),",
            "    'stdin': sys.stdin.read(),",
            "    'stdin_fd': os.readlink('/proc/self/fd/0'),",
            "}))",
            "print(json.dumps({'type': 'turn.completed'}))",
            "print('private stderr', file=sys.stderr)",
        ],
    )
    monkeypatch.setenv("PATH", f"{bin_dir}:{Path('/usr/bin')}")
    config = CmocConfig()
    # provider 設定の受け渡しも同じ起動で検査し、CLI と Git の準備を重複させない。
    # 既定 provider と mode ごとの変換は test_runtime_codex_profile.py で検証する。
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
    parameter = replace(
        codex_parameter(FileAccessMode.REPO_WRITE, agent_call_cwd=root),
        agent_call_kind="test_agent_call",
        enable_feedback_reporting=False,
    )
    call_config = config.codex.agent_calls[parameter.agent_call_kind]
    feedback_flags: list[bool] = []
    original_begin_feedback_call = exec_module.begin_feedback_call

    def observe_feedback_setting(**kwargs: object) -> object:
        value = kwargs.get("enable_feedback_reporting")
        assert isinstance(value, bool)
        feedback_flags.append(value)
        return original_begin_feedback_call(**kwargs)

    monkeypatch.setattr(exec_module, "begin_feedback_call", observe_feedback_setting)

    result = run_codex_exec(
        parameter,
        root=root,
        transient_poll_interval_sec=0,
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
    assert record["codex_home"] == str(codex_home)
    assert result.codex_home == codex_home
    assert record["stdin"] == "prompt"
    assert Path(record["stdin_fd"]).resolve() == result.prompt_log_path.resolve()
    assert result.prompt_log_path.name.endswith("_prompt.md")
    assert codex_arg_value(record["args"], "--sandbox") == "workspace-write"
    override_config = codex_override_config(record["args"])
    feedback_server = override_config["mcp_servers"]["cmoc_feedback"]
    assert feedback_server["enabled"] is False
    assert feedback_server["enabled_tools"] == []
    assert feedback_server["disabled_tools"] == ["submit_observation"]
    assert feedback_flags == [False]
    assert override_config["model_reasoning_effort"] == call_config.reasoning_effort
    assert "--oss" not in record["args"]
    assert "--local-provider" not in record["args"]
    assert "--disable" not in record["args"]
    assert override_config["model_provider"] == "local.provider"
    providers = override_config["model_providers"]
    assert isinstance(providers, dict)
    assert providers["local.provider"] == {
        "name": "local provider",
        "base_url": "http://127.0.0.1:43123/v1",
        "wire_api": "responses",
    }
    assert "default_permissions" not in override_config
    assert "permissions" not in override_config
    assert all(str(agents_file.resolve()) not in arg for arg in record["args"])
    assert (root / "oracle" / "created.md").read_text() == "created\n"
    assert (root / "src" / "created.py").read_text() == "created\n"
    assert (root / ".gitignore").read_text() == "memo\n"
    _assert_no_codex_home_config(codex_home)
    assert list(result.call_log_path.parent.glob("*_call.json")) == [
        result.call_log_path
    ]
    assert result.output_path.read_bytes() == output_bytes
    assert result.output_json is None
    assert result.output_text == "done\n\ufffd"
    # 補正の検査と共用する実 process の出力捕捉を、この代表起動で保証する。
    assert result.stdout_log_path.read_text() == '{"type": "turn.completed"}\n'
    assert result.stderr_log_path.read_text() == "private stderr\n"
    captured = capfd.readouterr()
    assert captured.out == captured.err == ""
