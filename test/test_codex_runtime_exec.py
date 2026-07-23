import hashlib
import json
import os
import shutil
from pathlib import Path

import pytest
from _codex_support import (
    codex_arg_value,
    codex_override_config,
    codex_parameter,
    configure_codex_home_for_test_local_ollama,
    setup_codex_home,
)
from _command_support import write_python_executable
from _git_support import make_repo
from _ollama_support import TEST_SLM_MODEL, local_ollama, use_test_local_ollama
from oracle.other.cmoc_config import CodexModelProviderConfig, CodexModelSpec

from basic.acp import AgentCallParameter, FileAccessMode, ModelClass, ReasoningEffort
from commons.runtime_codex import run_codex_exec
from commons.runtime_codex_profile import prepare_codex_override_args
from config.cmoc_config import CmocConfig

_REAL_CODEX = shutil.which("codex")


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
    assert all(prompt not in arg for arg in args)
    assert "--profile" not in args
    assert "-p" not in args
    assert codex_arg_value(args, "--sandbox") in {"read-only", "workspace-write"}
    assert codex_arg_value(args, "--ask-for-approval") == "on-request"
    override = codex_override_config(args)
    assert override["approvals_reviewer"] == "auto_review"
    assert "sandbox_workspace_write" not in override
    assert "features" not in override


def _assert_no_codex_home_config(codex_home: Path) -> None:
    """CODEX_HOME に利用者設定を生成していないことを検証する。"""
    assert not (codex_home / "config.toml").exists()
    assert not list(codex_home.glob("*.config.toml"))


@pytest.mark.gpu_integration
@pytest.mark.skipif(_REAL_CODEX is None, reason="real Codex CLI is not installed")
# {{work-root}}/oracle/doc/dev_rule/test_rule.md
# GPU 正常系の実測 86 秒に、cache miss と実行環境の揺らぎを加えた timeout。
@pytest.mark.timeout(600)
def test_run_codex_exec_invokes_real_codex_with_test_local_ollama_provider(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Real Codex CLI と case-local Ollama の結合動作を検証する。"""
    assert _REAL_CODEX is not None
    real_codex = _REAL_CODEX
    root = make_repo(tmp_path)
    codex_home = setup_codex_home(tmp_path, monkeypatch)
    configure_codex_home_for_test_local_ollama(codex_home)
    schema_source = tmp_path / "schema.json"
    schema_source.write_text(
        json.dumps(
            {
                "type": "object",
                "additionalProperties": False,
                "required": ["result"],
                "properties": {"result": {"type": "string"}},
            }
        )
    )
    prompt = (
        "次の JSON オブジェクトだけを正確に返し、他の文字列は返さないでください: "
        '{"result":"cmoc-real-codex-provider"}'
    )

    monkeypatch.setenv(
        "PATH", f"{Path(real_codex).parent}:{os.environ.get('PATH', '')}"
    )
    monkeypatch.setenv("OPENAI_API_KEY", "cmoc-local-test")
    monkeypatch.setenv("NO_PROXY", "127.0.0.1,localhost")
    monkeypatch.setenv("no_proxy", "127.0.0.1,localhost")
    # {{work-root}}/oracle/doc/dev_rule/test_rule.md
    # binary、process、model working set、port はこの test case の tmp_path に閉じる。
    with local_ollama(tmp_path) as ollama:
        config = use_test_local_ollama(CmocConfig(), ollama, (ModelClass.MINIMUM,))
        result = run_codex_exec(
            AgentCallParameter(
                ModelClass.MINIMUM,
                ReasoningEffort.LOW,
                FileAccessMode.READONLY,
                prompt,
                schema_source,
            ),
            root=root,
            capacity_initial_sleep_sec=0,
            max_capacity_retries=0,
            max_semantic_retries=1,
            config=config,
        )

    call_log_path = result.call_log_path
    call_log = json.loads(call_log_path.read_text())
    override_config = codex_override_config(call_log["argv"])
    _assert_codex_exec_contract(call_log["argv"], prompt)
    assert call_log["argv"][:3] == ["codex", "--ask-for-approval", "on-request"]
    exec_index = call_log["argv"].index("exec")
    assert call_log["argv"][exec_index + 1] == "--skip-git-repo-check"
    assert "--output-schema" in call_log["argv"]
    assert Path(call_log["prompt_log_path"]).read_text() == prompt
    assert call_log["model_class"] == ModelClass.MINIMUM.value
    assert codex_arg_value(call_log["argv"], "--model") == TEST_SLM_MODEL
    assert "--disable" not in call_log["argv"]
    assert override_config["model_provider"] == ollama.provider_id
    providers = override_config["model_providers"]
    assert isinstance(providers, dict)
    assert providers[ollama.provider_id] == {
        "name": "test-local Ollama",
        "base_url": f"http://{ollama.host}/v1",
        "wire_api": "responses",
    }
    # {{work-root}}/oracle/doc/app_spec/codex_exec_rule.md
    schema_arg = codex_arg_value(call_log["argv"], "--output-schema")
    assert schema_arg is not None
    output_schema_path = Path(schema_arg)
    schema_bytes = schema_source.read_bytes()
    assert output_schema_path == result.schema_path
    assert output_schema_path.parent == root / ".cmoc" / "gu" / "ar" / "schema"
    assert output_schema_path.read_bytes() == schema_bytes
    assert output_schema_path.name == f"{hashlib.sha256(schema_bytes).hexdigest()}.json"
    assert call_log["schema_path"] == str(output_schema_path)
    assert result.output_path.read_text() == result.output_text
    assert isinstance(result.output_json["result"], str)


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

    result = run_codex_exec(
        codex_parameter(FileAccessMode.REPO_WRITE),
        root=root,
        capacity_initial_sleep_sec=0,
        config=CmocConfig(),
    )

    record = json.loads(recorder.read_text())
    _assert_codex_exec_contract(record["args"], "prompt")
    assert record["args"][:4] == [
        "--ask-for-approval",
        "on-request",
        "--model",
        "gpt-5.6-luna",
    ]
    assert record["args"][record["args"].index("exec") + 1] == "--skip-git-repo-check"
    assert record["args"][record["args"].index("--cd") + 1] == str(root.resolve())
    assert record["cwd"] == str(root.resolve())
    assert record["stdin"] == "prompt"
    assert Path(record["stdin_fd"]).resolve() == result.prompt_log_path.resolve()
    assert result.prompt_log_path.name.endswith("_prompt.md")
    assert codex_arg_value(record["args"], "--sandbox") == "workspace-write"
    override_config = codex_override_config(record["args"])
    assert override_config["model_reasoning_effort"] == "low"
    assert "default_permissions" not in override_config
    assert "permissions" not in override_config
    assert (root / "oracle" / "created.md").read_text() == "created\n"
    assert (root / "src" / "created.py").read_text() == "created\n"
    assert (root / ".gitignore").read_text() == "memo\n"
    _assert_no_codex_home_config(codex_home)
    assert result.output_text == "done\n"


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
    config.codex.model[ModelClass.MINIMUM] = CodexModelSpec(
        "local.provider", TEST_SLM_MODEL
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
            ModelClass.MINIMUM,
            ReasoningEffort.LOW,
            FileAccessMode.READONLY,
            "prompt",
            None,
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
    assert codex_arg_value(record["args"], "--model") == TEST_SLM_MODEL
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

    override_args = prepare_codex_override_args(codex_parameter(), CmocConfig())

    assert "--profile" not in override_args
    assert "-p" not in override_args
    _assert_no_codex_home_config(codex_home)
