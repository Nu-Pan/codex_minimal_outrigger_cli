from _support import (
    AgentCallParameter,
    CmocError,
    FileAccessMode,
    ModelClass,
    Path,
    ReasoningEffort,
    SubcommandLogger,
    ThreadPoolExecutor,
    cmoc_runtime,
    json,
    make_repo,
    run_codex_exec,
    setup_codex_home,
)

def test_run_codex_exec_retries_semantic_output(tmp_path: Path, monkeypatch) -> None:
    root = make_repo(tmp_path)
    setup_codex_home(tmp_path, monkeypatch)
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    counter = tmp_path / "counter"
    fake_codex = bin_dir / "codex"
    fake_codex.write_text(
        "\n".join(
            [
                "#!/usr/bin/env python3",
                "import json, pathlib, sys",
                f"counter = pathlib.Path({str(counter)!r})",
                "count = int(counter.read_text()) if counter.exists() else 0",
                "counter.write_text(str(count + 1))",
                "args = sys.argv[1:]",
                "output = pathlib.Path(args[args.index('--output-last-message') + 1])",
                "payload = {'ok': True} if count else {'bad': True}",
                "output.write_text(json.dumps(payload))",
                "print(json.dumps({'type': 'turn.completed'}))",
            ]
        )
        + "\n"
    )
    fake_codex.chmod(0o755)
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
    logger = SubcommandLogger(root, "test")

    result = run_codex_exec(
        parameter,
        root=root,
        capacity_initial_sleep_sec=0,
        subcommand_logger=logger,
    )

    assert result.output_json == {"ok": True}
    assert counter.read_text() == "2"
    call_paths = sorted((root / ".cmoc" / "log" / "codex").glob("*_call.json"))
    call_logs = [json.loads(path.read_text()) for path in call_paths]
    assert len(call_logs) == 2
    assert [Path(log["output_path"]).read_text() for log in call_logs] == [
        '{"bad": true}',
        '{"ok": true}',
    ]
    assert len({log["stdout_log_path"] for log in call_logs}) == 2
    assert result.call_log_path == call_paths[1]
    log_events = [json.loads(line) for line in logger.path.read_text().splitlines()]
    codex_events = [event for event in log_events if event["event"] == "codex_call"]
    assert [event["status"] for event in codex_events] == [
        "schema_validation_retrying",
        "succeeded",
    ]
    assert codex_events[0]["returncode"] == 0
    assert codex_events[0]["call_log_path"] == str(call_paths[0])


def test_run_codex_exec_logs_capacity_retrying_call(
    tmp_path: Path, monkeypatch
) -> None:
    root = make_repo(tmp_path)
    setup_codex_home(tmp_path, monkeypatch)
    monkeypatch.setattr(cmoc_runtime.time, "sleep", lambda _seconds: None)
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    counter = tmp_path / "counter"
    fake_codex = bin_dir / "codex"
    fake_codex.write_text(
        "\n".join(
            [
                "#!/usr/bin/env python3",
                "import json, pathlib, sys",
                f"counter = pathlib.Path({str(counter)!r})",
                "count = int(counter.read_text()) if counter.exists() else 0",
                "counter.write_text(str(count + 1))",
                "args = sys.argv[1:]",
                "output = pathlib.Path(args[args.index('--output-last-message') + 1])",
                "if count == 0:",
                "    print('Selected model is at capacity', file=sys.stderr)",
                "    sys.exit(1)",
                "output.write_text(json.dumps({'ok': True}))",
                "print(json.dumps({'type': 'turn.completed'}))",
            ]
        )
        + "\n"
    )
    fake_codex.chmod(0o755)
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
        capacity_initial_sleep_sec=0,
        subcommand_logger=logger,
    )

    assert result.output_json == {"ok": True}
    call_paths = sorted((root / ".cmoc" / "log" / "codex").glob("*_call.json"))
    log_events = [json.loads(line) for line in logger.path.read_text().splitlines()]
    codex_events = [event for event in log_events if event["event"] == "codex_call"]
    assert [event["status"] for event in codex_events] == [
        "capacity_retrying",
        "succeeded",
    ]
    assert codex_events[0]["returncode"] == 1
    assert codex_events[0]["call_log_path"] == str(call_paths[0])
    assert "Selected model is at capacity" in codex_events[0]["error"]


def test_run_codex_exec_polls_and_resumes_after_quota(
    tmp_path: Path, monkeypatch, capsys
) -> None:
    root = make_repo(tmp_path)
    codex_home = setup_codex_home(tmp_path, monkeypatch)
    monkeypatch.setattr(cmoc_runtime.time, "sleep", lambda _seconds: None)
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    calls = tmp_path / "calls.jsonl"
    fake_codex = bin_dir / "codex"
    fake_codex.write_text(
        "\n".join(
            [
                "#!/usr/bin/env python3",
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
                "print(json.dumps({'type':'error','message':'Quota exceeded','session_id':'sess-1'}))",
                "sys.exit(1)",
            ]
        )
        + "\n"
    )
    fake_codex.chmod(0o755)
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
    assert Path(probe_logs[0]["stderr_log_path"]).read_text() == ""
    assert Path(probe_logs[0]["output_path"]).read_text() == '{"probe": true}'
    main_entries = [
        (path, log) for path, log in call_entries if log["purpose"] == "codex exec"
    ]
    main_logs = [log for _path, log in main_entries]
    assert len(main_logs) == 2
    assert main_logs[0]["argv"][1:] == argv_calls[0]
    assert "resume" not in main_logs[0]["argv"]
    assert main_logs[1]["argv"][1:] == argv_calls[2]
    assert "resume" in main_logs[1]["argv"]
    assert len({log["stdout_log_path"] for log in main_logs}) == 2
    assert Path(main_logs[0]["stdout_log_path"]).read_text().strip() == (
        '{"type": "error", "message": "Quota exceeded", "session_id": "sess-1"}'
    )
    assert Path(main_logs[1]["stdout_log_path"]).read_text().strip() == (
        '{"type": "turn.completed"}'
    )
    assert result.call_log_path == main_entries[1][0]
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
    assert codex_events[0]["output_path"] == main_logs[0]["output_path"]
    assert codex_events[1]["returncode"] == 0
    assert codex_events[1]["stdout_log_path"] == probe_logs[0]["stdout_log_path"]
    assert codex_events[1]["output_path"] == probe_logs[0]["output_path"]
    console = capsys.readouterr().out
    assert "- purpose: `codex exec`" in console
    assert "- purpose: `quota availability probe`" in console
    assert f"- call_log: `{probe_call_path}`" in console
    assert "- elapsed: `" in console
    assert "- returncode: `0`" in console


def test_run_codex_exec_fails_after_quota_without_resume_token(
    tmp_path: Path, monkeypatch
) -> None:
    root = make_repo(tmp_path)
    setup_codex_home(tmp_path, monkeypatch)
    monkeypatch.setattr(cmoc_runtime.time, "sleep", lambda _seconds: None)
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    calls = tmp_path / "calls.jsonl"
    fake_codex = bin_dir / "codex"
    fake_codex.write_text(
        "\n".join(
            [
                "#!/usr/bin/env python3",
                "import json, pathlib, sys",
                f"calls = pathlib.Path({str(calls)!r})",
                "args = sys.argv[1:]",
                "stdin = sys.stdin.read()",
                "with calls.open('a') as f: f.write(json.dumps({'args': args, 'stdin': stdin}) + '\\n')",
                "if stdin == 'quota availability probe':",
                "    output = pathlib.Path(args[args.index('--output-last-message') + 1])",
                "    output.write_text(json.dumps({'probe': True}))",
                "    print(json.dumps({'type': 'turn.completed'}))",
                "    sys.exit(0)",
                "print(json.dumps({'type':'error','message':'Quota exceeded'}))",
                "sys.exit(1)",
            ]
        )
        + "\n"
    )
    fake_codex.chmod(0o755)
    monkeypatch.setenv("PATH", f"{bin_dir}:{Path('/usr/bin')}")
    parameter = AgentCallParameter(
        ModelClass.EFFICIENCY,
        ReasoningEffort.LOW,
        FileAccessMode.READONLY,
        "prompt",
        None,
    )

    try:
        run_codex_exec(
            parameter,
            root=root,
            quota_poll_interval_sec=0,
            max_quota_polls=1,
        )
    except CmocError as exc:
        assert "resume token" in exc.summary
    else:
        raise AssertionError("run_codex_exec should fail without resume token")

    call_records = [json.loads(line) for line in calls.read_text().splitlines()]
    assert [record["stdin"] for record in call_records] == [
        "prompt",
        "quota availability probe",
    ]
    assert all("resume" not in record["args"] for record in call_records)


def test_run_codex_exec_uses_single_representative_quota_probe(
    tmp_path: Path, monkeypatch
) -> None:
    root = make_repo(tmp_path)
    setup_codex_home(tmp_path, monkeypatch)
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    calls = tmp_path / "parallel_calls.jsonl"
    fake_codex = bin_dir / "codex"
    fake_codex.write_text(
        "\n".join(
            [
                "#!/usr/bin/env python3",
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
                "print(json.dumps({'type':'error','message':'Quota exceeded','session_id':'sess-parallel'}))",
                "sys.exit(1)",
            ]
        )
        + "\n"
    )
    fake_codex.chmod(0o755)
    monkeypatch.setenv("PATH", f"{bin_dir}:{Path('/usr/bin')}")
    parameter = AgentCallParameter(
        ModelClass.EFFICIENCY,
        ReasoningEffort.LOW,
        FileAccessMode.READONLY,
        "prompt",
        None,
    )

    def call_codex():
        return run_codex_exec(
            parameter,
            root=root,
            quota_poll_interval_sec=0.05,
            max_quota_polls=1,
        )

    with ThreadPoolExecutor(max_workers=2) as executor:
        results = list(executor.map(lambda _index: call_codex(), range(2)))

    events = [json.loads(line) for line in calls.read_text().splitlines()]
    assert [event["kind"] for event in events].count("initial") == 2
    assert [event["kind"] for event in events].count("probe") == 1
    assert [event["kind"] for event in events].count("resume") == 2
    assert [result.output_json for result in results] == [{"ok": True}, {"ok": True}]
