import json
import shutil
import tomllib
from pathlib import Path

import pytest
from basic.acp import AgentCallParameter, FileAccessMode, ModelClass, ReasoningEffort
from config.cmoc_config import CmocConfig
from oracle.other.cmoc_config import CodexModelSpec
from commons.runtime_errors import CmocError
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


def test_run_codex_exec_invokes_real_codex_with_cmoc_managed_ollama_provider(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    real_codex = shutil.which("codex")
    if real_codex is None:
        pytest.skip("real Codex CLI is not installed")
    root = make_repo(tmp_path)
    setup_codex_home(tmp_path, monkeypatch)
    fake_env = fake_managed_ollama_env(root)
    for key, value in fake_env.items():
        monkeypatch.setenv(key, value)
    monkeypatch.setenv(
        "PATH",
        f"{root / '.cmoc' / 'local' / 'fake-bin'}:{Path(real_codex).parent}:/usr/bin",
    )
    monkeypatch.setenv("OPENAI_API_KEY", "cmoc-local-test")
    config = CmocConfig()
    config.codex.model[ModelClass.MINIMUM] = CodexModelSpec("cmoc", TEST_SLM_MODEL)

    # <work-root>/oracle/doc/dev_rule/test_rule.md: this intentionally uses the
    # real Codex CLI. The provider is controlled because LLM/provider quality is
    # outside cmoc's test goal.
    with pytest.raises(CmocError):
        run_codex_exec(
            AgentCallParameter(
                ModelClass.MINIMUM,
                ReasoningEffort.LOW,
                FileAccessMode.READONLY,
                "Reply with exactly cmoc-real-codex-provider.",
                None,
            ),
            root=root,
            capacity_initial_sleep_sec=0,
            max_capacity_retries=0,
            config=config,
        )

    call_log_path = next(
        (root / ".cmoc" / "local" / "log" / "codex").glob("*_call.json")
    )
    call_log = json.loads(call_log_path.read_text())
    profile = tomllib.loads(Path(call_log["profile_path"]).read_text())
    assert call_log["argv"][:3] == ["codex", "exec", "--skip-git-repo-check"]
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
        str((root / name).resolve())
        for name in ("bin", ".gitignore", "README.md", "oracle", "src", "test")
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
    assert 'sandbox_mode = "workspace-write"' in record["profile"]
    profile = tomllib.loads(record["profile"])
    assert profile["sandbox_workspace_write"]["writable_roots"] == []


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
