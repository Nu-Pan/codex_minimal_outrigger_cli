import json
from pathlib import Path

import cmoc_runtime
from basic.acp import AgentCallParameter, FileAccessMode, ModelClass, ReasoningEffort
from cmoc_runtime import CmocError, SubcommandLogger
from config.cmoc_config import CmocConfig
import pytest

from _support import (
    make_repo,
    setup_codex_home,
    stub_codex_profile,
    write_python_executable,
)
from commons.runtime_codex import run_codex_exec


def prompt_log_text(path: str) -> str:
    return Path(path).read_text()


def test_run_codex_exec_retries_semantic_output(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = make_repo(tmp_path)
    setup_codex_home(tmp_path, monkeypatch)
    stub_codex_profile(tmp_path, monkeypatch)
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    counter = tmp_path / "counter"
    fake_codex = bin_dir / "codex"
    write_python_executable(
        fake_codex,
        [
            "import json, pathlib, sys",
            f"counter = pathlib.Path({str(counter)!r})",
            "count = int(counter.read_text()) if counter.exists() else 0",
            "counter.write_text(str(count + 1))",
            "args = sys.argv[1:]",
            "output = pathlib.Path(args[args.index('--output-last-message') + 1])",
            "payload = {'ok': True} if count else {'bad': True}",
            "output.write_text(json.dumps(payload))",
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
    logger = SubcommandLogger(root, "test")

    result = run_codex_exec(
        parameter,
        root=root,
        capacity_initial_sleep_sec=0,
        config=CmocConfig(),
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
    assert [prompt_log_text(log["prompt_log_path"]) for log in call_logs] == [
        "prompt",
        "prompt",
    ]
    assert len({log["stdout_log_path"] for log in call_logs}) == 2
    assert len({log["prompt_log_path"] for log in call_logs}) == 2
    assert result.call_log_path == call_paths[1]
    log_events = [json.loads(line) for line in logger.path.read_text().splitlines()]
    codex_events = [event for event in log_events if event["event"] == "codex_call"]
    assert [event["status"] for event in codex_events] == [
        "schema_validation_retrying",
        "succeeded",
    ]
    assert codex_events[0]["returncode"] == 0
    assert codex_events[0]["call_log_path"] == str(call_paths[0])


@pytest.mark.parametrize(
    ("name", "first_output_lines", "expected_error"),
    [
        ("missing", [], "does not exist"),
        ("empty", ["output.write_text('')"], "is empty"),
        ("malformed", ["output.write_text('{')"], "is not valid JSON"),
    ],
)
def test_run_codex_exec_retries_structured_output_parse_failure(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    name: str,
    first_output_lines: list[str],
    expected_error: str,
) -> None:
    root = make_repo(tmp_path)
    setup_codex_home(tmp_path, monkeypatch)
    stub_codex_profile(tmp_path, monkeypatch)
    bin_dir = tmp_path / f"{name}_bin"
    bin_dir.mkdir()
    counter = tmp_path / f"{name}_counter"
    fake_codex = bin_dir / "codex"
    write_python_executable(
        fake_codex,
        [
            "import json, pathlib, sys",
            f"counter = pathlib.Path({str(counter)!r})",
            "count = int(counter.read_text()) if counter.exists() else 0",
            "counter.write_text(str(count + 1))",
            "args = sys.argv[1:]",
            "output = pathlib.Path(args[args.index('--output-last-message') + 1])",
            "if count == 0:",
            *([f"    {line}" for line in first_output_lines] or ["    pass"]),
            "else:",
            "    output.write_text(json.dumps({'ok': True}))",
            "print(json.dumps({'type': 'turn.completed'}))",
        ],
    )
    monkeypatch.setenv("PATH", f"{bin_dir}:{Path('/usr/bin')}")
    schema = tmp_path / f"{name}_schema.json"
    schema.write_text("{}")
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
        config=CmocConfig(),
        subcommand_logger=logger,
    )

    assert result.output_json == {"ok": True}
    assert counter.read_text() == "2"
    log_events = [json.loads(line) for line in logger.path.read_text().splitlines()]
    codex_events = [event for event in log_events if event["event"] == "codex_call"]
    assert [event["status"] for event in codex_events] == [
        "schema_validation_retrying",
        "succeeded",
    ]
    assert expected_error in codex_events[0]["error"]


def test_run_codex_exec_logs_capacity_retrying_call(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = make_repo(tmp_path)
    setup_codex_home(tmp_path, monkeypatch)
    stub_codex_profile(tmp_path, monkeypatch)
    monkeypatch.setattr(cmoc_runtime.time, "sleep", lambda _seconds: None)
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    counter = tmp_path / "counter"
    fake_codex = bin_dir / "codex"
    write_python_executable(
        fake_codex,
        [
            "import json, pathlib, sys",
            f"counter = pathlib.Path({str(counter)!r})",
            "count = int(counter.read_text()) if counter.exists() else 0",
            "counter.write_text(str(count + 1))",
            "args = sys.argv[1:]",
            "output = pathlib.Path(args[args.index('--output-last-message') + 1])",
            "if count == 0:",
            (
                "    print(json.dumps({'type': 'error', "
                "'message': 'Selected model is at capacity'}))"
            ),
            "    sys.exit(1)",
            "output.write_text(json.dumps({'ok': True}))",
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
    logger = SubcommandLogger(root, "test")

    result = run_codex_exec(
        parameter,
        root=root,
        capacity_initial_sleep_sec=0,
        config=CmocConfig(),
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


def test_run_codex_exec_ignores_error_markers_outside_stdout_jsonl(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = make_repo(tmp_path)
    setup_codex_home(tmp_path, monkeypatch)
    stub_codex_profile(tmp_path, monkeypatch)
    monkeypatch.setattr(cmoc_runtime.time, "sleep", lambda _seconds: None)
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    fake_codex = bin_dir / "codex"
    monkeypatch.setenv("PATH", f"{bin_dir}:{Path('/usr/bin')}")
    parameter = AgentCallParameter(
        ModelClass.EFFICIENCY,
        ReasoningEffort.LOW,
        FileAccessMode.READONLY,
        "prompt",
        None,
    )
    cases = [
        (
            "capacity",
            ["print('Selected model is at capacity', file=sys.stderr)"],
            {"capacity_initial_sleep_sec": 0, "max_capacity_retries": 1},
            "Selected model is at capacity",
        ),
        (
            "quota",
            ["print('Quota exceeded')", "print('Quota exceeded', file=sys.stderr)"],
            {"quota_poll_interval_sec": 0, "max_quota_polls": 1},
            "Quota exceeded",
        ),
    ]
    for name, marker_lines, kwargs, expected_detail in cases:
        counter = tmp_path / f"{name}_counter"
        write_python_executable(
            fake_codex,
            [
                "import pathlib, sys",
                f"counter = pathlib.Path({str(counter)!r})",
                "count = int(counter.read_text()) if counter.exists() else 0",
                "counter.write_text(str(count + 1))",
                *marker_lines,
                "sys.exit(1)",
            ],
        )
        try:
            run_codex_exec(parameter, root=root, config=CmocConfig(), **kwargs)
        except CmocError as exc:
            assert exc.summary == "Codex CLI 呼び出しが失敗しました。"
            assert expected_detail in exc.detail
        else:
            raise AssertionError(f"{name} marker outside JSONL should fail directly")
        assert counter.read_text() == "1"
