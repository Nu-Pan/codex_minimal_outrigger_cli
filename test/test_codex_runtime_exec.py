import json
import subprocess
import tomllib
from pathlib import Path

import cmoc_runtime
import pytest
from basic.acp import AgentCallParameter, FileAccessMode, ModelClass, ReasoningEffort
from cmoc_runtime import CmocError
from config.cmoc_config import CmocConfig
from _support import (
    make_repo,
    run_git,
    setup_codex_home,
    stub_codex_profile,
    write_python_executable,
)
from commons.runtime_codex import run_codex_exec, run_codex_tui
from commons.runtime_codex_profile import (
    run_codex_subprocess,
    run_tracked_codex_subprocess,
)


def _parameter(mode: FileAccessMode = FileAccessMode.READONLY) -> AgentCallParameter:
    return AgentCallParameter(
        ModelClass.EFFICIENCY,
        ReasoningEffort.LOW,
        mode,
        "prompt",
        None,
    )


def test_tracked_codex_subprocess_records_dedicated_process_group(
    tmp_path: Path,
) -> None:
    tracking_path = tmp_path / "apply.pid"
    tracking_path.write_text("111 222\n")
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    script = bin_dir / "codex"
    write_python_executable(
        script,
        [
            "import os, pathlib, sys, time",
            "time.sleep(0.2)",
            "print(os.getpid())",
            "print(os.getpgrp())",
            "print(pathlib.Path(sys.argv[1]).read_text(), end='')",
        ],
    )

    result = run_tracked_codex_subprocess(
        [str(script), str(tracking_path)],
        tracking_path,
        text=True,
        capture_output=True,
    )

    stdout_lines = result.stdout.splitlines()
    process_id = stdout_lines[0]
    assert stdout_lines[1] == process_id
    assert stdout_lines[2] == "111 222"
    assert stdout_lines[3].startswith(f"child {process_id} ")
    assert tracking_path.read_text() == "111 222\n"


def test_run_codex_subprocess_ignores_inherited_apply_tracking_env(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    tracking_path = tmp_path / "external" / "apply.pid"
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    write_python_executable(bin_dir / "codex", ["print('ok')"])
    monkeypatch.setenv("PATH", f"{bin_dir}:{Path('/usr/bin')}")
    monkeypatch.setenv(cmoc_runtime.APPLY_PROCESS_TRACKING_ENV, str(tracking_path))

    result = run_codex_subprocess(["codex"], text=True, capture_output=True)

    assert result.stdout == "ok\n"
    assert not tracking_path.exists()


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
        _parameter(FileAccessMode.REPO_WRITE),
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
    assert writable_roots == {str((root / "oracle").resolve())}
    assert (root / "oracle" / "created.md").read_text() == "created\n"
    assert result.output_text == "done\n"


def test_run_codex_exec_recovers_file_access_violations(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = make_repo(tmp_path)
    (root / "src").mkdir()
    (root / "src" / "app.py").write_text("")
    run_git(root, "add", "src")
    run_git(root, "commit", "-m", "add src")
    setup_codex_home(tmp_path, monkeypatch)
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    counter = tmp_path / "count.txt"
    write_python_executable(
        bin_dir / "codex",
        [
            "import json, pathlib, sys",
            f"counter = pathlib.Path({str(counter)!r})",
            "count = int(counter.read_text()) if counter.exists() else 0",
            "counter.write_text(str(count + 1))",
            "args = sys.argv[1:]",
            "output = pathlib.Path(args[args.index('--output-last-message') + 1])",
            "blocked = pathlib.Path('oracle/blocked.md')",
            "if count == 0:",
            "    blocked.write_text('blocked\\n')",
            "else:",
            "    blocked.unlink(missing_ok=True)",
            "output.write_text('{}\\n')",
            "print(json.dumps({'type': 'turn.completed'}))",
        ],
    )
    monkeypatch.setenv("PATH", f"{bin_dir}:{Path('/usr/bin')}")

    run_codex_exec(
        _parameter(FileAccessMode.REALIZATION_WRITE),
        root=root,
        capacity_initial_sleep_sec=0,
        config=CmocConfig(),
    )

    assert counter.read_text() == "2"
    assert not (root / "oracle" / "blocked.md").exists()


def test_run_codex_exec_limits_pure_oracle_read_to_oracle_cwd(
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
        _parameter(FileAccessMode.PURE_ORACLE_READ),
        root=root,
        capacity_initial_sleep_sec=0,
        config=CmocConfig(),
    )

    record = json.loads(recorder.read_text())
    oracle_root = str((root / "oracle").resolve())
    assert record["args"][record["args"].index("--cd") + 1] == oracle_root
    assert record["cwd"] == oracle_root
    assert 'sandbox_mode = "read-only"' in record["profile"]
    assert "sandbox_workspace_write" not in tomllib.loads(record["profile"])


def test_run_codex_exec_stores_schema_state_under_codex_work_root(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = make_repo(tmp_path)
    linked = root / ".cmoc" / "worktrees" / "linked"
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
    assert schema_arg.parent == linked / ".cmoc" / "state" / "schema"
    assert not (root / ".cmoc" / "state" / "schema").exists()


def test_run_codex_exec_does_not_check_protected_diffs_after_call(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = make_repo(tmp_path)
    setup_codex_home(tmp_path, monkeypatch)
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

    result = run_codex_exec(_parameter(), root=root, config=CmocConfig())

    assert result.output_json == {"ok": True}


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
            _parameter(FileAccessMode.REPO_WRITE),
            root=root,
            extra_read_paths=[root / "memo" / "prompt_cmpl.md"],
            config=CmocConfig(),
        )


def test_run_codex_tui_allows_complete_prompt_for_pure_oracle_read(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = make_repo(tmp_path)
    setup_codex_home(tmp_path, monkeypatch)
    prompt_path = root / ".cmoc" / "log" / "tui" / "20260101_cmpl.md"
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

    run_codex_tui(
        _parameter(FileAccessMode.PURE_ORACLE_READ),
        root=root,
        extra_read_paths=[prompt_path],
        config=CmocConfig(),
    )

    record = json.loads(recorder.read_text())
    assert record["cwd"] == str((root / "oracle").resolve())
    assert record["args"][record["args"].index("--cd") + 1] == str(
        (root / "oracle").resolve()
    )


def test_run_codex_tui_allows_repo_complete_prompt_from_linked_worktree(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = make_repo(tmp_path)
    setup_codex_home(tmp_path, monkeypatch)
    linked = root / ".cmoc" / "worktrees" / "linked"
    linked.parent.mkdir(parents=True)
    run_git(root, "worktree", "add", "-b", "linked-tui-runtime", str(linked), "HEAD")
    prompt_path = root / ".cmoc" / "log" / "tui" / "20260101_cmpl.md"
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

    run_codex_tui(
        _parameter(FileAccessMode.REPO_WRITE),
        root=root,
        cwd=linked,
        extra_read_paths=[prompt_path],
        config=CmocConfig(),
    )

    record = json.loads(recorder.read_text())
    assert record["cwd"] == str(linked.resolve())
    assert record["args"][record["args"].index("--cd") + 1] == str(linked.resolve())
    call_log = next((root / ".cmoc" / "log" / "codex").glob("*_tui_call.json"))
    profile = tomllib.loads(
        Path(json.loads(call_log.read_text())["profile_path"]).read_text()
    )
    assert profile["sandbox_workspace_write"]["writable_roots"] == [
        str((linked / "oracle").resolve())
    ]


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
    assert "- 目的: `codex tui`" in console
    assert "- 終了コード: `7`" in console
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
