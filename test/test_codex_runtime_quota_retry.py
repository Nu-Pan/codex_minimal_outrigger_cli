import json
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import cmoc_runtime
import commons.runtime_codex_exec as runtime_codex_exec
from basic.acp import AgentCallParameter, FileAccessMode, ModelClass, ReasoningEffort
from cmoc_runtime import SubcommandLogger
from config.cmoc_config import CmocConfig
import pytest

from _support import (
    make_repo,
    setup_codex_home,
    write_python_executable,
)
from commons.runtime_codex import run_codex_exec


def prompt_log_text(path: str) -> str:
    return json.loads(Path(path).read_text())["prompt"]


def test_run_codex_exec_polls_and_resumes_after_quota(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    root = make_repo(tmp_path)
    codex_home = setup_codex_home(tmp_path, monkeypatch)
    monkeypatch.setattr(cmoc_runtime.time, "sleep", lambda _seconds: None)
    timestamps = iter(
        [
            "2099-01-01_00-00_30_000000000",
            "2099-01-01_00-00_20_000000000",
            "2099-01-01_00-00_10_000000000",
        ]
    )
    monkeypatch.setattr(runtime_codex_exec, "timestamp", lambda: next(timestamps))
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    calls = tmp_path / "calls.jsonl"
    fake_codex = bin_dir / "codex"
    write_python_executable(
        fake_codex,
        [
            "import json, os, pathlib, sys",
            f"calls = pathlib.Path({str(calls)!r})",
            "args = sys.argv[1:]",
            "stdin = sys.stdin.read()",
            "with calls.open('a') as f: f.write(json.dumps({'args': args, 'stdin': stdin, 'codex_home': os.environ.get('CODEX_HOME')}) + '\\n')",
            "if 'resume' in args:",
            "    output = pathlib.Path(args[args.index('--output-last-message') + 1])",
            "    output.write_text(json.dumps({'ok': True}))",
            "    print(json.dumps({'type': 'turn.completed'}))",
            "    sys.exit(0)",
            "if stdin == 'quota availability probe':",
            "    output = pathlib.Path(args[args.index('--output-last-message') + 1])",
            "    output.write_text(json.dumps({'probe': True}))",
            "    print(json.dumps({'type': 'turn.completed'}))",
            "    sys.exit(0)",
            "print(json.dumps({'type':'thread.started','thread_id':'sess-1'}))",
            "print(json.dumps({'type':'error','message':'Quota exceeded'}))",
            "sys.exit(1)",
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
    logger = SubcommandLogger(root, "test")

    result = run_codex_exec(
        parameter,
        root=root,
        quota_poll_interval_sec=0,
        max_quota_polls=1,
        config=CmocConfig(),
        subcommand_logger=logger,
    )

    call_records = [json.loads(line) for line in calls.read_text().splitlines()]
    argv_calls = [record["args"] for record in call_records]
    assert argv_calls[0][-1] == "-"
    assert all(record["codex_home"] == str(codex_home) for record in call_records)
    assert call_records[1]["stdin"] == "quota availability probe"
    assert argv_calls[1][:2] == ["exec", "--profile"]
    assert argv_calls[1][2].startswith("cmoc_")
    assert "--json" in argv_calls[1]
    assert "--output-last-message" in argv_calls[1]
    assert argv_calls[1][-1] == "-"
    assert "resume" in argv_calls[2]
    assert "sess-1" in argv_calls[2]
    assert result.output_json == {"ok": True}
    call_entries = [
        (path, json.loads(path.read_text()))
        for path in sorted((root / ".cmoc" / "log" / "codex").glob("*_call.json"))
    ]
    call_logs = [log for _path, log in call_entries]
    assert [log["purpose"] for log in call_logs] == [
        "codex exec",
        "quota availability probe",
        "codex exec",
    ]
    probe_logs = [
        log for log in call_logs if log["purpose"] == "quota availability probe"
    ]
    probe_call_path = next(
        path
        for path, log in call_entries
        if log["purpose"] == "quota availability probe"
    )
    assert len(probe_logs) == 1
    assert probe_logs[0]["argv"][1:] == argv_calls[1]
    assert probe_logs[0]["profile_name"] == argv_calls[1][2]
    assert Path(probe_logs[0]["stdout_log_path"]).read_text().strip() == (
        '{"type": "turn.completed"}'
    )
    assert (
        prompt_log_text(probe_logs[0]["prompt_log_path"])
        == "quota availability probe"
    )
    assert Path(probe_logs[0]["stderr_log_path"]).read_text() == ""
    assert Path(probe_logs[0]["output_path"]).read_text() == '{"probe": true}'
    main_entries = [
        (path, log) for path, log in call_entries if log["purpose"] == "codex exec"
    ]
    main_logs = [log for _path, log in main_entries]
    assert len(main_logs) == 2
    assert [log["argv"][1:] for log in main_logs] == [argv_calls[0], argv_calls[2]]
    initial_log = next(log for log in main_logs if "resume" not in log["argv"])
    resume_log = next(log for log in main_logs if "resume" in log["argv"])
    resume_entry = next((path, log) for path, log in main_entries if log is resume_log)
    assert initial_log["argv"][1:] == argv_calls[0]
    assert resume_log["argv"][1:] == argv_calls[2]
    assert len({log["stdout_log_path"] for log in main_logs}) == 2
    assert [prompt_log_text(log["prompt_log_path"]) for log in main_logs] == [
        "prompt",
        "prompt",
    ]
    assert len({log["prompt_log_path"] for log in main_logs}) == 2
    assert Path(initial_log["stdout_log_path"]).read_text().strip() == (
        '{"type": "thread.started", "thread_id": "sess-1"}\n'
        '{"type": "error", "message": "Quota exceeded"}'
    )
    assert Path(resume_log["stdout_log_path"]).read_text().strip() == (
        '{"type": "turn.completed"}'
    )
    assert result.call_log_path == resume_entry[0]
    log_events = [json.loads(line) for line in logger.path.read_text().splitlines()]
    codex_events = [event for event in log_events if event["event"] == "codex_call"]
    assert [event["purpose"] for event in codex_events] == [
        "codex exec",
        "quota availability probe",
        "codex exec",
    ]
    assert [event["status"] for event in codex_events] == [
        "quota_waiting",
        "succeeded",
        "succeeded",
    ]
    assert codex_events[0]["returncode"] == 1
    assert codex_events[0]["stdout_log_path"] == main_logs[0]["stdout_log_path"]
    assert codex_events[0]["prompt_log_path"] == main_logs[0]["prompt_log_path"]
    assert codex_events[0]["output_path"] == main_logs[0]["output_path"]
    assert codex_events[1]["returncode"] == 0
    assert codex_events[1]["stdout_log_path"] == probe_logs[0]["stdout_log_path"]
    assert codex_events[1]["prompt_log_path"] == probe_logs[0]["prompt_log_path"]
    assert codex_events[1]["output_path"] == probe_logs[0]["output_path"]
    console = capsys.readouterr().out
    assert "- purpose: `codex exec`" in console
    assert "- purpose: `quota availability probe`" in console
    assert f"- call_log: `{probe_call_path}`" in console
    assert "- elapsed: `" in console
    assert "- returncode: `0`" in console


def test_run_codex_exec_reruns_after_quota_without_resume_token(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = make_repo(tmp_path)
    setup_codex_home(tmp_path, monkeypatch)
    monkeypatch.setattr(cmoc_runtime.time, "sleep", lambda _seconds: None)
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    calls = tmp_path / "calls.jsonl"
    fake_codex = bin_dir / "codex"
    write_python_executable(
        fake_codex,
        [
            "import json, pathlib, sys",
            f"calls = pathlib.Path({str(calls)!r})",
            "args = sys.argv[1:]",
            "stdin = sys.stdin.read()",
            "records = calls.read_text().splitlines() if calls.exists() else []",
            "with calls.open('a') as f: f.write(json.dumps({'args': args, 'stdin': stdin}) + '\\n')",
            "if stdin == 'quota availability probe':",
            "    output = pathlib.Path(args[args.index('--output-last-message') + 1])",
            "    output.write_text(json.dumps({'probe': True}))",
            "    print(json.dumps({'type': 'turn.completed'}))",
            "    sys.exit(0)",
            "if records:",
            "    output = pathlib.Path(args[args.index('--output-last-message') + 1])",
            "    output.write_text(json.dumps({'ok': True}))",
            "    print(json.dumps({'type': 'turn.completed'}))",
            "    sys.exit(0)",
            "print(json.dumps({'type':'error','message':'Quota exceeded'}))",
            "sys.exit(1)",
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

    result = run_codex_exec(
        parameter,
        root=root,
        quota_poll_interval_sec=0,
        max_quota_polls=1,
        config=CmocConfig(),
    )

    call_records = [json.loads(line) for line in calls.read_text().splitlines()]
    assert [record["stdin"] for record in call_records] == [
        "prompt",
        "quota availability probe",
        "prompt",
    ]
    assert all("resume" not in record["args"] for record in call_records)
    assert result.output_json == {"ok": True}


def test_run_codex_exec_uses_single_representative_quota_probe(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = make_repo(tmp_path)
    setup_codex_home(tmp_path, monkeypatch)
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    calls = tmp_path / "parallel_calls.jsonl"
    fake_codex = bin_dir / "codex"
    write_python_executable(
        fake_codex,
        [
            "import json, pathlib, sys, time",
            f"calls = pathlib.Path({str(calls)!r})",
            "args = sys.argv[1:]",
            "stdin = sys.stdin.read()",
            "kind = 'resume' if 'resume' in args else 'probe' if stdin == 'quota availability probe' else 'initial'",
            "with calls.open('a') as f: f.write(json.dumps({'kind': kind, 'args': args}) + '\\n')",
            "if kind == 'resume':",
            "    output = pathlib.Path(args[args.index('--output-last-message') + 1])",
            "    output.write_text(json.dumps({'ok': True}))",
            "    print(json.dumps({'type': 'turn.completed'}))",
            "    sys.exit(0)",
            "if kind == 'probe':",
            "    output = pathlib.Path(args[args.index('--output-last-message') + 1])",
            "    output.write_text(json.dumps({'probe': True}))",
            "    print(json.dumps({'type': 'turn.completed'}))",
            "    sys.exit(0)",
            "deadline = time.time() + 5",
            "while time.time() < deadline:",
            "    lines = calls.read_text().splitlines() if calls.exists() else []",
            "    if sum(1 for line in lines if json.loads(line)['kind'] == 'initial') >= 2:",
            "        break",
            "    time.sleep(0.01)",
            "print(json.dumps({'type':'thread.started','thread_id':'sess-parallel'}))",
            "print(json.dumps({'type':'error','message':'Quota exceeded'}))",
            "sys.exit(1)",
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

    def call_codex() -> object:
        return run_codex_exec(
            parameter,
            root=root,
            quota_poll_interval_sec=0.05,
            max_quota_polls=1,
            config=CmocConfig(),
        )

    with ThreadPoolExecutor(max_workers=2) as executor:
        results = list(executor.map(lambda _index: call_codex(), range(2)))

    events = [json.loads(line) for line in calls.read_text().splitlines()]
    assert [event["kind"] for event in events].count("initial") == 2
    assert [event["kind"] for event in events].count("probe") == 1
    assert [event["kind"] for event in events].count("resume") == 2
    assert [result.output_json for result in results] == [{"ok": True}, {"ok": True}]
