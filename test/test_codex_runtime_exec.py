import json
import os
import shutil
import socket
import subprocess
import time
import tomllib
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path

import pytest
from basic.acp import AgentCallParameter, FileAccessMode, ModelClass, ReasoningEffort
from config.cmoc_config import CmocConfig
from oracle.other.cmoc_config import CodexModelSpec
from _support import (
    TEST_SLM_MODEL,
    codex_parameter,
    fake_managed_ollama_env,
    make_repo,
    run_git,
    setup_codex_home,
    write_python_executable,
)
from commons.runtime_codex import run_codex_exec


def _port_available(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        try:
            sock.bind(("127.0.0.1", port))
        except OSError:
            return False
    return True


@contextmanager
def _real_test_ollama(root: Path) -> Iterator[dict[str, str]]:
    ollama = shutil.which("ollama")
    if ollama is None:
        pytest.skip("real Ollama is not installed")
    if not _port_available(11434):
        pytest.skip("127.0.0.1:11434 is already in use")
    home = root / ".cmoc" / "local" / "test-home"
    models = home / ".cmoc" / "ollama" / "models"
    models.mkdir(parents=True)
    env = os.environ.copy()
    env.update(
        {
            "HOME": str(home),
            "OLLAMA_HOST": "127.0.0.1:11434",
            "OLLAMA_MODELS": str(models),
        }
    )
    process = subprocess.Popen(
        [ollama, "serve"],
        env=env,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True,
    )
    try:
        for _ in range(120):
            result = subprocess.run(
                [ollama, "list"], env=env, text=True, capture_output=True, timeout=5
            )
            if result.returncode == 0:
                break
            time.sleep(0.25)
        else:
            pytest.skip("real Ollama did not start")
        if subprocess.run(
            [ollama, "show", TEST_SLM_MODEL],
            env=env,
            text=True,
            capture_output=True,
            timeout=30,
        ).returncode != 0:
            pull = subprocess.run(
                [ollama, "pull", TEST_SLM_MODEL],
                env=env,
                text=True,
                capture_output=True,
                timeout=900,
            )
            if pull.returncode != 0:
                pytest.skip(f"test SLM is not available: {pull.stderr.strip()}")
        yield {"HOME": str(home)}
    finally:
        process.terminate()
        try:
            process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait(timeout=10)


def test_run_codex_exec_invokes_real_codex_with_cmoc_managed_ollama_provider(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
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
        'Return exactly this JSON object and no other text: '
        '{"result":"cmoc-real-codex-provider"}'
    )

    with _real_test_ollama(root) as ollama_env:
        for key, value in ollama_env.items():
            monkeypatch.setenv(key, value)
        monkeypatch.setenv(
            "PATH", f"{Path(real_codex).parent}:{os.environ.get('PATH', '')}"
        )
        monkeypatch.setenv("OPENAI_API_KEY", "cmoc-local-test")
        # <work-root>/oracle/doc/dev_rule/test_rule.md: this intentionally uses
        # real Codex CLI with a local SLM provider. The assertions stay on
        # cmoc-owned integration artifacts, not answer quality.
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
    profile = tomllib.loads(Path(call_log["profile_path"]).read_text())
    assert call_log["argv"][:3] == ["codex", "exec", "--skip-git-repo-check"]
    assert "--output-schema" in call_log["argv"]
    assert call_log["schema_path"] == str(result.schema_path)
    assert Path(call_log["prompt_log_path"]).read_text() == prompt
    assert result.output_path.read_text() == result.output_text
    assert isinstance(result.output_json["result"], str)
    assert call_log["model_class"] == ModelClass.MINIMUM.value
    assert profile["model"] == TEST_SLM_MODEL
    assert profile["model_provider"] == "cmoc_managed_ollama"
    assert profile["model_providers"]["cmoc_managed_ollama"] == {
        "name": "cmoc managed ollama",
        "base_url": "http://127.0.0.1:11434/v1",
        "wire_api": "responses",
    }


def test_run_codex_exec_generates_profile_and_starts_codex(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = make_repo(tmp_path)
    setup_codex_home(tmp_path, monkeypatch)
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    recorder = tmp_path / "record.json"
    write_python_executable(
        bin_dir / "codex",
        [
            "import json, os, pathlib, sys",
            "args = sys.argv[1:]",
            "output = pathlib.Path(args[args.index('--output-last-message') + 1])",
            "profile = args[args.index('--profile') + 1]",
            "home = pathlib.Path(os.environ['CODEX_HOME'])",
            "profile_path = home / f'{profile}.config.toml'",
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
            "    'profile': profile_path.read_text(),",
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
    assert record["args"][:7] == [
        "exec",
        "--skip-git-repo-check",
        "--profile",
        result.profile_name,
        "--cd",
        str(root.resolve()),
        "--json",
    ]
    assert record["cwd"] == str(root.resolve())
    assert record["stdin"] == "prompt"
    assert Path(record["stdin_fd"]).resolve() == result.prompt_log_path.resolve()
    assert 'sandbox_mode = "workspace-write"' in record["profile"]
    writable_roots = set(
        tomllib.loads(record["profile"])["sandbox_workspace_write"]["writable_roots"]
    )
    assert writable_roots == {
        str(path.resolve())
        for path in (
            root / ".gitignore",
            root / "README.md",
            root / "bin",
            root / "oracle",
            root / "src",
            root / "test",
        )
    }
    assert (root / "oracle" / "created.md").read_text() == "created\n"
    assert (root / "src" / "created.py").read_text() == "created\n"
    assert (root / ".gitignore").read_text() == "memo\n"
    assert result.output_text == "done\n"


def test_run_codex_exec_uses_local_slm_profile_without_builtin_ollama_flags(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = make_repo(tmp_path)
    setup_codex_home(tmp_path, monkeypatch)
    fake_env = fake_managed_ollama_env(root)
    for key, value in fake_env.items():
        monkeypatch.setenv(key, value)
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
            "profile = args[args.index('--profile') + 1]",
            "home = pathlib.Path(os.environ['CODEX_HOME'])",
            "profile_path = home / f'{profile}.config.toml'",
            "output.write_text('done\\n')",
            f"pathlib.Path({str(recorder)!r}).write_text(json.dumps({{",
            "    'args': args,",
            "    'profile': profile_path.read_text(),",
            "}))",
            "print(json.dumps({'type': 'turn.completed'}))",
        ],
    )
    monkeypatch.setenv("PATH", f"{bin_dir}:{fake_env['PATH']}")

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
    profile = tomllib.loads(record["profile"])
    assert "--oss" not in record["args"]
    assert "--local-provider" not in record["args"]
    assert profile["model_provider"] == "cmoc_managed_ollama"
    assert profile["model_providers"]["cmoc_managed_ollama"] == {
        "name": "cmoc managed ollama",
        "base_url": "http://127.0.0.1:11434/v1",
        "wire_api": "responses",
    }


def test_run_codex_exec_uses_parameter_cwd_independent_of_pure_oracle_read(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = make_repo(tmp_path)
    setup_codex_home(tmp_path, monkeypatch)
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    recorder = tmp_path / "record.json"
    write_python_executable(
        bin_dir / "codex",
        [
            "import json, os, pathlib, sys",
            "args = sys.argv[1:]",
            "output = pathlib.Path(args[args.index('--output-last-message') + 1])",
            "profile = args[args.index('--profile') + 1]",
            "home = pathlib.Path(os.environ['CODEX_HOME'])",
            "profile_path = home / f'{profile}.config.toml'",
            "output.write_text('done\\n')",
            f"pathlib.Path({str(recorder)!r}).write_text(json.dumps({{",
            "    'args': args,",
            "    'cwd': os.getcwd(),",
            "    'profile': profile_path.read_text(),",
            "}))",
            "print(json.dumps({'type': 'turn.completed'}))",
        ],
    )
    monkeypatch.setenv("PATH", f"{bin_dir}:{Path('/usr/bin')}")

    run_codex_exec(
        codex_parameter(FileAccessMode.PURE_ORACLE_READ),
        root=root,
        capacity_initial_sleep_sec=0,
        config=CmocConfig(),
    )

    record = json.loads(recorder.read_text())
    work_root = str(root.resolve())
    assert record["args"][record["args"].index("--cd") + 1] == work_root
    assert record["cwd"] == work_root
    profile = tomllib.loads(record["profile"])
    assert "sandbox_mode" not in profile
    assert "sandbox_workspace_write" not in profile
    assert profile["default_permissions"] == "cmoc"
    assert profile["permissions"]["cmoc"]["filesystem"] == {
        str((root / "oracle").resolve()): "read"
    }


def test_run_codex_exec_stores_schema_state_under_repo_root(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = make_repo(tmp_path)
    linked = root / ".cmoc" / "local" / "worktree" / "linked"
    linked.parent.mkdir(parents=True)
    run_git(root, "worktree", "add", "-b", "linked-exec", str(linked), "HEAD")
    setup_codex_home(tmp_path, monkeypatch)
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    recorder = tmp_path / "record.json"
    write_python_executable(
        bin_dir / "codex",
        [
            "import json, os, pathlib, sys",
            "args = sys.argv[1:]",
            "output = pathlib.Path(args[args.index('--output-last-message') + 1])",
            "output.write_text(json.dumps({'ok': True}))",
            f"pathlib.Path({str(recorder)!r}).write_text(json.dumps({{",
            "    'args': args,",
            "    'cwd': os.getcwd(),",
            "}))",
            "print(json.dumps({'type': 'turn.completed'}))",
        ],
    )
    monkeypatch.setenv("PATH", f"{bin_dir}:{Path('/usr/bin')}")
    schema_source = tmp_path / "schema.json"
    schema_source.write_text(
        json.dumps(
            {
                "type": "object",
                "required": ["ok"],
                "properties": {"ok": {"type": "boolean"}},
            }
        )
    )
    parameter = AgentCallParameter(
        ModelClass.EFFICIENCY,
        ReasoningEffort.LOW,
        FileAccessMode.REPO_WRITE,
        "prompt",
        schema_source,
    )

    result = run_codex_exec(
        parameter,
        root=root,
        cwd=linked,
        capacity_initial_sleep_sec=0,
        config=CmocConfig(),
    )

    record = json.loads(recorder.read_text())
    schema_arg = Path(record["args"][record["args"].index("--output-schema") + 1])
    assert record["cwd"] == str(linked.resolve())
    assert result.schema_path == schema_arg
    assert schema_arg.parent == root / ".cmoc" / "local" / "schema"
    assert not (linked / ".cmoc" / "local" / "schema").exists()


def test_run_codex_exec_allows_repo_local_read_from_linked_worktree(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = make_repo(tmp_path)
    linked = root / ".cmoc" / "local" / "worktree" / "linked-exec-log"
    linked.parent.mkdir(parents=True)
    run_git(root, "worktree", "add", "-b", "linked-exec-log", str(linked), "HEAD")
    setup_codex_home(tmp_path, monkeypatch)
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
            "    'cwd': os.getcwd(),",
            "}))",
            "print(json.dumps({'type': 'turn.completed'}))",
        ],
    )
    monkeypatch.setenv("PATH", f"{bin_dir}:{Path('/usr/bin')}")

    run_codex_exec(
        codex_parameter(FileAccessMode.PURE_ORACLE_READ),
        root=root,
        cwd=linked,
        extra_read_paths=[root / ".cmoc" / "local" / "report" / "review" / "report.md"],
        capacity_initial_sleep_sec=0,
        config=CmocConfig(),
    )

    record = json.loads(recorder.read_text())
    assert record["cwd"] == str(linked.resolve())
    assert record["args"][record["args"].index("--cd") + 1] == str(linked.resolve())


def test_run_codex_exec_profile_does_not_open_agents_tree(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = make_repo(tmp_path)
    setup_codex_home(tmp_path, monkeypatch)
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    write_python_executable(
        bin_dir / "codex",
        [
            "import json, os, pathlib, sys, tomllib",
            "args = sys.argv[1:]",
            "output = pathlib.Path(args[args.index('--output-last-message') + 1])",
            "profile = args[args.index('--profile') + 1]",
            "home = pathlib.Path(os.environ['CODEX_HOME'])",
            "profile_path = home / f'{profile}.config.toml'",
            "roots = tomllib.loads(profile_path.read_text())",
            "roots = roots['sandbox_workspace_write']['writable_roots']",
            "agents = pathlib.Path('.agents').resolve()",
            "assert not any(agents.is_relative_to(pathlib.Path(root)) for root in roots)",
            "output.write_text(json.dumps({'ok': True}))",
            "print(json.dumps({'type': 'turn.completed'}))",
        ],
    )
    monkeypatch.setenv("PATH", f"{bin_dir}:{Path('/usr/bin')}")

    run_codex_exec(
        codex_parameter(FileAccessMode.REPO_WRITE),
        root=root,
        capacity_initial_sleep_sec=0,
        config=CmocConfig(),
    )

    profile_path = next(tmp_path.glob("codex_home/cmoc_*.config.toml"))
    writable_roots = tomllib.loads(profile_path.read_text())["sandbox_workspace_write"][
        "writable_roots"
    ]
    agents = (root / ".agents").resolve()
    assert not any(agents.is_relative_to(Path(path)) for path in writable_roots)
