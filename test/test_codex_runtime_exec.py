import json
import os
import shutil
import socket
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path

import pytest
from basic.acp import AgentCallParameter, FileAccessMode, ModelClass, ReasoningEffort
from config.cmoc_config import CmocConfig
from oracle.other.cmoc_config import CodexModelSpec
from _support import (
    TEST_SLM_MODEL,
    codex_arg_value,
    codex_override_config,
    codex_parameter,
    fake_managed_ollama_env,
    fake_managed_systemctl_env,
    make_repo,
    run_git,
    setup_codex_home,
    write_python_executable,
)
import commons.runtime_ollama as ollama_module
from commons.runtime_codex import run_codex_exec
from commons.runtime_codex_profile import prepare_codex_override_args


def _port_available(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        try:
            sock.bind(("127.0.0.1", port))
        except OSError:
            return False
    return True


def _managed_ollama_listener_available(executable: Path) -> bool:
    """共有 listener が fake managed service の process 系列に属するか確認する。"""
    if not ollama_module._service_active():
        return False
    main_pid = ollama_module._service_main_pid()
    return (
        main_pid is not None
        and ollama_module._process_argv_uses_executable(main_pid, executable)
        and ollama_module._listener_matches_service(main_pid, executable)
    )


@contextmanager
def _real_cmoc_managed_ollama_env(
    root: Path, monkeypatch: pytest.MonkeyPatch
) -> Iterator[dict[str, str]]:
    # <work-root>/oracle/doc/dev_rule/test_rule.md and
    # <work-root>/oracle/doc/app_spec/cmoc_managed_ollama.md: real Codex
    # integration uses the normal doctor preprocess managed-service path.
    managed_env = fake_managed_systemctl_env(root)
    for key, value in managed_env.items():
        monkeypatch.setenv(key, value)
    if not _port_available(11434):
        executable = Path(managed_env["HOME"]) / ".cmoc" / "ollama" / "bin" / "ollama"
        if not _managed_ollama_listener_available(executable):
            pytest.skip("127.0.0.1:11434 is already in use by a non-managed service")
    # <work-root>/oracle/doc/app_spec/cmoc_managed_ollama.md
    # The shared fake user service is intentionally left enabled after this test.
    yield managed_env


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

    with _real_cmoc_managed_ollama_env(root, monkeypatch) as ollama_env:
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
    override_config = codex_override_config(call_log["argv"])
    assert call_log["argv"][:3] == ["codex", "exec", "--skip-git-repo-check"]
    assert "--output-schema" in call_log["argv"]
    assert Path(call_log["prompt_log_path"]).read_text() == prompt
    assert call_log["model_class"] == ModelClass.MINIMUM.value
    assert codex_arg_value(call_log["argv"], "--model") == TEST_SLM_MODEL
    assert codex_arg_value(call_log["argv"], "--disable") == "multi_agent"
    assert "--profile" not in call_log["argv"]
    assert override_config["web_search"] == "disabled"
    assert override_config["model_provider"] == "cmoc_managed_ollama"
    assert override_config["model_providers"]["cmoc_managed_ollama"] == {
        "name": "cmoc managed ollama",
        "base_url": "http://127.0.0.1:11434/v1",
        "wire_api": "responses",
    }
    assert call_log["schema_path"] == str(result.schema_path)
    assert result.output_path.read_text() == result.output_text
    assert isinstance(result.output_json["result"], str)


def test_run_codex_exec_injects_overrides_and_starts_codex(
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
    assert record["args"][:4] == [
        "exec",
        "--skip-git-repo-check",
        "--model",
        "gpt-5.6-luna",
    ]
    assert "--profile" not in record["args"]
    assert record["args"][record["args"].index("--cd") + 1] == str(root.resolve())
    assert record["cwd"] == str(root.resolve())
    assert record["stdin"] == "prompt"
    assert Path(record["stdin_fd"]).resolve() == result.prompt_log_path.resolve()
    assert codex_arg_value(record["args"], "--sandbox") == "workspace-write"
    override_config = codex_override_config(record["args"])
    assert override_config["model_reasoning_effort"] == "low"
    writable_roots = set(
        override_config["sandbox_workspace_write"]["writable_roots"]
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


def test_run_codex_exec_uses_local_slm_overrides_without_builtin_ollama_flags(
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
            "output.write_text('done\\n')",
            f"pathlib.Path({str(recorder)!r}).write_text(json.dumps({{",
            "    'args': args,",
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
    override_config = codex_override_config(record["args"])
    assert "--oss" not in record["args"]
    assert "--local-provider" not in record["args"]
    assert "--profile" not in record["args"]
    assert codex_arg_value(record["args"], "--model") == TEST_SLM_MODEL
    assert codex_arg_value(record["args"], "--disable") == "multi_agent"
    assert override_config["web_search"] == "disabled"
    assert override_config["model_provider"] == "cmoc_managed_ollama"
    assert override_config["model_providers"]["cmoc_managed_ollama"] == {
        "name": "cmoc managed ollama",
        "base_url": "http://127.0.0.1:11434/v1",
        "wire_api": "responses",
    }


def test_prepare_local_slm_overrides_run_doctor_when_port_is_missing(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    fake_env = fake_managed_ollama_env(root)
    for key, value in fake_env.items():
        monkeypatch.setenv(key, value)
    codex_home = tmp_path / "codex_home"
    codex_home.mkdir()
    config = CmocConfig()
    config.codex.model[ModelClass.MINIMUM] = CodexModelSpec("cmoc", TEST_SLM_MODEL)

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
    assert "--profile" not in override_args
    assert not list(codex_home.glob("cmoc_*.config.toml"))
    assert (
        Path(fake_env["HOME"])
        / ".config"
        / "systemd"
        / "user"
        / "cmoc-ollama.service"
    ).is_file()


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
        capacity_initial_sleep_sec=0,
        config=CmocConfig(),
    )

    record = json.loads(recorder.read_text())
    work_root = str(root.resolve())
    assert record["args"][record["args"].index("--cd") + 1] == work_root
    assert record["cwd"] == work_root
    override_config = codex_override_config(record["args"])
    assert "--sandbox" not in record["args"]
    assert "sandbox_workspace_write" not in override_config
    assert override_config["default_permissions"] == "cmoc"
    assert override_config["permissions"]["cmoc"]["filesystem"] == {
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


def test_run_codex_exec_overrides_do_not_open_agents_tree(
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
            "import json, pathlib, sys",
            "args = sys.argv[1:]",
            "output = pathlib.Path(args[args.index('--output-last-message') + 1])",
            f"pathlib.Path({str(recorder)!r}).write_text(json.dumps(args))",
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

    args = json.loads(recorder.read_text())
    writable_roots = codex_override_config(args)["sandbox_workspace_write"][
        "writable_roots"
    ]
    agents = (root / ".agents").resolve()
    assert not any(agents.is_relative_to(Path(path)) for path in writable_roots)
    assert "--profile" not in args
