import json
import subprocess
import tomllib
from dataclasses import replace
from pathlib import Path

import cmoc_runtime
import pytest
from basic.acp import FileAccessMode
from cmoc_runtime import CmocError, SubcommandLogger
from config.cmoc_config import CmocConfig
from _support import (
    codex_parameter,
    make_repo,
    run_git,
    setup_codex_home,
    stub_codex_profile,
    write_python_executable,
)
from commons.runtime_codex import run_codex_tui
from commons.runtime_logging import (
    reset_current_subcommand_logger,
    set_current_subcommand_logger,
)


def test_run_codex_tui_checks_extra_read_path_before_starting_codex(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = make_repo(tmp_path)
    setup_codex_home(tmp_path, monkeypatch)

    def fail_run(*_args: object, **_kwargs: object) -> subprocess.CompletedProcess[str]:
        raise AssertionError("Codex subprocess must not start")

    monkeypatch.setattr(cmoc_runtime.subprocess, "run", fail_run)

    with pytest.raises(CmocError, match="許可領域外"):
        run_codex_tui(
            codex_parameter(FileAccessMode.REPO_WRITE),
            root=root,
            extra_read_paths=[root / "memo" / "prompt_cmpl.md"],
            config=CmocConfig(),
        )


def test_run_codex_tui_allows_complete_prompt_for_pure_oracle_read(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = make_repo(tmp_path)
    setup_codex_home(tmp_path, monkeypatch)
    prompt_path = root / ".cmoc" / "local" / "log" / "tui" / "20260101_cmpl.md"
    prompt_path.parent.mkdir(parents=True)
    prompt_path.write_text("complete prompt\n")
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    recorder = tmp_path / "record.json"
    write_python_executable(
        bin_dir / "codex",
        [
            "import json, os, pathlib, sys",
            "args = sys.argv[1:]",
            f"pathlib.Path({str(recorder)!r}).write_text(json.dumps({{",
            "    'args': args,",
            "    'cwd': os.getcwd(),",
            "}))",
        ],
    )
    monkeypatch.setenv("PATH", f"{bin_dir}:{Path('/usr/bin')}")

    schema_path = tmp_path / "schema.json"
    schema_path.write_text('{"type":"object"}\n')

    run_codex_tui(
        replace(
            codex_parameter(FileAccessMode.PURE_ORACLE_READ),
            structured_output_schema_path=schema_path,
        ),
        root=root,
        extra_read_paths=[prompt_path],
        config=CmocConfig(),
    )

    record = json.loads(recorder.read_text())
    assert record["cwd"] == str(root.resolve())
    assert record["args"][record["args"].index("--cd") + 1] == str(root.resolve())
    assert "--output-schema" not in record["args"]


def test_run_codex_tui_allows_repo_complete_prompt_from_linked_worktree(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = make_repo(tmp_path)
    setup_codex_home(tmp_path, monkeypatch)
    linked = root / ".cmoc" / "local" / "worktree" / "linked"
    linked.parent.mkdir(parents=True)
    run_git(root, "worktree", "add", "-b", "linked-tui-runtime", str(linked), "HEAD")
    prompt_path = root / ".cmoc" / "local" / "log" / "tui" / "20260101_cmpl.md"
    prompt_path.parent.mkdir(parents=True)
    prompt_path.write_text("complete prompt\n")
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    recorder = tmp_path / "record.json"
    write_python_executable(
        bin_dir / "codex",
        [
            "import json, os, pathlib, sys",
            "args = sys.argv[1:]",
            "prompt = args[-1]",
            "prompt_path = pathlib.Path(prompt.split(' を読んで')[0])",
            f"pathlib.Path({str(recorder)!r}).write_text(json.dumps({{",
            "    'args': args,",
            "    'cwd': os.getcwd(),",
            "    'prompt_text': prompt_path.read_text(),",
            "}))",
        ],
    )
    monkeypatch.setenv("PATH", f"{bin_dir}:{Path('/usr/bin')}")

    run_codex_tui(
        replace(
            codex_parameter(FileAccessMode.REPO_WRITE),
            prompt=f"{prompt_path} を読んで、その指示に従って下さい",
        ),
        root=root,
        cwd=linked,
        extra_read_paths=[prompt_path],
        config=CmocConfig(),
    )

    record = json.loads(recorder.read_text())
    assert record["cwd"] == str(linked.resolve())
    assert record["prompt_text"] == "complete prompt\n"
    assert record["args"][record["args"].index("--cd") + 1] == str(linked.resolve())
    call_log = next((root / ".cmoc" / "local" / "log" / "codex").glob("*_tui_call.json"))
    profile = tomllib.loads(
        Path(json.loads(call_log.read_text())["profile_path"]).read_text()
    )
    filesystem = profile["permissions"]["cmoc"]["filesystem"]
    assert profile["default_permissions"] == "cmoc"
    assert filesystem[str((root / ".cmoc" / "local").resolve())] == "read"
    assert filesystem[str((linked / "README.md").resolve())] == "write"
    assert filesystem[str((linked / "oracle").resolve())] == "write"
    assert "sandbox_workspace_write" not in profile


def test_run_codex_tui_logs_successful_call(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    root = make_repo(tmp_path)
    setup_codex_home(tmp_path, monkeypatch)
    stub_codex_profile(tmp_path, monkeypatch)
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    write_python_executable(bin_dir / "codex", ["import sys", "sys.exit(0)"])
    monkeypatch.setenv("PATH", f"{bin_dir}:{Path('/usr/bin')}")
    logger = SubcommandLogger(root, "test")
    token = set_current_subcommand_logger(logger)
    try:
        result = run_codex_tui(codex_parameter(), root=root, config=CmocConfig())
    finally:
        reset_current_subcommand_logger(token)

    assert result.returncode == 0
    console = capsys.readouterr().out
    assert "- Purpose: `codex tui`" in console
    assert "- Exit code: `0`" in console
    call_logs = list((root / ".cmoc" / "local" / "log" / "codex").glob("*_tui_call.json"))
    assert len(call_logs) == 1
    events = [json.loads(line) for line in logger.path.read_text().splitlines()]
    codex_events = [event for event in events if event["event"] == "codex_call"]
    assert len(codex_events) == 1
    assert codex_events[0]["status"] == "succeeded"
    assert codex_events[0]["returncode"] == 0
    assert codex_events[0]["call_log_path"] == str(call_logs[0])


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
        run_codex_tui(codex_parameter(), root=root, config=CmocConfig())

    console = capsys.readouterr().out
    assert "- Purpose: `codex tui`" in console
    assert "- Exit code: `7`" in console
    call_logs = list((root / ".cmoc" / "local" / "log" / "codex").glob("*_tui_call.json"))
    assert len(call_logs) == 1
    call_log = json.loads(call_logs[0].read_text())
    assert call_log["argv"][:3] == ["codex", "--profile", call_log["profile_name"]]
