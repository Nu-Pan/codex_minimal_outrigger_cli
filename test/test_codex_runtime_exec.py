import hashlib
import json
import os
import shutil
from pathlib import Path

import pytest
from basic.acp import AgentCallParameter, FileAccessMode, ModelClass, ReasoningEffort
from cmoc_runtime import CmocError
from config.cmoc_config import CmocConfig
from oracle.other.cmoc_config import CodexModelSpec
from _codex_support import (
    codex_arg_value,
    codex_override_config,
    codex_parameter,
    setup_codex_home,
    stub_managed_ollama_preflight,
)
from _command_support import write_python_executable
from _git_support import make_repo
from _ollama_support import TEST_SLM_MODEL
import commons.runtime_doctor as doctor_module
from commons.runtime_codex import run_codex_exec
from commons.runtime_codex_profile import prepare_codex_override_args
from commons.runtime_doctor import run_doctor_preprocess


def _prepare_production_managed_ollama(
    root: Path, config: CmocConfig
) -> None:
    """Require the real per-user managed service used by production Codex calls."""
    # {{work-root}}/oracle/doc/dev_rule/test_rule.md
    # {{work-root}}/oracle/doc/app_spec/cmoc_managed_ollama.md
    # 本番と同じサービスと永続モデルストアを検証するため、HOME、PATH、systemctl、
    # ~/.cmoc/ollama は差し替えない。
    try:
        run_doctor_preprocess(root, config)
    except (CmocError, OSError) as exc:
        pytest.skip(f"production cmoc managed ollama is unavailable: {exc}")


# {{work-root}}/oracle/doc/app_spec/codex_exec_rule.md
def _assert_codex_exec_contract(args: list[str], prompt: str) -> None:
    """Codex exec の必須 argv と prompt の stdin 渡しを検証する。"""
    assert "--json" in args
    assert "--output-last-message" in args
    assert args[-1] == "-"
    assert all(prompt not in arg for arg in args)
    assert "--profile" not in args
    assert "-p" not in args


def _assert_no_codex_home_config(codex_home: Path) -> None:
    """CODEX_HOME に利用者設定を生成していないことを検証する。"""
    assert not (codex_home / "config.toml").exists()
    assert not list(codex_home.glob("*.config.toml"))


def test_run_codex_exec_invokes_real_codex_with_cmoc_managed_ollama_provider(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Real Codex CLI と cmoc managed ollama の結合動作を検証する。"""
    real_codex = shutil.which("codex")
    if real_codex is None:
        pytest.skip("real Codex CLI is not installed")
    root = make_repo(tmp_path)
    setup_codex_home(tmp_path, monkeypatch)
    config = CmocConfig()
    config.codex.model[ModelClass.MINIMUM] = CodexModelSpec("cmoc", TEST_SLM_MODEL)
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
        '次の JSON オブジェクトだけを正確に返し、他の文字列は返さないでください: '
        '{"result":"cmoc-real-codex-provider"}'
    )

    _prepare_production_managed_ollama(root, config)
    monkeypatch.setenv(
        "PATH", f"{Path(real_codex).parent}:{os.environ.get('PATH', '')}"
    )
    monkeypatch.setenv("OPENAI_API_KEY", "cmoc-local-test")
    # {{work-root}}/oracle/doc/dev_rule/test_rule.md: ローカル SLM を provider にした
    # Real Codex CLI を意図的に使い、cmoc が所有する結合成果物だけを検証する。
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
    assert call_log["argv"][:3] == ["codex", "exec", "--skip-git-repo-check"]
    assert "--output-schema" in call_log["argv"]
    assert Path(call_log["prompt_log_path"]).read_text() == prompt
    assert call_log["model_class"] == ModelClass.MINIMUM.value
    assert codex_arg_value(call_log["argv"], "--model") == TEST_SLM_MODEL
    assert codex_arg_value(call_log["argv"], "--disable") == "multi_agent"
    assert override_config["web_search"] == "disabled"
    assert override_config["model_provider"] == "cmoc_managed_ollama"
    assert override_config["model_providers"]["cmoc_managed_ollama"] == {
        "name": "cmoc managed ollama",
        "base_url": "http://127.0.0.1:11434/v1",
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
        "exec",
        "--skip-git-repo-check",
        "--model",
        "gpt-5.6-luna",
    ]
    assert record["args"][record["args"].index("--cd") + 1] == str(root.resolve())
    assert record["cwd"] == str(root.resolve())
    assert record["stdin"] == "prompt"
    assert Path(record["stdin_fd"]).resolve() == result.prompt_log_path.resolve()
    assert "--sandbox" not in record["args"]
    override_config = codex_override_config(record["args"])
    assert override_config["model_reasoning_effort"] == "low"
    assert override_config["default_permissions"] == "cmoc"
    filesystem = override_config["permissions"]["cmoc"]["filesystem"]
    assert {
        path for path, access in filesystem.items() if access == "write"
    } == {str(root.resolve())}
    assert (root / "oracle" / "created.md").read_text() == "created\n"
    assert (root / "src" / "created.py").read_text() == "created\n"
    assert (root / ".gitignore").read_text() == "memo\n"
    _assert_no_codex_home_config(codex_home)
    assert result.output_text == "done\n"


def test_run_codex_exec_uses_local_slm_overrides_without_builtin_ollama_flags(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """local SLM 用 override と組み込み Ollama フラグの不使用を検証する。"""
    root = make_repo(tmp_path)
    codex_home = setup_codex_home(tmp_path, monkeypatch)
    stub_managed_ollama_preflight(monkeypatch)
    config = CmocConfig()
    config.codex.model[ModelClass.MINIMUM] = CodexModelSpec("cmoc", TEST_SLM_MODEL)
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
    assert codex_arg_value(record["args"], "--model") == TEST_SLM_MODEL
    assert codex_arg_value(record["args"], "--disable") == "multi_agent"
    assert override_config["web_search"] == "disabled"
    assert override_config["model_provider"] == "cmoc_managed_ollama"
    assert override_config["model_providers"]["cmoc_managed_ollama"] == {
        "name": "cmoc managed ollama",
        "base_url": "http://127.0.0.1:11434/v1",
        "wire_api": "responses",
    }
    _assert_no_codex_home_config(codex_home)


def test_prepare_local_slm_runs_managed_ollama_preflight(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """local SLM 用 override の構築前に Ollama preflight を実行することを検証する。"""
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    codex_home = tmp_path / "codex_home"
    codex_home.mkdir()
    # {{work-root}}/oracle/doc/app_spec/codex_exec_rule.md
    monkeypatch.setenv("CODEX_HOME", str(codex_home))
    config = CmocConfig()
    config.codex.model[ModelClass.MINIMUM] = CodexModelSpec("cmoc", TEST_SLM_MODEL)

    ollama_preflight_calls: list[tuple[Path, CmocConfig | None]] = []

    def record_ollama_preflight(
        actual_root: Path, actual_config: CmocConfig | None = None
    ) -> None:
        """Ollama preflight に渡された root と設定を記録する。"""
        ollama_preflight_calls.append((actual_root, actual_config))

    monkeypatch.setattr(
        doctor_module, "ensure_ollama_serves_local_slm", record_ollama_preflight
    )
    override_args = prepare_codex_override_args(
        AgentCallParameter(
            ModelClass.MINIMUM,
            ReasoningEffort.LOW,
            FileAccessMode.READONLY,
            "prompt",
            None,
        ),
        config,
        root,
    )

    assert codex_override_config(override_args)["model_provider"] == (
        "cmoc_managed_ollama"
    )
    assert ollama_preflight_calls == [(root.resolve(), config)]
    assert "--profile" not in override_args
    assert "-p" not in override_args
    _assert_no_codex_home_config(codex_home)

# {{work-root}}/oracle/doc/app_spec/codex_exec_rule.md
def test_prepare_codex_override_args_does_not_create_codex_home_config(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Codex override の構築時に CODEX_HOME の設定ファイルを作成しないことを検証する。"""
    root = make_repo(tmp_path)
    codex_home = setup_codex_home(tmp_path, monkeypatch)

    override_args = prepare_codex_override_args(
        codex_parameter(), CmocConfig(), root
    )

    assert "--profile" not in override_args
    assert "-p" not in override_args
    _assert_no_codex_home_config(codex_home)
