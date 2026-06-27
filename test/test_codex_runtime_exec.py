import json
import subprocess
import tomllib
from pathlib import Path

import cmoc_runtime
import pytest
from basic.acp import AgentCallParameter, FileAccessMode, ModelClass, ReasoningEffort
from cmoc_runtime import CmocError, SubcommandLogger
from config.cmoc_config import CmocConfig
from _support import (
    make_repo,
    setup_codex_home,
    stub_codex_profile,
    write_python_executable,
)
from commons.runtime_codex import run_codex_exec, run_codex_tui


def _parameter(mode: FileAccessMode = FileAccessMode.READONLY) -> AgentCallParameter:
    return AgentCallParameter(
        ModelClass.EFFICIENCY,
        ReasoningEffort.LOW,
        mode,
        "prompt",
        None,
    )


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
            f"pathlib.Path({str(recorder)!r}).write_text(json.dumps({{",
            "    'args': args,",
            "    'stdin': sys.stdin.read(),",
            "    'profile': profile_path.read_text(),",
            "}))",
            "print(json.dumps({'type': 'turn.completed'}))",
        ],
    )
    monkeypatch.setenv("PATH", f"{bin_dir}:{Path('/usr/bin')}")

    result = run_codex_exec(
        _parameter(FileAccessMode.REPO_WRITE),
        root=root,
        capacity_initial_sleep_sec=0,
        config=CmocConfig(),
    )

    record = json.loads(recorder.read_text())
    assert record["args"][:4] == [
        "exec",
        "--profile",
        result.profile_name,
        "--json",
    ]
    assert record["stdin"] == "prompt"
    assert 'sandbox_mode = "workspace-write"' in record["profile"]
    writable_roots = set(
        tomllib.loads(record["profile"])["sandbox_workspace_write"]["writable_roots"]
    )
    assert str(root.resolve()) not in writable_roots
    assert str((root / "README.md").resolve()) in writable_roots
    assert str((root / "oracle").resolve()) in writable_roots
    assert result.output_text == "done\n"


def test_run_codex_exec_logs_call_before_rejecting_agents_edit(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    root = make_repo(tmp_path)
    setup_codex_home(tmp_path, monkeypatch)
    stub_codex_profile(tmp_path, monkeypatch)
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    write_python_executable(
        bin_dir / "codex",
        [
            "import json, pathlib, sys",
            "args = sys.argv[1:]",
            "output = pathlib.Path(args[args.index('--output-last-message') + 1])",
            "output.write_text(json.dumps({'ok': True}))",
            "agents = pathlib.Path('.agents')",
            "agents.mkdir(exist_ok=True)",
            "(agents / 'generated.md').write_text('changed\\n')",
            "print(json.dumps({'type': 'turn.completed'}))",
        ],
    )
    monkeypatch.setenv("PATH", f"{bin_dir}:{Path('/usr/bin')}")
    logger = SubcommandLogger(root, "test")

    with pytest.raises(CmocError, match=r"\.agents 配下を変更"):
        run_codex_exec(
            _parameter(),
            root=root,
            capacity_initial_sleep_sec=0,
            config=CmocConfig(),
            subcommand_logger=logger,
        )

    events = [json.loads(line) for line in logger.path.read_text().splitlines()]
    codex_event = next(event for event in events if event["event"] == "codex_call")
    assert codex_event["purpose"] == "codex exec"
    assert codex_event["status"] == "failed"
    assert codex_event["returncode"] == 0
    assert ".agents" in codex_event["error"]
    assert Path(codex_event["call_log_path"]).exists()
    console = capsys.readouterr().out
    assert "- purpose: `codex exec`" in console
    assert f"- call_log: `{codex_event['call_log_path']}`" in console
    assert "- returncode: `0`" in console


def test_run_codex_tui_checks_extra_read_path_before_starting_codex(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = make_repo(tmp_path)
    setup_codex_home(tmp_path, monkeypatch)

    def fail_run(*_args: object, **_kwargs: object) -> subprocess.CompletedProcess[str]:
        raise AssertionError("Codex subprocess must not start")

    monkeypatch.setattr(cmoc_runtime.subprocess, "run", fail_run)

    with pytest.raises(CmocError, match="保護領域"):
        run_codex_tui(
            _parameter(FileAccessMode.REPO_WRITE),
            root=root,
            extra_read_paths=[root / "memo" / "prompt_cmpl.md"],
            config=CmocConfig(),
        )


def test_run_codex_tui_fails_when_codex_exits_nonzero(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    root = make_repo(tmp_path)
    setup_codex_home(tmp_path, monkeypatch)
    stub_codex_profile(tmp_path, monkeypatch)
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    write_python_executable(bin_dir / "codex", ["import sys", "sys.exit(7)"])
    monkeypatch.setenv("PATH", f"{bin_dir}:{Path('/usr/bin')}")

    with pytest.raises(CmocError, match="Codex CLI/TUI 呼び出しが失敗"):
        run_codex_tui(_parameter(), root=root, config=CmocConfig())

    console = capsys.readouterr().out
    assert "- purpose: `codex tui`" in console
    assert "- returncode: `7`" in console
    call_logs = list((root / ".cmoc" / "log" / "codex").glob("*_tui_call.json"))
    assert len(call_logs) == 1
    call_log = json.loads(call_logs[0].read_text())
    assert call_log["argv"][:3] == ["codex", "--profile", call_log["profile_name"]]


@pytest.mark.parametrize("runner", ["exec", "tui"])
def test_codex_runtime_reports_missing_codex_cli(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, runner: str
) -> None:
    root = make_repo(tmp_path)
    setup_codex_home(tmp_path, monkeypatch)
    stub_codex_profile(tmp_path, monkeypatch)
    real_run = subprocess.run

    def fake_run(args: list[str], *pos: object, **kwargs: object) -> object:
        if args[:1] == ["codex"]:
            raise FileNotFoundError("codex")
        return real_run(args, *pos, **kwargs)

    monkeypatch.setattr(cmoc_runtime.subprocess, "run", fake_run)

    with pytest.raises(CmocError, match="Codex CLI が見つかりません"):
        if runner == "exec":
            run_codex_exec(
                _parameter(),
                root=root,
                capacity_initial_sleep_sec=0,
                config=CmocConfig(),
            )
        else:
            run_codex_tui(_parameter(), root=root, config=CmocConfig())
