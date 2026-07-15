"""Codex exec の再試行と失敗時ログを検証する。

Structured Output の意味的失敗、capacity retry、JSONL error、中断、差分保持を
外部挙動として確認する。根拠は次の正本仕様断片にある。

このファイルは `run_codex_exec` の retry 状態、subprocess の呼び出し回数、call log、
subcommand event を同時に確認する一つの責務を持つ。semantic failure、capacity failure、
未知の JSONL error、中断は同じ状態機械の分岐であり、各テストは fake の応答から最終結果と
ログ列までを一続きの外部挙動として検証する。したがって、16,000 文字を超えても異常系を
別ファイルへ分けず、retry 状態と共有ログ schema を同じ読み取り文脈に保つ。

- {{work-root}}/oracle/doc/app_spec/codex_exec_rule.md
- {{work-root}}/oracle/doc/app_spec/console_and_file_log.md
- {{work-root}}/oracle/doc/dev_rule/coding_rule.md
- {{work-root}}/oracle/src/oracle/prompt_builder/parts/realization_standard.py
"""

import json
from pathlib import Path

import pytest
from _codex_support import setup_codex_home, stub_codex_overrides
from _command_support import write_python_executable
from _git_support import make_repo

import cmoc_runtime
import commons.runtime_codex_exec as runtime_codex_exec
from basic.acp import AgentCallParameter, FileAccessMode, ModelClass, ReasoningEffort
from cmoc_runtime import CmocError, SubcommandLogger
from commons.runtime_codex import run_codex_exec
from config.cmoc_config import CmocConfig


def test_run_codex_exec_retries_semantic_output(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Structured Output の意味的失敗を一度だけ再試行し、各ログを保存する。"""
    root = make_repo(tmp_path)
    setup_codex_home(tmp_path, monkeypatch)
    stub_codex_overrides(monkeypatch)
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
    call_paths = sorted(
        (root / ".cmoc" / "gu" / "ar" / "log" / "codex").glob("*_call.json")
    )
    call_logs = [json.loads(path.read_text()) for path in call_paths]
    assert len(call_logs) == 2
    assert [Path(log["output_path"]).read_text() for log in call_logs] == [
        '{"bad": true}',
        '{"ok": true}',
    ]
    assert [Path(log["prompt_log_path"]).read_text() for log in call_logs] == [
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


def test_run_codex_exec_logs_keyboard_interrupt(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """KeyboardInterrupt を failed call event として記録し、例外を伝播する。"""
    root = make_repo(tmp_path)
    setup_codex_home(tmp_path, monkeypatch)
    stub_codex_overrides(monkeypatch)

    def interrupt(*_args: object, **_kwargs: object) -> object:
        """Codex subprocess 呼び出しを KeyboardInterrupt で中断する fake。"""
        raise KeyboardInterrupt

    monkeypatch.setattr(runtime_codex_exec, "run_codex_subprocess", interrupt)
    logger = SubcommandLogger(root, "test")

    with pytest.raises(KeyboardInterrupt):
        run_codex_exec(
            AgentCallParameter(
                ModelClass.EFFICIENCY,
                ReasoningEffort.LOW,
                FileAccessMode.READONLY,
                "prompt",
                None,
            ),
            root=root,
            config=CmocConfig(),
            subcommand_logger=logger,
        )

    console = capsys.readouterr().out
    assert "- Exit code: `not started`" in console
    assert "- Error: `KeyboardInterrupt()`" in console
    call_logs = list(
        (root / ".cmoc" / "gu" / "ar" / "log" / "codex").glob("*_call.json")
    )
    events = [json.loads(line) for line in logger.path.read_text().splitlines()]
    codex_events = [event for event in events if event["event"] == "codex_call"]
    assert len(call_logs) == 1
    assert len(codex_events) == 1
    assert codex_events[0]["status"] == "failed"
    assert codex_events[0]["returncode"] is None
    assert codex_events[0]["error"] == "KeyboardInterrupt()"


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
    """Structured Output の欠落・空・不正 JSON を再試行し、失敗理由を記録する。"""
    root = make_repo(tmp_path)
    setup_codex_home(tmp_path, monkeypatch)
    stub_codex_overrides(monkeypatch)
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


@pytest.mark.parametrize("failure_returncode", [0, 1])
def test_run_codex_exec_logs_capacity_retrying_call(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, failure_returncode: int
) -> None:
    """capacity error を再試行し、戻り値に依存せず retry event を記録する。"""
    root = make_repo(tmp_path)
    setup_codex_home(tmp_path, monkeypatch)
    stub_codex_overrides(monkeypatch)
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
            f"    sys.exit({failure_returncode})",
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
    call_paths = sorted(
        (root / ".cmoc" / "gu" / "ar" / "log" / "codex").glob("*_call.json")
    )
    log_events = [json.loads(line) for line in logger.path.read_text().splitlines()]
    codex_events = [event for event in log_events if event["event"] == "codex_call"]
    assert [event["status"] for event in codex_events] == [
        "capacity_retrying",
        "succeeded",
    ]
    assert codex_events[0]["returncode"] == failure_returncode
    assert codex_events[0]["call_log_path"] == str(call_paths[0])
    assert "Selected model is at capacity" in codex_events[0]["error"]


@pytest.mark.parametrize(
    "event",
    [
        {"type": "error", "message": "unexpected failure"},
        {"type": "turn.failed", "error": {"message": "unexpected failure"}},
    ],
)
@pytest.mark.parametrize("structured_output", [False, True])
def test_run_codex_exec_fails_on_unknown_jsonl_error_with_zero_returncode(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    event: dict[str, object],
    structured_output: bool,
) -> None:
    """未知の JSONL error は終了コード 0 でも即時失敗させ、再試行しない。"""
    root = make_repo(tmp_path)
    setup_codex_home(tmp_path, monkeypatch)
    stub_codex_overrides(monkeypatch)
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    counter = tmp_path / "counter"
    fake_codex = bin_dir / "codex"
    event_text = json.dumps(event)
    write_python_executable(
        fake_codex,
        [
            "import json, pathlib, sys",
            f"counter = pathlib.Path({str(counter)!r})",
            "count = int(counter.read_text()) if counter.exists() else 0",
            "counter.write_text(str(count + 1))",
            "args = sys.argv[1:]",
            "output = pathlib.Path(args[args.index('--output-last-message') + 1])",
            "output.write_text(json.dumps({'ok': True}))",
            f"print({event_text!r})",
        ],
    )
    monkeypatch.setenv("PATH", f"{bin_dir}:{Path('/usr/bin')}")
    schema: Path | None = None
    if structured_output:
        schema = tmp_path / "schema.json"
        schema.write_text("{}")
    logger = SubcommandLogger(root, "test")

    with pytest.raises(CmocError, match="Codex CLI 呼び出しが失敗しました") as error:
        run_codex_exec(
            AgentCallParameter(
                ModelClass.EFFICIENCY,
                ReasoningEffort.LOW,
                FileAccessMode.READONLY,
                "prompt",
                schema,
            ),
            root=root,
            config=CmocConfig(),
            subcommand_logger=logger,
        )

    assert "unexpected failure" not in error.value.detail
    assert counter.read_text() == "1"
    log_events = [json.loads(line) for line in logger.path.read_text().splitlines()]
    codex_events = [event for event in log_events if event["event"] == "codex_call"]
    assert [event["status"] for event in codex_events] == ["failed"]
    assert codex_events[0]["returncode"] == 0
    assert "unexpected failure" in codex_events[0]["error"]


def test_run_codex_exec_keeps_agent_diff_after_capacity_retry(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """capacity retry を挟んでも Codex が作った agent diff を保持する。"""
    root = make_repo(tmp_path)
    setup_codex_home(tmp_path, monkeypatch)
    stub_codex_overrides(monkeypatch)
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
            "blocked = pathlib.Path('oracle/blocked.md')",
            "if count == 0:",
            "    blocked.write_text('blocked\\n')",
            (
                "    print(json.dumps({'type': 'error', "
                "'message': 'Selected model is at capacity'}))"
            ),
            "    sys.exit(1)",
            "output.write_text(json.dumps({'ok': True}) + '\\n')",
            "print(json.dumps({'type': 'turn.completed'}))",
        ],
    )
    monkeypatch.setenv("PATH", f"{bin_dir}:{Path('/usr/bin')}")

    run_codex_exec(
        AgentCallParameter(
            ModelClass.EFFICIENCY,
            ReasoningEffort.LOW,
            FileAccessMode.REALIZATION_WRITE,
            "prompt",
            None,
        ),
        root=root,
        capacity_initial_sleep_sec=0,
        config=CmocConfig(),
    )

    assert counter.read_text() == "2"
    assert (root / "oracle" / "blocked.md").read_text() == "blocked\n"


def test_run_codex_exec_ignores_error_markers_outside_stdout_jsonl(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """stdout JSONL 外の error marker を retry 判定に使わず、直接失敗させる。"""
    root = make_repo(tmp_path)
    setup_codex_home(tmp_path, monkeypatch)
    stub_codex_overrides(monkeypatch)
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
            assert expected_detail not in exc.detail
            assert expected_detail not in capsys.readouterr().out
        else:
            raise AssertionError(f"{name} marker outside JSONL should fail directly")
        assert counter.read_text() == "1"


@pytest.mark.parametrize(
    (
        "failure",
        "expected_calls",
        "expected_statuses",
        "expected_sleeps",
        "summary",
        "error_fragment",
    ),
    [
        (
            "semantic",
            3,
            ["schema_validation_retrying"] * 2 + ["schema_validation_failed"],
            [],
            "Codex CLI の Structured Output 検証に失敗しました。",
            "Additional properties",
        ),
        (
            "capacity",
            9,
            ["capacity_retrying"] * 8 + ["failed"],
            [5 * 2**attempt for attempt in range(8)],
            "Codex CLI 呼び出しが失敗しました。",
            "Selected model is at capacity",
        ),
    ],
)
def test_run_codex_exec_stops_after_retry_limit(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    failure: str,
    expected_calls: int,
    expected_statuses: list[str],
    expected_sleeps: list[int],
    summary: str,
    error_fragment: str,
) -> None:
    """永続失敗が retry 上限、backoff、最終 failure event を越えて続かない。"""
    root = make_repo(tmp_path)
    setup_codex_home(tmp_path, monkeypatch)
    stub_codex_overrides(monkeypatch)
    sleep_calls: list[float] = []
    monkeypatch.setattr(
        runtime_codex_exec.time, "sleep", lambda seconds: sleep_calls.append(seconds)
    )
    bin_dir = tmp_path / f"{failure}_bin"
    bin_dir.mkdir()
    counter = tmp_path / f"{failure}_counter"
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
            f"failure = {failure!r}",
            "if failure == 'semantic':",
            "    output.write_text(json.dumps({'bad': True}))",
            "    print(json.dumps({'type': 'turn.completed'}))",
            "else:",
            (
                "    print(json.dumps({'type': 'error', "
                "'message': 'Selected model is at capacity'}))"
            ),
            "    sys.exit(1)",
        ],
    )
    monkeypatch.setenv("PATH", f"{bin_dir}:{Path('/usr/bin')}")
    schema: Path | None = None
    if failure == "semantic":
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
    logger = SubcommandLogger(root, "test")

    with pytest.raises(CmocError, match=summary) as error:
        run_codex_exec(
            AgentCallParameter(
                ModelClass.EFFICIENCY,
                ReasoningEffort.LOW,
                FileAccessMode.READONLY,
                "prompt",
                schema,
            ),
            root=root,
            config=CmocConfig(),
            subcommand_logger=logger,
        )

    assert counter.read_text() == str(expected_calls)
    assert sleep_calls == expected_sleeps
    assert error.value.summary == summary
    if failure == "semantic":
        assert error_fragment in error.value.detail
    else:
        assert error_fragment not in error.value.detail
    call_paths = sorted(
        (root / ".cmoc" / "gu" / "ar" / "log" / "codex").glob("*_call.json")
    )
    assert len(call_paths) == expected_calls
    log_events = [json.loads(line) for line in logger.path.read_text().splitlines()]
    codex_events = [event for event in log_events if event["event"] == "codex_call"]
    assert [event["status"] for event in codex_events] == expected_statuses
    assert [event["call_log_path"] for event in codex_events] == [
        str(path) for path in call_paths
    ]
