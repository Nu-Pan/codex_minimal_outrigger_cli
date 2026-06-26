import tomllib

from _support import (
    AgentCallParameter,
    CmocConfig,
    FileAccessMode,
    ModelClass,
    Path,
    ReasoningEffort,
    SubcommandLogger,
    cmoc_runtime,
    json,
    make_repo,
    run_git,
    setup_codex_home,
    subprocess,
    write_python_executable,
)
from commons.runtime_codex import run_codex_exec, run_codex_tui

def test_run_codex_exec_uses_stdin_and_writes_logs(
    tmp_path: Path, monkeypatch, capsys
) -> None:
    root = make_repo(tmp_path)
    codex_home = setup_codex_home(tmp_path, monkeypatch)
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    recorder = tmp_path / "record.json"
    fake_codex = bin_dir / "codex"
    write_python_executable(
        fake_codex,
        [
            "import json, os, pathlib, sys",
            f"record = pathlib.Path({str(recorder)!r})",
            "stdin = sys.stdin.read()",
            "args = sys.argv[1:]",
            "output = pathlib.Path(args[args.index('--output-last-message') + 1])",
            "output.write_text(json.dumps({'ok': True, 'stdin': stdin}))",
            "record.write_text(json.dumps({'args': args, 'stdin': stdin, 'codex_home': os.environ.get('CODEX_HOME')}))",
            "print(json.dumps({'type': 'turn.completed'}))",
        ],
    )
    monkeypatch.setenv("PATH", f"{bin_dir}:{Path('/usr/bin')}")
    schema = tmp_path / "schema.json"
    schema.write_text(
        json.dumps(
            {
                "type": "object",
                "additionalProperties": False,
                "required": ["ok", "stdin"],
                "properties": {"ok": {"type": "boolean"}, "stdin": {"type": "string"}},
            }
        )
    )
    parameter = AgentCallParameter(
        ModelClass.EFFICIENCY,
        ReasoningEffort.LOW,
        FileAccessMode.READONLY,
        "SECRET PROMPT BODY",
        schema,
    )
    logger = SubcommandLogger(root, "test")

    result = run_codex_exec(
        parameter,
        root=root,
        capacity_initial_sleep_sec=0,
        config=CmocConfig(),
        subcommand_logger=logger,
    )

    recorded = json.loads(recorder.read_text())
    assert recorded["stdin"] == "SECRET PROMPT BODY"
    assert recorded["codex_home"] == str(codex_home)
    assert "SECRET PROMPT BODY" not in " ".join(recorded["args"])
    assert recorded["args"][:2] == ["exec", "--profile"]
    assert recorded["args"][2].startswith("cmoc_")
    assert "/" not in recorded["args"][2]
    assert "--json" in recorded["args"]
    assert "--output-schema" in recorded["args"]
    assert recorded["args"][-1] == "-"
    assert result.output_json == {"ok": True, "stdin": "SECRET PROMPT BODY"}
    assert result.call_log_path.is_file()
    assert result.stdout_log_path.read_text().strip() == '{"type": "turn.completed"}'
    assert result.stderr_log_path.read_text() == ""
    assert result.codex_home == codex_home
    assert result.profile_name == recorded["args"][2]
    assert result.profile_path.name.startswith("cmoc_")
    assert result.profile_path.suffixes == [".config", ".toml"]
    assert result.profile_path.parent == codex_home
    assert result.schema_path is not None
    assert result.schema_path.parent == root / ".cmoc" / "state" / "schema"
    call_log = json.loads(result.call_log_path.read_text())
    assert call_log["codex_home"] == str(codex_home)
    assert call_log["profile_name"] == result.profile_name
    log_events = [json.loads(line) for line in logger.path.read_text().splitlines()]
    codex_events = [event for event in log_events if event["event"] == "codex_call"]
    assert len(codex_events) == 1
    assert codex_events[0]["purpose"] == "codex exec"
    assert codex_events[0]["status"] == "succeeded"
    assert codex_events[0]["returncode"] == 0
    assert codex_events[0]["call_log_path"] == str(result.call_log_path)
    assert codex_events[0]["stdout_log_path"] == str(result.stdout_log_path)
    assert codex_events[0]["codex_home"] == str(codex_home)
    assert codex_events[0]["profile_name"] == result.profile_name
    assert codex_events[0]["elapsed_sec"] >= 0
    console = capsys.readouterr().out
    assert "# " in console
    assert "Codex CLI call" in console
    assert "- purpose: `codex exec`" in console
    assert f"- call_log: `{result.call_log_path}`" in console
    assert "- returncode: `0`" in console


def test_run_codex_exec_stores_schema_in_cwd_work_root(
    tmp_path: Path, monkeypatch
) -> None:
    root = make_repo(tmp_path)
    setup_codex_home(tmp_path, monkeypatch)
    linked = root / ".cmoc" / "worktrees" / "apply"
    linked.parent.mkdir(parents=True)
    run_git(root, "worktree", "add", "-b", "apply-test", str(linked), "HEAD")
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    recorder = tmp_path / "record.json"
    fake_codex = bin_dir / "codex"
    write_python_executable(
        fake_codex,
        [
            "import json, os, pathlib, sys",
            f"record = pathlib.Path({str(recorder)!r})",
            "args = sys.argv[1:]",
            "output = pathlib.Path(args[args.index('--output-last-message') + 1])",
            "output.write_text(json.dumps({'ok': True}))",
            "record.write_text(json.dumps({'args': args, 'cwd': os.getcwd()}))",
            "print(json.dumps({'type': 'turn.completed'}))",
        ],
    )
    monkeypatch.setenv("PATH", f"{bin_dir}:{Path('/usr/bin')}")
    schema = tmp_path / "schema.json"
    schema.write_text(
        json.dumps(
            {
                "type": "object",
                "additionalProperties": False,
                "required": ["ok"],
                "properties": {"ok": {"type": "boolean"}},
            }
        )
    )
    parameter = AgentCallParameter(
        ModelClass.EFFICIENCY,
        ReasoningEffort.LOW,
        FileAccessMode.READONLY,
        "prompt",
        schema,
    )

    result = run_codex_exec(
        parameter,
        root=root,
        cwd=linked,
        capacity_initial_sleep_sec=0,
        config=CmocConfig(),
    )

    recorded = json.loads(recorder.read_text())
    schema_arg = recorded["args"][recorded["args"].index("--output-schema") + 1]
    assert recorded["cwd"] == str(linked)
    assert result.output_json == {"ok": True}
    assert result.call_log_path.parent == root / ".cmoc" / "log" / "codex"
    assert result.schema_path is not None
    assert result.schema_path.parent == linked / ".cmoc" / "state" / "schema"
    assert schema_arg == str(result.schema_path)
    assert not (root / ".cmoc" / "state" / "schema").exists()


def test_run_codex_tui_uses_codex_command_and_prompt_argument(
    tmp_path: Path,
    monkeypatch,
    capsys,
) -> None:
    root = make_repo(tmp_path)
    codex_home = setup_codex_home(tmp_path, monkeypatch)
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    fake_codex = bin_dir / "codex"
    fake_codex.write_text("#!/bin/sh\nexit 0\n")
    fake_codex.chmod(0o755)
    monkeypatch.setenv("PATH", f"{bin_dir}:{Path('/usr/bin')}")
    recorded = {}

    def fake_run(argv, **kwargs):
        recorded.update({"argv": argv, "kwargs": kwargs})
        return subprocess.CompletedProcess(argv, 0)

    monkeypatch.setattr(cmoc_runtime.subprocess, "run", fake_run)
    parameter = AgentCallParameter(
        ModelClass.MAINSTREAM,
        ReasoningEffort.MEDIUM,
        FileAccessMode.REPO_WRITE,
        "TUI PROMPT BODY",
        None,
    )
    logger = SubcommandLogger(root, "test")
    token = cmoc_runtime.set_current_subcommand_logger(logger)

    try:
        prompt_file = root / ".cmoc" / "log" / "tui" / "prompt_cmpl.md"
        result = run_codex_tui(
            parameter,
            root=root,
            purpose="tui codex",
            extra_read_paths=[prompt_file],
            config=CmocConfig(),
        )
    finally:
        cmoc_runtime.reset_current_subcommand_logger(token)

    assert recorded["kwargs"]["cwd"] == root
    assert recorded["kwargs"]["env"]["CODEX_HOME"] == str(codex_home)
    assert "capture_output" not in recorded["kwargs"]
    assert "stdout" not in recorded["kwargs"]
    assert "stderr" not in recorded["kwargs"]
    assert recorded["argv"][0] == "codex"
    assert recorded["argv"][1] == "--profile"
    assert recorded["argv"][2].startswith("cmoc_")
    assert "exec" not in recorded["argv"]
    assert recorded["argv"][-1] == "TUI PROMPT BODY"
    profiles = list(codex_home.glob("cmoc_*.config.toml"))
    assert len(profiles) == 1
    workspace = tomllib.loads(profiles[0].read_text())["sandbox_workspace_write"]
    assert workspace["writable_roots"] == [str(root)]
    assert workspace["read_only_paths"] == [
        str(root / "memo"),
        str(root / ".agents"),
        str(prompt_file),
    ]
    call_logs = list((root / ".cmoc" / "log" / "codex").glob("*_tui_call.json"))
    assert len(call_logs) == 1
    assert json.loads(call_logs[0].read_text())["argv"] == [
        "codex",
        "--profile",
        recorded["argv"][2],
        "TUI PROMPT BODY",
    ]
    log_events = [json.loads(line) for line in logger.path.read_text().splitlines()]
    codex_events = [event for event in log_events if event["event"] == "codex_call"]
    assert len(codex_events) == 1
    assert codex_events[0]["purpose"] == "tui codex"
    assert codex_events[0]["status"] == "succeeded"
    assert codex_events[0]["returncode"] == 0
    assert codex_events[0]["call_log_path"] == str(call_logs[0])
    console = capsys.readouterr().out
    assert "Codex CLI call" in console
    assert "- purpose: `tui codex`" in console
    assert f"- call_log: `{call_logs[0]}`" in console
    assert "- returncode: `0`" in console
    assert result.returncode == 0
    assert result.stdout == ""
    assert result.stderr == ""

def test_run_codex_exec_loads_repo_config_json(tmp_path: Path, monkeypatch) -> None:
    root = make_repo(tmp_path)
    setup_codex_home(tmp_path, monkeypatch)
    config = cmoc_runtime.config_to_dict(cmoc_runtime.sync_config(root))
    config["codex"]["model"]["efficiency"] = "CUSTOM-EFFICIENCY"
    config["codex"]["reasoning_effort"]["low"] = "minimal"
    (root / ".cmoc" / "config.json").write_text(json.dumps(config, indent=2) + "\n")
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    fake_codex = bin_dir / "codex"
    write_python_executable(
        fake_codex,
        [
            "import json, pathlib, sys",
            "args = sys.argv[1:]",
            "output = pathlib.Path(args[args.index('--output-last-message') + 1])",
            "output.write_text('done\\n')",
            "print(json.dumps({'type': 'turn.completed'}))",
        ],
    )
    monkeypatch.setenv("PATH", f"{bin_dir}:{Path('/usr/bin')}")
    parameter = AgentCallParameter(
        ModelClass.EFFICIENCY,
        ReasoningEffort.LOW,
        FileAccessMode.READONLY,
        "prompt",
        None,
    )

    result = run_codex_exec(parameter, root=root, capacity_initial_sleep_sec=0)

    profile = result.profile_path.read_text()
    assert 'model = "CUSTOM-EFFICIENCY"' in profile
    assert 'reasoning_effort = "minimal"' in profile
